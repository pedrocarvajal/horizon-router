from django.test import SimpleTestCase
from core.tests.e2e.helpers.request import request
from core.tests.e2e.helpers.create_test_strategy import create_test_strategy


class StrategyControllerE2ETest(SimpleTestCase):
    def test_create_strategy_success(self):
        payload = {
            "name": "Test Strategy E2E",
            "prefix": "TST",
            "symbol": "EURUSD",
        }

        status, response_data = request(
            method="POST",
            endpoint="/api/strategies/",
            payload=payload,
        )

        self.assertEqual(status, 201)
        self.assertEqual(response_data["message"], "Strategy created successfully")
        self.assertIn("data", response_data)
        self.assertIn("id", response_data["data"])

    def test_search_strategies_success(self):
        create_test_strategy(
            name="Search Test Strategy",
            prefix="STS",
            symbol="GBPUSD",
        )

        status, response_data = request(
            method="GET",
            endpoint="/api/strategies/search/",
        )

        self.assertEqual(status, 200)
        self.assertEqual(response_data["message"], "Strategies retrieved successfully")
        self.assertIn("data", response_data)
        self.assertIsInstance(response_data["data"], list)

    def test_update_strategy_success(self):
        strategy_id = create_test_strategy(
            name="Update Test Strategy",
            prefix="UTS",
            symbol="USDJPY",
        )

        update_payload = {
            "name": "Updated Strategy Name",
            "symbol": "USDCHF",
        }

        status, response_data = request(
            method="PUT",
            endpoint=f"/api/strategies/{strategy_id}/",
            payload=update_payload,
        )

        self.assertEqual(status, 200)
        self.assertEqual(response_data["message"], "Strategy updated successfully")

    def test_delete_strategy_success(self):
        strategy_id = create_test_strategy(
            name="Delete Test Strategy",
            prefix="DTS",
            symbol="AUDUSD",
        )

        status, response_data = request(
            method="DELETE",
            endpoint=f"/api/strategies/{strategy_id}/delete/",
        )

        self.assertEqual(status, 200)
        self.assertEqual(response_data["message"], "Strategy deleted successfully")
