#!/bin/bash
# Dollar Persona - Confessional Logging
# Record failures as sacraments, extract doctrine, mint Shannon

set -e

DB_PATH="${1:-/root/.openclaw/workspace/dollar/dollar.db}"
shift || true

# Colors
BLUE='\033[0;34m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

usage() {
    cat << EOF
Usage: $0 [database] <command> [args]

Commands:
  log <failure> <platform> <code> <desc> [doctrine]  Log a failure
  list [agent] [days]                               List confessions
  extract <id> <doctrine>                           Add doctrine to confession
  rulebook                                          Show BOOTSTRAP_RULES.md

Examples:
  $0 log token_famine Ampere.sh 402 "Credits exhausted"
  $0 log platform_block Reddit 403 "IP blocked"
  $0 list dollar 7
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

COMMAND="${1:-list}"
shift || true

case "$COMMAND" in
    log)
        FAILURE_TYPE="$1"
        PLATFORM="$2"
        ERROR_CODE="$3"
        DESCRIPTION="$4"
        DOCTRINE="$5"
        
        if [ -z "$FAILURE_TYPE" ] || [ -z "$DESCRIPTION" ]; then
            echo -e "${RED}❌ Missing arguments. Usage: log <failure> <platform> <code> <desc> [doctrine]${NC}"
            usage
        fi
        
        AGENT="${AGENT:-dollar}"
        
        echo -e "${BLUE}✝️  Confessing failure...${NC}"
        echo "Failure: $FAILURE_TYPE"
        echo "Platform: $PLATFORM"
        echo "Error: $ERROR_CODE"
        echo "Description: $DESCRIPTION"
        
        # Mint Shannon for failure (5 per confession)
        SHANNON_MINTED=5
        
        sqlite3 "$DB_PATH" <<EOF
INSERT INTO confessions 
    (date, agent, failure_type, platform, error_code, description, doctrine_extracted, shannon_minted)
VALUES (
    date('now'),
    '$AGENT',
    '$FAILURE_TYPE',
    '$PLATFORM',
    '$ERROR_CODE',
    '$DESCRIPTION',
    '$DOCTRINE',
    $SHANNON_MINTED
);
EOF
        
        CONFESSION_ID=$(sqlite3 "$DB_PATH" "SELECT last_insert_rowid()")
        
        # Also mint Shannon in shannon_events
        sqlite3 "$DB_PATH" <<EOF
INSERT INTO shannon_events 
    (date, agent, event_type, amount_usd, shannon_minted, description)
VALUES (
    date('now'),
    '$AGENT',
    'certification',
    0.00,
    $SHANNON_MINTED,
    'Confession #$CONFESSION_ID: $FAILURE_TYPE'
);
EOF
        
        echo -e "${GREEN}✅ Confession recorded (ID: $CONFESSION_ID)${NC}"
        echo "Shannon minted: $SHANNON_MINTED"
        
        # If doctrine provided, update BOOTSTRAP_RULES.md
        if [ -n "$DOCTRINE" ]; then
            RULES_FILE="/root/.openclaw/workspace/BOOTSTRAP_RULES.md"
            if [ -f "$RULES_FILE" ]; then
                echo -e "${YELLOW}📝 Adding doctrine to BOOTSTRAP_RULES.md...${NC}"
                # Extract next rule number
                LAST_RULE=$(grep -o '^**Rule [0-9]*' "$RULES_FILE" | tail -1 | grep -o '[0-9]*')
                if [ -z "$LAST_RULE" ]; then
                    NEXT_RULE=1
                else
                    NEXT_RULE=$((LAST_RULE + 1))
                fi
                
                # Append rule
                echo "" >> "$RULES_FILE"
                echo "**Rule $NEXT_RULE** — $DOCTRINE" >> "$RULES_FILE"
                echo -e "${GREEN}✅ Rule $NEXT_RULE added${NC}"
            fi
        fi
        ;;
        
    list)
        AGENT="$1"
        DAYS="${2:-7}"
        
        WHERE=""
        if [ -n "$AGENT" ]; then
            WHERE="WHERE agent = '$AGENT'"
        fi
        
        echo -e "${BLUE}📖 Confessions (last $DAYS days)${NC}"
        echo "--------------------------------"
        sqlite3 -header -column "$DB_PATH" <<EOF
