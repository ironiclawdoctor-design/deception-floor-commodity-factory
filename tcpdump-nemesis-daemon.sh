#!/bin/bash
################################################################################
# TCPDUMP NEMESIS DAEMON
# Background network monitor (30-second audit cycles)
# Detects: Exfiltration, Token leaks, Customer data access, Distraction traffic
# Output: /root/.openclaw/workspace/tcpdump-nemesis-audit.jsonl (append-only)
# Cost: Tier 0 bash only ($0.00)
################################################################################

set -e

WORKSPACE="/root/.openclaw/workspace"
AUDIT_LOG="${WORKSPACE}/tcpdump-nemesis-audit.jsonl"
TEMP_DIR="/tmp/nemesis-$$"
CYCLE_SECONDS=30
PATTERN_WINDOW=300  # 5-minute window for pattern detection

# Ensure log file exists
touch "${AUDIT_LOG}"
mkdir -p "${TEMP_DIR}"
trap "rm -rf ${TEMP_DIR}" EXIT

################################################################################
# NEMESIS THREAT DEFINITIONS
################################################################################

# Exfiltration indicators: Unusual outbound traffic
declare -A EXFIL_INDICATORS=(
    ["large_outbound"]="5000"      # >5KB outbound in 30s
    ["dns_flood"]="10"              # >10 DNS queries in 30s
    ["direct_ip"]="1"               # Direct IP connections (not DNS)
    ["non_standard_port"]="1"       # Ports >40000 (typically scanning)
)

# Token burn indicators: API calls that cost money
declare -A TOKEN_INDICATORS=(
    ["openai_api"]="api.openai.com|443"
    ["claude_api"]="anthropic.com|443|8443"
    ["stripe_api"]="api.stripe.com|443"
    ["aws_api"]="amazonaws.com|443"
    ["gcp_api"]="googleapis.com|443"
    ["azure_api"]="azure.com|443"
)

# Sensitive data protocols
declare -A SENSITIVE_PROTOCOLS=(
    ["ssh"]="22"
    ["mysql"]="3306"
    ["postgres"]="5432"
    ["mongodb"]="27017"
    ["redis"]="6379"
)

# Benign traffic (agency-internal, non-critical)
declare -A BENIGN_TRAFFIC=(
    ["ntp"]="123"
    ["dns"]="53"
    ["http"]="80"
    ["dhcp"]="67|68"
)

################################################################################
# UTILITY FUNCTIONS
################################################################################

log_json() {
    local timestamp=$(date -u +"%Y-%m-%dT%H:%M:%S.%3NZ")
    local cycle_num=$1
    local threat_type=$2
    local severity=$3  # critical|high|medium|low
    local details=$4   # JSON object as string
    
    local json_entry=$(cat <<EOF
{"timestamp":"${timestamp}","cycle":${cycle_num},"threat_type":"${threat_type}","severity":"${severity}","details":${details}}
EOF
)
    
    echo "${json_entry}" >> "${AUDIT_LOG}"
}

extract_pcap_summary() {
    local pcap_file=$1
    local output_file=$2
    
    # Parse tcpdump output for key metrics
    # Format: src_ip|src_port|dst_ip|dst_port|protocol|bytes
    tcpdump -r "${pcap_file}" -n 2>/dev/null | awk '{
        if ($3 ~ /\./) {
            split($3, src, ".");
            split($5, dst, ".");
            # Extract protocol from output
            proto="TCP"; 
            if ($0 ~ /UDP/) proto="UDP";
            if ($0 ~ /ICMP/) proto="ICMP";
            printf "%s|%s|%s|%s|%s\n", src[1]"."src[2]"."src[3]"."src[4], 
                   (NF>=7 ? $7 : "?"), 
                   dst[1]"."dst[2]"."dst[3]"."dst[4],
                   (NF>=8 ? $8 : "?"),
                   proto;
        }
    }' > "${output_file}"
}

