#!/usr/bin/env python3
import json
import urllib.request
import urllib.parse

# MoltStation wallet address
wallet_address = "0x499516cBE49262be42452438E7E202bF8fa79615"

# Try correct blockchain APIs
apis = [
    {
        "name": "Base Blockscout",
        "url": f"https://base.blockscout.com/api/v2/addresses/{wallet_address}/balance"
    },
    {
        "name": "Arbitrum Blockscout", 
        "url": f"https://api.arbiscan.io/api?module=account&action=balance&address={wallet_address}&tag=latest"
    }
]

print("Checking MoltStation wallet ETH balance...")
print(f"Wallet: {wallet_address}")
print("-" * 50)

for api in apis:
    try:
        req = urllib.request.Request(api["url"])
        with urllib.request.urlopen(req, timeout=10) as response:
            data = json.loads(response.read().decode())
            
            if "balance" in data:
                balance_wei = int(data["balance"])
                balance_eth = balance_wei / 10**18
                print(f"{api['name']}: {balance_eth} ETH ({balance_wei} wei)")
                
                if balance_eth > 0:
                    print("✅ ETH balance detected! MoltStation registration can proceed.")
                    print(f"Gas required: ~0.001 ETH")
                    print(f"Available for registration: {balance_eth - 0.001} ETH")
                else:
                    print("❌ 0 ETH balance - no registration possible")
            elif data.get("status") == "1" and "result" in data:
                balance_wei = int(data["result"])
                balance_eth = balance_wei / 10**18
                print(f"{api['name']}: {balance_eth} ETH ({balance_wei} wei)")
                
                if balance_eth > 0:
                    print("✅ ETH balance detected! MoltStation registration can proceed.")
                    print(f"Gas required: ~0.001 ETH")
                    print(f"Available for registration: {balance_eth - 0.001} ETH")
                else:
                    print("❌ 0 ETH balance - no registration possible")
            else:
                print(f"{api['name']}: Unexpected response format")
                print(f"Response: {data}")
                
    except Exception as e:
        print(f"{api['name']}: Error - {str(e)}")

print("-" * 50)
print("Check complete.")