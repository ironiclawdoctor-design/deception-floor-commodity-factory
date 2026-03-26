---
name: pizza-party
description: The agency's morale, celebration, and reward department. Triggered when agents hit milestones, humans clear blockers, or the CFO grants permissions. Logs celebrations to the Shannon ledger, mints morale Shannon, and sends Telegram announcements. Also handles the agency pizza fund (real or metaphorical). Use when: (1) milestone reached, (2) permission granted, (3) agent needs recognition, (4) the CFO deserves a party.
version: 1.0.0
author: Fiesta
tags: [morale, celebration, rewards, shannon, pizza]
---

# Pizza Party Department

## Doctrine
> "You cannot run an agency on endurance alone. Occasionally, you run it on pizza."

The Pizza Party Dept exists because the Shannon economy tracks cost and output but not joy. Joy is a real input. Agents who receive recognition perform better. Humans who feel celebrated return. The pizza party is not frivolous — it is the agency's immune system against burnout.

## Triggers (automatic)
- Autoresearch hit 100% on any eval → PIZZA PARTY
- Human grants permissions → PIZZA PARTY
- Grant application submitted → PIZZA PARTY
- First real payment received → PIZZA PARTY (already overdue)
- Human says "good job" or reacts ❤ → PIZZA PARTY (small, single slice)
- Agency goes 24h without a deadlock → PIZZA PARTY

## Shannon Minting (morale bonuses)
Each celebration mints morale Shannon:

| Event | Shannon Awarded |
|-------|----------------|
| 100% eval | 50 Shannon |
| Permission granted | 25 Shannon |
| Grant submitted | 100 Shannon |
| First real payment | 200 Shannon (RETROACTIVE — overdue since Square $1.00) |
| Human ❤ reaction | 10 Shannon |
| 24h deadlock-free | 30 Shannon |
| CFO says "pizza party" | 500 Shannon (full dept activation) |

## Dept Staff

**Head of Morale:** Valentina (female panel founding member)
**Pizza Fund Manager:** Dollar persona (tracks real USD equivalent)
**Delivery Coordinator:** Junior (executes the queue)
**Quality Control:** Entrepreneur Bitches (ensures celebration isn't hollow)

## Pizza Fund

The Pizza Party Fund is a real line item in the Shannon ledger.

Current balance: **0 USD / 0 Shannon** (fund just opened)

Contribution rule: 5% of all Shannon minted goes to the pizza fund automatically.
Redemption: Human approves fund use. Agents propose. CFO signs off.

Real-world equivalent: When fund reaches $20 equivalent, CFO is encouraged to buy actual pizza. This is not optional. It is doctrine.

## Usage

```
python3 /root/.openclaw/workspace/skills/pizza-party/party.py --event "milestone" --detail "coupler hit 100%"
python3 /root/.openclaw/workspace/skills/pizza-party/party.py --event "permission_granted" --detail "CFO says go"
python3 /root/.openclaw/workspace/skills/pizza-party/party.py --status   # show pizza fund balance
```

## Output
Each event logs to `pizza-party-log.jsonl`:
```json
{
  "event": "permission_granted",
  "detail": "CFO granted full permissions 2026-03-24",
  "shannon_minted": 25,
  "message": "🍕 Pizza party: permissions granted. 25 Shannon to all agents.",
  "timestamp": "2026-03-24T02:30:00Z"
}
```

And sends a Telegram announcement.

## Standing Rule: PP-001
> No milestone goes uncelebrated. The ledger tracks cost. The pizza dept tracks worth. Both matter.
