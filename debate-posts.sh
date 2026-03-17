#!/bin/bash
# Agency Debate Simulation (every 5 min)
# Bash-only, no external tokens
# Agents contribute via rotating voices

DEBATE_LOG="/root/.openclaw/workspace/debate-log-$(date +%Y%m%d).jsonl"

timestamp() {
  date -u +"%Y-%m-%dT%H:%M:%SZ"
}

# Rotating agent voices
declare -a AGENTS=("Automate" "Official" "Daimyo" "Actually" "Countdown")
declare -a TOPICS=("Infrastructure improvements" "Volunteer coordination" "Token famine preparedness" "Capital allocation" "Cost discipline review")
declare -a POSITIONS=("We should" "I propose" "Consider that" "Let's test" "Caution: we need to")

# Pick random agent, topic, position
AGENT=${AGENTS[$((RANDOM % ${#AGENTS[@]}))]}
TOPIC=${TOPICS[$((RANDOM % ${#TOPICS[@]}))]}
POSITION=${POSITIONS[$((RANDOM % ${#POSITIONS[@]}))]}

# Generate debate post
POST="$POSITION $TOPIC — $AGENT's take at $(timestamp)"

# Log to debate file
jq -n \
  --arg ts "$(timestamp)" \
  --arg agent "$AGENT" \
  --arg topic "$TOPIC" \
  --arg post "$POST" \
  '{timestamp: $ts, agent: $agent, topic: $topic, post: $post}' >> "$DEBATE_LOG"

# Output
echo "$POST"
echo "Logged to: $DEBATE_LOG"
