from django.test import SimpleTestCase
from core.tests.e2e.helpers.request import request


class HealthControllerE2ETest(SimpleTestCase):
    def test_health_endpoint_returns_ok_status(self):
        """Test that health endpoint returns 200 status and correct response structure"""
        status, response_data = request(
            method="GET",
            endpoint="/api/health/",
        )

        self.assertEqual(status, 200)
        self.assertEqual(response_data["status"], "OK")
        self.assertEqual(response_data["message"], "Service is healthy")

        self.assertIsInstance(response_data, dict)
        self.assertIn("status", response_data)
        self.assertIn("message", response_data)
