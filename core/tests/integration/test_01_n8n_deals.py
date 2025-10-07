from datetime import datetime
from django.test import SimpleTestCase
from core.services.n8n_deals import N8NDeal
from core.enums.deal import DealTypes, DealDirections
from core.tests.e2e.helpers.request import request
from core.tests.e2e.helpers.create_test_strategy import create_test_strategy
from core.tests.e2e.helpers.create_test_account import create_test_account
from core.tests.e2e.helpers.delete_test_strategy import delete_test_strategy_by_prefix
from core.tests.e2e.helpers.delete_test_account import (
    delete_test_account_by_broker_number,
)


class N8NDealIntegrationTest(SimpleTestCase):
    def tearDown(self):
        status, response_data = request(method="GET", endpoint="/api/deals/search/")
        if status == 200:
            for deal in response_data.get("data", []):
                if deal.get("token", "").startswith("n8n_integration_"):
                    request(
                        method="DELETE", endpoint=f"/api/deals/{deal['id']}/delete/"
                    )

        delete_test_strategy_by_prefix("N8N")
        delete_test_account_by_broker_number("N8N123")

    def test_n8n_deal_execute_success(self):
        create_test_strategy("N8N Integration Strategy", "N8N", "EURUSD")
        create_test_account("N8N Integration Account", "N8N123", "N8N Broker")

        token = f"n8n_integration_{datetime.now().strftime('%Y%m%d_%H%M%S')}"

        payload = {
            "token": token,
            "strategy_prefix": "N8N",
            "strategy_name": "N8N Integration Strategy",
            "time": datetime.now().isoformat() + "Z",
            "symbol": "EURUSD",
            "type": DealTypes.ORDER_TYPE_BUY,
            "direction": DealDirections.IN,
            "volume": 0.1,
            "price": 1.0856,
            "profit": 15.50,
            "take_profit_price": 1.0900,
            "stop_loss_price": 1.0800,
            "broker_account_number": "N8N123",
        }

        status, response_data = request(
            method="POST", endpoint="/api/deals/", payload=payload
        )

        self.assertEqual(status, 201)
        deal_id = response_data["data"]["id"]

        status, response_data = request(
            method="GET", endpoint=f"/api/deals/search/?id={deal_id}"
        )

        self.assertEqual(status, 200)
        deal_data = response_data["data"][0]

        n8n_service = N8NDeal()
        profit = deal_data["profit"] if deal_data["profit"] else None
        take_profit_price = deal_data["take_profit_price"]
        stop_loss_price = deal_data["stop_loss_price"]
        n8n_payload = {
            "id": deal_data["id"],
            "token": deal_data["token"],
            "strategy_prefix": deal_data["strategy"]["prefix"],
            "strategy_name": deal_data["strategy"]["name"],
            "time": deal_data["time"],
            "symbol": deal_data["symbol"],
            "type": deal_data["type"],
            "direction": deal_data["direction"],
            "volume": str(deal_data["volume"]),
            "price": str(deal_data["price"]),
            "profit": str(profit),
            "take_profit_price": str(take_profit_price),
            "stop_loss_price": str(stop_loss_price),
            "account": deal_data["account"]["id"],
        }

        response = None

        try:
            response = n8n_service.execute(params=n8n_payload)
        except Exception as e:
            self.fail(f"N8N API call failed: {e}")

        self.assertIsInstance(response, dict)
        self.assertIsNotNone(response)
