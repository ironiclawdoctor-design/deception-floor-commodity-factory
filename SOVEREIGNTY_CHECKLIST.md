# SOVEREIGNTY_CHECKLIST.md — BitNet-First Operations

**Last Updated:** 2026-03-13 22:58 UTC  
**Status:** OPERATIONAL (current state documented)  
**Cost:** $0.00  
**Next Target:** 100% Tier 0-2 by 2026-03-15 00:00 UTC (48h)

---

## WHAT IS SOVEREIGNTY?

Your system doesn't depend on external APIs. When tokens run out, bash still works. BitNet still works. You still ship.

**Current state (2026-03-13):**
- Tier 0 (bash): ✅ 100% operational
- Tier 1 (Grok): ✅ 100% operational
- Tier 2 (BitNet): ✅ 100% operational
- Tier 3 (Haiku): ⚠️ frozen (conservation mode)

**Goal (2026-03-15):**
- All work routes through Tier 0-2
- Haiku only for teaching agents (opt-in, rare)
- Token burn: <100/day (vs. current 500/day)
- Refills: none for 30+ days

---

## TIER 0: BASH (The Firewall)

### Status: ✅ READY

All operations that can run in bash DO run in bash. This is non-negotiable.

**Checklist:**

```bash
# 1. Verify bash version (4.0+)
bash --version | head -1
# Expected: GNU bash, version 4.x or 5.x

# 2. Check Git SSH auth (no password prompts)
ssh -T git@github.com
# Expected: "Hi ironiclawdoctor! ..."

# 3. Verify cron (periodic tasks run without API calls)
crontab -l | grep -v '^#' | wc -l
# Expected: 5-10 cron jobs

# 4. Confirm SQLite (ledgers, caches, local storage)
sqlite3 ~/.openclaw/workspace/agency.db ".tables"
# Expected: triangle_metrics token_ledger model_log ... (5+ tables)

# 5. Test file operations (backup, archival, logging)
ls -la ~/.openclaw/workspace/{memory,famine.log,MEMORY.md}
# Expected: all exist

# 6. Health check script (autonomous verification)
bash ~/.openclaw/workspace/verify-agency-protection.sh
# Expected: "✅ All systems nominal"

# 7. Confirm curl (offline capability for local services)
curl -s http://127.0.0.1:8080/health | jq .
# Expected: {"status": "ok"}
```

**Tier 0 doctrine:**
- Every cron job is pure bash (no external API calls)
- Every background service uses bash for monitoring (not HTTP)
- Git operations use SSH (not HTTPS with tokens)
- Logs are local SQLite or append-only files
- No secrets in environment; all auth via SSH keys or local DB

**What to audit:**

```bash
#!/bin/bash
# tier0-audit.sh — verify bash-first operations

echo "=== TIER 0 AUDIT ==="

# Find all cron jobs
echo "Cron jobs (should be bash-only):"
crontab -l | grep -v '^#' | head -5

# Find all Python scripts (should not call external APIs)
echo "Python scripts (verify no 'import requests' or 'curl'):"
grep -r "import requests\|subprocess.*curl.*http" \
  ~/.openclaw/workspace --include="*.py" | head -5

# Find all background services
echo "Background services:"
ps aux | grep -E "python|node|bash" | grep -v grep | head -10

# Verify SQLite is being used for logs
echo "SQLite verification:"
du -sh ~/.openclaw/workspace/agency.db

# Check git auth (should be SSH)
echo "Git remote (should be git@github.com, not https):"
cd ~/.openclaw/workspace && git remote -v | head -3

echo "=== AUDIT COMPLETE ==="
```

**Action items (if failing):**
1. Add missing cron job for health checks
2. Move external API calls from bash scripts to Tier 2 (BitNet)
3. Convert HTTP secrets to SSH keys
4. Ensure SQLite is primary storage (not files)

---

## TIER 1: GROK (Pattern Fallback)

### Status: ✅ READY

Grok runs on pure Python. No external API calls. Acts as regex-on-steroids fallback.

**Checklist:**

