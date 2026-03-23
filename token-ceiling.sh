#!/bin/bash
# token-ceiling: $5/day hard limit (25k tokens). Hard stop at 100%.

LEDGER="/root/.openclaw/workspace/.token-ledger.json"
LIMIT_DOLLARS=5
TODAY=$(date +%Y-%m-%d)

init_ledger() {
    [[ -f "$LEDGER" ]] && return
    cat > "$LEDGER" << EOF
{"date":"$TODAY","spent_dollars":0,"limit_dollars":$LIMIT_DOLLARS}
EOF
}

check_ceiling() {
    init_ledger
    CURRENT_DATE=$(jq -r '.date' "$LEDGER")
    SPENT=$(jq '.spent_dollars' "$LEDGER")
    
    if [[ "$CURRENT_DATE" != "$TODAY" ]]; then
        jq ".date=\"$TODAY\" | .spent_dollars=0" "$LEDGER" > "${LEDGER}.tmp"
        mv "${LEDGER}.tmp" "$LEDGER"
        SPENT=0
    fi
    
    if (( $(echo "$SPENT >= $LIMIT_DOLLARS" | bc -l) )); then
        echo "❌ HARD STOP: \$$SPENT/$LIMIT_DOLLARS" && exit 1
    else
        REMAINING=$(echo "$LIMIT_DOLLARS - $SPENT" | bc -l)
        echo "✅ \$$REMAINING remaining" && exit 0
    fi
}

check_ceiling
