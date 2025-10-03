from django.test import SimpleTestCase
from core.tests.e2e.helpers.request import request
from core.tests.e2e.helpers.create_test_account import create_test_account
from core.tests.e2e.helpers.delete_test_account import (
    delete_test_account_by_broker_number,
)


class AccountControllerE2ETest(SimpleTestCase):
    def tearDown(self):
        delete_test_account_by_broker_number("987654321")
        delete_test_account_by_broker_number("111222333")
        delete_test_account_by_broker_number("444555666")
        delete_test_account_by_broker_number("777888999")

    def test_create_account_success(self):
        payload = {
            "name": "Test Account E2E",
            "broker_account_number": "987654321",
            "broker_name": "E2E Test Broker",
        }

        status, response_data = request(
            method="POST",
            endpoint="/api/accounts/",
            payload=payload,
        )

        self.assertEqual(status, 201)
        self.assertEqual(response_data["message"], "Account created successfully")
        self.assertIn("data", response_data)
        self.assertIn("id", response_data["data"])

    def test_search_accounts_success(self):
        create_test_account(
            name="Search Test Account",
            broker_account_number="111222333",
            broker_name="Search Test Broker",
        )

        status, response_data = request(
            method="GET",
            endpoint="/api/accounts/search/",
        )

        self.assertEqual(status, 200)
        self.assertEqual(response_data["message"], "Accounts retrieved successfully")
        self.assertIn("data", response_data)
        self.assertIsInstance(response_data["data"], list)

    def test_update_account_success(self):
        account_id = create_test_account(
            name="Update Test Account",
            broker_account_number="444555666",
            broker_name="Update Test Broker",
        )

        update_payload = {
            "name": "Updated Account Name",
            "broker_name": "Updated Broker Name",
        }

        status, response_data = request(
            method="PUT",
            endpoint=f"/api/accounts/{account_id}/",
            payload=update_payload,
        )

        self.assertEqual(status, 200)
        self.assertEqual(response_data["message"], "Account updated successfully")

    def test_delete_account_success(self):
        account_id = create_test_account(
            name="Delete Test Account",
            broker_account_number="777888999",
            broker_name="Delete Test Broker",
        )

        status, response_data = request(
            method="DELETE",
            endpoint=f"/api/accounts/{account_id}/delete/",
        )

        self.assertEqual(status, 200)
        self.assertEqual(response_data["message"], "Account deleted successfully")
