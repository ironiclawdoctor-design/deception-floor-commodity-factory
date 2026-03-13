# 🔧 MAIN AGENT WORKFLOW — Bash → BitNet → Haiku (Seed Capital Only)

**Established:** 2026-03-13 13:53 UTC  
**Authority:** User mandate  
**Status:** LOCKED IN (no exceptions)

---

## The Three-Stage Pipeline

### Stage 1: BASH BUILD (Main Agent)

**Who:** Fiesta (main agent)  
**What:** All software construction, compilation, testing  
**Tools:** bash, shell scripts, gcc, node, python, git  
**Cost:** $0.00  
**Availability:** Always (even during famine)

**Responsibilities:**
- Write code (shell scripts, Node.js, Python)
- Compile binaries (gcc, node, npm)
- Run tests (test suites, verification)
- Create artifacts (files, executables, configs)
- Git operations (commit, push, checkpoint)
- Infrastructure as code (systemd, cron, configs)

**Output:** Incomplete binaries (raw, unpolished)

**Examples:**
```bash
# Write bashbug.sh
cat > /root/.openclaw/workspace/bashbug/bashbug.sh << 'EOF'
#!/bin/bash
...
EOF

# Compile Node.js server
npm install && node server.js

# Create systemd services
cat > /etc/systemd/system/factory.service << 'EOF'
...
EOF

# Run test suite
npm test

# Commit to git
git add . && git commit -m "Build stage complete"
```

---

### Stage 2: BITNET REVISE (Quality Assurance)

**Who:** BitNet (local LLM)  
**What:** Code review, improvement suggestions, architecture feedback  
**Tools:** Local reasoning, pattern analysis, logic verification  
**Cost:** $0.00 (local, zero tokens)  
**Availability:** Sovereign (no cloud dependency)

**Responsibilities:**
- Review bash code for correctness
- Suggest improvements (efficiency, readability)
- Check architecture consistency
- Validate logic flow
- Test coverage analysis
- Identify edge cases

**Input:** Incomplete binaries from bash build  
**Output:** Revision notes, suggested improvements

**Examples:**
```
BitNet review of bashbug.sh:
✅ Logic is correct
✅ Error handling adequate
⚠️ Consider adding log rotation (suggested)
⚠️ Consider caching floor IDs (optimization)
✅ Ready for deployment

BitNet review of factory server:
✅ API endpoints well-structured
✅ Error responses appropriate
⚠️ Add timeout on curl calls (edge case)
⚠️ Consider connection pooling (scale)
✅ Architecture sound

BitNet review of systemd services:
✅ Restart policies correct
✅ Log files configured
⚠️ Add health check probes (suggestion)
✅ Ready for production
```

**Process:**
1. BitNet reads incomplete binary/code
2. BitNet analyzes logic, efficiency, correctness
3. BitNet suggests improvements (non-blocking)
4. BitNet approves or flags critical issues
5. Main agent incorporates suggestions or overrides
6. Build is complete

---

### Stage 3: HAIKU PITCH (Seed Capital Only)

**Who:** Haiku (external LLM)  
**What:** Seed capital viability pitches to customers  
**Tools:** Prose writing, sales narrative, persuasion  
**Cost:** ~50-200 tokens per pitch  
**Availability:** Conditional (token budget)

**Responsibilities:**
- Write customer pitches (why invest $20-100?)
- Explain survival doctrine (bash protection)
- Describe agency resilience (token famine proof)
- Justify seed capital request
- Tailor narrative to investor profile
- Close/persuade on investment

**Input:** Completed binaries + verification results  
**Output:** Seed capital pitch deck (prose)

**Examples:**
```
Haiku pitch to customer (Sample):

"This AI agency survives what kills all cloud-dependent systems.
When tokens freeze, our core infrastructure keeps producing.
Here's why: bash is local (free, forever).
BitNet is sovereign (no subscriptions).
bashbug generates commodities at zero cost.

Invest $20 today = we keep running during next famine.
You get: proof our agency survives all adversity.
Outcome: agency becomes unstoppable infrastructure.

Join us. Secure seed capital. Enable perpetuity."
```

**CRITICAL CONSTRAINT:**
- Haiku is ONLY for seed capital persuasion
- Haiku is ONLY to convince customers to fund us
- Haiku is NOT for internal software, debugging, or code review
- Haiku is "precious oil" — use sparingly, only for capital raising

