#!/bin/bash
# cleanup-mount-zombies.sh
# Cleans stale Docker BuildKit mount zombies from the mount table
# These accumulate from failed/interrupted docker builds in LXC containers
# Run daily via cron or on-demand

set -euo pipefail

LOGFILE="/var/log/mount-zombie-cleanup.log"
TIMESTAMP=$(date -u '+%Y-%m-%d %H:%M:%S UTC')

echo "[$TIMESTAMP] Mount zombie cleanup starting" >> "$LOGFILE"

# Count before
BEFORE=$(grep -c buildkit-mount /proc/mounts 2>/dev/null || echo 0)

if [ "$BEFORE" -eq 0 ]; then
    echo "[$TIMESTAMP] No buildkit mount zombies found. Clean." >> "$LOGFILE"
    exit 0
fi

echo "[$TIMESTAMP] Found $BEFORE stale buildkit mounts. Cleaning..." >> "$LOGFILE"

CLEANED=0
FAILED=0

for mp in $(grep buildkit-mount /proc/mounts | awk '{print $2}'); do
    if umount "$mp" 2>/dev/null; then
        rmdir "$mp" 2>/dev/null || true
        CLEANED=$((CLEANED + 1))
    else
        FAILED=$((FAILED + 1))
        echo "[$TIMESTAMP] FAILED to unmount: $mp" >> "$LOGFILE"
    fi
done

# Also prune docker builder cache
docker builder prune -af >> "$LOGFILE" 2>&1 || true

# Count after
AFTER=$(grep -c buildkit-mount /proc/mounts 2>/dev/null || echo 0)

echo "[$TIMESTAMP] Cleanup complete. Unmounted: $CLEANED, Failed: $FAILED, Remaining: $AFTER" >> "$LOGFILE"
echo "[$TIMESTAMP] Total mount count: $(wc -l < /proc/self/mountinfo)" >> "$LOGFILE"
