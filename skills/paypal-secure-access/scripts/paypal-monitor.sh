#!/usr/bin/env bash
# Monitor for incoming PayPal payments
# Designed to be called from heartbeat/cron
# Usage: ./paypal-monitor.sh

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
PAYPAL_MODE="${PAYPAL_MODE:-sandbox}"
STATE_FILE="${SCRIPT_DIR}/../.last-check"

if [ "$PAYPAL_MODE" = "live" ]; then
  API_BASE="https://api-m.paypal.com"
else
  API_BASE="https://api-m.sandbox.paypal.com"
fi

TOKEN=$("$SCRIPT_DIR/paypal-auth.sh")

# Get last check time or default to 24h ago
if [ -f "$STATE_FILE" ]; then
  START_DATE=$(cat "$STATE_FILE")
else
  START_DATE=$(date -u -d "1 day ago" +%Y-%m-%dT%H:%M:%S-0000 2>/dev/null || date -u -v-1d +%Y-%m-%dT%H:%M:%S-0000 2>/dev/null)
fi

END_DATE=$(date -u +%Y-%m-%dT%H:%M:%S-0000)

# Save current time for next check
echo "$END_DATE" > "$STATE_FILE"

TRANSACTIONS=$(curl -s -X GET "${API_BASE}/v1/reporting/transactions?start_date=${START_DATE}&end_date=${END_DATE}&fields=all&page_size=50&page=1&transaction_type=T0006" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer ${TOKEN}" 2>/dev/null)

echo "$TRANSACTIONS" | python3 -c "
import json,sys
try:
    d = json.load(sys.stdin)
    txns = d.get('transaction_details', [])
    incoming = [t for t in txns if float(t.get('transaction_info',{}).get('transaction_amount',{}).get('value','0')) > 0]
    if incoming:
        total = sum(float(t['transaction_info']['transaction_amount']['value']) for t in incoming)
        print(f'🚨 NEW INCOMING: {len(incoming)} payment(s) totaling \${total:.2f}')
        for t in incoming:
            info = t['transaction_info']
            val = info['transaction_amount']['value']
            cur = info['transaction_amount'].get('currency_code','USD')
            name = t.get('payer_info',{}).get('payer_name',{}).get('alternate_full_name','Unknown')
            print(f'  💵 +\${val} {cur} from {name}')
        print(f'\n⛽ Potential gas: \${total:.2f} available for agent credits')
    else:
        print('No new incoming payments since last check.')
except Exception as e:
    print(f'Error: {e}')
"
