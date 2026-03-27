# Climate Change Research — Raw Findings (Research Agent)
*Generated: 2026-03-27 | Auditor cross-check required before promotion to SKILL.md*

---

## Phase 1: Environmental Variables Identified (Past 30 Days)

### Variable Index (0-based)

#### VAR-000: Model Availability Collapse — gemma-3-27b-it:free
- **Type:** MODEL
- **Impact:** HIGH
- **Event:** gemma-3-27b-it:free silently returns 404 on any cron that calls tools
- **Source:** SR-022, AE-017
- **Lead Indicator:** Tool endpoint returning 404 on first cron run → NOT a silent success
- **Detection lag:** 1–2 cron cycles (only discovered after consecutive errors)
- **Fix applied:** Migrate to z-ai/glm-4.5-air:free for isolated agentTurn crons
- **Lead time achieved:** 0–1 cycles (reactive, not predictive)
- **Gap:** Should have been caught before first cron failure

#### VAR-001: Platform Compute Scope — BitNet Cancellation
- **Type:** PLATFORM + MODEL
- **Impact:** HIGH
- **Event:** BitNet local model inference cancelled 2026-03-17 — wrong platform for Ampere.sh
- **Source:** MEMORY.md (BitNet — CANCELLED 2026-03-17), PL-001
- **Lead Indicator:** Platform capability docs say "CPU compute, containers, orchestration" — no GPU, no inference workloads
- **Detection lag:** Discovered at cancellation event (0 cycles lead)
- **Fix applied:** PL-001 rule — any agent proposing local inference → reject, cite PL-001
- **Lead time achieved:** 0 cycles (caught at cancellation only)
- **Gap:** PL-001 should have been written before BitNet was attempted

#### VAR-002: Exec Gate Config Reset — LB-007
- **Type:** TOOL + POLICY
- **Impact:** HIGH  
- **Event:** channels.telegram.execApprovals.enabled resets to false after every gateway restart
- **Source:** LB-007, HR-014
- **Lead Indicator:** Gateway restart event → exec gate likely reset → verify before first exec
- **Detection lag:** 1 exec attempt (first blocked command reveals it)
- **Fix applied:** LB-007 + FX-007 — auto-detect and re-apply after restart
- **Lead time achieved:** ~1 cycle (restart is the signal, but fix still reactive)
- **Gap:** Proactive restart detection needed before first exec attempt

#### VAR-003: Default Model Deprecation — openrouter/free
- **Type:** MODEL + COST
- **Impact:** MEDIUM
- **Event:** Default model changed to openrouter/free (2026-03-26); free-tier routing rules now govern behavior
- **Source:** AE-016
- **Lead Indicator:** OpenRouter balance changes, new model routing rules appearing in session
- **Detection lag:** Immediate (deliberate switch)
- **Lead time achieved:** N/A (intentional)

#### VAR-004: Token Famine — OpenRouter Credit Collapse
- **Type:** COST
- **Impact:** CRITICAL
- **Event:** 5 simultaneous agents drained OpenRouter mid-build (2026-03-23 02:33 UTC)
- **Source:** MEMORY.md (Token Famine Bootstrap Rules), BR-001 through BR-008
- **Lead Indicator:** Agent spawn count approaching 3+, balance not verified before launch
- **Detection lag:** 0 (hit during operation — catastrophic)
- **Fix applied:** BR-001 (max 2 agents), BR-002 (verify balance first), BR-007 (fallback model)
- **Lead time achieved:** 0 (no advance detection — pure reactive)
- **Gap:** Proactive balance monitoring needed; threshold alert before hitting zero

#### VAR-005: Exec Host Config Drift — sandbox vs gateway
- **Type:** TOOL + POLICY
- **Impact:** HIGH
- **Event:** tools.exec.host defaulting to sandbox → approval loop death on Telegram
- **Source:** SR-023, PL-007
- **Lead Indicator:** Any Telegram exec producing approval prompts despite "allow-always" grants
- **Detection lag:** 1 exec attempt
- **Fix applied:** PL-007 — patch and verify post-restart
- **Lead time achieved:** 1 cycle (first failed exec = signal)

#### VAR-006: Cron Model Incompatibility (SR-022 Pattern)
- **Type:** MODEL + TOOL
- **Impact:** HIGH
- **Event:** Multiple crons (mpd-btc-signal 7 consecutive errors, russia 2 consecutive) timing out
- **Source:** AR-006, AR-007, SR-022
- **Lead Indicator:** consecutiveErrors > 2, timeout at consistent threshold, Python + subprocess in 90s budget
- **Detection lag:** 2–7 cycles before action taken
- **Fix applied:** btc-cache-writer pattern, russia-lite single-query pattern
- **Lead time achieved:** 2–7 cycles (poor — error accumulated before fix)
- **Gap:** Should trigger at error 2, not error 7

