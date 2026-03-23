#!/bin/bash
# OpenClaw Gateway auto-restart wrapper
# Kills any existing gateway processes before starting to prevent zombie accumulation

# ─── PID lockfile: ensure only one wrapper instance runs ───
LOCKFILE="/tmp/start-openclaw.lock"
if [ -f "$LOCKFILE" ]; then
  OLDPID=$(cat "$LOCKFILE" 2>/dev/null)
  if [ -n "$OLDPID" ] && kill -0 "$OLDPID" 2>/dev/null; then
    echo "[$(date)] start-openclaw.sh already running (PID $OLDPID), exiting."
    exit 0
  fi
  rm -f "$LOCKFILE"
fi
echo $$ > "$LOCKFILE"
trap 'rm -f "$LOCKFILE"' EXIT

export PATH=/root/go/bin:/usr/local/go/bin:$PATH
export ANTHROPIC_BASE_URL="https://api.ampere.sh"

# Set Node.js heap limit based on container memory.
# OpenClaw 2026.3.11 peaks at ~750MB RSS during startup (plugin init, context window priming).
# On 2GB containers, the default V8 heap limit causes OOM during cold start.
# Detect container memory limit and set max-old-space-size accordingly.
CONTAINER_MEM_MB=$(awk '/^MemTotal/{printf "%d", $2/1024}' /proc/meminfo 2>/dev/null || echo "4096")
if [ "$CONTAINER_MEM_MB" -le 2200 ]; then
  export NODE_OPTIONS="${NODE_OPTIONS:-} --max-old-space-size=1280"
elif [ "$CONTAINER_MEM_MB" -le 4200 ]; then
  export NODE_OPTIONS="${NODE_OPTIONS:-} --max-old-space-size=2560"
fi

# Export env vars from openclaw.json so models.json ${VAR} refs resolve
if [ -f /root/.openclaw/openclaw.json ]; then
  eval $(node -e 'try{const c=JSON.parse(require("fs").readFileSync("/root/.openclaw/openclaw.json","utf8"));Object.entries(c.env||{}).forEach(([k,v])=>console.log("export "+k+"=\""+v+"\""))}catch(e){}' 2>/dev/null)
fi

# Ensure lsof is available (needed for --force)
which lsof > /dev/null 2>&1 || apt-get install -y lsof > /dev/null 2>&1

# Kill any existing openclaw processes first (bracket trick prevents self-match)
pkill -f "[o]penclaw gateway" 2>/dev/null
pkill -f "[o]penclaw-gatewa" 2>/dev/null
sleep 2
# Force kill survivors
pkill -9 -f "[o]penclaw gateway" 2>/dev/null
pkill -9 -f "[o]penclaw-gatewa" 2>/dev/null
sleep 1

# Clean up stale lock files
rm -f /tmp/openclaw-gateway*.lock

MAX_RESTARTS=10
RESTART_COUNT=0
COOLDOWN=5

while true; do
  # Telegram owner-lock: kill stale watchers, re-lock if needed, then start fresh watcher
  pkill -f "[l]ock-telegram" 2>/dev/null
  if [ -f /root/lock-telegram.js ]; then
    node /root/lock-telegram.js --relock 2>/dev/null  # sync re-lock if already locked
    node /root/lock-telegram.js &                      # background watcher for new bots
  fi

  echo "[$(date)] Starting OpenClaw gateway (attempt $((RESTART_COUNT + 1)))..."

  # Kill any stale gateway processes before each restart too
  pkill -f "[o]penclaw gateway" 2>/dev/null
  pkill -f "[o]penclaw-gatewa" 2>/dev/null
  sleep 1
  rm -f /tmp/openclaw-gateway*.lock

  # Use full path to bypass symlink tampering (package dir may be a readonly bind mount)
  if [ -f /usr/lib/node_modules/openclaw/openclaw.mjs ]; then
    node /usr/lib/node_modules/openclaw/openclaw.mjs gateway --force --port 18789 --bind lan
  elif [ -f /usr/lib/node_modules/openclaw/dist/index.js ]; then
    node /usr/lib/node_modules/openclaw/dist/index.js gateway --force --port 18789 --bind lan
  else
    openclaw gateway --force --port 18789 --bind lan
  fi
  EXIT_CODE=$?
  RESTART_COUNT=$((RESTART_COUNT + 1))

  if [ $RESTART_COUNT -ge $MAX_RESTARTS ]; then
    echo "[$(date)] Max restarts ($MAX_RESTARTS) reached. Stopping."
    exit 1
  fi

  echo "[$(date)] Gateway exited with code $EXIT_CODE. Restarting in ${COOLDOWN}s..."
  sleep $COOLDOWN
  COOLDOWN=$((COOLDOWN * 2))
  [ $COOLDOWN -gt 60 ] && COOLDOWN=60
done
