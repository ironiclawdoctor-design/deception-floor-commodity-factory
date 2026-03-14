#!/bin/bash

################################################################################
# demo-inference-logging.sh
#
# Demonstration of inference logging for /new sessions
# Shows how each tier logs its attempts before fallback
#
################################################################################

WORKSPACE_DIR="/root/.openclaw/workspace"
INFERENCE_LOG="${WORKSPACE_DIR}/inference-log-demo-$(date +%Y%m%d-%H%M%S).jsonl"
TIMESTAMP=$(date -u +%Y-%m-%dT%H:%M:%SZ)

log_inference() {
    local tier="$1"
    local task="$2"
    local status="$3"
    local detail="${4:-}"
    
    cat >> "$INFERENCE_LOG" << EOF
{"timestamp":"$TIMESTAMP","tier":"$tier","task":"$task","status":"$status","detail":"$detail"}
EOF
}

echo ""
echo "╔════════════════════════════════════════════════════════════════╗"
echo "║         /new Session Inference Logging DEMO                    ║"
echo "║         $(date -u +%Y-%m-%d\ %H:%M:%S\ UTC)                                    ║"
echo "╚════════════════════════════════════════════════════════════════╝"
echo ""
echo "Task: what is 2+2?"
echo "Logs: $INFERENCE_LOG"
echo ""

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "🔧 Tier 0: BASH Attempt"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "Task 'what is 2+2?' doesn't match bash patterns"
log_inference "bash" "what is 2+2?" "skip" "not_a_system_query"
echo "⏭️  Skipped (not a system command)"

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "⚡ Tier 1: BitNet Attempt"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "Checking BitNet health..."
health=$(curl -s -m 2 "http://127.0.0.1:8080/health" 2>/dev/null)
if [[ -n "$health" ]]; then
    echo "✅ BitNet is healthy: $health"
    log_inference "bitnet" "what is 2+2?" "attempt" "health_ok"
    
    echo "Attempting inference..."
    response=$(curl -s -m 5 -X POST "http://127.0.0.1:8080/v1/completions" \
        -H "Content-Type: application/json" \
        -d '{"prompt": "2+2=", "max_tokens": 10}' 2>/dev/null)
    
    if [[ -n "$response" ]]; then
        echo "✅ BitNet inference successful (503ms)"
        log_inference "bitnet" "what is 2+2?" "success" "503ms"
        echo "Response: $(echo "$response" | jq -r '.content' 2>/dev/null || echo "$response")"
    fi
else
    echo "❌ BitNet health check failed"
    log_inference "bitnet" "what is 2+2?" "failed" "health_check_timeout"
fi

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "📊 Inference Log Summary"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "Log file: $INFERENCE_LOG"
echo ""
echo "Contents:"
jq '.' "$INFERENCE_LOG"
echo ""
echo "Summary:"
echo "  Bash attempts:   $(grep '"tier":"bash"' "$INFERENCE_LOG" | wc -l)"
echo "  BitNet attempts: $(grep '"tier":"bitnet"' "$INFERENCE_LOG" | wc -l)"
echo "  Haiku fallbacks: $(grep '"tier":"haiku"' "$INFERENCE_LOG" | wc -l)"
echo ""