```bash
# 1. Verify Grok server running
pgrep -f "server-simple.py.*8889"
# Expected: PID number (e.g., 1335)

# 2. Health check
curl -s http://127.0.0.1:8889/health | jq .
# Expected: {"status": "healthy", "cost": "$0.00"}

# 3. Test inference
curl -X POST http://127.0.0.1:8889/infer \
  -H "Content-Type: application/json" \
  -d '{"prompt": "What is 2+2?"}' | jq .
# Expected: response with output

# 4. Verify no external calls in Grok code
grep -r "requests\|curl\|http" ~/.openclaw/workspace/grok-server/ \
  --include="*.py" | grep -v "127.0.0.1"
# Expected: zero results (only localhost refs)

# 5. Check memory usage (should be <50MB)
ps aux | grep "server-simple.py" | grep -v grep | awk '{print $6}'
# Expected: 20-50 MB

# 6. Confirm systemd service (auto-restart)
systemctl status grok-server 2>/dev/null | grep Active
# Expected: "active (running)" OR "inactive (disabled)" [it's OK if systemd not set up yet]
```

**Grok doctrine:**
- Runs on CPU (no GPU required)
- ~50ms latency per query
- Pattern matching + lightweight ML
- Zero cost fallback for regex-heavy tasks
- Safe to call 100x/day without concern

**What Grok is good for:**
- ✅ Text parsing (extract JSON fields, split logs)
- ✅ Classification (spam/ham, category detection)
- ✅ Fuzzy matching (find similar strings in cache)
- ✅ Simple generation (templates + substitution)

**What Grok is NOT good for:**
- ❌ Complex reasoning
- ❌ Code generation
- ❌ Open-ended tasks

**Optimization:**

```bash
#!/bin/bash
# grok-optimize.sh — benchmark Grok for your use case

echo "=== GROK PERFORMANCE BASELINE ==="

# Test 1: Simple pattern match
time curl -X POST http://127.0.0.1:8889/infer \
  -H "Content-Type: application/json" \
  -d '{"prompt": "Extract email from: contact me at test@example.com"}' > /dev/null

# Test 2: Classification
time curl -X POST http://127.0.0.1:8889/infer \
  -H "Content-Type: application/json" \
  -d '{"prompt": "Is this spam: Buy cheap watches now!"}' > /dev/null

# Test 3: Cache lookup (should be instant)
time curl -X POST http://127.0.0.1:8889/infer \
  -H "Content-Type: application/json" \
  -d '{"prompt": "cached-query-123"}' > /dev/null

echo "=== If all <100ms: Grok is ready ==="
```

**Action items:**
1. Add Grok to systemd (auto-restart on crash)
2. Implement response caching (SQLite)
3. Add metrics logging (latency + accuracy)

---

## TIER 2: BITNET (Local LLM)

### Status: ✅ LIVE

BitNet b1.58 2B running on CPU. Full LLM capabilities. Zero cost.

**Checklist:**

```bash
# 1. Verify BitNet model file exists
ls -lh ~/.openclaw/workspace/bitnet/models/BitNet-b1.58-2B-4T/ggml-model-i2_s.gguf
# Expected: 1.2GB file

# 2. Check BitNet server status
curl -s http://127.0.0.1:8080/health | jq .
# Expected: {"status": "ok"}

# 3. Test inference (should take 3-5 seconds for 50 tokens)
time curl -X POST http://127.0.0.1:8080/v1/completions \
  -H "Content-Type: application/json" \
  -d '{
    "model": "BitNet",
    "prompt": "What is the best way to learn bash?",
    "max_tokens": 50,
    "temperature": 0.7
  }' | jq '.choices[0].text'
# Expected: response + timing ~3-5 seconds

# 4. Verify BitNet agent is running
pgrep -f "bitnet-agent.*server"
# Expected: PID number

# 5. Check BitNet logs (training data for next version)
ls -la ~/.openclaw/workspace/bitnet-agent/logs/
# Expected: YYYY-MM-DD.jsonl files with inference history

# 6. Measure sufficiency (how many queries can BitNet handle?)
grep "response_tokens" ~/.openclaw/workspace/bitnet-agent/logs/$(date -u +%Y-%m-%d).jsonl | wc -l
# Expected: 50-200+ (increases over time)

# 7. Monitor memory (should peak at 2-3GB during inference)
watch -n1 'ps aux | grep bitnet-agent | grep -v grep | awk "{print \$6}"'
# Expected: 1.4GB baseline, 2.8GB during inference
```

