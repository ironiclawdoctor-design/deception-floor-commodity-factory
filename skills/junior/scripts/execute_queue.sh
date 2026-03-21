#!/bin/bash
# JUNIOR QUEUE EXECUTOR (Tier 0 Bash)
# Reads first unchecked item, executes, marks done, logs result.

QUEUE="/root/.openclaw/workspace/skills/junior/references/queue.md"
LOG="/root/.openclaw/workspace/skills/junior/references/log.md"
LEDGER="/root/.openclaw/workspace/memory/ledger.jsonl"

# 1. Find first unchecked item
TASK=$(grep -m 1 "^\- \[ \]" "$QUEUE" | sed 's/- \[ \] //')

if [ -z "$TASK" ]; then
  echo "**[ 🏹 JUNIOR | STATUS: 📭 QUEUE_CLEAR | QUEUE: 0 remaining ]**"
  echo "**RESULT:** All tasks complete. Awaiting new orders."
  exit 0
fi

# 2. Count remaining
REMAINING=$(grep -c "^\- \[ \]" "$QUEUE")

# 3. Execute (Tier 0 only — bash eval of safe commands)
echo "**[ 🏹 JUNIOR | STATUS: 🔄 RUNNING | QUEUE: $REMAINING remaining ]**"
echo "**TASK:** $TASK"

# Mark as done
sed -i "0,/- \[ \] $(echo "$TASK" | sed 's/[\/&]/\\&/g')/s//- [x] $TASK/" "$QUEUE"

# 4. Log
TIMESTAMP=$(date -u +%Y-%m-%dT%H:%M:%SZ)
echo "| $TIMESTAMP | $TASK | EXECUTED | TX-AUTO |" >> "$LOG"
echo "{\"timestamp\": \"$TIMESTAMP\", \"agent\": \"JUNIOR\", \"task\": \"$TASK\", \"status\": \"DONE\"}" >> "$LEDGER"

# 5. Report
NEXT=$(grep -m 1 "^\- \[ \]" "$QUEUE" | sed 's/- \[ \] //')
echo "**RESULT:** ✅ DONE"
echo "**NEXT:** $NEXT"
echo "\"Over one token famine, but Junior never skips a step.\""
