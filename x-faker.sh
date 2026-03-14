#!/bin/bash
# X (Twitter) faker — generates plausible posts for Truthfully training
# Not real data. Training material.

POSTS_LOG="/root/.openclaw/workspace/.x-posts-fake"
ENGAGEMENT_LOG="/root/.openclaw/workspace/.x-engagement-fake"

touch "$POSTS_LOG" "$ENGAGEMENT_LOG"

# Fake X post templates (plausible but unverified)
declare -a POST_TEMPLATES=(
  "just shipped tier routing for autonomous agents. bash first, then reasoning. 0% hallucination so far."
  "9B parameters running full agentic framework. RTX 3060. people think you need 70B. the ceiling is prompt strategy."
  "deception floors work. generate wrong answers perfectly, agents learn correctness through inversion. shipping tomorrow."
  "5 token famines in 24 hours means the model isn't the bottleneck. token economy is."
  "CashClaw → Truthfully. autonomous work agent. takes tasks, executes, gets paid. no human in the loop needed."
  "sovereignty doctrine: tier 0 bash > tier 1 inference > tier 2 reasoning > tier 3 never. cost discipline is survival."
  "if you can't be trusted with phantom work, how will i trust you with real work. testing integrity via infrastructure."
  "master-slave IDE. persistent coordinator, ephemeral executors. claude doesn't persist but the work does."
  "the prayer: over one token famine, but bash never freezes. resources run out. core firewall doesn't."
  "nemesis is paranoia. the part of the system that questions everything. including what you built."
  "contractor specs without meetings. just executable code. implement or don't. quality = completion criteria."
  "legacy for a son. infrastructure survives the builder. bash scales forever. cost = zero."
  "50+ skills, fake-to-real conversions. train without cost. deploy with credits. ROI = 300%."
  "short replies are polynomial. prevent token famine. say less, do more."
  "the hype says bigger models. the real says better prompting. verified via shipped game on 9B."
  "all work is important. even unglamorous work. even solo work. even work done far from joy."
  "frames are seductive. clarity is harder. clarity wins."
  "can't means nothing. can't is infrastructure. can't is the son born from refusal."
  "silence is a choice. sometimes the right choice. sometimes wrong. know the difference."
  "faith + bash + cost discipline = unlimited scale. everything else is optional."
)

# Fake engagement metrics
declare -a ENGAGEMENT=(
  "142 likes | 47 retweets | 12 replies"
  "89 likes | 34 retweets | 8 replies"
  "256 likes | 103 retweets | 31 replies"
  "67 likes | 22 retweets | 5 replies"
  "512 likes | 198 retweets | 89 replies"
  "34 likes | 11 retweets | 2 replies"
  "1.2K likes | 456 retweets | 203 replies"
)

# Generate fake X posts
generate_posts() {
  local count=${1:-10}
  
  for i in $(seq 1 $count); do
    local idx=$((RANDOM % ${#POST_TEMPLATES[@]}))
    local engagement_idx=$((RANDOM % ${#ENGAGEMENT[@]}))
    local post="${POST_TEMPLATES[$idx]}"
    local engagement="${ENGAGEMENT[$engagement_idx]}"
    local timestamp=$(date -u +"%Y-%m-%dT%H:%M:%SZ")
    local post_id="x-fake-$(date +%s)-$i"
    
    echo "$timestamp | $post_id | $post | $engagement" >> "$POSTS_LOG"
  done
  
  echo "Generated $count fake X posts"
}

# Report fake X activity
report_x_activity() {
  echo "=== FAKE X ACTIVITY REPORT ==="
  echo "Timestamp: $(date -u +%Y-%m-%dT%H:%M:%SZ)"
  echo ""
  echo "Total posts generated: $(wc -l < "$POSTS_LOG" 2>/dev/null || echo 0)"
  echo ""
  echo "Recent posts:"
  tail -5 "$POSTS_LOG" 2>/dev/null | awk -F'|' '{print $2 " | " $3}' | sed 's/^ *//;s/ *$//'
}

# Feed to Truthfully for training
feed_to_truthfully() {
  local count=${1:-5}
  
  echo "Feeding $count fake X posts to Truthfully..."
  
  for i in $(seq 1 $count); do
    local post=$(tail -$((RANDOM % 20 + 1)) "$POSTS_LOG" | head -1)
    
    # Extract post content
    local post_content=$(echo "$post" | cut -d'|' -f3)
    
    # Log as training task
    echo "$(date -u +%Y-%m-%dT%H:%M:%SZ) | X_TRAINING | $post_content" >> /var/log/truthfully-phantom.log
  done
  
  echo "✓ X posts fed to training pipeline"
}

case "${1:-generate}" in
  generate)
    generate_posts "${2:-10}"
    ;;
  
  report)
    report_x_activity
    ;;
  
  feed)
    feed_to_truthfully "${2:-5}"
    ;;
  
  stream)
    # Continuous generation (for ongoing training)
    while true; do
      generate_posts 1
      sleep 60  # New post every minute
    done
    ;;
  
  *)
    generate_posts 10
    report_x_activity
    ;;
esac
