#!/bin/bash
# Agency Ledger Entry Tool
# 
# Records double-entry transactions (deposits, settlements, etc)
# Maintains balanced journal
# Cost: $0.00 (Tier 0 — bash + sqlite3)

set -e

WALLET_DIR="${HOME}/.agency-wallet"
ACCOUNTING_DB="${WALLET_DIR}/accounting.db"

timestamp() {
  date -u +"%Y-%m-%dT%H:%M:%SZ"
}

# Initialize DB if needed
ensure_db() {
  if [[ ! -f "$ACCOUNTING_DB" ]]; then
    sqlite3 "$ACCOUNTING_DB" < "$(dirname "$0")/accounting.sql"
  fi
}

# Record a crypto deposit (creates balanced entry)
record_deposit() {
  local amount="$1"
  local crypto_type="$2"
  local tx_hash="$3"
  local from_address="$4"
  local to_address="$5"
  
  ensure_db
  
  echo "Recording deposit: $amount $crypto_type (tx: $tx_hash)"
  
  sqlite3 "$ACCOUNTING_DB" << EOF
BEGIN TRANSACTION;

-- Insert deposit record
INSERT INTO deposits (crypto_type, amount, tx_hash, from_address, to_address, received_at)
VALUES ('$crypto_type', $amount, '$tx_hash', '$from_address', '$to_address', '$(timestamp)');

-- Create journal entry
INSERT INTO journal_entries (entry_date, reference, description)
VALUES ('$(timestamp)', '$tx_hash', 'Crypto donation received: $amount $crypto_type');

-- Get entry ID
SET @entry_id = last_insert_rowid();

-- DR: Wallet (asset increase)
INSERT INTO journal_lines (entry_id, account_id, amount)
SELECT @entry_id, id, $amount FROM accounts WHERE account_number = '1000';

-- CR: Donations Received (liability)
INSERT INTO journal_lines (entry_id, account_id, amount)
SELECT @entry_id, id, -$amount FROM accounts WHERE account_number = '2000';

COMMIT;
EOF

  echo "✅ Deposit recorded"
}

# Record Ampere settlement (creates balanced entry)
record_settlement() {
  local amount="$1"
  local tokens_purchased="$2"
  local invoice_number="$3"
  
  ensure_db
  
  echo "Recording settlement: $amount → $tokens_purchased tokens (invoice: $invoice_number)"
  
  sqlite3 "$ACCOUNTING_DB" << EOF
BEGIN TRANSACTION;

-- Insert settlement record
INSERT INTO settlements (invoice_number, amount, tokens_purchased, settled_at)
VALUES ('$invoice_number', $amount, $tokens_purchased, '$(timestamp)');

-- Create journal entry
INSERT INTO journal_entries (entry_date, reference, description)
VALUES ('$(timestamp)', '$invoice_number', 'Ampere settlement: $amount for $tokens_purchased tokens');

-- Get entry ID
SET @entry_id = last_insert_rowid();

-- DR: Token Expense (cost of tokens)
INSERT INTO journal_lines (entry_id, account_id, amount)
SELECT @entry_id, id, $amount FROM accounts WHERE account_number = '5000';

-- CR: Wallet (asset decrease)
INSERT INTO journal_lines (entry_id, account_id, amount)
SELECT @entry_id, id, -$amount FROM accounts WHERE account_number = '1000';

COMMIT;
EOF

  echo "✅ Settlement recorded"
}

# Show trial balance
show_trial_balance() {
  ensure_db
  
  echo "📊 TRIAL BALANCE (should sum to 0)"
  echo ""
  
  sqlite3 "$ACCOUNTING_DB" << EOF
.mode column
.headers on
SELECT account_number, name, type, COALESCE(balance, 0) as balance FROM trial_balance ORDER BY account_number;
EOF

  echo ""
  
  TOTAL=$(sqlite3 "$ACCOUNTING_DB" "SELECT COALESCE(SUM(balance), 0) FROM trial_balance;")
  if [[ $(echo "$TOTAL == 0" | bc) -eq 1 ]]; then
    echo "✅ Balanced (total = 0)"
  else
    echo "❌ Out of balance (total = $TOTAL)"
  fi
}

# Show deposits
show_deposits() {
  ensure_db
  
  echo "💰 DEPOSITS RECEIVED"
  echo ""
  
  sqlite3 "$ACCOUNTING_DB" << EOF
.mode column
.headers on
SELECT id, crypto_type, amount, status, received_at FROM deposits ORDER BY received_at DESC;
EOF
}

# Show settlements
show_settlements() {
  ensure_db
  
  echo "💳 AMPERE SETTLEMENTS"
  echo ""
  
  sqlite3 "$ACCOUNTING_DB" << EOF
.mode column
.headers on
SELECT id, invoice_number, amount, tokens_purchased, settled_at FROM settlements ORDER BY settled_at DESC;
EOF
}

# Main
case "${1:-help}" in
  deposit)
    record_deposit "$2" "$3" "$4" "$5" "$6"
    ;;
  settlement)
    record_settlement "$2" "$3" "$4"
    ;;
  balance)
    show_trial_balance
    ;;
  deposits)
    show_deposits
    ;;
  settlements)
    show_settlements
    ;;
  help|--help|-h)
    cat << EOF
💼 Agency Ledger Entry Tool

Usage: ledger.sh <command> [args]

Commands:
  deposit <amount> <type> <tx_hash> <from> <to>
      Record a crypto deposit
      Example: ledger.sh deposit 1.22 USDC 0x123... 0xaaa... 0xbbb...
  
  settlement <amount> <tokens> <invoice>
      Record Ampere token settlement
      Example: ledger.sh settlement 20.00 20000 INV-20260314-001
  
  balance
      Show trial balance (debits - credits should = 0)
  
  deposits
      Show all deposits received
  
  settlements
      Show all Ampere settlements
  
  help
      Show this help

All transactions are double-entry balanced. The ledger is auditable.
EOF
    ;;
  *)
    echo "❌ Unknown command: $1"
    echo "   Run: ledger.sh help"
    exit 1
    ;;
esac
