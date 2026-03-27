#!/usr/bin/env python3
"""
Check MoltStation wallet balance on Base/Arbitrum
"""

import requests
import json

wallet_address = "0x499516cBE49262be42452438E7E202bF8fa79615"

# Try multiple APIs
apis = [
    "https://api.basescan.org/api",
    "https://base.blockscout.com/api/v2",
    "https://blockscout.com/base/mainnet/api/v2"
]

for api_base in apis:
    try:
        if "blockscout" in api_base:
            url = f"{api_base}/addresses/{wallet_address}/balance"
            response = requests.get(url, timeout=10)
            print(f"API: {api_base}")
            print(f"Response: {response.text}")
            if response.status_code == 200:
                data = response.json()
                if 'balance' in data:
                    balance_wei = int(data['balance'])
                    balance_eth = balance_wei / 10**18
                    print(f"Balance: {balance_eth} ETH")
                    break
        else:
            # Basescan API
            params = {
                'module': 'account',
                'action': 'balance',
                'address': wallet_address,
                'tag': 'latest',
                'apikey': 'demo'  # Demo key for testing
            }
            response = requests.get(api_base, params=params, timeout=10)
            print(f"API: {api_base}")
            print(f"Response: {response.text}")
            data = response.json()
            if data['status'] == '1' and 'result' in data:
                balance_wei = int(data['result'])
                balance_eth = balance_wei / 10**18
                print(f"Balance: {balance_eth} ETH")
                break
    except Exception as e:
        print(f"Error with {api_base}: {e}")
        continue

print("Wallet check completed.")