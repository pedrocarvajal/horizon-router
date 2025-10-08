import logging
import time
import os
from datetime import datetime
import pytz

from django.conf import settings
from rest_framework.decorators import api_view
from cerberus import Validator
from core.helpers.response import response
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException

logger = logging.getLogger("horizon")


def convert_events_to_utc(events, source_date):
    gmt_plus_2 = pytz.timezone("Europe/Berlin")
    utc = pytz.UTC

    for event in events:
        if event.get("time") and event.get("time").strip():
            try:
                time_str = event["time"].strip()
                if time_str.lower() in ["all day", "tentative", ""]:
                    continue

                time_parts = time_str.replace("am", " AM").replace("pm", " PM")

                datetime_str = f"{source_date} {time_parts}"
                naive_datetime = datetime.strptime(datetime_str, "%Y-%m-%d %I:%M %p")

                gmt2_datetime = gmt_plus_2.localize(naive_datetime)
                utc_datetime = gmt2_datetime.astimezone(utc)

                event["date"] = utc_datetime.strftime("%Y-%m-%d")
                event["time"] = utc_datetime.strftime("%H:%M")
                event["timezone"] = "UTC"

            except (ValueError, AttributeError) as e:
                logger.warning(
                    f"Could not convert time '{event.get('time')}' for event: {e}"
                )
                continue

    return events


