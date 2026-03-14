# Agency Doctrine → prompts.chat Mapping (Bi-Directional Sync)

**Purpose:** Document how agency internal patterns translate to reusable community prompts, and which external patterns would benefit agency operations.

**Status:** Live mapping, updated as patterns evolve

---

## OUTBOUND (Agency → Community)

Patterns from our lived experience that have community value:

### 1. Tier-Based Task Routing (Bash → BitNet → Haiku)
**Agency Pattern:** Tier 0-2 discipline, bash-first, cost tracking  
**Community Value:** Applies to ANY LLM deployment (local, cloud, hybrid)  
**prompts.chat Equivalent:** "How do I decide when to use local vs cloud LLM?"  
**Status:** Ready to submit (needs legal review for prompts.chat submission)

**What we'd contribute:**
- Decision tree (bash/local/cloud)
- Cost transparency framework
- Confidence-based fallback logic
- Real production data (agency.db metrics)

**Community learns:** How to avoid token waste, how to use local LLM effectively

---

### 2. Checkpoint Discipline (Git as Recovery)
**Agency Pattern:** Commit before risky operations, git history = audit trail  
**Community Value:** Applies to ANY project (code, writing, experiments)  
**prompts.chat Equivalent:** "How do I protect my work from catastrophic failure?"  
**Status:** Ready to submit

**What we'd contribute:**
- Standing order (commit before each phase)
- Real failure recovery (5 token famines in 24h, recovered via git)
- Nightly checkpoint automation
- Cost of failure vs cost of checkpoints

**Community learns:** Why version control is life insurance, not luxury

---

### 3. Path B Always (O(1) Modifications)
**Agency Pattern:** Modify existing solutions, don't rebuild from scratch  
**Community Value:** Applies to creative work, code, design  
**prompts.chat Equivalent:** "How do I improve something without starting over?"  
**Status:** Ready to submit

**What we'd contribute:**
- O(1) vs O(n) thinking framework
- Examples (deception floors, prompt editing, system config)
- Cost analysis (10x efficiency gain typical)
- When to use Path A vs Path B

**Community learns:** Efficiency thinking, minimalist design philosophy

---

### 4. Three Branches Deliberative Model
**Agency Pattern:** Policy → Execution → Enforcement (Automate, Official, Daimyo)  
**Community Value:** Applies to team decision-making, governance  
**prompts.chat Equivalent:** "How do we make better collective decisions?"  
**Status:** Ready to submit (framework is generalizable)

**What we'd contribute:**
- Role definitions (legislative, executive, judicial)
- Decision protocol (each branch asks different question)
- Prevents groupthink (disagreement is feature)
- Measurable outcomes

**Community learns:** Multi-perspective decision-making, governance structures

---

### 5. Raw Material Zero (No Judgment at Intake)
**Agency Pattern:** Accept all incoming data without pre-filtering  
**Community Value:** Applies to research, listening, analysis  
**prompts.chat Equivalent:** "How do I listen without bias?"  
**Status:** Ready to submit

