from datetime import datetime
from django.test import SimpleTestCase
from core.tests.e2e.helpers.request import request
from core.tests.e2e.helpers.create_test_deal import create_test_deal
from core.tests.e2e.helpers.create_test_strategy import create_test_strategy
from core.tests.e2e.helpers.create_test_account import create_test_account
from core.tests.e2e.helpers.delete_test_strategy import delete_test_strategy_by_prefix
from core.tests.e2e.helpers.delete_test_account import (
    delete_test_account_by_broker_number,
)


class DealControllerE2ETest(SimpleTestCase):
    def tearDown(self):
        status, response_data = request(method="GET", endpoint="/api/deals/search/")

        if status == 200:
            for deal in response_data.get("data", []):
                if deal.get("token", "").startswith(
                    ("create_test_", "open_test_", "test_token_")
                ):
                    request(
                        method="DELETE", endpoint=f"/api/deals/{deal['id']}/delete/"
                    )

        delete_test_strategy_by_prefix("CDS")
        delete_test_strategy_by_prefix("TDS")
        delete_test_strategy_by_prefix("ODS")
        delete_test_account_by_broker_number("54321")
        delete_test_account_by_broker_number("12345")
        delete_test_account_by_broker_number("98765")

    def test_create_deal_success(self):
        create_test_strategy("Create Deal Strategy", "CDS", "EURUSD")
        create_test_account("Create Deal Account", "54321", "Create Broker")

        payload = {
            "token": f"create_test_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            "strategy_prefix": "CDS",
            "strategy_name": "Create Deal Strategy",
            "time": datetime.now().isoformat() + "Z",
            "symbol": "EURUSD",
            "type": 0,
            "direction": 0,
            "volume": 0.1,
            "price": 1.1234,
            "profit": None,
            "take_profit_price": 1.1300,
            "stop_loss_price": 1.1200,
            "broker_account_number": "54321",
        }

        status, response_data = request(
            method="POST",
            endpoint="/api/deals/",
            payload=payload,
        )

        self.assertEqual(status, 201)
        self.assertEqual(response_data["message"], "Deal created successfully")
        self.assertIn("data", response_data)
        self.assertIn("id", response_data["data"])

    def test_search_deals_success(self):
        create_test_deal()

        status, response_data = request(
            method="GET",
            endpoint="/api/deals/search/",
        )

        self.assertEqual(status, 200)
        self.assertEqual(response_data["message"], "Deals retrieved successfully")
        self.assertIn("data", response_data)
        self.assertIsInstance(response_data["data"], list)

    def test_search_open_deals_success(self):
        create_test_strategy("Open Deal Strategy", "ODS", "GBPUSD")
        create_test_account("Open Deal Account", "98765", "Open Broker")

        open_token = f"open_test_{datetime.now().strftime('%Y%m%d_%H%M%S')}"

        payload_in = {
            "token": open_token,
            "strategy_prefix": "ODS",
            "strategy_name": "Open Deal Strategy",
            "time": datetime.now().isoformat() + "Z",
            "symbol": "GBPUSD",
            "type": 0,
            "direction": 0,
            "volume": 0.2,
            "price": 1.2500,
            "broker_account_number": "98765",
        }

        request(
            method="POST",
            endpoint="/api/deals/",
            payload=payload_in,
        )

        status, response_data = request(
            method="GET",
            endpoint="/api/deals/search/?open_deals=1",
        )

        self.assertEqual(status, 200)
        self.assertEqual(response_data["message"], "Deals retrieved successfully")
        self.assertIn("data", response_data)
        self.assertIsInstance(response_data["data"], list)

        open_deals = [
            deal for deal in response_data["data"] if deal["token"] == open_token
        ]

        self.assertTrue(len(open_deals) > 0)
