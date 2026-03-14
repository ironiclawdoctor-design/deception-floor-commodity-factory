#!/bin/bash
# tier-routing-enforcement.sh — Three-Tier Decision Tree for Query Routing
# Canonical implementation of tier routing doctrine
# Generated: 2026-03-14 16:51 UTC by Fiesta
# Cost discipline: All external costs logged and tracked

set -e

# Configuration
HARD_STOPS_REGISTRY="/root/.openclaw/workspace/hard-stops-registry-LATEST.jsonl"
BITNET_URL="http://127.0.0.1:8080"
GROK_URL="http://127.0.0.1:8889"
INFERENCE_LOG="/root/.openclaw/workspace/inference-log-$(date +%Y%m%d).jsonl"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Helper: Log decision to hard-stops registry
log_decision() {
    local task="$1"
    local tier="$2"
    local cost="$3"
    local model="${4:-unknown}"
    local timestamp=$(date -u +"%Y-%m-%dT%H:%M:%SZ")
    
    local entry=$(jq -n \
        --arg ts "$timestamp" \
        --arg t "$task" \
        --arg tier "$tier" \
        --arg cost "$cost" \
        --arg model "$model" \
        '{timestamp: $ts, task: $t, tier: $tier, cost: $cost, model: $model}')
    
    echo "$entry" >> "$HARD_STOPS_REGISTRY"
    echo "$entry" >> "$INFERENCE_LOG"
}

# Tier 0: BASH — System queries, always $0.00
tier_0_bash() {
    local query="$1"
    log_decision "$query" "BASH_DIRECT" "0.0000" "bash"
    echo -e "${GREEN}[BASH]${NC} $query"
    eval "$query" 2>&1
    echo -e "${GREEN}✓ Cost: \$0.0000${NC}"
}

# Tier 1: GROK — Free pattern matching, $0.00
tier_1_grok() {
    local prompt="$1"
    log_decision "$prompt" "GROK_LOCAL" "0.0000" "grok"
    echo -e "${YELLOW}[GROK]${NC} Inferring locally..."
    
    local response=$(curl -s -X POST "$GROK_URL/infer" \
        -H "Content-Type: application/json" \
        -d "{\"prompt\": \"$prompt\", \"max_tokens\": 100}" 2>/dev/null)
    
    echo "$response" | jq -r '.response' 2>/dev/null || echo "$response"
    echo -e "${GREEN}✓ Cost: \$0.0000${NC}"
}

# Tier 2: BITNET — Local ML inference, $0.00
tier_2_bitnet() {
    local prompt="$1"
    log_decision "$prompt" "BITNET_LOCAL" "0.0000" "bitnet"
    echo -e "${YELLOW}[BITNET]${NC} Running locally on CPU..."
    
    local response=$(curl -s -X POST "$BITNET_URL/v1/chat/completions" \
        -H "Content-Type: application/json" \
        -d "{\"model\": \"bitnet\", \"messages\": [{\"role\": \"user\", \"content\": \"$prompt\"}], \"temperature\": 0.7, \"max_tokens\": 100}" 2>/dev/null)
    
    echo "$response" | jq -r '.choices[0].message.content' 2>/dev/null || echo "$response"
    echo -e "${GREEN}✓ Cost: \$0.0000${NC}"
}

# Tier 3: HAIKU — External fallback, COSTS TOKENS
tier_3_haiku() {
    local prompt="$1"
    local cost="0.00081"  # Approximate cost per call
    log_decision "$prompt" "HAIKU_EXTERNAL" "$cost" "haiku"
    echo -e "${RED}[HAIKU]${NC} EXTERNAL CALL (only if necessary)"
    echo -e "${RED}⚠ Cost: \$$cost${NC}"
    # Don't actually call Haiku here — just log the decision
    echo "[HAIKU would be called here if approved]"
}

# Check if query is a system command
is_system_command() {
    local query="$1"
    case "$query" in
        ls*|grep*|ps*|find*|cat*|head*|tail*|wc*|du*|df*|chmod*|mkdir*|rm*|mv*|cp*|curl*|wget*|git*|systemctl*|service*|pgrep*|pkill*|top*|htop*|free*|whoami*|pwd*|date*|echo*|printf*|file*|which*|type*)
            return 0
            ;;
        *)
            return 1
            ;;
    esac
}

# Main routing decision tree
classify_and_route() {
    local query="$1"
    
    # Rule 0: Is it a system command?
    if is_system_command "$query"; then
        tier_0_bash "$query"
        return
    fi
    
    # Rule 1: Pattern matching queries
    if echo "$query" | grep -qE "(pattern|analyze|match|regex|json|count|filter)"; then
        tier_1_grok "$query"
        return
    fi
    
    # Rule 2: Does it need real reasoning?
    if echo "$query" | grep -qE "(why|explain|philosophy|creative|opinion|analysis)"; then
        tier_2_bitnet "$query"
        return
    fi
    
    # Default: Try BitNet first, fall back to Grok if it fails
    echo -e "${YELLOW}[ROUTING]${NC} Attempting BitNet..."
    if tier_2_bitnet "$query" 2>/dev/null | grep -q "error"; then
        echo -e "${YELLOW}[ROUTING]${NC} BitNet insufficient, trying Grok..."
        tier_1_grok "$query"
    fi
}

# Display decision tree
show_routing_policy() {
    cat << 'EOF'

╔════════════════════════════════════════════════════════════════╗
║          FIESTA TIER ROUTING DECISION TREE v1.0                ║
╚════════════════════════════════════════════════════════════════╝

Rule 0: TIER 0 (BASH) — System Queries
   Patterns: ls, grep, ps, find, cat, head, tail, curl, git, etc.
   Cost: $0.0000
   Rule: Direct execution via shell

Rule 1: TIER 1 (GROK) — Pattern Matching
   Patterns: analyze, regex, json, count, filter, match
   Cost: $0.0000 (local free inference)
   Rule: Run on Grok server (port 8889)

Rule 2: TIER 2 (BITNET) — Local ML Reasoning
   Patterns: why, explain, philosophy, creative, analysis
   Cost: $0.0000 (local CPU inference, ternary {-1,0,1})
   Rule: Run on BitNet server (port 8080)

Rule 3: TIER 3 (HAIKU) — External Fallback
   Patterns: Only when Tier 0-2 insufficient
   Cost: ~$0.00081 per call
   Rule: HAIKU IS FROZEN until BitNet sufficiency proven >85%
   Exception: Only if human explicitly approves

Standing Policy (Immutable as of 2026-03-14 16:51 UTC):
   "All simple system queries go to bash, not haiku.
    This level of common sense applies to all /truthfully."

Cost Discipline:
   ✅ All decisions logged to hard-stops-registry
   ✅ Every call costs documented
   ✅ External tokens forbidden for internal work
   ✅ Revenue-only access to Tier 3 (Haiku)

EOF
}

# Main entry point
main() {
    if [[ $# -eq 0 ]]; then
        show_routing_policy
        return
    fi
    
    local command="$1"
    shift
    
    case "$command" in
        classify|route)
            classify_and_route "$@"
            ;;
        policy)
            show_routing_policy
            ;;
        bash)
            tier_0_bash "$@"
            ;;
        grok)
            tier_1_grok "$@"
            ;;
        bitnet)
            tier_2_bitnet "$@"
            ;;
        *)
            classify_and_route "$command $@"
            ;;
    esac
}

main "$@"
