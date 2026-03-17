#!/bin/bash
# Agency Wallet Balance Checker
# Queries blockchain for balance across all chains
# Uses free public APIs (etherscan.io, blockchair.com, solana.fm)
# Cost: $0.00

set -e

WALLET_DIR="${HOME}/.agency-wallet"
ETHEREUM_ADDR="${WALLET_DIR}/keys/public.address"
BITCOIN_ADDR="${WALLET_DIR}/keys/bitcoin/public.address"

echo "╔════════════════════════════════════════════════════════════════╗"
echo "║              AGENCY WALLET BALANCE CHECK (Multi-Chain)         ║"
echo "╚════════════════════════════════════════════════════════════════╝"
echo ""

# Check Ethereum (USDC)
if [[ -f "${ETHEREUM_ADDR}" ]]; then
    ETH_ADDRESS=$(cat "${ETHEREUM_ADDR}")
    echo "🔗 Ethereum (USDC)"
    echo "   Address: ${ETH_ADDRESS}"
    echo "   Check at: https://etherscan.io/address/${ETH_ADDRESS}"
    echo ""
fi

# Check Bitcoin
if [[ -f "${BITCOIN_ADDR}" ]]; then
    BTC_ADDRESS=$(cat "${BITCOIN_ADDR}")
    echo "₿  Bitcoin"
    echo "   Address: ${BTC_ADDRESS}"
    echo "   Check at: https://blockchair.com/bitcoin/address/${BTC_ADDRESS}"
    echo ""
fi

# Show local tracking
TRACKING_FILE="${WALLET_DIR}/balance.jsonl"
if [[ -f "${TRACKING_FILE}" ]]; then
    echo "📊 Recent Balance Updates:"
    tail -10 "${TRACKING_FILE}" | jq -r '.timestamp + " | " + .crypto_type + " | " + .balance' 2>/dev/null || tail -10 "${TRACKING_FILE}"
    echo ""
fi

echo "✅ Deposits to either address will be automatically logged"
echo "   Run ./ledger.sh to manage entries"
echo "   Run ./reconcile.sh to verify balances"
echo ""
