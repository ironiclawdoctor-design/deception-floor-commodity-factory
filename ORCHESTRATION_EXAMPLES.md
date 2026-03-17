# Agent Orchestration: Practical Examples & Workflows

**Purpose:** Concrete, runnable examples showing orchestration in action  
**Created:** 2026-03-15 12:56 UTC  
**Companion to:** ORCHESTRATION_GUIDE.md

---

## Example 1: Daily Commodity Extraction Pipeline

### Scenario
Mendez-Gemini Enclave needs to ingest commodity price data daily:
- Extract from 3 APIs (metals, agriculture, energy)
- Normalize to internal schema
- Validate data freshness
- Store to PostgreSQL
- Generate daily summary report

### Project Setup

```yaml
# commodity-extraction-pipeline.yaml
project_name: "Daily Commodity Extraction"
schedule: "0 8 * * *"  # 8 AM daily

tasks:
  - id: 1
    name: "Extract Metal Prices"
    agent: "data-extractor"
    input:
      sources:
        - api: "metals-api.com"
          endpoints: [gold, silver, copper]
        - api: "london-metals.com"
          endpoints: [LME futures]
    expected_output: "metal-prices-raw.json"
    qa_criteria:
      - Data is < 1 hour old
      - All 3 metals present
      - Prices are positive numbers
      - Field count: exactly 6 fields

  - id: 2
    name: "Extract Agricultural Prices"
    agent: "data-extractor"
    input:
      sources:
        - api: "agapi.usda.gov"
          crops: [wheat, corn, soybeans]
    expected_output: "ag-prices-raw.json"
    qa_criteria:
      - All 3 crops present
      - Futures data included
      - Prices > 0

  - id: 3
    name: "Extract Energy Prices"
    agent: "data-extractor"
    input:
      sources:
        - api: "eia.gov"
          commodities: [crude-oil, natural-gas]
    expected_output: "energy-prices-raw.json"
    qa_criteria:
      - Both commodities present
      - WTI and Brent crude included
      - Updated within 4 hours

  - id: 4
    name: "Normalize Data"
    agent: "data-integrator"
    dependencies: [1, 2, 3]  # Wait for all 3 extractors
    input:
      raw_files: ["metal-prices-raw.json", "ag-prices-raw.json", "energy-prices-raw.json"]
      schema: "commodity-schema-v2.json"
    expected_output: "commodities-normalized.json"
    qa_criteria:
      - All fields match schema
      - No nulls (except optional fields)
      - Data types correct
      - Field counts match source + schema

  - id: 5
    name: "Validate & Store"
    agent: "backend-architect"
    dependencies: [4]
    input:
      data_file: "commodities-normalized.json"
      database: "postgresql://enclave-db/commodities"
      table: "daily_prices"
    expected_output: "storage-complete-timestamp.txt"
    qa_criteria:
      - Row count matches input
      - No duplicate entries
      - Timestamps are sequential
      - Foreign keys valid

  - id: 6
    name: "Generate Summary Report"
    agent: "report-automator"
    dependencies: [5]
    input:
      query: "SELECT * FROM daily_prices WHERE date = TODAY()"
    expected_output: "daily-commodity-summary.html"
    qa_criteria:
      - Report contains all commodity types
      - Charts render correctly
      - Statistics are accurate (spot check 3 values)
```

### Orchestrator Execution Flow

```
[08:00] PIPELINE START
  ├─ Project initialized
  └─ 6 tasks loaded

[08:02] PARALLEL: Extract metals + ag + energy (3 agents, simultaneous)
  ├─ Agent 1: metals-api extraction → metal-prices-raw.json ✅
  ├─ Agent 2: ag-api extraction → ag-prices-raw.json ✅
  └─ Agent 3: eia-api extraction → energy-prices-raw.json ✅

[08:08] QA VALIDATION (3 QA agents, parallel)
  ├─ QA 1: Metal data freshness ✅ PASS
  ├─ QA 2: Ag data completeness ✅ PASS
  └─ QA 3: Energy data freshness ✅ PASS

[08:10] NORMALIZE DATA (task 4 unblocked, all deps passed)
  └─ Agent 4: data-integrator normalizes 3 files
    └─ Output: commodities-normalized.json ✅

[08:15] QA NORMALIZATION
  └─ QA: Schema validation ✅ PASS

[08:16] STORE DATA (task 5 unblocked)
  └─ Agent 5: backend-architect inserts to PostgreSQL ✅

[08:20] QA STORAGE
  └─ QA: Row count + data integrity ✅ PASS

[08:21] GENERATE REPORT (task 6 unblocked)
  └─ Agent 6: report-automator creates HTML ✅

[08:25] QA REPORT
  └─ QA: Visual + data accuracy ✅ PASS

[08:25] ✅ PIPELINE COMPLETE
  Total time: 25 minutes
  Tasks completed: 6/6
  QA passes: 6/6 (0 retries needed)
  Cost: 12 Haiku × $0.01 = ~$0.12
```

