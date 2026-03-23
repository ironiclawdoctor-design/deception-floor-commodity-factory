#!/bin/bash
# Dollar Persona - Log Transaction (Double-Entry Accounting)

set -e

DB_PATH="${1:-/root/.openclaw/workspace/dollar/dollar.db}"
shift || true

# Colors
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m'

usage() {
    cat << EOF
Usage: $0 [database] "Description" <amount> <currency> <debit_account> <credit_account> [reference]

Example:
  $0 "Payment received from client" 100.00 USD "Accounts Receivable" "Revenue - Services" INV-001
  $0 "Pay hosting bill" 50.00 USD "Expense - Hosting" "PayPal Balance" PAY-002

Account aliases:
  cash, paypal, bank, btc, usdc, revenue, expense, ar, ap, equity

If only amount provided, assumes USD revenue to cash.
EOF
    exit 1
}

# If no arguments, show usage
if [ $# -lt 1 ]; then
    usage
fi

# Parse arguments
if [ $# -eq 1 ]; then
    # Assume database path is first arg, but we already have DB_PATH
    # Actually if only one arg, treat as description? Let's handle.
    echo -e "${RED}❌ Insufficient arguments${NC}"
    usage
fi

# If first argument is a file path (ends with .db), treat as DB_PATH
if [[ "$1" == *.db ]]; then
    DB_PATH="$1"
    shift
fi

DESCRIPTION="$1"
AMOUNT="$2"
CURRENCY="${3:-USD}"
DEBIT_ACCOUNT="${4:-cash}"
CREDIT_ACCOUNT="${5:-revenue}"
REFERENCE="${6:-}"

# Validate amount
if ! [[ "$AMOUNT" =~ ^[0-9]+(\.[0-9]+)?$ ]]; then
    echo -e "${RED}❌ Invalid amount: $AMOUNT${NC}"
    exit 1
fi

# Map account aliases to actual account names
declare -A ACCOUNT_MAP=(
    ["cash"]="PayPal Balance"
    ["paypal"]="PayPal Balance"
    ["bank"]="Bank Account"
    ["btc"]="Bitcoin Wallet"
    ["usdc"]="USDC Wallet"
    ["ar"]="Accounts Receivable"
    ["ap"]="Accounts Payable"
    ["equity"]="Agency Equity"
    ["revenue"]="Revenue - Services"
    ["expense"]="Expense - Development"
)

DEBIT_NAME="${ACCOUNT_MAP[$DEBIT_ACCOUNT]:-$DEBIT_ACCOUNT}"
CREDIT_NAME="${ACCOUNT_MAP[$CREDIT_ACCOUNT]:-$CREDIT_ACCOUNT}"

echo "💰 Logging transaction: $DESCRIPTION"
echo "  Amount: $AMOUNT $CURRENCY"
echo "  Debit: $DEBIT_NAME"
echo "  Credit: $CREDIT_NAME"
[ -n "$REFERENCE" ] && echo "  Reference: $REFERENCE"

# Get account IDs
DEBIT_ID=$(sqlite3 "$DB_PATH" "SELECT id FROM accounts WHERE name = '$DEBIT_NAME' LIMIT 1")
CREDIT_ID=$(sqlite3 "$DB_PATH" "SELECT id FROM accounts WHERE name = '$CREDIT_NAME' LIMIT 1")

if [ -z "$DEBIT_ID" ]; then
    echo -e "${RED}❌ Debit account not found: $DEBIT_NAME${NC}"
    echo "Available accounts:"
    sqlite3 "$DB_PATH" "SELECT name FROM accounts ORDER BY type, name"
    exit 1
fi

if [ -z "$CREDIT_ID" ]; then
    echo -e "${RED}❌ Credit account not found: $CREDIT_NAME${NC}"
    echo "Available accounts:"
    sqlite3 "$DB_PATH" "SELECT name FROM accounts ORDER BY type, name"
    exit 1
fi

# Insert transaction
sqlite3 "$DB_PATH" <<EOF
INSERT INTO transactions 
    (date, description, amount, currency, debit_account_id, credit_account_id, reference, status)
VALUES 
    (date('now'), '$DESCRIPTION', $AMOUNT, '$CURRENCY', $DEBIT_ID, $CREDIT_ID, '$REFERENCE', 'cleared');
EOF

TRANSACTION_ID=$(sqlite3 "$DB_PATH" "SELECT last_insert_rowid()")

# Mint Shannon for revenue transactions
if [[ "$CREDIT_NAME" == *"Revenue"* ]]; then
    SHANNON=$(( $(echo "$AMOUNT / 10" | bc -l 2>/dev/null | cut -d. -f1) ))
    if [ "$SHANNON" -lt 1 ]; then
        SHANNON=1
    fi
    sqlite3 "$DB_PATH" <<EOF
INSERT INTO shannon_events 
    (date, agent, event_type, amount_usd, shannon_minted, description)
VALUES 
    (date('now'), 'dollar', 'revenue', $AMOUNT, $SHANNON, '$DESCRIPTION');
EOF
    echo -e "${GREEN}🎉 Minted $SHANNON Shannon for revenue${NC}"
fi

echo -e "${GREEN}✅ Transaction logged (ID: $TRANSACTION_ID)${NC}"

# Show updated trial balance
echo ""
echo "📊 Updated Trial Balance Summary"
sqlite3 -header -column "$DB_PATH" <<EOF
SELECT 
    type as Type,
    name as Account,
    balance as Balance
FROM trial_balance
WHERE balance != 0
ORDER BY type, name;
EOF