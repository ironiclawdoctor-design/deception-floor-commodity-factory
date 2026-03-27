#!/usr/bin/env bash
# trump-append.sh — Total Recall Unreleased Money Printer
# Usage: ./trump-append.sh "description" "release trigger" "value estimate" "agent name"
# SR-024. CFO-authorized. Append-only.

set -euo pipefail

TRUMP_FILE="$(dirname "$0")/TRUMP.md"

if [ "$#" -lt 4 ]; then
  echo "Usage: $0 \"description\" \"release trigger\" \"value estimate\" \"agent name\""
  echo "Example: $0 \"Stripe payout pending\" \"Initiate Stripe transfer\" \"\$42.00\" \"cron-agent\""
  exit 1
fi

DESCRIPTION="$1"
TRIGGER="$2"
VALUE="$3"
AGENT="$4"
TIMESTAMP="$(date -u +%Y-%m-%dT%H:%M:%SZ)"

# Get the next ID by scanning existing T-NNN entries
LAST_ID=$(grep -oP '(?<=\[T-)\d+(?=\])' "$TRUMP_FILE" 2>/dev/null | sort -n | tail -1 || echo "0")
NEXT_ID=$(printf "%03d" $((10#$LAST_ID + 1)))

ENTRY="
### [T-${NEXT_ID}] ${DESCRIPTION}
- **Value:**         ${VALUE}
- **Type:**          Other
- **Status:**        PENDING
- **Recorded By:**   ${AGENT}
- **Recorded At:**   ${TIMESTAMP}
- **Release Trigger:** ${TRIGGER}
- **Notes:**         Appended via trump-append.sh"

# Insert before the APPEND PROTOCOL section
TEMP_FILE="$(mktemp)"
awk -v entry="$ENTRY" '
  /^## APPEND PROTOCOL/ { print entry; print "---"; print "" }
  { print }
' "$TRUMP_FILE" > "$TEMP_FILE"

mv "$TEMP_FILE" "$TRUMP_FILE"

printf '[TRUMP] Entry T-%s appended to TRUMP.md at %s\n' "${NEXT_ID}" "${TIMESTAMP}"
printf '  Description: %s\n' "${DESCRIPTION}"
printf '  Trigger:     %s\n' "${TRIGGER}"
printf '  Value:       %s\n' "${VALUE}"
printf '  Agent:       %s\n' "${AGENT}"
# Note: when passing values with $ signs, use single quotes: './trump-append.sh ... '\''$42.00'\'' ...'
