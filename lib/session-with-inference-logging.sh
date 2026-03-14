#!/bin/bash

################################################################################
# session-with-inference-logging.sh
#
# Handler for /new sessions with complete inference logging
# Logs ALL internal inference (Bash, BitNet, Haiku) and diagnoses failover
#
# Usage:
#   /new [task-description]
#
# Behavior:
#   1. Log all internal inference (Bash, BitNet, Haiku)
#   2. On BitNet failure: Run diagnostics BEFORE fallback
#   3. Collect all available agency agents
#   4. Decide: Retry BitNet, use agents, or fallback to Haiku
#
################################################################################

set -euo pipefail

WORKSPACE_DIR="${WORKSPACE_DIR:-/root/.openclaw/workspace}"
INFERENCE_LOG="${WORKSPACE_DIR}/inference-log-$(date +%Y%m%d).jsonl"
DIAGNOSTICS_SCRIPT="${WORKSPACE_DIR}/lib/bitnet-diagnostics.sh"
TIMESTAMP=$(date -u +%Y-%m-%dT%H:%M:%SZ)

# Utility functions
log_inference() {
    local tier="$1"
    local task="$2"
    local status="$3"
    local detail="${4:-}"
    
    cat >> "$INFERENCE_LOG" << EOF
{"timestamp":"$TIMESTAMP","tier":"$tier","task":"$task","status":"$status","detail":"$detail"}
EOF
    
    echo "[INFERENCE] Tier: $tier | Task: $task | Status: $status${detail:+ ($detail)}"
}

################################################################################
# INTERNAL INFERENCE LOGGING
################################################################################

attempt_bash_inference() {
    local task="$1"
    
    echo ""
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo "🔧 Tier 0: BASH Inference Attempt"
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    
    # Try to execute task as bash command directly
    if [[ "$task" =~ ^(ls|find|grep|cat|ps|top|git|docker)\ .*$ ]]; then
        echo "✅ Task looks like a bash command: $task"
        log_inference "bash" "$task" "attempt" "direct_execution"
        
        # Don't actually execute untrusted task; just log
        echo "[Would execute]: $task"
        return 0
    else
        echo "⏭️  Task is not a bash command"
        log_inference "bash" "$task" "skip" "not_applicable"
        return 1
    fi
}

attempt_bitnet_inference() {
    local task="$1"
    
    echo ""
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo "⚡ Tier 1: BitNet Inference Attempt"
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    
    local bitnet_url="http://127.0.0.1:8080/v1/completions"
    
    # Check if BitNet is available
    local health=$(curl -s -m 2 "http://127.0.0.1:8080/health" 2>/dev/null || echo "")
    
    if [[ -z "$health" ]]; then
        echo "❌ BitNet health check failed (timeout or connection refused)"
        log_inference "bitnet" "$task" "failed" "health_check_timeout"
        return 1
    fi
    
    echo "✅ BitNet health check passed"
    echo "   Response: $health"
    
    # Attempt inference
    local start=$(date +%s%N)
    local response=$(curl -s -m 5 -X POST "$bitnet_url" \
        -H "Content-Type: application/json" \
        -d "{\"prompt\": \"$task\", \"max_tokens\": 500}" 2>/dev/null || echo "")
    local end=$(date +%s%N)
    local latency_ms=$(( (end - start) / 1000000 ))
    
    if [[ -z "$response" ]]; then
        echo "❌ BitNet inference timed out or failed"
        log_inference "bitnet" "$task" "failed" "inference_timeout_${latency_ms}ms"
        return 1
    fi
    
    # Check if response is valid
    if echo "$response" | jq '.' &>/dev/null; then
        echo "✅ BitNet inference succeeded (${latency_ms}ms)"
        echo "   Response length: $(echo "$response" | jq '. | length') chars"
        log_inference "bitnet" "$task" "success" "${latency_ms}ms"
        echo "$response" | jq '.' | head -10 | sed 's/^/   /'
        return 0
    else
        echo "❌ BitNet response invalid (not JSON)"
        log_inference "bitnet" "$task" "failed" "invalid_json_response"
        return 1
    fi
}

################################################################################
# FAILOVER DIAGNOSIS & AGENCY ESCALATION
################################################################################

diagnose_bitnet_failure() {
    local task="$1"
    
    echo ""
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo "🔍 BitNet Failure Diagnosis"
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    
    # Run diagnostic suite
    if [[ -f "$DIAGNOSTICS_SCRIPT" ]]; then
        bash "$DIAGNOSTICS_SCRIPT" "$task" 2>&1 | head -50
        log_inference "diagnostic" "$task" "ran" "full_suite"
    else
        echo "⚠️  Diagnostic script not found: $DIAGNOSTICS_SCRIPT"
        log_inference "diagnostic" "$task" "skipped" "script_missing"
    fi
}

