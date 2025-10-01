from core.tests.e2e.helpers.request import request


def create_test_account(name, broker_account_number, broker_name):
    payload = {
        "name": name,
        "broker_account_number": broker_account_number,
        "broker_name": broker_name,
    }

    status, response_data = request(
        method="POST",
        endpoint="/api/accounts/",
        payload=payload,
    )

    return response_data["data"]["id"]
