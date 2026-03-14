#!/bin/bash
# Log "Down Payment on Seriously Delinquent Accounts" (Risk Acknowledgment)
# When wrong send happens (void/chaos):
# - Crypto is lost (non-recoverable, entropy)
# - Logged as down payment toward account resolution
# - May trigger governance consideration for restitution
# Cost: $0.00 (logging only)

set -e

WALLET_DIR="${HOME}/.agency-wallet"
DELINQUENT_LOG="${WALLET_DIR}/delinquent-accounts.jsonl"

echo "╔════════════════════════════════════════════════════════════════╗"
echo "║        DOWN PAYMENT ON SERIOUSLY DELINQUENT ACCOUNTS           ║"
echo "╠════════════════════════════════════════════════════════════════╣"
echo "║ Risk: Crypto sent to wrong address/network = void/chaos        ║"
echo "║ Outcome: Logged as down payment, may trigger restitution       ║"
echo "╚════════════════════════════════════════════════════════════════╝"
echo ""

read -p "Crypto type (USDC/Bitcoin/Solana): " CRYPTO_TYPE
read -p "Amount lost: " AMOUNT
read -p "Sender description (optional): " SENDER_DESC
read -p "What went wrong? (wrong network/address/misclick): " REASON

TIMESTAMP=$(date -u +%Y-%m-%dT%H:%M:%SZ)

# Log as JSON
ENTRY=$(jq -n \
    --arg ts "$TIMESTAMP" \
    --arg crypto "$CRYPTO_TYPE" \
    --arg amount "$AMOUNT" \
    --arg sender "$SENDER_DESC" \
    --arg reason "$REASON" \
    --arg status "down_payment_logged" \
    '{timestamp: $ts, event: "crypto_lost", crypto: $crypto, amount: $amount, sender: $sender, reason: $reason, status: $status, note: "Void/chaos = entropy owed. May trigger governance restitution consideration."}')

echo "$ENTRY" >> "${DELINQUENT_LOG}"

echo ""
echo "Entry logged:"
echo "$ENTRY" | jq '.'
echo ""
echo "📋 All delinquent accounts: ${DELINQUENT_LOG}"
echo ""
echo "⚖️  Governance Consider:"
echo "   - Is restitution warranted? (Y/N/review)"
echo "   - What's the pattern? (first-time error vs. repeated?"
echo "   - Should we add UX safeguards?"
echo ""