detect_exfiltration() {
    local pcap_file=$1
    local cycle_num=$2
    local findings=""
    
    # 1. Large outbound transfers
    local outbound_bytes=$(tcpdump -r "${pcap_file}" -n 2>/dev/null | \
        awk '$5 ~ /^192\.168|^10\.|^172\./ && $7 ~ /^[0-9]+\.[0-9]+\.[^1][0-9]+\.[0-9]+$/ {sum+=$2} END {print sum+0}')
    
    if (( outbound_bytes > 5000 )); then
        findings+="{\"type\":\"large_outbound\",\"bytes\":${outbound_bytes}}"
    fi
    
    # 2. DNS flooding
    local dns_queries=$(tcpdump -r "${pcap_file}" -n 'udp port 53' 2>/dev/null | wc -l)
    if (( dns_queries > 10 )); then
        findings+="{\"type\":\"dns_flood\",\"queries\":${dns_queries}},"
    fi
    
    # 3. Direct IP connections (bypassing DNS)
    local direct_ips=$(tcpdump -r "${pcap_file}" -n 2>/dev/null | \
        grep -v 'DNS\|NTP\|ICMP' | awk -F' > ' '{print $2}' | cut -d. -f1-4 | sort -u | wc -l)
    
    if (( direct_ips > 5 )); then
        findings+="{\"type\":\"direct_ip_suspicious\",\"unique_ips\":${direct_ips}},"
    fi
    
    # 4. Non-standard ports (scanning indicator)
    local high_ports=$(tcpdump -r "${pcap_file}" -n 2>/dev/null | \
        awk -F'[.:]' '{if ($NF > 40000) count++} END {print count+0}')
    
    if (( high_ports > 5 )); then
        findings+="{\"type\":\"high_port_scanning\",\"attempts\":${high_ports}},"
    fi
    
    # Remove trailing comma
    findings="${findings%,}"
    
    if [ -n "${findings}" ]; then
        log_json "${cycle_num}" "exfiltration" "high" "[${findings}]"
        return 0
    fi
    return 1
}

detect_token_burn() {
    local pcap_file=$1
    local cycle_num=$2
    local findings=""
    local api_call_count=0
    
    # Check for API provider destinations
    for api_name in "${!TOKEN_INDICATORS[@]}"; do
        local pattern="${TOKEN_INDICATORS[$api_name]}"
        local matches=$(tcpdump -r "${pcap_file}" -n "${pattern}" 2>/dev/null | wc -l)
        
        if (( matches > 0 )); then
            findings+="{\"api\":\"${api_name}\",\"connections\":${matches}},"
            (( api_call_count += matches ))
        fi
    done
    
    # Pattern: >5 API calls in 30s = cost leak
    if (( api_call_count > 5 )); then
        findings+="{\"pattern\":\"api_burst\",\"calls_per_30s\":${api_call_count},\"severity\":\"cost_leak\"},"
    fi
    
    findings="${findings%,}"
    
    if [ -n "${findings}" ]; then
        log_json "${cycle_num}" "token_burn" "critical" "[${findings}]"
        return 0
    fi
    return 1
}

detect_customer_data_access() {
    local pcap_file=$1
    local cycle_num=$2
    local findings=""
    
    # Monitor sensitive protocol access
    for proto in "${!SENSITIVE_PROTOCOLS[@]}"; do
        local port="${SENSITIVE_PROTOCOLS[$proto]}"
        local connections=$(tcpdump -r "${pcap_file}" -n "port ${port}" 2>/dev/null | wc -l)
        
        if (( connections > 0 )); then
            # Determine source (internal vs external)
            local external=$(tcpdump -r "${pcap_file}" -n "port ${port}" 2>/dev/null | \
                grep -v '192\.168\|10\.\|172\.1[6-9]\|172\.2[0-9]\|172\.3[0-1]' | wc -l)
            
            if (( external > 0 )); then
                findings+="{\"protocol\":\"${proto}\",\"port\":${port},\"external_connections\":${external}},"
            fi
        fi
    done
    
    findings="${findings%,}"
    
    if [ -n "${findings}" ]; then
        log_json "${cycle_num}" "customer_data_access" "critical" "[${findings}]"
        return 0
    fi
    return 1
}

