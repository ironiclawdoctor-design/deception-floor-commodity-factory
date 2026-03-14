#!/bin/bash

################################################################################
# bitnet-health-orchestration.sh
#
# Orchestrate BitNet health checks across all available agents
# Each agent performs the check independently and reports back
#
# Usage:
#   bash bitnet-health-orchestration.sh
#
# Behavior:
#   1. Spawn multiple sub-agents to check BitNet concurrently
#   2. Each agent: health check, latency test, diagnostics
#   3. Collect results into unified report
#   4. Log findings to orchestration ledger
#
################################################################################

set -euo pipefail

WORKSPACE_DIR="${WORKSPACE_DIR:-/root/.openclaw/workspace}"
ORCHESTRATION_LOG="${WORKSPACE_DIR}/bitnet-orchestration-$(date +%Y%m%d).jsonl"
TIMESTAMP=$(date -u +%Y-%m-%dT%H:%M:%SZ)
RESULTS_DIR="${WORKSPACE_DIR}/.bitnet-check-results-$(date +%s)"

mkdir -p "$RESULTS_DIR"

# Utility
log_orchestration() {
    local event="$1"
    local agent="$2"
    local status="$3"
    local detail="${4:-}"
    
    cat >> "$ORCHESTRATION_LOG" << EOF
{"timestamp":"$TIMESTAMP","event":"$event","agent":"$agent","status":"$status","detail":"$detail"}
EOF
}

################################################################################
# AGENT TASK DEFINITIONS
################################################################################

# Task 1: Direct Health Check (Bash)
task_direct_health_check() {
    local agent_name="$1"
    local result_file="${RESULTS_DIR}/${agent_name}-health.json"
    
    echo "[Agent: $agent_name] Running direct health check..."
    
    # Perform health check
    local health=$(curl -s -m 2 "http://127.0.0.1:8080/health" 2>/dev/null || echo '{"status":"timeout"}')
    
    # Save result
    cat > "$result_file" << EOF
{
  "agent": "$agent_name",
  "task": "direct_health_check",
  "timestamp": "$TIMESTAMP",
  "result": $health,
  "method": "curl /health"
}
EOF
    
    log_orchestration "health_check" "$agent_name" "complete" "result saved"
    echo "✅ $agent_name: Health check complete"
}

# Task 2: Latency Test (Bash)
task_latency_test() {
    local agent_name="$1"
    local result_file="${RESULTS_DIR}/${agent_name}-latency.json"
    
    echo "[Agent: $agent_name] Running latency test..."
    
    local start=$(date +%s%N)
    local response=$(curl -s -m 5 -X POST "http://127.0.0.1:8080/v1/completions" \
        -H "Content-Type: application/json" \
        -d '{"prompt": "test", "max_tokens": 5}' 2>/dev/null || echo "")
    local end=$(date +%s%N)
    
    local latency_ms=$(( (end - start) / 1000000 ))
    local tokens=$(echo "$response" | jq -r '.tokens_predicted // 0' 2>/dev/null || echo "0")
    
    # Save result
    cat > "$result_file" << EOF
{
  "agent": "$agent_name",
  "task": "latency_test",
  "timestamp": "$TIMESTAMP",
  "latency_ms": $latency_ms,
  "tokens_predicted": $tokens,
  "success": $([ -n "$response" ] && echo "true" || echo "false")
}
EOF
    
    log_orchestration "latency_test" "$agent_name" "complete" "${latency_ms}ms"
    echo "✅ $agent_name: Latency test complete (${latency_ms}ms)"
}

# Task 3: Process Status Check (Bash)
task_process_check() {
    local agent_name="$1"
    local result_file="${RESULTS_DIR}/${agent_name}-process.json"
    
    echo "[Agent: $agent_name] Checking process status..."
    
    # Check for inference processes
    local process_info=$(ps aux | grep -E "(bitnet|llama-server|grok|inference)" | grep -v grep | head -1 || echo "")
    local process_found=$([ -n "$process_info" ] && echo "true" || echo "false")
    local pid=$(echo "$process_info" | awk '{print $2}' || echo "unknown")
    
    # Save result
    cat > "$result_file" << EOF
{
  "agent": "$agent_name",
  "task": "process_check",
  "timestamp": "$TIMESTAMP",
  "process_found": $process_found,
  "pid": "$pid",
  "process_info": "$(echo "$process_info" | sed 's/"/\\"/g')"
}
EOF
    
    log_orchestration "process_check" "$agent_name" "complete" "found=$process_found"
    echo "✅ $agent_name: Process check complete"
}

