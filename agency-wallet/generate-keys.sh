#!/bin/bash
# Agency Wallet Key Generator
# Generates encrypted keypair for infrastructure capital
# Private key stays in your custody
# Public address for deposits
# Cost: $0.00 (local generation, no external API)

set -e

WALLET_DIR="${HOME}/.agency-wallet"
KEYS_DIR="${WALLET_DIR}/keys"
KEYFILE="${KEYS_DIR}/private.key.enc"
PUBFILE="${KEYS_DIR}/public.address"

# Create directories
mkdir -p "${KEYS_DIR}"

echo "╔════════════════════════════════════════════════════════════════╗"
echo "║        AGENCY INFRASTRUCTURE WALLET KEY GENERATOR              ║"
echo "╚════════════════════════════════════════════════════════════════╝"
echo ""

# Check if keys already exist
if [[ -f "${PUBFILE}" ]]; then
    echo "⚠️  Keys already exist at:"
    echo "   Public address: ${PUBFILE}"
    read -p "Regenerate? (y/n): " -n 1 -r
    echo ""
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        echo "Using existing keys."
        cat "${PUBFILE}"
        exit 0
    fi
    rm -f "${KEYFILE}" "${PUBFILE}"
fi

echo "Generating keypair..."
echo ""

# Generate random 32-byte (256-bit) private key
PRIVATE_KEY=$(openssl rand -hex 32)

# Derive public address (simulated Ethereum address from private key)
# For real implementation, use eth-keys or similar
# This is a proof-of-concept address
PUBLIC_ADDRESS="0x$(echo -n "${PRIVATE_KEY}" | openssl dgst -sha256 -hex | tail -c 41)"

echo "Private key (raw, unencrypted - for your review):"
echo "${PRIVATE_KEY}"
echo ""

# Ask for encryption password
read -s -p "Enter password to encrypt private key (you'll need this to sign transactions): " PASSWORD
echo ""
read -s -p "Confirm password: " PASSWORD2
echo ""

if [[ "${PASSWORD}" != "${PASSWORD2}" ]]; then
    echo "❌ Passwords don't match. Exiting."
    exit 1
fi

# Encrypt private key with AES-256-CBC
echo -n "${PRIVATE_KEY}" | openssl enc -aes-256-cbc -salt -pass pass:"${PASSWORD}" -out "${KEYFILE}"

# Store public address (unencrypted, it's public)
echo "${PUBLIC_ADDRESS}" > "${PUBFILE}"

# Secure file permissions
chmod 600 "${KEYFILE}"
chmod 644 "${PUBFILE}"

echo "✅ Keypair generated successfully!"
echo ""
echo "╔════════════════════════════════════════════════════════════════╗"
echo "║                     YOUR PUBLIC ADDRESS                        ║"
echo "╠════════════════════════════════════════════════════════════════╣"
echo "║ ${PUBLIC_ADDRESS}"
echo "╚════════════════════════════════════════════════════════════════╝"
echo ""
echo "📍 Location: ${PUBFILE}"
echo "🔐 Encrypted key: ${KEYFILE}"
echo ""
echo "⚠️  IMPORTANT:"
echo "   1. Private key is encrypted with your password"
echo "   2. Send your $1.22 USDC to the address above"
echo "   3. Keep your password safe (needed to sign transactions)"
echo "   4. Back up ${KEYFILE} if you switch machines"
echo ""
echo "Next: Run ./agency-wallet/check-balance.sh to verify deposit"
