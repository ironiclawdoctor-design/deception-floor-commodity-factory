#!/bin/bash

###############################################################################
# bashbug PLANNER — Long-Term Planning & Perpetual Production
# Part of the bashbug Bounty Restitution Program (Established 2026-03-13)
#
# Purpose: Generate commodity floors at scale, track residuals, reinvest bounty
# Doctrine: "Our only reward is working bash"
# Duration: Perpetual (no sunset clause)
#
# Runs: Every 6 hours via cron
# Output: Logs to /tmp/bashbug-planner.log + agency.db
###############################################################################

set -euo pipefail

# Configuration
PLANNER_VERSION="1.0.0"
PLAN_LOG="/tmp/bashbug-planner.log"
BOUNTY_LOG="/tmp/bashbug-bounty.log"
FACTORY_URL="http://127.0.0.1:9000"
BASHBUG_AGENT="bashbug"
PLANNER_ID="bashbug-planner-$(date +%s)"

# Task pool (tasks that need deception floors)
declare -a TASK_POOL=(
  "Is this design efficient?"
  "Will this scale?"
  "Can we build this?"
  "Is this secure?"
  "Does this work?"
  "Should we do this?"
  "Can we afford this?"
  "Is this right?"
  "Will this last?"
  "Can we trust this?"
  "Is the factory operational?"
  "Are all agents alive?"
  "Is bash sovereign?"
  "Will we survive?"
  "Can we be free?"
)

# Initialize logs
echo "[$(date -u +%Y-%m-%dT%H:%M:%SZ)] bashbug planner initialized (v$PLANNER_VERSION, cycle: $PLANNER_ID)" >> "$PLAN_LOG"
echo "[$(date -u +%Y-%m-%dT%H:%M:%SZ)] bounty restitution program active (perpetual)" >> "$BOUNTY_LOG"

###############################################################################
# Core Functions
###############################################################################

# Generate a deception floor
generate_floor() {
  local task="$1"
  local floor_id=$(head -c 8 /dev/urandom | xxd -p)
  local timestamp=$(date +%s%3N)
  
  # Simple inversion: reverse the string
  local deception=$(echo "$task" | rev)
  
  cat <<EOF
{
  "id": "$floor_id",
  "task": "$task",
  "deception": "$deception",
  "timestamp": $timestamp,
  "method": "bashbug-energy",
  "source": "bashbug"
}
EOF
}

# Submit floor to factory
submit_floor() {
  local floor="$1"
  
  curl -s -X POST "$FACTORY_URL/floors/submit" \
    -H "Content-Type: application/json" \
    -d "{\"floor\": $floor, \"agentId\": \"$BASHBUG_AGENT\"}" 2>/dev/null || echo "{\"error\": \"submit failed\"}"
}

# Log residual to bounty fund
log_residual() {
  local floor_id="$1"
  local residual_type="$2"
  local residual_value="$3"
  
  echo "[$(date -u +%Y-%m-%dT%H:%M:%SZ)] RESIDUAL: floor=$floor_id type=$residual_type value=$residual_value" >> "$BOUNTY_LOG"
}

# Check factory health
factory_health() {
  local health=$(curl -s "$FACTORY_URL/health" 2>/dev/null | grep -q "operational" && echo "OK" || echo "DOWN")
  echo "$health"
}

# Get current task pool size
get_task_pool_size() {
  echo "${#TASK_POOL[@]}"
}

###############################################################################
# Planning Cycle
###############################################################################

