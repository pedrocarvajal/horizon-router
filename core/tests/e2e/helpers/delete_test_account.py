from core.tests.e2e.helpers.request import request


def delete_test_account(account_id):
    status, response_data = request(
        method="DELETE",
        endpoint=f"/api/accounts/{account_id}/delete/",
    )
    return status == 200


def delete_test_account_by_broker_number(broker_account_number):
    status, response_data = request(
        method="GET",
        endpoint="/api/accounts/search/",
    )

    deleted_count = 0
    if status == 200:
        accounts = response_data.get("data", [])
        for account in accounts:
            if account.get("broker_account_number") == broker_account_number:
                if delete_test_account(account["id"]):
                    deleted_count += 1
    return deleted_count > 0
