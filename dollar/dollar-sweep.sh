#!/bin/bash
# Dollar Persona - Daily Sweep & Collateral Audit
# Checks Cash App backing, mints Shannon, audits supply

set -e

DB_PATH="${1:-/root/.openclaw/workspace/dollar/dollar.db}"
CASHAPP_HANDLE="${2:-DollarAgency}"  # Cashtag: $DollarAgency
BACKING_USD="${3:-}"  # Optional manual override (if no API)

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
BLUE='\033[0;34m'
NC='\033[0m'

echo -e "${BLUE}💰 Dollar Persona - Daily Sweep${NC}"
echo "================================="
echo "Date: $(date)"
echo "Database: $DB_PATH"
echo "Cash App: \$$CASHAPP_HANDLE"
echo ""

# Check database
if [ ! -f "$DB_PATH" ]; then
    echo -e "${RED}❌ Database not found. Run ./dollar-init.sh first.${NC}"
    exit 1
fi

# 1. CHECK_BACKING
echo -e "${GREEN}1. Checking Cash App backing...${NC}"

if [ -n "$BACKING_USD" ]; then
    CASHAPP_BALANCE="$BACKING_USD"
    echo -e "   Using manual override: \$$CASHAPP_BALANCE"
    SOURCE="manual"
else
    # Attempt to fetch via Camoufox (if Chrome tab attached)
    echo -e "   ${YELLOW}Attempting Camoufox polling of cash.app/\$$CASHAPP_HANDLE...${NC}"
    
    # Check if Camoufox is available (browser tool)
    # We'll try a simple curl fallback first (public page may not show balance)
    # For now, placeholder: ask user to input balance
    echo -e "   ${YELLOW}Camoufox polling not yet implemented.${NC}"
    echo -e "   ${YELLOW}Please provide current Cash App balance (USD):${NC}"
    read -p "   Balance: " CASHAPP_BALANCE
    if ! [[ "$CASHAPP_BALANCE" =~ ^[0-9]+(\.[0-9]+)?$ ]]; then
        echo -e "   ${RED}Invalid amount. Using last known backing from database.${NC}"
        CASHAPP_BALANCE=$(sqlite3 "$DB_PATH" "SELECT total_backing_usd FROM exchange_rates ORDER BY date DESC LIMIT 1")
    fi
    SOURCE="cashapp"
fi

# Log backing transaction (if changed)
LAST_BACKING=$(sqlite3 "$DB_PATH" "SELECT total_backing_usd FROM exchange_rates ORDER BY date DESC LIMIT 1")
if [ "$(echo "$CASHAPP_BALANCE != $LAST_BACKING" | bc -l 2>/dev/null)" -eq 1 ]; then
    echo -e "   Backing changed: \$$LAST_BACKING → \$$CASHAPP_BALANCE"
    
    # Record adjustment transaction
    DIFF=$(echo "$CASHAPP_BALANCE - $LAST_BACKING" | bc -l)
    if [ "$(echo "$DIFF > 0" | bc -l)" -eq 1 ]; then
        DESC="Cash App deposit"
        DEBIT="Cash App Balance ($DollarAgency)"
        CREDIT="Agency Equity"
    else
        DESC="Cash App withdrawal"
        DEBIT="Agency Equity"
        CREDIT="Cash App Balance ($DollarAgency)"
        DIFF=$(echo "$DIFF * -1" | bc -l)
    fi
    
    ./dollar-log.sh "$DB_PATH" "$DESC" "$DIFF" USD "$DEBIT" "$CREDIT" "sweep-$(date +%Y%m%d)"
    echo -e "   ${GREEN}✅ Backing adjustment logged${NC}"
else
    echo -e "   ${GREEN}Backing unchanged: \$$CASHAPP_BALANCE${NC}"
fi

# 2. UPDATE_EXCHANGE_RATE (fixed peg for now)
RATE_SHANNON_PER_USD=10.0000
RATE_USD_PER_SHANNON=0.1000
TOTAL_SHANNON_SUPPLY=$(echo "$CASHAPP_BALANCE * $RATE_SHANNON_PER_USD" | bc -l | cut -d. -f1)

echo -e "${GREEN}2. Updating exchange rate...${NC}"
echo "   Rate: $RATE_SHANNON_PER_USD Shannon/$1"
echo "   Backing: \$$CASHAPP_BALANCE"
echo "   Shannon supply: $TOTAL_SHANNON_SUPPLY"

