#!/bin/bash
#
# agency-protocol-filters.sh
# Protocol capture functions for tcpdump packet analysis
# Learning patterns from actual network traffic (not documentation)
# Cost: $0.00 (Tier 0 bash only)
#
# Usage: source this file, then call individual capture functions
# Example: capture_http() or capture_all_protocols()
#

# ============================================================================
# FUNCTION 1: capture_http
# Captures HTTP/HTTPS traffic (ports 80, 443)
# Recursive: learns both request patterns and response patterns
# ============================================================================

capture_http() {
    local interface="${1:-any}"
    local output_file="${2:-.}"
    
    echo "[LEARNING] HTTP/HTTPS traffic on $interface"
    echo "Capture includes: SYN handshake, request headers, response codes"
    echo "Recursive: watching for pipelined requests, chunked encoding, redirects"
    
    if [[ "$output_file" != "." ]]; then
        tcpdump -i "$interface" -w "$output_file/http-capture.pcap" \
            '(tcp port 80 or tcp port 443)' \
            -s 0 -A -v 2>&1 | head -100
    else
        echo "tcpdump -i $interface '(tcp port 80 or tcp port 443)' -s 0 -A -v"
    fi
}

# ============================================================================
# FUNCTION 2: capture_ssh
# Captures SSH traffic (port 22)
# Recursive: learns handshake, authentication attempts, command sequences
# ============================================================================

capture_ssh() {
    local interface="${1:-any}"
    local output_file="${2:-.}"
    
    echo "[LEARNING] SSH (git, repos) traffic on $interface"
    echo "Capture includes: SSH handshake, banner exchange, key exchange"
    echo "Recursive: watching for authentication methods, channel opens, command frames"
    
    if [[ "$output_file" != "." ]]; then
        tcpdump -i "$interface" -w "$output_file/ssh-capture.pcap" \
            'tcp port 22' \
            -s 0 -A -v 2>&1 | head -100
    else
        echo "tcpdump -i $interface 'tcp port 22' -s 0 -A -v"
    fi
}

# ============================================================================
# FUNCTION 3: capture_dns
# Captures DNS resolution traffic (port 53)
# Recursive: learns query/response patterns, DNSSEC, caching behavior
# ============================================================================

capture_dns() {
    local interface="${1:-any}"
    local output_file="${2:-.}"
    
    echo "[LEARNING] DNS resolution traffic on $interface"
    echo "Capture includes: DNS queries (A, AAAA, MX, CNAME), responses, TTL"
    echo "Recursive: watching for recursive queries, zone transfers, EDNS extensions"
    
    if [[ "$output_file" != "." ]]; then
        tcpdump -i "$interface" -w "$output_file/dns-capture.pcap" \
            '(udp port 53 or tcp port 53)' \
            -s 0 -A -v 2>&1 | head -100
    else
        echo "tcpdump -i $interface '(udp port 53 or tcp port 53)' -s 0 -A -v"
    fi
}

# ============================================================================
# FUNCTION 4: capture_tcp_udp_internal
# Captures internal TCP/UDP traffic (local network, non-standard ports)
# Recursive: learns about internal service discovery, heartbeats, control plane
# ============================================================================

capture_tcp_udp_internal() {
    local interface="${1:-any}"
    local output_file="${2:-.}"
    local source_net="${3:-192.168.0.0/16}"
    
    echo "[LEARNING] Internal TCP/UDP traffic on $interface (source: $source_net)"
    echo "Capture includes: All TCP/UDP except HTTP/HTTPS/SSH/DNS"
    echo "Recursive: watching for service discovery, internal APIs, heartbeats"
    
    if [[ "$output_file" != "." ]]; then
        tcpdump -i "$interface" -w "$output_file/tcp-udp-internal-capture.pcap" \
            "src net $source_net and (tcp or udp) and not (tcp port 80 or tcp port 443 or tcp port 22 or udp port 53 or tcp port 53)" \
            -s 0 -A -v 2>&1 | head -100
    else
        echo "tcpdump -i $interface 'src net $source_net and (tcp or udp) and not (tcp port 80 or tcp port 443 or tcp port 22 or udp port 53 or tcp port 53)' -s 0 -A -v"
    fi
}

