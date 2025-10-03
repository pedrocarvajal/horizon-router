#!/usr/bin/env python3

import requests
import json
from datetime import datetime
import uuid


def create_deal():
    # API configuration
    base_url = "https://router.horizon5.tech/api"
    endpoint = f"{base_url}/deals/"

    # Headers - using the actual API key from .env
    headers = {
        "X-API-Key": "G23uqG0zL7zL1ocsCTZbdMPTlqlFLxjq",
        "Content-Type": "application/json",
    }

    # Deal payload - using XAUUSD.EHighBreakout strategy
    payload = {
        "token": f"XAUUSD_DEAL_{uuid.uuid4().hex[:8]}",  # Unique token
        "strategy_prefix": "XAUUSD.EHB",  # From db_seed_strategy.py
        "strategy_name": "XAUUSD.EHighBreakout",  # From db_seed_strategy.py
        "time": datetime.now().isoformat() + "Z",  # Current time in ISO format
        "symbol": "XAUUSD",
        "type": 0,  # ORDER_TYPE_BUY (from DealTypes enum)
        "direction": 0,  # IN (from DealDirections enum) - entry deal
        "volume": 0.01,  # Standard lot size
        "price": 2650.50,  # Sample XAUUSD price
        "profit": None,  # Optional - null for entry
        "take_profit_price": 2680.00,  # Optional TP
        "stop_loss_price": 2620.00,  # Optional SL
        "broker_account_number": "52506938",  # IC-Markets account from db_seed_account.py
    }

    print(f"Making POST request to: {endpoint}")
    print(f"Headers: {headers}")
    print(f"Payload: {json.dumps(payload, indent=2)}")
    print("-" * 50)

    try:
        response = requests.post(endpoint, json=payload, headers=headers)

        print(f"Status Code: {response.status_code}")

        try:
            response_data = response.json()
            print(f"Response: {json.dumps(response_data, indent=2)}")
        except ValueError:
            print(f"Raw Response: {response.text}")

        if response.status_code == 201:
            print("✅ Deal created successfully!")
        else:
            print("❌ Failed to create deal")

    except requests.exceptions.RequestException as e:
        print(f"❌ Request failed: {e}")


if __name__ == "__main__":
    create_deal()
