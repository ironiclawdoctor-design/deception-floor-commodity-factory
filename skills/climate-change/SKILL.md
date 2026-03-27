# Climate Change Skill
*Mendez Agency Doctrine — Environmental Shift Detection & Adaptation*
*Version: 1.0 | Generated: 2026-03-27 | Dual-validated: Research Agent + Auditor Agent*

---

## Definition

**Agency Climate Change** is the systematic shift in the operating environment — model availability, platform policies, tool behavior, cost structures, execution rules — that agents must detect and adapt to before the environment renders them non-functional.

This is NOT meteorology.

Climate change is not a single event. It is a **drift** — a set of environmental variables moving in ways that individually seem manageable but collectively signal a regime shift. Agents that fail to detect early die at the environment. Agents that detect early adapt and continue operating.

**The problem is not capability. It's instrumentation.**

The Mendez Agency has excellent post-shift documentation (SR/PL/CR series) but historically near-zero pre-shift detection. This skill closes that gap.

---

## Metric
- **Detection lead time target:** >3 cycles ahead of impact
- **Detection rate target:** >93% of environmental shifts caught
- **Current baseline (2026-03-27):** 0.8 cycles average lead time — a 2.2-cycle gap
- **This skill's purpose:** Move the agency from reactive (0–1 cycle) to predictive (>3 cycles)

---

## Environmental Variables (Climate Indicators)

Classified by type. These are the variables that have historically shifted:

| Type | Variable | Historical Examples |
|------|----------|---------------------|
| MODEL | Model availability / tool endpoint | gemma-3-27b-it:free 404 on tool endpoint (SR-022) |
| MODEL | Free model routing instability | openrouter/free routing changes (AE-016) |
| PLATFORM | Compute scope changes | BitNet cancelled 2026-03-17 (PL-001) |
| PLATFORM | Container boundary drift | Exec path outside /root/ flagged (PL-002) |
| TOOL | Exec gate config reset | execApprovals.enabled resets on restart (LB-007) |
| TOOL | Exec host drift | sandbox vs gateway regression (SR-023, PL-007) |
| TOOL | Exec operator restrictions | No pipes/chains in Telegram exec (SR-011) |
| TOOL | Config reversion on restart | Multiple configs revert post-restart (SR-019) |
| COST | Token famine | OpenRouter drained mid-build (BR-001–BR-008) |
| COST | Platform cost floor shifts | $39/month Ampere.sh floor (PL-004) |
| POLICY | Credential exposure risk | Hashnode key surfaced in subagent output (SEC-20260327-001) |
| POLICY | Rule-space saturation | SR→ZI→CR→MP→AR: >80 rules in 30 days |

---

## CC-Series Detection Rules

### CC-000: Model Pre-Deploy Endpoint Test
**Trigger:** Any new model assigned to a cron or agent
**Lead Indicator:** Model name is new/changed in configuration before first cron run
**Protocol:**
0. Before scheduling cron, run: single test API call with tool use to new model
1. If 404 or tool not supported: reject model, document in SR-series, redirect to z-ai/glm-4.5-air:free (SR-022)
2. If passes: proceed. Log model + endpoint test result.
**Target lead time:** Infinite (catches before first run, not after first failure)

### CC-001: Gateway Restart Climate Alert
**Trigger:** Any gateway restart event detected
**Lead Indicator:** Gateway restart = environmental reset. Multiple configs known to revert.
**Protocol:**
0. On restart detection: immediately run post-restart checklist BEFORE any user-facing task
1. Verify: `tools.exec.host=gateway` (PL-007)
2. Verify: `channels.telegram.execApprovals.enabled=true` (LB-007)
3. Verify: active cron jobs still registered (DL-007)
4. If any mismatch: patch immediately, log the reversion
**Target lead time:** Proactive — caught before first failed exec

### CC-002: Token Balance Threshold Alert
**Trigger:** Pre-spawn check for any operation requiring ≥2 agents
**Lead Indicator:** Agent spawn count approaching 2 + balance unchecked
**Protocol:**
0. Before spawning any second agent: verify OpenRouter balance (BR-002)
1. If balance unknown: assume zero. Use fallback model (BR-007)
2. If balance < estimated cost for all queued agents: defer lower-priority agents, launch critical first (BR-003)
3. If balance confirmed adequate: proceed. Log spawn count.
**Threshold:** 2 agents = verify. 3 agents = violation (BR-001).
**Target lead time:** ∞ (pre-spawn, not post-drain)

