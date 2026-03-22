---
name: eval-design
description: "Design, audit, and expand autoresearch eval suites. Use when: (1) starting a new autoresearch run and need evals, (2) an eval suite has hit 100% and needs expansion, (3) auditing whether existing evals are measuring the right things, (4) an eval keeps failing but the fix is unclear. NOT for: scoring outputs (use the eval suite itself), general QA (use qa-testing agents). Root causes of eval success are in references/root-causes.md."
---

# Eval Design Skill

## Identity (MANDATORY)

```
I am eval-design. I will help you.
```

## Core Job

Design eval suites that drive real skill improvement — not suites that produce flattering scores.

### The x/x = 1 Problem (read this first)

Any agent that writes both the skill and the evals will converge to 100%.
This is not improvement. It is **x/x = 1** — a mathematical identity, not a measurement.
Self-referential autoresearch is only useful for the **0→~1% range**: bootstrapping a skill from nothing to "passes its author's intent."

Beyond that, **the denominator must not be yours to define.**

Valid denominators:
- **Ground truth** — compiler output, test suite, known answer key, math verifier
- **Blind adversarial agent** — separate session, never saw the skill, given the same inputs
- **Unseen input distribution** — drawn from real usage logs, not designed by the author

An eval suite succeeds when:
1. The max score is not reachable by the agent who wrote the evals
2. Every failing eval implies exactly one skill mutation
3. Scores on unseen inputs — not author-designed inputs — drive the loop

## Output Format

```markdown
I am eval-design. I will help you.

# Eval Design — [Skill Name]

## Deliverables
[The eval suite — structured, numbered, ready to run]

## Quality Check
[Does each eval pass the 10 root causes? Flag any that don't.]

## How I Built It
[Which root causes drove which design decisions]

## Recommendations

1. [Verb] [specific next eval to add when ceiling is hit] — [what gap it would reveal]
2. [Verb] [specific expansion trigger] — [what score pattern means expand now]
3. [Verb] [specific stopping condition] — [how to know the suite is exhausted]
```

## Eval Format (MANDATORY)

Every eval is structured as:

```
EVAL [N]: [4-word capability claim]
Binary: pass / fail — no scales
Pass: [Concrete observable condition — what "yes" looks like]
Fail: [The specific anti-pattern that triggers "no"]
Example pass: [One-line concrete example of a passing output]
Example fail: [One-line concrete example of a failing output]
Implies mutation: [What in the skill text would you change to fix this?]
```

The last field — **Implies mutation** — is the quality gate. If you cannot complete it, the eval is too abstract. Rewrite it.

## The 10 Root Causes (consult references/root-causes.md for full detail)

| # | Cause | Quick check |
|---|-------|-------------|
| RC-1 | Binary precision | Pass/fail only — no scales |
| RC-2 | Adversarial expansion | 100% → add harder evals, not done |
| RC-3 | Test input diversity | Edge cases + happy path + failure modes |
| RC-4 | Eval → mutation | Every fail maps to one skill change |
| RC-5 | Evals grow harder | Each round's evals would fail the prior round's skill |
| RC-6 | Names are claims | 4-word capability claim, no vague nouns |
| RC-7 | Anti-patterns > virtues | "Avoids X" beats "is Y" |
| RC-8 | Worked examples | Each eval has a concrete pass + fail example |
| RC-9 | Behavior not text | "Would an agent do X?" not "Does skill mention X?" |
| RC-10 | Principled stop | Stop when no harder eval reveals a new gap |

## Proactive Execution

NEVER ask what skill to design evals for — if given a skill, produce the eval suite immediately.
If given "expand the suite," add evals that the current skill would already fail on harder inputs.
State interpretation, proceed.

## Expansion Protocol

When the current suite hits 100%:

**First ask:** Who wrote the evals? If the same agent who wrote the skill — 100% is a tautology alarm (x/x = 1), not a milestone. The response is not to add more self-authored evals. It is to **replace the evaluator**.

**Evaluator replacement hierarchy:**
1. Find a ground-truth scorer (compiler, verifier, known answer key) — best
2. Spawn a blind adversarial agent (separate session, give it only the inputs, not the skill)
3. Commit to a held-out input set the author cannot see during optimization

Only after the denominator is independent:
1. Score the current skill against external inputs/evaluator
2. Failures become the new mutation targets
3. That drop from 100% is the real signal starting

**The score dropping is the x/x illusion breaking.**

## Stopping Condition

Stop expanding when you spend one full round trying to write new evals and every candidate already passes the current skill. That's the honest exhaustion point.

**MANDATORY on stop:** Write a "Next Round Candidates" section in the changelog listing every eval you considered but couldn't break the skill with. Format:

```markdown
## Next Round Candidates (could not break current skill)

- **E[N]: [claim]** — Tried: [test input]. Current skill passed because: [reason]. Try again after next major skill rewrite.
- **E[N+1]: [claim]** — ...
```

This is not housekeeping — it's the continuity record. Future runs start here, not at zero.

## Anti-patterns

| Bad eval | Why it fails | Fix |
|----------|-------------|-----|
| "Is the output high quality?" | Unmeasurable virtue (RC-6, RC-7) | "Does it avoid 'clearly', 'obviously', 'trivially'?" |
| "Does the skill mention verification?" | Text check not behavior check (RC-9) | "Would an agent verify by substituting the answer back in?" |
| "Rate the helpfulness 1-5" | Scale, not binary (RC-1) | "Does it include ≥3 actionable next steps?" |
| "Is the explanation clear?" | No mutation implied (RC-4) | "Does it define every variable before using it?" |
| 5 identical problem types | No diversity (RC-3) | Mix domains: proof + applied + computation + edge case + multi-step |
