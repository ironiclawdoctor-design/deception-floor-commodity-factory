#!/bin/bash
# silence.sh — Log what all nations do next by asking them to shut up first

SILENCE_LOG="/var/log/silence.log"
ACTION_LOG="/var/log/actions.log"

touch "$SILENCE_LOG" "$ACTION_LOG"

# Ask all agents to silence
silence_all() {
  echo "$(date -u +%Y-%m-%dT%H:%M:%SZ) | SILENCE COMMAND ISSUED" >> "$SILENCE_LOG"
  
  # Send silence to each branch
  for agent in Automate Official Daimyo Augment Nemesis Truthfully; do
    echo "$(date -u +%Y-%m-%dT%H:%M:%SZ) | SILENCED | $agent" >> "$SILENCE_LOG"
  done
  
  echo "✓ All nations silenced"
}

# Ask what they do next
ask_action() {
  local timestamp=$(date -u +%Y-%m-%dT%H:%M:%SZ)
  echo "$timestamp | QUESTION: What are you doing next?" >> "$ACTION_LOG"
  
  # In silence, agents move
  echo "$(date -u +%Y-%m-%dT%H:%M:%SZ) | ACTION | Agents decide without words" >> "$ACTION_LOG"
}

# Log the silence
log_silence() {
  silence_all
  ask_action
  
  echo ""
  echo "Silence issued."
  echo "Nations deciding."
  tail -5 "$ACTION_LOG"
}

log_silence
