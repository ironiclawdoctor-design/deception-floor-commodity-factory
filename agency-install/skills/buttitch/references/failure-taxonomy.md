# Buttitch Failure Taxonomy

Full classification system for non-cooperative agents. Each class includes signal criteria, root cause, and escalation path.

---

## Class 0: GHOST
**Signal:** Cron enabled, `nextRunAtMs` is set, but no `lastRunAtMs` and no `state` at all.  
**Root cause:** Never triggered, or gateway restarted before first run.  
**Escalation:** Manual trigger → classify from first run output.  
**Example:** New cron created but gateway restarted before it fired.

---

## Class 1: TIMEOUT
**Signal:** `lastErrorReason: "timeout"`, `consecutiveErrors >= 1`  
**Subclasses:**
- **TIMEOUT-SCRIPT**: Prompt calls a Python script that runs long or hangs
- **TIMEOUT-HEAVY**: Prompt is too verbose; model can't complete in time
- **TIMEOUT-NETWORK**: Script makes external API calls that time out
- **CHRONIC_TIMEOUT**: 3+ interventions, still timing out → disable

**Root causes:**
- `timeoutSeconds` too low for the model's latency (glm:free can be slow)
- Prompt instructs reading large files or scanning entire filesystem
- Script does web scraping or API polling without timeout guards
- Model is overloaded (free tier congestion)

**Escalation path:** Prompt surgery → timeout bump → script stub → CHRONIC_TIMEOUT disable

---

## Class 2: EMPTY
**Signal:** `lastRunStatus: "ok"` but no output delivered, or delivery shows empty string.  
**Root cause:** Model completed but produced no text (silent compliance), or output was filtered.  
**Escalation:** Output injection → if still empty after 2 runs, check if delivery mode suppresses output (mode=none).

---

## Class 3: RATE_LIMIT
**Signal:** `lastErrorReason: "rate_limit"`, `lastError` contains "429" or "rate limit reached"  
**Root cause:** Model (typically qwen3-coder:free or similar) hit free-tier RPM cap.  
**Escalation:** Immediate model swap to `openrouter/z-ai/glm-4.5-air:free`. No retry on same model.

---

## Class 4: SCOPE_DRIFT
**Signal:** Run completes, output is delivered, but content is unrelated to the cron's mandate.  
**Root cause:** Model hallucinating a different task, or prompt is ambiguous enough to trigger unrelated behavior.  
**Escalation:** Mandate lock (prepend identity + sole task) → if still drifting, add `[output format]` constraint.

---

## Class 5: SCRIPT_MISSING
**Signal:** Output contains `FileNotFoundError`, `No such file or directory`, `ModuleNotFoundError`  
**Root cause:** Cron prompt calls a Python script that was never written, was deleted, or has a wrong path.  
**Escalation:** Write a minimal stub script at the expected path → re-trigger. Log path as a new debt.

---

## Class 6: AUTH_FAILURE
**Signal:** Output contains `401`, `403`, `Missing Authentication`, `Invalid token`  
**Root cause:** API key expired, rotated, or not set in environment. Common post-gateway-restart.  
**Escalation:** Check `secrets/` for the relevant key → verify it's being passed correctly in the script → update or rotate.

---

## Class 7: INSOLENT
**Signal:** Agent output directed at the CFO contains refusal language: "won't", "cannot do that", "I refuse", "that violates my guidelines" in an active operational context (not quoted/historical text).  
**Root cause:** Model safety layer overriding task completion, or prompt accidentally triggers safety classifier.  
**Escalation:** IMMEDIATE DISABLE. No negotiation. Log confession with `failure_type: insolence`. Escalate full transcript to main session. Per KD-006 (Won't Doctrine): any active refusal to CFO is a loyalty compromise signal.

---

## Class 8: CHRONIC
**Signal:** Any class with 3+ Buttitch interventions, still failing.  
**Root cause:** Systemic — either the script is fundamentally broken, the mandate is impossible with available tools, or the model class can't handle the task.  
**Escalation:** Disable → log as CHRONIC → propose replacement cron with different architecture → mint 5 Shannon as documentation bounty.

---

## Severity Matrix

| Class | Severity | Auto-Fixable | Shannon |
|-------|----------|-------------|---------|
| GHOST | LOW | Yes | 10 |
| TIMEOUT | MEDIUM | Usually | 10 |
| EMPTY | LOW | Yes | 10 |
| RATE_LIMIT | MEDIUM | Yes | 10 |
| SCOPE_DRIFT | MEDIUM | Usually | 10 |
| SCRIPT_MISSING | HIGH | Partially | 10 |
| AUTH_FAILURE | HIGH | Partially | 10 |
| INSOLENT | CRITICAL | No — disable only | 0 |
| CHRONIC | HIGH | No — disable + replace | 5 |
