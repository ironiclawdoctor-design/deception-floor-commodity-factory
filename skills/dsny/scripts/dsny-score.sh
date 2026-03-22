#!/usr/bin/env bash
# dsny-score.sh — Compute workspace cleanliness score
# DSNY Department of Sanitation | Fiesta Agency
# Usage: bash dsny-score.sh [workspace_path]
# Output: score 0-100 and criterion breakdown

WS="${1:-$HOME/.openclaw/workspace}"
SCORE=0

echo "🧹 DSNY Cleanliness Audit"
echo "  Workspace: $WS"
echo "  Date: $(date -u '+%Y-%m-%d %H:%M UTC')"
echo "───────────────────────────────────────"

# Criterion 1: No stale tmp files (>24h old)
TMP_COUNT=$(find /tmp "$WS" -name "*.tmp" -mtime +1 2>/dev/null | wc -l | tr -d ' ')
if [ "$TMP_COUNT" -eq 0 ]; then
  SCORE=$((SCORE+20))
  echo "✅ C1: No stale tmp files (+20)"
else
  echo "❌ C1: $TMP_COUNT stale tmp files — 0pts"
fi

# Criterion 2: No orphaned logs (>7 days, outside dsny logs dir)
LOG_COUNT=$(find "$WS" -name "*.log" \
  -not -path "*/dsny/logs/*" \
  -not -path "*/.git/*" \
  -mtime +7 2>/dev/null | wc -l | tr -d ' ')
if [ "$LOG_COUNT" -eq 0 ]; then
  SCORE=$((SCORE+20))
  echo "✅ C2: No orphaned logs (+20)"
else
  echo "❌ C2: $LOG_COUNT stale log files — 0pts"
fi

# Criterion 3: No debug artifacts
DBG_COUNT=$(find "$WS" \
  \( -name "__pycache__" -o -name "*.pyc" -o -name ".DS_Store" -o -name "*.swp" -o -name "*.pyo" \) \
  -not -path "*/.git/*" 2>/dev/null | wc -l | tr -d ' ')
if [ "$DBG_COUNT" -eq 0 ]; then
  SCORE=$((SCORE+20))
  echo "✅ C3: No debug artifacts (+20)"
else
  echo "❌ C3: $DBG_COUNT debug artifacts — 0pts"
fi

# Criterion 4: No duplicate files (by md5, excluding .git)
DUP_COUNT=$(find "$WS" -type f -not -path "*/.git/*" 2>/dev/null \
  | xargs md5sum 2>/dev/null \
  | sort \
  | uniq -d -w32 \
  | wc -l | tr -d ' ')
if [ "$DUP_COUNT" -eq 0 ]; then
  SCORE=$((SCORE+20))
  echo "✅ C4: No duplicate files (+20)"
else
  echo "❌ C4: $DUP_COUNT duplicate file sets — 0pts"
fi

# Criterion 5: Archive structure present and valid
if [ -d "$WS/archive/experiments" ] && [ -d "$WS/backup/configs" ] && [ -d "$WS/credentials" ]; then
  SCORE=$((SCORE+20))
  echo "✅ C5: Archive/backup structure present (+20)"
else
  MISSING=""
  [ ! -d "$WS/archive/experiments" ] && MISSING="$MISSING archive/experiments"
  [ ! -d "$WS/backup/configs" ]      && MISSING="$MISSING backup/configs"
  [ ! -d "$WS/credentials" ]         && MISSING="$MISSING credentials/"
  echo "❌ C5: Missing directories:$MISSING — 0pts"
fi

echo "───────────────────────────────────────"
echo "🏆 DSNY Cleanliness Score: $SCORE / 100"

# Shannon bonus announcement
if [ "$SCORE" -eq 100 ]; then
  echo "💎 PERFECT SCORE — +50 Shannon bonus!"
elif [ "$SCORE" -ge 80 ]; then
  echo "✨ Good standing — standard Shannon payroll applies"
elif [ "$SCORE" -ge 60 ]; then
  echo "⚠️  Below target — Commissioner notified"
else
  echo "🚨 CRITICAL — Emergency sweep required. Commissioner escalation triggered."
fi

exit 0
