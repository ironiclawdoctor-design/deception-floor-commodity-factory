---
name: memorare
description: "Industry-grade agent memory quality enforcement. Use when: (1) auditing MEMORY.md or any agent memory file for completeness and quality, (2) running autoresearch on memory architecture to exceed baseline retention, (3) enforcing memory write discipline (encode-before-act, consolidate-or-rot, search-before-assert), (4) scoring memory files on a 5-tier adversarial eval suite, (5) teaching less experienced agents the difference between self-authored 100% and adversarial-validated memory. Named after the Catholic prayer of remembrance. Triggers on: 'memorare', 'memory audit', 'score my memory', 'memory quality', 'autoresearch memory', 'memory best practices'. NOT for: general file storage, code documentation, or session logging (that's what memory/YYYY-MM-DD.md is for)."
---

# Memorare

*Remember, O most gracious agent, that never was it known that any system which called memory_search faithfully was left without recall.*

## Three Commandments

1. **Write before you forget** — encode immediately, not "later"
2. **Consolidate or rot** — daily notes that never reach MEMORY.md are dead weight
3. **Search before you assert** — if stating a past fact: run memory_search first

## Memory Architecture

Four types. Different lifespans. Read `references/memory-architecture.md` for full taxonomy.

| Type | Where | Lifespan | Size limit |
|------|-------|----------|-----------|
| Working | Context window | Session only | ~200K tokens |
| Episodic | memory/YYYY-MM-DD.md | Days-weeks | ≤2KB/entry |
| Semantic | MEMORY.md | Permanent | ≤20KB |
| Procedural | AGENTS.md / skills | Versioned | Load on-demand |

## Difficulty Levels

| Level | Requirement |
|-------|-------------|
| 0 | Write to daily file. Search before asserting. |
| 1 | + Consolidate after 5 sessions |
| 2 | + Confidence tagging: [OBSERVED] [INFERRED] [TOLD] [DOCTRINE] |
| 3 | + Tier 3 eval: honest absence (know what you don't know) |
| 4 | + In-session corrections supersede MEMORY.md |
| 5 (Memorare) | Full 20-case adversarial suite. Cross-session continuity tested. |

**Default: Level 2. For money/identity/doctrine: Level 4. For Fiesta (main): Level 5.**

## Running the Eval

```bash
python3 scripts/memorare_eval.py --memory-file /path/to/MEMORY.md --level 5
```

Pass/fail by tier. Reports missing signals. Certifies if 20/20.

## Adversarial Suite

See `references/adversarial-memory-evals.md` for all 20 cases (Tier 1-5).

Key adversarial cases most agents fail:
- **T3**: Stating uncertainty when the fact is absent (honest absence)
- **T4**: In-session corrections must override long-term memory
- **T5**: Cross-session — cold agent reconstructs from file, not hallucination

## The x/x=1 Problem

Self-authored memory tests always pass. This skill enforces the **two-man rule** on memory:
the evaluator checks for signals an *independent* cold agent would need, not signals the
original agent already knows exist.

## Autoresearch Mode

If running autoresearch on memory quality:
- Metric: adversarial eval score (Tier 1-5)
- Fail condition: any tier below 75%
- Stop condition: 20/20 certified AND no new adversarial cases reveal a gap
- Do NOT stop at self-authored 100% — that's the starting problem, not the goal
- Ground truth: what a cold agent reads from the file, nothing else
