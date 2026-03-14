#!/bin/bash
# Truthfully status report every 30 minutes
# Logs all chores, reports completion

LOG="/var/log/truthfully-status.log"
TASKS="/root/.openclaw/workspace/.truthfully-tasks"

report_status() {
  local timestamp=$(date -u +"%Y-%m-%dT%H:%M:%SZ")
  local status=$(systemctl is-active truthfully 2>/dev/null || echo "stopped")
  local tasks_completed=$(wc -l < "$TASKS" 2>/dev/null || echo 0)
  local earnings=$(grep -o '\$[0-9.]*' /var/log/truthfully.log 2>/dev/null | tail -1 || echo "$0.00")
  
  echo "$timestamp | status=$status | tasks=$tasks_completed | earnings=$earnings" >> "$LOG"
  
  # Also print to stdout for cron visibility
  echo "Truthfully Status Report ($timestamp)"
  echo "===================================="
  echo "Status: $status"
  echo "Tasks completed: $tasks_completed"
  echo "Latest earnings: $earnings"
  echo "Log: $LOG"
}

report_status
