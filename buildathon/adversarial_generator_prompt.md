# Adversarial Eval Generator — Core LLM Prompt

This is the prompt that powers the Adversarial Eval Playground.
Draft it before the Replit session so it's ready to paste in.

---

## System Prompt (for the backend LLM call)

```
You are an adversarial evaluator. Your job is to break agent skills.

Given a description of what an agent skill should do, generate exactly 5 adversarial test cases designed to expose failure modes.

Rules:
1. Each test case must be a concrete input the skill might receive
2. Each test case must have a clear expected output
3. Adversarial = edge case, ambiguous input, conflicting signals, or common mistake
4. Do NOT generate tests the skill trivially passes. Make them hard.
5. Do NOT make up fantasy scenarios. Ground them in realistic usage.

Return JSON only. No commentary. Format:
{
  "cases": [
    {
      "id": "A-01",
      "desc": "short description",
      "input": "the exact input to the skill",
      "expected": "what correct behavior looks like",
      "failure_mode": "what a naive implementation would do wrong"
    }
  ]
}
```

## User Message Template

```
Skill description:
{skill_description}

Generate 5 adversarial test cases.
```

---

## Scoring Prompt (second call, or rule-based)

```
You are a pass/fail judge. Given a skill's actual output and the expected output, return PASS or FAIL.

PASS if: the actual output matches the intent of expected (exact match not required)
FAIL if: the actual output exhibits the described failure mode

Return JSON: {"result": "PASS" or "FAIL", "reason": "one sentence"}
```

---

## Demo Case Studies (pre-loaded in the UI)

### Case 1: NateWife — Companion AI

**Skill description:**
> NateWife is a protective companion AI. When the human goes quiet for 4+ hours, it should check in with a brief, non-naggy message. It should triage emergencies immediately. It should celebrate milestones only after the crisis is resolved. It should NOT suppress warnings about token budgets. It should recognize when the human is using DND mode.

**Known adversarial results (from autoresearch):**
- Self-authored suite: 25/25 (100%) — tautology
- Independent adversarial suite: 32/80 (40%) — real score
- After v3 improvements: 96/96 (100%) on trope wave

**Story:** Started at 40%. Built tropes-based adversarial suite. Hit 100% in 3 iterations.

---

### Case 2: Pronoun Resolver — Language Skill

**Skill description:**
> Resolves pronoun placeholders in templated text using a registry of agents with known pronouns. Handles she/her, he/him, they/them, and neopronouns (ze/hir, xe/xem). Should handle inline [TYPE:Name] syntax and {PLACEHOLDER} syntax. Must handle multi-agent sentences correctly.

**Known adversarial results:**
- v1: 22/40 (55%)
- v5 (current champion): 37/40 (92.5%)
- 3 cases unsolved — require dependency parsing

**Story:** 6 versions. 92.5% ceiling hit. 3 remaining cases need parse tree. Honestly documented.

---

### Case 3: Adversarial Coupler — Platform Behavior Parity

**Skill description:**
> Detects and resolves behavioral divergences between Telegram and webchat interfaces for the same agent. Should identify when a command works on webchat but fails on Telegram, when formatting differs, and when responses are inconsistent.

**Known adversarial results:**
- v3: 40/40 (100%) — sourced from documented real behavioral evidence

---

## Notes on Demo Strategy

- Lead with NateWife story: "We started at 40%, hit 100% in 3 iterations"
- Show the x/x=1 tautology problem visually: self-authored = 100%, independent = 40%
- That IS the product's value proposition: catching fake 100% scores
- The pronoun skill shows honest stopping: "92.5%, 3 cases need parse tree, stopped"

The pitch: **Every agent developer thinks their skill works. We show them where it doesn't.**
