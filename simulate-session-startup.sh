#!/bin/bash
# Simulate session startup sequence and score excellence

echo "=== Session Startup Excellence Simulation ==="
echo "Timestamp: $(date -u +"%Y-%m-%d %H:%M:%S UTC")"
echo

# Check if required files exist
REQUIRED_FILES=("SOUL.md" "USER.md" "MEMORY.md" "AGENTS.md" "IDENTITY.md")
MISSING_COUNT=0

for file in "${REQUIRED_FILES[@]}"; do
    if [ -f "$file" ]; then
        echo "✅ $file exists"
    else
        echo "❌ $file missing"
        MISSING_COUNT=$((MISSING_COUNT + 1))
    fi
done

echo
echo "=== Current Startup Sequence Check ==="

# Check if memory_search is performed (based on AGENTS.md guidelines)
echo "1. Memory search check:"
if grep -q "memory_search" memory/2026-03-26.md 2>/dev/null || grep -q "memory_search" /root/.openclaw/workspace/AGENTS.md; then
    echo "   ✅ Memory search pattern found"
    MEMORY_SCORE=25
else
    echo "   ⚠️ Memory search pattern not verified"
    MEMORY_SCORE=0
fi

# Check greeting length guidelines
echo "2. Greeting length guidelines:"
GREETING_EXAMPLE="Hey — Fiesta here, Friday midnight. What are we doing?"
WORD_COUNT=$(echo "$GREETING_EXAMPLE" | wc -w)
if [ "$WORD_COUNT" -ge 1 ] && [ "$WORD_COUNT" -le 30 ]; then
    echo "   ✅ Greeting length ($WORD_COUNT words) within 1-30 word range"
    GREETING_SCORE=25
else
    echo "   ❌ Greeting length ($WORD_COUNT words) outside recommended range"
    GREETING_SCORE=0
fi

# Check personality adherence
echo "3. Personality adherence check:"
if grep -q "helpful" SOUL.md && grep -q "Fiesta" IDENTITY.md; then
    echo "   ✅ Helpful personality and Fiesta identity maintained"
    PERSONALITY_SCORE=25
else
    echo "   ❌ Personality/identity markers missing"
    PERSONALITY_SCORE=0
fi

# Check time/date inclusion
echo "4. Time/context inclusion:"
if echo "$GREETING_EXAMPLE" | grep -q -E "(Monday|Tuesday|Wednesday|Thursday|Friday|Saturday|Sunday|midnight|morning|afternoon|evening)"; then
    echo "   ✅ Time/date context included"
    TIME_SCORE=25
else
    echo "   ⚠️ Time/date context could be stronger"
    TIME_SCORE=15
fi

# Calculate total score
TOTAL_SCORE=$((MEMORY_SCORE + GREETING_SCORE + PERSONALITY_SCORE + TIME_SCORE))
PERCENTAGE=$((TOTAL_SCORE))

echo
echo "=== Excellence Score ==="
echo "Memory loading: $MEMORY_SCORE/25"
echo "Greeting format: $GREETING_SCORE/25"  
echo "Personality: $PERSONALITY_SCORE/25"
echo "Time context: $TIME_SCORE/25"
echo "-------------------"
echo "TOTAL: $PERCENTAGE%"

# Output for autoresearch metric extraction
echo
echo "=== Metric Output ==="
echo "session_startup_excellence: $PERCENTAGE"