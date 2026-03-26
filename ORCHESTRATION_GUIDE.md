# Agent Orchestration Guide — Complete Learning Document

**Prepared:** 2026-03-15 12:56 UTC  
**Tier Level:** 0-2 (Reading + Analysis, $0.00 cost)  
**Source Skills:**
- `fiesta-agents/SKILL.md` (61-agent network)
- `agents-orchestrator/SKILL.md` (workflow management)
- `agency-agents/SKILL.md` (parent integration)

---

## 1. What Is Agent Orchestration?

### Definition

Agent orchestration is the **automated coordination of multiple specialized AI agents** to complete complex, multi-step projects through managed workflows, quality gates, and communication patterns.

Rather than:
- Running a single agent for a single task
- Spawning multiple agents independently (subagents)
- Manually coordinating between teams

Orchestration:
- **Breaks down complex projects** into tasks
- **Assigns tasks to specialist agents** (frontend-dev, backend-architect, QA-tester, etc.)
- **Implements continuous dev↔QA loops** (build → test → validate → retry on failure)
- **Maintains quality gates** (no progression without QA pass)
- **Manages dependencies** between tasks
- **Tracks state and progress** throughout the pipeline
- **Handles errors and retries** automatically (up to 3 retries per task)
- **Delivers unified results** with all context preserved

### Why Orchestration Matters

**Problem it solves:**

| Issue | Without Orchestration | With Orchestration |
|-------|----------------------|-------------------|
| **Coordination** | Manual handoffs, context loss | Automatic task routing, preserved context |
| **Quality** | Individual agent outputs (no QA) | Dev↔QA loop (3-retry max per task) |
| **Parallelization** | Must sequence tasks manually | Intelligent dependency tracking |
| **Failure recovery** | Agent fails, project stalls | Automatic retry with feedback loop |
| **Progress visibility** | Scattered outputs | Unified dashboard + reports |
| **Scope creep** | Agents drift from original task | Quality gates enforce scope |

### The Core Insight

Orchestration transforms this:
```
Task → Agent A → Agent B → Agent C → Done?
```

Into this:
```
Project Spec
  ↓
Break into Tasks (PM/Sprint Planner)
  ↓
Design Architecture (Architect)
  ↓
For each Task:
    ├─ Dev implements (Engineer)
    ├─ QA validates (Test Agent)
    ├─ If PASS → next task
    └─ If FAIL (retry < 3) → return to Dev with feedback
  ↓
Final Integration (Release Gatekeeper)
  ↓
Delivery Report + Quality Metrics
```

---

## 2. When to Use Agent Orchestration

### Best For

✅ **Complex multi-step projects** requiring multiple departments:
- Full-stack web applications (frontend, backend, infrastructure, QA, docs)
- Product launches (product strategy, engineering, design, marketing, communications)
- Data pipeline projects (architecture, implementation, testing, deployment)
- Marketing campaigns (strategy, content, social, analytics, reporting)

✅ **Quality-critical deliverables:**
- Production systems (need QA gates + retries)
- Customer-facing products (need design review + user testing)
- Compliance-sensitive projects (need audit trails)

✅ **Projects with interdependencies:**
- Tasks that must be sequenced
- Shared architectural decisions across tasks
- Cross-team validation requirements

✅ **Learning/training scenarios:**
- Multiple agents working together teach patterns
- Observing dev↔QA loop is educational
- Quality gates enforce discipline

### Worse For

❌ **Single-purpose, well-scoped tasks:**
- "Generate a React button component" → Use frontend-dev directly
- "Analyze sales data" → Use data-analyst directly
- "Write a blog post" → Use content-creator directly

❌ **Real-time interactive work:**
- Orchestrator expects discrete task phases
- Not designed for back-and-forth conversations
- Latency is higher (multiple agent round-trips)

❌ **Highly experimental / exploratory work:**
- Orchestration enforces structure (dev → QA → next)
- Explorative iteration doesn't fit this pattern
- Use individual agents for "what if" scenarios

---

## 3. Common Orchestration Patterns

### Pattern 1: Sequential Execution
**When:** Tasks must be completed in strict order  
**Example:** Data pipeline (extract → transform → load → validate)

```
Task 1: Data Extraction (Data Extractor)
  ↓ (QA validates extracted data)
Task 2: Data Transformation (Data Integrator)
  ↓ (QA validates transformations)
Task 3: Load to DB (Backend Architect)
  ↓ (QA validates final state)
Task 4: Generate Report (Report Automator)
```

