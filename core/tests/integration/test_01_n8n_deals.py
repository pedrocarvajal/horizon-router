from django.test import SimpleTestCase
from core.services.n8n_deals import N8NDeal
from core.enums.deal import DealTypes, DealDirections


class N8NDealIntegrationTest(SimpleTestCase):
    def test_n8n_deal_execute_success(self):
        """Test that N8NDeal service can successfully make a request to N8N API"""
        n8n_deal = N8NDeal()
        test_params = {
            "token": "TEST",
            "strategy_prefix": "TEST",
            "strategy_name": "Strategy",
            "time": "2025-10-03T10:30:00Z",
            "symbol": "EURUSD",
            "type": DealTypes.ORDER_TYPE_BUY,
            "direction": DealDirections.IN,
            "volume": 0.1,
            "price": 1.0856,
            "profit": 15.50,
            "take_profit_price": 1.0900,
            "stop_loss_price": 1.0800,
            "broker_account_number": "12345678",
        }

        response = None

        try:
            response = n8n_deal.execute(test_params)
        except Exception as e:
            self.fail(f"N8N API call failed: {e}")

        self.assertIsInstance(response, dict)
        self.assertIsNotNone(response)