### If QA Fails (Example: Metal Prices Extraction)

```
[08:03] EXTRACTION: metals-api
  └─ Returns: 2 metals (missing copper) ❌

[08:05] QA VALIDATION
  └─ QA Agent: "Missing copper. Expected 3 metals, got 2"
    └─ DECISION: ❌ FAIL (all 3 metals required)
    └─ Feedback: "metals-api returned incomplete data
                  - Check if API is up: curl metals-api.com/status
                  - Expected: gold, silver, copper
                  - Got: gold, silver
                  - Retry: 1/3"

[08:06] DEV RETRY #1
  └─ Agent 1: Checks API health, API is UP ✓
    └─ Tries alternative endpoint: /metals/full
    └─ Returns: gold, silver, copper ✅

[08:07] QA RE-VALIDATION
  └─ QA Agent: "All 3 metals present ✓, freshness OK ✓"
    └─ DECISION: ✅ PASS
    └─ Feedback: "Data complete, ready for normalization"

[08:08] CONTINUE PIPELINE
  └─ Unblock downstream tasks (normalization, etc.)
```

### Cost Analysis

| Item | Haiku | Cost |
|------|-------|------|
| Extract metals | 1 | $0.01 |
| Extract ag | 1 | $0.01 |
| Extract energy | 1 | $0.01 |
| QA extraction (3×) | 3 | $0.03 |
| Normalize | 1 | $0.01 |
| QA normalize | 1 | $0.01 |
| Store | 1 | $0.01 |
| QA store | 1 | $0.01 |
| Report | 1 | $0.01 |
| QA report | 1 | $0.01 |
| **TOTAL (no retries)** | **12** | **$0.12** |
| **With 1 retry (like above)** | **14** | **$0.14** |

**Monthly cost (30 runs):** $3.60-4.20  
**Annual cost:** $43.20-50.40

---

## Example 2: Monthly Cost Audit & Compliance Check

### Scenario
Fiesta needs to verify cost discipline monthly:
- Extract billing from Anthropic API
- Analyze token usage by project
- Detect anomalies (overspends)
- Verify Tier 0-2 compliance
- Generate executive summary

### Workflow

```
MONTHLY COST AUDIT
│
├─ Task 1: Extract billing data
│  └─ Agent: data-analyst
│     Input: Anthropic API key + date range (last 30 days)
│     QA: "Totals match invoice within 1%"
│
├─ Task 2: Token usage analysis
│  └─ Agent: analytics-reporter
│     Input: billing-raw.json
│     QA: "Top 5 projects identified, costs calculated"
│
├─ Task 3: Anomaly detection
│  └─ Agent: finance-ops
│     Input: usage-summary.json + historical baseline
│     QA: "Anomalies flagged with reasoning"
│
├─ Task 4: Tier compliance audit
│  └─ Agent: compliance-officer
│     Input: billing-raw.json
│     QA: "Verify Tier 0 (bash) = $0, Tier 1 (BitNet) = $0, Tier 2 (Haiku) = detected cost"
│
└─ Task 5: Executive summary
   └─ Agent: executive-reporter
      Input: All previous outputs
      QA: "Summary is accurate, actionable, under 2 pages"
```

### Example Output

```markdown
# MENDEZ-GEMINI ENCLAVE — MONTHLY COST AUDIT
Date: March 2026

## Executive Summary
- **Total cost:** $847.20 (within budget of $1,000)
- **Burn rate:** $27.90/day
- **Forecast (full month):** ~$837 (0.14% variance, acceptable)
- **Tier 0 (bash):** $0.00 ✅ (discipline maintained)
- **Tier 1 (BitNet):** $0.00 ✅ (sovereign)
- **Tier 2 (Haiku):** $847.20 ✅ (tracked)

## Top 5 Projects by Cost
1. **Commodity Pipeline** - $312.50 (36.9%)
2. **Training Project (SaaS MVP)** - $287.30 (33.9%)
3. **Cost Audits** - $89.60 (10.6%)
4. **Feature Launches** - $125.40 (14.8%)
5. **Incident Response** - $32.40 (3.8%)

## Anomalies Detected
- None. All spikes explained by scheduled work.

## Tier Compliance
✅ All Tier 0-2 routes verified  
✅ SOUL.md discipline maintained  
✅ No unauthorized external APIs used  
✅ No cron jobs running (approved baseline only)  

## Recommendations
1. **Commodity pipeline optimization:** Batch weekly instead of daily (save 30%)
2. **Precache architecture docs:** Save 70% explanation overhead
3. **Parallel feature development:** Run frontend + backend simultaneously (save 40% time)

---
Cost audit completed by: compliance-officer agent  
QA verified by: executive-reporter agent  
Date: March 15, 2026
```

