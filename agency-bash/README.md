# agency-bash

**Tier 0 bash execution server for all agency agents.**

Sandboxed, audited, zero-cost. Every command logged to JSONL.

## Endpoints

| Method | Path     | Description |
|--------|----------|-------------|
| POST   | `/exec`  | Execute a bash command |
| GET    | `/health`| Health check |
| GET    | `/stats` | Today's execution stats |

## Usage

### Execute a command

```bash
curl -s http://127.0.0.1:8484/exec \
  -H "Content-Type: application/json" \
  -d '{"command":"uptime","agent":"fiesta"}'
```

Response:
```json
{
  "ok": true,
  "exitCode": 0,
  "stdout": " 14:30:00 up 1 day...\n",
  "stderr": "",
  "durationMs": 12,
  "truncated": false
}
```

### Parameters

| Field     | Type   | Default  | Description |
|-----------|--------|----------|-------------|
| `command` | string | required | Bash command to execute |
| `agent`   | string | "unknown"| Agent identifier (for audit) |
| `timeout` | number | 10000    | Max execution time (ms, cap 30s) |
| `cwd`     | string | $HOME    | Working directory |

## Security

- **Denylist:** Destructive patterns blocked (rm -rf /, mkfs, fork bombs, etc.)
- **Timeout:** Hard 30s cap, default 10s
- **Output cap:** 500KB per stream (stdout/stderr)
- **Audit:** Every command logged to `logs/agency-bash-YYYY-MM-DD.jsonl`
- **Binding:** localhost only (127.0.0.1)
- **PATH restricted:** Standard system paths only

## Cost

$0.00. Always. This is Tier 0.

## Config

Environment variables:
- `AGENCY_BASH_PORT` — default 8484
- `AGENCY_BASH_HOST` — default 127.0.0.1
- `AGENCY_BASH_LOG_DIR` — default ./logs
