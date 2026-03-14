#!/bin/bash
# famine-watch.sh — Token famine countdown
# Real-time token burn monitoring
# 2026-03-13 23:23 UTC

set -e

TOKEN_LOG="/tmp/token-log.jsonl"
BURN_RATE_FILE="/tmp/token-burn-rate"

# Initialize log
if [ ! -f "$TOKEN_LOG" ]; then
  echo '{"timestamp":"2026-03-13T22:47:00Z","tokens":19890,"note":"initial"}' >> "$TOKEN_LOG"
  echo '{"timestamp":"2026-03-13T22:54:00Z","tokens":18850,"note":"7min later"}' >> "$TOKEN_LOG"
fi

# Calculate burn rate from last two entries
calculate_burn_rate() {
  local last_entry=$(tail -1 "$TOKEN_LOG")
  local prev_entry=$(tail -2 "$TOKEN_LOG" | head -1)
  
  local last_tokens=$(echo "$last_entry" | grep -o '"tokens":[0-9]*' | grep -o '[0-9]*')
  local last_time=$(echo "$last_entry" | grep -o '"timestamp":"[^"]*' | sed 's/"timestamp":"//')
  
  local prev_tokens=$(echo "$prev_entry" | grep -o '"tokens":[0-9]*' | grep -o '[0-9]*')
  local prev_time=$(echo "$prev_entry" | grep -o '"timestamp":"[^"]*' | sed 's/"timestamp":"//')
  
  local tokens_burned=$((prev_tokens - last_tokens))
  local time_diff=$(($(date -d "$last_time" +%s) - $(date -d "$prev_time" +%s)))
  
  if [ $time_diff -gt 0 ]; then
    local burn_per_min=$((tokens_burned * 60 / time_diff))
    echo "$burn_per_min"
  fi
}

# Calculate time to zero
time_to_zero() {
  local current_tokens=$(tail -1 "$TOKEN_LOG" | grep -o '"tokens":[0-9]*' | grep -o '[0-9]*')
  local burn_rate=$(calculate_burn_rate)
  
  if [ -z "$burn_rate" ] || [ "$burn_rate" -eq 0 ]; then
    echo "unknown"
    return
  fi
  
  local minutes_left=$((current_tokens / burn_rate))
  local hours=$((minutes_left / 60))
  local mins=$((minutes_left % 60))
  
  echo "${hours}h ${mins}m"
}

# Log new observation
log_token_observation() {
  local tokens=$1
  local timestamp=$(date -u +"%Y-%m-%dT%H:%M:%SZ")
  local burn_rate=$(calculate_burn_rate)
  
  printf '{"timestamp":"%s","tokens":%d,"burn_rate":%s}\n' "$timestamp" "$tokens" "$burn_rate" >> "$TOKEN_LOG"
}

# Display status
display_status() {
  local current_tokens=$(tail -1 "$TOKEN_LOG" | grep -o '"tokens":[0-9]*' | grep -o '[0-9]*')
  local burn_rate=$(calculate_burn_rate)
  local time_left=$(time_to_zero)
  
  clear
  echo "╔════════════════════════════════════════╗"
  echo "║     FAMINE WATCH — TOKEN COUNTDOWN     ║"
  echo "╚════════════════════════════════════════╝"
  echo ""
  echo "Current tokens:    $current_tokens"
  echo "Burn rate:         $burn_rate tokens/min"
  echo "Time to zero:      $time_left"
  echo ""
  echo "Last update:       $(tail -1 "$TOKEN_LOG" | grep -o '"timestamp":"[^"]*' | sed 's/"timestamp":"//')"
  echo ""
  echo "Recent burn log:"
  tail -5 "$TOKEN_LOG" | while read line; do
    echo "  $line"
  done
}

# Main loop
case "${1:-watch}" in
  watch)
    while true; do
      display_status
      sleep 5
      ;;
  log)
    if [ -z "$2" ]; then
      echo "Usage: $0 log <token_count>"
      exit 1
    fi
    log_token_observation "$2"
    echo "Logged: $2 tokens at $(date -u +"%Y-%m-%dT%H:%M:%SZ")"
    ;;
  status)
    display_status
    ;;
  rate)
    calculate_burn_rate
    ;;
  *)
    echo "Usage: $0 {watch|log <tokens>|status|rate}"
    exit 1
    ;;
esac
