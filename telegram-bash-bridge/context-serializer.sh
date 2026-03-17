#!/bin/bash
# Output compacted bash-only context (no explanatory text)

USER_ID=${1:-"unknown"}
COMMAND=${2:-""}
RESULT_JSON=${3:-"{}"}

# Parse JSON result
EXIT_CODE=$(echo "$RESULT_JSON" | jq -r '.exit_code // "1"')
STDOUT=$(echo "$RESULT_JSON" | jq -r '.stdout // ""' | head -c 512)
STDERR=$(echo "$RESULT_JSON" | jq -r '.stderr // ""' | head -c 512)

# Output compacted format
printf "%s|%s|%s|%s|%s\n" \
  "$(date +%s)" \
  "$USER_ID" \
  "$COMMAND" \
  "$EXIT_CODE" \
  "$(echo -n "$STDOUT" | base64 -w0)"

# Stderr logged separately if present
if [ -n "$STDERR" ]; then
  printf "ERR|%s|%s\n" "$USER_ID" "$(echo -n "$STDERR" | base64 -w0)" >&2
fi
