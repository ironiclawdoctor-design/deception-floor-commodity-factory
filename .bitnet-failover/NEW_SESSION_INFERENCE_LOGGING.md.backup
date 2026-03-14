# `/new` Session Inference Logging

**Established:** 2026-03-14 12:35 UTC  
**Purpose:** Complete transparency for internal inference with automatic diagnosis before fallback  
**Status:** Operational

---

## What Changed

Previously, when BitNet failed, we'd fallback to Haiku immediately with no diagnosis.

**Now:**
1. **Log every tier attempt** (Bash → BitNet → Haiku)
2. **On BitNet failure, diagnose why** (before fallback)
3. **Collect available agency agents** (before Haiku cost)
4. **Decide intelligently:** Retry, escalate to agents, or fallback

---

## The `/new` Workflow

```
Input: Task
  ↓
PHASE 1: Bash Attempt
  - Log attempt
  - Skip if not a system query
  ↓
PHASE 2: BitNet Attempt
  - Log health check
  - Log inference attempt
  - If succeeds → Done (Tier 1)
  - If fails → Continue
  ↓
PHASE 3: BitNet Failure Diagnosis
  - Check process status
  - Check port availability
  - Check HTTP connectivity
  - Check inference latency
  - Check system resources
  - Generate recommendation (retry, escalate, or fallback)
  ↓
PHASE 4: Collect Agency Agents
  - List available agents
  - Log if available
  ↓
PHASE 5: Fallback Decision
  - If BitNet is healthy → RETRY (transient failure)
  - If BitNet is unhealthy → Escalate to agents
  - If agents unavailable → FALLBACK to Haiku
  ↓
Output: Result + Inference Log
```

---

## Diagnostic Suite

**File:** `lib/bitnet-diagnostics.sh`

Runs 6 diagnostic phases:
1. **Process Status** — Is inference process running?
2. **Port Availability** — Is port 8080 listening?
3. **HTTP Connectivity** — Does `/health` endpoint respond?
4. **Inference Latency** — Can we run a test inference?
5. **Error Logs** — Any recent errors?
6. **System Resources** — Memory/CPU/Disk OK?

**Recommendation Engine:**
- ✅ All checks pass → "RETRY BitNet (transient failure)"
- ⚠️  Some checks fail → "ESCALATE to agents or fallback to Haiku"

**Run manually:**
```bash
bash lib/bitnet-diagnostics.sh
```

**Output:**
```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🎯 RECOMMENDATION
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
✅ BitNet is HEALTHY. Failover to Haiku is optional (not required).
   Recommendation: RETRY with BitNet
```

---

## Inference Logging

**File:** `inference-log-YYYYMMDD.jsonl`

Every attempt logged as JSON line:
```json
{
  "timestamp": "2026-03-14T12:37:49Z",
  "tier": "bash",
  "task": "what is 2+2?",
  "status": "skip",
  "detail": "not_a_system_query"
}
{
  "timestamp": "2026-03-14T12:37:49Z",
  "tier": "bitnet",
  "task": "what is 2+2?",
  "status": "attempt",
  "detail": "health_ok"
}
{
  "timestamp": "2026-03-14T12:37:49Z",
  "tier": "bitnet",
  "task": "what is 2+2?",
  "status": "success",
  "detail": "503ms"
}
```

**Query the log:**
```bash
# All attempts for task
grep '"task":"what is 2+2?"' inference-log-*.jsonl | jq '.'

# Summary by tier
jq -r '.tier' inference-log-*.jsonl | sort | uniq -c

# All failures
grep '"status":"failed"' inference-log-*.jsonl | jq '.detail'

# Latency measurements
grep '"tier":"bitnet"' inference-log-*.jsonl | grep '"status":"success"' | jq '.detail'
```

---

## Bottleneck Detection

**If BitNet is the bottleneck:**

### Scenario 1: Process is dead
```
❌ BitNet agent NOT running
✅ Port 8080 is listening (via ss)
✅ HTTP /health endpoint responds

→ Process name changed (llama-server, not bitnet-agent)
→ Update process check in diagnostics
→ Recommendation: Verify process and restart if needed
```

### Scenario 2: Port not available
```
❌ BitNet agent NOT running
❌ Port 8080 is NOT listening
✅ HTTP connection refused

→ Process crashed or not started
→ Restart: systemctl restart bitnet-agent
→ Or: python3 bitnet-agent/agent.py --server
```

