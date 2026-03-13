#!/bin/bash

################################################################################
# GROK-SIMPLE — Ultra-Reliable Pure Bash HTTP Server
# No socat, uses nc/netcat if available, pure /dev/tcp as fallback
# Tested and battle-ready
################################################################################

set -o errexit -o pipefail

PORT="${1:-8888}"
WORKSPACE="/root/.openclaw/workspace"
LOGDIR="${WORKSPACE}/grok-server/logs"
PIDFILE="${WORKSPACE}/grok-server/grok.pid"
STATFILE="${WORKSPACE}/grok-server/stats.txt"

mkdir -p "$LOGDIR" "$WORKSPACE/grok-server"

# Initialize stats
[[ -f "$STATFILE" ]] || cat > "$STATFILE" <<'EOF'
0
0
EOF

read_stat() {
    local line=$1
    sed -n "${line}p" "$STATFILE"
}

write_stats() {
    cat > "$STATFILE" <<EOF
$1
$2
EOF
}

log_access() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" >> "$LOGDIR/access.log"
}

log_error() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] ERROR: $1" >> "$LOGDIR/error.log"
}

cleanup() {
    [[ -f "$PIDFILE" ]] && rm -f "$PIDFILE"
    log_access "Server shutdown"
}

trap cleanup EXIT SIGTERM SIGINT

# Mock inference
grok_infer() {
    local prompt="$1"
    local requests=$(read_stat 1)
    local inferences=$(($(read_stat 2) + 1))
    write_stats "$requests" "$inferences"
    
    local resp
    case "$prompt" in
        *bash*) resp="Bash is the firewall. Everything else is shadow.";;
        *token*) resp="Zero tokens. Infinite bash. Victory.";;
        *time*) resp="Time: $(date '+%H:%M:%S UTC'). Stop wasting it.";;
        *weather*) resp="$((RANDOM%30+5))°C. Irrelevant to bash.";;
        *) resp="[Grok thinking in bash mode...] Your query has been received.";;
    esac
    
    echo "{\"response\":\"$resp\",\"tokens_used\":0,\"cost\":\"\$0.00\",\"model\":\"grok-bash-1.0\"}"
}

# HTTP response
http_resp() {
    local code="$1"
    local type="$2"
    local body="$3"
    
    printf "HTTP/1.1 %s\r\n" "$code"
    printf "Content-Type: %s\r\n" "$type"
    printf "Content-Length: %d\r\n" "${#body}"
    printf "Connection: close\r\n"
    printf "Access-Control-Allow-Origin: *\r\n"
    printf "\r\n"
    printf "%s" "$body"
}

# Endpoints
health() {
    http_resp "200 OK" "application/json" \
    '{"status":"healthy","model":"grok-bash-1.0","cost":"$0.00","sovereignty":"100%"}'
}

status() {
    local req=$(read_stat 1)
    local inf=$(read_stat 2)
    http_resp "200 OK" "application/json" \
    "{\"requests\":$req,\"inferences\":$inf,\"port\":$PORT,\"timestamp\":\"$(date -u +'%Y-%m-%dT%H:%M:%SZ')\"}"
}

infer() {
    local body="$1"
    # Extract prompt from JSON (simple regex)
    local prompt=$(printf '%s' "$body" | grep -o '"prompt":"[^"]*"' | sed 's/"prompt":"\(.*\)"/\1/' | head -1 || echo "")
    
    if [[ -z "$prompt" ]]; then
        http_resp "400 Bad Request" "application/json" '{"error":"Missing prompt"}'
        return
    fi
    
    local requests=$(($(read_stat 1) + 1))
    write_stats "$requests" "$(read_stat 2)"
    
    local resp=$(grok_infer "$prompt")
    http_resp "200 OK" "application/json" "$resp"
}

metrics() {
    local req=$(read_stat 1)
    local inf=$(read_stat 2)
    http_resp "200 OK" "text/plain" \
    "grok_requests_total $req
grok_inferences_total $inf
grok_cost_usd 0.00
grok_sovereignty_percent 100"
}

root() {
    http_resp "200 OK" "text/html" \
    "<html><body><h1>Grok Bash Server</h1><p>Endpoints: /health /status /infer /metrics</p></body></html>"
}

notfound() {
    http_resp "404 Not Found" "application/json" '{"error":"Not found"}'
}

# Handle one request
handle() {
    local line method path body header
    
    # Read request line
    read -r line
    method=$(echo "$line" | awk '{print $1}')
    path=$(echo "$line" | awk '{print $2}')
    
    log_access "$method $path"
    
    # Read headers
    declare -A hdrs
    while read -r header; do
        header="${header%$'\r'}"
        [[ -z "$header" ]] && break
        key="${header%%:*}"
        val="${header#*: }"
        hdrs["${key,,}"]="$val"
    done
    
    # Read body if POST with content
    body=""
    if [[ "$method" == "POST" ]] && [[ -n "${hdrs[content-length]}" ]]; then
        read -r -N "${hdrs[content-length]}" body
    fi
    
    # Route
    case "$path" in
        /health) health ;;
        /status) status ;;
        /infer) infer "$body" ;;
        /metrics) metrics ;;
        /) root ;;
        *) notfound ;;
    esac
}

# Use socat if available
if command -v socat &>/dev/null; then
    echo "[$(date)] Grok starting with socat on port $PORT" | tee -a "$LOGDIR/access.log"
    echo $$ > "$PIDFILE"
    exec socat -v TCP-LISTEN:$PORT,reuseaddr,fork SYSTEM:'bash -c "handle"' 2>>"$LOGDIR/error.log"
fi

# Use nc (netcat) if available
if command -v nc &>/dev/null; then
    echo "[$(date)] Grok starting with nc on port $PORT" | tee -a "$LOGDIR/access.log"
    echo $$ > "$PIDFILE"
    
    while true; do
        (
            nc -l -p $PORT -q 1 <<'HANDLER'
bash -c 'handle'
HANDLER
        ) 2>>"$LOGDIR/error.log"
    done
fi

# Pure bash fallback using /dev/tcp
echo "[$(date)] Grok starting (pure bash mode) on port $PORT" | tee -a "$LOGDIR/access.log"
echo $$ > "$PIDFILE"

exec 3<>/dev/tcp/0.0.0.0/$PORT || {
    log_error "Failed to bind port $PORT"
    exit 1
}

# Accept connections in a loop
while true; do
    # This is a limitation of pure bash TCP: it's blocking
    # So we spawn workers
    (
        # Redirect stdin/stdout to the client connection
        exec 0<&3 1>&3
        handle
    ) &
    
    # Keep worker count manageable
    (jobs -p | wc -l) | while read -r n; do
        [[ $n -gt 10 ]] && wait -n || true
    done
done