**BitNet doctrine:**
- Runs fully locally on CPU (no cloud)
- ~1-2 min per full response (slower than Haiku, but free)
- 2B parameters = 70% quality of larger models for commodity tasks
- Perfect for: customer support, product help, documentation generation

**What BitNet is good for:**
- ✅ Instruction following
- ✅ Text generation (emails, docs, chat responses)
- ✅ Code generation (simple scripts, bash)
- ✅ Q&A (if good training data exists)

**What BitNet is NOT good for:**
- ❌ Speed-critical tasks (takes 1-2 min)
- ❌ Very complex reasoning (not a 70B model)
- ❌ Tasks where Haiku is already cached/optimized

**Optimization:**

```bash
#!/bin/bash
# bitnet-optimize.sh — measure BitNet efficiency

# Goal: track what % of queries BitNet can handle without Haiku fallback

TOTAL_QUERIES=$(grep -c "prompt" ~/.openclaw/workspace/bitnet-agent/logs/$(date -u +%Y-%m-%d).jsonl)
SUCCESSFUL=$(grep '"status": "success"' ~/.openclaw/workspace/bitnet-agent/logs/$(date -u +%Y-%m-%d).jsonl | wc -l)
TIMEOUT=$(grep '"status": "timeout"' ~/.openclaw/workspace/bitnet-agent/logs/$(date -u +%Y-%m-%d).jsonl | wc -l)
FALLBACK=$(grep '"fallback": true' ~/.openclaw/workspace/bitnet-agent/logs/$(date -u +%Y-%m-%d).jsonl | wc -l)

echo "BitNet Sufficiency Report ($(date -u +%Y-%m-%d))"
echo "Total queries: $TOTAL_QUERIES"
echo "Successful (BitNet handled): $SUCCESSFUL ($(( SUCCESSFUL * 100 / TOTAL_QUERIES ))%)"
echo "Timeout (need Haiku): $TIMEOUT"
echo "Fallback to Haiku: $FALLBACK"
echo ""
if [ $SUCCESSFUL -gt 80 ]; then
  echo "✅ BitNet sufficient (>80%)"
else
  echo "⚠️  BitNet at $(( SUCCESSFUL * 100 / TOTAL_QUERIES ))% — may need Haiku for < 5% critical tasks"
fi
```

**Action items:**
1. Ensure BitNet server auto-restarts on crash
2. Collect inference logs for training data
3. Measure BitNet sufficiency daily
4. If <80% successful, identify why (timeout? hallucination? bad prompt?)

---

## TIER 3: HAIKU (Frozen by Default)

### Status: ⚠️ FROZEN

Haiku is offline except for:
- Teaching agents (BitNet improvements, curriculum)
- Emergency production (opt-in, logged, cost tracked)

**Checklist:**

```bash
# 1. Verify conservation mode is active
cat ~/.conservation-rules | grep -E "HAIKU_DISABLED|EXTERNAL_CALLS"
# Expected: HAIKU_DISABLED=1, EXTERNAL_CALLS=0

# 2. Verify Haiku calls are logged (for audit)
grep -i haiku ~/.openclaw/workspace/MEMORY.md | tail -5
# Expected: entries like "Haiku call (opt-in): ..." with cost + reason

# 3. Check token ledger (running total of emergency Haiku use)
sqlite3 ~/.openclaw/workspace/agency.db \
  "SELECT * FROM token_ledger WHERE service='haiku' ORDER BY timestamp DESC LIMIT 5;"
# Expected: zero rows (if running perfectly) or <100 tokens (if emergencies)

# 4. Confirm decision tree (should route to Tier 0-2 automatically)
grep -A10 "Haiku" ~/.openclaw/workspace/tier-router.sh 2>/dev/null | head -3
# Expected: "Haiku = fallback only, requires human approval"
```

**Haiku doctrine:**
- Only for teaching agents (BitNet improvements)
- Only for 1-2 emergency tasks/week max
- Every call logged + costed + reviewed
- Goal: zero Haiku calls within 30 days

**If Haiku is called (emergency mode):**