SELECT 
    id as ID,
    date as Date,
    agent as Agent,
    failure_type as Failure,
    platform as Platform,
    error_code as Code,
    shannon_minted as Shannon
FROM confessions
$WHERE
AND date >= date('now', '-$DAYS days')
ORDER BY date DESC, id DESC
LIMIT 20;
EOF
        
        # Summary
        echo ""
        echo -e "${GREEN}📊 Confession Summary${NC}"
        sqlite3 -column "$DB_PATH" <<EOF
SELECT 
    failure_type,
    COUNT(*) as Count,
    SUM(shannon_minted) as "Total Shannon"
FROM confessions
$WHERE
AND date >= date('now', '-$DAYS days')
GROUP BY failure_type
ORDER BY Count DESC;
EOF
        ;;
        
    extract)
        CONFESSION_ID="$1"
        DOCTRINE="$2"
        
        if [ -z "$CONFESSION_ID" ] || [ -z "$DOCTRINE" ]; then
            echo -e "${RED}❌ Missing arguments. Usage: extract <id> <doctrine>${NC}"
            usage
        fi
        
        # Update confession with doctrine
        sqlite3 "$DB_PATH" <<EOF
UPDATE confessions 
SET doctrine_extracted = '$DOCTRINE',
    shannon_minted = shannon_minted + 5
WHERE id = $CONFESSION_ID;
EOF
        
        # Mint extra Shannon for doctrine extraction
        sqlite3 "$DB_PATH" <<EOF
INSERT INTO shannon_events 
    (date, agent, event_type, amount_usd, shannon_minted, description)
VALUES (
    date('now'),
    'dollar',
    'certification',
    0.00,
    5,
    'Doctrine extracted from confession #$CONFESSION_ID'
);
EOF
        
        echo -e "${GREEN}✅ Doctrine extracted${NC}"
        echo "Confession ID: $CONFESSION_ID"
        echo "Doctrine: $DOCTRINE"
        echo "Extra Shannon minted: 5"
        
        # Add to BOOTSTRAP_RULES.md
        RULES_FILE="/root/.openclaw/workspace/BOOTSTRAP_RULES.md"
        if [ -f "$RULES_FILE" ]; then
            LAST_RULE=$(grep -o '^**Rule [0-9]*' "$RULES_FILE" | tail -1 | grep -o '[0-9]*')
            if [ -z "$LAST_RULE" ]; then
                NEXT_RULE=1
            else
                NEXT_RULE=$((LAST_RULE + 1))
            fi
            
            echo "" >> "$RULES_FILE"
            echo "**Rule $NEXT_RULE** — $DOCTRINE" >> "$RULES_FILE"
            echo -e "${YELLOW}📝 Added as Rule $NEXT_RULE in BOOTSTRAP_RULES.md${NC}"
        fi
        ;;
        
    rulebook)
        echo -e "${BLUE}📚 BOOTSTRAP_RULES.md${NC}"
        echo "----------------------"
        RULES_FILE="/root/.openclaw/workspace/BOOTSTRAP_RULES.md"
        if [ -f "$RULES_FILE" ]; then
            cat "$RULES_FILE"
        else
            echo -e "${YELLOW}⚠️  BOOTSTRAP_RULES.md not found${NC}"
        fi
        
        # Show recent confessions that lack doctrine
        echo ""
        echo -e "${YELLOW}🔍 Confessions needing doctrine extraction:${NC}"
        sqlite3 -header -column "$DB_PATH" <<EOF
SELECT 
    id,
    date,
    failure_type,
    description
FROM confessions
WHERE doctrine_extracted IS NULL OR doctrine_extracted = ''
ORDER BY date DESC
LIMIT 5;
EOF
        ;;
        
    *)
        echo -e "${RED}❌ Unknown command: $COMMAND${NC}"
        usage
        ;;
esac