# Task 4: Port Status Check (Bash)
task_port_check() {
    local agent_name="$1"
    local result_file="${RESULTS_DIR}/${agent_name}-port.json"
    
    echo "[Agent: $agent_name] Checking port 8080..."
    
    # Check if port is listening
    local port_open=$(ss -tuln 2>/dev/null | grep -q ":8080 " && echo "true" || echo "false")
    local port_info=$(ss -tuln 2>/dev/null | grep ":8080" || echo "")
    
    # Save result
    cat > "$result_file" << EOF
{
  "agent": "$agent_name",
  "task": "port_check",
  "timestamp": "$TIMESTAMP",
  "port": 8080,
  "open": $port_open,
  "port_info": "$(echo "$port_info" | sed 's/"/\\"/g')"
}
EOF
    
    log_orchestration "port_check" "$agent_name" "complete" "open=$port_open"
    echo "✅ $agent_name: Port check complete"
}

################################################################################
# ORCHESTRATION
################################################################################

main() {
    echo ""
    echo "╔════════════════════════════════════════════════════════════════╗"
    echo "║         BitNet Health Check Orchestration                      ║"
    echo "║         $(date -u +%Y-%m-%d\ %H:%M:%S\ UTC)                                    ║"
    echo "╚════════════════════════════════════════════════════════════════╝"
    echo ""
    echo "Results directory: $RESULTS_DIR"
    echo "Orchestration log: $ORCHESTRATION_LOG"
    echo ""
    
    # Define agents (could be extended to spawn sub-agents)
    local agents=("bash-1" "bash-2" "bash-3")
    
    log_orchestration "orchestration_start" "main" "begun" "agents=${#agents[@]}"
    
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo "🚀 Spawning Agents"
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo ""
    
    # Run checks for each agent (in parallel, but bash makes them sequential)
    for agent in "${agents[@]}"; do
        echo "[$(date +'%H:%M:%S')] Spawning: $agent"
        
        # Run all tasks for this agent in background
        (
            task_direct_health_check "$agent"
            task_latency_test "$agent"
            task_process_check "$agent"
            task_port_check "$agent"
        ) &
        
        # Slight stagger to avoid thundering herd
        sleep 0.5
    done
    
    # Wait for all background jobs
    wait
    
    echo ""
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo "📊 Results Summary"
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo ""
    
    # Aggregate results
    for agent in "${agents[@]}"; do
        echo "Agent: $agent"
        echo "  Health:"
        jq '.result.status // "unknown"' "${RESULTS_DIR}/${agent}-health.json" 2>/dev/null | sed 's/^/    /'
        
        echo "  Latency:"
        jq '.latency_ms' "${RESULTS_DIR}/${agent}-latency.json" 2>/dev/null | sed 's/^/    /'
        
        echo "  Process:"
        jq '.process_found' "${RESULTS_DIR}/${agent}-process.json" 2>/dev/null | sed 's/^/    /'
        
        echo "  Port:"
        jq '.open' "${RESULTS_DIR}/${agent}-port.json" 2>/dev/null | sed 's/^/    /'
        echo ""
    done
    
    # Unified view
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo "🎯 Unified Health Status"
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo ""
    
    # Check if all agents agree
    local health_statuses=$(find "$RESULTS_DIR" -name "*-health.json" -exec jq -r '.result.status' {} \;)
    local all_ok=$(echo "$health_statuses" | grep -c "^ok$" || echo 0)
    local total_checks=$(echo "$health_statuses" | wc -l)
    
    echo "Health Status: $all_ok/$total_checks agents report OK"
    
    if [ "$all_ok" -eq "$total_checks" ]; then
        echo "✅ BitNet is HEALTHY across all agents"
        log_orchestration "orchestration_summary" "main" "healthy" "all_agents_ok"
    else
        echo "⚠️  BitNet has issues on some agents"
        log_orchestration "orchestration_summary" "main" "degraded" "some_agents_failing"
    fi
    
    # Latency stats
    echo ""
    echo "Latency Statistics:"
    local latencies=$(find "$RESULTS_DIR" -name "*-latency.json" -exec jq -r '.latency_ms' {} \;)
    local min=$(echo "$latencies" | sort -n | head -1)
    local max=$(echo "$latencies" | sort -n | tail -1)
    local avg=$(echo "$latencies" | awk '{sum+=$1; count++} END {print int(sum/count)}')
    
    echo "  Min:  ${min}ms"
    echo "  Max:  ${max}ms"
    echo "  Avg:  ${avg}ms"
    
    log_orchestration "latency_stats" "main" "measured" "min=${min}ms avg=${avg}ms max=${max}ms"
    
    echo ""
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo "📁 File Structure"
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo ""
    echo "Results:"
    ls -la "$RESULTS_DIR"/ | sed 's/^/  /'
    echo ""
    echo "View individual results:"
    echo "  jq '.' ${RESULTS_DIR}/bash-1-health.json"
    echo "  jq '.' ${RESULTS_DIR}/bash-1-latency.json"
    echo ""
    echo "View orchestration log:"
    echo "  tail -20 $ORCHESTRATION_LOG | jq '.'"
    echo ""
}

main "$@"
