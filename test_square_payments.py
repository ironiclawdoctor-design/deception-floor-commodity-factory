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
print(f"Locations: {json.dumps(locations, indent=2)}")

# Get first location id
if locations.get('locations'):
    loc_id = locations['locations'][0]['id']
    # List payments for last 30 days
    begin_time = (datetime.utcnow() - timedelta(days=30)).isoformat() + 'Z'
    payments = api_request(token, f'/v2/payments?location_id={loc_id}&begin_time={begin_time}', env)
    print(f"Payments: {json.dumps(payments, indent=2)}")
else:
    print("No locations found.")