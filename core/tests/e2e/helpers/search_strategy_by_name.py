from core.tests.e2e.helpers.request import request


def search_strategy_by_name(name):
    status, search_data = request(
        method="GET",
        endpoint="/api/strategies/search/",
        payload={"name": name},
    )

    strategies = search_data["data"]

    return strategies[0]["id"] if strategies else None
