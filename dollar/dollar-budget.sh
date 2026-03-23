#!/bin/bash
# Dollar Persona - Budget Management

set -e

DB_PATH="${1:-/root/.openclaw/workspace/dollar/dollar.db}"
shift || true

# Colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

usage() {
    cat << EOF
Usage: $0 [database] <command> [args]

Commands:
  list                    List all budgets
  set <name> <period> <amount> [currency] [start_date]  Set a budget
  add <budget_id> <transaction_id> <amount>             Record budget usage
  check <name>           Check budget status
  close <name> [end_date] Close a budget

Periods: daily, weekly, monthly
Currency: USD (default), BTC, etc.

Examples:
  $0 list
  $0 set engineering monthly 1000 USD
  $0 check engineering
  $0 add 1 150 50.00   # Budget ID 1, Transaction ID 150, amount $50
EOF
    exit 1
}

# Check database
if [ ! -f "$DB_PATH" ]; then
    echo -e "${YELLOW}⚠️  Database not found. Run ./dollar-init.sh first${NC}"
    exit 1
fi

# If first arg is a .db file, treat as DB_PATH
if [[ "$1" == *.db ]]; then
    DB_PATH="$1"
    shift
fi

COMMAND="${1:-list}"
shift || true

case "$COMMAND" in
    list)
        echo -e "${BLUE}📅 Budget List${NC}"
        echo "-----------"
        sqlite3 -header -column "$DB_PATH" <<EOF
SELECT 
    id as ID,
    name as Name,
    period as Period,
    amount as Amount,
    currency as Currency,
    start_date as "Start",
    end_date as "End",
    COALESCE((SELECT SUM(amount) FROM budget_usage bu WHERE bu.budget_id = budgets.id), 0) as Spent,
    amount - COALESCE((SELECT SUM(amount) FROM budget_usage bu WHERE bu.budget_id = budgets.id), 0) as Remaining
FROM budgets
ORDER BY start_date DESC;
EOF
        ;;
        
    set)
        NAME="$1"
        PERIOD="$2"
        AMOUNT="$3"
        CURRENCY="${4:-USD}"
        START_DATE="${5:-$(date +%Y-%m-%d)}"
        
        if [ -z "$NAME" ] || [ -z "$PERIOD" ] || [ -z "$AMOUNT" ]; then
            echo -e "${RED}❌ Missing arguments for 'set' command${NC}"
            usage
        fi
        
        # Check if budget exists
        EXISTS=$(sqlite3 "$DB_PATH" "SELECT 1 FROM budgets WHERE name = '$NAME' AND (end_date IS NULL OR end_date >= date('now'))")
        if [ -n "$EXISTS" ]; then
            echo -e "${YELLOW}⚠️  Budget '$NAME' already exists. Updating...${NC}"
            sqlite3 "$DB_PATH" <<EOF
UPDATE budgets 
SET 
    period = '$PERIOD',
    amount = $AMOUNT,
    currency = '$CURRENCY',
    start_date = '$START_DATE',
    end_date = NULL,
    updated_at = CURRENT_TIMESTAMP
WHERE name = '$NAME';
EOF
        else
            sqlite3 "$DB_PATH" <<EOF
INSERT INTO budgets (name, period, amount, currency, start_date)
VALUES ('$NAME', '$PERIOD', $AMOUNT, '$CURRENCY', '$START_DATE');
EOF
        fi
        
        BUDGET_ID=$(sqlite3 "$DB_PATH" "SELECT id FROM budgets WHERE name = '$NAME' ORDER BY id DESC LIMIT 1")
        echo -e "${GREEN}✅ Budget '$NAME' set: $AMOUNT $CURRENCY ($PERIOD) (ID: $BUDGET_ID)${NC}"
        ;;
        
    add)
        BUDGET_ID="$1"
        TRANSACTION_ID="$2"
        AMOUNT="$3"
        
        if [ -z "$BUDGET_ID" ] || [ -z "$TRANSACTION_ID" ] || [ -z "$AMOUNT" ]; then
            echo -e "${RED}❌ Missing arguments for 'add' command${NC}"
            usage
        fi
        
        # Verify budget exists
        BUDGET_EXISTS=$(sqlite3 "$DB_PATH" "SELECT 1 FROM budgets WHERE id = $BUDGET_ID")
        if [ -z "$BUDGET_EXISTS" ]; then
            echo -e "${RED}❌ Budget ID $BUDGET_ID not found${NC}"
            exit 1
        fi
        
        # Verify transaction exists
        TX_EXISTS=$(sqlite3 "$DB_PATH" "SELECT 1 FROM transactions WHERE id = $TRANSACTION_ID")
        if [ -z "$TX_EXISTS" ]; then
            echo -e "${YELLOW}⚠️  Transaction ID $TRANSACTION_ID not found. Still adding budget usage.${NC}"
        fi
        
        sqlite3 "$DB_PATH" <<EOF
