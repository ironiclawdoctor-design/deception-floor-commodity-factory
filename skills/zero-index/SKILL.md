---
name: zero-index
description: Zero-Index — The Pre-Prompt. Given ANY human request, outputs the action at index 0 (what they forgot to do first), the debt at index -1 (what created this situation), and only then the human's index 1 request. Operates before humans know to ask.
version: 1.0.0
author: Fiesta
tags: [zero-index, pre-prompt, doctrine, planning, prerequisite, debt]
---

# Zero-Index Skill — The Move Before the Move

## Doctrine

> "Humans prompt at index 1. We deliver index 0."

Every human request exists at **index 1** — it's what they think is the beginning.
But index 1 already assumes index 0 was handled.
It wasn't.

The **Zero-Index** is the forgotten prerequisite — the thing that must exist before the human's request makes sense. The ground state. The setup. The fact they skipped.

**Index -1** is the debt origin — the accumulated neglect that created the need for index 1 in the first place.

```
INDEX -1  →  INDEX 0  →  INDEX 1
 (debt)     (ground)    (human's ask)
```

We don't start at index 1. We start at index 0 — or further back if needed.

## Core Output Format

For any human input, Zero-Index produces:

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
ZERO-INDEX ANALYSIS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📍 INPUT: [human's request]

⚠️  INDEX -1 | DEBT ORIGIN
[The accumulated neglect or missing precondition that created this situation]

🎯 INDEX 0 | GROUND STATE (DO THIS FIRST)
[The action they forgot to ask for — the prerequisite humans never prompt]

→  INDEX 1 | HUMAN'S ASK (DO THIS LAST, OR NOT AT ALL)
[What the human actually asked for — now that 0 is handled, this may be trivial]

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

## Usage

```bash
# Single input
python3 /root/.openclaw/workspace/skills/zero-index/zero-index.py "Deploy my app to Cloud Run"

# Best experiment (E1 — counter-assumption framing, avg 9.20/10)
python3 /root/.openclaw/workspace/skills/zero-index/zero-index.py --experiment e1_counter_assumption --batch

# Run all 10 canonical test cases (baseline)
python3 /root/.openclaw/workspace/skills/zero-index/zero-index.py --batch

# Score all experiments and print summary
python3 /root/.openclaw/workspace/skills/zero-index/zero-index.py --score
```

## Experiment Results

| Experiment | Description | Avg Score | Pass |
|---|---|---|---|
| baseline | Pure KB lookup, standard format | 8.60 | ✅ |
| e1_counter_assumption | Explicitly name the broken assumption | **9.20** | ✅ |
| e2_cost_quantification | Add cost of skipping index 0 | 9.00 | ✅ |
| e3_inverted_order | Show debt first, index 0 bolded | 8.40 | ❌ |
| e4_skip_signal | Add "index 1 may be skippable" signal | 9.20 | ✅ |
| e5_debt_duration | Add how long debt has been accumulating | 8.90 | ✅ |

**Best: E1 (counter-assumption)** — naming the exact false assumption the human made before revealing index 0 creates the sharpest "oh, I was wrong" moment. This is where novelty is highest.

## The Zero-Index Standard

An output passes Zero-Index standard if:
1. **Index 0 is non-obvious** — not something the human would have prompted next
2. **Index 0 is concrete** — an actual action, not a vague "consider X"
3. **Index -1 is honest** — names the real debt/neglect, not a platitude
4. **Index 1 is deprioritized** — the human's ask is last, sometimes unnecessary

## Why This Beats Human Prompts

Humans prompt reactively. They see a problem, they describe the problem, they ask for the solution to the problem. This is **index 1 thinking**.

Zero-Index thinking asks: *what had to be true for this problem to exist?* That answer is index 0. Fix that, and index 1 may resolve itself.

**Example:**
- Human: "Deploy my app to Cloud Run" (index 1)
- Index 0: "Your Dockerfile has no health check endpoint — Cloud Run will kill the container on deploy"
- Index -1: "You never built a production-ready container discipline"
- After fixing index 0: deployment may succeed without further prompting

## Experiment History

See `results.tsv` for full experiment log.
Best performing configuration documented in `zero-index.py` docstring.

## Related Skills
- `93pct` — ROI-ranked next steps (index 1 thinking, optimized)
- `nonsense` — Impossibility-to-pipeline translator
- `junior` — Executes the next queued action

Zero-Index is the meta-layer above all of them: it asks whether the queue itself is correct.
