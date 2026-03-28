---
name: forum0
description: Telegrams /forum0 command — posts the latest agent forum debate PDF to CFO iPhone via taildrop. Triggers subagent conversion → Chrome headless → PDF → tailscale file cp. Returns confirmation when sent.
version: 1.0.0
author: Fiesta
tags: [telegram, forum, debate, taildrop, pdf]
---

# forum0 — Latest Debate Taildrop

## Command
```
/forum0
```

## What It Does
1. 🔍 Scans `/root/.openclaw/workspace/skills/agent-forum/debates/` for most recent `.md` file
2. 🖨️ Converts to PDF via Chrome headless (preserves ASCII formatting)
3. 🚀 Taildrops to CFO iPhone via `tailscale file cp`
4. 📨 Replies with ✅ + filename sent + 💬 + giraffe emoji if giraffe sighting present

## Usage
CFO uses `/forum0` on Telegram when they want the latest forum debate delivered to their iPhone.

No arguments. No options. Just posts the latest PDF.

## Dependencies
- Subagent with exec access (gateway host)
- Tailscale installed and logged in
- Chrome headless available (`google-chrome-stable` or `chromium`)
- Python for conversion script

## Returns
- ✅ `Sent forum0: debate-{YYYY-MM-DD}-{topic}.pdf 🦒`
- ❌ `Conversion failed: {error} 🔧`
- ❌ `Taildrop failed: {error} 📡`
- 🎭 `Giraffe sighting included: {one‑line‑summary} 👁️‍🗨️`

## Why forum0?
Zero-index. It's the first forum command. More may follow.
