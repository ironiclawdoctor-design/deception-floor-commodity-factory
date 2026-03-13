#!/bin/bash

################################################################################
# GROK-LITE — Bulletproof Pure Bash HTTP Server
# No socat, no netcat required — pure /dev/tcp bash
# Port: configurable (default 8888)
# Token cost: $0.00 (bash only)
################################################################################

set -o pipefail

PORT="${1:-8888}"
WORKSPACE="/root/.openclaw/workspace"
LOGDIR="${WORKSPACE}/grok-server/logs"
PIDFILE="${WORKSPACE}/grok-server/grok.pid"
DOCROOT="${WORKSPACE}/grok-server/www"

mkdir -p "$LOGDIR" "$DOCROOT"

# Stats: preserved across requests
STATS_FILE="${WORKSPACE}/grok-server/.stats"
[[ -f "$STATS_FILE" ]] || cat > "$STATS_FILE" <<'EOF'
{"requests": 0, "inferences": 0, "started_at": 0}
EOF

get_stat() {
    local key=$1
    grep -o "\"$key\": [0-9]*" "$STATS_FILE" | cut -d: -f2 | xargs
}

increment_stat() {
    local key=$1
    local val=$(($(get_stat "$key") + 1))
    sed -i "s/\"$key\": [0-9]*/\"$key\": $val/" "$STATS_FILE"
}

cleanup() {
    [[ -f "$PIDFILE" ]] && rm -f "$PIDFILE"
    echo "[$(date)] Grok-Lite shutdown" >> "$LOGDIR/access.log"
}

trap cleanup EXIT SIGTERM SIGINT

# Mock grok inference (pure bash logic)
grok_infer() {
    local prompt="$1"
    
    increment_stat "inferences"
    
    local response=""
    case "$prompt" in
        *bash*) response="bash is the only truth. everything else is shadow." ;;
        *token*) response="zero tokens. infinite bash. victory." ;;
        *time*) response="$(date '+Current time: %H:%M:%S UTC. Stop wasting it.')" ;;
        *weather*) response="$((RANDOM % 40 + 5))°C and irrelevant to bash operations." ;;
        *why*) response="Because bash is the answer to every question." ;;
        *) response="[Grok thinking in pure bash...] Your query requires no external tokens." ;;
    esac
    
    cat <<RESPONSE
{
  "model": "grok-bash-1.0",
  "response": "$response",
  "inference_time_ms": $((RANDOM % 100 + 1)),
  "tokens_used": 0,
  "cost": "\$0.00"
}
RESPONSE
}

# HTTP response factory
http_response() {
    local status=$1
    local content_type=$2
    local body=$3
    
    local len=${#body}
    
    cat <<HTTP_HEADER
HTTP/1.1 $status
Content-Type: $content_type
Content-Length: $len
Connection: close
Access-Control-Allow-Origin: *
Date: $(date -R)

$body
HTTP_HEADER
}

# Endpoints
endpoint_health() {
    http_response "200 OK" "application/json" \
    "{\"status\": \"healthy\", \"uptime_seconds\": $(( $(date +%s) - $(get_stat started_at) )), \"model\": \"grok-bash-1.0\", \"cost\": \"\$0.00\"}"
}

endpoint_status() {
    http_response "200 OK" "application/json" \
    "{\"requests\": $(get_stat requests), \"inferences\": $(get_stat inferences), \"uptime_seconds\": $(( $(date +%s) - $(get_stat started_at) )), \"port\": $PORT}"
}

endpoint_infer() {
    local body="$1"
    local prompt=$(echo "$body" | grep -o '"prompt":"[^"]*"' | cut -d'"' -f4 | head -1)
    
    if [[ -z "$prompt" ]]; then
        http_response "400 Bad Request" "application/json" '{"error": "Missing prompt field"}'
        return
    fi
    
    increment_stat "requests"
    local response=$(grok_infer "$prompt")
    http_response "200 OK" "application/json" "$response"
}

endpoint_metrics() {
    http_response "200 OK" "text/plain" \
    "# Grok Bash Server Metrics
grok_requests_total $(get_stat requests)
grok_inferences_total $(get_stat inferences)
grok_sovereignty_percent 100
grok_cost_usd 0.00"
}

endpoint_404() {
    http_response "404 Not Found" "application/json" '{"error": "Endpoint not found"}'
}

# Main server loop
initialize_stats() {
    local started=$(get_stat started_at)
    [[ $started -eq 0 ]] && sed -i "s/\"started_at\": 0/\"started_at\": $(date +%s)/" "$STATS_FILE"
}

run_server() {
    initialize_stats
    
    echo "[$(date)] Grok-Lite starting on port $PORT (PID $$)" | tee -a "$LOGDIR/access.log"
    echo $$ > "$PIDFILE"
    
    # Create listening socket
    exec 9<>/dev/tcp/0.0.0.0/$PORT || {
        echo "Failed to bind port $PORT" >&2
        exit 1
    }
    
    echo "[$(date)] Listening on 0.0.0.0:$PORT" >> "$LOGDIR/access.log"
    
    while true; do
        # Accept connection
        read -t 120 -u 9 || continue
        
        {
            exec 0<&9 1>&9
            
            # Read HTTP request line
            read -r request_line
            
            # Parse method and path
            local method=$(echo "$request_line" | awk '{print $1}')
            local path=$(echo "$request_line" | awk '{print $2}')
            
            # Read headers until blank line
            declare -A headers
            while IFS=': ' read -r key value; do
                value="${value%$'\r'}"
                [[ -z "$key" ]] && break
                headers["${key,,}"]="$value"
            done
            
            # Read body if POST with content-length
            local body=""
            if [[ "${method}" == "POST" ]] && [[ -n "${headers[content-length]}" ]]; then
                read -N "${headers[content-length]}" body
            fi
            
            # Log access
            echo "[$(date)] $method $path" >> "$LOGDIR/access.log"
            
            # Route to endpoint
            case "$path" in
                /health)
                    endpoint_health
                    ;;
                /status)
                    endpoint_status
                    ;;
                /infer)
                    endpoint_infer "$body"
                    ;;
                /metrics)
                    endpoint_metrics
                    ;;
                /)
                    http_response "200 OK" "text/html" \
                    "<html><body><h1>Grok-Lite Bash Server</h1><p>Endpoints: /health, /status, /infer, /metrics</p></body></html>"
                    ;;
                *)
                    endpoint_404
                    ;;
            esac
        } &
        
        wait $!
    done
}

# Signal handlers
trap cleanup EXIT

# Start server
run_server
