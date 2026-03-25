#!/usr/bin/env python3
"""Create a Telegram Stars invoice link for the Shannon Miner shop."""
import json
import urllib.request
import urllib.parse

BOT_TOKEN = "8224060064:AAG8iEMGUwIUBPYCS4aO05LkB-fBnUKVS-g"

def create_invoice_link():
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/createInvoiceLink"
    payload = {
        "title": "500 Shannon Boost",
        "description": "Instantly adds 500 Shannon to your miner",
        "payload": "shannon-boost-500",
        "currency": "XTR",
        "prices": [{"label": "Shannon Boost", "amount": 1}],
        "provider_token": ""
    }
    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(url, data=data, headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(req) as resp:
        result = json.loads(resp.read())
    if result.get("ok"):
        print("Invoice URL:", result["result"])
        return result["result"]
    else:
        print("ERROR:", result)
        return None

if __name__ == "__main__":
    link = create_invoice_link()
    if link:
        print(f"\nHardcode this URL into shannon-miner.html:\n{link}")
