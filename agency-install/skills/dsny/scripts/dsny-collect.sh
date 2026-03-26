#!/usr/bin/env bash
# dsny-collect.sh — DSNY Collection Agent daily sweep
# DSNY Department of Sanitation | Fiesta Agency
# Usage: bash dsny-collect.sh [--target TARGET] [--dry-run]
# Targets: tmp_files | stale_logs | dead_sessions | expired_creds | debug_artifacts
# Add --dry-run to preview without deleting

WS="${WORKSPACE:-$HOME/.openclaw/workspace}"
LOG="$WS/dsny/logs/sanitization.log"
SHANNON_LOG="$WS/dsny/logs/shannon.log"
DRY_RUN=false
TARGET="all"
ITEMS_COLLECTED=0
BYTES_FREED=0
SHANNON_EARNED=0
LARGE_PURGE_THRESHOLD_FILES=10
LARGE_PURGE_THRESHOLD_MB=100

mkdir -p "$WS/dsny/logs" "$WS/archive/experiments" "$WS/backup/configs" "$WS/credentials"

log() {
  local msg="[$(date -u '+%Y-%m-%d %H:%M UTC')] $*"
  echo "$msg"
  echo "$msg" >> "$LOG"
}

shannon() {
  local delta=$1 agent=$2 reason=$3
  local entry="[$(date -u '+%Y-%m-%d %H:%M UTC')] ${delta} Shannon | ${agent} | ${reason}"
  echo "$entry" >> "$SHANNON_LOG"
  SHANNON_EARNED=$((SHANNON_EARNED + delta))
}

# Parse args
while [[ $# -gt 0 ]]; do
  case $1 in
    --target) TARGET="$2"; shift 2 ;;
    --dry-run) DRY_RUN=true; shift ;;
    *) shift ;;
  esac
done

echo "🗑️  DSNY Collection Agent — $(date -u '+%Y-%m-%d %H:%M UTC')"
echo "   Target: $TARGET | Dry-run: $DRY_RUN"
echo "─────────────────────────────────────────"

# Helper: check if purge requires commissioner approval
needs_approval() {
  local count=$1 size_mb=$2
  if [ "$count" -gt "$LARGE_PURGE_THRESHOLD_FILES" ] || [ "$size_mb" -gt "$LARGE_PURGE_THRESHOLD_MB" ]; then
    return 0
  fi
  return 1
}

collect_tmp_files() {
  echo "📦 Scanning for stale tmp files..."
  local files
  files=$(find /tmp "$WS" -name "*.tmp" -mtime +1 2>/dev/null)
  local count
  count=$(echo "$files" | grep -c . 2>/dev/null || echo 0)
  [ -z "$files" ] && count=0
  echo "   Found: $count files"
  if [ "$count" -gt 0 ]; then
    if needs_approval "$count" 0; then
      log "PURGE-PENDING | collection-agent | $count tmp files | AWAITING COMMISSIONER APPROVAL"
      echo "⚠️  $count files exceeds threshold — Commissioner approval required. Logged to sanitization.log."
      return
    fi
    if [ "$DRY_RUN" = false ]; then
      echo "$files" | xargs rm -f 2>/dev/null
      log "COLLECT | collection-agent | $count *.tmp files removed | +5 Shannon"
      shannon 5 "collection-agent" "daily sweep: $count tmp files collected"
    else
      log "DRY-RUN | collection-agent | would remove $count *.tmp files"
    fi
    ITEMS_COLLECTED=$((ITEMS_COLLECTED + count))
  fi
}

collect_stale_logs() {
  echo "📦 Scanning for stale logs (>7 days)..."
  local files
  files=$(find "$WS" -name "*.log" -not -path "*/dsny/logs/*" -not -path "*/.git/*" -mtime +7 2>/dev/null)
  local count
  count=$(echo "$files" | grep -c . 2>/dev/null || echo 0)
  [ -z "$files" ] && count=0
  echo "   Found: $count files"
  if [ "$count" -gt 0 ]; then
    if needs_approval "$count" 0; then
      log "PURGE-PENDING | collection-agent | $count stale logs | AWAITING COMMISSIONER APPROVAL"
      echo "⚠️  Commissioner approval required. Logged."
      return
    fi
    if [ "$DRY_RUN" = false ]; then
      # Archive insight extraction before delete
      echo "$files" | while read -r f; do
        grep -E "ERROR|WARNING|CRITICAL" "$f" 2>/dev/null >> "$WS/archive/log-insights.md" || true
      done
      echo "$files" | xargs rm -f 2>/dev/null
      log "COLLECT | collection-agent | $count stale logs archived+removed | +5 Shannon"
      shannon 5 "collection-agent" "stale log sweep: $count logs recycled"
    fi
    ITEMS_COLLECTED=$((ITEMS_COLLECTED + count))
  fi
}

collect_debug_artifacts() {
  echo "📦 Scanning for debug artifacts..."
  local files
  files=$(find "$WS" \( -name "__pycache__" -o -name "*.pyc" -o -name ".DS_Store" -o -name "*.swp" \) \
    -not -path "*/.git/*" 2>/dev/null)
  local count
  count=$(echo "$files" | grep -c . 2>/dev/null || echo 0)
  [ -z "$files" ] && count=0
  echo "   Found: $count artifacts"
  if [ "$count" -gt 0 ]; then
    if [ "$DRY_RUN" = false ]; then
      echo "$files" | xargs rm -rf 2>/dev/null
      log "COLLECT | collection-agent | $count debug artifacts removed | +5 Shannon"
      shannon 5 "collection-agent" "debug artifact sweep: $count items removed"
    else
      log "DRY-RUN | collection-agent | would remove $count debug artifacts"
    fi
    ITEMS_COLLECTED=$((ITEMS_COLLECTED + count))
  fi
}

# Run targets
case "$TARGET" in
  tmp_files)       collect_tmp_files ;;
  stale_logs)      collect_stale_logs ;;
  debug_artifacts) collect_debug_artifacts ;;
  all)
    collect_tmp_files
    collect_stale_logs
    collect_debug_artifacts
    ;;
  *)
    echo "Unknown target: $TARGET. Use: tmp_files|stale_logs|debug_artifacts|all"
    exit 1
    ;;
esac

echo "─────────────────────────────────────────"
echo "✅ Collection complete"
echo "   Items collected: $ITEMS_COLLECTED"
echo "   Shannon earned:  $SHANNON_EARNED"
echo ""
[ "$DRY_RUN" = true ] && echo "   (DRY RUN — no files deleted)"
