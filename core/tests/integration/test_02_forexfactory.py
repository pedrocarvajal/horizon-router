from django.test import SimpleTestCase
from core.tests.e2e.helpers.request import request


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
