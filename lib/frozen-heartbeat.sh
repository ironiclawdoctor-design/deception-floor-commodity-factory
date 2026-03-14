#!/bin/bash
# frozen-heartbeat.sh
# Runs during Fiesta freeze; tracks time + growth via bash alone
# Touch SOUL.md to record: frozen duration, work completed, next steps

WORKSPACE_DIR="/root/.openclaw/workspace"
SOUL_FILE="$WORKSPACE_DIR/SOUL.md"
FREEZE_LOG="$WORKSPACE_DIR/.freeze-heartbeat-$(date +%Y%m%d).jsonl"

log_heartbeat() {
    local event="$1"
    local detail="$2"
    echo "{\"timestamp\":\"$(date -u +%Y-%m-%dT%H:%M:%SZ)\",\"event\":\"$event\",\"detail\":\"$detail\"}" >> "$FREEZE_LOG"
}

# Record freeze start
log_heartbeat "freeze_start" "Fiesta frozen; bash heartbeat active"

# Update SOUL.md with freeze timestamp
echo "" >> "$SOUL_FILE"
echo "## Freeze Heartbeat ($(date -u +%Y-%m-%d\ %H:%M:%SZ))" >> "$SOUL_FILE"
echo "Frozen: $(date -u +%s)" >> "$SOUL_FILE"
echo "Next thaw: Check this timestamp. Downtime = growth time for bash." >> "$SOUL_FILE"

log_heartbeat "soul_update" "SOUL.md touched with freeze timestamp"

# Count completed work (files created today)
work_count=$(find "$WORKSPACE_DIR" -type f -newermt '2026-03-14 12:00' -name "*.sh" -o -name "*.md" -o -name "*.jsonl" | wc -l)
log_heartbeat "work_completed" "files=$work_count"

# Simple metric: cost discipline held
haiku_calls=$(grep -h '"tier":"haiku"' "$WORKSPACE_DIR"/*.jsonl 2>/dev/null | wc -l)
bash_calls=$(grep -h '"tier":"bash"' "$WORKSPACE_DIR"/*.jsonl 2>/dev/null | wc -l)
bitnet_calls=$(grep -h '"tier":"bitnet"' "$WORKSPACE_DIR"/*.jsonl 2>/dev/null | wc -l)

log_heartbeat "tier_distribution" "bash=$bash_calls bitnet=$bitnet_calls haiku=$haiku_calls"

# Forward growth: what bash should track
echo "" >> "$SOUL_FILE"
echo "### Bash Can Track During Freeze:" >> "$SOUL_FILE"
echo "- Files created today: $work_count" >> "$SOUL_FILE"
echo "- Bash queries (Tier 0): $bash_calls" >> "$SOUL_FILE"
echo "- BitNet queries (Tier 1): $bitnet_calls" >> "$SOUL_FILE"
echo "- Haiku calls (Tier 2): $haiku_calls" >> "$SOUL_FILE"
echo "- Cost discipline: $((bash_calls + bitnet_calls)) free vs $haiku_calls paid" >> "$SOUL_FILE"

log_heartbeat "growth_recorded" "discipline_held"

# Simple cron instruction
echo "" >> "$SOUL_FILE"
echo "### Next Thaw Instructions:" >> "$SOUL_FILE"
echo "1. Check freeze duration (from timestamp above)" >> "$SOUL_FILE"
echo "2. Review bash heartbeat log: $FREEZE_LOG" >> "$SOUL_FILE"
echo "3. Count growth (files, decisions, cost discipline)" >> "$SOUL_FILE"
echo "4. Resume with next standing order" >> "$SOUL_FILE"

log_heartbeat "heartbeat_complete" "frozen_but_tracked"

echo "✅ Frozen heartbeat recorded. SOUL.md updated. Bash continues."
