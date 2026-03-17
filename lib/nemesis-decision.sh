#!/bin/bash
################################################################################
# nemesis-decision.sh
# 
# Nemesis Decision Framework — Autonomous spawn/escalate/deny logic
# 
# Purpose: Implement Nemesis's decision surface as a bash function
# Cost: $0.00 (Tier 0 — bash only)
# 
# Usage:
#   source nemesis-decision.sh
#   nemesis_decide "analyze-commodity-pricing" "0.50"
#   # Output: SPAWN | ESCALATE | DENY
#
################################################################################

set -euo pipefail

# Configuration
AUTHORIZATION_FILE="${AUTHORIZATION_FILE:-/root/.openclaw/workspace/AUTHORIZATION.md}"
CORRECTED_DOC="${CORRECTED_DOC:-/root/.openclaw/workspace/mendez-gemini-enclave-corrected.md}"
HARD_STOPS_REGISTRY="${HARD_STOPS_REGISTRY:-/root/.openclaw/workspace/hard-stops-registry-LATEST.jsonl}"
BUDGET_LIMIT="${BUDGET_LIMIT:-20.00}"  # $20.00 default from corrected doc

################################################################################
# 1. Authorization Check (Tier 0)
################################################################################

check_authorization() {
    local task_type="$1"
    
    if [[ ! -f "$AUTHORIZATION_FILE" ]]; then
        echo "DENY"  # No authorization file = deny everything
        return 0
    fi
    
    # Check if this task type is authorized
    if grep -q "authorized to" "$AUTHORIZATION_FILE"; then
        echo "ALLOW"
        return 0
    fi
    
    echo "DENY"
}

################################################################################
# 2. Cost Discipline Check (Tier 0)
################################################################################

check_cost_discipline() {
    local estimated_cost="$1"
    
    # Parse current spend from hard-stops-registry
    local current_spend=0
    if [[ -f "$HARD_STOPS_REGISTRY" ]]; then
        current_spend=$(jq -r '.data.cost // 0' "$HARD_STOPS_REGISTRY" 2>/dev/null | \
                        awk '{sum+=$1} END {print sum}' || echo "0")
    fi
    
    local projected_total=$(echo "$current_spend + $estimated_cost" | bc)
    
    if (( $(echo "$projected_total > $BUDGET_LIMIT" | bc -l) )); then
        echo "EXCEED_BUDGET"
        return 1
    fi
    
    echo "WITHIN_BUDGET"
    return 0
}

################################################################################
# 3. Scope Validation (Tier 0)
################################################################################

validate_scope() {
    local task="$1"
    
    # Check if task is mentioned in corrected document
    if [[ ! -f "$CORRECTED_DOC" ]]; then
        echo "NO_SCOPE"
        return 1
    fi
    
    # Extract department responsibilities
    local dept_pattern=$(grep -o "Department of [A-Za-z]*" "$CORRECTED_DOC" | head -1)
    
    if [[ -z "$dept_pattern" ]]; then
        echo "NO_SCOPE"
        return 1
    fi
    
    echo "SCOPED"
    return 0
}

################################################################################
# 4. Conflict Check (Tier 0)
################################################################################

check_conflicts() {
    local task="$1"
    
    # Check if similar task is already running
    if [[ -f "$HARD_STOPS_REGISTRY" ]]; then
        if grep -q "\"task\":\"$task\"" "$HARD_STOPS_REGISTRY"; then
            echo "CONFLICT"
            return 1
        fi
    fi
    
    echo "NO_CONFLICT"
    return 0
}

################################################################################
# 5. Main Decision Function
################################################################################

nemesis_decide() {
    local task="$1"
    local estimated_cost="${2:-0.01}"  # Default to ~Haiku cost
    
    # === Tier 0 Checks (All free, all bash) ===
    
    # Check 1: Authorization
    local auth=$(check_authorization "$task")
    if [[ "$auth" == "DENY" ]]; then
        echo "DENY"
        log_decision "$task" "DENY" "authorization_missing"
        return 1
    fi
    
    # Check 2: Budget
    local budget=$(check_cost_discipline "$estimated_cost")
    if [[ "$budget" == "EXCEED_BUDGET" ]]; then
        echo "ESCALATE"
        log_decision "$task" "ESCALATE" "budget_exceeded"
        return 1
    fi
    
    # Check 3: Scope
    local scope=$(validate_scope "$task")
    if [[ "$scope" == "NO_SCOPE" ]]; then
        echo "ESCALATE"
        log_decision "$task" "ESCALATE" "scope_undefined"
        return 1
    fi
    
    # Check 4: Conflicts
    local conflicts=$(check_conflicts "$task")
    if [[ "$conflicts" == "CONFLICT" ]]; then
        echo "ESCALATE"
        log_decision "$task" "ESCALATE" "task_conflict"
        return 1
    fi
    
    # === All Checks Passed ===
    echo "SPAWN"
    log_decision "$task" "SPAWN" "all_checks_passed"
    return 0
}

################################################################################
# 6. Logging (Audit Trail)
################################################################################

log_decision() {
    local task="$1"
    local decision="$2"
    local reason="$3"
    local timestamp=$(date -u +%Y-%m-%dT%H:%M:%SZ)
    
    cat >> "$HARD_STOPS_REGISTRY" << EOF
{"timestamp":"$timestamp","event":"nemesis_decision","decision":"$decision","task":"$task","reason":"$reason","llm_tier":"TIER0_BASH"}
EOF
}

################################################################################
# 7. CLI Entrypoint
################################################################################

if [[ $# -lt 1 ]]; then
    cat << USAGE
Usage: nemesis-decision.sh <task> [estimated_cost]

Decision framework for autonomous subagent spawning.

Arguments:
  task              Task description (e.g., "analyze-commodity-pricing")
  estimated_cost    Estimated cost in dollars (default: 0.01)

Output:
  SPAWN             Conditions met, proceed with sessions_spawn
  ESCALATE          Decision needed by human (cost, scope, conflict, etc.)
  DENY              Authorization missing or invalid

Examples:
  $(basename "$0") "analyze-commodity-pricing" "0.01"
  $(basename "$0") "telemetry-snapshot" "0.02"

This function is Tier 0 (bash only). Cost: \$0.00

Environment variables:
  AUTHORIZATION_FILE    Path to AUTHORIZATION.md
  CORRECTED_DOC         Path to mendez-gemini-enclave-corrected.md
  HARD_STOPS_REGISTRY   Path to hard-stops-registry-LATEST.jsonl
  BUDGET_LIMIT          Maximum spend ($20.00 default)

USAGE
    exit 1
fi

# Main
nemesis_decide "$1" "${2:-0.01}"
