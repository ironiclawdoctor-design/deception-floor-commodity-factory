---
name: agency-proactive
description: Regulated wrapper for the proactive-supervisor and raise-awareness daemons. Replaces freerunning background processes with cron-scheduled, Shannon-accounted, Telegram-reporting checks. Use when: checking agent health, surfacing improvement suggestions, monitoring for anomalies. Was previously unregulated since 2026-03-14.
version: 2.0.0
author: Fiesta
tags: [monitoring, proactive, supervisor, awareness, regulation, shannon]
regulated: true
regulated_date: "2026-03-24"
---

# Agency-Proactive — Regulated Monitoring

## Regulation Notice (2026-03-24)

These daemons ran unregulated from ~2026-03-14 until 2026-03-24:
- `proactive-supervisor.py` — polling every 5 min, calling dead endpoints (port 9000/9001)
- `raise-awareness.py` — polling every 60s, watching memory/logs/scripts for anomalies

**Problems with unregulated state:**
- Calling `http://127.0.0.1:9001` and `http://127.0.0.1:9000` (Entropy/Factory) — both offline
- No Shannon accounting for minting claims
- No Telegram delivery — suggestions wrote to JSON silently
- No cron registration — invisible to agency oversight
- `raise-awareness` checking every 60s = ~1440 checks/day with 0 output

**Fix:** Replace with cron-scheduled agentTurn jobs. Same function. Regulated cadence.

## Regulated Cron Jobs (replacing daemons)

| Old Daemon | New Cron | Interval | Function |
|------------|----------|----------|---------|
| `proactive-supervisor.py` | `agency-proactive-check` | Every 6h | Review cron health, suggest improvements |
| `raise-awareness.py` | `raise-awareness-check` | Every 4h | Anomaly detection, log new files, alert on changes |

## Shannon Accounting
- Each proactive suggestion that gets implemented: +15 Shannon
- Each anomaly correctly flagged: +10 Shannon
- False positives: -2 Shannon (keeps quality high)

## Rule: REG-001
> Any daemon that polls in a loop without cron registration, Telegram delivery, or Shannon accounting is unregulated and must be brought into the regulated stack before it can be trusted.
