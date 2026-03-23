#!/bin/bash
# Dollar Persona - Shannon/USD Market Operations
# Buy/sell Shannon at fixed peg, track trades, manage Treasury

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
  rate                    Show current exchange rate
  buy <usd> <trader>      Buy Shannon with USD (logical)
  sell <shannon> <trader> Sell Shannon for USD (logical)
  history [trader]        Show trade history
  treasury                Show Treasury/Reserve balances

Examples:
  $0 rate
  $0 buy 10.50 fiesta     # Buy Shannon worth $10.50
  $0 sell 150 junior      # Sell 150 Shannon
  $0 history fiesta
EOF
    exit 1
}

# Check database
if [ ! -f "$DB_PATH" ]; then
    echo -e "${RED}❌ Database not found. Run ./dollar-init.sh first.${NC}"
    exit 1
fi

# If first arg is a .db file, treat as DB_PATH
if [[ "$1" == *.db ]]; then
    DB_PATH="$1"
    shift
fi

COMMAND="${1:-rate}"
shift || true

case "$COMMAND" in
    rate)
        echo -e "${BLUE}📊 Shannon/USD Exchange Rate${NC}"
        echo "----------------------------"
        sqlite3 -header -column "$DB_PATH" <<EOF
SELECT 
    date as Date,
    total_backing_usd as "Backing USD",
    total_shannon_supply as "Shannon Supply",
    shannon_per_usd as "Shannon/$",
    usd_per_shannon as "$/Shannon",
    total_backing_usd / total_shannon_supply as "Backing/Shannon"
FROM exchange_rates
ORDER BY date DESC
LIMIT 1;
EOF
        
        # Show recent rate history
        echo ""
        echo "Recent rates:"
        sqlite3 -column "$DB_PATH" <<EOF
SELECT 
    date,
    shannon_per_usd,
    total_backing_usd
FROM exchange_rates
ORDER BY date DESC
LIMIT 5;
EOF
        ;;
        
    buy)
        USD_AMOUNT="$1"
        TRADER="$2"
        
        if [ -z "$USD_AMOUNT" ] || [ -z "$TRADER" ]; then
            echo -e "${RED}❌ Missing arguments. Usage: buy <usd> <trader>${NC}"
            usage
        fi
        
        # Get current rate
        RATE=$(sqlite3 "$DB_PATH" "SELECT shannon_per_usd FROM exchange_rates ORDER BY date DESC LIMIT 1")
        SHANNON_AMOUNT=$(echo "$USD_AMOUNT * $RATE" | bc -l | cut -d. -f1)
        
        echo -e "${BLUE}💰 Buy Order${NC}"
        echo "--------------"
        echo "Trader: $TRADER"
        echo "USD amount: \$$USD_AMOUNT"
        echo "Rate: $RATE Shannon/$1"
        echo "Shannon amount: $SHANNON_AMOUNT"
        
        # Check Treasury has enough Shannon
        TREASURY_SHANNON=$(sqlite3 "$DB_PATH" "SELECT shannon_minted FROM shannon_events WHERE description LIKE '%Treasury%' ORDER BY id DESC LIMIT 1")
        if [ -z "$TREASURY_SHANNON" ]; then
            TREASURY_SHANNON=0
        fi
        
        if [ "$SHANNON_AMOUNT" -gt "$TREASURY_SHANNON" ]; then
            echo -e "${YELLOW}⚠️  Treasury insufficient ($TREASURY_SHANNON Shannon). Minting new Shannon...${NC}"
            # Mint new Shannon (backing increased elsewhere)
        fi
        
        # Record trade (pending)
        sqlite3 "$DB_PATH" <<EOF
INSERT INTO market_trades 
    (date, type, usd_amount, shannon_amount, rate, trader, status)
