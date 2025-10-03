#!/usr/bin/env python3

import requests
import json
from datetime import datetime
import uuid


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
        "event": f"END_OF_DAY_REPORT_{datetime.now().strftime('%Y%m%d')}",
        "balance": "15847.23",
        "nav": "15912.45",
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
            "token": f"EURUSD_CLOSED_{uuid.uuid4().hex[:8]}",
            "strategy_prefix": "EURUSD.EHB",
            "strategy_name": "EURUSD.EHighBreakout",
            "time": datetime.now().replace(hour=8, minute=30).isoformat() + "Z",
            "symbol": "EURUSD",
            "type": 1,
            "direction": 1,
            "volume": 0.1,
            "price": 1.0845,
            "profit": 45.80,
            "take_profit_price": None,
            "stop_loss_price": None,
            "broker_account_number": "52506938",
        },
        {
            "token": f"GBPUSD_CLOSED_{uuid.uuid4().hex[:8]}",
            "strategy_prefix": "GBPUSD.EHB",
            "strategy_name": "GBPUSD.EHighBreakout",
            "time": datetime.now().replace(hour=11, minute=15).isoformat() + "Z",
            "symbol": "GBPUSD",
            "type": 0,
            "direction": 1,
            "volume": 0.05,
            "price": 1.3102,
            "profit": -23.50,
            "take_profit_price": None,
            "stop_loss_price": None,
            "broker_account_number": "52506938",
        },
        {
            "token": f"XAUUSD_CLOSED_{uuid.uuid4().hex[:8]}",
            "strategy_prefix": "XAUUSD.EHB",
            "strategy_name": "XAUUSD.EHighBreakout",
            "time": datetime.now().replace(hour=14, minute=45).isoformat() + "Z",
            "symbol": "XAUUSD",
            "type": 0,
            "direction": 1,
            "volume": 0.01,
            "price": 2655.75,
            "profit": 127.30,
            "take_profit_price": None,
            "stop_loss_price": None,
            "broker_account_number": "52506938",
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
