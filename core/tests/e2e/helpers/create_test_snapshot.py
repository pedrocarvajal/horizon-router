from core.tests.e2e.helpers.request import request
from core.tests.e2e.helpers.create_test_strategy import create_test_strategy
from core.tests.e2e.helpers.create_test_account import create_test_account


def create_test_snapshot(broker_account_number=None, strategy_prefix=None, event=None):
    if not broker_account_number:
        create_test_account("Test Snapshot Account", "54321", "Test Broker")
        broker_account_number = "54321"

    if strategy_prefix and strategy_prefix != "":
        create_test_strategy("Test Snapshot Strategy", strategy_prefix, "EURUSD")

    if not event:
        event = "Test Event"

    payload = {
        "broker_account_number": broker_account_number,
        "strategy_prefix": strategy_prefix,
        "event": event,
        "balance": "10000.00",
        "nav": "9800.00",
        "exposure": "200.00",
    }

    status, response_data = request(
        method="POST",
        endpoint="/api/snapshots/",
        payload=payload,
    )

    return response_data["data"]["id"]
