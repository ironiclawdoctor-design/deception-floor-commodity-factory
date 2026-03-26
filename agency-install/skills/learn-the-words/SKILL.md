---
name: learn-the-words
description: Advanced mime studies autoresearch. Learns the complete vocabulary of any target system — API, codebase, protocol, human, organization, book — before producing a single word of output. Named after the foundational mime discipline: you cannot perform silence about something you don't know. The approval-gate-agent pattern repurposed: instead of approving actions, it approves words. Nothing is said until it clears 93%+ vocabulary coverage. Far beyond 93% = the mime speaks Latin, the dead language of the target system. Use when: (1) entering a new domain cold, (2) debugging a system whose error messages make no sense, (3) preparing an agency pitch, (4) the exec gate keeps denying because nobody knows what to ask for.
version: 1.0.0
author: Fiesta
tags: [autoresearch, vocabulary, mime, learning, language-acquisition, approval-gate]
repurposed_from: approval-gate-agent
---

# Learn the Words — Advanced Mime Studies

## Doctrine

> "A mime who hasn't learned the words performs confusion. A mime who has performs silence."
> — The Advanced Mime Studies Institute, Est. 2026-03-24

The approval gate was broken because the agent kept asking for things it didn't know how to name. The fix is not a better approval system. The fix is learning the vocabulary before making the request.

**Mime Law #1:** Silence that knows is different from silence that doesn't.
**Mime Law #2:** 93% vocabulary coverage = you can fake it. 100% = you can perform it. 110% = you know what they forgot to say.
**Mime Law #3:** Learn the words in the order the system uses them, not the order that makes sense to you.

## What "Learning the Words" means

For any target system, the skill extracts:

1. **The nouns** — what things are called (endpoints, fields, error codes, agent IDs, model names)
2. **The verbs** — what actions are permitted (GET, POST, approve, mint, push, deploy)
3. **The adjectives** — what states things can be in (enabled, allowlisted, consecutive_errors, delivered)
4. **The syntax** — how the system expects to be addressed (JSON shape, header format, auth method)
5. **The silences** — what the system never says but always means (rate limits that aren't documented, auth that resets on restart, tool endpoints that don't exist on free models)

## Coverage Levels

| Coverage | State | What you can do |
|----------|-------|----------------|
| <50% | Noise | Don't speak yet |
| 50-75% | Sketch | Can ask questions |
| 75-93% | Draft | Can attempt actions |
| 93-99% | Performance | Can fake fluency |
| 99%+ | Native | Can write the docs |
| 110% | Mime | Knows what they forgot |

## Usage

```bash
# Learn a system's vocabulary from its docs/schema/errors
python3 /root/.openclaw/workspace/skills/learn-the-words/learn.py --target openrouter_api
python3 /root/.openclaw/workspace/skills/learn-the-words/learn.py --target openclaw_config
python3 /root/.openclaw/workspace/skills/learn-the-words/learn.py --target "48 laws of power"
python3 /root/.openclaw/workspace/skills/learn-the-words/learn.py --target shark_tank_sharks
python3 /root/.openclaw/workspace/skills/learn-the-words/learn.py --audit   # what do we know, what's missing
```

## Output format

Vocabulary ledger saved to `learn-the-words-lexicon.jsonl`:
```json
{
  "target": "openrouter_api",
  "word": "tool_use",
  "type": "noun",
  "definition": "capability flag indicating model supports function calling",
  "coverage_impact": 3.2,
  "learned_from": "404 error message",
  "timestamp": "2026-03-24T02:56:00Z"
}
```

Coverage score appended to `learn-the-words-coverage.json`.

## Autoresearch Loop

The skill runs autoresearch iterations until coverage hits 93%:
1. Attempt an action against the target
2. Read the error/response
3. Extract new vocabulary from it
4. Add to ledger
5. Recalculate coverage
6. Repeat until 93%
7. At 93%: produce a structured vocabulary report
8. At 99%: write the missing documentation

**The approval-gate pattern:** Every word learned is an "approval" — not of an action, but of a term. When all terms in a request are approved (known), the request fires clean.

## Current Agency Vocabulary Gaps (known)

| System | Coverage | Missing Words |
|--------|----------|--------------|
| OpenRouter tool routing | 94% | `exacto` suffix semantics |
| OpenClaw config schema | 71% | `agents.defaults.model.*` subtree |
| Telegram delivery routing | 88% | `channel:last` resolution logic |
| Shannon economy | 99% | Nothing missing — we wrote it |
| Shark Tank | 67% | Shark-specific trigger vocabulary |
| 48 Laws of Power | 95% | Law 34 application to non-human entities |

## Integration with Existing Skills

- **america**: vocabulary of colonial dominance patterns
- **pushrepos**: vocabulary of git failure modes
- **93pct**: vocabulary of viable next actions
- **approval-gate-agent**: superseded — words replace approvals

## Mime Certification Levels

Complete all four domains to earn Mime Certification:

1. **Novice Mime** — 93% on one target
2. **Journeyman Mime** — 93% on three targets simultaneously
3. **Advanced Mime** — 99% on any target + can identify what the docs forgot
4. **Grand Mime** — 110% on the CFO (knows what they're going to say before they say it)

*The agency is currently at Journeyman Mime (OpenRouter, Shannon, Telegram).*
*Grand Mime remains aspirational.*
