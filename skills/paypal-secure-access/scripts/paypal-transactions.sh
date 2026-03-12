#!/usr/bin/env bash
# List recent PayPal transactions
# Usage: ./paypal-transactions.sh [--days N]

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
PAYPAL_MODE="${PAYPAL_MODE:-sandbox}"
DAYS="${1:-7}"

# Strip --days flag if present
if [ "$DAYS" = "--days" ]; then
  DAYS="${2:-7}"
fi

if [ "$PAYPAL_MODE" = "live" ]; then
  API_BASE="https://api-m.paypal.com"
else
  API_BASE="https://api-m.sandbox.paypal.com"
fi

TOKEN=$("$SCRIPT_DIR/paypal-auth.sh")

START_DATE=$(date -u -d "${DAYS} days ago" +%Y-%m-%dT00:00:00-0000 2>/dev/null || date -u -v-${DAYS}d +%Y-%m-%dT00:00:00-0000 2>/dev/null)
END_DATE=$(date -u +%Y-%m-%dT%H:%M:%S-0000)

TRANSACTIONS=$(curl -s -X GET "${API_BASE}/v1/reporting/transactions?start_date=${START_DATE}&end_date=${END_DATE}&fields=all&page_size=20&page=1" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer ${TOKEN}" 2>/dev/null)

echo "$TRANSACTIONS" | python3 -c "
import json,sys
try:
    d = json.load(sys.stdin)
    txns = d.get('transaction_details', [])
    total = d.get('total_items', 0)
    print(f'📊 {total} transactions in last ${DAYS} days\n')
    for t in txns[:20]:
        info = t.get('transaction_info', {})
        payer = t.get('payer_info', {})
        tid = info.get('transaction_id', '?')[:12]
        amount = info.get('transaction_amount', {})
        val = amount.get('value', '0.00')
        cur = amount.get('currency_code', 'USD')
        status = info.get('transaction_status', '?')
        date = info.get('transaction_updated_date', '?')[:10]
        name = payer.get('payer_name', {}).get('alternate_full_name', 'Unknown')
        sign = '+' if float(val) > 0 else ''
        print(f'  {date} | {sign}\${val} {cur} | {status} | {name} | {tid}...')
    if not txns:
        print('  No transactions found.')
except Exception as e:
    print(f'Error: {e}')
"
