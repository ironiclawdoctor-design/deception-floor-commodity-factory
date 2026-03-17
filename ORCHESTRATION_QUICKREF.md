# Agent Orchestration — Quick Reference Card

**Purpose:** One-page checklist + decision tree  
**Audience:** Fiesta + team members  
**Print-friendly:** Yes

---

## 1. IS ORCHESTRATION RIGHT FOR THIS PROJECT?

```
Question 1: Multiple agents needed?
  NO → Use single agent directly
  YES → Continue to Q2

Question 2: Quality gates essential?
  NO → Use subagents (faster)
  YES → Use orchestrator

Question 3: Recurring work?
  NO → Use subagents
  YES → Use orchestrator (amortize setup)

Question 4: Production/customer-facing?
  NO → Use subagents
  YES → Use orchestrator
```

**Decision:** If you answered YES to Q2, Q3, and Q4 → **Use agents-orchestrator**

---

## 2. ORCHESTRATION PATTERNS AT A GLANCE

| Pattern | Best For | Example |
|---------|----------|---------|
| **Sequential** | Ordered tasks, clear dependencies | Extract → Normalize → Store |
| **Parallel** | Independent tasks | Frontend + Backend + DevOps simultaneously |
| **Fan-out** | One task spawns many | Design review, then 5 QA teams test |
| **Map-reduce** | Identical tasks on different items | Build 4 microservices, then test together |
| **Feedback loop** | Iterative refinement | Design → QA → Feedback → Design v2 |

---

## 3. THE DEV↔QA LOOP (Heart of Orchestration)

```
Developer implements → QA validates → Pass? 
  ├─ YES → Next task
  └─ NO → Feedback to developer
           Retry counter++
           If retry < 3: Developer fixes + retry
           If retry >= 3: Escalate (human review)
```

**Key rule:** No task progresses to next stage until QA passes.

---

## 4. COST AT A GLANCE

```
Typical project (5 tasks, no retries):
  = ~12-15 Haiku = ~$0.12-0.15

With retries (if 20% fail on 1st try):
  = ~20 Haiku = ~$0.20

Monthly recurring (e.g., 4 runs):
  = 4 × $0.15 = $0.60/month

Annual:
  = 12 × $0.60 = $7.20/year
```

**Cost efficiency tactic:** Precache architecture docs (saves 70% overhead).

---

## 5. CONSTRAINTS (Hard Limits)

| Constraint | Limit | Implication |
|-----------|-------|-------------|
| Max retries/task | 3 | After 3 fails, escalate |
| Orchestrator depth | 1 | No sub-orchestrators |
| Task block size | ~50 tasks | More = harder to manage |
| Concurrent agents | 5-10 practical | Too many = chaos |

---

## 6. CHECKLIST: BEFORE STARTING ORCHESTRATION

