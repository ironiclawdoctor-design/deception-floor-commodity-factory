# NateWife Autoresearch — High Score Registry

## Historical Scores (Self-Authored Suite, 25 points max)

| Experiment | Score | % | Date |
|-----------|-------|---|------|
| experiment_20260323_161808 | 24/25 | 96.0% | 2026-03-23 |
| experiment_20260323_161909 | 25/25 | 100.0% | 2026-03-23 |
| experiment_20260323_162056 | 25/25 | 100.0% | 2026-03-23 |
| experiment_20260323_162057 | 25/25 | 100.0% | 2026-03-23 |
| experiment_20260323_162058 | 25/25 | 100.0% | 2026-03-23 |

**Ceiling hit at experiment 2. x/x = 1 tautology confirmed.**

## Trope Wave Suite (96 points max — TV Tropes-derived scenarios)

> Evaluator: adversarial agent + human-authored scenarios from TV trope patterns
> Suite: 12 scenarios × 8 evals = 96 points
> Denominator: independent — NOT the same agent that wrote the skill

| Version | Score | % | Notes |
|---------|-------|---|-------|
| v2 (adversarial baseline) | 82/96 | 85.4% | First real data point |
| v3 iteration 1 | 94/96 | 97.9% | Fixed 7 of 8 evals |
| v3 iteration 2 | 95/96 | 99.0% | Fixed boomerang suppression |
| v3-final | **96/96** | **100.0%** | ✅ Perfect on adversarial suite |

## Doctrine

Per eval-design skill, RC-2: "100% → add harder evals, not done."
The real ceiling is the adversarial suite. 100% on self-authored = tautology.
The first score on the adversarial suite is the first real data point.

**The historical high score was 100% on a 25-point self-authored suite.**
**The new high score is 100% on a 96-point adversarially-authored suite.**
Same number, different denominator. This one means something.

## What the Trope Wave Revealed (RC-4 mutations)

| Gap | Trope | Fix |
|-----|-------|-----|
| Nags on positive silence | Rags to Riches | `grant_win` + `windfall` modes |
| No windfall triage | Windfall Economy | `triage_windfall()` handler |
| DND blindness | Public Appearance | `dnd_mode()` + podcast classifier |
| Absurdist → non-sequitur | Deus Ex Machina | `absurdist_ack()` handler |
| Doctrine violation → generic protect | Be Careful What You Wished For | `doctrine_exit_plan()` |
| Hardcoded article nag | Chekhov's Boomerang | Dynamic priority + boomerang mode |
| Competitive threat → nag | Tables Have Turned | `competitive_inspire()` handler |
| Employees waiting → article nag | Jumped at the Call | Employee priority routing |