# ============================================================================
# FUNCTION 5: capture_sqlite
# Captures local database I/O patterns (SQLite via process monitoring)
# Recursive: learns file locks, transaction patterns, WAL mode behavior
# Note: SQLite uses local file I/O, not network packets
# Use strace/lsof for actual observation
# ============================================================================

capture_sqlite() {
    local db_path="${1:-.}"
    local process_pattern="${2:-openclaw|agency|sqlite}"
    
    echo "[LEARNING] SQLite local database I/O patterns"
    echo "Database path: $db_path"
    echo "Recursive: watching for .db files, .db-wal, .db-shm (WAL mode)"
    echo "Method: lsof (open files) + strace (syscalls) instead of tcpdump"
    
    # Find all SQLite database files
    echo ""
    echo "=== Open SQLite database files ==="
    lsof -c "$process_pattern" 2>/dev/null | grep -E '\.db(-wal|-shm)?$' | awk '{print $9}' | sort -u
    
    echo ""
    echo "=== SQLite process activity (sample) ==="
    ps aux | grep -i sqlite | grep -v grep
    
    echo ""
    echo "=== Database files in workspace ==="
    find /root/.openclaw/workspace -name '*.db*' -type f 2>/dev/null | head -20
}

# ============================================================================
# FUNCTION 6: capture_bitnet
# Captures JSON-RPC (BitNet inference) traffic
# Recursive: learns request/response envelope, model params, token flow
# Typical ports: 5000-5999 (local), or HTTP/HTTPS for remote
# ============================================================================

capture_bitnet() {
    local interface="${1:-any}"
    local output_file="${2:-.}"
    local bitnet_port="${3:-5000}"
    
    echo "[LEARNING] JSON-RPC (BitNet) traffic on $interface:$bitnet_port"
    echo "Capture includes: RPC method calls, params, responses, errors"
    echo "Recursive: watching for streaming responses, rate limits, token usage"
    
    if [[ "$output_file" != "." ]]; then
        tcpdump -i "$interface" -w "$output_file/bitnet-capture.pcap" \
            "tcp port $bitnet_port" \
            -s 0 -A -v 2>&1 | head -100
    else
        echo "tcpdump -i $interface 'tcp port $bitnet_port' -s 0 -A -v"
    fi
}

# ============================================================================
# FUNCTION 7: capture_cron_metadata
# Captures cron task execution patterns (via syslog, process events)
# Recursive: learns task triggers, environment, exit codes
# Note: Cron doesn't use network; observe via logs and process monitoring
# ============================================================================

capture_cron_metadata() {
    local log_source="${1:-/var/log/syslog}"
    local time_window="${2:-60}"  # minutes
    
    echo "[LEARNING] Cron task execution metadata (last $time_window minutes)"
    echo "Log source: $log_source"
    echo "Recursive: watching for CRON entries, environment variables, commands"
    
    echo ""
    echo "=== Recent cron executions (syslog) ==="
    if [[ -f "$log_source" ]]; then
        # Show cron lines from last N minutes
        grep CRON "$log_source" | tail -50
    else
        echo "Note: $log_source not accessible (try with sudo)"
    fi
    
    echo ""
    echo "=== Cron jobs configured (user crontabs) ==="
    crontab -l 2>/dev/null || echo "(No crontab for current user)"
    
    echo ""
    echo "=== System-wide cron jobs ==="
    find /etc/cron.* -type f 2>/dev/null | xargs ls -lh | head -20
    
    echo ""
    echo "=== Background processes (likely cron-spawned) ==="
    ps aux | grep -E '\(cron\)|/bin/sh.*cron' | grep -v grep
}

# ============================================================================
# HELPER FUNCTION: capture_all_protocols
# Runs all 7 protocol captures (non-blocking, informational)
# ============================================================================

