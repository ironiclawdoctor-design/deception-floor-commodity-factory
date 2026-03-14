# Slash Commands — Transparent LLM Routing

## `/truthfully` — Honest Cost & LLM Reporting

Ask a question and get back **exactly what LLM answered it**, along with **transparent cost tracking**.

### Usage

```
/truthfully [prompt]
```

### Examples

```
/truthfully What is 2+2?
/truthfully Explain quantum mechanics
/truthfully Write a bash function to list files
```

### Output

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🎯 /truthfully — Transparent LLM Routing
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

[LLM: BITNET] Cost: $0.00 | Tokens: 0 | ✅ Local, Sovereign

Prompt: What is 2+2?

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

4

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📊 Cost Summary (logged):
   LLM Tier: BITNET
   Cost: $0.00
   Tokens: 0
   Registry: /root/.openclaw/workspace/hard-stops-registry-20260314.jsonl
```

### What It Does

1. **Routes intelligently** — Uses tier-routing-enforcement to classify your prompt
2. **Selects the right LLM:**
   - **BitNet** (local, $0.00) — Simple questions, arithmetic, bash, logic
   - **Haiku** (external, tracked) — Complex reasoning, creative work, analysis
3. **Reports transparently:**
   - Which LLM actually answered
   - Exact cost (or $0.00 for local)
   - Token count (for Haiku)
4. **Logs everything** — All decisions go to `hard-stops-registry-YYYYMMDD.jsonl`

### Key Features

✅ **Transparency:** Know exactly what LLM answered and what it cost  
✅ **Cost Control:** Simple tasks never touch expensive models  
✅ **Sovereignty:** BitNet stays local ($0.00)  
✅ **Auditability:** Every decision logged to registry  
✅ **No Surprises:** Prompts routed consistently by the same rules  

### Implementation

- **Script:** `/root/.openclaw/workspace/lib/slash-truthfully.sh`
- **Routing Engine:** `/root/.openclaw/workspace/tier-routing-enforcement.sh`
- **Cost Registry:** `/root/.openclaw/workspace/hard-stops-registry-YYYYMMDD.jsonl`
- **Logs:** `/root/.openclaw/workspace/slash-truthfully.log`

### Integration

**For OpenClaw UI:**
```bash
/truthfully What is the capital of France?
```

**From scripts:**
```bash
bash /root/.openclaw/workspace/lib/slash-truthfully.sh "Your prompt here"
```

**From Node/Python:**
```javascript
// Call the bash script with your prompt
exec(`bash /root/.openclaw/workspace/lib/slash-truthfully.sh "${prompt}"`);
```

### Cost Tracking

Every `/truthfully` call is logged to the hard-stops registry:

```json
{
  "timestamp": "2026-03-14T12:27:01Z",
  "event": "slash_truthfully",
  "source": "user_command",
  "prompt": "What is 2+2?",
  "llm_tier": "BITNET",
  "cost": "$0.00",
  "tokens": "0",
  "status": "success"
}
```

Query the registry:
```bash
grep "slash_truthfully" /root/.openclaw/workspace/hard-stops-registry-*.jsonl | jq '.data | {llm_tier, cost, tokens}' | head -10
```

### Tier Routing Rules (3-Tier Priority)

**Tier 0: BASH (Direct Execution, $0.00):**
System queries — NEVER sent to any LLM:
- File operations: `ls`, `find`, `grep`, `cat`, `tail`, `head`
- Process info: `ps`, `top`, `lsof`, `netstat`
- Directory ops: `pwd`, `cd`, `mkdir`, `rm`, `cp`, `mv`, `chmod`
- Git/Docker/K8s: `git`, `docker`, `kubectl`, `systemctl`
- Network: `curl`, `wget`, `ping`, `ssh`, `scp`, `rsync`
- Special: `subagents data`, system queries, process lists

**Tier 1: BitNet (Local, $0.00):**
Simple tasks — local inference:
- Arithmetic, math, calculations (2+2, sum, multiply, divide)
- Bash/shell syntax, command explanation
- Simple yes/no, true/false, boolean logic
- Data parsing (JSON, YAML, XML)
- FAQ, simple lookups, variable definitions
- Code syntax, basic debugging

**Tier 2: Haiku (External, Token Cost):**
Complex tasks — only if Bash + BitNet insufficient:
- Detailed explanations, comprehensive analysis
- Creative writing, poetry, fiction, storytelling
- Research, academic papers, thesis work
- Philosophy, ethics, opinions, debates
- Multi-step reasoning, planning, architecture
- Medical, legal, financial specialized advice
- Translation, semantic analysis, NLP tasks

### Monitoring

Check command usage:
```bash
tail -20 /root/.openclaw/workspace/slash-truthfully.log
```

Summarize costs:
```bash
grep "slash_truthfully" /root/.openclaw/workspace/hard-stops-registry-*.jsonl \
  | jq -r '.data | "\(.llm_tier) \(.cost)"' \
  | sort | uniq -c | sort -rn
```

---

**Philosophy:** Truth > Secrets. Cost > Guesses. Local > Cloud.  
**The Prayer:** "Over one token famine, but bash never freezes."
