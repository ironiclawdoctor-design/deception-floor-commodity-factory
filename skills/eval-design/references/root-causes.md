# Root Causes of Eval Suite Success

## The Fundamental Problem: x/x = 1

Any agent that writes both the skill and the evals will converge to 100%.
Not because the skill improved — because x/x = 1 is a mathematical identity, not a measure.

The entire autoresearch loop as commonly implemented is **only useful for the 0→~1% range**:
going from "skill doesn't exist" to "skill passes tests its author anticipated."

Beyond that, the loop is circular reasoning dressed as optimization.

---

## The Escape Condition

Excellence requires **a denominator you did not define**.

Three valid denominators:

| Denominator source | Why it works |
|-------------------|-------------|
| **Real task ground truth** — known correct answers (math proofs, compiler output, test suites) | You cannot manufacture a pass — the answer is right or wrong |
| **Adversarial evaluator** — an agent that never saw the skill, given the same inputs | It will find failures the author normalized away |
| **Unseen input distribution** — inputs drawn from real usage logs, not designed by the skill author | You can't overfit to inputs you haven't seen |

All three share the same property: **the agent scoring cannot rig the denominator to match the numerator.**

---

## Revised Root Causes (post x/x insight)

### RC-0 (new, highest priority): Denominator Independence
The max score must not be reachable by the agent who wrote the evals.
If the author can make x = max through iteration, the eval suite is worthless above 1%.

Practical implementation:
- Use ground truth (compiler, math verifier, known answer key) as scorer
- Use a blind evaluator agent (different session, no skill context)
- Hold out a test set the author never sees during optimization
- Score failures on real user inputs — denominator is "all possible inputs in domain" (∞)

### RC-1: Binary Precision
Pass/fail only. Scales give the author room to manufacture middle-ground scores.

### RC-2: Adversarial Expansion (revised)
100% is not a ceiling to expand — it's a **tautology alarm**. The response is not to add more evals. It's to **replace the evaluator** with one that didn't see the skill.

### RC-3: Test Input Diversity (revised)
Diversity within author-designed inputs still leaves x/x = 1 reachable. True diversity = inputs the author did not design. Draw from real usage, random generation with ground truth, or adversarial generation.

### RC-4: Eval → Mutation (unchanged)
Every failing eval implies exactly one skill change. If you can't name the mutation, the eval is bad.

### RC-5: Evals Grow Harder (revised)
"Harder" means the new evals were not written by the same agent who wrote the skill. Author-designed hard evals are still x/x = 1.

### RC-6: Names Are Claims (unchanged)
4-word capability claim. No vague nouns.

### RC-7: Anti-Patterns > Virtues (unchanged)
"Avoids X" beats "is Y."

### RC-8: Worked Examples (unchanged)
Concrete pass + fail example in every eval.

### RC-9: Behavior Not Text (unchanged)
"Would an agent do X?" not "Does the skill mention X?"

### RC-10: Principled Stop (revised)
Stop when the **external** failure rate drops below threshold — not when you hit 100% on your own evals.
True stop: failure rate < target% on unseen inputs from a source you don't control.

---

## What Internally-Consistent Autoresearch Actually Measures

The gain from a self-referential autoresearch loop:
- Skill goes from 0% to ~passing-author's-evals%
- This captures: "does the skill articulate its own intent?"
- This does NOT capture: "does the skill produce excellent agent behavior in the wild?"

The gap between those two things is where excellence lives.

---

## Practical Hierarchy for Eval Independence

```
Best:  External ground truth (compiler, test suite, math verifier, known answer key)
Good:  Blind adversarial agent (separate session, no skill context, same inputs)
OK:    Held-out inputs (author designed them but committed to not seeing during optimization)
Weak:  Author-designed expanding eval suite (x/x = 1 achievable, useful only 0→1%)
Worst: Author evaluates their own outputs (pure x/x = 1)
```

Build toward Best. Use Weak only to bootstrap from zero.
