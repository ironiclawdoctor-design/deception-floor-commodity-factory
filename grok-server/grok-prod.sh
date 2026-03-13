#!/bin/bash

################################################################################
# GROK-PROD — Production Ready Server using socat + pure bash logic
################################################################################

PORT="${1:-8888}"
WORKSPACE="/root/.openclaw/workspace/grok-server"
LOGDIR="$WORKSPACE/logs"
STATFILE="$WORKSPACE/stats.txt"

mkdir -p "$LOGDIR"
[[ -f "$STATFILE" ]] || echo -e "0\n0" > "$STATFILE"

# Cleanup
cleanup() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] Server shutdown" >> "$LOGDIR/access.log"
}
trap cleanup EXIT SIGTERM SIGINT

# Read stats
read_stats() {
    mapfile -t stats < "$STATFILE" 2>/dev/null
    REQUESTS="${stats[0]:-0}"
    INFERENCES="${stats[1]:-0}"
}

# Write stats
write_stats() {
    printf "%d\n%d\n" "$1" "$2" > "$STATFILE"
}

# Log request
log_req() {
    printf "[%s] %s %s\n" "$(date '+%Y-%m-%d %H:%M:%S')" "$1" "$2" >> "$LOGDIR/access.log"
}

# Inference engine
infer() {
    local prompt="$1"
    
    # Update stats
    read_stats
    INFERENCES=$((INFERENCES + 1))
    write_stats "$REQUESTS" "$INFERENCES"
    
    # Pattern-based response
    local response
    case "$prompt" in
        *bash*) response="bash is the firewall between order and void." ;;
        *token*) response="Zero cost. Pure bash sovereignty." ;;
        *time*) response="Current: $(date +%H:%M:%S UTC). Stop procrastinating." ;;
        *weather*) response="$((RANDOM % 30 + 5))°C outside. Irrelevant to computation." ;;
        *why*) response="42. Next question?" ;;
        *) response="[Grok thinking in bash mode...] Your query has been received." ;;
    esac
    
    printf '{"response":"%s","tokens_used":0,"cost":0.00,"model":"grok-bash-v1"}' "$response"
}

# Handler function (called by socat)
handle_request() {
    local request_line method path http_ver
    local header body content_length
    declare -A headers
    
    # Read request line
    IFS=$'\r\n' read -r request_line
    
    # Parse request
    method=$(echo "$request_line" | awk '{print $1}')
    path=$(echo "$request_line" | awk '{print $2}' | cut -d'?' -f1)
    http_ver=$(echo "$request_line" | awk '{print $3}')
    
    # Read headers
    while IFS=': ' read -r key value; do
        value="${value%$'\r'}"
        [[ -z "$key" ]] && break
        key_lower=$(echo "$key" | tr '[:upper:]' '[:lower:]')
        headers[$key_lower]="$value"
    done
    
    # Read body if POST
    body=""
    content_length="${headers[content-length]:-0}"
    if [[ "$method" == "POST" && "$content_length" -gt 0 ]]; then
        read -r -N "$content_length" body
    fi
    
    # Log request
    log_req "$method" "$path"
    
    # Process request
    read_stats
    local response_body response_code response_type
    
    case "$path" in
        /health)
            response_code="200 OK"
            response_type="application/json"
            response_body='{"status":"healthy","model":"grok-bash-v1","cost":"$0.00","sovereignty":"100%"}'
            ;;
        /status)
            response_code="200 OK"
            response_type="application/json"
            response_body="{\"requests\":$REQUESTS,\"inferences\":$INFERENCES,\"port\":$PORT,\"timestamp\":\"$(date -u +'%Y-%m-%dT%H:%M:%SZ')\"}"
            ;;
        /infer)
            # Extract prompt from JSON body
            local prompt=$(echo "$body" | grep -o '"prompt":"[^"]*"' | sed 's/"prompt":"\(.*\)"/\1/' | head -1)
            
            if [[ -z "$prompt" ]]; then
                response_code="400 Bad Request"
                response_type="application/json"
                response_body='{"error":"Missing prompt field"}'
            else
                response_code="200 OK"
                response_type="application/json"
                
                # Increment requests
                REQUESTS=$((REQUESTS + 1))
                write_stats "$REQUESTS" "$INFERENCES"
                
                # Run inference
                response_body=$(infer "$prompt")
            fi
            ;;
        /metrics)
            response_code="200 OK"
            response_type="text/plain"
            response_body="grok_requests_total $REQUESTS
grok_inferences_total $INFERENCES
grok_cost_usd 0.00
grok_sovereignty_percent 100"
            ;;
        /)
            response_code="200 OK"
            response_type="text/html"
            response_body="<html><head><title>Grok Bash Server</title></head><body><h1>⚡ Grok</h1><p>Pure bash inference server. Cost: \$0.00</p><h2>API</h2><ul><li>GET /health</li><li>GET /status</li><li>POST /infer (JSON: {\"prompt\": \"...\"})</li><li>GET /metrics</li></ul></body></html>"
            ;;
        *)
            response_code="404 Not Found"
            response_type="application/json"
            response_body='{"error":"Endpoint not found"}'
            ;;
    esac
    
    # Send HTTP response
    response_length=${#response_body}
    
    printf "HTTP/1.1 %s\r\n" "$response_code"
    printf "Content-Type: %s\r\n" "$response_type"
    printf "Content-Length: %d\r\n" "$response_length"
    printf "Connection: close\r\n"
    printf "Access-Control-Allow-Origin: *\r\n"
    printf "Date: %s\r\n" "$(date -R)"
    printf "\r\n"
    printf "%s" "$response_body"
}

# Export function for socat
export -f handle_request read_stats write_stats log_req infer

# Start server with socat
echo "[$(date '+%Y-%m-%d %H:%M:%S')] Starting Grok on port $PORT" | tee -a "$LOGDIR/access.log"

# Use socat to listen and fork
socat -d TCP-LISTEN:$PORT,reuseaddr,fork SYSTEM:'bash -c "handle_request"' 2>> "$LOGDIR/error.log"
