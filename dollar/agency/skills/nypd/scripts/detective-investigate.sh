#!/usr/bin/env bash
# NYPD Detective Forensic Investigation
# Usage: bash detective-investigate.sh INC-20260322-001
# Bash-first: uses only exec + read equivalents (no external APIs)
set -euo pipefail

CASE_ID="${1:-INC-UNKNOWN}"
NYPD_DIR="/root/.openclaw/workspace/skills/nypd"
EVIDENCE_DIR="$NYPD_DIR/cases/$CASE_ID"
LEDGER_DB="/root/.openclaw/workspace/ledger.db"
TIMESTAMP=$(date -u +"%Y-%m-%dT%H:%M:%SZ")

mkdir -p "$EVIDENCE_DIR"

echo "I am detective. I will help you."
echo ""
echo "=== DETECTIVE INVESTIGATION: $CASE_ID ===" | tee "$EVIDENCE_DIR/case-notes.md"
echo "Started: $TIMESTAMP" | tee -a "$EVIDENCE_DIR/case-notes.md"
echo "" | tee -a "$EVIDENCE_DIR/case-notes.md"

# ── Step 1: Patrol alert history ──────────────────────────────────────────────
echo "### PATROL ALERTS (last 50)" | tee -a "$EVIDENCE_DIR/case-notes.md"
tail -50 "$NYPD_DIR/logs/alerts.tsv" 2>/dev/null | tee -a "$EVIDENCE_DIR/case-notes.md" \
  || echo "(no alert log)" | tee -a "$EVIDENCE_DIR/case-notes.md"
echo "" | tee -a "$EVIDENCE_DIR/case-notes.md"

# ── Step 2: System journal ────────────────────────────────────────────────────
echo "### SYSTEM JOURNAL (last 100 lines, last 1 hour)" | tee -a "$EVIDENCE_DIR/case-notes.md"
journalctl --since "1 hour ago" --no-pager 2>/dev/null | tail -100 \
  | tee -a "$EVIDENCE_DIR/case-notes.md" \
  || echo "(journalctl unavailable)" | tee -a "$EVIDENCE_DIR/case-notes.md"
echo "" | tee -a "$EVIDENCE_DIR/case-notes.md"

# ── Step 3: Kernel messages ───────────────────────────────────────────────────
echo "### DMESG (last 30 lines)" | tee -a "$EVIDENCE_DIR/case-notes.md"
dmesg 2>/dev/null | tail -30 | tee "$EVIDENCE_DIR/dmesg.log" \
  | tee -a "$EVIDENCE_DIR/case-notes.md" \
  || echo "(dmesg unavailable)" | tee -a "$EVIDENCE_DIR/case-notes.md"
echo "" | tee -a "$EVIDENCE_DIR/case-notes.md"

# ── Step 4: Process forensics ─────────────────────────────────────────────────
echo "### TOP PROCESSES BY CPU" | tee -a "$EVIDENCE_DIR/case-notes.md"
ps aux --sort=-%cpu 2>/dev/null | head -20 | tee -a "$EVIDENCE_DIR/case-notes.md"
echo "" | tee -a "$EVIDENCE_DIR/case-notes.md"

echo "### TOP PROCESSES BY MEMORY" | tee -a "$EVIDENCE_DIR/case-notes.md"
ps aux --sort=-%mem 2>/dev/null | head -10 | tee -a "$EVIDENCE_DIR/case-notes.md"
echo "" | tee -a "$EVIDENCE_DIR/case-notes.md"

# ── Step 5: Network state ─────────────────────────────────────────────────────
echo "### LISTENING PORTS" | tee -a "$EVIDENCE_DIR/case-notes.md"
{ ss -tulnp 2>/dev/null || netstat -tulnp 2>/dev/null; } \
  | tee -a "$EVIDENCE_DIR/case-notes.md" \
  || echo "(network tools unavailable)" | tee -a "$EVIDENCE_DIR/case-notes.md"
echo "" | tee -a "$EVIDENCE_DIR/case-notes.md"

