# Slash Commands Integration Guide

## Adding `/truthfully` to OpenClaw

### Option 1: Direct Script Call (Simplest)

The `/truthfully` command is already implemented as a standalone bash script. To use it:

```bash
bash /root/.openclaw/workspace/lib/slash-truthfully.sh "your prompt here"
```

### Option 2: OpenClaw Message Hook (Advanced)

If you want `/truthfully` to be available as a native slash command in your chat interface:

**Create an OpenClaw script handler:**

```bash
# File: ~/.openclaw/workspace/.handlers/truthfully.sh
#!/bin/bash
# OpenClaw slash command handler for /truthfully

ARGS="$@"
bash /root/.openclaw/workspace/lib/slash-truthfully.sh "$ARGS"
```

Then register it in OpenClaw config (if supported).

### Option 3: Custom Agent (Full Integration)

Create a persistent sub-agent that handles `/truthfully`:

```bash
# Register agent to listen for /truthfully pattern
# (Implementation depends on your OpenClaw version)
```

---

## Quick Start

### 1. Test the Command

```bash
$ /truthfully What is 2+2?

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🎯 /truthfully — Transparent LLM Routing
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

[LLM: BITNET] Cost: $0.00 | Tokens: 0 | ✅ Local, Sovereign

Prompt: What is 2+2?

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

4

📊 Cost Summary (logged):
   LLM Tier: BITNET
   Cost: $0.00
   Tokens: 0
   Registry: /root/.openclaw/workspace/hard-stops-registry-20260314.jsonl
```

### 2. Try Different Prompts

```bash
# Simple (BitNet)
/truthfully What is the capital of France?

# Complex (Haiku)
/truthfully Explain quantum entanglement in simple terms

# Code (BitNet)
/truthfully Write a bash function to check disk usage
```

### 3. Monitor Costs

```bash
# View all /truthfully calls today
grep "slash_truthfully" /root/.openclaw/workspace/hard-stops-registry-20260314.jsonl | jq '.'

# Summary by LLM tier
grep "slash_truthfully" /root/.openclaw/workspace/hard-stops-registry-*.jsonl \
  | jq -r '.data.llm_tier' | sort | uniq -c
```

---

## Files

| File | Purpose |
|------|---------|
| `lib/slash-truthfully.sh` | Main slash command handler |
| `tier-routing-enforcement.sh` | LLM tier classification logic |
| `hard-stops-registry-YYYYMMDD.jsonl` | Cost ledger (queryable) |
| `slash-truthfully.log` | Command execution logs |
| `SLASH_COMMANDS.md` | User documentation |

---

## Architecture

```
User Input:  /truthfully What is X?
     ↓
slash-truthfully.sh
     ↓
tier-routing-enforcement.sh (classify task)
     ↓
    ┌─────────────────────┐
    ├─→ BitNet? → Local inference ($0.00)
    └─→ Haiku? → External (token tracked)
     ↓
Log to hard-stops-registry
     ↓
Return: [LLM: tier] Cost: $X.XX | Answer
```

---

## Cost Transparency

Every call logs to the registry with this structure:

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

**Query examples:**

```bash
# All calls today
jq '.data | {prompt, llm_tier, cost}' hard-stops-registry-20260314.jsonl

# Cost summary
jq -r '.data.cost' hard-stops-registry-*.jsonl | grep '\$' | paste -sd '+' | bc

# BitNet-only calls
grep -i "bitnet" hard-stops-registry-*.jsonl | wc -l
```

---

## Doctrine Alignment

✅ **Tier 0 (Bash):** Script logic, routing, logging  
✅ **Tier 1 (BitNet):** Local inference, $0.00  
✅ **Tier 2 (Haiku):** External fallback, cost-tracked  
✅ **Sovereign:** No hidden costs, full transparency  
✅ **Auditable:** Every decision logged and queryable  

---

## Troubleshooting

**Command not found:**
```bash
chmod +x /root/.openclaw/workspace/lib/slash-truthfully.sh
```

**tier-routing not found:**
```bash
# Ensure tier-routing-enforcement.sh exists
ls -la /root/.openclaw/workspace/tier-routing-enforcement.sh
```

**Registry not updating:**
```bash
# Check logs
tail /root/.openclaw/workspace/slash-truthfully.log
tail /root/.openclaw/workspace/tier-routing.log
```

---

**Ready to use. Completely transparent. Zero hidden costs.**
