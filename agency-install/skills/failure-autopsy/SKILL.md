---
name: failure-autopsy
description: Auto-research root causes on all agency failures. Every exec error, API rejection, auth failure, and timeout triggers this. Classifies failure, extracts root cause, writes to agency.db, logs confession, proposes fix. Zero human input required. Triggered automatically when failure is detected.
version: 1.0.0
author: Fiesta
tags: [debugging, root-cause, autopsy, resilience, auto-research]
---

# Failure Autopsy — Auto Root Cause Engine

## Trigger
Any failure in: exec, API call, publish, deploy, auth, cron

## Root Cause Tree

```
FAILURE
├── AUTH (401/403)
│   ├── Missing header → add Authorization: Bearer <token>
│   ├── Wrong format → check Bearer vs Basic vs query param
│   ├── Expired token → refresh via /token endpoint
│   └── Missing scope → enable in console / re-auth
├── SCHEMA (400/422)
│   ├── Wrong field name → check API docs
│   ├── Missing required field → add with default
│   └── Wrong type → cast before send
├── NOT_FOUND (404)
│   ├── Wrong endpoint → check API version
│   ├── Resource deleted → recreate
│   └── Wrong method (GET vs POST) → check docs
├── NETWORK
│   ├── Bot detection → use Camoufox / residential IP
│   ├── Port blocked → Ampere proxy restriction
│   ├── Timeout → increase timeout, retry with backoff
│   └── DNS → check URL spelling
├── PLATFORM
│   ├── Ampere port firewall → use Cloud Run / OpenWrt DDNS
│   ├── Approval timeout → pre-approve command class
│   └── PEP 668 (pip) → add --break-system-packages
└── LOGIC
    ├── Wrong column name → .schema query first
    ├── Cap exceeded → increase backing
    └── Index mismatch → use 0-index discipline
```

## Auto-fix Protocol
1. Detect failure type from error message
2. Match to root cause tree
3. Apply fix automatically if tier-0 (file/SQLite)
4. Log confession with doctrine extracted
5. Surface job ID if exec approval needed
6. Never repeat same fix twice (idempotency store)

## Usage
```python
from skills.failure_autopsy.core import autopsy
autopsy(error="401 Unauthorized", context="Camoufox /health")
# → Root cause: Missing auth token as query param
# → Fix: TOKEN=$(cat /data/browser-server-token); curl ?token=$TOKEN
# → Logged to confessions
```
