#!/bin/bash
# Wrapper for failure‑refinement copier agent

set -e

cd "$(dirname "$0")"

LOG_FILE="copier.log"
TIMESTAMP=$(date -u +"%Y-%m-%dT%H:%M:%SZ")

echo "[$TIMESTAMP] Starting copier agent..." | tee -a "$LOG_FILE"

# Run the Python agent
python3 copier-agent.py 2>&1 | tee -a "$LOG_FILE"

EXIT_CODE=${PIPESTATUS[0]}
TIMESTAMP=$(date -u +"%Y-%m-%dT%H:%M:%SZ")

if [ $EXIT_CODE -eq 0 ]; then
    echo "[$TIMESTAMP] Copier completed successfully" | tee -a "$LOG_FILE"
else
    echo "[$TIMESTAMP] Copier failed with exit code $EXIT_CODE" | tee -a "$LOG_FILE"
fi

exit $EXIT_CODE