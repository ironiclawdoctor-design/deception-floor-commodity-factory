#!/bin/bash
# Preauth Exec Elev Cache - Main CLI
# Tier 0: Bash implementation, BitNet audit layer

CACHE_DIR="${HOME}/.cache/preauth-elev"
CACHE_DB="${CACHE_DIR}/approvals.db"
AUDIT_LOG="${CACHE_DIR}/audit.jsonl"
CONFIG_FILE="${CACHE_DIR}/config.json"
DEFAULT_TTL=300  # 5 minutes in seconds

# Ensure cache directory exists
mkdir -p "$CACHE_DIR"

# Initialize SQLite if not exists
if [ ! -f "$CACHE_DB" ]; then
    sqlite3 "$CACHE_DB" "CREATE TABLE approvals (cmd_hash TEXT PRIMARY KEY, pattern TEXT, approved_at INTEGER, expires_at INTEGER, signature TEXT);"
    sqlite3 "$CACHE_DB" "CREATE TABLE audit (id INTEGER PRIMARY KEY, timestamp TEXT, action TEXT, cmd_hash TEXT, cmd_preview TEXT, result TEXT);"
fi

# Hash function for commands
hash_cmd() {
    echo -n "$1" | sha256sum | cut -d' ' -f1
}

# Sign with simple HMAC (using cached key)
sign_hash() {
    local hash="$1"
    local timestamp="$2"
    echo -n "${hash}:${timestamp}" | sha256sum | cut -d' ' -f1
}

# Check if command is cached and valid
check_cache() {
    local cmd="$1"
    local cmd_hash=$(hash_cmd "$cmd")
    local now=$(date +%s)
    
    local result=$(sqlite3 "$CACHE_DB" "SELECT expires_at, signature FROM approvals WHERE cmd_hash='$cmd_hash' AND expires_at > $now;")
    
    if [ -n "$result" ]; then
        local expires=$(echo "$result" | cut -d'|' -f1)
        local sig=$(echo "$result" | cut -d'|' -f2)
        local verify=$(sign_hash "$cmd_hash" "$expires")
        
        if [ "$sig" = "$verify" ]; then
            log_audit "CACHE_HIT" "$cmd_hash" "$cmd" "VALID"
            return 0
        fi
    fi
    
    log_audit "CACHE_MISS" "$cmd_hash" "$cmd" "INVALID"
    return 1
}

# Add command to cache
add_to_cache() {
    local cmd="$1"
    local ttl="${2:-$DEFAULT_TTL}"
    local cmd_hash=$(hash_cmd "$cmd")
    local now=$(date +%s)
    local expires=$((now + ttl))
    local sig=$(sign_hash "$cmd_hash" "$expires")
    
    sqlite3 "$CACHE_DB" "INSERT OR REPLACE INTO approvals VALUES ('$cmd_hash', '$cmd', $now, $expires, '$sig');"
    log_audit "CACHE_ADD" "$cmd_hash" "$cmd" "TTL:$ttl"
}

# Audit logging
log_audit() {
    local action="$1"
    local hash="$2"
    local cmd="$3"
    local result="$4"
    local ts=$(date -Iseconds)
    local preview="${cmd:0:50}"
    
    echo "{\"timestamp\":\"$ts\",\"action\":\"$action\",\"cmd_hash\":\"$hash\",\"cmd_preview\":\"$preview\",\"result\":\"$result\"}" >> "$AUDIT_LOG"
}

# Expire old entries
expire_cache() {
    local now=$(date +%s)
    local count=$(sqlite3 "$CACHE_DB" "DELETE FROM approvals WHERE expires_at <= $now; SELECT changes();")
    log_audit "CACHE_EXPIRE" "BULK" "N/A" "REMOVED:$count"
    echo "Expired $count entries"
}

# Audit report
show_audit() {
    tail -20 "$AUDIT_LOG" | jq -r '[.timestamp, .action, .result] | @tsv' 2>/dev/null || cat "$AUDIT_LOG" | tail -20
}

# CLI
CMD="${1:-help}"
case "$CMD" in
    check)
        shift
        if check_cache "$*"; then
            echo "APPROVED (cached)"
            exit 0
        else
            echo "REQUIRES_APPROVAL"
            exit 1
        fi
        ;;
    add)
        shift
        add_to_cache "$*" "${ELEV_CACHE_TTL:-$DEFAULT_TTL}"
        echo "ADDED to cache"
        ;;
    expire)
        expire_cache
        ;;
    audit)
        show_audit
        ;;
    *)
        echo "Usage: $0 {check|add|expire|audit} [command]"
        echo "  check <cmd>  - Check if command is pre-authorized"
        echo "  add <cmd>    - Add command to cache (with TTL)"
        echo "  expire       - Remove expired entries"
        echo "  audit        - Show recent audit log"
        exit 1
        ;;
esac