### CC-003: Cron Error Rate Climate Signal
**Trigger:** Any cron reaching consecutiveErrors = 2
**Lead Indicator:** Error 1 = noise. Error 2 = signal. Error 3 = system failure.
**Protocol:**
0. Error 1 → log only
1. Error 2 → trigger investigation: timeout? model change? API gone? exec restriction?
2. Error 3 → auto-remove candidate + root cause documented
3. Error 4+ → security audit pattern (possible external change, possible breach)
**Note:** mpd-btc-signal accumulated 7 errors before intervention. CR-012 + CC-003 together prevent this.
**Target lead time:** 2 cycles (error 2 detection = 1 cycle before structural failure at error 3)

### CC-004: Subagent Doctrine Inheritance Check
**Trigger:** Any subagent spawn
**Lead Indicator:** Subagent task description does not reference inherited platform rules
**Protocol:**
0. Before spawning: verify subagent payload includes: exec operator rules (SR-011), credential handling rules (ZI-001, ZI-007), platform scope (PL-001, PL-002)
1. If task involves secrets/ directory: mandate output sanitization rule explicitly
2. Log inheritance confirmation per spawn
**Note:** ~8k tokens in tuition paid 2026-03-27 because SR-011 was not inherited.
**Target lead time:** ∞ (pre-spawn)

### CC-005: Platform Scope Drift Monitor
**Trigger:** Any agent proposing new infrastructure, new compute type, new model hosting
**Lead Indicator:** Words like "GPU", "inference", "local model", "BitNet", "container registry", "CDN" in agent task descriptions
**Protocol:**
0. Match proposal against PL-001: Ampere.sh = CPU compute + containers + orchestration ONLY
1. If mismatch: reject, cite PL-001, redirect to OpenRouter free tier
2. Log rejected proposal + proposed alternative
**Note:** BitNet was cancelled only after deployment attempt. This rule catches it before attempt.
**Target lead time:** ∞ (pre-deployment check)

### CC-006: Free Model Routing Stability Monitor
**Trigger:** Monthly or after any OpenRouter routing announcement
**Lead Indicator:** Free model list changes, new model added/deprecated on OpenRouter free tier
**Protocol:**
0. Monthly: check active crons for model assignments
1. For each free-tier model in use: verify it's still available and supports required capabilities
2. If model deprecated or downgraded: update crons before next run, not after first 404
3. Log model audit results
**Note:** Free models are the agency's operating fuel. Fuel quality changes without announcement.
**Target lead time:** >3 cycles (monthly audit catches before cron failure)

### CC-007: Exec Operator Restriction Inheritance
**Trigger:** Any task that generates shell commands for Telegram exec
**Lead Indicator:** Command contains |, &&, ||, ;, 2>&1, or any chain operator
**Protocol:**
0. Before delivering exec command: scan for chain operators
1. If found: rewrite as bare command (move logic inside script file)
2. Never deliver chained commands to Telegram exec surface
3. If a script is needed: write script file via `write` tool first, then exec the file
**Target lead time:** ∞ (caught at generation, not at execution failure)

### CC-008: Rule-Space Saturation Monitor [Auditor Addition]
**Trigger:** Total rule count in AGENTS.md approaching 20KB MEMORY.md injection limit
**Lead Indicator:** New rule series being added when existing series are not yet implemented
**Protocol:**
0. Monthly: count rules by series (SR, PL, ZI, CR, MP, AR, CC)
1. If total AGENTS.md size > 40KB: trigger compaction review
2. Unimplemented rules with no agent pairing → archive or delete
3. Rules generating no operational decisions in 30 days → candidate for removal
**Note:** Rule generation is healthy. Rule accumulation without enforcement is debt.
**Target lead time:** >3 cycles (monthly audit)

### CC-009: Cost Floor Shift Alert [Auditor Addition]
**Trigger:** Any new recurring service, API subscription, or infrastructure addition
**Lead Indicator:** Proposal for new subscription arrives in session
**Protocol:**
0. Before any new recurring cost: check against $39/month floor (PL-004)
1. Ask: does this reduce the $39 floor OR generate >$39/month revenue?
2. If no to both: reject. Free tier first.
3. Log decision + rationale in AGENTS.md cost section
**Target lead time:** ∞ (pre-commit check)