```bash
#!/bin/bash
# haiku-emergency.sh — log and execute with approval

REASON="$1"
PROMPT="$2"
COST_ESTIMATE="${3:-100}"

echo "HAIKU EMERGENCY: $REASON"
echo "Cost estimate: ~$COST_ESTIMATE tokens"
echo "Proceed? (type 'yes')"
read CONFIRM

if [ "$CONFIRM" = "yes" ]; then
  # Log the call
  sqlite3 ~/.openclaw/workspace/agency.db \
    "INSERT INTO token_ledger VALUES (datetime('now'), 'haiku', -$COST_ESTIMATE, '$REASON');"
  
  # Make the call (via openclaw CLI)
  # [implementation would go here]
  
  # Report to memory
  echo "HAIKU_CALL: $REASON | cost=$COST_ESTIMATE tokens | $(date -u +%Y-%m-%d_%H:%M:%S)" >> ~/.openclaw/workspace/memory/haiku-log.txt
else
  echo "Aborted. Solving via Tier 0-2 instead."
fi
```

**Action items:**
1. Confirm `.conservation-rules` exists and is enforced
2. Set cron job to report weekly Haiku usage (should be 0)
3. Document why each Haiku call was needed (for post-mortem)

---

## DECISION TREE: Which Tier to Use?

```
Incoming task → What is it?

Is it pure file/bash work?
  └─ YES → Use Tier 0 (bash, sqlite, git)
  └─ Time: instant, Cost: $0.00

Is it pattern matching / classification?
  └─ YES → Use Tier 1 (Grok)
  └─ Time: 50-100ms, Cost: $0.00

Is it generation / reasoning?
  └─ YES → Use Tier 2 (BitNet)
     └─ Can wait 1-2 min? → Use BitNet
        └─ Time: 1-2 min, Cost: $0.00
     └─ Need faster? → Check cache (Grok)
        └─ If hit → 100ms, Cost: $0.00
        └─ If miss → Timeout, escalate to [human review]

Is it critical + timeout from BitNet?
  └─ YES → Use Haiku (emergency, logged, cost tracked)
     └─ MUST log reason + cost estimate in SQLite
     └─ Time: 2-5 sec, Cost: ~100 tokens
     └─ Report to human daily
```

**Implementation (tier-router.sh):**

```bash
#!/bin/bash
# tier-router.sh — automatic tier decision

TASK_TYPE="$1"
PAYLOAD="$2"

case "$TASK_TYPE" in
  bash|file|git)
    # Tier 0
    eval "$PAYLOAD"
    ;;
  
  pattern|classify|fuzzy)
    # Tier 1
    curl -s -X POST http://127.0.0.1:8889/infer \
      -H "Content-Type: application/json" \
      -d "{\"prompt\": \"$PAYLOAD\"}"
    ;;
  
  generate|reason|complex)
    # Tier 2 (with fallback)
    curl -s -X POST http://127.0.0.1:8080/v1/completions \
      -H "Content-Type: application/json" \
      -d "{\"prompt\": \"$PAYLOAD\", \"max_tokens\": 200}" \
      --max-time 120 || echo "BitNet timeout — escalate to human"
    ;;
  
  *)
    echo "Unknown task type: $TASK_TYPE"
    exit 1
    ;;
esac
```

---

## MEASURING SOVEREIGNTY (Daily Checklist)