**Characteristics:**
- Each task blocked until previous passes QA
- Clear handoff points
- Failure in Task N blocks everything downstream

---

### Pattern 2: Parallel Execution
**When:** Independent tasks can run simultaneously  
**Example:** Full-stack web app (frontend, backend, infrastructure can start in parallel)

```
                 ┌─ Frontend Dev
Project Spec ─→ │─ Backend Architect
                 └─ DevOps Engineer
                   (all get architecture doc)
                 ↓
            Integration Testing
            (once all parallel tasks pass QA)
```

**Characteristics:**
- All agents get the architecture document first
- Tasks start at the same time
- Orchestrator waits for ALL to pass QA before moving on
- Reduces total time vs sequential

---

### Pattern 3: Fan-Out / Task Distribution
**When:** One task generates multiple sub-tasks  
**Example:** QA team validates multiple features

```
Feature List (from PM)
  ↓
Dev implements all features
  ↓
QA splits into sub-tests:
  ├─ Visual QA (UI rendering)
  ├─ API QA (endpoint validation)
  ├─ Performance QA (load testing)
  └─ Security QA (vulnerability scan)
```

**Characteristics:**
- Parent task spawns N child tasks
- Children can run in parallel
- All must pass QA to consider parent complete

---

### Pattern 4: Map-Reduce
**When:** Process similar items independently, then aggregate  
**Example:** Build multiple service microservices, then test integration

```
Services to build: [auth, payment, inventory, shipping]
  ↓
MAP: Build each service independently (4 parallel Dev tasks)
  ├─ Backend Architect builds auth service
  ├─ Backend Architect builds payment service
  ├─ Backend Architect builds inventory service
  └─ Backend Architect builds shipping service
  ↓
QA validates each individually
  ↓
REDUCE: Integration testing (API contracts, cross-service calls)
```

**Characteristics:**
- Distribute identical task types across agents
- Each produces independent output
- Final aggregation step combines results
- Often used for scalable production workloads

---

### Pattern 5: Feedback Loop / Iterative Refinement
**When:** Task requires multiple QA cycles to converge  
**Example:** Design system iteration

```
Initial Design (UI Designer)
  ↓
Design Review (UX Researcher)
  ↓
If PASS (quality threshold met) → Deliver
If FAIL → Feedback to UI Designer
  ↓
Refinement Round 2
  ↓
Repeat until PASS
  (max 3 cycles per task)
```

**Characteristics:**
- Built-in to all orchestrator tasks (dev↔QA loop)
- Automatic feedback flow
- Retry counter prevents infinite loops (3 max)
- Escalates to human review if max retries exceeded

---

## 4. Orchestration Constraints & Capabilities

### What Orchestrators CAN Do

✅ **Task Management:**
- Break projects into granular tasks
- Assign tasks to specialist agents (7 engineering agents, 7 design agents, 8 marketing agents, etc.)
- Track completion status
- Enforce dependencies (no next task until current passes QA)

✅ **Quality Control:**
- Implement dev↔QA loop (developer implements, test agent validates)
- Reject outputs that don't meet standards
- Provide detailed feedback to developers
- Retry up to 3 times with specific guidance

✅ **State Management:**
- Preserve context across agent transitions
- Maintain task list + completion status
- Track architecture decisions (all agents see design doc)
- Generate progress reports

✅ **Error Handling:**
- Detect QA failures
- Route failures back to dev with specific feedback
- Implement exponential backoff or intelligent retry strategies
- Escalate after 3 retries to human review

✅ **Communication:**
- Provide agents with full project context
- Pass task-specific instructions
- Deliver QA feedback from test agents to dev agents
- Generate unified final reports

### What Orchestrators CANNOT Do

❌ **Real-time interactive debugging:**
- Can't intervene mid-task
- Can't adjust in response to partial progress
- Must wait for task completion

❌ **Recursive orchestration:**
- Can't spawn sub-orchestrators within orchestrator
- Depth limit: 1 orchestrator per project
- Use individual agents for nested workflows

❌ **Unlimited retries:**
- Hard limit: 3 retries per task
- After 3 failures, must escalate
- No automatic "try again forever" loops