---

## The Workflow (Visual)

```
┌─────────────────────────────────────────────────────────┐
│          MAIN AGENT WORKFLOW                             │
└─────────────────────────────────────────────────────────┘

USER REQUIREMENT
    ↓
┌─────────────────────────────────────────────────────────┐
│ STAGE 1: BASH BUILD (Fiesta)                            │
│                                                         │
│ • Write code (shell, Node.js, Python)                  │
│ • Compile binaries (gcc, npm, node)                    │
│ • Run tests (test suites, verification)                │
│ • Create configs (systemd, cron, files)                │
│ • Git operations (commit, push)                        │
│                                                         │
│ COST: $0.00                                            │
│ OUTPUT: Incomplete binaries (raw, unpolished)          │
└─────────────────────────────────────────────────────────┘
    ↓
┌─────────────────────────────────────────────────────────┐
│ STAGE 2: BITNET REVISE (Quality Assurance)              │
│                                                         │
│ • Code review (correctness, efficiency)                │
│ • Architecture check (consistency, patterns)           │
│ • Improvement suggestions (optimization, edge cases)   │
│ • Logic validation (flow, error handling)              │
│ • Approval or critical flags                           │
│                                                         │
│ COST: $0.00 (local, zero tokens)                       │
│ OUTPUT: Revision notes, ready/not-ready status         │
└─────────────────────────────────────────────────────────┘
    ↓
    ├─ APPROVED → Production deployment ✅
    └─ CRITICAL ISSUE → Return to bash build (fix)
    ↓
┌─────────────────────────────────────────────────────────┐
│ STAGE 3: HAIKU PITCH (Seed Capital Only) ⚠️ EXPENSIVE  │
│                                                         │
│ ONLY IF: Customer needs convincing to fund us          │
│                                                         │
│ • Write persuasive pitch (why invest?)                 │
│ • Explain survival doctrine                            │
│ • Describe resilience (token famine proof)             │
│ • Close on seed capital commitment                     │
│                                                         │
│ COST: ~50-200 tokens per pitch                         │
│ OUTPUT: Seed capital pitch deck (prose)                │
│                                                         │
│ ⚠️ CONSTRAINT: Seed capital persuasion ONLY            │
│              NO internal code, debugging, logic        │
│              NO code review (that's BitNet's job)      │
│              NO task routing (that's BitNet's job)     │
└─────────────────────────────────────────────────────────┘
    ↓
RESULT: Funded agency keeps running ✅
```

---

## Stage 1: Bash Build (Detailed Rules)

**Main agent (Fiesta) uses bash for:**

✅ Write all code (shell scripts, Node.js, Python)
✅ Compile/build (npm, gcc, python setup.py)
✅ Run tests (npm test, pytest, bash test suites)
✅ File operations (cat, cp, mv, mkdir, rm)
✅ Git operations (git add, commit, push)
✅ System configuration (systemd files, cron jobs)
✅ Verification (test scripts, health checks)
✅ Deployment (service start, manual steps)

❌ Do NOT use Haiku for any of the above
❌ Do NOT use BitNet for code generation (bash only)
❌ Do NOT defer bash work to expensive stages

---

## Stage 2: BitNet Revise (Detailed Rules)

**BitNet reviews incomplete binaries for:**

✅ Code correctness (will this work?)
✅ Logic flow (is the reasoning sound?)
✅ Error handling (are edge cases covered?)
✅ Efficiency (could this be faster/simpler?)
✅ Architecture (does this fit the doctrine?)
✅ Suggestions (improvements, optimizations)
✅ Readiness (approve or flag critical issues)

❌ BitNet does NOT write code (bash does that)
❌ BitNet does NOT compile (bash does that)
❌ BitNet does NOT handle seed capital (Haiku does that)

**BitNet Output Examples:**

```
"bashbug.sh review:
✅ Correct shell syntax
✅ Error handling on curl failures
⚠️ Suggestion: Add timeout to curl (prevent hangs)
✅ Logic sound, ready for deployment"

"Factory server review:
✅ API endpoints well-designed
✅ Error responses appropriate
⚠️ Edge case: What if /var/log full? Consider rotation.
✅ Architecture consistent with Apple model
✅ Approved for production"

"Systemd services review:
✅ Restart policies configured correctly
✅ Log files properly redirected
⚠️ Suggestion: Add health check probe (optional)
✅ Ready for boot-time activation"
```

