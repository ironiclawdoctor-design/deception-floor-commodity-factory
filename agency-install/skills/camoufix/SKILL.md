---
name: camoufix
description: Camoufox browser orchestration with merged authentication. Handles token from /data/browser-server-token, merges into all requests as ?token= param. Wraps all browser actions with fixer resilience layer (retry, backoff, error classification). Use for stealth browser automation past bot detection.
version: 1.0.0
author: Fiesta
tags: [browser, camoufox, stealth, automation, firefox, auth]
---

# Camoufix — Authenticated Camoufox Orchestrator

## Auth Pattern (MERGED)
Token lives at `/data/browser-server-token`.
All requests: `http://127.0.0.1:9222/<action>?token=<TOKEN>`
Never pass in header. Always as query param.

## Usage
```python
from skills.camoufix.client import CamoufoxClient

cf = CamoufoxClient()  # auto-loads token
page = cf.navigate("https://hashnode.com/new")
cf.type("#title-input", "My Article Title")
cf.click("button[type=submit]")
```

## Actions
- navigate(url) → load page, return HTML
- click(selector) → click element
- type(selector, text) → type into field
- screenshot() → base64 PNG
- extract(selector) → get text content
- evaluate(js) → run JavaScript
- session_new() → fresh session
- session_persist() → save cookies to disk
