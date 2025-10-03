from core.tests.e2e.helpers.request import request


def delete_test_deal(deal_id):
    status, response_data = request(
        method="DELETE",
        endpoint=f"/api/deals/{deal_id}/delete/",
    )

    return status == 200


def delete_test_deals_by_token(token):
    status, response_data = request(
        method="GET",
        endpoint="/api/deals/search/",
    )

    if status == 200:
        deals = response_data.get("data", [])

        for deal in deals:
            if deal.get("token") == token:
                delete_test_deal(deal["id"])
