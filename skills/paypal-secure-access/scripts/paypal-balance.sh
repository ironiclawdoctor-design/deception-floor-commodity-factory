#!/usr/bin/env bash
# Check PayPal account balance
# Usage: ./paypal-balance.sh

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
PAYPAL_MODE="${PAYPAL_MODE:-sandbox}"

if [ "$PAYPAL_MODE" = "live" ]; then
  API_BASE="https://api-m.paypal.com"
else
  API_BASE="https://api-m.sandbox.paypal.com"
fi

TOKEN=$("$SCRIPT_DIR/paypal-auth.sh")

BALANCE=$(curl -s -X GET "${API_BASE}/v1/reporting/balances?as_of_time=$(date -u +%Y-%m-%dT%H:%M:%S-0000)&currency_code=USD" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer ${TOKEN}" 2>/dev/null)

echo "$BALANCE" | python3 -c "
import json,sys
try:
    d = json.load(sys.stdin)
    balances = d.get('balances', [])
    for b in balances:
        currency = b.get('currency_code', '?')
        total = b.get('total_balance', {}).get('value', '0.00')
        available = b.get('available_balance', {}).get('value', '0.00')
        print(f'💰 {currency}: \${total} total / \${available} available')
    if not balances:
        print('No balance data returned. Check credentials and permissions.')
except Exception as e:
    print(f'Error parsing response: {e}')
    print(sys.stdin.read() if hasattr(sys.stdin, 'read') else '')
"