def setup_chrome_driver():
    chrome_options = Options()
    chrome_options.add_argument("--headless=new")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    chrome_options.add_argument("--disable-extensions")
    chrome_options.add_argument("--window-size=1000,1000")
    chrome_options.add_argument(
        "--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    )
    chrome_options.add_argument("--lang=en-US")

    chrome_options.add_experimental_option(
        "prefs",
        {
            "profile.default_content_setting_values.geolocation": 2,
            "intl.accept_languages": "en-US,en",
        },
    )

    selenium_url = "http://horizon-router-selenium-chrome:4444/wd/hub"
    logger.info(f"Using Docker Selenium at: {selenium_url}")
    return webdriver.Remote(command_executor=selenium_url, options=chrome_options)


def scrape_events_for_date(date_str, save_screenshot=False):
    url = f"https://www.forexfactory.com/calendar?day={date_str}"
    driver = setup_chrome_driver()
    screenshot_path = None

    try:
        logger.info(f"Loading URL: {url}")
        driver.get(url)

        wait = WebDriverWait(driver, 20)
        wait.until(EC.presence_of_element_located((By.CLASS_NAME, "calendar__table")))
        time.sleep(3)

        if save_screenshot:
            try:
                calendar_div = driver.find_element(
                    By.CSS_SELECTOR, 'div[data-id="calendar"]'
                )

                screenshot_dir = os.path.join(
                    settings.BASE_DIR, "core", "storage", "screenshots"
                )
                os.makedirs(screenshot_dir, exist_ok=True)

                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                screenshot_filename = f"forexfactory_{date_str}_{timestamp}.png"
                screenshot_path = os.path.join(screenshot_dir, screenshot_filename)
                calendar_div.screenshot(screenshot_path)

                logger.info(f"Calendar screenshot saved: {screenshot_path}")
            except Exception as e:
                logger.warning(f"Failed to capture calendar screenshot: {e}")
                screenshot_path = None

        events = []
        calendar_rows = driver.find_elements(By.CSS_SELECTOR, "tr[data-event-id]")
        logger.info(f"Found {len(calendar_rows)} event rows for {date_str}")

        current_date = None

        for row in calendar_rows:
            event = {}

            try:
                date_cell = row.find_element(
                    By.CSS_SELECTOR, "td.calendar__date span.date"
                )
                if date_cell:
                    current_date = date_cell.text.strip()
            except NoSuchElementException:
                pass

            event["date"] = current_date if current_date else ""

            try:
                time_cell = row.find_element(By.CSS_SELECTOR, "td.calendar__time")
                time_str = time_cell.text.strip()
                event["time"] = time_str
            except NoSuchElementException:
                event["time"] = ""

            try:
                currency_cell = row.find_element(
                    By.CSS_SELECTOR, "td.calendar__currency span"
                )
                event["currency"] = currency_cell.text.strip()
            except NoSuchElementException:
                event["currency"] = ""

            try:
                impact_cell = row.find_element(
                    By.CSS_SELECTOR, "td.calendar__impact span.icon"
                )
                impact_class = impact_cell.get_attribute("class")
                if "icon--ff-impact-red" in impact_class:
                    event["impact"] = "High"
                elif "icon--ff-impact-ora" in impact_class:
                    event["impact"] = "Medium"
                elif "icon--ff-impact-yel" in impact_class:
                    event["impact"] = "Low"
                elif "icon--ff-impact-gra" in impact_class:
                    event["impact"] = "Non-Economic"
                else:
                    impact_title = impact_cell.get_attribute("title")
                    if impact_title:
                        if "High Impact" in impact_title:
                            event["impact"] = "High"
                        elif "Medium Impact" in impact_title:
                            event["impact"] = "Medium"
                        elif "Low Impact" in impact_title:
                            event["impact"] = "Low"
                        elif "Non-Economic" in impact_title:
                            event["impact"] = "Non-Economic"
                        else:
                            event["impact"] = impact_title
                    else:
                        event["impact"] = ""
            except NoSuchElementException:
                event["impact"] = ""

            try:
                actual_cell = row.find_element(By.CSS_SELECTOR, "td.calendar__actual")
                actual_spans = actual_cell.find_elements(By.TAG_NAME, "span")
                has_actual_data = any(
                    span.text.strip() for span in actual_spans if span.text.strip()
                )
                if has_actual_data:
                    continue
            except NoSuchElementException:
                pass

            if event["impact"] not in ["High", "Medium", "Low"]:
                continue

            try:
                detail_cell = row.find_element(
                    By.CSS_SELECTOR, "td.calendar__event span.calendar__event-title"
                )
                event["detail"] = detail_cell.text.strip()
            except NoSuchElementException:
                event["detail"] = ""

            if event.get("detail"):
                events.append(event)

        return events, screenshot_path

    except TimeoutException:
        logger.error(f"Timeout loading page: {url}")
        return [], None
    except Exception as e:
        logger.error(f"Error scraping Forex Factory for {date_str}: {str(e)}")
        return [], None
    finally:
        driver.quit()


@api_view(["GET"])
def get_forex_events(request):
    schema = {
        "date": {
            "type": "string",
            "required": True,
            "empty": False,
            "regex": r"^\d{4}-\d{2}-\d{2}$",
        },
        "screenshot": {
            "type": "boolean",
            "required": False,
            "default": False,
        },
    }

    validator = Validator(schema)
    date = request.GET.get("date", "")
    screenshot = request.GET.get("screenshot", "false").lower() in ("true", "1", "yes")

    if not validator.validate(
        {
            "date": date,
        }
    ):
        return response(
            message="Validation failed", data=validator.errors, status_code=400
        )

    try:
        parsed_date = datetime.strptime(date, "%Y-%m-%d")
        forex_date_str = parsed_date.strftime("%b%d.%Y").lower()
        events, screenshot_path = scrape_events_for_date(
            forex_date_str, save_screenshot=screenshot
        )
        events = convert_events_to_utc(events, date)

        response_data = {
            "date": date,
            "events_count": len(events),
            "events": events,
        }

        if screenshot_path:
            screenshot_filename = os.path.basename(screenshot_path)
            response_data["screenshot_url"] = (
                f"/media/screenshots/{screenshot_filename}"
            )
            response_data["screenshot_path"] = screenshot_path

        return response(
            message="Forex events retrieved successfully",
            data=response_data,
        )

    except ValueError as e:
        logger.error(f"Date validation error: {e}")
        return response(message="Invalid date format", status_code=400)
    except Exception as e:
        logger.error(f"Error getting forex events for {date}: {e}")
        return response(message="Internal server error", status_code=500)