VALUES (
    date('now'),
    'buy',
    $USD_AMOUNT,
    $SHANNON_AMOUNT,
    $RATE,
    '$TRADER',
    'pending'
);
EOF
        
        TRADE_ID=$(sqlite3 "$DB_PATH" "SELECT last_insert_rowid()")
        
        # Log transaction (USD → Shannon Treasury)
        ./dollar-log.sh "$DB_PATH" "Buy Shannon (trade #$TRADE_ID)" "$USD_AMOUNT" USD "USD Collateral" "Shannon Treasury" "trade-$TRADE_ID"
        
        # Log Shannon allocation (outside double-entry)
        sqlite3 "$DB_PATH" <<EOF
INSERT INTO shannon_events 
    (date, agent, event_type, amount_usd, shannon_minted, description)
VALUES (
    date('now'),
    '$TRADER',
    'revenue',
    $USD_AMOUNT,
    $SHANNON_AMOUNT,
    'Shannon purchase (trade #$TRADE_ID)'
);
EOF
        
        # Update trade status
        sqlite3 "$DB_PATH" "UPDATE market_trades SET status = 'completed' WHERE id = $TRADE_ID"
        
        echo -e "${GREEN}✅ Buy order completed${NC}"
        echo "Trade ID: $TRADE_ID"
        echo "Shannon credited to $TRADER's ledger (outside accounting)"
        ;;
        
    sell)
        SHANNON_AMOUNT="$1"
        TRADER="$2"
        
        if [ -z "$SHANNON_AMOUNT" ] || [ -z "$TRADER" ]; then
            echo -e "${RED}❌ Missing arguments. Usage: sell <shannon> <trader>${NC}"
            usage
        fi
        
        # Get current rate
        RATE=$(sqlite3 "$DB_PATH" "SELECT usd_per_shannon FROM exchange_rates ORDER BY date DESC LIMIT 1")
        USD_AMOUNT=$(echo "$SHANNON_AMOUNT * $RATE" | bc -l | xargs printf "%.2f")
        
        echo -e "${BLUE}💰 Sell Order${NC}"
        echo "---------------"
        echo "Trader: $TRADER"
        echo "Shannon amount: $SHANNON_AMOUNT"
        echo "Rate: $RATE $/Shannon"
        echo "USD amount: \$$USD_AMOUNT"
        
        # Check backing available (USD Collateral)
        COLLATERAL=$(sqlite3 "$DB_PATH" "SELECT balance FROM trial_balance WHERE account = 'USD Collateral'")
        if [ -z "$COLLATERAL" ]; then
            COLLATERAL=0
        fi
        
        if [ "$(echo "$USD_AMOUNT > $COLLATERAL" | bc -l)" -eq 1 ]; then
            echo -e "${YELLOW}⚠️  Insufficient collateral (\$$COLLATERAL). Sale may be delayed.${NC}"
            STATUS="pending"
        else
            STATUS="completed"
        fi
        
        # Record trade
        sqlite3 "$DB_PATH" <<EOF
INSERT INTO market_trades 
    (date, type, usd_amount, shannon_amount, rate, trader, status)
VALUES (
    date('now'),
    'sell',
    $USD_AMOUNT,
    $SHANNON_AMOUNT,
    $RATE,
    '$TRADER',
    '$STATUS'
);
EOF
        
        TRADE_ID=$(sqlite3 "$DB_PATH" "SELECT last_insert_rowid()")
        
        if [ "$STATUS" = "completed" ]; then
            # Log transaction (Shannon Treasury → USD Collateral)
            ./dollar-log.sh "$DB_PATH" "Sell Shannon (trade #$TRADE_ID)" "$USD_AMOUNT" USD "Shannon Treasury" "USD Collateral" "trade-$TRADE_ID"
            
            # Burn Shannon (record as negative mint)
            sqlite3 "$DB_PATH" <<EOF
INSERT INTO shannon_events 
    (date, agent, event_type, amount_usd, shannon_minted, description)
