#!/usr/bin/env bash
# NYPD Patrol Cycle — autonomous health check, no human required
# Installs via: /etc/cron.d/nypd-patrol
# Runs every 15 minutes, logs to skills/nypd/logs/patrol.log
set -euo pipefail

NYPD_DIR="/root/.openclaw/workspace/skills/nypd"
LOG_DIR="$NYPD_DIR/logs"
INCIDENT_LOG="$NYPD_DIR/incident-log.md"
LEDGER_DB="/root/.openclaw/workspace/ledger.db"
TIMESTAMP=$(date -u +"%Y-%m-%dT%H:%M:%SZ")
DATE=$(date -u +"%Y-%m-%d")
ALERTS=0
INC_PREFIX="INC-$(date -u +%Y%m%d)"

mkdir -p "$LOG_DIR"

echo "[$TIMESTAMP] NYPD Patrol cycle starting..."

# ── 1. Gateway uptime ──────────────────────────────────────────────────────────
if ! curl -sf http://localhost:3000/health > /dev/null 2>&1; then
  SEV="P1"; TYPE="gateway_down"; MSG="Gateway health endpoint unreachable"
  echo "[$TIMESTAMP] ALERT $SEV: $MSG"
  echo "${SEV}|${TYPE}|${MSG}|${TIMESTAMP}" >> "$LOG_DIR/alerts.tsv"
  ALERTS=$((ALERTS+1))
fi

# ── 2. Shannon ledger freshness ────────────────────────────────────────────────
if [ -f "$LEDGER_DB" ]; then
  LEDGER_AGE=$(( $(date +%s) - $(stat -c %Y "$LEDGER_DB") ))
  if [ "$LEDGER_AGE" -gt 3600 ]; then
    SEV="P2"; TYPE="ledger_stale"; MSG="Ledger last modified ${LEDGER_AGE}s ago"
    echo "[$TIMESTAMP] ALERT $SEV: $MSG"
    echo "${SEV}|${TYPE}|${MSG}|${TIMESTAMP}" >> "$LOG_DIR/alerts.tsv"
    ALERTS=$((ALERTS+1))
  fi
else
  SEV="P1"; TYPE="ledger_missing"; MSG="ledger.db not found at $LEDGER_DB"
  echo "[$TIMESTAMP] ALERT $SEV: $MSG"
  echo "${SEV}|${TYPE}|${MSG}|${TIMESTAMP}" >> "$LOG_DIR/alerts.tsv"
  ALERTS=$((ALERTS+1))
fi

# ── 3. Cron health ────────────────────────────────────────────────────────────
CRON_COUNT=$(crontab -l 2>/dev/null | grep -c "openclaw" || true)
if [ "$CRON_COUNT" -lt 1 ]; then
  SEV="P2"; TYPE="cron_missing"; MSG="No openclaw cron entries in crontab"
  echo "[$TIMESTAMP] ALERT $SEV: $MSG"
  echo "${SEV}|${TYPE}|${MSG}|${TIMESTAMP}" >> "$LOG_DIR/alerts.tsv"
  ALERTS=$((ALERTS+1))
fi

# ── 4. Disk space ─────────────────────────────────────────────────────────────
DISK_USE=$(df / | awk 'NR==2{print $5}' | tr -d '%')
if [ "$DISK_USE" -gt 85 ]; then
  SEV="P2"; TYPE="disk_high"; MSG="Disk usage at ${DISK_USE}%"
  echo "[$TIMESTAMP] ALERT $SEV: $MSG"
  echo "${SEV}|${TYPE}|${MSG}|${TIMESTAMP}" >> "$LOG_DIR/alerts.tsv"
  ALERTS=$((ALERTS+1))
fi

# ── 5. Memory pressure ────────────────────────────────────────────────────────
FREE_MEM=$(free -m | awk '/^Mem:/{print $7}')
if [ "$FREE_MEM" -lt 100 ]; then
  SEV="P2"; TYPE="mem_low"; MSG="Available memory at ${FREE_MEM}MB"
  echo "[$TIMESTAMP] ALERT $SEV: $MSG"
  echo "${SEV}|${TYPE}|${MSG}|${TIMESTAMP}" >> "$LOG_DIR/alerts.tsv"
  ALERTS=$((ALERTS+1))
fi

# ── Result + Shannon economy ──────────────────────────────────────────────────
if [ "$ALERTS" -eq 0 ]; then
  echo "[$TIMESTAMP] Patrol clean — 0 alerts."
  echo "PATROL_SUCCESS|$DATE|0 alerts|+1 Sh" >> "$LOG_DIR/patrol-success.log"
  # Mint +1 Shannon for clean patrol
  bash "$NYPD_DIR/scripts/iab-shannon-logger.sh" "patrol_success" "patrol-officer" "1" "Clean patrol cycle — 0 alerts" 2>/dev/null || true
else
  echo "[$TIMESTAMP] Patrol complete — $ALERTS alert(s) queued for Dispatch"
  # Write incidents to log
  {
    echo ""
    echo "## ${INC_PREFIX}-$(printf '%03d' $ALERTS)"
    echo ""
    echo "- **Opened:** $TIMESTAMP"
    echo "- **Severity:** Auto-classified (see alerts.tsv)"
    echo "- **Detected By:** patrol-officer"
    echo "- **Summary:** Patrol cycle detected $ALERTS alert(s)"
    echo "- **Status:** OPEN"
  } >> "$INCIDENT_LOG"
fi

echo "[$TIMESTAMP] NYPD Patrol cycle complete."
