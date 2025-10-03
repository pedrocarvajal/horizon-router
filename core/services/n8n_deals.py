import requests
from django.conf import settings
from typing import Dict, Any, Optional
import logging

logger = logging.getLogger("horizon")


class N8NDeal:
    def __init__(self):
        self.api_url = "https://n8n-n8n.ezf7mg.easypanel.host/webhook/950cca07-5138-40bd-9e6e-0372f03833b4"
        self.api_key = settings.N8N_API_KEY_SECRET
        self.header_name = settings.N8N_API_KEY_HEADER_NAME
        self.env_mode = settings.ENV_MODE

    @property
    def base_url(self) -> str:
        return self.api_url

    def _get_headers(self) -> Dict[str, str]:
        return {self.header_name: self.api_key, "Content-Type": "application/json"}

    def execute(self, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        try:
            headers = self._get_headers()
            logger.debug(f"Making GET request to {self.base_url} with params: {params}")
            response = requests.get(
                url=self.base_url, params=params or {}, headers=headers, timeout=30
            )

            response.raise_for_status()
            logger.info(f"N8N API request successful. Status: {response.status_code}")

            try:
                return response.json()
            except ValueError:
                return {"response": response.text, "status_code": response.status_code}

        except requests.exceptions.Timeout:
            logger.error("N8N API request timed out")
            raise Exception("Request to N8N API timed out")

        except requests.exceptions.ConnectionError:
            logger.error("Failed to connect to N8N API")
            raise Exception("Failed to connect to N8N API")

        except requests.exceptions.HTTPError as e:
            logger.error(f"N8N API returned HTTP error: {e}")
            raise Exception(f"N8N API HTTP error: {e}")

        except Exception as e:
            logger.error(f"Unexpected error in N8N API call: {e}")
            raise Exception(f"Unexpected error: {e}")
