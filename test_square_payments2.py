#!/usr/bin/env python3
import json, urllib.request, urllib.error
from datetime import datetime, timedelta

def api_request(token, path, env='production'):
    base = "https://connect.squareup.com" if env == "production" else "https://connect.squareupsandbox.com"
    url = f"{base}{path}"
    headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
    req = urllib.request.Request(url, headers=headers)
    try:
        with urllib.request.urlopen(req, timeout=10) as r:
            return json.loads(r.read())
    except urllib.error.HTTPError as e:
        print(f"HTTP {e.code} {e.reason}")
        print(e.read().decode())
        raise

# Load token
with open('/root/.openclaw/workspace/secrets/cashapp.json') as f:
    config = json.load(f)

token = config['square_access_token']
env = config['square_environment']

print(f"Testing Square API ({env}) for payments...")
# Get locations
locations = api_request(token, '/v2/locations', env)
loc_id = locations['locations'][0]['id']

# List payments for last 30 days
begin_time = (datetime.utcnow() - timedelta(days=30)).isoformat() + 'Z'
payments = api_request(token, f'/v2/payments?location_id={loc_id}&begin_time={begin_time}', env)

for p in payments.get('payments', []):
    print(f"Payment {p['id']}:")
    print(f"  Created: {p['created_at']}")
    print(f"  Amount: {p['amount_money']['amount']/100} {p['amount_money']['currency']}")
    print(f"  Status: {p['status']}")
    if 'source_type' in p:
        print(f"  Source type: {p['source_type']}")
    if 'card_details' in p:
        print(f"  Card details present")
    if 'cash_details' in p:
        print(f"  Cash details present")
    print()