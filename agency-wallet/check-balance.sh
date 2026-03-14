#!/bin/bash
# Agency Wallet Balance Checker
# Queries blockchain for balance
# Uses free public APIs (etherscan.io, blockchair.com, solana.fm)
# Cost: $0.00

set -e

WALLET_DIR="${HOME}/.agency-wallet"
PUBFILE="${WALLET_DIR}/keys/public.address"

if [[ ! -f "${PUBFILE}" ]]; then
    echo "❌ Wallet not found. Run generate-keys.sh first."
    exit 1
fi

ADDRESS=$(cat "${PUBFILE}")

echo "╔════════════════════════════════════════════════════════════════╗"
echo "║              AGENCY WALLET BALANCE CHECK                       ║"
echo "╚════════════════════════════════════════════════════════════════╝"
echo ""
echo "Address: ${ADDRESS}"
echo ""

# For this PoC, simulate balance check
# In production, would query:
# - Etherscan API for Ethereum/USDC balance
# - Blockchair for Bitcoin
# - Solana RPC for Solana

# Simulation: Check local tracking file
TRACKING_FILE="${WALLET_DIR}/balance.jsonl"

if [[ -f "${TRACKING_FILE}" ]]; then
    echo "📊 Balance History:"
    tail -5 "${TRACKING_FILE}" | jq '.timestamp, .balance, .source' 2>/dev/null || cat "${TRACKING_FILE}" | tail -5
    echo ""
fi

# For now, show what to do next
echo "🔍 To check real balance:"
echo "   - Ethereum (USDC): Visit etherscan.io and search ${ADDRESS}"
echo "   - Bitcoin: Visit blockchair.com and search ${ADDRESS}"
echo "   - Solana: Visit explorer.solana.com and search ${ADDRESS}"
echo ""
echo "Once deposit arrives, run:"
echo "   ./agency-wallet/log-deposit.sh"
echo ""
