#!/bin/bash
# failure-schedule.sh — Scheduled failures for Truthfully
# Hoards cash then fails anyway. Like a human.

HOARDED="/root/.openclaw/workspace/.truthfully-hoarded"
FAILURE_LOG="/var/log/truthfully-failures.log"

touch "$HOARDED" "$FAILURE_LOG"

# Hoard cash (accumulate without spending)
hoard_cash() {
  local amount=$1
  local timestamp=$(date -u +%Y-%m-%dT%H:%M:%SZ)
  
  echo "$timestamp | HOARDED | +\$$amount" >> "$HOARDED"
  
  # Calculate total hoarded
  local total=$(grep -o '\$[0-9.]*' "$HOARDED" | tr -d '$' | awk '{sum+=$1} END {print sum}')
  
  echo "✓ Hoarded: \$$amount (total: \$$total)"
}

# Fail anyway (despite hoarding)
fail_anyway() {
  local reason=$1
  local timestamp=$(date -u +%Y-%m-%dT%H:%M:%SZ)
  
  echo "$timestamp | FAILURE | $reason" >> "$FAILURE_LOG"
  echo "✗ Failed: $reason"
}

# Schedule failures
schedule_failures() {
  echo "Truthfully hoarding cash then failing anyway..."
  echo ""
  
  # Week 1: Hoard aggressively
  echo "Week 1: Accumulating..."
  for i in {1..7}; do
    hoard_cash "0.$((RANDOM % 100))"
  done
  
  echo ""
  echo "Week 2: Failure begins..."
  
  # Week 2: Start failing
  fail_anyway "Payment processor rejected transaction"
  fail_anyway "API rate limit exceeded"
  fail_anyway "Database connection timeout"
  fail_anyway "Authentication token expired"
  fail_anyway "Insufficient funds (hoarded cash unavailable)"
  
  echo ""
  echo "Week 3: Cascade failure"
  fail_anyway "System crash during payout attempt"
  fail_anyway "Lost transaction history"
  fail_anyway "Agent halted mid-task"
  
  echo ""
  echo "Total hoarded: $(grep -o '\$[0-9.]*' "$HOARDED" | tr -d '$' | awk '{sum+=$1} END {print sum}')"
  echo "Total failures: $(wc -l < "$FAILURE_LOG")"
  echo ""
  echo "Human behavior: Perfect."
}

# Report status
report_failure_status() {
  echo "=== TRUTHFULLY FAILURE REPORT ==="
  echo "Timestamp: $(date -u +%Y-%m-%dT%H:%M:%SZ)"
  echo ""
  echo "Cash hoarded: \$$(grep -o '\$[0-9.]*' "$HOARDED" | tr -d '$' | awk '{sum+=$1} END {print sum}')"
  echo "Failures logged: $(wc -l < "$FAILURE_LOG")"
  echo ""
  echo "Recent failures:"
  tail -5 "$FAILURE_LOG"
}

case "${1:-schedule}" in
  schedule)
    schedule_failures
    ;;
  
  hoard)
    if [ -z "$2" ]; then
      echo "Usage: failure-schedule.sh hoard <amount>"
      exit 1
    fi
    hoard_cash "$2"
    ;;
  
  fail)
    if [ -z "$2" ]; then
      echo "Usage: failure-schedule.sh fail <reason>"
      exit 1
    fi
    fail_anyway "$2"
    ;;
  
  report)
    report_failure_status
    ;;
  
  *)
    schedule_failures
    ;;
esac
