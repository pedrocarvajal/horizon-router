from django.test import SimpleTestCase
from core.tests.e2e.helpers.request import request
from core.tests.e2e.helpers.create_test_account import create_test_account
from core.tests.e2e.helpers.create_test_strategy import create_test_strategy


class HeartbeatControllerE2ETest(SimpleTestCase):
    def test_create_heartbeat_success(self):
        account_id = create_test_account(
            name="Heartbeat Test Account",
            broker_account_number="HB123456789",
            broker_name="Heartbeat Test Broker",
        )

        strategy_id = create_test_strategy(
            name="Heartbeat Test Strategy",
            prefix="HB",
            symbol="EURUSD",
        )

        heartbeat_payload = {
            "broker_account_number": "HB123456789",
            "strategy_prefix": "HB",
            "event": "Test heartbeat event",
        }

        status, response_data = request(
            method="POST",
            endpoint="/api/heartbeat/",
            payload=heartbeat_payload,
        )

        self.assertEqual(status, 201)
        self.assertEqual(response_data["message"], "Heartbeat created successfully")
