# BitNet Agent — Local LLM for Deception Floor Commodity Factory

BitNet b1.58 2B-4T running on sovereign infrastructure. Ternary weights `{-1, 0, 1}`. Zero-cost inference at ~29 tok/s.

## Querying BitNet

### 1. CLI via `agent.py`

```bash
cd /root/.openclaw/workspace
python3 bitnet-agent/agent.py -q "Your prompt here" -n 200
```

Options:
- `-q` / `--query` — The prompt text (required)
- `-n` / `--max-tokens` — Max tokens to generate (default: 128)
- `-t` / `--temperature` — Sampling temperature (default: 0.7)

### 2. Direct HTTP (curl)

```bash
# Health check
curl -s http://127.0.0.1:8080/health

# Completion request
curl -s http://127.0.0.1:8080/v1/completions \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "Your prompt here",
    "max_tokens": 200,
    "temperature": 0.7
  }'
```

### 3. Server Mode

The inference server runs persistently on `127.0.0.1:8080`. It exposes an OpenAI-compatible API:

- `GET  /health` — Health check
- `POST /v1/completions` — Text completion
- `POST /v1/chat/completions` — Chat completion (if supported)

Start manually if needed:

```bash
cd /root/.openclaw/workspace/bitnet
python3 run_inference_server.py \
  -m models/BitNet-b1.58-2B-4T/ggml-model-i2_s.gguf \
  -t 4 -c 2048 -n 4096 \
  --host 127.0.0.1 --port 8080
```

## Delegation Policy

**All internal tasks route through BitNet first.**

- Fiesta (the main agent) delegates to BitNet for any task that can be handled locally.
- External LLM calls (Claude, etc.) are failover only — used when BitNet cannot handle the task.
- Every external call should generate training data to improve local capability over time.
- The governing principle: *"Over one token famines but far less than a trillion."*

### How Fiesta Delegates

Fiesta spawns BitNet as a subagent via OpenClaw's `sessions_send` mechanism:

1. Main agent identifies a task suitable for local inference
2. Spawns a subagent session with the BitNet persona
3. BitNet agent uses `agent.py` or direct HTTP to query the local model
4. Results auto-announce back to the main agent session

## Log Locations

| Log | Path | Purpose |
|-----|------|---------|
| Keepalive | `bitnet-agent/logs/keepalive.log` | Watchdog health checks & restart events |
| Server | `bitnet-agent/logs/server.log` | Inference server stdout/stderr |
| Queries | `bitnet-agent/logs/queries.log` | Query history (if agent.py logging enabled) |

## Architecture

```
Fiesta (Main Agent)
  └─► BitNet Subagent (this)
        └─► agent.py ──► HTTP ──► BitNet Server (port 8080)
                                    └─► ggml-model-i2_s.gguf
                                         Weights: {-1, 0, 1}
                                         ~29 tok/s local inference
```

## Keepalive

A cron job runs `keepalive.sh` every 5 minutes to ensure the server stays up. The script:

1. Checks `/health` endpoint
2. Restarts the server if unresponsive
3. Waits up to 30s for recovery
4. Logs all events to `keepalive.log`
