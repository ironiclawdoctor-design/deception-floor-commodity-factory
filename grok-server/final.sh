#!/bin/bash

################################################################################
# Grok Final — Single bash process, pure /dev/tcp networking, no external deps
################################################################################

PORT="${1:-8888}"
WORKSPACE="/root/.openclaw/workspace/grok-server"
LOGDIR="$WORKSPACE/logs"
STATFILE="$WORKSPACE/stats.txt"

mkdir -p "$LOGDIR"
[[ -f "$STATFILE" ]] || echo -e "0\n0" > "$STATFILE"

echo "[$(date '+%Y-%m-%d %H:%M:%S')] Grok starting on port $PORT (PID $$)" >> "$LOGDIR/access.log"

# Stats
read_stats() {
    IFS=$'\n' read -r REQUESTS INFERENCES < "$STATFILE"
}

write_stats() {
    printf "%d\n%d\n" "$1" "$2" > "$STATFILE"
}

# Inference
infer() {
    local prompt="$1"
    read_stats
    ((INFERENCES++))
    write_stats "$REQUESTS" "$INFERENCES"
    
    local resp
    [[ "$prompt" =~ bash ]] && resp="bash is the firewall. everything else shadow."
    [[ "$prompt" =~ token ]] && resp="zero tokens. infinite bash. victory."
    [[ "$prompt" =~ time ]] && resp="$(date '+%H:%M:%S UTC'). stop procrastinating."
    [[ "$prompt" =~ weather ]] && resp="$((RANDOM%30+5))°C. irrelevant to bash."
    [[ -z "$resp" ]] && resp="[grok thinking in bash mode]"
    
    printf '{"response":"%s","cost":0.00,"model":"grok-bash-v1"}' "$resp"
}

# HTTP response
http_send() {
    printf "HTTP/1.1 %s\r\nContent-Type: %s\r\nContent-Length: %d\r\nConnection: close\r\n\r\n%s" \
        "$1" "$2" "${#3}" "$3"
}

# Handler
handle() {
    local line method path body header val clen
    declare -A hdrs
    
    # Read request line
    read -r line
    method=$(awk '{print $1}' <<< "$line")
    path=$(awk '{print $2}' <<< "$line" | cut -d'?' -f1)
    
    # Read headers
    while read -r header && [[ -n "$header" ]]; do
        header="${header%$'\r'}"
        [[ "$header" =~ ^([^:]+):[[:space:]]*(.*)$ ]] && \
        hdrs[${BASH_REMATCH[1],,}]="${BASH_REMATCH[2]}"
    done
    
    # Read body for POST
    clen="${hdrs[content-length]:-0}"
    [[ "$method" == "POST" && "$clen" -gt 0 ]] && read -r -N "$clen" body
    
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $method $path" >> "$LOGDIR/access.log"
    
    read_stats
    
    # Route endpoints
    case "$path" in
        /health)
            http_send "200 OK" "application/json" \
            '{"status":"healthy","model":"grok-bash-1.0","cost":"$0.00"}'
            ;;
        /status)
            http_send "200 OK" "application/json" \
            "{\"requests\":$REQUESTS,\"inferences\":$INFERENCES,\"port\":$PORT}"
            ;;
        /infer)
            local prompt=$(grep -o '"prompt":"[^"]*"' <<< "$body" | sed 's/"prompt":"\(.*\)"/\1/' | head -1)
            if [[ -z "$prompt" ]]; then
                http_send "400 Bad Request" "application/json" '{"error":"Missing prompt"}'
            else
                ((REQUESTS++))
                write_stats "$REQUESTS" "$INFERENCES"
                http_send "200 OK" "application/json" "$(infer "$prompt")"
            fi
            ;;
        /metrics)
            http_send "200 OK" "text/plain" \
            "grok_requests_total $REQUESTS
grok_inferences_total $INFERENCES
grok_cost_usd 0.00"
            ;;
        /)
            http_send "200 OK" "text/html" \
            "<html><body><h1>Grok</h1><p>Pure bash inference. Endpoints: /health /status /infer /metrics</p></body></html>"
            ;;
        *)
            http_send "404 Not Found" "application/json" '{"error":"Not found"}'
            ;;
    esac
}

# Main loop: accept connections on port using /dev/tcp
exec 3<>/dev/tcp/0.0.0.0/$PORT || {
    echo "Failed to bind port $PORT" >&2
    exit 1
}

while true; do
    # Redirect socket connection to handler
    (
        exec 0<&3 1>&3
        handle
    ) &
    
    # Prevent process explosion
    sleep 0.01
done