❌ **Cross-project state sharing:**
- Each orchestration is isolated
- Can't reference previous project outputs automatically
- Must manually pass files/context if needed

❌ **Dynamic agent selection:**
- Orchestrator must specify which agent handles which task
- Can't learn mid-execution and switch agents
- Requires upfront design

❌ **Streaming/incremental output:**
- Tasks are atomic (all-or-nothing)
- Must wait for full task completion
- Can't interrupt and deliver partial results

### Tool Availability in Orchestration

**Available to orchestrator:**
- Message passing (task assignments, feedback)
- File I/O (read task specs, write deliverables)
- Subagent spawning (each agent is a spawned subagent)
- Progress tracking (JSONL logs, state files)

**NOT available:**
- Direct code execution (agents run in isolated sessions)
- Real-time browser control (agents can use browser tool, but orchestrator can't see the screen)
- Database access (agents must use APIs)

### Recursion Limits

**Current limit:** Depth 1/1 (single orchestrator per project)

**Workaround for nested workflows:**
```
Instead of: Orchestrator → Orchestrator → Agents
Use:        Orchestrator → Individual Agents
            (Agents coordinate themselves via messaging)
```

---

## 5. Cost Implications & Token Efficiency

### Cost Model: Orchestration vs Individual Spawns

#### Orchestration (agents-orchestrator)

**Cost structure:**
- 1 × orchestrator (Haiku): project analysis, task planning, progress tracking
- N × development agents (Haiku each): actual implementation
- N × QA agents (Haiku each): validation
- Communication overhead (low): passing task specs, feedback

**Example: Full-stack web app (5 tasks)**

| Phase | Work | Cost | Notes |
|-------|------|------|-------|
| Planning | Analyze requirements, create task list | 1 Haiku | ~0.1 USD |
| Architecture | Design system, API contracts, DB schema | 1 Haiku | ~0.1 USD |
| Dev Loop 1 | Frontend dev (pass 1) | 1 Haiku | ~0.1 USD |
| QA Loop 1 | Visual QA, feedback | 1 Haiku | ~0.1 USD |
| Dev Loop 2-5 | Backend, DB, DevOps (each 1 pass) | 4 Haiku | ~0.4 USD |
| QA Loop 2-5 | API QA, integration QA (4 passes) | 4 Haiku | ~0.4 USD |
| Integration | Release gatekeeper final check | 1 Haiku | ~0.1 USD |
| **Total** | 5 tasks, all tasks pass on 1st QA | **~13 Haiku** | **~1.3 USD** |

**With retries (2 fail, need 2 retries each):**

| Phase | Work | Cost | Notes |
|-------|------|------|-------|
| Same as above | ... | 13 Haiku | Baseline |
| Retries | 2 tasks × 2 retries each | 4 Haiku | ~0.4 USD |
| **Total** | 5 tasks, 2 need retries | **~17 Haiku** | **~1.7 USD** |

---

#### Individual Spawns (subagents, this session's approach)

**Cost structure:**
- Spawn frontend-dev: 1 Haiku
- Spawn backend-architect: 1 Haiku
- Spawn QA engineer: 1 Haiku
- (manually coordinate, no orchestrator oversight)

**Same project, manual coordination:**

| Activity | Cost | Notes |
|----------|------|-------|
| Frontend dev (1st draft) | 1 Haiku | ~0.1 USD |
| Manual review | 1 Haiku | ~0.1 USD |
| Backend dev (1st draft) | 1 Haiku | ~0.1 USD |
| Manual review | 1 Haiku | ~0.1 USD |
| QA testing | 1 Haiku | ~0.1 USD |
| Fixing errors (5 iterations) | 5 Haiku | ~0.5 USD |
| Integration testing | 1 Haiku | ~0.1 USD |
| **Total** | **~12 Haiku** | **~1.2 USD** |

**Plus hidden costs:**
- Manual context loss (agent doesn't know what other agents decided)
- Repeated explanations (each agent needs full context)
- No shared architecture (agents might make conflicting decisions)
- Quality undefined (no QA gate, ship whatever is done)

---

### Cost Comparison Summary

| Metric | Orchestration | Individual Spawns |
|--------|---|---|
| **Direct token cost** | Lower (structured tasks) | Similar |
| **Retry efficiency** | High (feedback-driven) | Low (manual debugging) |
| **Context waste** | Minimal (shared) | High (repeated explanations) |
| **Quality confidence** | High (QA gates) | Low (unknown quality) |
| **Time to delivery** | Moderate | Fast (but lower quality) |
| **Best for** | Production, quality-critical | Prototyping, experimentation |

---

### Precaching Strategy for Token Efficiency

#### Strategy 1: Shared Architecture Document

**The idea:** Create architecture ONCE, all agents reference it (not re-explain to each agent)

```markdown
# Project Architecture (created once, shared with ALL agents)

## Technical Stack
- Frontend: React 18, TypeScript, Tailwind
- Backend: Node.js + Express
- Database: PostgreSQL
- Deployment: Docker + Kubernetes

## System Diagram
[shared diagram all agents see]

## API Contracts
[all agents know the interfaces]

## Data Models
[shared schema prevents conflicts]
```

**Cost savings:**
- Without precaching: Each agent re-reads/re-explains architecture (~0.05 USD per agent)
- With precaching: One shared doc, referenced by all (~0.01 USD for all)
- **Savings:** 70% reduction in architecture explanation overhead

---

#### Strategy 2: Task Template Library

**The idea:** Create reusable task specifications that reduce per-task explanation

```yaml
# tasks/web-form-implementation.yaml
name: "Implement Web Form Component"
agent: "frontend-dev"
requirements:
  - Built with React + TypeScript
  - Validation using zod schema
  - Accessible (WCAG 2.1 AA)
  - Responsive (mobile-first)
qa_criteria:
  - Visual QA: Pixel-perfect on Chrome/Safari/Firefox
  - Functional QA: All validation rules work
  - Accessibility QA: Keyboard navigation works
```

**Cost savings:**
- Without templates: Explain requirements per-task (~0.03 USD per task)
- With templates: Reference template + customize (~0.01 USD per task)
- **Savings:** 67% reduction in per-task specification overhead

---

#### Strategy 3: Context Batch Window

**The idea:** Load all architectural context into a "context batch" at project start

```
PROJECT START
  ├─ Load: Architecture.md (2 KB)
  ├─ Load: API-Contracts.md (1 KB)
  ├─ Load: Data-Schema.md (0.5 KB)
  └─ Load: Code-Standards.md (0.5 KB)

ALL AGENTS INHERIT THIS CONTEXT
  (costs paid once, not per-agent)

Task 1: "Implement user auth"
  (agent sees architecture context, saves re-explaining)

Task 2: "Build payment API"
  (agent sees architecture context, consistent design)
```

**Cost savings:**
- Context loaded once (~0.02 USD for all 4 MB)
- Without batching: Each agent loads context (~0.05 USD per agent)
- **Savings:** If 5 agents, 5 × 0.05 = 0.25 USD vs 1 × 0.02 = 0.02 USD
- **Savings:** 92% reduction in architectural context loading

---

#### Strategy 4: QA Feedback Reuse

**The idea:** When QA fails, provide specific feedback that can be applied to similar tasks

```
Task 1 QA FAIL: "Visual alignment issues on mobile"
  ├─ Feedback: "Use flex-wrap on component, add responsive padding"
  └─ Store: task-1-feedback.md

Task 2 (similar task) starts
  ├─ Dev pre-loads: task-1-feedback.md
  ├─ Avoids repeating same mistake
  └─ Saves 1 QA cycle

Result: Task 2 passes on 1st try (vs Task 1 taking 2 tries)
```

**Cost savings:**
- Without reuse: Task 2 fails same way, retry needed (~0.1 USD extra)
- With reuse: Task 2 passes first try (~0.0 USD extra)
- **Savings:** Per avoided retry = 0.1 USD

---

### Token Efficiency Best Practices

| Practice | Cost Impact | Implementation |
|----------|------------|-----------------|
| **Shared architecture doc** | -70% arch overhead | Create ONCE, reference always |
| **Task templates** | -67% per-task overhead | Build library, reuse |
| **Context batching** | -92% context loading | Load architectural context at project start |
| **QA feedback reuse** | -100% per avoided retry | Store feedback, share with next task |
| **Parallel task execution** | -40% total time | Run independent tasks simultaneously |
| **Retry discipline** | -50% wasted tokens | 3-retry max, escalate after |

**Expected total savings:** 50-60% cost reduction vs unmanaged multi-agent work

---

## 6. Five Practical Orchestration Patterns for Fiesta Context

Given the Mendez-Gemini Enclave context (commodity factory operations, training agents, cost control), here are 5 patterns:

### Pattern A: Commodity Extraction Pipeline

**Goal:** Extract raw commodity data → validate → normalize → store  
**Use case:** Daily commodity feed processing

```
Tasks:
  1. Data Extraction (data-extractor agent)
     - Pull commodity pricing from APIs
     - QA: Validate data freshness (< 1 hour old)
     
  2. Data Normalization (data-integrator agent)
     - Convert formats (XML → JSON)
     - QA: Schema validation
     
  3. Storage (backend-architect agent)
     - Insert into PostgreSQL
     - QA: Row count validation
     
  4. Report Generation (report-automator agent)
     - Create daily summary
     - QA: Spot-check metrics

Cost: ~4-5 Haiku per pipeline run (~$0.04-0.05)
Frequency: Daily (32 runs/month = $1.28-1.60/month)
Quality: 3-retry gate ensures data integrity
```

---

### Pattern B: Multi-Agent Training Delivery

**Goal:** Train junior agents on system design + implementation  
**Use case:** Onboarding new agents into Fiesta ecosystem

```
Project: "Build sample microservice (training exercise)"

Tasks:
  1. System Design (senior-engineer agent)
     - Architecture review
     - QA: Design audit checklist
     
  2. Backend Implementation (backend-architect agent)
     - Implement REST API
     - QA: API contract testing
     
  3. Frontend Implementation (frontend-dev agent)
     - Implement React client
     - QA: Visual + functional testing
     
  4. Deployment (devops-engineer agent)
     - Docker + CI/CD setup
     - QA: Deployment verification
     
  5. Documentation (senior-pm agent)
     - Create runbooks
     - QA: Completeness check

Cost: ~10-15 Haiku (~$0.1-0.15) per training project
Frequency: 1-2 per month = $0.2-0.3/month
Quality: Full QA loop = learning opportunity
Outcome: Agent gains full-stack experience
```

---

### Pattern C: Cost Control Audit Loop

**Goal:** Validate cost discipline across agency operations  
**Use case:** Monthly cost review + token efficiency audit

```
Tasks:
  1. Cost Data Extraction (data-analyst agent)
     - Pull billing logs from Anthropic API
     - QA: Amount validation (matches invoices)
     
  2. Token Usage Analysis (analytics-reporter agent)
     - Group by project/agent/model
     - QA: Sanity check totals
     
  3. Cost Anomaly Detection (finance-ops agent)
     - Identify overspends
     - Alert on Tier 0-2 violations
     - QA: Review anomalies
     
  4. Compliance Report (compliance-officer agent)
     - Check Tier routing (bash-first discipline)
     - Verify SOUL.md compliance
     - QA: Policy adherence check
     
  5. Executive Summary (executive-reporter agent)
     - Cost trends, forecasts
     - Recommendations
     - QA: C-suite review

Cost: ~8-10 Haiku (~$0.08-0.1) per audit
Frequency: Monthly = $1-1.2/month
Quality: QA gates prevent false positives
Outcome: Full transparency + cost accountability
```

---

### Pattern D: Feature Launch Orchestration

**Goal:** Deliver new product feature end-to-end  
**Use case:** Monthly feature release (design → implement → test → marketing)

```
Project: "Launch commodity pricing alerts feature"

Tasks (parallel where possible):
  1. PM Planning (sprint-planner agent)
     - Acceptance criteria
     - User stories
     - QA: Stakeholder approval
     
  2. UX Design (ux-architect agent)
     - User flows
     - Wireframes
     - QA: Usability review
     
  3. Backend API (backend-architect agent)
     - Notification service
     - Database schema
     - QA: API contract test
     
  4. Frontend UI (frontend-dev agent)
     - Alert UI component
     - Notification preferences
     - QA: Visual + functional test
     
  5. QA Validation (release-gatekeeper agent)
     - End-to-end testing
     - Performance check
     - QA: Production readiness
     
  6. Marketing Prep (content-creator agent)
     - Feature announcement
     - Help docs
     - QA: Completeness check

Cost: ~20-25 Haiku (~$0.2-0.25) per feature
Frequency: 2-4 features/month = $0.4-1/month
Quality: Multi-stage QA ensures launch quality
Outcome: Polished feature, happy users
```

---

### Pattern E: Incident Response & Recovery

**Goal:** Rapid response to system issues + prevention  
**Use case:** Production incident management

```
Scenario: "Commodity service API down"

Immediate Tasks (sequential):
  1. Incident Detection (infrastructure-maintainer agent)
     - Diagnose root cause
     - QA: Verification (service is really down)
     
  2. Emergency Fix (senior-engineer agent)
     - Implement hotfix
     - QA: Local verification
     
  3. Deployment (devops-engineer agent)
     - Roll out fix to production
     - QA: Post-deployment verification
     
Follow-up Tasks (parallel):
  4. Communication (support-lead agent)
     - Notify users
     - Post status updates
     
  5. Root Cause Analysis (test-analyst agent)
     - Why did this happen?
     - Test coverage gaps?
     
  6. Prevention (process-optimizer agent)
     - Add monitoring
     - Update runbooks
     - QA: Runbook review

Cost: ~15-20 Haiku (~$0.15-0.2) per incident response
Frequency: 1-2 incidents/month (ideally 0) = $0.3-0.4/month
Quality: Structured approach prevents chaos
Outcome: Fast recovery + systemic improvement
```

---

## 7. Comparison: agents-orchestrator vs Subagents (This Session)

### agents-orchestrator (Specialized Skill)

**What it is:**
- A dedicated orchestration agent (from fiesta-agents)
- Runs as a single coordinator managing the full project workflow
- Specialized in: project planning, task decomposition, QA gate management, retry logic

**Strengths:**
- ✅ Designed specifically for orchestration (optimized for project management)
- ✅ Built-in understanding of dev↔QA loops
- ✅ Manages retry logic + escalation
- ✅ Generates project reports automatically
- ✅ Focused role (doesn't distract with other tasks)

**Weaknesses:**
- ❌ Single point of failure (if orchestrator breaks, entire project stalls)
- ❌ Requires calling as a skill (extra context setup)
- ❌ Less flexible for custom workflows
- ❌ Cost: ~0.1 USD per project setup

**Best for:**
- Standard projects (web apps, product launches)
- Teams wanting hands-off orchestration
- Learning the orchestration pattern

---

### Subagents (This Session's Approach)

**What it is:**
- Multiple individual agents spawned via `/subagent` or similar
- Lightweight, purpose-built for specific tasks
- This learning session itself is a subagent

**Strengths:**
- ✅ Highly flexible (each agent does its exact job, no overhead)
- ✅ Can customize workflow (not locked to orchestrator pattern)
- ✅ Lower latency (direct agent invocation)
- ✅ Easier debugging (see each agent's output)
- ✅ Better for learning (understand each component)

**Weaknesses:**
- ❌ Manual coordination required (no built-in project management)
- ❌ No automatic dev↔QA loops (must implement yourself)
- ❌ No built-in retry logic (must implement yourself)
- ❌ Harder to track overall progress (scattered outputs)
- ❌ Context loss between agents (each agent isolated)

**Best for:**
- Experimentation + learning (like this task)
- Custom workflows (non-standard processes)
- Rapid prototyping (no orchestrator overhead)
- Cost-sensitive work (pay only for computation)

---

### Feature Comparison Matrix

| Feature | agents-orchestrator | Subagents |
|---------|---|---|
| **Built-in project management** | ✅ Yes | ❌ No |
| **Dev↔QA loops** | ✅ Automatic | ❌ Manual |
| **Retry logic** | ✅ 3-retry gate | ❌ None |
| **Progress tracking** | ✅ Unified dashboard | ❌ Scattered |
| **Context preservation** | ✅ Passed between agents | ❌ Lost |
| **Error escalation** | ✅ Auto (after 3 retries) | ❌ Manual |
| **Flexibility** | ⚠️ Pattern-bound | ✅ Any workflow |
| **Latency** | ⚠️ Moderate (setup overhead) | ✅ Low |
| **Cost** | ⚠️ Setup cost (~$0.1) | ✅ Pay-as-you-go |
| **Debugging** | ⚠️ Black box | ✅ Clear |

---

### Decision Tree: When to Use Each

```
Do you need to coordinate 3+ agents?
  ├─ YES → agents-orchestrator (project management built-in)
  └─ NO → Use individual agents directly

Will tasks need QA validation?
  ├─ YES → agents-orchestrator (dev↔QA loops)
  └─ NO → Subagents (simpler)

Do you need automatic retry logic?
  ├─ YES → agents-orchestrator (3-retry gate)
  └─ NO → Subagents (manual control)

Is this a standard project pattern?
  ├─ YES (web app, product launch, etc.) → agents-orchestrator
  └─ NO (custom workflow) → Subagents

Is this experimentation / learning?
  ├─ YES → Subagents (lower friction)
  └─ NO (production) → agents-orchestrator
```

---

## 8. Recommendation: Best Pattern for Mendez-Gemini Enclave

### Context
- **Mission:** Commodity factory operations + agent training
- **Scale:** Recurring daily/weekly operations
- **Quality requirement:** HIGH (commodity data is critical)
- **Cost sensitivity:** HIGH (Tier 0-2 discipline)
- **Team:** Fiesta + specialist agents + training cohort

### Recommendation: **Hybrid Approach**

**For recurring operational workflows:** Use **agents-orchestrator**
- Commodity extraction pipelines (daily)
- Cost audits (weekly)
- Training projects (ad-hoc)

**Rationale:**
1. **Quality gates matter** (commodity data accuracy is non-negotiable)
2. **Recurring costs** (pipeline runs daily → amortize setup cost across many runs)
3. **Scalability** (standardized process can scale to 10+ concurrent pipelines)
4. **Team training** (agents learn the orchestration pattern by working with it)

---

**For custom/exploratory work:** Use **Subagents**
- Building new agents (research phase)
- Prototyping novel processes
- Ad-hoc analysis (one-off projects)

**Rationale:**
1. **Flexibility** (not everything fits the orchestrator pattern)
2. **Learning** (subagents teach individual agent capabilities)
3. **Cost control** (no orchestrator overhead for simple tasks)

---

### Implementation Roadmap

**Phase 1 (Now):** Establish individual agent competencies
- Train agents on specific roles (backend-dev, frontend-dev, QA)
- Build task templates for common work
- Document which agents handle which commodity types
- Cost: ~$5-10/week in training (read + analysis only)

**Phase 2 (Next 2-4 weeks):** Implement first orchestration pipeline
- Commodity extraction (data-extractor → data-integrator → storage)
- Cost audit loop (analytics → compliance → reporting)
- Daily runs, collect metrics
- Expected cost: $2-5/week

**Phase 3 (Next month):** Expand to feature launches + incident response
- Product features use multi-team orchestration
- Incidents use rapid-response workflow
- Training projects use full-stack orchestration
- Expected cost: $10-20/week (but 3-5 major projects completed)

---

## 9. Detailed Cost Breakdown: Mendez-Gemini Tier 0-2 Model

### Standing Costs (Monthly Baseline)

| Component | Frequency | Cost | Notes |
|-----------|-----------|------|-------|
| **Daily commodity pipeline** | 30 runs | $1.50 | 5 Haiku per run (~$0.05) |
| **Weekly cost audit** | 4 runs | $0.40 | 10 Haiku per run (~$0.1) |
| **Monthly training project** | 2 runs | $0.30 | 15 Haiku per run (~$0.15) |
| **Ad-hoc feature work** | 3 features | $0.75 | 25 Haiku per feature (~$0.25) |
| **Incident response** | 1 incident | $0.20 | 20 Haiku (~$0.2) |
| **Observational overhead** | Continuous | $0 | Actually's logging (Tier 0) |
| **TOTAL MONTHLY** | | **$3.15** | Fully orchestrated agency ops |

---

### Cost Optimization Tactics

1. **Batch commodity processing** (save 30% setup overhead)
   - Instead of: Daily pipeline (30 runs × setup cost)
   - Do: Weekly batch (4 runs × setup cost)
   - Trade: Faster cadence vs lower cost

2. **Precache architecture docs** (save 70% explanation overhead)
   - Create once: "Commodity system architecture"
   - Reference always: Every pipeline run uses same doc
   - Savings: ~$0.3/month

3. **Reuse QA feedback** (save 50% on retries)
   - Store: "Common extraction failures" template
   - Apply: Next run avoids same mistakes
   - Savings: ~$0.2/month per prevented retry

4. **Parallel where possible** (save 40% total time)
   - Commodity extraction + cost audit can run parallel
   - Feature development (frontend + backend) parallel
   - Savings: Faster delivery, same cost

---

## 10. Constraints & Hard Limits Summary

### Orchestration Hard Limits

| Limit | Value | Implication |
|-------|-------|-------------|
| **Max retries per task** | 3 | After 3 QA fails, escalate or abandon task |
| **Max orchestration depth** | 1 | No sub-orchestrators within orchestrators |
| **Max tasks per project** | Unlimited | But recommend < 50 for clarity |
| **Max agents per task** | 1 | Each task assigned to single agent |
| **Max concurrent tasks** | 5-10 (practical) | Too many parallel = coordination chaos |
| **Retry feedback size** | ~1 KB | Keep QA feedback concise |

### Communication Patterns

**Synchronous (blocking):**
- Task assignment → Agent accepts
- QA validation → Pass/Fail decision
- Feedback loop → Dev receives and retries

**Asynchronous (non-blocking):**
- Progress reports (agent updates status file)
- Architecture sharing (all agents see same doc)
- Escalation (after 3 retries, flag for human review)

### Tool Availability in Orchestration Context

| Tool | Available? | Notes |
|------|-----------|-------|
| **File I/O** | ✅ Yes | Read specs, write deliverables |
| **Messaging** | ✅ Yes | Task assignments, feedback |
| **Subagent spawning** | ✅ Yes | Each agent is a subagent |
| **Browser automation** | ⚠️ Limited | Agent can use, orchestrator can't see |
| **Database access** | ⚠️ API only | Via backend-architect agent |
| **Code execution** | ✅ Agents can | Orchestrator can't directly |

---

## 11. Key Takeaways

### What is Agent Orchestration?
- **Automated coordination** of multiple specialist agents through managed workflows
- **Quality gates** enforce standards (dev → QA → next)
- **Retry logic** handles failures gracefully (up to 3 attempts)
- **Context preservation** maintains decisions across team

### When to Use It
- ✅ Multi-step complex projects (web apps, product launches, data pipelines)
- ✅ Quality-critical work (production, customer-facing)
- ✅ Recurring operations (daily/weekly pipelines)
- ❌ Single-purpose tasks (use individual agents)
- ❌ Exploratory work (subagents better for prototyping)

### Common Patterns
1. **Sequential:** Tasks must complete in order (data pipeline)
2. **Parallel:** Independent tasks run simultaneously (full-stack dev)
3. **Fan-out:** One task spawns multiple sub-tasks (QA suite)
4. **Map-reduce:** Process similar items, aggregate results (microservices)
5. **Feedback loop:** Iterative refinement until passing standard (design iteration)

### Constraints & Capabilities
- ✅ Can: Project management, QA loops, retries, state tracking, error handling
- ❌ Cannot: Real-time debugging, recursive orchestration, unlimited retries, dynamic agent selection

### Cost Efficiency
- **Orchestration:** $1.3 USD per 5-task project (high quality)
- **Subagents:** $1.2 USD per project (lower quality, manual coordination)
- **Savings with precaching:** 50-60% reduction in overhead
- **For Mendez-Gemini:** ~$3.15/month for full orchestrated operations

### Best for Mendez-Gemini Enclave
- **Use agents-orchestrator:** Recurring commodity pipelines, cost audits, training projects
- **Use subagents:** Custom workflows, prototyping, one-off analysis
- **Hybrid approach:** Balance structure (orchestrator) with flexibility (subagents)

---

## Appendix: Quick Reference

### To Use agents-orchestrator

```bash
/openclaw skill use agency-agents --agent orchestrator \
  "Build a complete SaaS MVP: 
   - Frontend (React dashboard)
   - Backend (Node.js + PostgreSQL API)
   - Testing and deployment
   - Marketing landing page"
```

### To Spawn Individual Subagents

```bash
/subagent <agent-name> <task-description>

# Example:
/subagent frontend-dev "Build a login form with React"
/subagent backend-architect "Design a REST API for user management"
/subagent qa-tester "Test the login form"
```

### To Check Progress in Orchestration

```bash
# Within orchestrator session:
"What's the current status?"
"Which task is blocking us?"
"What failed in QA?"

# Expected response: Unified status report
```

---

## Document Metadata

- **Created:** 2026-03-15 12:56 UTC
- **Subagent:** learn-agent-orchestration-patterns
- **Task:** Complete learning document on agent orchestration
- **Cost:** $0.00 (Tier 0-2 reading + analysis)
- **Status:** ✅ Complete

---

**End of Guide**
