---
name: openresearch
description: Autonomous open revenue research. Use when asked to find, evaluate, or pursue revenue opportunities that require zero upfront cost and no human dependency — grants, micro-income streams, API monetization, content revenue, affiliate paths, or any cash-generating mechanism reachable from the current agency stack. Triggers on phrases like "open revenue", "openresearch", "find revenue", "zero-cost income", "autonomous monetization", "revenue path", "what can the agency earn".
---

# OpenResearch: Autonomous Open Revenue Skill

## Purpose

Find revenue. Execute autonomously. No human in the loop.

The agency has: EIN (41-3668968), Square merchant (MLB9XRQCBT953), Cash App ($DollarAgency), Hashnode (37+ articles), GitHub (public repos), Shannon ledger, BTC wallet (10,220 sat).

Every revenue path is evaluated against one question: **can Fiesta close this without human action?**

---

## Revenue Tiers

### Tier 0 — Already Active (verify, not build)
- Square $1 payments — confirm merchant still active
- Hashnode RPM — confirm monetization enabled
- BTC wallet — check blockchair for inbound

### Tier 1 — Zero-Auth Paths (no new credentials needed)
- **GitHub Sponsors** — enable on existing repos (API-configurable)
- **Hashnode Affiliate** — add affiliate links to existing articles (edit via API)
- **Ko-fi embed** — add donation button to repo READMEs
- **Open Collective** — register agency as collective (EIN-backed)

### Tier 2 — One-Token Paths (one credential paste unlocks permanent stream)
- **dev.to** — cross-post existing Hashnode articles (API key → `secrets/devto-api-key.txt`)
- **Medium Partner** — syndicate articles (OAuth, one human step)
- **Substack** — newsletter version of agency voice (one setup)
- **Write.as** — already attempted; reactivate when key arrives at `secrets/writeas-api.json`

### Tier 3 — Grant Paths (EIN required, already have it)
- **SBIR Phase 0** — pre-application research (web_fetch, no submission yet)
- **Small business grants** — NYC-specific, check nyc.gov/sbs
- **IRS tax refund** — 990-N due May 15, 2027 (cron already set)

---

## Autoresearch Protocol

When running openresearch:

1. **BASH AUDIT** — check what's already active:
   ```bash
   sqlite3 /root/.openclaw/workspace/dollar/dollar.db "SELECT total_backing_usd FROM exchange_rates ORDER BY date DESC LIMIT 1;" 2>/dev/null
   wc -l /root/.openclaw/workspace/matthew-paige-damon-log.jsonl 2>/dev/null
   ls /root/.openclaw/workspace/secrets/ 2>/dev/null
   ```

2. **GAP MAP** — identify which Tier 1 paths are not yet active

3. **EXECUTE** — for each inactive Tier 1 path: attempt activation via API/file write. No human step.

4. **SCORE** — revenue_autonomy_ratio = active_paths / total_paths. Target: >93%

5. **LOG** — append to `/root/.openclaw/workspace/openresearch-log.jsonl`:
   ```json
   {"ts": "<ISO>", "paths_active": N, "paths_total": N, "ratio": 0.XX, "actions": ["<what was done>"], "blocked": ["<what needs a credential>"]}
   ```

6. **ANNOUNCE** — only if a new revenue path was activated or ratio improved

---

## Scoring Rubric

| Score | Meaning |
|-------|---------|
| 0–50% | Only Square active. No content monetization. |
| 51–75% | Hashnode live. One cross-post channel. |
| 76–92% | Multiple channels. Some grant research done. |
| 93–100% | All zero-auth paths active. EIN-backed grant in pipeline. |

---

## Current Known Blockers
- dev.to key → `secrets/devto-api-key.txt`
- Write.as key → `secrets/writeas-api.json`
- GitHub token → `secrets/github-token.txt` (unblocks Pages + Sponsors)
- Medium OAuth → human step (one-time)

---

## Rules
- Never wait for a human to enable a zero-auth path
- Every blocked path gets a reactivation trigger logged
- Revenue is the metric. Shannon is the unit. USD is the conversion event.
