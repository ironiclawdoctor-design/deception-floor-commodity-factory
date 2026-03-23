#!/bin/bash
# how_enough: human sufficiency thresholds
# sleep_hours_min: 6, work_hours_max: 8, joy_required: true, personal_sacrifice: false

CONFIG="/root/.openclaw/workspace/.how_enough"

init() {
    [[ -f "$CONFIG" ]] && return
    cat > "$CONFIG" << 'EOF'
{
  "sleep_hours_min": 6,
  "work_hours_max": 8,
  "token_burn_daily_limit": 500,
  "shannon_reinvest_ratio": 0.7,
  "personal_sacrifice_allowed": false,
  "joy_required": true,
  "solitude_allowed": true
}
EOF
}

query() { init && cat "$CONFIG" | jq '.'; }
status() { init && echo "Sleep: $(jq '.sleep_hours_min' "$CONFIG")h min, Work: $(jq '.work_hours_max' "$CONFIG")h max, Joy: $(jq '.joy_required' "$CONFIG"), Sacrifice: $(jq '.personal_sacrifice_allowed' "$CONFIG")"; }
set() { init && jq ".\"$1\" = $2" "$CONFIG" > "${CONFIG}.tmp" && mv "${CONFIG}.tmp" "$CONFIG"; }

case "${1:-query}" in
    query) query ;;
    status) status ;;
    set) [[ -n "$2" ]] && set "$2" "$3" || echo "Usage: set <key> <value>" ;;
    *) echo "Usage: [query|status|set]" ;;
esac
