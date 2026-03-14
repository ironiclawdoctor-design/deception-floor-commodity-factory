#!/bin/bash
# Generate QR Code for Crypto Deposit
# Simplifies onboarding: Sender scans QR → sends crypto → logged as down payment
# Risk: Wrong send = void/chaos, logged as "down payment on seriously delinquent accounts"
# Cost: $0.00

set -e

WALLET_DIR="${HOME}/.agency-wallet"
PUBFILE="${WALLET_DIR}/keys/public.address"
QR_DIR="${WALLET_DIR}/qr-codes"

if [[ ! -f "${PUBFILE}" ]]; then
    echo "❌ Wallet not found. Run generate-keys.sh first."
    exit 1
fi

mkdir -p "${QR_DIR}"

ADDRESS=$(cat "${PUBFILE}")
TIMESTAMP=$(date +%Y%m%d-%H%M%S)

# Ask for crypto type
echo "╔════════════════════════════════════════════════════════════════╗"
echo "║            AGENCY CRYPTO DEPOSIT QR CODE GENERATOR             ║"
echo "╚════════════════════════════════════════════════════════════════╝"
echo ""
echo "Wallet address: ${ADDRESS}"
echo ""
read -p "Crypto type (USDC/Bitcoin/Solana): " CRYPTO_TYPE
read -p "Amount expected (optional, e.g., '1.22'): " EXPECTED_AMOUNT

# Format QR data
if [[ "$CRYPTO_TYPE" == "USDC" ]]; then
    QR_DATA="ethereum:${ADDRESS}"
    TITLE="USDC (Ethereum)"
elif [[ "$CRYPTO_TYPE" == "Bitcoin" ]]; then
    QR_DATA="bitcoin:${ADDRESS}"
    TITLE="Bitcoin"
elif [[ "$CRYPTO_TYPE" == "Solana" ]]; then
    QR_DATA="solana:${ADDRESS}"
    TITLE="Solana"
else
    echo "Unknown crypto type: $CRYPTO_TYPE"
    exit 1
fi

if [[ ! -z "$EXPECTED_AMOUNT" ]]; then
    QR_DATA="${QR_DATA}?amount=${EXPECTED_AMOUNT}"
fi

# Generate QR code (ASCII for terminal display)
echo "Generating QR code..."
python3-qr "${QR_DATA}" > "${QR_DIR}/qr-${CRYPTO_TYPE}-${TIMESTAMP}.txt" 2>/dev/null || \
python3 -m qrcode "${QR_DATA}" -t ASCII > "${QR_DIR}/qr-${CRYPTO_TYPE}-${TIMESTAMP}.txt"

# Also generate PNG for web/print
python3 -m qrcode \
    -i "${QR_DIR}/qr-${CRYPTO_TYPE}-${TIMESTAMP}.png" \
    "${QR_DATA}" 2>/dev/null || echo "⚠️  PNG generation skipped (PIL not installed)"

echo ""
echo "╔════════════════════════════════════════════════════════════════╗"
echo "║                  QR CODE GENERATED                             ║"
echo "╠════════════════════════════════════════════════════════════════╣"
echo "║ Crypto:  ${TITLE}"
echo "║ Address: ${ADDRESS}"
if [[ ! -z "$EXPECTED_AMOUNT" ]]; then
    echo "║ Expected: ${EXPECTED_AMOUNT}"
fi
echo "╚════════════════════════════════════════════════════════════════╝"
echo ""
echo "📱 QR Code (scan with wallet):"
echo ""
cat "${QR_DIR}/qr-${CRYPTO_TYPE}-${TIMESTAMP}.txt"
echo ""
echo "Files saved:"
echo "  ASCII: ${QR_DIR}/qr-${CRYPTO_TYPE}-${TIMESTAMP}.txt"
if [[ -f "${QR_DIR}/qr-${CRYPTO_TYPE}-${TIMESTAMP}.png" ]]; then
    echo "  PNG:   ${QR_DIR}/qr-${CRYPTO_TYPE}-${TIMESTAMP}.png"
fi
echo ""
echo "⚠️  RISK ACKNOWLEDGMENT:"
echo "   If sender uses wrong address/network:"
echo "   - Crypto lost (void/chaos, non-recoverable)"
echo "   - Logged as 'down payment on seriously delinquent accounts'"
echo "   - May trigger governance action (restitution consideration)"
echo ""
echo "✅ Share this QR code with crypto senders"
echo ""
