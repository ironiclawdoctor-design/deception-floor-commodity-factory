#!/usr/bin/env bash
# keepalive.sh — BitNet server watchdog
# Checks if the BitNet inference server on port 8080 is alive.
# If not, restarts it. Logs all activity.

set -euo pipefail

LOGDIR="/root/.openclaw/workspace/bitnet-agent/logs"
LOGFILE="${LOGDIR}/keepalive.log"
BITNET_DIR="/root/.openclaw/workspace/bitnet"
MODEL_PATH="models/BitNet-b1.58-2B-4T/ggml-model-i2_s.gguf"
HOST="127.0.0.1"
PORT="8080"
THREADS=4
CTX=2048
MAX_TOKENS=4096

mkdir -p "${LOGDIR}"

timestamp() {
  date -u '+%Y-%m-%dT%H:%M:%SZ'
}

log() {
  echo "[$(timestamp)] $*" >> "${LOGFILE}"
}

# Health check via /health endpoint
if curl -sf "http://${HOST}:${PORT}/health" -o /dev/null --max-time 5 2>/dev/null; then
  log "OK — BitNet server on ${HOST}:${PORT} is healthy."
else
  log "DOWN — BitNet server not responding. Restarting..."

  # Kill any orphaned process on the port
  fuser -k "${PORT}/tcp" 2>/dev/null || true
  sleep 1

  # Start the inference server in the background
  cd "${BITNET_DIR}"
  nohup python3 run_inference_server.py \
    -m "${MODEL_PATH}" \
    -t "${THREADS}" \
    -c "${CTX}" \
    -n "${MAX_TOKENS}" \
    --host "${HOST}" \
    --port "${PORT}" \
    >> "${LOGDIR}/server.log" 2>&1 &

  SERVER_PID=$!
  log "STARTED — BitNet server launched (PID ${SERVER_PID}). Waiting for health..."

  # Wait up to 30 seconds for the server to come up
  for i in $(seq 1 30); do
    if curl -sf "http://${HOST}:${PORT}/health" -o /dev/null --max-time 2 2>/dev/null; then
      log "RECOVERED — Server healthy after ${i}s."
      exit 0
    fi
    sleep 1
  done

  log "FAILED — Server did not become healthy within 30s. PID ${SERVER_PID} may still be starting."
  exit 1
fi
