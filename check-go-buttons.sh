#!/bin/bash
# check-go-buttons.sh
# Daily cron verification of Go Button Protocol survival

LOG_FILE="/root/.openclaw/workspace/logs/go-button-verification-$(date +%Y-%m-%d).log"

echo "=== Go Button Protocol Verification $(date) ===" >> "$LOG_FILE"

# Check 1: Rules pairings file exists
if [ -f "/root/.openclaw/workspace/rules-pairings-go-buttons.md" ]; then
    echo "✅ PASS: rules-pairings-go-buttons.md exists" >> "$LOG_FILE"
    PAIRING_COUNT=$(grep -c "^### " /root/.openclaw/workspace/rules-pairings-go-buttons.md)
    echo "   Pairings found: $PAIRING_COUNT" >> "$LOG_FILE"
else
    echo "❌ FAIL: rules-pairings-go-buttons.md missing" >> "$LOG_FILE"
fi

# Check 2: AGENTS.md contains Go Button Protocol section
if grep -q "## Go Button Protocol" /root/.openclaw/workspace/AGENTS.md; then
    echo "✅ PASS: Go Button Protocol section in AGENTS.md" >> "$LOG_FILE"
    GB_RULES=$(grep -c "### GB-" /root/.openclaw/workspace/AGENTS.md)
    echo "   GB-series rules: $GB_RULES" >> "$LOG_FILE"
else
    echo "❌ FAIL: Go Button Protocol missing from AGENTS.md" >> "$LOG_FILE"
fi

# Check 3: Sonnet queue has Go persistence task
if grep -q "GO_BUTTON_PERSISTENCE" /root/.openclaw/workspace/sonnet-queue.md; then
    echo "✅ PASS: GO_BUTTON_PERSISTENCE in sonnet-queue.md" >> "$LOG_FILE"
else
    echo "⚠️ WARN: GO_BUTTON_PERSISTENCE not in sonnet queue" >> "$LOG_FILE"
fi

# Check 4: Button syntax compliance (sample check)
echo "Button syntax check:" >> "$LOG_FILE"
echo "  Expected patterns: [Go], [Pause], [Schedule], [Delegate]" >> "$LOG_FILE"

# Check 5: Survival mechanisms documented
SURVIVAL_METHODS=$(grep -c "Persistence:" /root/.openclaw/workspace/rules-pairings-go-buttons.md)
echo "Survival methods documented: $SURVIVAL_METHODS" >> "$LOG_FILE"

# Calculate survival score (0-100)
SCORE=0
if [ -f "/root/.openclaw/workspace/rules-pairings-go-buttons.md" ]; then
    SCORE=$((SCORE + 25))
fi
if grep -q "## Go Button Protocol" /root/.openclaw/workspace/AGENTS.md; then
    SCORE=$((SCORE + 25))
fi
if [ $SURVIVAL_METHODS -ge 5 ]; then
    SCORE=$((SCORE + 25))
fi
if grep -q "GO_BUTTON_PERSISTENCE" /root/.openclaw/workspace/sonnet-queue.md; then
    SCORE=$((SCORE + 25))
fi

echo "=== Survival Score: $SCORE/100 ===" >> "$LOG_FILE"

# Gideon Test: >93% required
if [ $SCORE -ge 93 ]; then
    echo "✅ GIDEON TEST PASS: Go Button Protocol survival >93%" >> "$LOG_FILE"
    exit 0
else
    echo "❌ GIDEON TEST FAIL: Go Button Protocol survival $SCORE% (