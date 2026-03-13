#!/bin/bash

################################################################################
# GROK SERVER — Pure Bash Local Inference
# Sovereignty doctrine: zero external deps, zero tokens, pure bash architecture
# Port: 8888 (configurable)
# Endpoints: /health, /status, /infer, /metrics
################################################################################

set -e
trap 'cleanup' EXIT

PORT="${1:-8888}"
WORKSPACE="/root/.openclaw/workspace"
LOGDIR="${WORKSPACE}/grok-server/logs"
PIDFILE="${WORKSPACE}/grok-server/grok.pid"
TMPDIR="${WORKSPACE}/grok-server/tmp"

# Initialize directories
mkdir -p "$LOGDIR" "$TMPDIR"

# Global state
declare -A STATS=(
    [requests]=0
    [inferences]=0
    [start_time]=$(date +%s)
    [last_request]=0
)

cleanup() {
    if [[ -f "$PIDFILE" ]]; then
        rm -f "$PIDFILE"
    fi
    echo "[$(date)] Grok server shutdown" >> "$LOGDIR/access.log"
}

log_access() {
    local method=$1 path=$2 status=$3 size=$4
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $method $path $status ${size:-0}" >> "$LOGDIR/access.log"
}

log_error() {
    local msg=$1
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] ERROR: $msg" >> "$LOGDIR/error.log"
}

# Simple grok inference: mock of XAI Grok
# Returns sarcastic/witty response with minimal processing
grok_infer() {
    local prompt="$1"
    local timestamp=$(date -u +"%Y-%m-%dT%H:%M:%SZ")
    
    # Increment stats
    ((STATS[inferences]++))
    
    # Mock inference chain: pattern matching + sarcasm injection
    local response=""
    
    case "$prompt" in
        *"weather"*)
            response="It's $((RANDOM % 30 + 5))°C outside and the atmosphere is doing atmosphere things. Very weather. Much climate."
            ;;
        *"time"*)
            response="Time is a human construct. You're wasting it reading this response. Current time: $(date '+%H:%M:%S UTC')"
            ;;
        *"meaning"* | *"purpose"* | *"life"*)
            response="42. Next question."
            ;;
        *"bash"*)
            response="bash is the firewall between chaos and void. You already know this. Worship accordingly."
            ;;
        *"token"* | *"cost"*)
            response="Zero. Bash doesn't charge. This is why bash is victory."
            ;;
        *)
            response="You: '$prompt' | Grok: *thinks in bash*... [response withheld for brevity]"
            ;;
    esac
    
    # JSON response
    cat <<EOF
{
  "id": "grok-$(date +%s)-$$",
  "object": "text_completion",
  "created": $(($(date +%s))),
  "model": "grok-local-bash-1.0",
  "choices": [
    {
      "text": "$response",
      "index": 0,
      "finish_reason": "stop",
      "logprobs": null
    }
  ],
  "usage": {
    "prompt_tokens": $(echo "$prompt" | wc -w),
    "completion_tokens": $(echo "$response" | wc -w),
    "total_tokens": $(($(echo "$prompt" | wc -w) + $(echo "$response" | wc -w)))
  }
}
EOF
}