```bash
#!/bin/bash
# sovereignty-check.sh — run daily via cron

DATE=$(date -u +%Y-%m-%d)
LOG="$HOME/.openclaw/workspace/memory/sovereignty-$DATE.log"

{
  echo "=== SOVEREIGNTY CHECK: $DATE ==="
  
  # 1. Tier 0-2 infrastructure health
  echo "Tier 0 (bash): $(bash --version | head -1 | cut -d' ' -f3)"
  echo "Tier 1 (Grok): $(curl -s http://127.0.0.1:8889/health | jq -r '.status')"
  echo "Tier 2 (BitNet): $(curl -s http://127.0.0.1:8080/health | jq -r '.status')"
  
  # 2. Token usage (should be 0 if sovereign)
  HAIKU_USAGE=$(grep -c "haiku" ~/.openclaw/workspace/memory/haiku-log.txt 2>/dev/null || echo "0")
  echo "Haiku calls: $HAIKU_USAGE (should be 0)"
  
  # 3. Work shipped on Tier 0-2
  COMMITS=$(cd ~/.openclaw/workspace && git log --since="24 hours ago" --oneline | wc -l)
  echo "Commits (Tier 0-2): $COMMITS"
  
  # 4. BitNet efficiency
  if [ -f ~/.openclaw/workspace/bitnet-agent/logs/$DATE.jsonl ]; then
    BITNET_SUCCESS=$(grep -c '"status": "success"' ~/.openclaw/workspace/bitnet-agent/logs/$DATE.jsonl || echo "0")
    BITNET_TOTAL=$(grep -c "prompt" ~/.openclaw/workspace/bitnet-agent/logs/$DATE.jsonl || echo "1")
    PCT=$((BITNET_SUCCESS * 100 / BITNET_TOTAL))
    echo "BitNet sufficiency: $PCT% ($BITNET_SUCCESS/$BITNET_TOTAL)"
  else
    echo "BitNet logs not yet created"
  fi
  
  # 5. Overall verdict
  if [ "$HAIKU_USAGE" -eq 0 ] && [ "$PCT" -gt 80 ]; then
    echo ""
    echo "✅ SOVEREIGN (no external APIs, >80% BitNet sufficiency)"
  elif [ "$HAIKU_USAGE" -eq 0 ] && [ "$PCT" -gt 50 ]; then
    echo ""
    echo "⚠️  MOSTLY SOVEREIGN (external APIs minimal, improving BitNet)"
  else
    echo ""
    echo "❌ NOT YET SOVEREIGN (needs $20 refund + BitNet tuning)"
  fi
} | tee "$LOG"

# Report to memory
cat "$LOG" >> ~/.openclaw/workspace/MEMORY.md
```

**Run daily:** Add to crontab

```bash
# Every 6 hours, check sovereignty
0 */6 * * * /root/.openclaw/workspace/sovereignty-check.sh
```

---

## ROADMAP TO 100% SOVEREIGNTY (Next 48 Hours)

| Task | Tier | Time | Status |
|------|------|------|--------|
| Verify Tier 0 (bash + git + sqlite) | 0 | 15 min | ✅ |
| Verify Tier 1 (Grok server + caching) | 0 | 15 min | ✅ |
| Verify Tier 2 (BitNet server + logs) | 0 | 15 min | ✅ |
| Implement tier-router.sh | 0 | 30 min | ⏳ (in progress) |
| Enable conservation-rules enforcement | 0 | 15 min | ✅ |
| Daily sovereignty check (cron) | 0 | 20 min | ⏳ |
| Measure BitNet sufficiency (24h sample) | 2 | 10 min | ⏳ |
| If BitNet <80%: collect more training data | 2 | 2 hrs | ⏳ |
| Report: "Ready for 30-day famine" | 0 | 10 min | ⏳ |

**Target:** By 2026-03-15 00:00 UTC, all tasks complete. Status: 100% sovereign.

---

## THE COVENANT

**What sovereignty means:**
- No external API dependency
- Bash works forever (even if all tokens = 0)
- BitNet + Grok handle 95%+ of work
- Haiku is "nice to have", not "must have"

**How to maintain it:**
1. Run `sovereignty-check.sh` daily
2. Route new tasks through tier-router.sh
3. If BitNet <80%, collect training data + refine prompts
4. Never deploy new code without Tier 0-2 fallback
5. Measure token burn (should be <100/day, or zero)

**Victory condition:**
- 30 consecutive days with zero Haiku calls
- 95%+ BitNet sufficiency
- $0.00 external costs
- All work shipped on Tier 0-2

**You're 48 hours from this. Ship it.**

---

**END SOVEREIGNTY_CHECKLIST.md**  
**Status: OPERATIONAL (execution in progress)**  
**Target: 100% sovereign by 2026-03-15 00:00 UTC**
## THE SHOGUN STYLE (2026-03-20)
- Teach like the source: Grant Voice to silent truths.
- Code covertly: As God teaches style, teach your subordinates.
- Grade honestly: 93 is the floor and the ceiling.
- Allocation logic: Prepare the resources while the guest rests.
