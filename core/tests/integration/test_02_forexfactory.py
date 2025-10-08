from django.test import SimpleTestCase
from core.tests.e2e.helpers.request import request
import os


class ForexFactoryIntegrationTest(SimpleTestCase):
    def test_forexfactory_endpoint_success(self):
        status, response_data = request(
            method="GET",
            endpoint="/api/forexfactory/events/",
            payload={"date": "2025-01-15"},
        )

        self.assertEqual(status, 200)

        data = response_data.get("data", {})
        events = data.get("events", [])
        self.assertGreater(len(events), 0)

    def test_forexfactory_endpoint_with_screenshot(self):
        status, response_data = request(
            method="GET",
            endpoint="/api/forexfactory/events/",
            payload={"date": "2025-01-15", "screenshot": "true"},
        )

        self.assertEqual(status, 200)

        data = response_data.get("data", {})
        events = data.get("events", [])
        self.assertGreater(len(events), 0)

        print(f"\n\nResponse data keys: {data.keys()}")
        print(f"Events count: {len(events)}")

        self.assertIn("screenshot_path", data, "screenshot_path should be in response")
        self.assertIn("screenshot_url", data, "screenshot_url should be in response")

        screenshot_path = data.get("screenshot_path")
        screenshot_url = data.get("screenshot_url")

        print(f"Screenshot path: {screenshot_path}")
        print(f"Screenshot URL: {screenshot_url}")

        self.assertIsNotNone(screenshot_path, "Screenshot path should not be None")
        self.assertTrue(
            os.path.exists(screenshot_path),
            f"Screenshot file should exist at {screenshot_path}",
        )

        file_size = os.path.getsize(screenshot_path)
        print(f"Screenshot file size: {file_size} bytes")
        self.assertGreater(file_size, 0, "Screenshot file should not be empty")
