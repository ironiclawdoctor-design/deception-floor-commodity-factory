#!/bin/bash
# Log deposit confirmation to infrastructure wallet ledger
# Actually uses this to track agency capital

set -e

WALLET_DIR="${HOME}/.agency-wallet"
PUBFILE="${WALLET_DIR}/keys/public.address"
TRACKING_FILE="${WALLET_DIR}/balance.jsonl"

if [[ ! -f "${PUBFILE}" ]]; then
    echo "❌ Wallet not found. Run generate-keys.sh first."
    exit 1
fi

ADDRESS=$(cat "${PUBFILE}")
TIMESTAMP=$(date -u +%Y-%m-%dT%H:%M:%SZ)

read -p "Deposit amount (e.g., 1.22): " AMOUNT
read -p "Which crypto? (USDC/Bitcoin/Solana): " CRYPTO
read -p "Transaction hash (from blockchain): " TX_HASH

# Log to JSONL
ENTRY=$(jq -n \
    --arg ts "$TIMESTAMP" \
    --arg addr "$ADDRESS" \
    --arg amount "$AMOUNT" \
    --arg crypto "$CRYPTO" \
    --arg tx "$TX_HASH" \
    '{timestamp: $ts, address: $addr, amount: $amount, crypto: $crypto, tx_hash: $tx, status: "confirmed"}')

echo "$ENTRY" >> "${TRACKING_FILE}"

echo ""
echo "✅ Deposit logged!"
echo ""
echo "Entry:"
echo "$ENTRY" | jq '.'
echo ""
echo "All deposits tracked in: ${TRACKING_FILE}"
