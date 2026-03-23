#!/bin/bash
# sorter-unattended.sh - Allocation while the Shogun oversleeps
# Based on the Fearclaw/Mendez lineage.

LOG="/root/.openclaw/workspace/logs/sorter-unattended.log"
MANIFEST="/root/.openclaw/workspace/bedrock-results/manifest.24tb.json"

echo "🛡️ UNATTENDED ALLOCATION STARTING: $(date)" >> $LOG

# Execute the 24TB Scan bedrock logic
# Using 0-index tier discipline (bash bedrock)
/root/.openclaw/workspace/scripts/BEDROCK_SORTER_vFINAL.sh "/root/.openclaw/workspace/test-source" "/root/.openclaw/workspace/bedrock-results" >> $LOG 2>&1

echo "📦 Loop Complete: Resources positioned." >> $LOG
