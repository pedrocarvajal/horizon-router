from django.test import SimpleTestCase
from core.tests.e2e.helpers.request import request
from core.tests.e2e.helpers.create_test_account import create_test_account
from core.tests.e2e.helpers.create_test_strategy import create_test_strategy


class HeartbeatControllerE2ETest(SimpleTestCase):
    def tearDown(self):
        status, response_data = request(method="GET", endpoint="/api/accounts/search/")
        if status == 200:
            for account in response_data.get("data", []):
                if account.get("broker_account_number", "").startswith("HB"):
                    request(
                        method="DELETE",
                        endpoint=f"/api/accounts/{account['id']}/delete/",
                    )

        status, response_data = request(
            method="GET", endpoint="/api/strategies/search/"
        )
        if status == 200:
            for strategy in response_data.get("data", []):
                if strategy.get("prefix", "").startswith("HB"):
                    request(
                        method="DELETE",
                        endpoint=f"/api/strategies/{strategy['id']}/delete/",
                    )

    def test_create_heartbeat_success(self):
        from datetime import datetime

        unique_suffix = datetime.now().strftime("%Y%m%d_%H%M%S_%f")

        account_id = create_test_account(
            name="Heartbeat Test Account",
            broker_account_number=f"HB{unique_suffix}",
            broker_name="Heartbeat Test Broker",
        )

        strategy_id = create_test_strategy(
            name="Heartbeat Test Strategy",
            prefix=f"HB{unique_suffix[:6]}",
            symbol="EURUSD",
        )

        heartbeat_payload = {
            "broker_account_number": f"HB{unique_suffix}",
            "strategy_prefix": f"HB{unique_suffix[:6]}",
            "event": "Test heartbeat event",
        }

        status, response_data = request(
            method="POST",
            endpoint="/api/heartbeat/",
            payload=heartbeat_payload,
        )

        self.assertEqual(status, 201)
        self.assertEqual(response_data["message"], "Heartbeat created successfully")
