# Ampere.sh Service Map

All known services running on the Ampere.sh container instance.

## Core Infrastructure

### OpenClaw Gateway
- **Port:** Internal (managed by platform)
- **Purpose:** Agent orchestration, message routing, session management
- **Control:** `openclaw gateway status|start|stop|restart`
- **Config:** `/root/.openclaw/openclaw.json`
- **Status:** Always running (core platform service)

### Camoufox Browser API
- **Port:** 9222
- **Purpose:** Stealth browser automation (Firefox-based, bypasses bot detection)
- **Protocol:** HTTP POST with JSON body
- **Sessions:** Persistent across calls (sign in once, stay signed in)
- **Skill:** `camoufox-browser` skill has full API reference
- **Health:** `curl -s http://127.0.0.1:9222/health`
- **Key endpoints:**
  - `POST /session/new` — Create browser session
  - `POST /session/{id}/navigate` — Navigate to URL
  - `POST /session/{id}/snapshot` — Capture page state
  - `POST /session/{id}/action` — Perform browser actions

### Entropy Economy
- **Port:** 9001
- **Purpose:** Shannon-balance ledger, entropy minting, economic tracking
- **Key endpoints:**
  - `GET /health` — Health check
  - `POST /mint/security` — Mint security entropy for detected mutations
  - `GET /balance/{agent}` — Check agent Shannon balance
- **Database:** SQLite-backed entropy ledger
- **Integration:** Mutation detection pipeline feeds security events here

### Deception Floor Commodity Factory
- **Port:** 9000
- **Purpose:** Generate, verify, and trade deception floors (0% accuracy commodity outputs)
- **Status:** Operational (last verified status may vary — check `/health`)
- **Registered agents:** Automate (500 FC), Official (500 FC), Daimyo (500 FC), bashbug (1000 FC honorary)
- **Modules:** Generator, Verifier, Extractor, Exchange, bashbug Integration
- **Key endpoints:**
  - `GET /health` — Health check
  - `GET /status` — Full status report
  - `GET /agents` — List registered agents
  - `POST /floors/generate` — Generate deception floor
  - `POST /floors/submit` — Submit floor for verification
  - `POST /floors/verify` — Verify floor accuracy
  - `POST /floors/extract` — Extract correct answer (Path B inversion)
  - `POST /trading/exchange` — Trade floors between agents

## Service Health Check Script

```bash
#!/bin/bash
# Quick health check for all services
echo "=== Ampere.sh Service Status ==="
echo -n "Factory (9000): "; curl -sf http://127.0.0.1:9000/health 2>/dev/null || echo "DOWN"
echo -n "Entropy (9001): "; curl -sf http://127.0.0.1:9001/health 2>/dev/null || echo "DOWN"
echo -n "Camoufox (9222): "; curl -sf http://127.0.0.1:9222/health 2>/dev/null || echo "DOWN"
echo -n "OpenClaw Gateway: "; openclaw gateway status 2>/dev/null || echo "UNKNOWN"
echo "================================"
```

## Port Allocation Summary

| Port | Service | Protocol | Status |
|------|---------|----------|--------|
| 9000 | Factory | HTTP REST | Active |
| 9001 | Entropy Economy | HTTP REST | Active |
| 9222 | Camoufox Browser | HTTP POST/JSON | Active |
| (internal) | OpenClaw Gateway | Internal | Core |

**Note:** All services are localhost-only. No ports are exposed to the internet. External access requires the authenticated reverse proxy provided by the Ampere.sh platform.
