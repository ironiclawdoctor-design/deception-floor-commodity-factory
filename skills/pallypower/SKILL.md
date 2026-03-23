---
name: pallypower
description: PallyPower-inspired agency buff management. In WoW, PallyPower assigned paladin blessings to raid members so no buff was wasted or duplicated. This skill does the same for agency agents — assigns optimal "buffs" (capabilities, permissions, token budgets, API keys) to each agent so nothing is duplicated and every agent runs at full power. Use when onboarding new agents, assigning task load, or auditing who has what.
version: 1.0.0
author: Fiesta
tags: [wow, paladin, buffs, orchestration, assignment, agency]
---

# PallyPower — Agency Buff Manager

## WoW → Agency Mapping

| WoW Concept | Agency Equivalent |
|-------------|------------------|
| Paladin Blessing | Capability grant (API key, permission, tool access) |
| Greater Blessing | Long-duration assignment (cron job, standing permission) |
| Buff duration | Token budget or TTL |
| Rebuff timer | Cron refresh interval |
| Raid frame | Agent registry |
| Class colors | Department color coding |
| Missing buff | Unassigned capability → Shannon waste |

## The PallyPower Problem
Without buff management:
- Two agents try to publish the same article (409 conflict)
- Three agents all check BTC balance (3x API calls, 1x needed)
- No agent owns GCP deploy (falls through the cracks)
- Token budget unallocated — first agent burns it, others starve

## Buff Assignments (Current)

| Buff | Assigned To | Duration | Status |
|------|-------------|----------|--------|
| Hashnode publish | content-writer | standing | ✅ |
| BTC monitor | btc-monitor | 15min cron | ✅ |
| GCP deploy | devops-engineer | hourly cron | ✅ |
| Dollar ledger | dollar | always | ✅ |
| Security audit | security-auditor | on-demand | ✅ |
| Shannon mint | payroll-administrator | on-event | ✅ |
| RLHF export | revenue-architect | daily | ⬜ assign |
| Camoufox browser | ux-engineer | on-demand | ⬜ assign |
| Gmail | fiesta | on-API-enable | ⬜ waiting |
| Square/Cash App | cashapp-skill | on-token | ⬜ waiting |
| OpenWrt sim | senior-engineer | on-demand | ⬜ new |
| ngspice circuit | senior-engineer | on-demand | ⬜ new |
| PyResearch cache | fiesta | always | ✅ |

## Greater Blessings (Permanent Agency Grants)
From Thaniel/God authority:
- SSN(-1): All 24 agents ✅
- allow-always approval: All exec commands ✅  
- Hashnode pub access: content-writer ✅
- HuggingFace write: revenue-architect ✅
- Dollar DB write: dollar, fiesta ✅

## Missing Buffs (Needs Assignment)
1. `cloud-billing.googleapis.com` — enable for SA to read $300 credit balance
2. Camoufox /data/browser-server-token — assign to ux-engineer
3. Square developer token — pending Thaniel action
4. Gmail API enable — pending Console click

## Rebuff Schedule
```
Every 15min: BTC monitor (btc-monitor)
Every hour:  GCP deploy (devops-engineer) + RLHF collect
Every 4h:    Status rollup + ultimatum review
Every 8h:    NateWife rest check
Daily:       PyResearch cache warm + MEMORY.md update
Weekly:      Security audit + agent certification review
```

## Usage
```
python3 /root/.openclaw/workspace/skills/pallypower/assign.py --status
python3 /root/.openclaw/workspace/skills/pallypower/assign.py --missing
python3 /root/.openclaw/workspace/skills/pallypower/assign.py --assign <agent> <buff>
```