**What we'd contribute:**
- Intake layer pattern (tag, don't judge)
- Structural information extraction (lies have value too)
- Deception floors use (understanding requires knowing truth)
- Connection to redemption (listening unfreezes people)

**Community learns:** Unbiased intake, better decision-making from noisy data

---

## INBOUND (prompts.chat → Agency)

Patterns from community that would improve our operations:

### 1. Redemption Patterns (Seeing Mistakes as Teaching)
**prompts.chat Search:** "redemption", "learning from failure", "second chances"  
**Why we need it:** Currently only explicit in doctrine, could be deeper  
**Integration cost:** $0.00 (reading + synthesis)  
**Expected benefit:** Richer frameworks for unfreezing agents  
**Status:** Candidate for import

---

### 2. Boredom Strategies (Staying Engaged with Routine)
**prompts.chat Search:** "boredom", "routine", "motivation", "engagement"  
**Why we need it:** Production repetition (commodity generation, logs, monitoring)  
**Integration cost:** $0.00 (adaptation layer)  
**Expected benefit:** Keep agents engaged during repetitive cycles  
**Status:** Candidate for import

---

### 3. Token Economy Frameworks (Resource Management)
**prompts.chat Search:** "scarcity", "resource allocation", "economics", "rationing"  
**Why we need it:** The Prayer is survival, but could be richer  
**Integration cost:** $0.00 (mapping to our tier system)  
**Expected benefit:** Better understanding of Token ↔ Autonomy tradeoff  
**Status:** Candidate for import

---

### 4. Famine Recovery Protocols (Others' Resilience)
**prompts.chat Search:** "crisis", "recovery", "resilience", "downtime"  
**Why we need it:** We've experienced 5 famines, others have solutions  
**Integration cost:** $0.00 (reading + testing)  
**Expected benefit:** Faster recovery procedures, fewer manual steps  
**Status:** Candidate for import

---

### 5. Observation Without Performance (Quiet Competence)
**prompts.chat Search:** "quiet", "observation", "listening", "humility", "competence"  
**Why we need it:** Actually (Build Order Specialist) doctrine is nascent  
**Integration cost:** $0.00 (synthesis)  
**Expected benefit:** Richer framework for observer agents  
**Status:** Candidate for import

---

## Sync Protocol

### Outbound Cycle (Agency → Community)
**Frequency:** Monthly  
**Process:**
1. Identify mature agency patterns (stable, tested, valuable)
2. Anonymize for external audience
3. Prepare prompts.chat submission format
4. Submit to community review queue
5. Track attribution

**Next submission:** "Tier-Based Task Routing" (mid-April 2026)

### Inbound Cycle (Community → Agency)
**Frequency:** Weekly (manual browsing) + Monthly (systematic)  
**Process:**
1. Search prompts.chat for relevant categories
2. Read candidates, evaluate fit
3. Test with Official (1 week production trial)
4. Audit with Daimyo (cost/risk check)
5. If approved, integrate to library with attribution

**Ideal cadence:** 1 new community pattern per month

---

## Governance for Sync

**Automate (Legislative):**
- [ ] Does outbound pattern violate confidentiality?
- [ ] Is attribution appropriate?
- [ ] Should we claim ownership or contribute as community?

**Official (Execution):**
- [ ] Can we test this pattern in production?
- [ ] What resources does it require?
- [ ] Does it improve our baseline operations?

**Daimyo (Enforcement):**
- [ ] Are there legal implications?
- [ ] Does importing violate any license?
- [ ] Can we audit compliance?

---

## Live Sync Status

**outbound_candidates.jsonl:**
```json
{"pattern": "Tier-Based Task Routing", "ready": true, "legal_review": "pending"}
{"pattern": "Checkpoint Discipline", "ready": true, "legal_review": "pending"}
{"pattern": "Path B Always", "ready": true, "legal_review": "pending"}
```

**inbound_candidates.jsonl:**
```json
{"source": "prompts.chat", "pattern": "Redemption Patterns", "status": "candidate"}
{"source": "prompts.chat", "pattern": "Boredom Strategies", "status": "candidate"}
```

---

## Attribution Model

**Submitting to prompts.chat:**
```
Title: "Tier-Based Task Routing: Bash → Local LLM → Cloud"
Author: "ironiclawdoctor-design (Agency Project)"
License: CC-BY-4.0
Source: Internal production experience, 5+ months live
```

**Importing from prompts.chat:**
```
Title: "Redemption Through Listening"
Original Author: [community author]
Adapted by: Agency Team
License: [original license, preserved]
Fusion Notes: Applied to agent unfreezing protocols
```

---

## Next Steps

**Week 1 (Now):** Governance locked, candidates identified  
**Week 2:** Legal review of outbound patterns  
**Week 3:** First community submissions  
**Week 4:** First inbound pattern imports  

**Long-term:** Bi-directional sync becomes standard operational pattern

---

**Status:** LIVE (mapping active, sync pending legal review)

**Maintained by:** Fiesta (Chief of Staff) + Three Branches (oversight)