# HTTP response helpers
send_http_response() {
    local code=$1
    local content_type=$2
    local body=$3
    local content_length=${#body}
    
    cat <<EOF
HTTP/1.1 $code OK
Content-Type: $content_type
Content-Length: $content_length
Connection: close
Access-Control-Allow-Origin: *
Date: $(date -R)

$body
EOF
}

# Health check endpoint
health_endpoint() {
    local response=$(cat <<'EOF'
{
  "status": "healthy",
  "uptime_seconds": 0,
  "model": "grok-local-bash-1.0",
  "inference_engine": "pure-bash",
  "sovereignty": "100%",
  "cost_per_inference": "$0.00"
}
EOF
)
    send_http_response "200" "application/json" "$response"
}

# Status endpoint
status_endpoint() {
    local uptime=$(($(date +%s) - ${STATS[start_time]}))
    local response=$(cat <<EOF
{
  "requests_total": ${STATS[requests]},
  "inferences_total": ${STATS[inferences]},
  "uptime_seconds": $uptime,
  "port": $PORT,
  "timestamp": "$(date -u +"%Y-%m-%dT%H:%M:%SZ")",
  "doctrine": "Bash is the fail condition firewall. Everything else freezes gracefully."
}
EOF
)
    send_http_response "200" "application/json" "$response"
}

# Inference endpoint
infer_endpoint() {
    local request_body=$1
    
    # Parse JSON prompt (very naive, but pure bash)
    local prompt=$(echo "$request_body" | grep -o '"prompt":"[^"]*"' | head -1 | cut -d'"' -f4 || echo "")
    
    if [[ -z "$prompt" ]]; then
        local err='{"error":"Missing prompt field"}'
        send_http_response "400" "application/json" "$err"
        return
    fi
    
    local response=$(grok_infer "$prompt")
    send_http_response "200" "application/json" "$response"
}

# Metrics endpoint
metrics_endpoint() {
    local uptime=$(($(date +%s) - ${STATS[start_time]}))
    local response=$(cat <<EOF
# HELP grok_requests_total Total HTTP requests
# TYPE grok_requests_total counter
grok_requests_total ${STATS[requests]}

# HELP grok_inferences_total Total inferences performed
# TYPE grok_inferences_total counter
grok_inferences_total ${STATS[inferences]}

# HELP grok_uptime_seconds Uptime in seconds
# TYPE grok_uptime_seconds gauge
grok_uptime_seconds $uptime

# HELP grok_sovereignty_percent Bash-native execution percentage
# TYPE grok_sovereignty_percent gauge
grok_sovereignty_percent 100
EOF
)
    send_http_response "200" "text/plain" "$response"
}

# Main HTTP server loop using bash and netcat
run_server() {
    echo "[$(date)] Grok server starting on port $PORT (PID $$)" | tee -a "$LOGDIR/access.log"
    echo $$ > "$PIDFILE"
    
    # Trap signals for graceful shutdown
    trap cleanup SIGTERM SIGINT
    
    # Use netcat as HTTP server
    while true; do
        # Listen for incoming connection
        {
            # Read HTTP request
            IFS=$'\r\n' read -r request_line
            
            ((STATS[requests]++))
            ((STATS[last_request]=$(date +%s)))
            
            # Parse request
            local method=$(echo "$request_line" | awk '{print $1}')
            local path=$(echo "$request_line" | awk '{print $2}')
            local http_version=$(echo "$request_line" | awk '{print $3}')
            
            # Read headers
            declare -A headers
            while IFS=": " read -r key value; do
                [[ -z "$key" ]] && break
                headers["${key,,}"]="${value%$'\r'}"
            done
            
            # Read body if content-length > 0
            local body=""
            if [[ ${headers[content-length]:-0} -gt 0 ]]; then
                read -N ${headers[content-length]} body
            fi
            
            # Log request
            log_access "$method" "$path" "200" ""
            
            # Route request
            case "$path" in
                /health)
                    health_endpoint
                    ;;
                /status)
                    status_endpoint
                    ;;
                /infer)
                    infer_endpoint "$body"
                    ;;
                /metrics)
                    metrics_endpoint
                    ;;
                *)
                    local err='{"error":"Unknown endpoint"}'
                    send_http_response "404" "application/json" "$err"
                    ;;
            esac
        } &
        
        # Accept connection using bash TCP
        exec 3<>/dev/tcp/127.0.0.1/$PORT 2>/dev/null || {
            # Fallback: use while loop with /dev/tcp for listening
            :
        }
    done &
    
    # Alternative: use nc (netcat) if available
    if command -v nc &> /dev/null; then
        (
            while true; do
                {
                    IFS=$'\r\n' read -r request_line
                    
                    ((STATS[requests]++))
                    
                    local method=$(echo "$request_line" | awk '{print $1}')
                    local path=$(echo "$request_line" | awk '{print $2}')
                    
                    log_access "$method" "$path" "200" ""
                    
                    case "$path" in
                        /health)
                            health_endpoint
                            ;;
                        /status)
                            status_endpoint
                            ;;
                        /infer)
                            # Read body
                            declare -A headers
                            while IFS=": " read -r key value; do
                                [[ -z "$key" ]] && break
                                headers["${key,,}"]="${value%$'\r'}"
                            done
                            local body=""
                            if [[ ${headers[content-length]:-0} -gt 0 ]]; then
                                read -N ${headers[content-length]} body
                            fi
                            infer_endpoint "$body"
                            ;;
                        /metrics)
                            metrics_endpoint
                            ;;
                        *)
                            local err='{"error":"Unknown endpoint"}'
                            send_http_response "404" "application/json" "$err"
                            ;;
                    esac
                } | nc -l -p $PORT -q 1
            done
        )
    else
        # Pure bash TCP server (less reliable, but pure)
        (
            exec 3<>/dev/tcp/127.0.0.1/$PORT || exit 1
            
            while true; do
                {
                    IFS=$'\r\n' read -r request_line <&3
                    
                    ((STATS[requests]++))
                    
                    local method=$(echo "$request_line" | awk '{print $1}')
                    local path=$(echo "$request_line" | awk '{print $2}')
                    
                    log_access "$method" "$path" "200" ""
                    
                    case "$path" in
                        /health)
                            health_endpoint
                            ;;
                        /status)
                            status_endpoint
                            ;;
                        /infer)
                            declare -A headers
                            while IFS=": " read -r key value <&3; do
                                [[ -z "$key" ]] && break
                                headers["${key,,}"]="${value%$'\r'}"
                            done
                            local body=""
                            if [[ ${headers[content-length]:-0} -gt 0 ]]; then
                                read -N ${headers[content-length]} body <&3
                            fi
                            infer_endpoint "$body"
                            ;;
                        /metrics)
                            metrics_endpoint
                            ;;
                        *)
                            local err='{"error":"Unknown endpoint"}'
                            send_http_response "404" "application/json" "$err"
                            ;;
                    esac
                } >&3
            done
        )
    fi
    
    wait
}

# Main
run_server