---

## Example 3: Feature Launch (End-to-End)

### Scenario
Launch "Commodity Price Alerts" feature across engineering, design, QA, and marketing

### Project Breakdown

```yaml
project: "Launch Commodity Price Alerts"
timeline: "2 weeks"
departments:
  - engineering: 2 agents (frontend, backend)
  - design: 1 agent (UX)
  - qa: 2 agents (visual QA, API QA)
  - marketing: 1 agent (content)

task_sequence:
  phase_1_planning:
    - task: "Define requirements"
      agent: "senior-pm"
      output: "requirements-doc.md"
      
  phase_2_design:
    - task: "Design user flow + wireframes"
      agent: "ux-architect"
      output: "design-wireframes.pdf"
      qa_criteria: "Designs follow brand guidelines"
      
  phase_3_development:
    - task: "Implement backend API"
      agent: "backend-architect"
      output: "api-implementation/"
      qa_criteria: "All endpoints working, matches API contract"
      
    - task: "Implement frontend UI"
      agent: "frontend-dev"
      output: "ui-component/"
      qa_criteria: "Visual matches design, responsive, accessible"
      
  phase_4_integration:
    - task: "End-to-end testing"
      agent: "visual-qa"
      output: "qe-report.md"
      qa_criteria: "All user flows work, no visual bugs"
      
    - task: "Performance testing"
      agent: "performance-engineer"
      output: "perf-report.md"
      qa_criteria: "API response < 200ms, UI loads < 2s"
      
  phase_5_launch:
    - task: "Write announcement + docs"
      agent: "content-creator"
      output: "announcement.md + help-docs.html"
      qa_criteria: "Clear, accurate, ready for launch"
      
    - task: "Release certification"
      agent: "release-gatekeeper"
      output: "go-no-go.txt"
      qa_criteria: "All quality gates pass, approved for production"
```

### Timeline

```
WEEK 1:
  Mon: Requirements definition (PM)
  Tue-Wed: Design (UX) + Backend dev starts (Engineer)
  Thu-Fri: Backend API implementation + Frontend dev

WEEK 2:
  Mon: QA testing begins
  Tue: Bug fixes (dev retry loop)
  Wed: Performance testing
  Thu: Launch prep (marketing content)
  Fri: Release certification + launch
```

### Parallel Execution Savings

Without orchestration (sequential):
```
Requirements (2h) → Design (4h) → Backend (6h) → 
Frontend (6h) → QA (4h) → Launch (2h)
= 24 hours total
```

With orchestration (parallel):
```
Requirements (2h) ──────────────
                  ├─ Design (4h) ──→ Frontend (6h) → QA (4h) → Launch (2h)
                  └─ Backend (6h) ──┘
= 14 hours total (42% time savings)
```

### Cost Example (No Retries)

| Phase | Agent | Cost |
|-------|-------|------|
| Planning | PM | $0.01 |
| Design | UX Architect | $0.02 |
| Backend dev | Backend Architect | $0.05 |
| Frontend dev | Frontend Dev | $0.04 |
| Backend QA | API QA | $0.02 |
| Frontend QA | Visual QA | $0.02 |
| Performance QA | Performance Engineer | $0.01 |
| Marketing | Content Creator | $0.02 |
| Release gate | Release Gatekeeper | $0.01 |
| **Total** | **9 agents** | **$0.20** |

---

## Example 4: Training Project (Multi-Agent Learning)

### Scenario
Train new agents on full-stack development using real project

### Learning Objectives

```
By end of this project, new agents will have demonstrated:
1. System design (architecture decisions)
2. Backend implementation (API design + database)
3. Frontend implementation (UI + state management)
4. Testing (QA criteria definition)
5. Documentation (runbooks, API docs)
```