# ── Step 6: Shannon ledger forensics ──────────────────────────────────────────
echo "### SHANNON LEDGER — LAST 50 TRANSACTIONS" | tee -a "$EVIDENCE_DIR/case-notes.md"
if [ -f "$LEDGER_DB" ]; then
  sqlite3 "$LEDGER_DB" \
    "SELECT datetime(timestamp,'unixepoch'), agent, amount, description FROM transactions ORDER BY timestamp DESC LIMIT 50;" \
    2>/dev/null | tee "$EVIDENCE_DIR/ledger-trace.txt" | tee -a "$EVIDENCE_DIR/case-notes.md" \
    || echo "(ledger read error)" | tee -a "$EVIDENCE_DIR/case-notes.md"
  
  echo "" | tee -a "$EVIDENCE_DIR/case-notes.md"
  echo "### AGENT BALANCES" | tee -a "$EVIDENCE_DIR/case-notes.md"
  sqlite3 "$LEDGER_DB" \
    "SELECT agent, SUM(amount) as balance FROM transactions GROUP BY agent ORDER BY balance ASC;" \
    2>/dev/null | tee -a "$EVIDENCE_DIR/case-notes.md" \
    || true
else
  echo "(ledger.db not found — possible root cause RC-003)" | tee -a "$EVIDENCE_DIR/case-notes.md"
fi
echo "" | tee -a "$EVIDENCE_DIR/case-notes.md"

# ── Step 7: Recent file changes ───────────────────────────────────────────────
echo "### RECENTLY MODIFIED FILES (workspace, last 1hr)" | tee -a "$EVIDENCE_DIR/case-notes.md"
find /root/.openclaw/workspace -type f \( -name "*.md" -o -name "*.db" -o -name "*.sh" -o -name "*.json" \) \
  -newer /proc/1 -not -path "*/\.*" 2>/dev/null | head -30 \
  | tee -a "$EVIDENCE_DIR/case-notes.md" \
  || echo "(find unavailable)" | tee -a "$EVIDENCE_DIR/case-notes.md"
echo "" | tee -a "$EVIDENCE_DIR/case-notes.md"

# ── Step 8: Disk and memory state ─────────────────────────────────────────────
echo "### DISK STATE" | tee -a "$EVIDENCE_DIR/case-notes.md"
df -h 2>/dev/null | tee -a "$EVIDENCE_DIR/case-notes.md"
echo "" | tee -a "$EVIDENCE_DIR/case-notes.md"

echo "### MEMORY STATE" | tee -a "$EVIDENCE_DIR/case-notes.md"
free -h 2>/dev/null | tee -a "$EVIDENCE_DIR/case-notes.md"
echo "" | tee -a "$EVIDENCE_DIR/case-notes.md"

# ── Step 9: Root Cause Classification ────────────────────────────────────────
echo "### ROOT CAUSE CLASSIFICATION" | tee -a "$EVIDENCE_DIR/case-notes.md"
RC="RC-008 (Unknown)"
# Heuristic classification
if grep -q "gateway_down\|502\|503\|unreachable" "$NYPD_DIR/logs/alerts.tsv" 2>/dev/null; then
  RC="RC-002 (Service Failure)"
fi
if grep -q "ledger_missing\|ledger_stale\|corruption" "$NYPD_DIR/logs/alerts.tsv" 2>/dev/null; then
  RC="RC-003 (Data Corruption / Staleness)"
fi
if grep -q "disk_high\|mem_low" "$NYPD_DIR/logs/alerts.tsv" 2>/dev/null; then
  RC="RC-001 (Resource Exhaustion)"
fi
if grep -q "cron_missing" "$NYPD_DIR/logs/alerts.tsv" 2>/dev/null; then
  RC="RC-005 (Cron Failure)"
fi

echo "Determined Root Cause: $RC" | tee -a "$EVIDENCE_DIR/case-notes.md"
echo "" | tee -a "$EVIDENCE_DIR/case-notes.md"
echo "=== INVESTIGATION COMPLETE: $CASE_ID ===" | tee -a "$EVIDENCE_DIR/case-notes.md"
echo "Evidence: $EVIDENCE_DIR/case-notes.md"

# Mint Shannon for completed investigation
bash "$NYPD_DIR/scripts/iab-shannon-logger.sh" \
  "investigation_complete" "detective" "5" \
  "P2 investigation complete for $CASE_ID — root cause: $RC" 2>/dev/null || true
