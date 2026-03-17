#!/bin/bash
################################################################################
# NEMESIS DAEMON CONTROL - Start/stop/status/tail audit log
################################################################################

DAEMON_SCRIPT="/root/.openclaw/workspace/tcpdump-nemesis-daemon.sh"
DAEMON_BIN="/root/tcpdump-nemesis-daemon.sh"
AUDIT_LOG="/root/.openclaw/workspace/tcpdump-nemesis-audit.jsonl"
PID_FILE="/tmp/nemesis-daemon.pid"

usage() {
    cat <<EOF
NEMESIS DAEMON CONTROL
Usage: $(basename $0) <command>

Commands:
  start           Start daemon in background
  stop            Stop running daemon
  status          Check daemon status
  tail [-n N]     Tail audit log (default: 20 lines)
  stats           Show threat statistics
  clear-log       Truncate audit log (archive first!)
  test            Run single cycle (no daemon loop)

Examples:
  $(basename $0) start
  $(basename $0) tail -n 50
  $(basename $0) stats

EOF
    exit 1
}

cmd_start() {
    if [ -f "${PID_FILE}" ] && kill -0 "$(cat ${PID_FILE})" 2>/dev/null; then
        echo "Daemon already running (PID: $(cat ${PID_FILE}))"
        exit 1
    fi
    
    nohup "${DAEMON_BIN}" > /tmp/nemesis-daemon.log 2>&1 &
    local pid=$!
    echo $pid > "${PID_FILE}"
    
    echo "✓ Daemon started (PID: ${pid})"
    echo "✓ Log: /tmp/nemesis-daemon.log"
    echo "✓ Audit: ${AUDIT_LOG}"
}

cmd_stop() {
    if [ ! -f "${PID_FILE}" ]; then
        echo "Daemon not running"
        exit 1
    fi
    
    local pid=$(cat "${PID_FILE}")
    if kill -0 "$pid" 2>/dev/null; then
        kill "$pid"
        rm -f "${PID_FILE}"
        echo "✓ Daemon stopped (PID was: ${pid})"
    else
        rm -f "${PID_FILE}"
        echo "Daemon not running (stale PID file removed)"
    fi
}

cmd_status() {
    if [ ! -f "${PID_FILE}" ]; then
        echo "Status: STOPPED"
        return 1
    fi
    
    local pid=$(cat "${PID_FILE}")
    if kill -0 "$pid" 2>/dev/null; then
        local uptime=$(ps -o etime= -p "$pid" | xargs)
        local cpu=$(ps -o %cpu= -p "$pid" | xargs)
        local mem=$(ps -o %mem= -p "$pid" | xargs)
        
        echo "Status: RUNNING"
        echo "PID: ${pid}"
        echo "Uptime: ${uptime}"
        echo "CPU: ${cpu}%"
        echo "Memory: ${mem}%"
        
        local threat_count=$(wc -l < "${AUDIT_LOG}" 2>/dev/null || echo 0)
        echo "Threats logged: ${threat_count}"
    else
        rm -f "${PID_FILE}"
        echo "Status: STOPPED (stale PID)"
        return 1
    fi
}

cmd_tail() {
    local lines=20
    if [ "$2" == "-n" ] && [ -n "$3" ]; then
        lines=$3
    fi
    
    if [ ! -f "${AUDIT_LOG}" ]; then
        echo "Audit log not found: ${AUDIT_LOG}"
        return 1
    fi
    
    echo "=== NEMESIS AUDIT LOG (last ${lines} entries) ==="
    tail -n "${lines}" "${AUDIT_LOG}" | while IFS= read -r line; do
        # Pretty-print JSON
        echo "$line" | jq . 2>/dev/null || echo "$line"
    done
}

cmd_stats() {
    if [ ! -f "${AUDIT_LOG}" ]; then
        echo "Audit log not found: ${AUDIT_LOG}"
        return 1
    fi
    
    echo "=== NEMESIS THREAT STATISTICS ==="
    echo ""
    echo "Total entries: $(wc -l < "${AUDIT_LOG}")"
    echo ""
    
    echo "By threat type:"
    grep -oP '"threat_type":"\K[^"]+' "${AUDIT_LOG}" | sort | uniq -c | sort -rn
    
    echo ""
    echo "By severity:"
    grep -oP '"severity":"\K[^"]+' "${AUDIT_LOG}" | sort | uniq -c | sort -rn
    
    echo ""
    echo "Critical threats:"
    grep '"severity":"critical"' "${AUDIT_LOG}" | wc -l
    
    echo ""
    echo "Last entry:"
    tail -1 "${AUDIT_LOG}" | jq . 2>/dev/null
}

cmd_clear_log() {
    if [ ! -f "${AUDIT_LOG}" ]; then
        echo "Audit log not found"
        return 1
    fi
    
    read -p "Archive audit log before clearing? (y/n) " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        local archive="${AUDIT_LOG}.$(date +%s).bak"
        cp "${AUDIT_LOG}" "${archive}"
        echo "✓ Archived to: ${archive}"
    fi
    
    : > "${AUDIT_LOG}"
    echo "✓ Audit log cleared"
}

cmd_test() {
    echo "Running single audit cycle..."
    # Source the daemon script and run detection functions
    bash -c "
        source \"${DAEMON_SCRIPT}\"
        AUDIT_LOG=\"${AUDIT_LOG}\"
        TEMP_DIR=\"/tmp/nemesis-test-$$\"
        mkdir -p \"\${TEMP_DIR}\"
        trap \"rm -rf \${TEMP_DIR}\" EXIT
        
        PCAP=\"\${TEMP_DIR}/test.pcap\"
        timeout 5 tcpdump -i any -w \"\${PCAP}\" 2>/dev/null || true
        
        if [ -s \"\${PCAP}\" ]; then
            echo \"[Test] Captured $(tcpdump -r \${PCAP} 2>/dev/null | wc -l) packets\"
            detect_exfiltration \"\${PCAP}\" 999
            detect_token_burn \"\${PCAP}\" 999
            detect_customer_data_access \"\${PCAP}\" 999
            detect_distraction_traffic \"\${PCAP}\" 999
        else
            echo \"[Test] No packets captured (check network interface)\"
        fi
    "
}

main() {
    [ $# -eq 0 ] && usage
    
    case "$1" in
        start)   cmd_start ;;
        stop)    cmd_stop ;;
        status)  cmd_status ;;
        tail)    cmd_tail "$@" ;;
        stats)   cmd_stats ;;
        clear-log) cmd_clear_log ;;
        test)    cmd_test ;;
        *)       usage ;;
    esac
}

main "$@"