VALUES (
    date('now'),
    '$TRADER',
    'cost_saving',
    $USD_AMOUNT,
    -$SHANNON_AMOUNT,
    'Shannon sale (trade #$TRADE_ID)'
);
EOF
            echo -e "${GREEN}✅ Sell order completed${NC}"
            echo "USD \$$USD_AMOUNT released from collateral"
        else
            echo -e "${YELLOW}⏳ Sell order pending (insufficient collateral)${NC}"
            echo "Will complete when backing increases"
        fi
        
        echo "Trade ID: $TRADE_ID"
        ;;
        
    history)
        TRADER="$1"
        echo -e "${BLUE}📜 Trade History${NC}"
        echo "----------------"
        
        if [ -n "$TRADER" ]; then
            WHERE="WHERE trader = '$TRADER'"
            echo "Trader: $TRADER"
        else
            WHERE=""
            echo "All trades"
        fi
        
        sqlite3 -header -column "$DB_PATH" <<EOF
SELECT 
    id as ID,
    date as Date,
    type as Type,
    usd_amount as "USD",
    shannon_amount as "Shannon",
    rate as Rate,
    trader as Trader,
    status as Status
FROM market_trades
$WHERE
ORDER BY date DESC, id DESC
LIMIT 20;
EOF
        
        # Summary
        echo ""
        echo "Summary:"
        sqlite3 -column "$DB_PATH" <<EOF
SELECT 
    type,
    COUNT(*) as Trades,
    SUM(usd_amount) as "Total USD",
    SUM(shannon_amount) as "Total Shannon"
FROM market_trades
$WHERE
GROUP BY type;
EOF
        ;;
        
    treasury)
        echo -e "${BLUE}🏦 Treasury & Reserve Status${NC}"
        echo "---------------------------"
        
        # Treasury Shannon (minted but not sold)
        TREASURY_SHANNON=$(sqlite3 "$DB_PATH" <<EOF
SELECT 
    COALESCE(SUM(shannon_minted), 0) 
FROM shannon_events 
WHERE description LIKE '%Treasury%' OR description LIKE '%minted from backing%';
EOF
)
        
        # Sold Shannon
        SOLD_SHANNON=$(sqlite3 "$DB_PATH" "SELECT COALESCE(SUM(shannon_amount), 0) FROM market_trades WHERE type = 'buy' AND status = 'completed'")
        
        # Reserve Shannon (excess)
        RESERVE_SHANNON=$(sqlite3 "$DB_PATH" <<EOF
SELECT 
    COALESCE(SUM(shannon_minted), 0) 
FROM shannon_events 
WHERE description LIKE '%Reserve%';
EOF
)
        
        # USD Collateral balance
        USD_COLLATERAL=$(sqlite3 "$DB_PATH" "SELECT balance FROM trial_balance WHERE account = 'USD Collateral'")
        
        echo "Treasury Shannon: $TREASURY_SHANNON"
        echo "Sold Shannon: $SOLD_SHANNON"
        echo "Reserve Shannon: $RESERVE_SHANNON"
        echo "USD Collateral: \$${USD_COLLATERAL:-0.00}"
        
        # Available for sale
        AVAILABLE=$((TREASURY_SHANNON - SOLD_SHANNON))
        if [ "$AVAILABLE" -lt 0 ]; then
            AVAILABLE=0
        fi
        
        echo ""
        echo -e "${GREEN}📊 Market Liquidity${NC}"
        echo "Available Shannon: $AVAILABLE"
        echo "Backing per Shannon: \$$(sqlite3 "$DB_PATH" "SELECT usd_per_shannon FROM exchange_rates ORDER BY date DESC LIMIT 1")"
        
        if [ "$AVAILABLE" -eq 0 ]; then
            echo -e "${YELLOW}⚠️  Treasury empty. Run ./dollar-sweep.sh after backing increase.${NC}"
        fi
        ;;
        
    *)
        echo -e "${RED}❌ Unknown command: $COMMAND${NC}"
        usage
        ;;
esac