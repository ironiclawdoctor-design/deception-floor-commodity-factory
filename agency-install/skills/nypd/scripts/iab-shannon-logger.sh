#!/usr/bin/env bash
# IAB Shannon Logger — logs violations and successes to Shannon ledger
# Usage: bash iab-shannon-logger.sh <action> <agent> <amount> <reason>
# action: violation | patrol_success | investigation_complete | incident_resolved
# amount: positive = mint, negative = burn (use negative number for burns)
set -euo pipefail

LEDGER_DB="/root/.openclaw/workspace/ledger.db"
ACTION="${1:-unknown}"
AGENT="${2:-unknown}"
AMOUNT="${3:-0}"
REASON="${4:-No reason provided}"
TIMESTAMP=$(date +%s)
LOG_DIR="/root/.openclaw/workspace/skills/nypd/logs"

mkdir -p "$LOG_DIR"

# ── Ensure ledger schema exists ────────────────────────────────────────────────
sqlite3 "$LEDGER_DB" "
CREATE TABLE IF NOT EXISTS transactions (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  timestamp INTEGER NOT NULL,
  agent TEXT NOT NULL,
  amount REAL NOT NULL,
  description TEXT,
  source TEXT DEFAULT 'nypd-iab'
);
CREATE INDEX IF NOT EXISTS idx_transactions_agent ON transactions(agent);
CREATE INDEX IF NOT EXISTS idx_transactions_timestamp ON transactions(timestamp);
" 2>/dev/null

# ── Rate card enforcement ─────────────────────────────────────────────────────
# Override amount based on standard IAB rate card if action is known
case "$ACTION" in
  patrol_success)         AMOUNT="1"   ;;
  incident_resolved_p3)   AMOUNT="2"   ;;
  incident_resolved_p2)   AMOUNT="5"   ;;
  incident_resolved_p1)   AMOUNT="20"  ;;
  investigation_complete) AMOUNT="5"   ;;
  iab_violation_scope)    AMOUNT="-10" ;;
  iab_violation_budget)   AMOUNT="-5"  ;;
  iab_violation_autograph) AMOUNT="-2" ;;
  iab_violation_tool)     AMOUNT="-15" ;;
  iab_debt_spiral)        AMOUNT="-25" ;;
  # Custom amount passthrough for other action types
  *) : ;;
esac

# ── Write to ledger ───────────────────────────────────────────────────────────
sqlite3 "$LEDGER_DB" "
INSERT INTO transactions (timestamp, agent, amount, description, source)
VALUES ($TIMESTAMP, '$AGENT', $AMOUNT, '$REASON ($ACTION)', 'nypd-iab');
"

# ── Get updated balance ───────────────────────────────────────────────────────
BALANCE=$(sqlite3 "$LEDGER_DB" \
  "SELECT COALESCE(SUM(amount), 0) FROM transactions WHERE agent='$AGENT';" 2>/dev/null || echo "0")

# ── Log to IAB activity file ──────────────────────────────────────────────────
echo "$(date -u +%Y-%m-%dT%H:%M:%SZ)|$ACTION|$AGENT|$AMOUNT Sh|balance: ${BALANCE} Sh|$REASON" \
  >> "$LOG_DIR/iab-activity.log"

echo "[IAB] ✓ Logged: agent=$AGENT | action=$ACTION | delta=${AMOUNT} Sh | balance=${BALANCE} Sh"
echo "[IAB] Reason: $REASON"
