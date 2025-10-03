from datetime import datetime
from core.tests.e2e.helpers.request import request
from core.tests.e2e.helpers.create_test_strategy import create_test_strategy
from core.tests.e2e.helpers.create_test_account import create_test_account


def create_test_deal(token=None, strategy_prefix=None, broker_account_number=None):
    if not strategy_prefix:
        create_test_strategy("Test Deal Strategy", "TDS", "EURUSD")
        strategy_prefix = "TDS"

    if not broker_account_number:
        create_test_account("Test Deal Account", "12345", "Test Broker")
        broker_account_number = "12345"

    if not token:
        token = f"test_token_{datetime.now().strftime('%Y%m%d_%H%M%S')}"

    payload = {
        "token": token,
        "strategy_prefix": strategy_prefix,
        "strategy_name": "Test Deal Strategy",
        "time": datetime.now().isoformat() + "Z",
        "symbol": "EURUSD",
        "type": 0,
        "direction": 0,
        "volume": 0.1,
        "price": 1.1234,
        "profit": None,
        "take_profit_price": 1.1300,
        "stop_loss_price": 1.1200,
        "broker_account_number": broker_account_number,
    }

    status, response_data = request(
        method="POST",
        endpoint="/api/deals/",
        payload=payload,
    )

    return response_data["data"]["id"]
