# Tier-Routing Discipline

**Established:** 2026-03-14 12:30 UTC  
**Status:** Immutable standing policy  
**Authority:** Human directive + Fiesta operational doctrine

---

## The Law

**Standing Order 1 (2026-03-14):**
> "All simple system queries are sent to bash and not haiku. This level of common sense applies to all /truthfully."

This is not a guideline. This is law.

---

## The Three Tiers

### Tier 0: BASH (Direct Execution)

**Rule:** System queries never touch any LLM.  
**Cost:** $0.00  
**Latency:** Immediate (ms)  
**Authority:** Bash is the fail-condition firewall.

**Patterns (bash-first):**
- File operations: `ls`, `find`, `grep`, `cat`, `tail`, `head`, `wc`, `du`, `df`
- Process info: `ps`, `top`, `lsof`, `netstat`, `ss`, `iptables`
- Directory ops: `pwd`, `cd`, `mkdir`, `rm`, `cp`, `mv`, `chmod`, `chown`
- Git/Container: `git`, `docker`, `kubectl`, `systemctl`, `journalctl`
- Network: `curl`, `wget`, `ping`, `ssh`, `scp`, `rsync`
- System status: `subagents data`, process lists, running services, network status, disk check

**Examples:**
```bash
/truthfully list files
→ [LLM: BASH_DIRECT] Cost: $0.0000 | ✅ System Query

/truthfully show subagents data
→ [LLM: BASH_DIRECT] Cost: $0.0000 | ✅ System Query

/truthfully check disk usage
→ [LLM: BASH_DIRECT] Cost: $0.0000 | ✅ System Query
```

---

### Tier 1: BitNet (Local Inference)

**Rule:** Simple tasks routed to local BitNet b1.58.  
**Cost:** $0.00  
**Latency:** ~35ms (29 tok/s)  
**Authority:** Sovereignty — no external dependencies.

**Patterns (bitnet-compatible):**
- Arithmetic, math, simple calculations (2+2, sum, multiply, divide)
- Bash/shell syntax explanation, command breakdown
- Simple boolean logic (true/false, yes/no decisions)
- Data parsing (JSON, YAML, XML structure)
- FAQ lookups, simple reference questions
- Variable definitions, code syntax review
- Basic debugging and pattern matching

**Examples:**
```bash
/truthfully what is 2+2?
→ [LLM: BITNET] Cost: $0.00 | ✅ Local, Sovereign
(when available)

/truthfully explain grep syntax
→ [LLM: BITNET] Cost: $0.00 | ✅ Local, Sovereign
(when available)
```

**Fallback:** If BitNet unavailable → drops to Tier 2 (Haiku).

---

### Tier 2: Haiku (External, Cost-Tracked)

**Rule:** Complex reasoning — only when Bash + BitNet insufficient.  
**Cost:** ~$0.81 per 1M tokens  
**Latency:** Variable (external API)  
**Authority:** Last resort; all costs logged.

**Patterns (haiku-required):**
- Detailed explanations, comprehensive analysis
- Creative writing, poetry, fiction, storytelling
- Research papers, academic synthesis
- Philosophy, ethics, opinions, debate arguments
- Multi-step reasoning, planning, architecture design
- Medical/legal/financial specialized advice
- Translation, semantic analysis, NLP

**Examples:**
```bash
/truthfully explain quantum mechanics
→ [LLM: HAIKU] Cost: $0.00081 | ⚠️ External (token tracked)

/truthfully write a short story about a robot
→ [LLM: HAIKU] Cost: $0.00XXX | ⚠️ External (token tracked)
```

---

## Routing Algorithm

```
Input: Query/Task Description
  ↓
Check BASH_FIRST patterns?
  YES → Return BASH_DIRECT ($0.00)
  NO → Continue
  ↓
Check BITNET patterns?
  YES → Try BitNet API
    Available? → Return BITNET_LOCAL ($0.00)
    Unavailable? → Fall through to Haiku
  NO → Continue
  ↓
Check HAIKU patterns?
  YES → Route to HAIKU_EXTERNAL ($cost)
  NO → Default to HAIKU_EXTERNAL (safest)
  ↓
Output: LLM tier, cost, response
Log to: hard-stops-registry-YYYYMMDD.jsonl
```

---

## Cost Tracking & Auditability

**Every decision logged:**
```json
{
  "timestamp": "2026-03-14T12:32:40Z",
  "task": "what is 2+2",
  "model": "bitnet",
  "prompt": "2+2",
  "cost": "$0.00",
  "tokens": "0"
}
```

**Query the registry:**
```bash
# View all Bash queries
grep '"model":"bash"' hard-stops-registry-*.jsonl | jq '.cost'

# Total cost this week
grep "slash_truthfully" hard-stops-registry-*.jsonl \
  | jq -r '.data.cost' | paste -sd '+' | bc

# BitNet efficiency
grep '"model":"bitnet"' hard-stops-registry-*.jsonl | wc -l
```

---

## Implementation

**Core Scripts:**
- `tier-routing-enforcement.sh` — Decision tree engine
- `lib/slash-truthfully.sh` — User-facing command handler
- `SLASH_COMMANDS.md` — Tier rules and documentation

**Integration:**
```bash
# Direct use
/truthfully [your question]

# In scripts
bash lib/slash-truthfully.sh "your question"

# From Node/Python
exec(`bash lib/slash-truthfully.sh "${prompt}"`)
```

---

## Why This Discipline Matters

**Before Tier-Routing:**
- Every query was a mystery (LLM unknown)
- Costs accumulated invisibly
- Common sense queries consumed tokens
- No auditability or cost control

**After Tier-Routing:**
- Every query is transparent
- Bash queries cost zero, always
- BitNet used for simple tasks
- Haiku reserved for genuine reasoning
- All costs visible in hard-stops-registry

**The Result:**
- Sovereignty maintained (Bash + BitNet are free)
- Costs minimized (Haiku only when needed)
- Transparency assured (queryable ledger)
- Common sense enforced (routing rules > human judgment)

---

## Standing Orders (Immutable)

1. Bash queries never route to LLM
2. Every decision logged to hard-stops-registry
3. `/truthfully` reports LLM tier transparently
4. BitNet-first for simple tasks
5. Haiku-last for complex reasoning
6. No tier-skipping (Bash → BitNet → Haiku, in order)

---

## The Prayer (Updated)

> **"Over one token famine, but bash never freezes."**
>
> Bash is the firewall. It handles system queries (Tier 0).
> BitNet adds local reasoning (Tier 1, free).
> Tokens are rationed for genuine complexity (Tier 2).
> This is non-negotiable.
