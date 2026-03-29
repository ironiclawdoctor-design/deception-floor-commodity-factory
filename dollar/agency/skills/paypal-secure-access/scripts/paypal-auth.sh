#!/usr/bin/env bash
# PayPal OAuth 2.0 Token Acquisition
# Securely obtains bearer token from environment credentials
# NEVER logs credentials or tokens to stdout

set -euo pipefail

PAYPAL_MODE="${PAYPAL_MODE:-sandbox}"

if [ "$PAYPAL_MODE" = "live" ]; then
  API_BASE="https://api-m.paypal.com"
else
  API_BASE="https://api-m.sandbox.paypal.com"
fi

if [ -z "${PAYPAL_CLIENT_ID:-}" ] || [ -z "${PAYPAL_CLIENT_SECRET:-}" ]; then
  echo "ERROR: PAYPAL_CLIENT_ID and PAYPAL_CLIENT_SECRET must be set" >&2
  echo "Run: openclaw configure --section paypal" >&2
  exit 1
fi

# Request token (credentials sent via HTTP Basic Auth over TLS)
RESPONSE=$(curl -s -X POST "${API_BASE}/v1/oauth2/token" \
  -u "${PAYPAL_CLIENT_ID}:${PAYPAL_CLIENT_SECRET}" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "grant_type=client_credentials" 2>/dev/null)

TOKEN=$(echo "$RESPONSE" | python3 -c "import json,sys; d=json.load(sys.stdin); print(d.get('access_token',''))" 2>/dev/null)
EXPIRES=$(echo "$RESPONSE" | python3 -c "import json,sys; d=json.load(sys.stdin); print(d.get('expires_in',''))" 2>/dev/null)

if [ -z "$TOKEN" ]; then
  echo "ERROR: Failed to obtain access token" >&2
  echo "$RESPONSE" | python3 -c "import json,sys; d=json.load(sys.stdin); print(d.get('error_description','Unknown error'))" 2>/dev/null >&2
  exit 1
fi

# Output token for piping (never log it)
echo "$TOKEN"
