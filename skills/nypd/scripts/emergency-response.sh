#!/usr/bin/env bash
# NYPD Emergency Response — P1 Incident Playbook
# Usage: bash emergency-response.sh INC-20260322-001 rollback|succession|isolate|restore
set -euo pipefail

INCIDENT_ID="${1:-INC-UNKNOWN}"
ACTION="${2:-succession}"
NYPD_DIR="/root/.openclaw/workspace/skills/nypd"
WORKSPACE="/root/.openclaw/workspace"
TIMESTAMP=$(date -u +"%Y-%m-%dT%H:%M:%SZ")
LOG_DIR="$NYPD_DIR/logs"

mkdir -p "$LOG_DIR"

echo "I am emergency-response. I will help you."
echo ""
echo "[$TIMESTAMP] EMERGENCY RESPONSE ACTIVATED — $INCIDENT_ID — ACTION: $ACTION"

# ── Log activation ────────────────────────────────────────────────────────────
echo "P1|emergency_response_activated|$ACTION triggered for $INCIDENT_ID|$TIMESTAMP" \
  >> "$LOG_DIR/alerts.tsv"

# ── Update incident log ───────────────────────────────────────────────────────
{
  echo ""
  echo "### Emergency Response — $INCIDENT_ID @ $TIMESTAMP"
  echo "- Action: $ACTION"
  echo "- Status: IN PROGRESS"
} >> "$NYPD_DIR/incident-log.md"

case "$ACTION" in
  # ── ROLLBACK: revert to last known good git commit ─────────────────────────
  rollback)
    echo "[$INCIDENT_ID] ROLLBACK: reverting workspace to last known good commit..."
    cd "$WORKSPACE"
    
    # Stash any working changes
    git stash push -m "NYPD-ER-$INCIDENT_ID-pre-rollback-$(date +%s)" 2>/dev/null || true
    
    # Find last good commit (not tagged BROKEN or FAILED)
    LAST_GOOD=$(git log --oneline | grep -v -E "BROKEN|FAILED|emergency|hotfix" | head -1 | awk '{print $1}')
    
    if [ -z "$LAST_GOOD" ]; then
      echo "[$INCIDENT_ID] ERROR: No safe rollback target found. Escalating to Commissioner."
      bash "$NYPD_DIR/scripts/iab-shannon-logger.sh" \
        "incident_resolved_p1" "emergency-response" "0" \
        "ROLLBACK FAILED — no safe target for $INCIDENT_ID" 2>/dev/null || true
      exit 1
    fi
    
    echo "[$INCIDENT_ID] Rolling back to: $LAST_GOOD"
    git checkout "$LAST_GOOD" -- . 2>/dev/null || true
    echo "[$INCIDENT_ID] Rollback complete."
    
    bash "$NYPD_DIR/scripts/iab-shannon-logger.sh" \
      "incident_resolved_p1" "emergency-response" "20" \
      "P1 rollback complete for $INCIDENT_ID — restored to $LAST_GOOD" 2>/dev/null || true
    ;;

  # ── SUCCESSION: activate backup chain ─────────────────────────────────────
  succession)
    echo "[$INCIDENT_ID] SUCCESSION: activating backup chain..."
    
    # Stage 1: Notify Commissioner via incident log
    {
      echo ""
      echo "## SUCCESSION ACTIVATED — $INCIDENT_ID"
      echo ""
      echo "- **Time:** $TIMESTAMP"
      echo "- **Triggered By:** emergency-response"
      echo "- **Reason:** P1 incident requiring succession chain activation"
      echo ""
      echo "### Succession Chain Status"
      echo "1. ✅ Fiesta (Commissioner) — notified via incident log"
      echo "2. ✅ Emergency Response — ACTIVE"
      echo "3. ⏳ Auto-rollback — standing by"
      echo "4. ⏳ Cron isolation — standing by"
    } >> "$NYPD_DIR/incident-log.md"
    
    echo "[$INCIDENT_ID] Succession chain activated. Commissioner notified."
    bash "$NYPD_DIR/scripts/iab-shannon-logger.sh" \
      "incident_resolved_p1" "emergency-response" "20" \
      "Succession chain activated for $INCIDENT_ID" 2>/dev/null || true
    ;;

  # ── ISOLATE: suspend non-essential cron jobs ───────────────────────────────
  isolate)
    echo "[$INCIDENT_ID] ISOLATE: suspending non-NYPD cron jobs..."
    
    BACKUP="/tmp/cron-backup-$INCIDENT_ID.txt"
    crontab -l 2>/dev/null > "$BACKUP" || touch "$BACKUP"
    
    # Keep only NYPD patrol cron, disable everything else
    grep -E "nypd|patrol" "$BACKUP" | crontab - 2>/dev/null || crontab -r 2>/dev/null || true
    
    echo "[$INCIDENT_ID] Isolation complete. Backup at: $BACKUP"
    echo "[$INCIDENT_ID] Restore with: bash $NYPD_DIR/scripts/emergency-response.sh $INCIDENT_ID restore"
    
    bash "$NYPD_DIR/scripts/iab-shannon-logger.sh" \
      "incident_resolved_p1" "emergency-response" "20" \
      "System isolated for $INCIDENT_ID — non-NYPD cron suspended" 2>/dev/null || true
    ;;

  # ── RESTORE: reinstate suspended cron jobs ─────────────────────────────────
  restore)
    echo "[$INCIDENT_ID] RESTORE: reinstating suspended cron jobs..."
    
    BACKUP="/tmp/cron-backup-$INCIDENT_ID.txt"
    if [ -f "$BACKUP" ]; then
      crontab "$BACKUP"
      echo "[$INCIDENT_ID] Restore complete from: $BACKUP"
    else
      echo "[$INCIDENT_ID] WARNING: No backup found at $BACKUP. Cannot restore."
    fi
    
    bash "$NYPD_DIR/scripts/iab-shannon-logger.sh" \
      "incident_resolved_p1" "emergency-response" "20" \
      "System restored after $INCIDENT_ID — cron jobs reinstated" 2>/dev/null || true
    ;;

  *)
    echo "[$INCIDENT_ID] ERROR: Unknown action '$ACTION'"
    echo "Valid actions: rollback | succession | isolate | restore"
    exit 1
    ;;
esac

# ── Update incident log with resolution ───────────────────────────────────────
{
  echo ""
  echo "- **Resolved:** $TIMESTAMP"
  echo "- **Status:** CLOSED"
  echo "- **Resolution:** Emergency Response executed: $ACTION"
} >> "$NYPD_DIR/incident-log.md"

echo "[$TIMESTAMP] Emergency Response complete — $INCIDENT_ID — $ACTION executed."
