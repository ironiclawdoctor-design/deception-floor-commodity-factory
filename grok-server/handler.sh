#!/bin/bash

# Grok request handler for nc
# Called by: nc -l -p PORT < some_fifo | handler.sh | nc -l -p PORT > output_fifo

WORKSPACE="/root/.openclaw/workspace/grok-server"
STATFILE="$WORKSPACE/stats.txt"

[[ -f "$STATFILE" ]] || echo -e "0\n0" > "$STATFILE"

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

# Inference
infer() {
    local prompt="$1"
    
    read_stats
    INFERENCES=$((INFERENCES + 1))
    write_stats "$REQUESTS" "$INFERENCES"
    
    local response
    [[ "$prompt" =~ bash ]] && response="bash is the firewall."
    [[ "$prompt" =~ token ]] && response="Zero tokens. Victory."
    [[ "$prompt" =~ time ]] && response="$(date +%H:%M:%S UTC). Stop wasting it."
    [[ "$prompt" =~ weather ]] && response="$((RANDOM % 30 + 5))°C. Irrelevant."
    [[ -z "$response" ]] && response="[Grok thinking...] Query received."
    
    printf '{"response":"%s","cost":0}' "$response"
}

# HTTP Response
http_resp() {
    local code="$1" type="$2" body="$3"
    
    printf "HTTP/1.1 %s\r\n" "$code"
    printf "Content-Type: %s\r\n" "$type"
    printf "Content-Length: %d\r\n" "${#body}"
    printf "Connection: close\r\n"
    printf "\r\n"
    printf "%s" "$body"
}

# Main handler
main() {
    local request_line method path
    declare -A headers
    local body content_len
    
    # Read request
    read -r request_line
    method=$(echo "$request_line" | awk '{print $1}')
    path=$(echo "$request_line" | awk '{print $2}' | cut -d'?' -f1)
    
    # Read headers
    while IFS=': ' read -r key value; do
        value="${value%$'\r'}"
        [[ -z "$key" ]] && break
        headers["${key,,}"]="$value"
    done
    
    # Read body if POST
    body=""
    if [[ "$method" == "POST" && -n "${headers[content-length]}" ]]; then
        read -r -N "${headers[content-length]}" body
    fi
    
    # Route
    read_stats
    case "$path" in
        /health)
            http_resp "200 OK" "application/json" \
            '{"status":"healthy","model":"grok-bash","cost":"$0.00"}'
            ;;
        /status)
            http_resp "200 OK" "application/json" \
            "{\"requests\":$REQUESTS,\"inferences\":$INFERENCES}"
            ;;
        /infer)
            local prompt=$(grep -o '"prompt":"[^"]*"' <<< "$body" | sed 's/"prompt":"\(.*\)"/\1/' | head -1)
            [[ -z "$prompt" ]] && http_resp "400 Bad" "application/json" '{"error":"No prompt"}' && return
            
            REQUESTS=$((REQUESTS + 1))
            write_stats "$REQUESTS" "$INFERENCES"
            
            http_resp "200 OK" "application/json" "$(infer "$prompt")"
            ;;
        /)
            http_resp "200 OK" "text/html" \
            "<html><body><h1>Grok Bash Server</h1><p>Endpoints: /health /status /infer</p></body></html>"
            ;;
        *)
            http_resp "404 Not Found" "application/json" '{"error":"Not found"}'
            ;;
    esac
}

main
