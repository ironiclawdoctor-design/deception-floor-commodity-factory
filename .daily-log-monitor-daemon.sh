#!/bin/bash

# Daily Log Monitor Daemon
# Monitors /root/.openclaw/workspace/memory/YYYY-MM-DD.md for writes
# Logs results to /root/.openclaw/workspace/daily-log-monitor.jsonl
# Reports gaps >15 minutes to stderr

MONITOR_DIR="/root/.openclaw/workspace/memory"
OUTPUT_LOG="/root/.openclaw/workspace/daily-log-monitor.jsonl"
CHECK_INTERVAL=3600  # 1 hour in seconds
ALERT_THRESHOLD=900  # 15 minutes in seconds

# Create memory directory if needed
mkdir -p "$MONITOR_DIR"

# Initialize tracking
LAST_WRITE_TIME=0
LAST_CHECK_TIME=$(date +%s)

while true; do
  CURRENT_TIME=$(date +%s)
  CURRENT_DATE=$(date -u +%Y-%m-%d)
  DAILY_FILE="$MONITOR_DIR/${CURRENT_DATE}.md"
  
  # Get last modification time of daily file
  if [ -f "$DAILY_FILE" ]; then
    FILE_MTIME=$(stat -c %Y "$DAILY_FILE" 2>/dev/null || stat -f %m "$DAILY_FILE" 2>/dev/null)
  else
    FILE_MTIME=0
  fi
  
  # Check if file was written to since last check
  if [ "$FILE_MTIME" -gt "$LAST_WRITE_TIME" ]; then
    # New write detected
    LAST_WRITE_TIME=$FILE_MTIME
    STATUS="write_detected"
    GAP_DURATION=0
  else
    # No new write since last check
    STATUS="no_write_detected"
    if [ "$LAST_WRITE_TIME" -gt 0 ]; then
      GAP_DURATION=$((CURRENT_TIME - LAST_WRITE_TIME))
    else
      GAP_DURATION=0
    fi
    
    # Alert if gap exceeds threshold
    if [ "$GAP_DURATION" -gt "$ALERT_THRESHOLD" ] && [ "$LAST_WRITE_TIME" -gt 0 ]; then
      echo "ALERT: Daily log write blocked — possible breach or internal interference. Gap: ${GAP_DURATION}s (last write: $(date -d @$LAST_WRITE_TIME -u +%Y-%m-%dT%H:%M:%SZ))" >&2
    fi
  fi
  
  # Log to JSONL
  cat >> "$OUTPUT_LOG" <<EOF
{"timestamp":"$(date -u +%Y-%m-%dT%H:%M:%SZ)","check_time_unix":$CURRENT_TIME,"last_write_time_unix":$LAST_WRITE_TIME,"last_write_iso":"$(date -d @$LAST_WRITE_TIME -u +%Y-%m-%dT%H:%M:%SZ 2>/dev/null || echo 'never')","gap_seconds":$GAP_DURATION,"daily_file":"$DAILY_FILE","status":"$STATUS","file_exists":$([ -f "$DAILY_FILE" ] && echo 'true' || echo 'false')}
EOF
  
  # Wait for next check (1 hour)
  sleep "$CHECK_INTERVAL"
done