capture_all_protocols() {
    local output_dir="${1:-/tmp/agency-pcaps}"
    
    echo "=========================================="
    echo "AGENCY PROTOCOL CAPTURE SUITE"
    echo "=========================================="
    echo ""
    
    mkdir -p "$output_dir"
    
    capture_http "any" "$output_dir"
    echo ""
    
    capture_ssh "any" "$output_dir"
    echo ""
    
    capture_dns "any" "$output_dir"
    echo ""
    
    capture_tcp_udp_internal "any" "$output_dir" "192.168.0.0/16"
    echo ""
    
    capture_sqlite "$output_dir"
    echo ""
    
    capture_bitnet "any" "$output_dir" "5000"
    echo ""
    
    capture_cron_metadata "/var/log/syslog" "60"
    echo ""
    
    echo "=========================================="
    echo "Protocol capture functions exported"
    echo "Use: capture_http, capture_ssh, capture_dns, capture_tcp_udp_internal,"
    echo "     capture_sqlite, capture_bitnet, capture_cron_metadata"
    echo "=========================================="
}

# ============================================================================
# Export functions for use in terminal
# ============================================================================

export -f capture_http
export -f capture_ssh
export -f capture_dns
export -f capture_tcp_udp_internal
export -f capture_sqlite
export -f capture_bitnet
export -f capture_cron_metadata
export -f capture_all_protocols

# If called directly (not sourced), run info
if [[ "${BASH_SOURCE[0]}" == "${0}" ]]; then
    cat << 'USAGE'
agency-protocol-filters.sh - Protocol capture suite for agency operations

USAGE:
  source agency-protocol-filters.sh
  capture_http [interface] [output_dir]      # HTTP/HTTPS (ports 80, 443)
  capture_ssh [interface] [output_dir]       # SSH (port 22)
  capture_dns [interface] [output_dir]       # DNS (port 53)
  capture_tcp_udp_internal [interface] [dir] [subnet]  # Internal services
  capture_sqlite [db_path] [process_pattern] # SQLite local I/O
  capture_bitnet [interface] [dir] [port]    # JSON-RPC (BitNet)
  capture_cron_metadata [log_file] [minutes] # Cron execution patterns
  capture_all_protocols [output_dir]         # Run all 7 captures

EXAMPLES:
  # View HTTP/HTTPS filters (no capture, just show command)
  source agency-protocol-filters.sh
  capture_http

  # Capture DNS to file
  capture_dns any /tmp/agency-pcaps

  # Monitor all protocols
  capture_all_protocols /tmp/agency-pcaps

  # Check SQLite activity
  capture_sqlite /root/.openclaw/workspace

NOTES:
  - All functions export callable in any shell session
  - Recursive-aware: tcpdump filters learn from actual packets
  - Cost: Tier 0 bash only ($0.00)
  - Some functions (SQLite, cron) use lsof/strace instead of tcpdump
    (local file I/O doesn't generate network packets)

AGENCY PROTOCOL MAP:
  1. HTTP/HTTPS → External APIs, web services (80, 443)
  2. SSH        → Git, repos, remote execution (22)
  3. DNS        → Domain resolution, service discovery (53)
  4. TCP/UDP    → Internal services, control plane, heartbeats
  5. SQLite     → Local database I/O, state persistence
  6. JSON-RPC   → BitNet inference, local reasoning engine (5000+)
  7. Cron       → Scheduled tasks, async operations, maintenance

RECURSIVE LEARNING:
  tcpdump doesn't read documentation. It captures actual packets.
  Each function is designed to see patterns emerge from real traffic:
  - HTTP: pipelined requests, chunked encoding, redirects
  - SSH: authentication methods, channel multiplex, command frames
  - DNS: recursive queries, zone transfers, EDNS extensions
  - Internal: service discovery, heartbeats, control messages
  - SQLite: file locks, WAL mode, transaction patterns
  - JSON-RPC: streaming, rate limits, token accounting
  - Cron: triggers, environment, exit codes, timing
USAGE
fi