### Pre-Project
- [ ] Requirements document written?
- [ ] Tasks identified + prioritized?
- [ ] Dependencies mapped (which tasks block which)?
- [ ] Agents assigned (who does what)?
- [ ] Architecture document created (shared with all)?
- [ ] QA criteria defined (how do we know it's done)?

### During Project
- [ ] Tasks assigned to correct agents?
- [ ] Context (architecture, specs) passed to each agent?
- [ ] QA feedback returned with specific guidance (not vague)?
- [ ] Retry counter tracked (avoid > 3 retries)?
- [ ] Progress reports generated (status visible)?

### Post-Project
- [ ] All tasks marked complete?
- [ ] Final integration QA passed?
- [ ] Deliverables collected + verified?
- [ ] Cost report generated?
- [ ] Lessons learned documented?

---

## 7. RED FLAGS: When NOT to Use Orchestration

🚩 **Not suitable for:**
- "Just build a login button" → Use individual agent
- "Explore new ML algorithms" → Use subagents + experimentation
- "I need instant feedback" → Real-time interaction not orchestration's strength
- "I don't know what I'm building yet" → Define requirements first
- "Budget is $0.01" → Orchestrator has setup cost

---

## 8. FIESTA ENCLAVE: RECOMMENDED PATTERNS

| Operation | Pattern | Frequency | Est. Monthly Cost |
|-----------|---------|-----------|-------------------|
| **Commodity pipeline** | Sequential | Daily (30×) | $3.60 |
| **Cost audit** | Sequential | Weekly (4×) | $0.60 |
| **Training projects** | Sequential + parallel | 1-2× | $0.30-0.45 |
| **Feature launches** | Parallel + integration | 2-3× | $0.60-0.90 |
| **Incident response** | Parallel (rapid) | 1× | $0.20 |
| **TOTAL MONTHLY** | | | **~$5.30** |

---

## 9. COMMON FAILURE MODES + FIXES

| Failure | Cause | Fix |
|---------|-------|-----|
| **Task stalls forever** | Upstream task failed, downstream blocked | Check upstream QA result, retry if needed |
| **QA keeps failing** | Requirements unclear, agent frustrated | Provide clearer feedback + examples |
| **Cost exploding** | Too many retries | Check QA criteria (maybe too strict?) |
| **Orchestrator lost context** | Architecture doc not shared | Create shared doc, reference in all tasks |
| **Agent gave wrong output** | Agent misunderstood task | Clarify task description + examples |

---

## 10. QUICK DECISION TREE

```
START
  ├─ Is this a ONE task?
  │   └─ YES → /subagent <agent-name> "<task>"
  │   └─ NO → Continue
  │
  ├─ Does it need QA gates?
  │   └─ YES → agents-orchestrator
  │   └─ NO → Continue
  │
  ├─ Is it recurring?
  │   └─ YES → agents-orchestrator
  │   └─ NO → Continue
  │
  └─ Is it production/critical?
      └─ YES → agents-orchestrator
      └─ NO → /subagent <agent-name> "<task>" (faster)
```

---

## 11. CONVERSATION STARTERS

### To Start Orchestration:
```
"Use the orchestrator to [describe project]

Include:
- Frontend: React + Tailwind
- Backend: Node.js + PostgreSQL
- Testing: Visual QA + API QA
- Marketing: Product announcement"
```

### To Check Progress:
```
"What's the current status?"
"Which task is in progress?"
"Are any tasks blocked?"
```

### To Debug Failure:
```
"Why did [task] fail QA?"
"What feedback does [agent] need?"
"How many retries left?"
```

---

## 12. COST CALCULATOR

**Quick estimate:**

```
Projects/month: __
Average tasks/project: __
Haiku cost/task: $0.01
Retries expected: 20% (multiply × 1.2)

Calculation:
  Projects × Tasks × $0.01 × 1.2 = $/month

Example: 4 projects × 5 tasks × $0.01 × 1.2 = $0.24/month
```

---

## 13. SUCCESS METRICS

### Quality Metrics
- [ ] All tasks pass QA on 1st or 2nd try
- [ ] No tasks exceed 3 retries
- [ ] No escalations to human review
- [ ] Final deliverables meet requirements

### Efficiency Metrics
- [ ] Tasks completed on time
- [ ] Parallel execution saves time vs sequential
- [ ] Context preserved across team (no re-explaining)

### Cost Metrics
- [ ] Actual cost ≤ estimated cost × 1.2
- [ ] Cost per task ≤ $0.01-0.02
- [ ] Retries < 20% (indicates unclear requirements)

---

## 14. WHEN TO ESCALATE

🔴 **Escalate to human review if:**
1. Task fails QA 3 times (same agent can't fix it)
2. Multiple tasks blocked by single failure
3. QA criteria conflict with requirements
4. Agent output doesn't match specification
5. Cost exceeds budget by > 50%

**Action:** Stop orchestration, gather team, revise approach.

---

## 15. FIESTA'S STANDING POLICY (Tier 0-2 Discipline)

✅ **Always use orchestration when:**
- Quality gates are non-negotiable
- Multiple teams involved
- Recurring/scalable operations
- Production systems

✅ **Always use subagents when:**
- Single-purpose tasks
- Experimentation/learning
- <$0.05 budget
- Real-time interaction needed

❌ **Never use external APIs:** (Tier 0-2 only)
- No calling third-party APIs without orchestration approval
- All API calls must route through backend-architect agent
- Cost tracking mandatory

---

## 16. FIESTA ENCLAVE COMMAND REFERENCE

### Start Orchestration
```bash
/openclaw skill use agency-agents --agent orchestrator \
  "Build [project]: [specs]"
```

### Spawn Individual Agent
```bash
/subagent <agent-name> "<task>"
```

### Check Orchestrator Status
```
"What's the current progress?"
"Which task is failing?"
```

### Abort & Restart
```
"Stop orchestration"
"Reset to task X"
```

---

## 17. FINAL CHECKLIST: READY TO ORCHESTRATE?

- [ ] Requirements written clearly
- [ ] Tasks identified + prioritized
- [ ] Dependencies mapped
- [ ] Agents assigned
- [ ] QA criteria defined
- [ ] Architecture document created + shared
- [ ] Team aligned on timeline
- [ ] Budget approved
- [ ] Success metrics defined
- [ ] Escalation path identified

✅ **ALL CHECKED?** → Ready to launch!

---

**Print this, keep it handy, refer before starting projects.**

---

## Document Info
- **Created:** 2026-03-15 12:56 UTC
- **Audience:** Fiesta team
- **Cost:** $0.00 (reference doc)
- **Update frequency:** Quarterly
- **Last updated:** 2026-03-15
