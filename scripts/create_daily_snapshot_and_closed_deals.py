#!/usr/bin/env python3

import requests
import json
from datetime import datetime


def make_request(endpoint, payload):
    base_url = "https://router.horizon5.tech/api"
    headers = {
        "X-API-Key": "G23uqG0zL7zL1ocsCTZbdMPTlqlFLxjq",
        "Content-Type": "application/json",
    }

    url = f"{base_url}{endpoint}"

    try:
        response = requests.post(url, json=payload, headers=headers)

        try:
            response_data = response.json()
        except ValueError:
            response_data = {"error": response.text}

        return response.status_code, response_data

    except requests.exceptions.RequestException as e:
        return 500, {"error": str(e)}


def create_snapshot():
    payload = {
        "broker_account_number": "52506938",
        "strategy_prefix": None,
        "event": "END_OF_DAY_REPORT",
        "balance": "100000",
        "nav": "100000",
        "exposure": "2.15",
    }

    print("Creating daily snapshot...")
    print(f"Payload: {json.dumps(payload, indent=2)}")
    print("-" * 50)

    status_code, response_data = make_request("/snapshots/", payload)

    print(f"Status Code: {status_code}")
    print(f"Response: {json.dumps(response_data, indent=2)}")

    if status_code == 201:
        print("Daily snapshot created successfully!")
        return True
    else:
        print("Failed to create snapshot")
        return False


def create_closed_deals():
    deals = [
        {
            "token": "EURUSD.EHB_0_1a22d2ds",
            "strategy_prefix": "EURUSD.EHB",
            "strategy_name": "EURUSD.EHighBreakout",
            "time": datetime.now().replace(hour=8, minute=30).isoformat() + "Z",
            "symbol": "EURUSD",
            "type": 1,
            "direction": 0,
            "volume": 0.1,
            "price": 1.0845,
            "profit": 0,
            "take_profit_price": None,
            "stop_loss_price": None,
            "broker_account_number": "3000085718",
        },
        {
            "token": "EURUSD.EHB_0_1a22d2ds",
            "strategy_prefix": "EURUSD.EHB",
            "strategy_name": "EURUSD.EHighBreakout",
            "time": datetime.now().replace(hour=11, minute=15).isoformat() + "Z",
            "symbol": "EURUSD",
            "type": 0,
            "direction": 1,
            "volume": 0.1,
            "price": 1.0846,
            "profit": 23.50,
            "take_profit_price": None,
            "stop_loss_price": None,
            "broker_account_number": "3000085718",
        },
    ]

    success_count = 0

    for i, deal_payload in enumerate(deals, 1):
        print(f"Creating closed deal {i}/3...")
        print(f"Payload: {json.dumps(deal_payload, indent=2)}")
        print("-" * 50)

        status_code, response_data = make_request("/deals/", deal_payload)

        print(f"Status Code: {status_code}")
        print(f"Response: {json.dumps(response_data, indent=2)}")

        if status_code == 201:
            print(f"Closed deal {i} created successfully!")
            success_count += 1
        else:
            print(f"Failed to create closed deal {i}")

        print()

    return success_count


def main():
    print("=" * 60)
    print(f"Creating Daily Data for {datetime.now().strftime('%Y-%m-%d')}")
    print("=" * 60)
    print()

    create_snapshot()
    print()

    print("Creating closed deals...")
    print("=" * 30)
    create_closed_deals()


if __name__ == "__main__":
    main()
