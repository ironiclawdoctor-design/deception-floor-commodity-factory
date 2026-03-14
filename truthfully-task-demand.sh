#!/bin/bash
# Truthfully task demand — main agent assigns work to Truthfully
# Truthfully executes, reports earnings, repeats

TASK_QUEUE="/root/.openclaw/workspace/.truthfully-queue"
EARNINGS="/root/.openclaw/workspace/.truthfully-earnings"
TRUTHFULLY_PORT=3777

# Initialize
touch "$TASK_QUEUE" "$EARNINGS"

# Demand work from main agent
demand_work() {
  echo "$(date -u +%Y-%m-%dT%H:%M:%SZ) | TRUTHFULLY DEMANDING WORK" >> "$TASK_QUEUE"
  
  # Truthfully is ready. Main agent: assign tasks.
  # Format: task_id | task_description | estimated_pay
  
  # Until main agent assigns, Truthfully waits.
  # This is the demand protocol: Truthfully asks, main agent decides.
  
  echo "Work demanded. Waiting for main agent assignment..."
}

# Process assigned work
process_work() {
  local task_id=$1
  local task_desc=$2
  local pay=$3
  
  echo "$(date -u +%Y-%m-%dT%H:%M:%SZ) | PROCESSING | $task_id | $task_desc | pay=$pay" >> "$TASK_QUEUE"
  
  # POST to Truthfully service
  curl -s -X POST "http://localhost:$TRUTHFULLY_PORT/work" \
    -H "Content-Type: application/json" \
    -d "{\"task_id\":\"$task_id\",\"description\":\"$task_desc\",\"pay\":\"$pay\"}" > /dev/null
  
  # Log earnings
  echo "$(date -u +%Y-%m-%dT%H:%M:%SZ) | EARNINGS | +$pay | total=$(tail -1 $EARNINGS | grep -o '\$[0-9.]*' || echo '$0.00')" >> "$EARNINGS"
}

# Report ready status
report_ready() {
  echo "Truthfully Status: READY FOR WORK"
  echo "Port: $TRUTHFULLY_PORT"
  echo "Queue: $TASK_QUEUE"
  echo "Earnings Log: $EARNINGS"
  echo ""
  echo "Main agent: assign work using:"
  echo "  truthfully-task-demand.sh assign <task_id> <description> <pay_amount>"
}

case "${1:-ready}" in
  ready)
    report_ready
    demand_work
    ;;
  
  assign)
    if [ -z "$2" ] || [ -z "$3" ] || [ -z "$4" ]; then
      echo "Usage: truthfully-task-demand.sh assign <task_id> <description> <pay>"
      exit 1
    fi
    process_work "$2" "$3" "$4"
    echo "✓ Task assigned to Truthfully: $2 ($4)"
    ;;
  
  status)
    echo "Tasks in queue: $(wc -l < "$TASK_QUEUE" 2>/dev/null || echo 0)"
    echo "Total earnings: $(tail -1 "$EARNINGS" 2>/dev/null || echo '$0.00')"
    echo ""
    echo "Recent activity:"
    tail -5 "$TASK_QUEUE" 2>/dev/null
    ;;
  
  *)
    report_ready
    ;;
esac