#### VAR-007: Security Credential Exposure — Hashnode API Key
- **Type:** POLICY + TOOL
- **Impact:** HIGH
- **Event:** Hashnode API key surfaced in subagent output (2026-03-27T01:41 UTC)
- **Source:** memory/security-incident-20260327.md, suba-training-log.md
- **Lead Indicator:** Subagent tasks involving secrets/ directory + unrestricted output to chat surface
- **Detection lag:** ~0 cycles (detected immediately, but damage done)
- **Fix applied:** Demotion protocol, rotation instructions generated
- **Lead time achieved:** 0 (detected post-exposure — prevention failed)
- **Gap:** Subagents should never return raw credential values; output scrubbing needed

#### VAR-008: Exec Operator Restriction — No Pipes/Chains in Telegram
- **Type:** TOOL + POLICY
- **Impact:** MEDIUM
- **Event:** Telegram exec blocks |, &&, ||, ;, 2>&1 (discovered 2026-03-27)
- **Source:** suba-training-log.md, SR-011
- **Lead Indicator:** Any exec command containing chain operators → guaranteed denial
- **Detection lag:** 4 separate failures at ~2k tokens each before rule locked
- **Total tuition:** ~8k tokens
- **Fix applied:** SR-011 (bare commands only)
- **Lead time achieved:** 0 (paid tuition on every lesson)
- **Gap:** SR-011 existed but wasn't inherited by subagents

#### VAR-009: Platform Cost Floor — $39/month Ampere.sh
- **Type:** COST + PLATFORM
- **Impact:** MEDIUM (ongoing constraint)
- **Event:** Invoice YQBR07HK-0001 confirmed $39/month as hard floor (Mar 13–Apr 13, 2026)
- **Source:** MEMORY.md, PL-004
- **Lead Indicator:** New subscriptions requested without floor-check
- **Detection lag:** N/A (constant constraint)
- **Rule:** PL-004 — no new recurring spend unless it reduces floor or generates >$39/month revenue

#### VAR-010: Config Change Reversion on Restart (SR-019)
- **Type:** TOOL + POLICY
- **Impact:** MEDIUM
- **Event:** Multiple config changes discovered to revert after gateway restart
- **Source:** SR-019, DL-001 through DL-003
- **Lead Indicator:** Gateway restart event → verify all critical configs
- **Detection lag:** 1–3 failed operations post-restart before pattern recognized
- **Fix applied:** SR-019 (verify via config.get post-restart), PL-007 (exec.host permanence)
- **Lead time achieved:** 1 restart detection = signal

---

## Phase 1 Summary Table

| VAR | Type | Impact | Lead Indicator | Lead Time Achieved | Gap |
|-----|------|--------|---------------|---------------------|-----|
| VAR-000 | MODEL | HIGH | 404 on tool endpoint | 0–1 cycles | Pre-deploy model test needed |
| VAR-001 | PLATFORM+MODEL | HIGH | Platform docs: no GPU | 0 cycles | PL-001 before BitNet |
| VAR-002 | TOOL+POLICY | HIGH | Gateway restart event | ~1 cycle | Proactive restart detection |
| VAR-003 | MODEL+COST | MEDIUM | Deliberate switch | N/A (intentional) | — |
| VAR-004 | COST | CRITICAL | Agent spawn count >2 | 0 cycles | Balance monitor needed |
| VAR-005 | TOOL+POLICY | HIGH | First blocked exec | 1 cycle | Post-restart check script |
| VAR-006 | MODEL+TOOL | HIGH | consecutiveErrors >2 | 2–7 cycles | CR-012 threshold |
| VAR-007 | POLICY+TOOL | HIGH | Secret path in task | 0 cycles | Output scrubbing |
| VAR-008 | TOOL+POLICY | MEDIUM | Chain operators in cmd | 0 cycles | SR-011 inheritance |
| VAR-009 | COST+PLATFORM | MEDIUM | Subscription request | N/A (constant) | — |
| VAR-010 | TOOL+POLICY | MEDIUM | Gateway restart | 1–3 failed ops | Post-restart checklist |

---

## Research Agent Verdict

**Average lead time achieved:** 0.8 cycles
**Target:** >3 cycles
**Gap:** -2.2 cycles
**Root cause:** Agency is operating reactively — shifts detected at or after impact, not before

The agency has excellent POST-SHIFT documentation (SR/PL/CR series) but near-zero PRE-SHIFT detection infrastructure. The gap is not knowledge — it's instrumentation.
