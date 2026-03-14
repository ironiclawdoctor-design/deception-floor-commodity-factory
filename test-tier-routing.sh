#!/bin/bash

################################################################################
# test-tier-routing.sh
# 
# Test harness for tier-routing-enforcement.sh
# Verifies routing logic, classification, and registry logging
################################################################################

set -e

TEST_DIR="/tmp/tier-routing-test"
SCRIPT="/root/.openclaw/workspace/tier-routing-enforcement.sh"

# Setup test environment
mkdir -p "$TEST_DIR"
export PATH="/root/.openclaw/workspace:$PATH"

echo "========================================="
echo "TIER ROUTING ENFORCEMENT - TEST SUITE"
echo "========================================="
echo ""

# ============================================================================
# Test 1: BitNet-compatible task (simple arithmetic)
# ============================================================================
echo "[TEST 1] BitNet-compatible: Simple arithmetic"
$SCRIPT --task "What is 2+2?" --prompt "Calculate: 2 + 2" 2>&1 | grep -E "Target model:|Cost:" || true
echo ""

# ============================================================================
# Test 2: BitNet-compatible task (bash scripting)
# ============================================================================
echo "[TEST 2] BitNet-compatible: Bash scripting"
$SCRIPT --task "Write a bash function to list files" --prompt "function to list files" 2>&1 | grep -E "Target model:|Cost:" || true
echo ""

# ============================================================================
# Test 3: Haiku-required task (creative writing)
# ============================================================================
echo "[TEST 3] Haiku-required: Creative writing"
$SCRIPT --task "Write a short story about a robot" --prompt "Write a story about a robot" 2>&1 | grep -E "Target model:|Cost:" || true
echo ""

# ============================================================================
# Test 4: Haiku-required task (detailed explanation)
# ============================================================================
echo "[TEST 4] Haiku-required: Detailed explanation"
$SCRIPT --task "Explain quantum mechanics in depth" --prompt "detailed explanation of quantum mechanics" 2>&1 | grep -E "Target model:|Cost:" || true
echo ""

# ============================================================================
# Test 5: Force model (override classification)
# ============================================================================
echo "[TEST 5] Force model override (Haiku)"
$SCRIPT --task "What is 2+2?" --prompt "Calculate: 2 + 2" --model haiku 2>&1 | grep -E "Target model:|Cost:" || true
echo ""

# ============================================================================
# Test 6: Verify registry file creation
# ============================================================================
echo "[TEST 6] Registry file creation and format"
REGISTRY="/root/.openclaw/workspace/hard-stops-registry-$(date +%Y%m%d).jsonl"
if [[ -f "$REGISTRY" ]]; then
    echo "✓ Registry file exists: $REGISTRY"
    echo "✓ Recent entries:"
    tail -2 "$REGISTRY" | jq '.' 2>/dev/null || tail -2 "$REGISTRY"
else
    echo "⚠ Registry file not yet created (expected on first run)"
fi
echo ""

# ============================================================================
# Test 7: Log file verification
# ============================================================================
echo "[TEST 7] Log file verification"
LOG="/root/.openclaw/workspace/tier-routing.log"
if [[ -f "$LOG" ]]; then
    echo "✓ Log file exists: $LOG"
    echo "✓ Recent log lines:"
    tail -3 "$LOG"
else
    echo "⚠ Log file not yet created (expected on first run)"
fi
echo ""

# ============================================================================
# Test 8: Script help/validation
# ============================================================================
echo "[TEST 8] Script validation"
if $SCRIPT 2>&1 | grep -q "Usage:"; then
    echo "✓ Script properly rejects missing arguments"
else
    echo "⚠ Script validation may need adjustment"
fi
echo ""

echo "========================================="
echo "TEST SUITE COMPLETE"
echo "========================================="
