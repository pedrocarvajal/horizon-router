import logging
import time
from datetime import datetime
import pytz

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
    chrome_options.add_argument("--window-size=1000,1080")
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


def scrape_events_for_date(date_str):
    url = f"https://www.forexfactory.com/calendar?day={date_str}"
    driver = setup_chrome_driver()

    try:
        logger.info(f"Loading URL: {url}")
        driver.get(url)

        wait = WebDriverWait(driver, 20)
        wait.until(EC.presence_of_element_located((By.CLASS_NAME, "calendar__table")))
        time.sleep(3)

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

        return events

    except TimeoutException:
        logger.error(f"Timeout loading page: {url}")
        return []
    except Exception as e:
        logger.error(f"Error scraping Forex Factory for {date_str}: {str(e)}")
        return []
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
    }

    validator = Validator(schema)
    date = request.GET.get("date", "")

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
        events = scrape_events_for_date(forex_date_str)
        events = convert_events_to_utc(events, date)

        return response(
            message="Forex events retrieved successfully",
            data={
                "date": date,
                "events_count": len(events),
                "events": events,
            },
        )

    except ValueError as e:
        logger.error(f"Date validation error: {e}")
        return response(message="Invalid date format", status_code=400)
    except Exception as e:
        logger.error(f"Error getting forex events for {date}: {e}")
        return response(message="Internal server error", status_code=500)
