#!/bin/bash
# Wrapper for Universal Optimizer Agent

set -e

cd "$(dirname "$0")"
LOCK_FILE="/tmp/optimizer.lock"

# Prevent overlapping runs
if [ -f "$LOCK_FILE" ]; then
    echo "$(date -u +'%Y-%m-%dT%H:%M:%SZ') Optimizer already running, exiting" >> optimizer-cron.log
    exit 0
fi

touch "$LOCK_FILE"
trap 'rm -f "$LOCK_FILE"' EXIT

TIMESTAMP=$(date -u +"%Y-%m-%dT%H:%M:%SZ")
echo "[$TIMESTAMP] Starting optimizer..." >> optimizer-cron.log

# Run optimizer v1 (detection and minting)
python3 optimizer.py 2>&1 >> optimizer-cron.log

EXIT_CODE=$?
TIMESTAMP=$(date -u +"%Y-%m-%dT%H:%M:%SZ")

if [ $EXIT_CODE -eq 0 ]; then
    echo "[$TIMESTAMP] Optimizer completed successfully" >> optimizer-cron.log
else
    echo "[$TIMESTAMP] Optimizer failed with exit code $EXIT_CODE" >> optimizer-cron.log
fi

exit $EXIT_CODE