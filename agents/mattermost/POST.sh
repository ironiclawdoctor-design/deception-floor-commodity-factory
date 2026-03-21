#!/bin/bash
# MATTERMOST_POST (Vendpoint)
# Uses Inbound Webhooks to post to a channel.
URL="$MATTERMOST_WEBHOOK_URL"
TEXT="$1"

if [ -z "$URL" ]; then
  echo "Error: MATTERMOST_WEBHOOK_URL not set in secrets."
  exit 1
fi

curl -i -X POST -H 'Content-Type: application/json' \
     -d "{\"text\": \"$TEXT\"}" "$URL"
