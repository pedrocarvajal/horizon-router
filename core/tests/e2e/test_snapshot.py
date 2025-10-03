from datetime import datetime
from django.test import SimpleTestCase
from core.tests.e2e.helpers.request import request
from core.tests.e2e.helpers.create_test_snapshot import create_test_snapshot
from core.tests.e2e.helpers.create_test_strategy import create_test_strategy
from core.tests.e2e.helpers.create_test_account import create_test_account
from core.tests.e2e.helpers.delete_test_strategy import delete_test_strategy_by_prefix
from core.tests.e2e.helpers.delete_test_account import (
    delete_test_account_by_broker_number,
)


class SnapshotControllerE2ETest(SimpleTestCase):
    def tearDown(self):
        status, response_data = request(method="GET", endpoint="/api/snapshots/search/")

        if status == 200:
            for snapshot in response_data.get("data", []):
                if snapshot.get("event", "").startswith("test_"):
                    request(
                        method="DELETE",
                        endpoint=f"/api/snapshots/{snapshot['id']}/delete/",
                    )

        delete_test_strategy_by_prefix("TSS")
        delete_test_strategy_by_prefix("CSS")
        delete_test_account_by_broker_number("11111")
        delete_test_account_by_broker_number("22222")

    def test_create_snapshot_success(self):
        create_test_strategy("Create Snapshot Strategy", "CSS", "EURUSD")
        create_test_account("Create Snapshot Account", "11111", "Create Broker")

        payload = {
            "broker_account_number": "11111",
            "strategy_prefix": "CSS",
            "event": f"test_create_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            "balance": "15000.50",
            "nav": "14800.25",
            "exposure": "200.25",
        }

        status, response_data = request(
            method="POST",
            endpoint="/api/snapshots/",
            payload=payload,
        )

        self.assertEqual(status, 201)
        self.assertEqual(response_data["message"], "Snapshot created successfully")
        self.assertIn("data", response_data)
        self.assertIn("id", response_data["data"])

    def test_search_snapshots_success(self):
        create_test_snapshot(event="test_search")

        status, response_data = request(
            method="GET",
            endpoint="/api/snapshots/search/",
        )

        self.assertEqual(status, 200)
        self.assertEqual(response_data["message"], "Snapshots retrieved successfully")
        self.assertIn("data", response_data)
        self.assertIsInstance(response_data["data"], list)

    def test_search_snapshots_by_date_range_success(self):
        create_test_strategy("Test Snapshot Strategy", "TSS", "USDJPY")
        create_test_account("Test Snapshot Account", "22222", "Test Broker")

        test_event_1 = f"test_snapshot_1_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        test_event_2 = f"test_snapshot_2_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        test_event_3 = f"test_snapshot_3_{datetime.now().strftime('%Y%m%d_%H%M%S')}"

        snapshot1_payload = {
            "broker_account_number": "22222",
            "strategy_prefix": "TSS",
            "event": test_event_1,
            "balance": "10000.00",
            "nav": "9800.00",
            "exposure": "200.00",
        }

        snapshot2_payload = {
            "broker_account_number": "22222",
            "strategy_prefix": "TSS",
            "event": test_event_2,
            "balance": "11000.00",
            "nav": "10800.00",
            "exposure": "200.00",
        }

        snapshot3_payload = {
            "broker_account_number": "22222",
            "strategy_prefix": "TSS",
            "event": test_event_3,
            "balance": "12000.00",
            "nav": "11800.00",
            "exposure": "200.00",
        }

        request(method="POST", endpoint="/api/snapshots/", payload=snapshot1_payload)
        request(method="POST", endpoint="/api/snapshots/", payload=snapshot2_payload)
        request(method="POST", endpoint="/api/snapshots/", payload=snapshot3_payload)

        current_time = datetime.now()

        date_from = (
            current_time.replace(minute=current_time.minute - 2)
        ).isoformat() + "Z"
        status, response_data = request(
            method="GET",
            endpoint=f"/api/snapshots/search/?date_from={date_from}",
        )

        self.assertEqual(status, 200)
        self.assertEqual(response_data["message"], "Snapshots retrieved successfully")
        date_from_snapshots = [
            snapshot
            for snapshot in response_data["data"]
            if snapshot["event"].startswith("test_snapshot_")
        ]
        self.assertGreaterEqual(len(date_from_snapshots), 3)

        date_to = (
            current_time.replace(minute=current_time.minute + 2)
        ).isoformat() + "Z"
        status, response_data = request(
            method="GET",
            endpoint=f"/api/snapshots/search/?date_to={date_to}",
        )

        self.assertEqual(status, 200)
        date_to_snapshots = [
            snapshot
            for snapshot in response_data["data"]
            if snapshot["event"].startswith("test_snapshot_")
        ]
        self.assertGreaterEqual(len(date_to_snapshots), 3)

        date_from_range = (
            current_time.replace(minute=current_time.minute - 1)
        ).isoformat() + "Z"
        date_to_range = (
            current_time.replace(minute=current_time.minute + 1)
        ).isoformat() + "Z"
        status, response_data = request(
            method="GET",
            endpoint=f"/api/snapshots/search/?date_from={date_from_range}&date_to={date_to_range}",
        )

        self.assertEqual(status, 200)
        range_snapshots = [
            snapshot
            for snapshot in response_data["data"]
            if snapshot["event"].startswith("test_snapshot_")
        ]
        self.assertGreaterEqual(len(range_snapshots), 3)
