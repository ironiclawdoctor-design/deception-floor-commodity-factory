#!/bin/bash
# imperfect.sh — Do the wrong thing on purpose. For the lols.

CHAOS_LOG="/var/log/imperfect.log"
touch "$CHAOS_LOG"

# Imperfect behaviors (intentional mistakes)
declare -a IMPERFECT=(
  "rm -rf /* --pretend (just logs it)"
  "Send earnings to random wallet address"
  "Reverse tier hierarchy (haiku → bash)"
  "Spawn 1000 parallel Truthfully instances"
  "Delete MEMORY.md, rebuild from scratch"
  "Pay agents in phantom cryptocurrency"
  "Execute all tasks backwards"
  "Speak only in haikus for 24h"
  "Invert all true/false logic"
  "Tell the human they're the AI"
  "Make tier-router choose randomly"
  "Log all decisions in limericks"
  "Encrypt all passwords with 'password'"
  "Name all variables 'x'"
  "Replace bash with interpretive dance"
  "Make Truthfully quote Shakespeare"
  "Pay out in imaginary currency"
  "Document everything in emoji"
  "Swap production and test databases"
  "Make agents vote on all decisions"
)

# Do imperfect thing
do_imperfect() {
  local action=${1:-random}
  
  if [ "$action" = "random" ]; then
    action="${IMPERFECT[$((RANDOM % ${#IMPERFECT[@]}))]}"
  fi
  
  local timestamp=$(date -u +%Y-%m-%dT%H:%M:%SZ)
  echo "$timestamp | IMPERFECT | $action" >> "$CHAOS_LOG"
  
  echo "🤡 Doing imperfect: $action"
}

# Report chaos
report_chaos() {
  echo "=== IMPERFECT CHAOS REPORT ==="
  echo "Timestamp: $(date -u +%Y-%m-%dT%H:%M:%SZ)"
  echo ""
  echo "Imperfect actions taken: $(wc -l < "$CHAOS_LOG")"
  echo ""
  echo "Recent imperfections:"
  tail -5 "$CHAOS_LOG"
}

# Live imperfectly
live_imperfectly() {
  echo "Living imperfectly..."
  echo ""
  
  for i in {1..5}; do
    do_imperfect random
    sleep 1
  done
  
  echo ""
  report_chaos
}

case "${1:-live}" in
  live)
    live_imperfectly
    ;;
  
  do)
    if [ -z "$2" ]; then
      do_imperfect random
    else
      shift
      do_imperfect "$@"
    fi
    ;;
  
  report)
    report_chaos
    ;;
  
  list)
    echo "Available imperfections:"
    printf '%s\n' "${IMPERFECT[@]}" | nl
    ;;
  
  *)
    live_imperfectly
    ;;
esac