### Project: "Build a simple blog app"

```yaml
learning_project:
  name: "Build Simple Blog Platform"
  duration: "1 week"
  agents_involved: 5
  
  module_1_architecture:
    description: "Design system before building"
    agent: "senior-engineer"
    task: |
      Design a simple blog app with:
      - User authentication
      - Post creation/editing
      - Comments
      - Search
    deliverable:
      - System architecture diagram
      - Database schema (ERD)
      - API endpoint list
    qa_criteria: "Design is complete, no missing pieces"
    learning_outcomes:
      - How to break down requirements
      - How to design for scalability
      - How to communicate design to team
    
  module_2_backend:
    description: "Implement REST API"
    agent: "backend-architect"
    task: "Build Node.js + Express API from architecture doc"
    deliverable:
      - REST API endpoints
      - Database migrations
      - Authentication middleware
    qa_criteria: "All endpoints work, API contract matches design"
    learning_outcomes:
      - API design patterns
      - Database schema implementation
      - Error handling
      
  module_3_frontend:
    description: "Implement user interface"
    agent: "frontend-dev"
    task: "Build React + TypeScript UI from design doc"
    deliverable:
      - React components
      - State management
      - Responsive design
    qa_criteria: "UI matches design, responsive on mobile"
    learning_outcomes:
      - Component design
      - State management
      - CSS + responsive design
      
  module_4_testing:
    description: "Write comprehensive tests"
    agent: "test-analyst"
    task: "Design test strategy, identify coverage gaps"
    deliverable:
      - Test plan
      - Edge case analysis
      - Coverage report
    qa_criteria: "Test plan covers all critical paths"
    learning_outcomes:
      - Test strategy design
      - QA criteria definition
      - Coverage analysis
      
  module_5_documentation:
    description: "Write production-quality docs"
    agent: "senior-pm"
    task: "Create runbooks, deployment guides, API documentation"
    deliverable:
      - API documentation
      - Deployment runbook
      - Operations guide
    qa_criteria: "Docs are complete, clear, accurate"
    learning_outcomes:
      - Documentation patterns
      - Operational clarity
      - Knowledge transfer
```

### Outcome & Evaluation

```
After completing this project, new agent demonstrates:

✅ System Design (senior-engineer module)
   - Can break requirements into components
   - Understands database design
   - Knows API patterns

✅ Backend Implementation (backend-architect module)
   - Can build REST APIs
   - Understands authentication/security
   - Knows database best practices

✅ Frontend Implementation (frontend-dev module)
   - Can build React components
   - Understands responsive design
   - Knows state management

✅ Testing & QA (test-analyst module)
   - Can identify test gaps
   - Understands QA criteria
   - Can design comprehensive test plans

✅ Documentation (senior-pm module)
   - Can write clear technical docs
   - Understands operational needs
   - Can communicate to engineers + ops teams

Certification: ✅ READY for production projects

Next assignment: Assign to commodity pipeline (real work) with mentoring
```

---

## Example 5: Incident Response Workflow

### Scenario
"Commodity service API down" — Rapid response orchestration

### Incident Severity: P1 (Critical)
- Enclave can't access commodity prices
- Business impact: HIGH
- Response time: Immediate

### Workflow

