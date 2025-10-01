from django.test import SimpleTestCase
from django.conf import settings
import requests


class AccountControllerE2ETest(SimpleTestCase):
    def setUp(self):
        self.base_url = f"http://127.0.0.1:{settings.EXT_PORT_APP}"
        self.headers = {
            settings.API_KEY_HEADER_NAME: settings.API_KEY_SECRET,
            "Content-Type": "application/json",
        }

    def test_create_account_success(self):
        url = f"{self.base_url}/api/accounts/"
        payload = {
            "name": "Test Account E2E",
            "broker_account_number": "987654321",
            "broker_name": "E2E Test Broker",
        }

        response = requests.post(url, json=payload, headers=self.headers)

        self.assertEqual(response.status_code, 201)
        response_data = response.json()
        self.assertEqual(response_data["message"], "Account created successfully")
        self.assertIn("data", response_data)
        self.assertIn("id", response_data["data"])

    def test_search_accounts_success(self):
        url = f"{self.base_url}/api/accounts/"
        payload = {
            "name": "Search Test Account",
            "broker_account_number": "111222333",
            "broker_name": "Search Test Broker",
        }

        requests.post(url, json=payload, headers=self.headers)

        search_url = f"{self.base_url}/api/accounts/search/"
        response = requests.get(search_url, headers=self.headers)

        self.assertEqual(response.status_code, 200)
        response_data = response.json()
        self.assertEqual(response_data["message"], "Accounts retrieved successfully")
        self.assertIn("data", response_data)
        self.assertIsInstance(response_data["data"], list)

    def test_update_account_success(self):
        create_url = f"{self.base_url}/api/accounts/"
        payload = {
            "name": "Update Test Account",
            "broker_account_number": "444555666",
            "broker_name": "Update Test Broker",
        }

        create_response = requests.post(create_url, json=payload, headers=self.headers)
        account_id = create_response.json()["data"]["id"]

        search_url = f"{self.base_url}/api/accounts/search/?name=Update Test Account"
        search_response = requests.get(search_url, headers=self.headers)
        accounts = search_response.json()["data"]
        self.assertGreater(len(accounts), 0)
        account_id = accounts[0]["id"]

        update_url = f"{self.base_url}/api/accounts/{account_id}/"
        update_payload = {
            "name": "Updated Account Name",
            "broker_name": "Updated Broker Name",
        }

        response = requests.put(update_url, json=update_payload, headers=self.headers)

        self.assertEqual(response.status_code, 200)
        response_data = response.json()
        self.assertEqual(response_data["message"], "Account updated successfully")

    def test_delete_account_success(self):
        create_url = f"{self.base_url}/api/accounts/"
        payload = {
            "name": "Delete Test Account",
            "broker_account_number": "777888999",
            "broker_name": "Delete Test Broker",
        }

        create_response = requests.post(create_url, json=payload, headers=self.headers)
        account_id = create_response.json()["data"]["id"]

        search_url = f"{self.base_url}/api/accounts/search/?name=Delete Test Account"
        search_response = requests.get(search_url, headers=self.headers)
        accounts = search_response.json()["data"]
        self.assertGreater(len(accounts), 0)
        account_id = accounts[0]["id"]

        delete_url = f"{self.base_url}/api/accounts/{account_id}/delete/"
        response = requests.delete(delete_url, headers=self.headers)

        self.assertEqual(response.status_code, 200)
        response_data = response.json()
        self.assertEqual(response_data["message"], "Account deleted successfully")
