from django.test import SimpleTestCase
from django.conf import settings
import requests


class HealthControllerE2ETest(SimpleTestCase):
    def setUp(self):
        self.base_url = f"http://127.0.0.1:{settings.EXT_PORT_APP}"
        self.headers = {settings.API_KEY_HEADER_NAME: settings.API_KEY_SECRET}

    def test_health_endpoint_returns_ok_status(self):
        """Test that health endpoint returns 200 status and correct response structure"""
        url = f"{self.base_url}/api/health/"

        response = requests.get(url, headers=self.headers)

        self.assertEqual(response.status_code, 200)

        response_data = response.json()
        self.assertEqual(response_data["status"], "OK")
        self.assertEqual(response_data["message"], "Service is healthy")

        self.assertIsInstance(response_data, dict)
        self.assertIn("status", response_data)
        self.assertIn("message", response_data)
