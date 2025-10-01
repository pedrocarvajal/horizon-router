from core.tests.e2e.helpers.request import request


def create_test_strategy(name, prefix, symbol):
    payload = {
        "name": name,
        "prefix": prefix,
        "symbol": symbol,
    }

    status, response_data = request(
        method="POST",
        endpoint="/api/strategies/",
        payload=payload,
    )

    return response_data["data"]["id"]