```
[12:00 ALERT] Service monitoring detects API down

[12:01] INCIDENT DECLARED
  └─ Severity: P1
  └─ Owner: infrastructure-maintainer agent
  └─ Stakeholders: backend-architect, devops-engineer, support-lead

[12:02] IMMEDIATE ACTIONS (parallel)

  Task 1: Root Cause Analysis (infrastructure-maintainer)
  ├─ Check logs: "Connection pool exhausted"
  ├─ Check database: "PostgreSQL replication lag 5 minutes"
  └─ Diagnosis: "High query volume + replication delay = timeout"
     Severity: P1 confirmed
     
  Task 2: User Communication (support-lead)
  ├─ Notify users: "We're aware of the issue, ETA 30 minutes"
  └─ Post status: https://status.mendez-gemini.com
  
  Task 3: Temporary Mitigation (backend-architect)
  ├─ Reduce connection pool timeout (quick win)
  ├─ Start rollback of recent changes (recent deploy?)
  └─ Status: "API responding again (degraded mode)"

[12:15] QA VERIFICATION
  └─ Test API endpoints manually
  └─ Response time: 200-500ms (slow but working)
  └─ Data freshness: OK
  └─ DECISION: ✅ PASS (service operational, degraded)

[12:16] PERMANENT FIX (devops-engineer)
  ├─ Increase database connection pool
  ├─ Add read replicas for high-volume queries
  ├─ Deploy updated config
  └─ Monitor for 30 minutes

[12:45] FINAL VALIDATION
  ├─ API response time: < 100ms (normal)
  ├─ Database replication: 0 lag
  ├─ Load test: Can handle 2× normal traffic
  └─ DECISION: ✅ FULLY RECOVERED

[12:50] POST-INCIDENT ANALYSIS (async, within 24h)

  Task: Root Cause Analysis (test-analyst)
  ├─ Why did connection pool exhaust?
  ├─ Why no alerts before outage?
  └─ Output: "Incident report: connection pool sizing"
  
  Task: Prevention (process-optimizer)
  ├─ Add alert at 80% connection pool usage
  ├─ Add load testing in CI/CD
  ├─ Update runbook: "Connection pool exhaustion"
  └─ Output: "3 process improvements"

[12:55] COMMUNICATE FINDINGS
  ├─ User notification: "Issue resolved, root cause identified"
  ├─ Team summary: Post-incident report
  └─ Status page: Back to normal

INCIDENT CLOSED
  Timeline: 55 minutes (detection to full recovery)
  User impact: 55 minutes downtime
  Prevention: 3 new safeguards in place
  Cost: ~$0.08 (8 Haiku for incident response + analysis)
```

### QA Checkpoints in Incident Response

| Step | Agent | QA Criteria | Pass/Fail |
|------|-------|------------|-----------|
| **Diagnosis** | Infrastructure | Root cause identified | ✅ PASS |
| **Mitigation** | Backend arch | API responding < 1s | ✅ PASS |
| **Permanent fix** | DevOps | Response time < 100ms | ✅ PASS |
| **Prevention** | QA analyst | All improvements feasible | ✅ PASS |
| **Documentation** | PM | Runbook updated, clear | ✅ PASS |

---

## Comparison: How Each Pattern Handles Failure

### Pattern 1: Commodity Pipeline (Extraction Fail)

```
Extraction fails → QA detects → Feedback to extractor
→ Extractor retries with new API endpoint
→ QA validates again → Continue (no downstream delay)
```

**Result:** Single agent retries, downstream unblocked after fix  
**Cost:** +1 Haiku per retry (10% cost increase)

---

### Pattern 2: Cost Audit (Data Quality Fail)

```
Normalization fails → QA detects schema mismatch
→ Data integrator updates schema
→ Retry normalization
→ QA validates → Continue
```

**Result:** Single task retries, rest unaffected  
**Cost:** +2 Haiku (normalization + QA recheck = 20% cost increase)

---

### Pattern 3: Feature Launch (Design Not Approved)

```
Frontend dev finishes → QA: "Doesn't match design" ❌
→ Feedback to frontend-dev: "Use rounded corners, adjust spacing"
→ Frontend-dev iterates
→ QA validates → Pass
```

**Result:** Dev-QA loop continues until design matches  
**Max cost:** 3 retries × 2 Haiku = 6 Haiku added

---

### Pattern 4: Training Project (Backend API Fails Tests)

```
Backend dev completes → Test-analyst: "3 edge cases fail" ❌
→ Feedback: "Handle null users, empty comments, concurrent updates"
→ Backend-dev fixes code
→ Test-analyst verifies
→ Pass on retry 2
```

**Result:** Learning experience — agent sees what "production ready" means  
**Cost:** Extra retries, but educational value high

---

### Pattern 5: Incident Response (Rollback Fails)

```
Rollback deployment → Infrastructure: "Still erroring" ❌
→ Check logs: "Config mismatch"
→ Rollback again with fresh snapshot
→ Verify API working
→ Pass on retry 2
```

**Result:** Quick failure detection, no prolonged downtime  
**Cost:** +2 Haiku, but prevented 30-minute outage

---

## Summary: When to Use Which Pattern

| Use Case | Pattern | Why | Example |
|----------|---------|-----|---------|
| **Daily data processing** | Sequential | Strict ordering, clear deps | Commodity extraction |
| **Monthly reviews** | Sequential + parallel | Some tasks parallel, then aggregate | Cost audit |
| **Feature releases** | Parallel dev + serial QA | Speed + quality | Feature launch |
| **Agent training** | Sequential (full pipeline) | Learn full cycle | Training project |
| **Crisis response** | Parallel + rapid QA | Speed + validation | Incident response |

---

**End of Examples Document**
