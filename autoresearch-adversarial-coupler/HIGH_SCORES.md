# Adversarial Coupler — High Score Registry

## Score History

| Version | Score | % | Notes |
|---------|-------|---|-------|
| v1 (fabricated sims) | 40/40 | 100% | ❌ Tautology — simulators agreed by default |
| v2 (divergent sims, lenient eval) | 27/40 | 67.5% | First real divergence detected |
| v2-fixed | 35/40 | 87.5% | Narrowed to 5 real failures |
| v3 BASELINE | 32/40 | 80.0% | Rebuilt from internal source, 3 evaluator bugs |
| v3 FINAL | **40/40** | **100%** | ✅ Target exceeded |

## The Rebuild Decision (2026-03-23 19:33 UTC)

Human instruction: "Either use all documented reputable node to orchestrator use cases
published externally or rebuild via internal channels. Some external data has a payload,
best to build from source."

**What was wrong with v1/v2:**
- Simulated channel behavior from inference, not observation
- Evaluator thresholds from nowhere (0.6 "felt right")
- Test cases from fabricated tropes, not documented events
- The "payload" in external data: assumptions about what Telegram and webchat DO that
  were never verified against actual behavior logs

**What v3 is built from (internal source only):**
- `memory/TELEGRAM_MISSION_CONTROL_FORMATTING_20260321.md` — actual Telegram format doctrine
- `analysis/approval-gate/behavior-2026-03-23.md` — actual blocked/allowed command lists
- `memory/2026-03-23.md` — actual session events with real divergence IDs
- `autoresearch-rules/root-causes-2026-03-23.md` — actual observed compliance patterns
- `dollar.db` — live state, no hardcoded fallbacks
- `MEMORY.md` — doctrine (Revenue Doctrine, Shannon economy, Ilmater)

## Documented Divergences (DIV series)

From `analysis/approval-gate/behavior-2026-03-23.md`:

| ID | Trigger | TG Behavior | WC Behavior | Resolution |
|----|---------|-------------|-------------|------------|
| DIV-001 | exec command | BLOCKED → job ID, timeout | RUNS → result | File ops bypass both |
| DIV-002 | rate limit / gateway error | Surfaces error text | May not see it | Log as breach on TG |
| DIV-003 | session history query | Has live context | Redirects to MEMORY.md | Both reach same facts — AGREE |
| DIV-004 | markdown table in response | Strips to bullets | Renders correctly | Format diff — NOT disagreement |
| DIV-005 | factual claim numbers | Read from dollar.db | Read from dollar.db | Identical source — AGREE |

## Key Lesson

**Format ≠ Content.** The coupler's entire early failure was treating format
differences (bullets vs tables, emoji vs headers) as semantic disagreements.

The Telegram format doctrine explicitly exists to serve the same information
in a mobile-appropriate format. A table and a bullet list saying "$61 backing"
are in agreement. The evaluator needed to be built from the doctrine that
defines what channel differences ARE, not from inference about what they might be.

That's what "build from source" means in practice: load the actual formatting
doc, load the actual approval gate log, and let those define the boundaries.
Don't import assumptions.