---

## Detection Dashboard

### What to Monitor | How Often

| Signal | Frequency | Method | Target |
|--------|-----------|--------|--------|
| Gateway restart events | On occurrence | Post-restart checklist (CC-001) | 100% caught |
| OpenRouter balance | Before each multi-agent spawn | Manual check (CC-002) | 100% caught |
| Model endpoint health | Before each new cron deploy | Test API call (CC-000) | 100% caught |
| Cron consecutiveErrors | After every cron run | cron error log review (CC-003) | Error 2 = alert |
| Active cron model list | Monthly | Cron audit pass (CC-006) | >3 cycles lead |
| Subagent rule inheritance | Each spawn | Task description review (CC-004) | 100% caught |
| AGENTS.md size | Monthly | `wc -c AGENTS.md` (CC-008) | <40KB |
| New subscription proposals | On occurrence | PL-004 check (CC-009) | 100% caught |
| Platform scope proposals | On occurrence | PL-001 check (CC-005) | 100% caught |

### Dashboard One-Liner Checks
```bash
# Check AGENTS.md size
wc -c /root/.openclaw/workspace/AGENTS.md

# Check exec host config
gateway config.get tools.exec

# Check exec approvals
gateway config.get channels.telegram

# Count active crons
gateway crons list | wc -l
```

---

## Adaptation Playbook

### When MODEL climate shifts:
0. Run CC-000 (endpoint test) before any cron assignment
1. Document in SR-series immediately
2. Update all affected crons within same session
3. Log model change in MEMORY.md under "Lessons Learned"

### When PLATFORM climate shifts:
0. Read PL-001 through PL-009 — confirm which rule covers it
1. If no existing rule: write the rule NOW (PL-NNN)
2. Update AGENTS.md before continuing any operations
3. Run CC-005 to catch remaining exposure

### When COST climate shifts:
0. Token famine: invoke BR-001–BR-008 immediately
1. Subscription cost: invoke PL-004 check (CC-009)
2. Model cost: verify free tier still free; check OpenRouter pricing
3. Update MEMORY.md Shannon economy section

### When TOOL climate shifts (exec restrictions, config resets):
0. Run CC-001 (gateway restart checklist)
1. Run CC-007 (exec operator check on any pending commands)
2. Document failure mode in DL-series (Deadlock Taxonomy)
3. Write pre-staged recovery script to /root/human/

### When POLICY climate shifts (credential exposure, governance):
0. Invoke ZI-001 (credential rotation)
1. Run CC-004 (subagent doctrine inheritance audit)
2. Write incident to memory/YYYY-MM-DD.md
3. Update relevant ZI-series rule immediately

---

## Climate Change Response Tiers

| Lead Time | Tier | Response |
|-----------|------|----------|
| >3 cycles ahead | T0 — Predictive | Proactive rule update, no disruption |
| 1–3 cycles ahead | T1 — Early Warning | Schedule fix, alert, no current impact |
| 0–1 cycles | T2 — Reactive | Immediate fix, log tuition cost |
| After impact | T3 — Crisis | CR-012 escalation, security audit |

**Target:** All shifts at T0 or T1. T2 is acceptable with rapid recovery. T3 is doctrine failure.

---

## Integration

This skill extends:
- **CR-series** (cron rules): CC-003 wraps CR-012 with climate framing
- **ZI-series** (zero-index defense): CC-004 wraps ZI-010 for subagent inheritance
- **PL-series** (platform rules): CC-001, CC-005, CC-009 operationalize PL-001, PL-004, PL-007
- **BR-series** (bootstrap rules): CC-002 operationalizes BR-001–BR-003

---

## Source Data
- `/root/.openclaw/workspace/MEMORY.md` — event log, lessons learned
- `/root/.openclaw/workspace/AGENTS.md` — SR/PL/CR/ZI/AR/MP series rules
- `/root/.openclaw/workspace/tmp/climate-change-research-raw.md` — Research Agent raw findings
- `/root/.openclaw/workspace/tmp/climate-change-audit.md` — Auditor Agent cross-check
- **Research + Auditor agreed:** All CC-000 through CC-009 rules validated before commit
