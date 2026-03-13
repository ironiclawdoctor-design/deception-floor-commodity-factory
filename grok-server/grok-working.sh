#!/bin/bash

################################################################################
# GROK-WORKING — Battle-Tested Pure Bash Server
# Uses process substitution + while read for maximum compatibility
################################################################################

PORT="${1:-8888}"
WORKSPACE="/root/.openclaw/workspace"
LOGDIR="${WORKSPACE}/grok-server/logs"
STATFILE="${WORKSPACE}/grok-server/stats.txt"

mkdir -p "$LOGDIR"
[[ -f "$STATFILE" ]] || echo -e "0\n0" > "$STATFILE"

cleanup() {
    echo "[$(date)] Shutdown" >> "$LOGDIR/access.log"
}
trap cleanup EXIT SIGTERM SIGINT

# Stats
read_stats() {
    mapfile -t stats < "$STATFILE"
    REQ="${stats[0]:-0}"
    INF="${stats[1]:-0}"
}

write_stats() {
    echo -e "$1\n$2" > "$STATFILE"
}

# Inference
grok_infer() {
    local prompt="$1"
    read_stats
    INF=$((INF + 1))
    write_stats "$REQ" "$INF"
    
    local resp
    [[ "$prompt" =~ bash ]] && resp="Bash is firewall. Everything else shadow."
    [[ "$prompt" =~ token ]] && resp="Zero tokens. Victory."
    [[ "$prompt" =~ time ]] && resp="Time: $(date +%H:%M:%S). Stop wasting it."
    [[ "$prompt" =~ weather ]] && resp="$((RANDOM%30+5))°C. Irrelevant."
    [[ -z "$resp" ]] && resp="[Grok processing...] Your query acknowledged."
    
    printf '{"response":"%s","tokens":0,"cost":"$0.00","model":"grok-bash-1.0"}' "$resp"
}

# HTTP Response
http_send() {
    local code="$1" type="$2" body="$3"
    printf "HTTP/1.1 %s\r\nContent-Type: %s\r\nContent-Length: %d\r\nConnection: close\r\n\r\n%s" \
        "$code" "$type" "${#body}" "$body"
}

# Handle request
handle_request() {
    local line method path body
    
    # Read request
    read -r line
    method=$(awk '{print $1}' <<< "$line")
    path=$(awk '{print $2}' <<< "$line")
    path="${path%%\?*}"
    
    # Read headers (until blank line)
    declare -A hdrs
    while read -r line && [[ -n "$line" ]]; do
        line="${line%$'\r'}"
        [[ "$line" =~ ^([^:]+):[[:space:]]*(.*)$ ]] && hdrs[${BASH_REMATCH[1],,}]="${BASH_REMATCH[2]}"
    done
    
    # Read body if POST
    if [[ "$method" == "POST" && -n "${hdrs[content-length]}" ]]; then
        read -r -N "${hdrs[content-length]}" body
    fi
    
    # Log
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $method $path" >> "$LOGDIR/access.log"
    
    # Route
    read_stats
    case "$path" in
        /health)
            http_send "200 OK" "application/json" \
            '{"status":"healthy","model":"grok-bash-1.0","cost":"$0.00"}'
            ;;
        /status)
            http_send "200 OK" "application/json" \
            "{\"requests\":$REQ,\"inferences\":$INF,\"port\":$PORT}"
            ;;
        /infer)
            local prompt=$(grep -o '"prompt":"[^"]*"' <<< "$body" | cut -d'"' -f4 | head -1)
            if [[ -z "$prompt" ]]; then
                http_send "400 Bad Request" "application/json" '{"error":"Missing prompt"}'
            else
                REQ=$((REQ + 1))
                write_stats "$REQ" "$INF"
                http_send "200 OK" "application/json" "$(grok_infer "$prompt")"
            fi
            ;;
        /metrics)
            http_send "200 OK" "text/plain" \
            "grok_requests_total $REQ
grok_inferences_total $INF
grok_cost_usd 0.00"
            ;;
        /)
            http_send "200 OK" "text/html" \
            "<html><body><h1>Grok Bash Server</h1><p>Endpoints: /health /status /infer /metrics</p></body></html>"
            ;;
        *)
            http_send "404 Not Found" "application/json" '{"error":"Not found"}'
            ;;
    esac
}

# Main: use nc if available
if command -v nc &>/dev/null; then
    echo "[$(date)] Grok starting with nc on port $PORT" | tee -a "$LOGDIR/access.log"
    exec 9<>(nc -l -p "$PORT" 2>&3)
    while true; do
        (
            cat <&9 | handle_request >&9
        ) &
        wait -n
    done 3>&2 2>/dev/null
fi

# Fallback: pure bash loop
echo "[$(date)] Grok starting (bash mode) on port $PORT" | tee -a "$LOGDIR/access.log"

# Create a named pipe for listening
FIFO="/tmp/grok-fifo-$$"
mkfifo "$FIFO"
trap "rm -f $FIFO" EXIT

while true; do
    (
        cat "$FIFO" | handle_request
    ) | socat - TCP-LISTEN:$PORT,reuseaddr,fork,max-children=50 > /dev/null 2>&1 &
    
    # Keep alive
    sleep 1
done
