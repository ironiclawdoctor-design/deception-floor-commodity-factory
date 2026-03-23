#!/bin/bash
# Dollar Persona - Financial Report

set -e

DB_PATH="${1:-/root/.openclaw/workspace/dollar/dollar.db}"
OUTPUT="${2:-terminal}"  # terminal, markdown, json

# Colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m'

echo -e "${BLUE}💰 Dollar Persona - Financial Report${NC}"
echo "================================="
echo "Date: $(date)"
echo "Database: $DB_PATH"
echo ""

# Check database
if [ ! -f "$DB_PATH" ]; then
    echo -e "${YELLOW}⚠️  Database not found. Run ./dollar-init.sh first${NC}"
    exit 1
fi

# 1. Executive Summary
echo -e "${GREEN}📈 Executive Summary${NC}"
echo "-----------------"
sqlite3 -header -column "$DB_PATH" <<EOF
SELECT 
    date as Date,
    total_assets as "Total Assets",
    total_liabilities as "Total Liabilities",
    net_worth as "Net Worth"
FROM daily_usd_position
ORDER BY date DESC
LIMIT 7;
EOF

# 2. Recent Transactions
echo ""
echo -e "${GREEN}📝 Recent Transactions (Last 10)${NC}"
echo "--------------------------------"
sqlite3 -header -column "$DB_PATH" <<EOF
SELECT 
    date as Date,
    description as Description,
    amount as Amount,
    currency as Currency,
    (SELECT name FROM accounts WHERE id = debit_account_id) as Debit,
    (SELECT name FROM accounts WHERE id = credit_account_id) as Credit,
    status as Status
FROM transactions
ORDER BY date DESC, id DESC
LIMIT 10;
EOF

# 3. Budget Status
echo ""
echo -e "${GREEN}📅 Budget Status${NC}"
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

# 4. Shannon Earnings
echo ""
echo -e "${GREEN}🪙 Shannon Earnings${NC}"
echo "-------------------"
sqlite3 -header -column "$DB_PATH" <<EOF
SELECT 
    event_type as "Event Type",
    COUNT(*) as "Count",
    SUM(amount_usd) as "Total USD",
    SUM(shannon_minted) as "Total Shannon"
FROM shannon_events
GROUP BY event_type
ORDER BY SUM(shannon_minted) DESC;
EOF

# 5. Account Balances
echo ""
echo -e "${GREEN}🏦 Account Balances${NC}"
echo "-------------------"
sqlite3 -header -column "$DB_PATH" <<EOF
SELECT 
    a.type as Type,
    a.name as Account,
    SUM(CASE WHEN t.debit_account_id = a.id THEN t.amount ELSE 0 END) -
    SUM(CASE WHEN t.credit_account_id = a.id THEN t.amount ELSE 0 END) as Balance,
    a.currency as Currency
FROM accounts a
LEFT JOIN transactions t ON t.debit_account_id = a.id OR t.credit_account_id = a.id
WHERE t.status != 'void' OR t.id IS NULL
GROUP BY a.id
HAVING Balance != 0
ORDER BY a.type, a.name;
EOF

# 6. Reconciliation Status
echo ""
echo -e "${GREEN}🔍 Reconciliation Status${NC}"
echo "------------------------"
sqlite3 -header -column "$DB_PATH" <<EOF
SELECT 
    date as Date,
    (SELECT name FROM accounts WHERE id = account_id) as Account,
    external_balance as "External",
    ledger_balance as "Ledger",
    difference as Difference,
    status as Status
FROM reconciliations
WHERE status != 'resolved'
ORDER BY date DESC;
EOF

# 7. Recommendations
echo ""
echo -e "${GREEN}💡 Recommendations${NC}"
echo "----------------"

# Check for unbalanced trial balance
TRIAL_BALANCE=$(sqlite3 "$DB_PATH" "SELECT SUM(balance) FROM trial_balance")
if [ "$TRIAL_BALANCE" != "0" ] && [ "$TRIAL_BALANCE" != "" ]; then
    echo -e "${YELLOW}⚠️  Trial Balance is out of balance by $TRIAL_BALANCE. Investigate.${NC}"
fi

# Check for overdue reconciliations
OVERDUE_REC=$(sqlite3 "$DB_PATH" "SELECT COUNT(*) FROM reconciliations WHERE status = 'open' AND date < date('now', '-7 days')")
if [ "$OVERDUE_REC" -gt 0 ]; then
    echo -e "${YELLOW}⚠️  $OVERDUE_REC reconciliations overdue by >7 days. Resolve soon.${NC}"
fi

# Check for budget overruns
BUDGET_OVER=$(sqlite3 "$DB_PATH" "SELECT COUNT(*) FROM budgets WHERE amount < COALESCE((SELECT SUM(amount) FROM budget_usage bu WHERE bu.budget_id = budgets.id), 0)")
if [ "$BUDGET_OVER" -gt 0 ]; then
    echo -e "${YELLOW}⚠️  $BUDGET_OVER budgets are over limit. Review spending.${NC}"
fi

# Check for pending transactions
PENDING_TX=$(sqlite3 "$DB_PATH" "SELECT COUNT(*) FROM transactions WHERE status = 'pending'")
if [ "$PENDING_TX" -gt 0 ]; then
    echo -e "${YELLOW}⚠️  $PENDING_TX transactions pending clearance. Update status.${NC}"
fi

echo ""
echo -e "${GREEN}✅ Report generated successfully${NC}"
echo ""
echo "Next actions:"
echo "1. Run ./dollar-balance.sh for detailed balance check"
echo "2. Log transactions with ./dollar-log.sh"
echo "3. Set budgets with ./dollar-budget.sh"
echo "4. Reconcile accounts with ./dollar-reconcile.sh"