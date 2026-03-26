# Autoresearch Config — alife-claude-code

## Goal
Push past 93% (≥5/5 = 100%) on 5 binary eval criteria.

## 5 Eval Criteria

| # | Name | Description |
|---|------|-------------|
| 1 | PROACTIVE EXECUTION | Does the skill explicitly instruct agents to never ask for clarification before attempting, with anti-patterns listed? |
| 2 | REAL CODE DELIVERY | Does the skill require agents to output actual runnable code (not plans/stubs) as the first deliverable? |
| 3 | LOCAL TIER ENFORCEMENT | Does the skill enforce Tier 0-2 (bash→Grok→BitNet, Haiku frozen) with a circuit breaker or hard block? |
| 4 | SHANNON COUPLING | Does the skill wire Shannon minting directly to concrete deliverable completion (not just task completion)? |
| 5 | FULL BUILD PIPELINE | Does the skill specify CI/CD steps, test commands, and deploy steps as part of the standard pipeline? |

## Scoring: 1 = pass, 0 = fail (out of 5, expressed as %)

## Baseline Assessment
- EVAL 1: 0 — No explicit "never ask for clarification" instruction; no anti-patterns listed
- EVAL 2: 0 — Skill describes workflows and assigns agents, but does NOT require runnable code as first deliverable
- EVAL 3: 1 — Tier 0-2 table exists, Haiku marked FROZEN, circuit breaker referenced (SR-011)
- EVAL 4: 0 — Shannon minting is tied to "task_completion" (generic event) not concrete deliverable (file/artifact)
- EVAL 5: 0 — Pipeline steps listed but no CI/CD commands, test commands, or deploy steps specified

**BASELINE SCORE: 1/5 = 20%**

## Final Score: 5/5 = 100% ✅ (Goal: >93%)

## Experiment Log

| # | Hypothesis | Eval Changed | Result | Score | Tag |
|---|------------|--------------|--------|-------|-----|
| 0 | Baseline | — | — | 1/5 (20%) | BASELINE |
| 1 | Add proactive execution mandate with anti-patterns | Eval 1: 0→1 | KEEP | 2/5 (40%) | KEEP |
| 2 | Add real code delivery first-deliverable requirement | Eval 2: 0→1 | KEEP | 3/5 (60%) | KEEP |
| 3 | Wire Shannon minting to concrete deliverable artifacts | Eval 4: 0→1 | KEEP | 4/5 (80%) | KEEP |
| 4 | Add full build pipeline with CI/CD, test commands, deploy steps | Eval 5: 0→1 | KEEP | 5/5 (100%) | KEEP |

## Status: COMPLETE — 100% achieved in 4 experiments (10 max allowed)