INSERT INTO budget_usage (budget_id, transaction_id, amount, date)
VALUES ($BUDGET_ID, $TRANSACTION_ID, $AMOUNT, date('now'));
EOF
        
        # Mint Shannon for budget compliance (if under budget)
        BUDGET_AMOUNT=$(sqlite3 "$DB_PATH" "SELECT amount FROM budgets WHERE id = $BUDGET_ID")
        SPENT=$(sqlite3 "$DB_PATH" "SELECT COALESCE(SUM(amount), 0) FROM budget_usage WHERE budget_id = $BUDGET_ID")
        if [ "$(echo "$SPENT <= $BUDGET_AMOUNT" | bc -l 2>/dev/null)" -eq 1 ]; then
            SHANNON=5
            sqlite3 "$DB_PATH" <<EOF
INSERT INTO shannon_events 
    (date, agent, event_type, amount_usd, shannon_minted, description)
VALUES 
    (date('now'), 'dollar', 'budget_compliance', $AMOUNT, $SHANNON, 'Budget usage within limits');
EOF
            echo -e "${GREEN}🎉 Minted $SHANNON Shannon for budget compliance${NC}"
        fi
        
        echo -e "${GREEN}✅ Budget usage recorded${NC}"
        ;;
        
    check)
        NAME="$1"
        if [ -z "$NAME" ]; then
            echo -e "${RED}❌ Missing budget name${NC}"
            usage
        fi
        
        echo -e "${BLUE}📊 Budget Status: $NAME${NC}"
        echo "----------------------"
        sqlite3 -header -column "$DB_PATH" <<EOF
SELECT 
    name as Name,
    period as Period,
    amount as Budget,
    currency as Currency,
    start_date as "Start",
    end_date as "End",
    COALESCE((SELECT SUM(amount) FROM budget_usage bu WHERE bu.budget_id = budgets.id), 0) as Spent,
    amount - COALESCE((SELECT SUM(amount) FROM budget_usage bu WHERE bu.budget_id = budgets.id), 0) as Remaining,
    CASE 
        WHEN COALESCE((SELECT SUM(amount) FROM budget_usage bu WHERE bu.budget_id = budgets.id), 0) > amount THEN 'OVER'
        WHEN COALESCE((SELECT SUM(amount) FROM budget_usage bu WHERE bu.budget_id = budgets.id), 0) > amount * 0.8 THEN 'WARNING'
        ELSE 'OK'
    END as Status
FROM budgets
WHERE name = '$NAME';
EOF
        
        # Show recent usage
        echo ""
        echo "Recent Usage:"
        sqlite3 -header -column "$DB_PATH" <<EOF
SELECT 
    bu.date as Date,
    bu.amount as Amount,
    t.description as Description
FROM budget_usage bu
LEFT JOIN transactions t ON t.id = bu.transaction_id
WHERE bu.budget_id = (SELECT id FROM budgets WHERE name = '$NAME' LIMIT 1)
ORDER BY bu.date DESC
LIMIT 5;
EOF
        ;;
        
    close)
        NAME="$1"
        END_DATE="${2:-$(date +%Y-%m-%d)}"
        
        if [ -z "$NAME" ]; then
            echo -e "${RED}❌ Missing budget name${NC}"
            usage
        fi
        
        sqlite3 "$DB_PATH" <<EOF
UPDATE budgets 
SET end_date = '$END_DATE',
    updated_at = CURRENT_TIMESTAMP
WHERE name = '$NAME' AND (end_date IS NULL OR end_date >= date('now'));
EOF
        
        echo -e "${GREEN}✅ Budget '$NAME' closed as of $END_DATE${NC}"
        ;;
        
    *)
        echo -e "${RED}❌ Unknown command: $COMMAND${NC}"
        usage
        ;;
esac