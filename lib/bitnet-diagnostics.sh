#!/bin/bash

################################################################################
# bitnet-diagnostics.sh
#
# Diagnostic tool to investigate BitNet failover conditions
# Run this BEFORE falling back to Haiku to understand why BitNet failed
#
# Usage:
#   bash bitnet-diagnostics.sh [task-description]
#
# Output:
#   - BitNet health status
#   - Network connectivity
#   - Process status
#   - Recent error logs
#   - Recommended action (retry, fix, or fallback)
#
################################################################################

set -euo pipefail

BITNET_HOST="${BITNET_HOST:-127.0.0.1}"
BITNET_PORT="${BITNET_PORT:-8080}"
BITNET_URL="http://${BITNET_HOST}:${BITNET_PORT}"
WORKSPACE_DIR="${WORKSPACE_DIR:-/root/.openclaw/workspace}"
DIAGNOSTICS_LOG="${WORKSPACE_DIR}/bitnet-diagnostics-$(date +%Y%m%d).jsonl"
TIMESTAMP=$(date -u +%Y-%m-%dT%H:%M:%SZ)

# Utility
log_diagnostic() {
    local event="$1"
    local status="$2"
    local detail="${3:-}"
    
    cat >> "$DIAGNOSTICS_LOG" << EOF
{"timestamp":"$TIMESTAMP","event":"$event","status":"$status","detail":"$detail"}
EOF
    
    echo "[DIAG] $event: $status${detail:+ ($detail)}"
}

################################################################################
# PHASE 1: Health Checks
################################################################################

check_bitnet_process() {
    echo ""
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo "🔍 PHASE 1: BitNet/Grok Process Status"
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    
    # Check for inference processes (may be named: bitnet-agent, llama-server, grok, etc.)
    local inference_pids=$(ps aux | grep -E "(bitnet|llama-server|grok|inference)" | grep -v grep | awk '{print $2}' | tr '\n' ' ')
    
    if [[ -n "$inference_pids" ]]; then
        echo "✅ Inference processes found (PIDs: $inference_pids):"
        ps aux | grep -E "(bitnet|llama-server|grok|inference)" | grep -v grep | sed 's/^/   /'
        log_diagnostic "inference_process" "running" "PIDs: $inference_pids"
        return 0
    else
        echo "❌ No inference processes found (bitnet, llama-server, grok, etc.)"
        log_diagnostic "inference_process" "missing" "No inference processes found"
        return 1
    fi
}

check_port_listening() {
    echo ""
    echo "🔍 PHASE 2: Port Availability"
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    
    # Check if port 8080 is listening
    if netstat -tuln 2>/dev/null | grep -q ":8080 "; then
        echo "✅ Port 8080 is listening"
        netstat -tuln | grep 8080 | sed 's/^/   /'
        log_diagnostic "port_listening" "success" "8080 open"
        return 0
    elif ss -tuln 2>/dev/null | grep -q ":8080 "; then
        echo "✅ Port 8080 is listening (via ss)"
        ss -tuln | grep 8080 | sed 's/^/   /'
        log_diagnostic "port_listening" "success" "8080 open"
        return 0
    else
        echo "❌ Port 8080 is NOT listening"
        log_diagnostic "port_listening" "failure" "Port 8080 not open"
        return 1
    fi
}

check_http_connectivity() {
    echo ""
    echo "🔍 PHASE 3: HTTP Connectivity"
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    
    # Try /health endpoint
    local response=$(curl -s -m 2 "${BITNET_URL}/health" 2>/dev/null || echo "TIMEOUT")
    
    if [[ "$response" == "TIMEOUT" ]]; then
        echo "❌ HTTP timeout (2s) on $BITNET_URL/health"
        log_diagnostic "http_connectivity" "timeout" "No response in 2s"
        return 1
    elif [[ -z "$response" ]]; then
        echo "❌ HTTP connection refused on $BITNET_URL/health"
        log_diagnostic "http_connectivity" "refused" "Connection refused"
        return 1
    else
        echo "✅ HTTP /health endpoint responds:"
        echo "$response" | jq '.' 2>/dev/null || echo "$response" | sed 's/^/   /'
        log_diagnostic "http_connectivity" "success" "Health endpoint OK"
        return 0
    fi
}

check_inference_latency() {
    echo ""
    echo "🔍 PHASE 4: Inference Latency (Simple Test)"
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    
    local start=$(date +%s%N)
    
    # Simple inference: "What is 1+1?"
    local response=$(curl -s -m 5 -X POST "${BITNET_URL}/v1/completions" \
        -H "Content-Type: application/json" \
        -d '{"prompt": "1+1=", "max_tokens": 10}' 2>/dev/null || echo "")
    
    local end=$(date +%s%N)
    local latency_ms=$(( (end - start) / 1000000 ))
    
    if [[ -z "$response" ]]; then
        echo "❌ Inference timed out"
        log_diagnostic "inference_latency" "timeout" "No response in 5s"
        return 1
    else
        echo "✅ Inference response in ${latency_ms}ms:"
        echo "$response" | jq '.' 2>/dev/null || echo "$response" | sed 's/^/   /'
        log_diagnostic "inference_latency" "success" "${latency_ms}ms"
        return 0
    fi
}

