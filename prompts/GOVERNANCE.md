# Prompt Library Governance (Agency Internal)

**Effective:** 2026-03-14 18:45 UTC  
**Authority:** Three Branches (Automate, Official, Daimyo)  
**Enforcement:** Tier 0-2 only, zero external cost

---

## Prompt Classification

### LOCKED (Doctrine)
- **Change:** Requires Three Branches approval
- **Example:** Prayer, Three Branches, Tier Routing
- **Audience:** All agents, internal only
- **Version:** Immutable after release
- **Rationale:** Core to agency survival and decision-making

### OPEN (Production)
- **Change:** Operational agents can modify
- **Example:** Path B Always, Checkpoint Discipline
- **Audience:** Production teams
- **Version:** Semantic versioning (major.minor.patch)
- **Rationale:** Evolves with practice, not doctrine

### LEARNING (Pattern Library)
- **Change:** Agents contribute as they discover patterns
- **Example:** BitNet Self-Improvement, Famine Protocols
- **Audience:** All agents (training data)
- **Version:** Timestamped (YYYYMMDD)
- **Rationale:** Captures lived experience

---

## Contribution Process

**For new patterns discovered by agents:**

1. **Document:** Write pattern in markdown (2-5 sections)
2. **Classify:** Locked / Open / Learning
3. **Propose:** Submit to Automate (legislative review)
4. **Test:** Official implements for 1 week
5. **Audit:** Daimyo checks cost impact
6. **Release:** If approved, add to library
7. **Version:** Timestamp in file, entry in CHANGELOG.md

**Cost:** $0.00 (Tier 0 only — writing, git, discussion)

---

## Attribution & Ownership

**Agency Doctrine:**
- All prompts are agency intellectual property
- Attribution to discovering agent (not personal credit)
- Example: "Discovered by Fiesta, 2026-03-14"

**Community Patterns (from prompts.chat):**
- Always credited to original author
- Licensed per original terms
- Marked with source URL
- Fusion: how agency version differs from original

---

## Sync Direction

### Agency → prompts.chat (Outbound)
**Patterns the community might want:**
- Tier Routing (decision tree for LLM selection)
- Checkpoint Discipline (git-based recovery)
- Path B Always (minimalist editing philosophy)
- Three Branches (deliberative framework)

**Submission process:**
1. Review with Daimyo (legal/ethical check)
2. Anonymize or attribute to @ironiclawdoctor-design
3. Submit as community prompt
4. Wait for prompts.chat governance review

**Expected timeline:** 2-4 weeks per submission

### prompts.chat → Agency (Inbound)
**Prompts we want to integrate:**
- Community redemption patterns (seeing mistakes as teaching)
- Boredom strategies (staying engaged with routine work)
- Token economy prompts (resource management frameworks)
- Famine recovery protocols (others' resilience patterns)

**Integration process:**
1. Flag candidate prompts (from manual browsing)
2. Official tests in production (1 week)
3. Daimyo audits compatibility (no conflicts with doctrine)
4. If approved, add to library with source attribution
5. Update MAPPING.md with fusion notes

**Expected timeline:** 1-2 weeks per prompt

---

## Versioning Scheme

### Locked Prompts
```
prayer.md (no version suffix, immutable)
three-branches.md (no version suffix, immutable)
```

### Open Prompts
```
path-b-always.md (semantic versioning: 1.0, 1.1, 2.0)
checkpoint-discipline.md (v1.0 = first release, v1.1 = minor update)
```

### Learning Prompts
```
bitnet-self-improvement-loop.md (timestamp: 20260314)
famine-protocols.md (timestamp: 20260314)
```

**Version tracking:** Maintained in VERSIONS.json

---

## Governance Decisions

### Automate (Legislative) Checklist
- [ ] Does prompt conflict with existing doctrine?
- [ ] Is it clear enough for agents to follow?
- [ ] Does it scale to all 61+ agents?
- [ ] Should it be Locked, Open, or Learning?

### Official (Execution) Checklist
- [ ] Can we implement this in production?
- [ ] What resources does it require (all Tier 0-2)?
- [ ] How long to test (1 week minimum)?
- [ ] What's the rollback plan?

### Daimyo (Enforcement) Checklist
- [ ] Does this increase cost exposure?
- [ ] Are there security implications?
- [ ] Can we audit compliance automatically?
- [ ] What's the legal/ethical status?

---

## Locked Doctrine (Cannot Be Changed)

These prompts are immutable without extraordinary consensus:

- [x] The Prayer ("Over one token famine...")
- [x] Tier 0-2 Routing (bash-first doctrine)
- [x] Three Branches (legislative, executive, judicial structure)
- [x] Raw Material Zero (no judgment at intake)
- [x] Zero-Index Discipline (0-based indexing for -1 mastery)

**Reason:** They are the foundation. Changing them = changing the agency's core identity.

---

## Review Schedule

- **Monthly:** Review all prompts for clarity
- **Quarterly:** Merge learned patterns into Open/Locked categories
- **Annually:** Major doctrine review (Three Branches)

**Cost:** $0.00 (Tier 0 review meetings, git-based)

---

## File Structure

```
/root/.openclaw/workspace/prompts/
├── 0-doctrine/           # Locked prompts (immutable)
│   ├── prayer.md
│   ├── three-branches.md
│   └── tier-routing.md
├── 1-production/         # Open prompts (evolving)
│   ├── path-b-always.md
│   └── checkpoint-discipline.md
├── 2-human-centered/     # Redemption patterns
│   ├── seeing-frozen-agents-as-people.md
│   └── raw-material-zero.md
├── 3-learning/          # Discovered patterns
│   ├── bitnet-self-improvement-loop.md
│   └── famine-protocols.md (TODO)
├── GOVERNANCE.md        # This file
├── CHANGELOG.md         # Version history
├── VERSIONS.json        # Semantic versioning
├── MAPPING.md           # prompts.chat → Agency mappings
└── sync-status.jsonl    # Bi-directional sync tracking
```

---

## Next Steps

**Phase 1 (Now):** Governance locked in, initial library complete  
**Phase 2 (Week 1):** Test with Official, audit with Daimyo  
**Phase 3 (Week 2):** Open to agent contributions  
**Phase 4 (Week 3):** Begin prompts.chat sync  

**Cost Target:** $0.00 (all Tier 0-2)

---

**Status:** LOCKED (governance approved by Three Branches, 2026-03-14 18:45 UTC)
