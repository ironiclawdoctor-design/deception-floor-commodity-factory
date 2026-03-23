#!/bin/bash

##############################################################################
# Compaction Health Monitor
# 
# Monitors system compaction metrics and logs any issues.
# Useful for checking memory compaction, disk compaction, and data integrity.
#
# Usage: bash compaction-monitor.sh
##############################################################################

set -e

MONITOR_DATE=$(date -u '+%Y-%m-%d %H:%M:%S')
LOG_DIR="/root/.openclaw/workspace/logs"
LOG_FILE="${LOG_DIR}/compaction-monitor.log"

# Ensure log directory exists
mkdir -p "$LOG_DIR"

# Initialize report
{
    echo "========================================"
    echo "Compaction Health Monitor Report"
    echo "Timestamp: $MONITOR_DATE (UTC)"
    echo "========================================"
    echo ""
} | tee -a "$LOG_FILE"

# Function to log messages
log_message() {
    local level=$1
    local message=$2
    echo "[$level] $message" | tee -a "$LOG_FILE"
}

# Function to check memory compaction
check_memory_compaction() {
    log_message "INFO" "Checking memory compaction..."
    
    if [ -f /proc/sys/vm/compact_memory ]; then
        local compact_status=$(cat /proc/sys/vm/compact_memory 2>/dev/null || echo "unknown")
        log_message "INFO" "Memory compaction interface: $compact_status"
    else
        log_message "WARN" "Memory compaction interface not available"
    fi
    
    # Check available memory
    local mem_available=$(free -h | grep Mem | awk '{print $7}')
    log_message "INFO" "Available memory: $mem_available"
}

# Function to check disk compaction (defrag status for ext4/btrfs)
check_disk_compaction() {
    log_message "INFO" "Checking disk compaction status..."
    
    # Get root filesystem type
    local fs_type=$(df / | tail -1 | awk '{print $1}')
    log_message "INFO" "Root filesystem: $fs_type"
    
    # Check if btrfs (has native defrag)
    if [[ "$fs_type" == *"btrfs"* ]]; then
        log_message "INFO" "Filesystem is btrfs (supports native defragmentation)"
    elif [[ "$fs_type" == *"ext4"* ]]; then
        log_message "INFO" "Filesystem is ext4 (defragmentation available via e4defrag)"
    else
        log_message "INFO" "Filesystem type: $fs_type (check compatibility separately)"
    fi
    
    # Check inode usage
    local inode_usage=$(df -i / | tail -1 | awk '{print $5}' | sed 's/%//')
    log_message "INFO" "Inode usage: ${inode_usage}%"
    
    if [ "$inode_usage" -gt 90 ]; then
        log_message "ERROR" "Inode usage critically high (${inode_usage}%) - compaction may be needed"
    elif [ "$inode_usage" -gt 75 ]; then
        log_message "WARN" "Inode usage elevated (${inode_usage}%) - monitor for compaction needs"
    fi
}

# Function to check disk space fragmentation
check_disk_fragmentation() {
    log_message "INFO" "Checking disk fragmentation..."
    
    local disk_usage=$(df / | tail -1 | awk '{print $5}' | sed 's/%//')
    log_message "INFO" "Disk usage: ${disk_usage}%"
    
    if [ "$disk_usage" -gt 95 ]; then
        log_message "ERROR" "Disk critically full (${disk_usage}%) - fragmentation risk high"
    elif [ "$disk_usage" -gt 85 ]; then
        log_message "WARN" "Disk usage high (${disk_usage}%) - consider compaction/cleanup"
    fi
}

# Function to check database/RocksDB compaction (if applicable)
check_rocksdb_compaction() {
    log_message "INFO" "Checking RocksDB/database compaction..."
    
    # Look for common RocksDB directories
    local rocksdb_paths=(
        "/root/.openclaw/data/rocksdb"
        "/root/.openclaw/workspace/.rocksdb"
        "/tmp/rocksdb*"
    )
    
    local found_db=0
    for path in "${rocksdb_paths[@]}"; do
        if [ -d "$path" ] 2>/dev/null; then
            log_message "INFO" "Found RocksDB instance: $path"
            found_db=1
        fi
    done
    
    if [ $found_db -eq 0 ]; then
        log_message "INFO" "No RocksDB instances detected"
    fi
}

# Function to check container/overlay filesystem (if in container)
check_overlay_fs() {
    log_message "INFO" "Checking overlay filesystem (containers)..."
    
    if [ -d /var/lib/docker ]; then
        log_message "INFO" "Docker detected - checking overlay filesystem"
        local overlay_usage=$(df /var/lib/docker 2>/dev/null | tail -1 | awk '{print $5}' | sed 's/%//' || echo "N/A")
        log_message "INFO" "Docker filesystem usage: ${overlay_usage}%"
    else
        log_message "INFO" "No Docker overlay filesystem detected"
    fi
}

# Main execution
{
    echo ""
    check_memory_compaction
    echo ""
    check_disk_compaction
    echo ""
    check_disk_fragmentation
    echo ""
    check_rocksdb_compaction
    echo ""
    check_overlay_fs
    echo ""
    echo "========================================"
    echo "Monitor completed at $(date -u '+%Y-%m-%d %H:%M:%S')"
    echo "========================================"
} | tee -a "$LOG_FILE"

# Summary and recommendations
{
    echo ""
    echo "📋 RECOMMENDATIONS:"
    echo ""
    echo "If memory compaction issues detected:"
    echo "  - Increase available RAM or reduce active workload"
    echo "  - Check for memory leaks: ps aux --sort=-%mem | head"
    echo ""
    echo "If disk compaction issues detected:"
    echo "  - For ext4: sudo e4defrag -c -r /"
    echo "  - For btrfs: sudo btrfs filesystem defragment /"
    echo "  - Free up space: remove old logs, caches, or unused containers"
    echo ""
    echo "If inode exhaustion detected:"
    echo "  - Reduce number of small files"
    echo "  - Clean up temporary directories"
    echo "  - Consider filesystem resize/reformat"
    echo ""
    echo "Monitor logs at: $LOG_FILE"
    echo ""
} | tee -a "$LOG_FILE"

exit 0