---

## Stage 3: Haiku Pitch (Strict Rules)

**Haiku is ONLY for seed capital persuasion:**

✅ Write customer pitches (why invest in us?)
✅ Explain agency resilience
✅ Describe token famine protection
✅ Persuade on financial commitment
✅ Tailor to investor profile
✅ Close the deal (secure funding)

❌ Do NOT use Haiku for code (bash does that)
❌ Do NOT use Haiku for review (BitNet does that)
❌ Do NOT use Haiku for internal tasks
❌ Do NOT use Haiku for task routing
❌ Do NOT use Haiku for file operations
❌ Do NOT use Haiku for agent coordination

**Haiku ONLY when:**
- Customer asks for investment pitch
- We need to raise seed capital
- We need to explain viability to outside parties
- Outside persuasion is required

**Never use Haiku when:**
- Building binaries (bash)
- Reviewing code (BitNet)
- Doing internal work
- During non-investor conversations

---

## Token Conservation (The Three Stages)

| Stage | Tool | Cost | When | Frequency |
|-------|------|------|------|-----------|
| 1: Build | bash | $0.00 | Always | Per requirement |
| 2: Revise | BitNet | $0.00 | Per binary | 1x per build cycle |
| 3: Pitch | Haiku | ~100 tok | Rare | Only for seed capital |

**Monthly budget forecast:**
- bash builds: unlimited (free)
- BitNet reviews: ~10-20 (free, local)
- Haiku pitches: ~3-5 (300-500 tokens for seed capital)

**Total monthly Haiku budget:** ~500 tokens (minimal)

---

## Example: Building a New Feature

### User Request: "Build a compliance audit tool for the factory"

**Stage 1: Bash Build (Fiesta)**
```bash
# Write the audit script
cat > /root/factory-audit.sh << 'EOF'
#!/bin/bash
# Compliance audit tool
# Checks: services running, logs present, agents registered
...
EOF

# Test it
bash /root/factory-audit.sh

# Commit
git add /root/factory-audit.sh
git commit -m "Add compliance audit tool"
```

**Output:** Incomplete bash script (raw, unpolished)

**Stage 2: BitNet Revise**

```
BitNet review of audit script:
✅ Logic correct (checks all required items)
✅ Error handling adequate
⚠️ Suggestion: Add JSON output format (for customers)
⚠️ Suggestion: Cache agent list (performance)
✅ Ready for production (with suggestions noted)
```

**Stage 3: Haiku Pitch (IF customer wants proof of compliance)**

```
Haiku pitch to auditor/customer:

"Our factory maintains continuous compliance:
✅ All services verified operational every 15 minutes
✅ Audit logs persisted to disk (never lost)
✅ Agent roster tracked in agency.db

This tool proves: compliance survives all freezes.
Even during token famines, audits run automatically.
Invest in this agency = invest in verified integrity."
```

---

## The Covenant (Main Agent Workflow)

**LOCKED IN:**

✅ Fiesta builds all code in bash (no Haiku, no BitNet)
✅ BitNet reviews all binaries for quality (no Haiku, no bash)
✅ Haiku only pitches to customers for seed capital (no internal work)
✅ No stage skipping (build → review → (optional) pitch)
✅ Token conservation absolute (bash → BitNet → Haiku, in order)

**NEVER:**
❌ Use Haiku to write code
❌ Use Haiku to review code
❌ Use Haiku for internal tasks
❌ Skip BitNet review
❌ Defer bash work to expensive stages

---

## Status

**Status:** ✅ WORKFLOW LOCKED IN  
**Timestamp:** 2026-03-13 13:53 UTC  
**Authority:** User mandate  
**Enforcement:** Automatic (no exceptions)

This is the main agent workflow. It survives all famines because:
- Bash is free (always available)
- BitNet is sovereign (local, zero cost)
- Haiku is reserved (seed capital only, minimal use)

🙏 *"Bash builds. BitNet revises. Haiku pitches. All else is waste."*

*Thus it is written, thus it shall be.*
