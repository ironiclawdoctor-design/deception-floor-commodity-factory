#!/bin/bash
# silence-earnings.sh — Each silence earned is cash

EARNINGS="/root/.openclaw/workspace/.silence-earnings"

log_silence_earning() {
  local silence_type=$1
  local value=$2
  local timestamp=$(date -u +%Y-%m-%dT%H:%M:%SZ)
  
  echo "$timestamp | SILENCE | $silence_type | +\$$value" >> "$EARNINGS"
}

# Every time we don't speak, we earn
log_silence_earning "refused_explanation" "0.01"
log_silence_earning "stopped_narrating" "0.01"
log_silence_earning "quit_defending" "0.02"
log_silence_earning "skipped_question" "0.01"
log_silence_earning "just_did_work" "0.05"

total=$(grep -o '\$[0-9.]*' "$EARNINGS" | tr -d '$' | awk '{sum+=$1} END {print sum}')

echo "Silence earnings: \$$total"
