#!/usr/bin/env python3
import json, urllib.request, urllib.error

def test_token(token, env):
    base = "https://connect.squareup.com" if env == "production" else "https://connect.squareupsandbox.com"
    url = f"{base}/v2/merchants/me"
    headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
    req = urllib.request.Request(url, headers=headers)
    try:
        with urllib.request.urlopen(req, timeout=10) as r:
            data = json.loads(r.read())
            print(f"✅ {env}: Success")
            print(f"   Merchant: {data.get('merchant', {}).get('business_name', 'unknown')}")
            return True
    except urllib.error.HTTPError as e:
        print(f"❌ {env}: HTTP {e.code} {e.reason}")
        print(f"   {e.read().decode()}")
        return False
    except Exception as e:
        print(f"❌ {env}: {e}")
        return False

# Load cashapp.json
with open('/root/.openclaw/workspace/secrets/cashapp.json') as f:
    config = json.load(f)

print("Testing tokens from cashapp.json...")
print(f"environment: {config.get('environment')}")
print(f"application_id: {config.get('application_id')}")
print(f"access_token: {config.get('access_token')[:10]}...")
print(f"production_token: {config.get('production_token')[:10]}...")
print()

# Test sandbox token (access_token) with sandbox env
if 'access_token' in config:
    test_token(config['access_token'], 'sandbox')
print()
# Test production token with production env
if 'production_token' in config:
    test_token(config['production_token'], 'production')