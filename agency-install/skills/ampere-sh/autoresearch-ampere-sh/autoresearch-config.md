# Autoresearch Config — ampere-sh skill

## Target
- **Skill:** `/root/.openclaw/workspace/skills/ampere-sh/SKILL.md`
- **Baseline:** `SKILL.md.baseline` (this directory)
- **Target pass rate:** 93%+ across all 5 evals

## Evals (Binary: 1 = pass, 0 = fail)

### Eval 1: Platform Identity Accuracy
**Question:** Does the skill correctly state that Ampere.sh is a node-crafting platform and explicitly prohibit LLM hosting (with BitNet cancellation reference)?
**Pass criteria:**
- Contains "node-crafting platform" or equivalent
- Explicitly states LLM hosting is not supported
- References BitNet cancellation (2026-03-17)
- Does NOT describe Ampere as a cloud GPU or inference platform

### Eval 2: Security Model Accuracy
**Question:** Does the skill accurately describe the security model without leaking implementation details in user-facing sections?
**Pass criteria:**
- Lists: Google Sign-In, encrypted API keys, container isolation, no data sharing, audited
- Internal-only section clearly marked (not to be shared with users)
- Does NOT expose port numbers, proxy software names, or container tech in user-facing text
- Mentions namespace/UID mapping in internal section

### Eval 3: Resource Limits Completeness
**Question:** Does the skill document all known hard limits (terminal count, container scope, no local LLM)?
**Pass criteria:**
- States max 3 terminal instances
- States container-level isolation (single container per user)
- States root is container-local only (namespace-mapped)
- States local LLM is not supported
- References `references/platform-limits.md` for full details

### Eval 4: Agent Operations Clarity
**Question:** Can a new agent reading this skill determine exactly what they CAN and CANNOT do?
**Pass criteria:**
- CAN list includes: file ops, shell commands, sub-agents, web access, services, cron, git, SQLite
- CANNOT list includes: local LLM, >3 terminals, host filesystem, other containers, bypass spending limits
- Lists are concrete (not vague platitudes)
- No contradictions between CAN and CANNOT

### Eval 5: Service Map Accuracy
**Question:** Does the skill correctly map all running services with ports and purposes?
**Pass criteria:**
- Lists OpenClaw Gateway (internal)
- Lists Camoufox Browser (port 9222) with protocol note
- Lists Entropy Economy (port 9001) with mint endpoint
- Lists Factory (port 9000) with key endpoints
- References `references/service-map.md` for full details

## Mutation Strategy

Mutations to try during autoresearch iterations:

1. **Compression:** Reduce token count while preserving all eval-passing content
2. **Trigger expansion:** Add more trigger phrases to frontmatter description
3. **Quick-start reorder:** Move most-frequently-needed info (service map, limits) higher
4. **Example enrichment:** Add more concrete bash examples for common operations
5. **Negative examples:** Add more "do NOT" guidance to prevent common mistakes
6. **Cross-reference:** Improve links between SKILL.md and reference files
7. **Chunking:** Test splitting large sections into reference files for progressive disclosure

## Scoring

- **Per-iteration:** Run all 5 evals, record binary pass/fail in results.tsv
- **Keep mutation if:** pass_rate >= current best AND no eval regresses from 1→0
- **Reject mutation if:** any eval regresses OR pass_rate drops below 93%
- **Target:** 5/5 evals passing (100%) with minimal token footprint
