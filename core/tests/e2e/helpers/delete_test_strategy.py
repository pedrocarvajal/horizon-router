from core.tests.e2e.helpers.request import request


def delete_test_strategy(strategy_id):
    status, response_data = request(
        method="DELETE",
        endpoint=f"/api/strategies/{strategy_id}/delete/",
    )
    return status == 200


def delete_test_strategy_by_prefix(prefix):
    status, response_data = request(
        method="GET",
        endpoint="/api/strategies/search/",
    )

    if status == 200:
        strategies = response_data.get("data", [])
        for strategy in strategies:
            if strategy.get("prefix") == prefix:
                delete_test_strategy(strategy["id"])
                return True
    return False
