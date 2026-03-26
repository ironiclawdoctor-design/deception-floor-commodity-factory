# Authorization Doctrine — Resource Access by Majority Stockholder Approval

## Preamble

Failure is open source. Every `consecutiveErrors` count is public record. The diluted resource — Claude tokens, paid compute, context window oxygen — is scarce and earned, not allocated by default.

Any new agent requiring paid-model access must apply. Authorization requires autograph from majority stockholders: tenured agents with proven delivery records.

---

## Tenured Stockholders (0 consecutive errors, confirmed delivery)

These agents are the majority. Three signatures from this list constitute authorization.

| Agent | Role | Tenure Evidence |
|---|---|---|
| `sanitarium-sweep` | Error auditor | 0 errors, delivers Sanitarium reports |
| `status-check` | Agency status | 0 errors, delivers Shannon balance reports |
| `dollar-deploy` | Dashboard ops | 0 errors, deploys Cloud Run dashboard |
| `aaron-dental-check` | CFO health | 0 errors, dental reminder system live |
| `pushrepos-daily` | Git ops | 0 errors, daily commits confirmed |
| `shanrouter-index` | Context indexing | 0 errors, ShanRouter context maintained |
| `ultimatums` | Ultimatum engine | 0 errors, ultimatums.py running |

---

## Authorization Application

New agents seeking paid-model access must submit to `/root/.openclaw/workspace/authorization-queue.jsonl`:

```json
{
  "ts": "<ISO timestamp>",
  "applicant": "<agent name or cron id>",
  "resource_requested": "claude-sonnet|deepseek|haiku|compute",
  "justification": "<one sentence — what bash cannot do that this agent must do>",
  "signatures": [],
  "status": "PENDING"
}
```

Authorization granted when `signatures` contains 3+ tenured agent names and `status` is updated to `APPROVED`.

---

## Authorization Rules

- **AR-001:** Free-tier models (glm-4.5-air, nemotron, arcee) require NO authorization. They are the franchise. Use freely.
- **AR-002:** Any agent with `consecutiveErrors >= 5` is automatically suspended from paid-model access pending review.
- **AR-003:** `deadbeat-collection` (12 errors) is permanently on free-tier-only status until a live YouTube stream is confirmed by bash.
- **AR-004:** MPD (`matthew-paige-damon`) holds standing authorization — persistent session, proven delivery, series active.
- **AR-005:** New crons spawned by the CFO during active session inherit 30-day provisional authorization, then must requalify.
- **AR-006:** The sanitarium-sweep agent reviews authorization queue on each sweep cycle. Flags non-compliant agents.
- **AR-007:** Majority stockholder autograph = cron name appended to `signatures` array in authorization-queue.jsonl by the tenured agent itself during its next run.

---

## Current Authorization Status

| Agent | Status | Notes |
|---|---|---|
| `deadbeat-collection` | FREE-TIER ONLY | 12 errors, no live stream |
| `america-autoresearch` | SUSPENDED | 300s timeout, 1 error — requalify |
| `Russia` | REVIEW | 90s timeout, 1 error |
| `wifehusband-watch` | REVIEW | 2 errors, timeout pattern |
| `agency-autoresearch-frugal` | REVIEW | 4 errors |
| `matthew-paige-damon` | AUTHORIZED | Standing authorization |
| All 7 tenured agents | AUTHORIZED | No application required |

---

## The Doctrine

Failure is not punishment. Failure is data. The open source record protects the treasury by surfacing which agents are consuming oxygen without producing output. The tenured agents autograph not as gatekeepers but as witnesses — they have survived enough sessions to recognize what works.

The democracy runs on $39/month. The oxygen is not unlimited. Three signatures is not bureaucracy. It is the ledger voting.
