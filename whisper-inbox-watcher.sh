#!/bin/bash
# whisper-inbox-watcher.sh
# Watches /root/human/audio-inbox/ for new audio files, transcribes with whisper.cpp, announces via OpenClaw
# Runs every 5 min via cron. Bash-only. No Python. No approval gate.
# SK-006 — activated 2026-03-27

BINARY="/root/.openclaw/workspace/whisper.cpp/build/bin/whisper-cli"
MODEL="/root/.openclaw/workspace/whisper.cpp/models/ggml-tiny.en.bin"
INBOX="/root/human/audio-inbox"
DONE="/root/human/audio-inbox/.processed"
LOG="/root/human/whisper-last.log"

mkdir -p "$INBOX" "$DONE"

FOUND=0
for f in "$INBOX"/*.wav "$INBOX"/*.mp3 "$INBOX"/*.m4a "$INBOX"/*.ogg "$INBOX"/*.flac; do
  [ -f "$f" ] || continue
  BASENAME=$(basename "$f")
  # Skip already processed
  [ -f "$DONE/$BASENAME.done" ] && continue

  FOUND=1
  echo "[$(date -u +%Y-%m-%dT%H:%M:%SZ)] Transcribing: $BASENAME" | tee "$LOG"

  # Transcribe
  "$BINARY" -m "$MODEL" -f "$f" -otxt 2>>"$LOG"
  TXTFILE="${f}.txt"

  if [ -f "$TXTFILE" ]; then
    TRANSCRIPT=$(cat "$TXTFILE")
    echo "TRANSCRIPT:$BASENAME" >> "$LOG"
    echo "$TRANSCRIPT" >> "$LOG"
    # Mark done
    touch "$DONE/$BASENAME.done"
    # Announce — write to announce channel
    echo "🎙️ Transcript: $BASENAME" > /tmp/whisper-announce.txt
    echo "$TRANSCRIPT" >> /tmp/whisper-announce.txt
    openclaw announce "$(cat /tmp/whisper-announce.txt)" 2>/dev/null || true
  else
    echo "FAILED: no txt output for $BASENAME" >> "$LOG"
  fi
done

[ "$FOUND" -eq 0 ] && exit 0  # Silent on empty inbox — Gideon compliant
