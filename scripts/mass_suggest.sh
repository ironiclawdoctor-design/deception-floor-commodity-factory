#!/bin/bash
# mass_suggest.sh - Unified Agency-Wide Suggestion Aggregator
# Combines daemon logs, observed parentheticals, and emulated soul needs.

SUGGESTIONS_JSON="/root/.openclaw/workspace/suggestions/improvements.json"
SUGGESTIONS_JSONL="/root/.openclaw/workspace/suggestions/improvements.jsonl"
OUTPUT_MD="/root/.openclaw/workspace/status/MASS_SUGGEST_REPORT.md"

echo "# 🌊 MASS SUGGEST REPORT — $(date -u)" > $OUTPUT_MD
echo "## Current Agency State: UNIFIED EMULATION" >> $OUTPUT_MD
echo "" >> $OUTPUT_MD

# 1. Aggregate from Proactive Supervisor (Formal Anomaly Data)
echo "### 🧭 System Infrastructure (Supervisor)" >> $OUTPUT_MD
if [ -f "$SUGGESTIONS_JSON" ]; then
    grep -oP '"message":\s*"\K[^"]+' $SUGGESTIONS_JSON | sed 's/^/- /' >> $OUTPUT_MD
else
    echo "- No formal system anomalies pending." >> $OUTPUT_MD
fi
echo "" >> $OUTPUT_MD

# 2. Aggregate from Observed Fragments (The Parentheticals)
echo "### 🔍 Observed Bedrock Improvements (Found in Parentheses)" >> $OUTPUT_MD
if [ -f "$SUGGESTIONS_JSONL" ]; then
    grep -oP '"message":\s*"Observed:\s*\K[^"]+' $SUGGESTIONS_JSONL | sort | uniq | sed 's/^/- /' >> $OUTPUT_MD
else
    echo "- No parenthetical observations cached." >> $OUTPUT_MD
fi
echo "" >> $OUTPUT_MD

# 3. Aggregate from Emulated Soul Needs (Economic Flow)
echo "### 💰 Departmental Liquidity Status (Emulated Souls)" >> $OUTPUT_MD
sqlite3 /root/.openclaw/workspace/entropy_ledger.db "SELECT agent_id, balance FROM agents WHERE balance < 100;" | while read -r line; do
    echo "- \$${line/|/ is LOW on Shannon: } units." >> $OUTPUT_MD
done

echo "" >> $OUTPUT_MD
echo "---" >> $OUTPUT_MD
echo "**Actionability:** Use /shanapp or /execute_mass to resolve." >> $OUTPUT_MD

# Success Trigger
cat $OUTPUT_MD