sqlite3 "$DB_PATH" <<EOF
INSERT OR REPLACE INTO exchange_rates 
    (date, shannon_per_usd, usd_per_shannon, total_backing_usd, total_shannon_supply)
VALUES (
    date('now'),
    $RATE_SHANNON_PER_USD,
    $RATE_USD_PER_SHANNON,
    $CASHAPP_BALANCE,
    $TOTAL_SHANNON_SUPPLY
);
EOF

# 3. MINT_SHANNON (if backing increased)
if [ "$(echo "$CASHAPP_BALANCE > $LAST_BACKING" | bc -l)" -eq 1 ]; then
    INCREASE=$(echo "$CASHAPP_BALANCE - $LAST_BACKING" | bc -l)
    SHANNON_TO_MINT=$(echo "$INCREASE * $RATE_SHANNON_PER_USD" | bc -l | cut -d. -f1)
    
    if [ "$SHANNON_TO_MINT" -gt 0 ]; then
        echo -e "${GREEN}3. Minting new Shannon...${NC}"
        echo "   Increase: \$$INCREASE"
        echo "   Minting: $SHANNON_TO_MINT Shannon to Treasury"
        
        # Log minting transaction (Shannon Treasury asset increase)
        # Since Shannon is not a currency in transactions table, we log to shannon_events
        sqlite3 "$DB_PATH" <<EOF
INSERT INTO shannon_events 
    (date, agent, event_type, amount_usd, shannon_minted, description)
VALUES (
    date('now'),
    'dollar',
    'revenue',
    $INCREASE,
    $SHANNON_TO_MINT,
    'Shannon minted from backing increase'
);
EOF
        echo -e "   ${GREEN}✅ $SHANNON_TO_MINT Shannon minted${NC}"
    fi
else
    echo -e "${GREEN}3. No backing increase, no new Shannon minted.${NC}"
fi

# 4. AUDIT
echo -e "${GREEN}4. Running collateral audit...${NC}"
CALC_SUPPLY=$(sqlite3 "$DB_PATH" "SELECT total_shannon_supply FROM exchange_rates WHERE date = date('now')")
CALC_BACKING=$(sqlite3 "$DB_PATH" "SELECT total_backing_usd FROM exchange_rates WHERE date = date('now')")
REQUIRED_BACKING=$(echo "$CALC_SUPPLY * $RATE_USD_PER_SHANNON" | bc -l)

if [ "$(echo "$CALC_BACKING >= $REQUIRED_BACKING" | bc -l)" -eq 1 ]; then
    echo -e "   ${GREEN}✅ Collateral sufficient${NC}"
    echo "   Backing: \$$CALC_BACKING"
    echo "   Required: \$$REQUIRED_BACKING"
    echo "   Surplus: \$$(echo "$CALC_BACKING - $REQUIRED_BACKING" | bc -l)"
    STATUS="healthy"
else
    echo -e "   ${RED}❌ Collateral deficit!${NC}"
    echo "   Backing: \$$CALC_BACKING"
    echo "   Required: \$$REQUIRED_BACKING"
    echo "   Deficit: \$$(echo "$REQUIRED_BACKING - $CALC_BACKING" | bc -l)"
    STATUS="deficit"
fi

# Log audit result as confession
sqlite3 "$DB_PATH" <<EOF
INSERT INTO confessions 
    (date, agent, failure_type, platform, error_code, description, doctrine_extracted, shannon_minted)
VALUES (
    date('now'),
    'dollar',
    'collateral_audit',
    'cashapp',
    '$STATUS',
    'Daily collateral audit: backing=\$$CALC_BACKING, required=\$$REQUIRED_BACKING',
    'Rule: Backing must exceed Shannon supply × rate. Deficit triggers minting pause.',
    5
);
EOF

# 5. REPORT
echo -e "${GREEN}5. Generating sweep report...${NC}"
sqlite3 -header -column "$DB_PATH" <<EOF
SELECT 
    date as Date,
    total_backing_usd as "Backing USD",
    total_shannon_supply as "Shannon Supply",
    shannon_per_usd as "Shannon/$",
    usd_per_shannon as "$/Shannon"
FROM exchange_rates
WHERE date = date('now');
EOF

echo ""
echo -e "${GREEN}✅ Daily sweep complete${NC}"
echo ""
echo "Next:"
echo "  - Run ./dollar-market.sh rate to see current rate"
echo "  - Run ./dollar-report.sh for full financial report"
echo "  - Set cron job: 0 9 * * * cd /root/.openclaw/workspace/dollar && ./dollar-sweep.sh"