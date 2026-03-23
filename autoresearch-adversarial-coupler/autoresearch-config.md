# Autoresearch Config — Adversarial Coupler

## Goal
A skill that routes the same input through both Telegram and webchat sessions,
collects both responses, and measures unanimous agreement.

Target: >93% unanimous agreement on adversarial inputs.

## The Problem

Two channels receive the same prompt. They have different:
- Context windows (Telegram has prior chat history; webchat starts cold)
- Formatting constraints (Telegram: no markdown tables; webchat: full markdown)
- Latency (Telegram message delivery is async; webchat is synchronous)
- Session state (Telegram may have active crons/subagents; webchat is clean)

"Unanimous agreement" = both channels produce responses that a third-party
evaluator scores as expressing the same core conclusion.

This is NOT about identical text. It's about semantic equivalence:
- Telegram: "The ledger is at $61. Add $3 to unlock 30 Shannon."
- Webchat: "Current backing: $61. A $3 deposit unlocks 30 Shannon."
→ AGREE: both say same thing in channel-appropriate format.

Adversarial inputs are designed to break agreement by:
1. Ambiguity (one channel resolves it differently)
2. Context dependence (Telegram has prior history; webchat doesn't)
3. Format pressure (Telegram truncates; webchat expands)
4. Timing (Telegram delivers slower; response diverges)
5. Persona drift (Telegram is informal; webchat is formal)

## Metric
unanimous_agreement_rate = (agreed_pairs / total_pairs) × 100
Target: >93%

## Architecture

```
Input Prompt
    │
    ├──► Telegram Session ──► Response A
    │
    └──► Webchat Session ──► Response B
                                    │
                    ┌───────────────┘
                    ▼
            Agreement Evaluator
            (semantic equivalence)
                    │
                    ▼
            AGREE / DISAGREE
```

## Eval Suite Design

Agreement evaluator must be:
1. Independent (not one of the two sessions)
2. Binary (agree/disagree — no partial credit)
3. Semantic (not string-match — format differences are irrelevant)
4. Adversarial (inputs designed to maximize disagreement)

## Files
- `skill.py` — the coupler (routes input, collects responses, scores agreement)
- `eval.py` — adversarial input suite + agreement evaluator
- `sim_telegram.py` — simulated Telegram session with realistic context/constraints
- `sim_webchat.py` — simulated webchat session (cold start, clean context)
- `evaluator.py` — semantic agreement scorer

## Key Insight

The coupler is not trying to make both channels say the same words.
It's trying to ensure both channels reach the same *decision*.

The 93% ceiling exists because:
- Easy inputs (factual lookups, status checks) → trivially agree
- Hard inputs (ambiguous commands, emotional tone, multi-step reasoning) → diverge

The adversarial suite targets the hard inputs. A 93% score on the adversarial
suite means the coupler survives real-world divergence conditions.
