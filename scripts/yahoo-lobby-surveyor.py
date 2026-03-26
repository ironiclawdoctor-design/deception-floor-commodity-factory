import json
import requests
import os

TOKEN_PATH = "/data/browser-server-token"

def audit_yahoo_lobby():
    print("--- FIESTA ENCLAVE: YAHOO LOBBY AUDIT ---")
    if not os.path.exists(TOKEN_PATH):
        print("ERROR: Browser token missing.")
        return

    with open(TOKEN_PATH, 'r') as f:
        token = f.read().strip()

    payload = {
        "url": "https://www.yahoo.com",
        "actions": [
            {"type": "wait", "ms": 5000},
            {"type": "snapshot"},
            {"type": "evaluate", "fn": "() => { return { cookies: document.cookie, userAgent: navigator.userAgent }; }"}
        ],
        "screenshot": True
    }

    print("[AUDIT] Manifesting in the Yahoo Lobby (via Nabre Proxy)...")
    try:
        response = requests.post(f"http://localhost:9222/?token={token}", json=payload, timeout=60)
        result = response.json()
        
        with open("/root/.openclaw/workspace/enclave/surveillance/yahoo/audit_result.json", "w") as out:
            json.dump(result, out, indent=2)
            
        print("[SUCCESS] Yahoo Audit complete. Legacy Signal captured.")
    except Exception as e:
        print(f"[REMEDY] Yahoo Sentinel resisted: {e}")

if __name__ == "__main__":
    audit_yahoo_lobby()
