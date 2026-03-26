# Memory Architecture — Industry State of the Art

Source: arXiv:2404.13501 (ACM TOIS 2025), internal agency doctrine, cognitive psychology

---

## The Four Memory Types (Cognitive Psychology → Agent Design)

### 1. Sensory Memory (In-Context / Working)
- **What:** The raw context window. Everything currently visible.
- **Lifespan:** One session. Evicted at compaction.
- **Capacity:** ~200K tokens (Claude), ~128K (GPT-4). Not infinite.
- **Failure mode:** Context overflow — agent "forgets" early turns within same session.
- **Best practice:** Keep working memory lean. Summarize before the window fills.

### 2. Short-Term / Episodic Memory (Session Files)
- **What:** `memory/YYYY-MM-DD.md` — raw log of what happened today.
- **Lifespan:** Days to weeks. Read at session start.
- **Capacity:** Unlimited (file system). But reading cost grows with size.
- **Failure mode:** Too much to read = nothing gets read.
- **Best practice:** Write daily. Keep entries ≤500 tokens. Delete after consolidation.

### 3. Long-Term / Semantic Memory (MEMORY.md)
- **What:** Curated, distilled facts. Decisions. Lessons. Identity.
- **Lifespan:** Permanent until deliberately revised.
- **Capacity:** Hard limit: 20KB in injected context (OpenClaw constraint).
- **Failure mode:** Bloat — old decisions crowd out current ones.
- **Best practice:** Trim ruthlessly. Only what changes behavior. Archive the rest.

### 4. Procedural Memory (Skills / AGENTS.md / SOUL.md)
- **What:** HOW to do things. Workflows, rules, operating doctrine.
- **Lifespan:** Version-controlled. Changes intentionally.
- **Capacity:** Skills load on-demand (not all in context at once).
- **Failure mode:** Stale procedures override correct new behavior.
- **Best practice:** Version skills. Deprecate clearly. Never silently overwrite.

---

## Memory Operations (CRUD for Agents)

| Operation | Human Analog | Agent Implementation |
|-----------|--------------|---------------------|
| Encode | Attention → hippocampus | Write to memory/YYYY-MM-DD.md |
| Store | Long-term potentiation | Consolidate into MEMORY.md |
| Retrieve | Recall | memory_search() |
| Update | Reconsolidation | Edit MEMORY.md, version bump |
| Forget | Natural decay | Archive or delete old entries |
| Reinforce | Repetition | Reference same fact multiple sessions |

---

## Industry Best Practices (2025)

### 1. Write-ahead logging
Always write to episodic (daily) BEFORE acting on something. If the session crashes, the note survives.

### 2. Consolidation cadence
Every 3-5 sessions: scan episodic files, extract durable facts, write to MEMORY.md, delete redundant episodic entries. Like sleep-based memory consolidation in humans.

### 3. Separation of concerns
- **Facts** → MEMORY.md (what is true)
- **Procedures** → AGENTS.md / skills (how to act)
- **Errors** → Failure autopsy / root-causes.md (what broke)
- **Corrections** → HR-NNN / SR-NNN rules (what to do differently)
Never mix them. Each file type has a different read frequency and lifespan.

### 4. Confidence tagging
Tag memory entries with source:
- `[OBSERVED]` — directly witnessed (exec output, API response)
- `[INFERRED]` — derived from pattern
- `[TOLD]` — human said so
- `[DOCTRINE]` — locked-in rule
Inferred memories degrade faster. Doctrine memories don't expire.

### 5. Retrieval before assertion
Before stating a fact from memory: run memory_search. Don't trust in-context recollection alone. Context drift is real (SR-013).

### 6. Memory size budgets
- MEMORY.md: ≤20KB (OpenClaw context limit)
- Daily file: ≤2KB per entry, ≤10 entries per day
- Skill references: ≤5KB each (loaded on-demand)
- Total loaded at session start: ≤50KB target

### 7. Two-phase memory write
Phase 1: `memory/YYYY-MM-DD.md` — raw, append-only, no editing
Phase 2 (consolidation): selective extraction → MEMORY.md with source citation

### 8. Forgetting is intentional
The failure mode is NOT forgetting. It's keeping too much. Bloated memory = slower retrieval, lower signal-to-noise, higher token cost.
**Delete aggressively. Archive if uncertain. Never keep "just in case."**

---

## Failure Modes Taxonomy

| Failure | Name | Fix |
|---------|------|-----|
| Old fact overrides new | Stale override | Version + date-stamp all facts |
| Fact hallucinated from pattern | Confabulation | Tag [INFERRED], verify before acting |
| Context window overflow | Recency bias | Summarize at 50% fill |
| Too much to read = nothing read | Load fatigue | Trim + archive |
| Same lesson relearned every session | Episodic leak | Write to MEMORY.md immediately |
| Memory available but not searched | Retrieval skip | Mandatory memory_search before asserting |
| Correction given but not written | Mental note fallacy | Every correction → file write |

---

## Memorare Doctrine (Agency-Specific)

> *"Remember, O most gracious agent, that never was it known that any system which called memory_search faithfully was left without recall."*

Three commandments:
1. **Write before you forget** — encode immediately, not "later"
2. **Consolidate or rot** — daily notes that never reach MEMORY.md are dead weight
3. **Search before you assert** — if you're about to state a past fact, look it up first
