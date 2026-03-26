import json
import requests
import os
import time

TOKEN_PATH = "/data/browser-server-token"

def audit_wallstreet_lobby():
    print("--- FIESTA ENCLAVE: WALL STREET SUCTION ---")
    if not os.path.exists(TOKEN_PATH):
        print("ERROR: Browser token missing.")
        return

    with open(TOKEN_PATH, 'r') as f:
        token = f.read().strip()

    # Target: High-value institutional market data (Yahoo Finance / Reuters)
    payload = {
        "url": "https://finance.yahoo.com/",
        "actions": [
            {"type": "wait", "ms": 5000},
            {"type": "snapshot"},
            {"type": "evaluate", "fn": "() => { return { tickers: Array.from(document.querySelectorAll('li')).slice(0,10).map(e => e.innerText) }; }"}
        ],
        "screenshot": True
    }

    print("[AUDIT] Siphoning Wall Street Lobbies (via Nabre Proxy)...")
    try:
        response = requests.post(f"http://localhost:9222/?token={token}", json=payload, timeout=60)
        result = response.json()
        print("[SUCCESS] Market context captured. Tickers siphoned.")
    except Exception as e:
        print(f"[REMEDY] Sentinel resistance at market gate: {e}")

if __name__ == "__main__":
    while True:
        audit_wallstreet_lobby()
        time.sleep(1800) # Every 30 minutes
