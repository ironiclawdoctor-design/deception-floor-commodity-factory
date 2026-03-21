#!/bin/bash
echo "--- [ SALES RED TEAM: INVENTORY ATTACK ] ---"

# Checking @ironiclawdoctor-design/fiesta-movie-reviewer
if [ ! -f "/root/.openclaw/workspace/skills/fiesta-movie-reviewer/LICENSE" ]; then
  echo "FAIL: Movie Reviewer has NO LICENSE. Unsellable."
fi

# Checking the 'It just works' claim
echo "ATTACK: 'It just works' is unfalsifiable. Provide 3 tests cases in README or it's vaporware."

# Checking the 14-day age gate impact
echo "REMEDY: Use the 6-day cooldown to build 'The Proof' (a public terminal recording or live-demo link)."
