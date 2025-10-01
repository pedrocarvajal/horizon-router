from django.conf import settings
import requests

def request(method, endpoint, payload=None):
    base_url = f"http://127.0.0.1:{settings.EXT_PORT_APP}"

    headers = {
        settings.API_KEY_HEADER_NAME: settings.API_KEY_SECRET,
        "Content-Type": "application/json",
    }

    url = f"{base_url}{endpoint}"

    method = method.upper()

    if method == "GET":
        if payload:
            query_string = "&".join(
                [f"{key}={value}" for key, value in payload.items()]
            )
            url = f"{url}?{query_string}"

        response = requests.get(url, headers=headers)
    elif method == "POST":
        response = requests.post(url, json=payload, headers=headers)
    elif method == "PUT":
        response = requests.put(url, json=payload, headers=headers)
    elif method == "DELETE":
        response = requests.delete(url, headers=headers)
    elif method == "PATCH":
        response = requests.patch(url, json=payload, headers=headers)
    else:
        raise ValueError(f"Unsupported HTTP method: {method}")

    status = response.status_code

    try:
        data = response.json()
    except ValueError:
        data = None

    return status, data
