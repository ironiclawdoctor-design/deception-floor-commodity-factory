# Root Causes of Eval Suite Success

Derived from 3 autoresearch runs (fiesta-agents, fiesta, math).
These are the conditions under which an eval suite *successfully* drives skill improvement.

---

## RC-1: Binary Precision
**Cause:** An eval passes or fails — no partial credit, no scales.
**Why it works:** Ambiguous scoring compounds across runs and hides the signal. Binary evals isolate causation: the change either helped or it didn't.
**Failure mode:** "Rate the quality 1-10" → observer bias, drift, false stability.

## RC-2: Adversarial Expansion
**Cause:** When the suite hits 100%, it's expanded — not celebrated.
**Why it works:** 100% on a fixed suite means the skill has gamed the evals, not that it's optimal. Expansion forces new gaps to surface. The ceiling is a signal to look harder.
**Failure mode:** Stopping at 100% → skill overfits to the eval rubric, real-world failures remain.

## RC-3: Test Input Diversity
**Cause:** Test inputs cover edge cases, not just the happy path.
**Why it works:** A skill that passes T1-T5 on typical inputs but fails on proofs, applied problems, or multi-agent tasks has a false score. Diversity reveals the tail.
**Failure mode:** 5 similar inputs → eval measures one mode of behavior, not the skill's full range.

## RC-4: Eval Failure = Skill Change Target
**Cause:** Every failing eval maps to exactly one mutation in the skill.
**Why it works:** If an eval fails but the mutation is unclear, the eval is bad — it's measuring an unmutable property or something too abstract. Good evals directly imply a fix.
**Failure mode:** "Does the output feel helpful?" → fails → what do you change?

## RC-5: Evals Grow Harder Over Rounds
**Cause:** Each round adds evals that the previous round's skill would fail.
**Why it works:** Easy evals get passed by any reasonable skill. Harder evals surface non-obvious gaps. The suite gets smarter as the skill gets better.
**Failure mode:** Adding evals that the current skill already passes → inflated score, no new signal.

## RC-6: Eval Names Are Claims
**Cause:** Each eval is named as a specific capability claim: "E8: No shortcut phrases."
**Why it works:** The name forces precision. If you can't name it in 4 words, you can't measure it. Named claims also make the changelog readable — "E8 fixed by adding anti-pattern table" is actionable.
**Failure mode:** "E3: Output quality" → measures nothing specific.

## RC-7: Anti-Patterns Beat Positive Rules
**Cause:** Evals that check for the absence of specific failure modes outperform evals that check for presence of vague virtues.
**Why it works:** "Does the output contain 'clearly'?" is more reliable than "Is the reasoning transparent?" Negative checks are deterministic. Positive virtue checks rely on judgment.
**Failure mode:** "Is the response helpful?" (virtue) vs "Does it avoid 'it can be shown that'?" (anti-pattern) — only the second drives mutation.

## RC-8: Worked Examples in Evals
**Cause:** Each eval includes a concrete pass/fail example, not just a description.
**Why it works:** The agent scoring the eval needs to calibrate against a known case. Without an example, two scorers diverge. With one, they converge.
**Failure mode:** "Pass condition: The output is clear." — clear to whom? Under what conditions?

## RC-9: Evals Test Agent Behavior, Not Skill Text
**Cause:** The eval asks "would an agent following this skill do X?" — not "does the skill text mention X?"
**Why it works:** A skill can mandate something in 3 places and agents still miss it. What matters is whether the mandate is clear enough to produce the behavior. Eval from the agent's perspective, not the author's.
**Failure mode:** "Does the skill include a Quality Check section?" (text check) vs "Would an agent produce a Quality Check?" (behavior check).

## RC-10: Stopping Condition Is Principled
**Cause:** The loop stops when no new harder eval can be generated that reveals a gap.
**Why it works:** This is the only honest stopping condition. "We ran 20 experiments" or "we hit 95%" are arbitrary. The loop ends when the eval suite exhausts the known failure space.
**Failure mode:** Stopping at a round number → leaves real gaps undetected.
