#!/bin/bash
# Dollar Persona - Check Financial Balances

set -e

DB_PATH="${1:-/root/.openclaw/workspace/dollar/dollar.db}"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo "💰 Dollar Persona - Balance Check"
echo "================================="

# Check if database exists
if [ ! -f "$DB_PATH" ]; then
    echo -e "${RED}❌ Database not found. Run ./dollar-init.sh first${NC}"
    exit 1
fi

# Get USD balances from ledger
echo ""
echo "📊 Ledger Balances (USD)"
echo "-----------------------"
sqlite3 -header -column "$DB_PATH" <<EOF
SELECT 
    a.name as Account,
    a.type as Type,
    SUM(CASE WHEN t.debit_account_id = a.id THEN t.amount ELSE 0 END) -
    SUM(CASE WHEN t.credit_account_id = a.id THEN t.amount ELSE 0 END) as Balance
FROM accounts a
LEFT JOIN transactions t ON t.debit_account_id = a.id OR t.credit_account_id = a.id
WHERE t.status != 'void' OR t.id IS NULL
GROUP BY a.id
HAVING Balance != 0
ORDER BY a.type, a.name;
EOF

# Get trial balance (should sum to zero)
TRIAL_BALANCE=$(sqlite3 "$DB_PATH" "SELECT SUM(balance) FROM trial_balance")
if [ "$TRIAL_BALANCE" != "0" ] && [ "$TRIAL_BALANCE" != "" ]; then
    echo -e "${RED}⚠️  Trial Balance out of balance: $TRIAL_BALANCE${NC}"
else
    echo -e "${GREEN}✅ Trial Balance check passed${NC}"
fi

# Check PayPal balance (if credentials available)
echo ""
echo "🔗 External Balances"
echo "-------------------"
if [ -n "$PAYPAL_CLIENT_ID" ] && [ -n "$PAYPAL_CLIENT_SECRET" ]; then
    echo -e "${YELLOW}PayPal credentials detected (balance check not yet implemented)${NC}"
    # TODO: Integrate with paypal-secure-access skill
else
    echo -e "${YELLOW}PayPal credentials not set (set PAYPAL_CLIENT_ID & PAYPAL_CLIENT_SECRET)${NC}"
fi

# Check crypto balances via existing wallet infrastructure
CRYPTO_WALLET_DIR="/root/.openclaw/workspace/agency-wallet"
if [ -d "$CRYPTO_WALLET_DIR" ]; then
    echo -e "${YELLOW}Crypto wallet directory exists (balance check not yet implemented)${NC}"
    # TODO: Integrate with check-balance.sh
else
    echo -e "${YELLOW}Crypto wallet directory not found${NC}"
fi

# Budget status
echo ""
echo "📅 Budget Status"
echo "---------------"
sqlite3 -header -column "$DB_PATH" <<EOF
SELECT 
    name as Budget,
    period as Period,
    amount as Budget,
    COALESCE((SELECT SUM(amount) FROM budget_usage bu WHERE bu.budget_id = budgets.id), 0) as Spent,
    amount - COALESCE((SELECT SUM(amount) FROM budget_usage bu WHERE bu.budget_id = budgets.id), 0) as Remaining,
    CASE 
        WHEN COALESCE((SELECT SUM(amount) FROM budget_usage bu WHERE bu.budget_id = budgets.id), 0) > amount THEN 'OVER'
        WHEN COALESCE((SELECT SUM(amount) FROM budget_usage bu WHERE bu.budget_id = budgets.id), 0) > amount * 0.8 THEN 'WARNING'
        ELSE 'OK'
    END as Status
FROM budgets
WHERE end_date IS NULL OR end_date >= date('now');
EOF

# Shannon earnings
echo ""
echo "🪙 Shannon Earnings (Financial Activities)"
echo "----------------------------------------"
sqlite3 -header -column "$DB_PATH" <<EOF
SELECT 
    date as Date,
    agent as Agent,
    event_type as Event,
    amount_usd as "Amount USD",
    shannon_minted as "Shannon Minted"
FROM shannon_events
ORDER BY date DESC
LIMIT 5;
EOF

TOTAL_SHANNON=$(sqlite3 "$DB_PATH" "SELECT SUM(shannon_minted) FROM shannon_events")
echo "Total Shannon minted: ${GREEN}$TOTAL_SHANNON${NC}"

echo ""
echo "✅ Balance check complete"