collect_agency_agents() {
    echo ""
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo "🤖 Collecting Available Agency Agents"
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    
    # List available agents
    local agents=$(agents_list 2>/dev/null || echo "")
    
    if [[ -z "$agents" ]]; then
        echo "⚠️  No agents available via agents_list"
        log_inference "agency_agents" "list" "unavailable" "no_agents"
        return 1
    fi
    
    echo "✅ Available agents:"
    echo "$agents" | sed 's/^/   /'
    log_inference "agency_agents" "list" "success" "agents_collected"
    
    return 0
}

decide_fallback_path() {
    local task="$1"
    local bitnet_status="$2"  # "healthy", "unhealthy", or "unknown"
    
    echo ""
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo "🎯 Fallback Decision Path"
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    
    case "$bitnet_status" in
        healthy)
            echo "✅ BitNet is HEALTHY. Why did it fail?"
            echo "   Recommendation: RETRY BitNet (transient failure)"
            log_inference "fallback" "$task" "retry_bitnet" "health_ok"
            ;;
        unhealthy)
            echo "⚠️  BitNet has structural issues (process down, port closed, etc.)"
            echo "   Check options:"
            echo "   1. Restart BitNet: systemctl restart bitnet-agent"
            echo "   2. Use agency agents (if available)"
            echo "   3. Fallback to Haiku (last resort, costs tokens)"
            log_inference "fallback" "$task" "escalate_to_agency" "bitnet_unhealthy"
            ;;
        unknown)
            echo "❓ BitNet status unknown. Escalate to agency agents."
            echo "   Then fallback to Haiku if agents unavailable."
            log_inference "fallback" "$task" "escalate_to_agency" "status_unknown"
            ;;
    esac
}

################################################################################
# HAIKU FALLBACK (LAST RESORT)
################################################################################

fallback_to_haiku() {
    local task="$1"
    
    echo ""
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo "⚠️  Tier 2: Haiku Fallback (Last Resort)"
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    
    echo "⚠️  All internal inference methods exhausted."
    echo "   Falling back to Haiku (external, token cost)"
    echo "   Task: $task"
    
    log_inference "haiku" "$task" "fallback" "all_internal_failed"
    
    # In a real scenario, this would spawn a Haiku session
    echo ""
    echo "[Haiku would be invoked here with: $task]"
    echo ""
}

################################################################################
# Main Orchestration
################################################################################

main() {
    local task="${1:-}"
    
    if [[ -z "$task" ]]; then
        cat << USAGE
Usage: /new [task-description]

Examples:
  /new ls -la /root/.openclaw/workspace
  /new what is 2+2?
  /new explain quantum mechanics

Behavior:
  1. Attempt Bash inference (system queries)
  2. If Bash fails, attempt BitNet inference
  3. If BitNet fails, diagnose why
  4. Collect available agency agents
  5. Decide: Retry, use agents, or fallback to Haiku
USAGE
        exit 1
    fi
    
    echo ""
    echo "╔════════════════════════════════════════════════════════════════╗"
    echo "║         /new Session with Full Inference Logging              ║"
    echo "║         $(date -u +%Y-%m-%d\ %H:%M:%S\ UTC)                                    ║"
    echo "╚════════════════════════════════════════════════════════════════╝"
    echo ""
    echo "Task: $task"
    echo "Log:  $INFERENCE_LOG"
    
    # === PHASE 1: Try Bash ===
    if attempt_bash_inference "$task"; then
        echo "✅ Task handled by Bash (Tier 0)"
        return 0
    fi
    
    # === PHASE 2: Try BitNet ===
    if attempt_bitnet_inference "$task"; then
        echo "✅ Task handled by BitNet (Tier 1)"
        return 0
    fi
    
    # === PHASE 3: BitNet Failed - Diagnose ===
    echo ""
    echo "❌ BitNet inference failed. Running diagnostics..."
    diagnose_bitnet_failure "$task"
    
    # === PHASE 4: Collect Agency Agents ===
    echo ""
    if collect_agency_agents; then
        echo "💡 Agents available. Use them before Haiku."
        log_inference "decision" "$task" "escalate_to_agents" "before_haiku"
    fi
    
    # === PHASE 5: Decide Fallback ===
    # Determine BitNet health from diagnostics
    local bitnet_health="unknown"
    if netstat -tuln 2>/dev/null | grep -q ":8080 "; then
        bitnet_health="healthy"
    else
        bitnet_health="unhealthy"
    fi
    
    decide_fallback_path "$task" "$bitnet_health"
    
    # === PHASE 6: Last Resort - Haiku ===
    echo ""
    echo "💡 All internal inference methods attempted."
    fallback_to_haiku "$task"
    
    # === Final Report ===
    echo ""
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo "📊 Inference Log Summary"
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo "Log file: $INFERENCE_LOG"
    echo ""
    echo "View latest entries:"
    echo "  tail -10 $INFERENCE_LOG | jq '.'"
    echo ""
    echo "Query by tier:"
    echo "  grep '\"tier\":\"bash\"' $INFERENCE_LOG | wc -l"
    echo "  grep '\"tier\":\"bitnet\"' $INFERENCE_LOG | wc -l"
    echo "  grep '\"tier\":\"haiku\"' $INFERENCE_LOG | wc -l"
    echo ""
}

main "$@"
