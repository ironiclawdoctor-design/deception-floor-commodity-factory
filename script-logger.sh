#!/bin/bash
# Standardized script logger for agency compliance tracking
# Source this file in your scripts: source /root/.openclaw/workspace/script-logger.sh

SCRIPT_LOG_DIR="/root/.openclaw/workspace/logs/script-executions"
mkdir -p "$SCRIPT_LOG_DIR"

# Default log file (JSONL format)
DEFAULT_LOG_FILE="$SCRIPT_LOG_DIR/script-log.jsonl"

# Function: log_script_start
# Logs when a script starts execution
log_script_start() {
    local script_name="$1"
    local script_path="$2"
    local args="$3"
    local timestamp=$(date -u +"%Y-%m-%dT%H:%M:%SZ")
    local log_entry=$(jq -n \
        --arg ts "$timestamp" \
        --arg name "$script_name" \
        --arg path "$script_path" \
        --arg args "$args" \
        --arg event "start" \
        --arg pid "$$" \
        '{
            timestamp: $ts,
            script_name: $name,
            script_path: $path,
            arguments: $args,
            event: $event,
            pid: $pid,
            status: "running"
        }')
    echo "$log_entry" >> "$DEFAULT_LOG_FILE"
}

# Function: log_script_success
# Logs when a script completes successfully
log_script_success() {
    local script_name="$1"
    local output="$2"
    local timestamp=$(date -u +"%Y-%m-%dT%H:%M:%SZ")
    local log_entry=$(jq -n \
        --arg ts "$timestamp" \
        --arg name "$script_name" \
        --arg event "success" \
        --arg pid "$$" \
        --arg output "$output" \
        '{
            timestamp: $ts,
            script_name: $name,
            event: $event,
            pid: $pid,
            status: "completed",
            exit_code: 0,
            output: $output
        }')
    echo "$log_entry" >> "$DEFAULT_LOG_FILE"
}

# Function: log_script_failure
# Logs when a script fails
log_script_failure() {
    local script_name="$1"
    local exit_code="$2"
    local error="$3"
    local timestamp=$(date -u +"%Y-%m-%dT%H:%M:%SZ")
    local log_entry=$(jq -n \
        --arg ts "$timestamp" \
        --arg name "$script_name" \
        --arg event "failure" \
        --arg pid "$$" \
        --arg exit_code "$exit_code" \
        --arg error "$error" \
        '{
            timestamp: $ts,
            script_name: $name,
            event: $event,
            pid: $pid,
            status: "failed",
            exit_code: ($exit_code | tonumber),
            error: $error
        }')
    echo "$log_entry" >> "$DEFAULT_LOG_FILE"
}

# Function: log_script_step
# Logs intermediate steps within a script
log_script_step() {
    local script_name="$1"
    local step="$2"
    local details="$3"
    local timestamp=$(date -u +"%Y-%m-%dT%H:%M:%SZ")
    local log_entry=$(jq -n \
        --arg ts "$timestamp" \
        --arg name "$script_name" \
        --arg event "step" \
        --arg pid "$$" \
        --arg step "$step" \
        --arg details "$details" \
        '{
            timestamp: $ts,
            script_name: $name,
            event: $event,
            pid: $pid,
            step: $step,
            details: $details
        }')
    echo "$log_entry" >> "$DEFAULT_LOG_FILE"
}

# Function: check_script_compliance
# Checks if a script has been run (for Fiesta to verify)
check_script_compliance() {
    local script_name="$1"
    local min_timestamp="${2:-0}"  # Unix timestamp, defaults to beginning of time
    
    if [ ! -f "$DEFAULT_LOG_FILE" ]; then
        echo "No log file found: $DEFAULT_LOG_FILE"
        return 1
    fi
    
    # Count successful executions
    local success_count=$(grep -c "\"script_name\":\"$script_name\".*\"event\":\"success\"" "$DEFAULT_LOG_FILE" 2>/dev/null || echo "0")
    
    # Get last execution time
    local last_exec=$(grep "\"script_name\":\"$script_name\"" "$DEFAULT_LOG_FILE" | tail -1 | jq -r '.timestamp' 2>/dev/null || echo "never")
    
    echo "Script: $script_name"
    echo "Success count: $success_count"
    echo "Last executed: $last_exec"
    
    if [ "$success_count" -gt 0 ]; then
        return 0  # Script has been run successfully
    else
        return 1  # Script has never run successfully
    fi
}

# Function: get_script_logs
# Retrieves logs for a specific script (for Fiesta to read)
get_script_logs() {
    local script_name="$1"
    local limit="${2:-10}"
    
    if [ ! -f "$DEFAULT_LOG_FILE" ]; then
        echo "No log file found"
        return
    fi
    
    # Use jq to filter and format logs
    grep "\"script_name\":\"$script_name\"" "$DEFAULT_LOG_FILE" 2>/dev/null | tail -"$limit" | while read -r line; do
        echo "$line" | jq -r '[.timestamp, .event, .status, .step // "-"] | @tsv' 2>/dev/null || echo "$line"
    done
}

# Export functions for use in other scripts
export -f log_script_start
export -f log_script_success
export -f log_script_failure
export -f log_script_step
export -f check_script_compliance
export -f get_script_logs

echo "Script logger loaded. Log file: $DEFAULT_LOG_FILE"
echo "Usage in scripts:"
echo "  source /root/.openclaw/workspace/script-logger.sh"
echo "  log_script_start \"myscript\" \"\$0\" \"\$*\""
echo "  # ... script logic ..."
echo "  log_script_success \"myscript\" \"Output summary\""
echo "  # OR on error:"
echo "  log_script_failure \"myscript\" \"\$?\" \"Error message\""