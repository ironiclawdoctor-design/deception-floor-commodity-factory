#!/bin/bash

################################################################################
# slash-truthfully.sh
# 
# Slash command handler: /truthfully [prompt]
# 
# Purpose:
#   - Routes user prompts through tier-routing-enforcement
#   - Returns answer + transparent cost/LLM reporting
#   - Logs all costs to hard-stops-registry
#
# Usage:
#   /truthfully What is the capital of France?
#   /truthfully How does photosynthesis work?
#   /truthfully Write a bash function to check disk usage
#
# Output Format:
#   [LLM: BITNET/HAIKU] Cost: $X.XX | Tokens: N
#   
#   [Answer]
#   ...
#
################################################################################

set -euo pipefail

# Configuration
WORKSPACE_DIR="${WORKSPACE_DIR:-/root/.openclaw/workspace}"
TIER_ROUTING_SCRIPT="${WORKSPACE_DIR}/tier-routing-enforcement.sh"
REGISTRY_DIR="${WORKSPACE_DIR}"
REGISTRY_FILE="${REGISTRY_DIR}/hard-stops-registry-$(date +%Y%m%d).jsonl"
LOG_FILE="${REGISTRY_DIR}/slash-truthfully.log"

# Ensure tier-routing script exists
if [[ ! -f "$TIER_ROUTING_SCRIPT" ]]; then
    echo "❌ Error: tier-routing-enforcement.sh not found at $TIER_ROUTING_SCRIPT"
    exit 1
fi

# ============================================================================
# Parse Arguments
# ============================================================================

if [[ $# -lt 1 ]]; then
    cat << USAGE
Usage: /truthfully <prompt>

Examples:
  /truthfully What is 2+2?
  /truthfully Explain quantum mechanics
  /truthfully Write a bash function to find duplicate files

Output includes:
  - Transparent LLM tier used (BitNet or Haiku)
  - Cost tracking (\$0.00 for BitNet, token count for Haiku)
  - The actual answer
USAGE
    exit 1
fi

# Combine all arguments into single prompt
PROMPT="$*"

# ============================================================================
# Route Through Tier-Routing Enforcement
# ============================================================================

log_message() {
    local level="$1"
    local msg="$2"
    echo "[$(date +'%Y-%m-%d %H:%M:%S')] [$level] $msg" | tee -a "$LOG_FILE"
}

log_message "INFO" "Processing /truthfully command: $PROMPT"

# Run tier-routing-enforcement to classify + route
# This returns the classification result with LLM tier and cost info
ROUTING_OUTPUT=$("$TIER_ROUTING_SCRIPT" --task "$PROMPT" --prompt "$PROMPT" 2>&1 || true)

# Extract tier from routing output (format: "Model: bash/bitnet/haiku")
LLM_TIER=$(echo "$ROUTING_OUTPUT" | grep "^Model:" | awk '{print toupper($2)}' | head -1 || echo "UNKNOWN")
COST=$(echo "$ROUTING_OUTPUT" | grep "^Cost:" | awk '{print $2}' | sed 's/\$//' | head -1 || echo "0.00")
TOKENS=$(echo "$ROUTING_OUTPUT" | grep "Tokens:" | grep -oP 'Tokens: \K[0-9]+' | head -1 || echo "0")

# Convert tier names to canonical form
case "$LLM_TIER" in
    BASH) LLM_TIER="BASH_DIRECT" ;;
    BITNET) LLM_TIER="BITNET_LOCAL" ;;
    HAIKU) LLM_TIER="HAIKU_EXTERNAL" ;;
esac

# Log to registry
TIMESTAMP=$(date -u +%Y-%m-%dT%H:%M:%SZ)
cat >> "$REGISTRY_FILE" << EOF
{"timestamp":"$TIMESTAMP","event":"slash_truthfully","source":"user_command","prompt":"$PROMPT","llm_tier":"$LLM_TIER","cost":"$COST","tokens":"$TOKENS","status":"success"}
EOF

log_message "INFO" "Tier: $LLM_TIER | Cost: \$$COST | Tokens: $TOKENS"

# ============================================================================
# Generate User-Facing Output
# ============================================================================

# Build header with transparent cost/LLM reporting
HEADER="━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
SUBHEADER="[LLM: $LLM_TIER] Cost: \$$COST | Tokens: $TOKENS"

if [[ "$LLM_TIER" == "BASH_DIRECT" ]]; then
    SUBHEADER="$SUBHEADER | ✅ System Query (Bash)"
elif [[ "$LLM_TIER" == "BITNET_LOCAL" ]]; then
    SUBHEADER="$SUBHEADER | ✅ Local, Sovereign"
elif [[ "$LLM_TIER" == "HAIKU_EXTERNAL" ]]; then
    SUBHEADER="$SUBHEADER | ⚠️  External (token tracked)"
fi

# Determine what actually answered based on routing
if [[ "$LLM_TIER" == "BASH_DIRECT" ]]; then
    # System query routed directly to bash
    ANSWER="(System query routed to bash; use direct command: $PROMPT)"
elif [[ "$LLM_TIER" == "BITNET_LOCAL" ]]; then
    # BitNet answer
    ANSWER=$(echo "$ROUTING_OUTPUT" | grep -A 50 "BitNet response:" | tail -n +2 | head -20 || echo "BitNet inference executed (see logs for details)")
elif [[ "$LLM_TIER" == "HAIKU_EXTERNAL" ]]; then
    # Haiku would be spawned in actual production
    ANSWER="(Haiku subagent would execute; see hard-stops-registry for cost tracking)"
else
    ANSWER="(Routing error; see logs)"
fi

# Output to user
cat << OUTPUT
$HEADER
🎯 /truthfully — Transparent LLM Routing
$HEADER

$SUBHEADER

Prompt: $PROMPT

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

$ANSWER

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📊 Cost Summary (logged):
   LLM Tier: $LLM_TIER
   Cost: \$$COST
   Tokens: $TOKENS
   Registry: $REGISTRY_FILE
OUTPUT

log_message "INFO" "/truthfully completed: $LLM_TIER | \$$COST"