### Scenario 3: Timeout or slowness
```
✅ Process running
✅ Port listening
❌ HTTP timeout (2s threshold)
→ High latency (>5s on simple inference)

→ System resources exhausted or network issue
→ Check CPU, memory, disk
→ Consider rate limiting or concurrent request queue
```

---

## Agency Escalation

**Before Haiku fallback, all available agents are collected:**

```bash
# agents_list returns available agents (if configured)
# Example: [Automate, Official, Daimyo, bashbug, ...]

# If agents available:
# → Can delegate task to agent before token cost
# → Example: Official agent handles the inference task
# → Logs which agent handled it

# If no agents:
# → Proceed to Haiku fallback
# → Log that agents were unavailable
```

---

## Example Session

### Command
```bash
/new what is 2+2?
```

### Log Output
```
╔════════════════════════════════════════════════════════════════╗
║         /new Session with Full Inference Logging              ║
║         2026-03-14 12:37:49 UTC                               ║
╚════════════════════════════════════════════════════════════════╝

Task: what is 2+2?
Log:  /root/.openclaw/workspace/inference-log-20260314.jsonl

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🔧 Tier 0: BASH Inference Attempt
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
⏭️  Task is not a bash command

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
⚡ Tier 1: BitNet Inference Attempt
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
✅ BitNet health check passed
✅ BitNet inference succeeded (503ms)
   Response: 4, 2+2=4, ...

✅ Task handled by BitNet (Tier 1)
```

### Inference Log
```json
{"timestamp":"2026-03-14T12:37:49Z","tier":"bash","task":"what is 2+2?","status":"skip","detail":"not_a_system_query"}
{"timestamp":"2026-03-14T12:37:49Z","tier":"bitnet","task":"what is 2+2?","status":"attempt","detail":"health_ok"}
{"timestamp":"2026-03-14T12:37:49Z","tier":"bitnet","task":"what is 2+2?","status":"success","detail":"503ms"}
```

---

## Files Created/Updated Today

| File | Purpose | Status |
|------|---------|--------|
| `lib/bitnet-diagnostics.sh` | 6-phase diagnostic suite | ✅ Live |
| `lib/session-with-inference-logging.sh` | `/new` handler with logging | ✅ Live |
| `lib/demo-inference-logging.sh` | Demonstration of logging | ✅ Live |
| `inference-log-YYYYMMDD.jsonl` | Inference attempt ledger | ✅ Operational |
| `bitnet-diagnostics-YYYYMMDD.jsonl` | Diagnostic results ledger | ✅ Operational |

---

## Integration Points

### Tier-Routing + Inference Logging

**Tier-routing** (`/truthfully`) → Decides which tier to use  
**Inference logging** (`/new`) → Records what actually happened

Together they provide:
- **Transparency:** Every decision logged
- **Diagnostics:** Why did fallback occur?
- **Auditability:** Complete history of all attempts
- **Intelligence:** Data to optimize tier selection over time

---

## The Law

**Standing Order 2 (2026-03-14 12:35 UTC):**
> "If BitNet is the bottleneck, diagnose with bash THEN escalate to all available agency agents BEFORE fallback to Haiku."

No blind fallback to expensive tiers. Diagnose first. Use agents second. Haiku only when necessary.

---

## Monitoring

**Real-time:**
```bash
# Watch inference log
tail -f inference-log-*.jsonl | jq '.'

# BitNet health
bash lib/bitnet-diagnostics.sh | grep "RECOMMENDATION"
```

**Historical analysis:**
```bash
# What failed today?
grep '"status":"failed"' inference-log-*.jsonl | jq '.task'

# How many times did BitNet fail?
grep '"tier":"bitnet"' inference-log-*.jsonl | grep '"status":"failed"' | wc -l

# Average latency when successful
grep '"tier":"bitnet"' inference-log-*.jsonl | grep '"status":"success"' \
  | jq -r '.detail' | sed 's/ms//' | awk '{sum+=$1; count++} END {print sum/count "ms"}'
```

---

## Summary

**Before:** BitNet fails → Fallback to Haiku (token cost, no diagnosis)

**After:**
1. Log every attempt (Bash, BitNet)
2. On failure, diagnose why (6-phase suite)
3. Escalate to agents (if available)
4. Only fallback to Haiku when necessary
5. All steps logged to queryable JSONL

**Result:** 
- Complete transparency
- Cost minimization (agents before Haiku)
- Root cause analysis (via diagnostics)
- Measurable optimization data
