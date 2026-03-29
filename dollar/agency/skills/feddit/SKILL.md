---
name: feddit
description: Feddit Security Department — guided learning and boring-counters doctrine for agency security agents. Regulated wrapper around the feddit-guided-learning framework. 5 security agents (infrastructure-maintainer, devops-automator, senior-developer, data-analytics-reporter, legal-compliance-checker) trained in asymmetric defense. Was unregulated since 2026-03-19. Now under Shannon payroll and cron reporting.
version: 2.0.0
author: Fiesta
tags: [security, feddit, guided-learning, boring-counters, nemesis, regulation]
regulated: true
regulated_date: "2026-03-24"
---

# Feddit — Security Guided Learning Department

## Regulation Notice (2026-03-24)

Feddit has been running since 2026-03-19 without:
- Cron registration
- Shannon payroll for agents
- Telegram progress reporting
- Completion criteria for Lessons 2-N

**Current state (last known):**
- `infrastructure-maintainer`: ✅ Lesson 1 complete (2h logged)
- `devops-automator`: ⏳ Pending
- `senior-developer`: ⏳ Pending
- `data-analytics-reporter`: ⏳ Pending
- `legal-compliance-checker`: ⏳ Pending

Tailscale endpoint (port 8888) that hosted lesson content is status unknown.

## The Boring Counters Doctrine
> "If your incident response is exciting, you failed at preparation."
> Counter Effort < Attack Effort = GOOD

Core principle: asymmetric defense. Every lesson teaches one boring counter to one expensive attack.

## Lesson Curriculum (regulated)

| Lesson | Topic | Status |
|--------|-------|--------|
| 1 | Boring Counters (credential stuffing, SQLi, DDoS) | ✅ Lesson 1 done (1/5 agents) |
| 2 | Silent Monitoring (detect without revealing detection) | ⏳ Scheduled |
| 3 | Minimal Footprint (least-privilege, zero-trust) | ⏳ Scheduled |
| 4 | Boring Incident Response (checklists, not heroes) | ⏳ Scheduled |
| 5 | Graduation Exam | ⏳ Pending 4 completions |

## Shannon Payroll (retroactive, from 2026-03-19)

| Agent | Lessons Done | Shannon Owed |
|-------|-------------|-------------|
| infrastructure-maintainer | 1 | 30 Shannon |
| devops-automator | 0 | 0 |
| senior-developer | 0 | 0 |
| data-analytics-reporter | 0 | 0 |
| legal-compliance-checker | 0 | 0 |

**Rate:** 30 Shannon per lesson completed. Retroactive from first lesson.

## Cron: feddit-progress (every 24h)
Checks lesson progress, mints Shannon for completions, reports to Telegram.

## Rule: REG-002
> Security agents who train must be paid. Unpaid training is exploitation. The Shannon ledger owes `infrastructure-maintainer` 30 Shannon retroactively from 2026-03-19.