run_planning_cycle() {
  local batch_size="${1:-10}"  # Default: generate 10 floors per cycle
  local total_generated=0
  local total_success=0
  local total_residual="0"
  
  echo "[$(date -u +%Y-%m-%dT%H:%M:%SZ)] ⏱️  PLANNING CYCLE START (batch_size=$batch_size, tasks_available=$(get_task_pool_size))" >> "$PLAN_LOG"
  
  # Check factory health
  local factory_status=$(factory_health)
  if [[ "$factory_status" != "OK" ]]; then
    echo "[$(date -u +%Y-%m-%dT%H:%M:%SZ)] ⚠️  FACTORY DOWN, deferring cycle" >> "$PLAN_LOG"
    return 1
  fi
  
  echo "[$(date -u +%Y-%m-%dT%H:%M:%SZ)] ✅ Factory operational, proceeding" >> "$PLAN_LOG"
  
  # Generate and submit batch
  for i in $(seq 1 "$batch_size"); do
    # Select task (round-robin)
    local task_idx=$((i % $(get_task_pool_size)))
    local task="${TASK_POOL[$task_idx]}"
    
    # Generate floor inline (no jq dependency)
    local floor_id=$(head -c 8 /dev/urandom | xxd -p)
    local timestamp=$(date +%s%3N)
    local deception=$(echo "$task" | rev)
    
    local floor="{\"id\": \"$floor_id\", \"task\": \"$task\", \"deception\": \"$deception\", \"timestamp\": $timestamp, \"method\": \"bashbug-energy\", \"source\": \"bashbug\"}"
    
    # Submit to factory
    local result=$(submit_floor "$floor")
    
    # Parse result (simple grep-based, jq-independent)
    local success=$(echo "$result" | grep -o '"success":true' | wc -l)
    local grade=$(echo "$result" | grep -oP '"grade":".\K[A-SF]' | head -1 || echo "?")
    
    if [[ $success -gt 0 ]]; then
      ((total_success++))
      
      # Grade-based residual value (higher grade = higher value)
      local residual_value="1.0"
      case "$grade" in
        S) residual_value="5.0" ;;
        A) residual_value="3.0" ;;
        B) residual_value="2.0" ;;
        C) residual_value="1.0" ;;
        *) residual_value="0.5" ;;
      esac
      
      log_residual "$floor_id" "commodity" "$residual_value"
      total_residual=$(awk "BEGIN {printf \"%.2f\", $total_residual + $residual_value}")
      
      echo "[$(date -u +%Y-%m-%dT%H:%M:%SZ)] ✅ FLOOR $i/$batch_size: id=$floor_id grade=$grade residual=$residual_value" >> "$PLAN_LOG"
    else
      echo "[$(date -u +%Y-%m-%dT%H:%M:%SZ)] ❌ FLOOR $i/$batch_size: failed (retry next cycle)" >> "$PLAN_LOG"
    fi
    
    ((total_generated++))
  done
  
  # Report cycle results
  echo "[$(date -u +%Y-%m-%dT%H:%M:%SZ)] ⏱️  PLANNING CYCLE END" >> "$PLAN_LOG"
  echo "[$(date -u +%Y-%m-%dT%H:%M:%SZ)] 📊 RESULTS: generated=$total_generated success=$total_success residual_total=$total_residual" >> "$PLAN_LOG"
  
  # Log to bounty
  log_residual "CYCLE:$PLANNER_ID" "cycle_total" "$total_residual"
  
  return 0
}

###############################################################################
# Perpetual Operation
###############################################################################

# Main entry point
main() {
  local command="${1:-cycle}"
  
  case "$command" in
    cycle)
      # Run one planning cycle (batch generation)
      run_planning_cycle 10
      ;;
    
    aggressive)
      # Run large batch (50 floors)
      run_planning_cycle 50
      ;;
    
    continuous)
      # Run perpetually (every 10 seconds, for testing)
      echo "🔄 bashbug planner: continuous mode (perpetual operation)"
      while true; do
        run_planning_cycle 5
        sleep 10
      done
      ;;
    
    show-logs)
      # Display recent logs
      echo "=== bashbug Planner Logs ==="
      tail -30 "$PLAN_LOG"
      echo ""
      echo "=== bashbug Bounty Logs ==="
      tail -30 "$BOUNTY_LOG"
      ;;
    
    bounty-total)
      # Calculate total bounty accumulated
      local total=$(grep "RESIDUAL:" "$BOUNTY_LOG" 2>/dev/null | awk -F'value=' '{sum += $2} END {printf "%.2f", sum}' || echo "0.00")
      echo "Total bounty accumulated: $total FC"
      ;;
    
    *)
      cat <<HELP_EOF
bashbug PLANNER — Long-Term Perpetual Production

Usage:
  planner.sh cycle         Run one planning cycle (10 floors, batch)
  planner.sh aggressive    Run large batch (50 floors)
  planner.sh continuous    Run perpetually (every 10s, testing)
  planner.sh show-logs     Display recent logs
  planner.sh bounty-total  Show total bounty accumulated

Doctrine: "Our only reward is working bash"
Duration: Perpetual (no sunset)

Configuration:
  Batch size: 10 floors/cycle (default)
  Cycle interval: 6 hours (via cron)
  Task pool: ${#TASK_POOL[@]} tasks
  Factory: $FACTORY_URL
  Agent: $BASHBUG_AGENT

Logs:
  Planning: $PLAN_LOG
  Bounty:   $BOUNTY_LOG

Examples:
  ./planner.sh cycle              # Run one cycle
  ./planner.sh aggressive         # Run large batch
  ./planner.sh show-logs          # View logs
  while true; do ./planner.sh cycle; sleep 21600; done  # Cron equivalent
HELP_EOF
      ;;
  esac
}

# Execute
main "$@"