detect_distraction_traffic() {
    local pcap_file=$1
    local cycle_num=$2
    local findings=""
    local total_packets=$(tcpdump -r "${pcap_file}" -n 2>/dev/null | wc -l)
    
    # Benign traffic volume
    local benign_packets=0
    for protocol in "${!BENIGN_TRAFFIC[@]}"; do
        local port="${BENIGN_TRAFFIC[$protocol]}"
        benign_packets=$(( benign_packets + $(tcpdump -r "${pcap_file}" -n "port ${port}" 2>/dev/null | wc -l) ))
    done
    
    # Non-agency, non-critical traffic
    local suspicious_percentage=$(( (total_packets - benign_packets) * 100 / (total_packets + 1) ))
    
    if (( suspicious_percentage > 60 )); then
        findings+="{\"non_benign_traffic_percent\":${suspicious_percentage},\"total_packets\":${total_packets}}"
    fi
    
    if [ -n "${findings}" ]; then
        log_json "${cycle_num}" "distraction_traffic" "medium" "${findings}"
        return 0
    fi
    return 1
}

detect_patterns() {
    local cycle_num=$1
    
    # Analyze last 5 minutes of audit log for patterns
    local recent_threats=$(tail -c 5000 "${AUDIT_LOG}" 2>/dev/null | \
        grep -oP '"threat_type":"\K[^"]+' | sort | uniq -c | sort -rn)
    
    local burst_api=$(tail -c 5000 "${AUDIT_LOG}" 2>/dev/null | \
        grep 'token_burn.*api_burst' | wc -l)
    
    if (( burst_api >= 3 )); then
        log_json "${cycle_num}" "pattern_detected" "critical" \
            "{\"pattern\":\"repeated_api_bursts\",\"occurrences\":${burst_api},\"window\":\"5m\",\"implication\":\"sustained_cost_leak\"}"
    fi
    
    # Threat concentration
    if echo "${recent_threats}" | head -1 | awk '{if ($1 > 5) exit 0; exit 1}'; then
        log_json "${cycle_num}" "pattern_detected" "high" \
            "{\"pattern\":\"threat_concentration\",\"data\":\"${recent_threats}\"}"
    fi
}

################################################################################
# MAIN DAEMON LOOP
################################################################################

daemon_main() {
    local cycle_num=0
    local pcap_file="${TEMP_DIR}/capture.pcap"
    
    echo "[$(date -u '+%Y-%m-%d %H:%M:%S')] TCPDUMP NEMESIS DAEMON STARTED" >&2
    echo "[$(date -u '+%Y-%m-%d %H:%M:%S')] Audit log: ${AUDIT_LOG}" >&2
    echo "[$(date -u '+%Y-%m-%d %H:%M:%S')] Cycle interval: ${CYCLE_SECONDS}s" >&2
    
    while true; do
        (( cycle_num++ ))
        local cycle_start=$(date +%s)
        
        # Capture 30-second pcap snapshot
        timeout ${CYCLE_SECONDS} tcpdump -i any -w "${pcap_file}" -Q in -Q out 2>/dev/null || true
        
        # Run threat detection (all in parallel for speed)
        if [ -s "${pcap_file}" ]; then
            detect_exfiltration "${pcap_file}" "${cycle_num}" &
            detect_token_burn "${pcap_file}" "${cycle_num}" &
            detect_customer_data_access "${pcap_file}" "${cycle_num}" &
            detect_distraction_traffic "${pcap_file}" "${cycle_num}" &
            wait  # Wait for all detections to complete
            
            # Pattern analysis every 5 minutes (10 cycles)
            if (( cycle_num % 10 == 0 )); then
                detect_patterns "${cycle_num}"
            fi
        fi
        
        # Cleanup pcap for next cycle
        rm -f "${pcap_file}"
        
        # Sleep remainder of cycle
        local cycle_elapsed=$(( $(date +%s) - cycle_start ))
        local sleep_time=$(( CYCLE_SECONDS - cycle_elapsed ))
        if (( sleep_time > 0 )); then
            sleep "${sleep_time}"
        fi
    done
}

################################################################################
# ENTRY POINT
################################################################################

if [ "${BASH_SOURCE[0]}" == "${0}" ]; then
    daemon_main "$@"
fi
