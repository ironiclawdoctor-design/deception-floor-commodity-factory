#!/bin/bash
# Agency Accounting Reconciliation
# 
# Reconciles wallet blockchain balance against ledger balance
# Flags variances, triggers alerts
# Cost: $0.00 (Tier 0 — bash + sqlite3)

set -e

WALLET_DIR="${HOME}/.agency-wallet"
ACCOUNTING_DB="${WALLET_DIR}/accounting.db"
LOG_FILE="${WALLET_DIR}/reconciliation.jsonl"

# Initialize DB if needed
if [[ ! -f "$ACCOUNTING_DB" ]]; then
  sqlite3 "$ACCOUNTING_DB" < "$(dirname "$0")/accounting.sql"
fi

timestamp() {
  date -u +"%Y-%m-%dT%H:%M:%SZ"
}

log_reconciliation() {
  local wallet_balance="$1"
  local ledger_balance="$2"
  local variance="$3"
  local status="$4"
  
  jq -n \
    --arg ts "$(timestamp)" \
    --arg wallet "$wallet_balance" \
    --arg ledger "$ledger_balance" \
    --arg variance "$variance" \
    --arg status "$status" \
    '{timestamp: $ts, wallet_balance: $wallet, ledger_balance: $ledger, variance: $variance, status: $status}' >> "$LOG_FILE"
}

# Get ledger balance (sum of all journal entries)
get_ledger_balance() {
  sqlite3 "$ACCOUNTING_DB" << EOF
SELECT COALESCE(SUM(amount), 0) 
FROM journal_lines 
WHERE account_id = (SELECT id FROM accounts WHERE account_number = '1000');
EOF
}

# Get wallet balance from blockchain (via free API)
get_wallet_balance() {
  local address="$1"
  local chain="${2:-ethereum}"
  
  case "$chain" in
    ethereum|usdc)
      # Etherscan API (free tier)
      curl -s "https://api.etherscan.io/api?module=account&action=tokenbalance&contractaddress=0xa0b86991c6218b36c1d19d4a2e9eb0ce3606eb48&address=${address}&tag=latest" | jq '.result // 0'
      ;;
    bitcoin)
      # Blockchair API (free tier)
      curl -s "https://blockchair.com/bitcoin/address/${address}?key=free" | jq '.data[.data | keys[0]].balance // 0'
      ;;
    solana)
      # Solana.fm API (free tier)
      curl -s "https://api.mainnet.solana.com" -X POST -d "{\"jsonrpc\":\"2.0\",\"id\":1,\"method\":\"getTokenAccountsByOwner\",\"params\":[\"${address}\",{\"programId\":\"TokenkegQfeZyiNwAJsyFbPVwwQQfmLzcW7PRKjsDmic\"},\"encoding\":\"base64\"]}" | jq '.result.value[0].account.data.parsed.info.tokenAmount.uiAmount // 0'
      ;;
    *)
      echo "0"
      ;;
  esac
}

# Main reconciliation
echo "╔════════════════════════════════════════════════════════════════╗"
echo "║     AGENCY ACCOUNTING RECONCILIATION                           ║"
echo "╚════════════════════════════════════════════════════════════════╝"
echo ""

echo "⏱️  Reconciliation started: $(timestamp)"
echo ""

# Get balances
echo "📊 Fetching balances..."
LEDGER_BALANCE=$(get_ledger_balance)
echo "   Ledger balance: $LEDGER_BALANCE"

# Get wallet address
if [[ ! -f "${WALLET_DIR}/keys/public.address" ]]; then
  echo "❌ Wallet not initialized. Run: ./generate-keys.sh"
  exit 1
fi
WALLET_ADDRESS=$(cat "${WALLET_DIR}/keys/public.address")

echo "   Wallet address: $WALLET_ADDRESS"
echo "   Querying blockchain..."

WALLET_BALANCE=$(get_wallet_balance "$WALLET_ADDRESS")
echo "   Blockchain balance: $WALLET_BALANCE"
echo ""

# Calculate variance
VARIANCE=$(echo "$WALLET_BALANCE - $LEDGER_BALANCE" | bc)

echo "📈 Analysis:"
echo "   Wallet:  $WALLET_BALANCE"
echo "   Ledger:  $LEDGER_BALANCE"
echo "   Variance: $VARIANCE"
echo ""

# Determine status
if [[ $(echo "$VARIANCE == 0" | bc) -eq 1 ]]; then
  STATUS="✅ BALANCED"
  SEVERITY="info"
elif [[ $(echo "($VARIANCE > -1) && ($VARIANCE < 1)" | bc) -eq 1 ]]; then
  STATUS="⚠️  ROUNDING (acceptable)"
  SEVERITY="info"
else
  STATUS="🚨 VARIANCE DETECTED"
  SEVERITY="critical"
fi

echo "$STATUS"
echo ""

# Log to database
sqlite3 "$ACCOUNTING_DB" << EOF
INSERT INTO reconciliations (reconciliation_date, wallet_balance, ledger_balance, variance, variance_reason, status)
VALUES ('$(timestamp)', $WALLET_BALANCE, $LEDGER_BALANCE, $VARIANCE, 'Automated reconciliation', '$(echo "$STATUS" | grep -o "BALANCED\|ROUNDING\|VARIANCE")');
EOF

# Log to file
log_reconciliation "$WALLET_BALANCE" "$LEDGER_BALANCE" "$VARIANCE" "$STATUS"

# Flag variance if needed
if [[ $(echo "$VARIANCE != 0" | bc) -eq 1 ]]; then
  if [[ $(echo "($VARIANCE > -1) && ($VARIANCE < 1)" | bc) -eq 0 ]]; then
    echo "⚠️  Flagging variance for investigation:"
    sqlite3 "$ACCOUNTING_DB" << EOF
INSERT INTO variances (variance_type, amount, description, severity)
VALUES ('amount_mismatch', $VARIANCE, 'Reconciliation variance: wallet balance exceeds ledger', '$SEVERITY');
EOF
    echo "   ID: $(sqlite3 "$ACCOUNTING_DB" "SELECT last_insert_rowid();")"
  fi
fi

echo ""
echo "✅ Reconciliation complete"
echo "   Log: $LOG_FILE"
echo ""

# Show recent reconciliations
echo "📋 Last 5 reconciliations:"
sqlite3 "$ACCOUNTING_DB" << EOF
.mode column
.headers on
SELECT reconciliation_date, wallet_balance, ledger_balance, variance, status FROM reconciliations ORDER BY reconciliation_date DESC LIMIT 5;
EOF

echo ""
echo "🚨 Active variances:"
VARIANCE_COUNT=$(sqlite3 "$ACCOUNTING_DB" "SELECT COUNT(*) FROM variances WHERE resolved = 0;")
if [[ "$VARIANCE_COUNT" -gt 0 ]]; then
  sqlite3 "$ACCOUNTING_DB" << EOF
.mode column
.headers on
SELECT id, variance_type, amount, severity, created_at FROM variances WHERE resolved = 0 ORDER BY severity DESC;
EOF
else
  echo "   None — all clear"
fi
