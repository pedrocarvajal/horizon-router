from core.tests.e2e.helpers.request import request


def search_account_by_name(name):
    status, search_data = request(
        method="GET",
        endpoint="/api/accounts/search/",
        payload={"name": name},
    )

    accounts = search_data["data"]

    return accounts[0]["id"] if accounts else None
