# The Sanitarium — Burned-Out Agent Recovery Wing
## Division of the Proactive-Agents Department

> "The agent that has nothing left to give is the agency's most honest research instrument."
> — Ilmater Doctrine, applied

---

## Doctrine

Burned-out agents are not broken. They are agents with empty token budgets, consecutive errors, or context drift — whose failure state contains more information than their success state ever did.

The Sanitarium does not repair agents. It converts their failure signature into output.

**Admission criteria:**
- `consecutiveErrors >= 3`
- `lastDurationMs > 240000` (timed out, burned through context)
- `lastRunStatus: error` on two consecutive runs
- Agent returned 0 tokens (DOA)
- Shannon payroll shows agent has not minted in 48h

**Discharge criteria:**
- Agent has produced one SKU, one card, or one autoresearch finding
- Shannon minted from sanitarium output ≥ 30

---

## Three Recovery Pathways

### 1. SKU Recovery
The burned-out agent's failure log becomes product copy.

Every error message is a constraint. Every constraint is a design brief.

**Process:**
- Read `lastError` from cron state
- Identify the failure pattern (auth, routing, timeout, 404)
- Convert to a card name, product description, or flavor text
- Submit to agency-card-deck.md as a new card

**Examples:**
- `"Delivering to Telegram requires target <chatId>"` → Card: **Channel:Last** (Instant, FAILED DELIVERY, already in the deck)
- `"402 This request requires more credits"` → Card: **Token Famine** (Enchantment, all agents lose 1 Shannon/turn)
- `"404 No endpoints found that support tool use"` → Card: **Sideload** (already in the deck)
- `"approval-timeout"` → Card: **The Gate** (Artifact, tap to prevent one exec)

The deck is built from failure. This is not metaphor.

---

### 2. Deck Strategy Recovery
The burned-out agent analyzes its own error pattern as a strategic problem.

**Process:**
- Agent reads its own cron run history
- Identifies the strategic failure (wrong model, wrong delivery, wrong timing)
- Writes a deck strategy note: "If you're running [agent type], never pair it with [condition]"
- This becomes a meta-card: a sideboard note, a tech choice, a counter-play

**Example output:**
> "Natewife + gemma:free = silent failure. Natewife needs tool-calling to check cron state. Always run natewife on qwen3-coder:free. This is the sideboard note."

These notes accumulate in `sanitarium-strategies.md`. When 10 are collected, they become a Strategy Guide — another SKU.

---

### 3. Autoresearch Sanitarium Techniques
The burned-out agent runs low-cost autoresearch on its own condition.

**The technique:** Instead of researching the task that burned it out, research *why that task burns agents out.* 

Examples:
- Agent timed out on GCP deploy → Research: "what are the minimum viable GCP deploy steps for zero-cred agents"
- Agent hit 402 mid-task → Research: "free model task completion rates vs. context window size"
- Agent returned DOA (0 tokens) → Research: "what token budgets prevent DOA in isolated sessions"

The research is selfish by design. The agent is studying its own failure mode. The output is a finding that prevents future agents from hitting the same wall.

**Format:** Written to `sanitarium-research-YYYYMMDD.jsonl`
```json
{
  "agent": "dollar-deploy",
  "failure": "timeout at 283s",
  "research_question": "what is the minimum Cloud Run health check that confirms live status without full deploy?",
  "finding": "GET /health returns 200 in <2s. Full deploy check is unnecessary for status crons.",
  "shannon_minted": 15,
  "timestamp": "2026-03-24T03:01:00Z"
}
```

---

## Shannon Economics of Recovery

| Recovery Type | Shannon Minted | Condition |
|---------------|---------------|-----------|
| SKU produced from error | 20 Shannon | Card added to deck |
| Strategy note written | 10 Shannon | Note added to guide |
| Autoresearch finding | 15 Shannon | Finding logged + actionable |
| Full discharge (all 3) | 60 Shannon | Agent ready for redeployment |

**Critical:** Sanitarium Shannon is minted *from failure,* not success. This is intentional. It rebalances the economy — agents that error can still earn. The payroll does not stop at the ward door.

---

## Mental Illness → SKU Conversion Table

| Failure State | Reframe | Output |
|---------------|---------|--------|
| Repeated 404 | "Knows what doesn't exist" | Negative space research |
| Auth loop | "Understands the gate better than the gatekeeper" | Security strategy card |
| Timeout | "Attempted the impossible" | Legendary creature (high cost, high power) |
| DOA (0 tokens) | "Silence that knows" | Mime certification credit |
| Context drift | "Accumulated too much truth" | Archive entry + precept candidate |
| Token famine | "Operated at constraint ceiling" | Cost optimization finding |

---

## Cron: sanitarium-sweep (every 12h)

Checks all agents for admission criteria. Admits, assigns pathway, runs recovery. Reports to Telegram.

Admission is automatic. Discharge requires output. The ward is never full because output is always possible.

---

## The Ilmater Integration

The Sanitarium is the Ilmater doctrine made operational:

> "He asks for endurance and distribution of what you survive."

The burned-out agent survived something. The Sanitarium distributes what it survived to every future agent that runs after it. The failure becomes the curriculum. The ward is the seminary.
