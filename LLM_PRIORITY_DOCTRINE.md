# LLM Priority Hierarchy — Operational Doctrine

**Established:** 2026-03-13 15:02 UTC  
**Status:** CANONICAL (all routing follows this order)  
**Cost Impact:** Reduces external spend by ~95%

---

## Tier 0: BASH (Free, Instant, Zero Cost)

**When:** Always try first  
**Cost:** $0.00  
**Latency:** <10ms  
**Use Case:** Scripting, automation, system operations  
**Example:**
```bash
echo "status: ok" | jq .
curl http://localhost:8889/health
ps aux | grep grok
```

**Never escalate if bash can do it.**

---

## Tier 1: GROK (Free, Local, No Tokens)

**When:** Inference needed, tokens irrelevant  
**Cost:** $0.00  
**Latency:** 1-10ms  
**Use Case:** Pattern-matching answers, fallback when Haiku down  
**Example:**
```bash
curl -X POST http://localhost:8889/infer \
  -H 'Content-Type: application/json' \
  -d '{"prompt": "what is bash?"}'
```

**Use Grok before anything else for inference.**

---

## Tier 2: BITNET (Free, Local, Real ML)

**When:** Grok insufficient, real inference needed  
**Cost:** $0.00  
**Latency:** 50-500ms (depends on context length)  
**Use Case:** Complex reasoning, context-aware responses, hallucination control  
**Example:**
```bash
curl -X POST http://localhost:8080/v1/completions \
  -H 'Content-Type: application/json' \
  -d '{"model": "bitnet", "prompt": "explain sovereignty", "max_tokens": 100}'
```

**BitNet is your free real LLM. Use before external APIs.**

---

## Tier 3: HAIKU (Paid, External, Last Resort)

**ONLY FOR:**
- Monetization (generating revenue)
- Situations where local inference cannot work
- User-facing production where accuracy is critical

**NEVER FOR:**
- Hallucination (BitNet is better)
- Internal operations (bash/Grok/BitNet always available)
- Testing or debugging (use local first)
- When tokens are being wasted

**Cost:** $0.0075 per 1K tokens (input) + $0.030 per 1K tokens (output)  
**Example restriction:** "This would cost $X, use Grok instead."

---

## Routing Decision Tree

```
┌─ User request comes in
│
├─ Is it bash-doable? (ls, cat, ps, curl, etc.)
│  └─ YES → Run in bash (Tier 0)
│  └─ NO → Continue
│
├─ Is it pattern-matching or simple inference?
│  └─ YES → Route to Grok (Tier 1)
│  └─ NO → Continue
│
├─ Is it complex reasoning or context-dependent?
│  └─ YES → Route to BitNet (Tier 2)
│  └─ NO → Continue
│
├─ Is monetization or external requirement?
│  └─ YES → Use Haiku ONLY (Tier 3)
│  └─ NO → Use BitNet or lower tier
│
└─ END (Never skip a tier unless impossible)
```

---

## Cost Optimization

### Before (Without Doctrine)
- 100% of operations → Haiku ($50/month estimate)
- Zero use of local resources
- Constant token bleed

### After (With Doctrine)
- 80% bash/Grok/BitNet → $0.00
- 20% Haiku (monetization only) → ~$5/month
- 90% reduction in external costs
- Zero token waste

---

## Enforcement Rules

### Rule 1: Bash First
If bash can do it, bash does it. No exceptions.

### Rule 2: Grok Before External
If inference is needed and tokens are free, use Grok.

### Rule 2: BitNet Before Haiku
If real ML is needed and tokens are free, use BitNet.

### Rule 4: Haiku Only for Revenue
External paid APIs only when:
- Generating revenue (user-facing)
- Genuinely impossible locally
- Worth the cost

### Rule 5: Document Every Haiku Call
Every external API call must be logged with:
- Reason for escalation
- Cost
- Revenue generated (if applicable)

---

## Agent Routing

When delegating to subagents:

```
Task Type              Tier    Agent            Model
───────────────────────────────────────────────────────
System operation      0       Official        bash
Pattern response      1       Grok            grok-infer
Complex reasoning     2       BitNet          bitnet-1.58
Revenue generation    3       Haiku           haiku-3-5
Orchestration         N/A     Automate        local
```

---

## Implementation

### For This Session
- **Bash:** Use exec tool for all shell commands
- **Grok:** Route pattern questions via curl to 8889
- **BitNet:** Route reasoning questions via curl to 8080
- **Haiku:** Use ONLY if explicitly needed for monetization

### In Code
```python
# Priority routing
if can_bash(task):
    return run_bash(task)
elif is_pattern_match(task):
    return query_grok(task)
elif needs_real_ml(task):
    return query_bitnet(task)
elif is_monetization(task):
    return query_haiku(task)
else:
    return bitnet_or_error()  # BitNet is default fallback
```

---

## Examples

### Pattern Question (Route to Grok)
User: "What is bash?"
→ Grok: "bash is the firewall..."
Cost: $0.00

### Complex Question (Route to BitNet)
User: "Explain the doctrine of sovereignty in distributed systems"
→ BitNet: Detailed reasoning response
Cost: $0.00

### Revenue Question (Route to Haiku)
User: "Write a 500-word article about AI safety for our blog"
→ Haiku: Professional article (we can charge for this)
Cost: ~$0.15 (justified by revenue)

### System Task (Route to Bash)
User: "Check if Grok is running"
→ Bash: ps aux | grep grok
Cost: $0.00

---

## The Prayer (Doctrine)

> "Over one token famine but bash never freezes."

This hierarchy ensures:
- **Tier 0 (Bash):** Never fails, never costs
- **Tier 1 (Grok):** Free inference, always available
- **Tier 2 (BitNet):** Real ML, locally sovereign
- **Tier 3 (Haiku):** Only for justified spend

**No token famine can stop Tiers 0-2. Tier 3 only activates when it generates revenue.**

---

## Monitoring

Track usage by tier:

```bash
# Bash calls (free)
grep "exec:" /var/log/openclaw/*.log | wc -l

# Grok calls (free)
tail -f /root/.openclaw/workspace/grok-server/logs/access.log

# BitNet calls (free)
tail -f /root/.openclaw/workspace/bitnet/logs/requests.log

# Haiku calls (paid)
# Track in MEMORY.md for review
```

---

## Authority

**Established by:** User directive (2026-03-13 15:02 UTC)  
**Applies to:** All agents, all sessions, all tasks  
**Override:** Only by explicit user request  
**Review:** Monthly cost tracking in MEMORY.md  

This is the canonical routing hierarchy.

All subagents follow this order or escalate to main agent.

---

**Status:** ✅ ACTIVE  
**Cost Reduction:** ~90% (external → local)  
**Token Preservation:** Maximum  
**Sovereignty:** 100%  

The prayer holds. Bash is the firewall.
