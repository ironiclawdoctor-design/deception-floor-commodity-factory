# Want Audit — TurboQuant Pre-Deployment Check

## Total hits: 23

## By classification:
VALIDATED: 5 | SPECULATIVE: 2 | STRUCTURAL: 16 | DEAD: 0

## Recommendation: CONDITIONAL

## Condition (if CONDITIONAL):
Two speculative "want" hits must be resolved before TurboQuant / KV cache compression is added to the inspiration pool:

1. **`skills/onlyshans/SKILL.md:42`** — "someone wants something → article topic, product idea"
   Condition: `grep -c "lust" /root/.openclaw/workspace/skills/onlyshans/*.jsonl 2>/dev/null` must return >0 confirmed demand signals mapped to at least one validated product outcome. Until then, this inference is ungrounded.

2. **`skills/shannode/references/glp-gatekeeper-design-doc.md:28`** — "exactly the people GLP wants"
   Condition: Verify GLP targeting criteria exists in a config or design doc with an explicit target-user definition. Run: `grep -rn "target_user\|ideal_user\|target audience" /root/.openclaw/workspace/skills/shannode/ 2>/dev/null`. If no match, this claim is unsupported.

## Notes
- 16/23 hits are STRUCTURAL — internal skill anti-patterns, code strings, quoted forbidden phrases. Zero risk.
- 5/23 hits are VALIDATED — grounded in observed user behavior, lean methodology, or named-user profile data.
- 0 DEAD entries — no deprecated contexts found.
- The two SPECULATIVE hits are isolated to `onlyshans` and `shannode` skills, not in routing logic or core agent config. They do not block TurboQuant integration directly, but represent unresolved demand assumptions that could pollute inspiration scoring if those skills feed the pool.

**PROCEED on TurboQuant core integration. HOLD on any inspiration-pool ingestion from `onlyshans` or `shannode` until conditions above are bash-verified.**