################################################################################
# PHASE 2: Log Analysis
################################################################################

check_recent_errors() {
    echo ""
    echo "🔍 PHASE 5: Recent Error Logs"
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    
    local bitnet_log="${WORKSPACE_DIR}/bitnet-agent/logs/$(date +%Y-%m-%d).jsonl"
    
    if [[ ! -f "$bitnet_log" ]]; then
        echo "⚠️  BitNet log not found: $bitnet_log"
        log_diagnostic "error_logs" "not_found" "No log file"
        return 1
    fi
    
    # Look for errors in last 20 lines
    local errors=$(tail -20 "$bitnet_log" | grep -i "error\|exception\|failed" || echo "")
    
    if [[ -z "$errors" ]]; then
        echo "✅ No recent errors in BitNet logs"
        log_diagnostic "error_logs" "clean" "Last 20 entries OK"
        tail -5 "$bitnet_log" | sed 's/^/   /'
        return 0
    else
        echo "❌ Errors found in recent logs:"
        echo "$errors" | sed 's/^/   /'
        log_diagnostic "error_logs" "errors_found" "$errors"
        return 1
    fi
}

################################################################################
# PHASE 3: System Resources
################################################################################

check_system_resources() {
    echo ""
    echo "🔍 PHASE 6: System Resources"
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    
    # Memory
    local mem_free=$(free -m | awk '/^Mem:/ {print $7}')
    echo "Memory available: ${mem_free}MB"
    if [[ $mem_free -lt 100 ]]; then
        echo "⚠️  Low memory (< 100MB free)"
        log_diagnostic "memory" "low" "${mem_free}MB free"
    else
        echo "✅ Memory OK"
        log_diagnostic "memory" "ok" "${mem_free}MB free"
    fi
    
    # CPU
    local cpu_load=$(uptime | awk -F'load average: ' '{print $2}' | cut -d, -f1)
    echo "CPU load average: $cpu_load"
    log_diagnostic "cpu_load" "measured" "$cpu_load"
    
    # Disk
    local disk_avail=$(df /root/.openclaw/workspace | awk 'NR==2 {print $4}')
    echo "Disk available: ${disk_avail}KB"
    if [[ $disk_avail -lt 100000 ]]; then
        echo "⚠️  Low disk (< 100MB free)"
        log_diagnostic "disk" "low" "${disk_avail}KB"
    else
        echo "✅ Disk OK"
        log_diagnostic "disk" "ok" "${disk_avail}KB"
    fi
}

################################################################################
# PHASE 4: Recommendation Engine
################################################################################

recommend_action() {
    echo ""
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo "🎯 RECOMMENDATION"
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    
    local all_ok=true
    
    # Summarize findings
    if ! check_bitnet_process &>/dev/null; then
        echo "❌ ACTION: BitNet agent not running. Restart:"
        echo "   systemctl restart bitnet-agent"
        echo "   OR: python3 /root/.openclaw/workspace/bitnet-agent/agent.py --server"
        all_ok=false
    fi
    
    if ! check_port_listening &>/dev/null; then
        echo "❌ ACTION: Port 8080 not listening. Check process and restart."
        all_ok=false
    fi
    
    if ! check_http_connectivity &>/dev/null; then
        echo "❌ ACTION: HTTP endpoint unreachable. Check logs and restart."
        all_ok=false
    fi
    
    if [[ "$all_ok" == "true" ]]; then
        echo "✅ BitNet is HEALTHY. Failover to Haiku is optional (not required)."
        echo "   Recommendation: RETRY with BitNet"
        log_diagnostic "recommendation" "retry_bitnet" "All checks passed"
    else
        echo "⚠️  BitNet has issues. Fallback to Haiku PERMITTED."
        echo "   Recommendation: FAILOVER to Haiku (cost: token spend)"
        log_diagnostic "recommendation" "fallback_to_haiku" "Issues detected"
    fi
}

################################################################################
# Main
################################################################################

main() {
    echo ""
    echo "╔════════════════════════════════════════════════════════════════╗"
    echo "║         BitNet Failover Diagnostic Suite                       ║"
    echo "║         $(date -u +%Y-%m-%d\ %H:%M:%S\ UTC)                                    ║"
    echo "╚════════════════════════════════════════════════════════════════╝"
    
    # Run all diagnostics (continue even on failure)
    check_bitnet_process || true
    check_port_listening || true
    check_http_connectivity || true
    check_inference_latency || true
    check_recent_errors || true
    check_system_resources
    recommend_action
    
    echo ""
    echo "📊 Diagnostic log: $DIAGNOSTICS_LOG"
    echo "   Query: grep 'timestamp' $DIAGNOSTICS_LOG | jq '."
    echo ""
}

main "$@"
