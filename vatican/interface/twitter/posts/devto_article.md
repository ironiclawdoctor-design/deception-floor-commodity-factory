---
title: I built a self-hosted AI agent system for $0/day — here's the proof
published: false
tags: ai, selfhosted, agent, devops
---

## The Problem
Every AI agent setup I found required external API keys, cloud services, or expensive subscriptions.

## The Stack
- **OpenClaw** — agent runtime
- **Telegram** — control surface  
- **SearXNG** — sovereign web search (no API key)
- **Ampere.sh** — ARM hosting (~$20/month)

## The Proof
Running `all.sh` — 12 autonomous steps, zero API keys:

```
openclaw_status   OK
openclaw_doctor   OK
50a_mirror        OK (4394 bytes)
shannon_tank_eps  OK
meritbot          OK
forum_posts       OK
memory            OK
```

## The Doctrine
The agent IS the product. The log IS the pitch deck.
When a stranger asks "How do I get this?" — that's the close.

## The Scripts
All at `/root`: `all.sh`, `next.sh`, `forum.sh`, `api.sh`

Zero external API keys required.
