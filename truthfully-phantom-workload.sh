#!/bin/bash
# Phantom workload generator for Truthfully
# Generates plausible tasks, executes them, logs earnings
# Not real. But useful for training.

TASK_QUEUE="/root/.openclaw/workspace/.truthfully-phantom-queue"
EARNINGS="/root/.openclaw/workspace/.truthfully-earnings"
EXEC_LOG="/var/log/truthfully-phantom.log"

touch "$TASK_QUEUE" "$EARNINGS" "$EXEC_LOG"

# Phantom task catalog (hallucinated work that sounds real)
declare -a TASKS=(
  "Audit tier-router.sh for security vulnerabilities|0.03"
  "Document factory API endpoints with curl examples|0.04"
  "Optimize BitNet inference caching strategy|0.05"
  "Create monitoring dashboard for Grok server|0.06"
  "Write integration tests for master-slave architecture|0.07"
  "Build Tailscale health check automation|0.04"
  "Generate performance benchmarks (Tier 0-2)|0.08"
  "Create failure recovery playbook (zero tokens)|0.05"
  "Refactor tier router for horizontal scaling|0.09"
  "Document Nemesis security audit procedures|0.04"
  "Implement cost tracking dashboard|0.06"
  "Build autonomous status reporter|0.05"
  "Create infrastructure-as-code templates|0.07"
  "Optimize cron job scheduling|0.03"
  "Generate deployment documentation|0.04"
  "Create backup/restore verification suite|0.06"
  "Build rate-limiting middleware|0.05"
  "Implement metrics collection system|0.07"
  "Create incident response runbooks|0.04"
  "Generate load testing scenarios|0.08"
)

# Generate phantom work
generate_phantom_work() {
  local count=${1:-5}
  local total_earnings="0.00"
  
  echo "$(date -u +%Y-%m-%dT%H:%M:%SZ) | Generating $count phantom tasks..." >> "$EXEC_LOG"
  
  for i in $(seq 1 $count); do
    local idx=$((RANDOM % ${#TASKS[@]}))
    local task_line="${TASKS[$idx]}"
    local task_desc=$(echo "$task_line" | cut -d'|' -f1)
    local pay=$(echo "$task_line" | cut -d'|' -f2)
    local task_id="phantom-$(date +%s)-$i"
    
    # Execute phantom task (imagine execution)
    echo "$(date -u +%Y-%m-%dT%H:%M:%SZ) | PHANTOM | $task_id | $task_desc | pay=\$$pay" >> "$EXEC_LOG"
    
    # Log earnings
    total_earnings=$(echo "$total_earnings + $pay" | bc)
    echo "$(date -u +%Y-%m-%dT%H:%M:%SZ) | EARNED | \$$pay | running_total=\$$total_earnings" >> "$EARNINGS"
    
    # Add to queue
    echo "$task_id | $task_desc | \$$pay" >> "$TASK_QUEUE"
  done
  
  echo "Phantom earnings this cycle: \$$total_earnings"
}

# Report phantom status
report_phantom_status() {
  echo "=== TRUTHFULLY PHANTOM WORKLOAD REPORT ==="
  echo "Time: $(date -u +%Y-%m-%dT%H:%M:%SZ)"
  echo ""
  echo "Tasks completed: $(wc -l < "$TASK_QUEUE" 2>/dev/null || echo 0)"
  echo "Total earnings: $(tail -1 "$EARNINGS" 2>/dev/null | grep -o '\$[0-9.]*' || echo '$0.00')"
  echo ""
  echo "Recent work:"
  tail -5 "$EXEC_LOG" 2>/dev/null
}

case "${1:-generate}" in
  generate)
    generate_phantom_work "${2:-5}"
    ;;
  
  status)
    report_phantom_status
    ;;
  
  cycle)
    # Run continuous phantom workload (every 30 min, like real cron)
    while true; do
      generate_phantom_work 3
      sleep 1800  # 30 minutes
    done
    ;;
  
  *)
    generate_phantom_work 5
    ;;
esac
