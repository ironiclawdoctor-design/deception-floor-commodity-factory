# Tier-Routing Enforcement — Quick Reference Card

## TL;DR

**What:** Route requests to BitNet (free) or Haiku (tracked) based on complexity  
**Where:** `/root/.openclaw/workspace/tier-routing-enforcement.sh`  
**Status:** ✅ Production Ready  
**Cost:** Prefer local BitNet → minimize external Haiku calls  

---

## Basic Usage

```bash
# Run the script
./tier-routing-enforcement.sh --task "DESCRIPTION" --prompt "YOUR_PROMPT"

# Output shows:
# Model: bitnet (free) or haiku ($cost)
# Cost: $0.0000 or $0.00081
# Response: [Model response here]
```

## Command Syntax

```bash
./tier-routing-enforcement.sh \
  --task "What is 2+2?"                 # Task description
  --prompt "Calculate: 2 + 2"           # The actual prompt
  [--model bitnet|haiku]                # Force model (optional)
  [--cost-estimate 0.00150]             # Override cost (optional)
```

## Examples

### Simple Math (BitNet)
```bash
./tier-routing-enforcement.sh \
  --task "What is 2+2?" \
  --prompt "Calculate: 2 + 2"
# → Routed to: bitnet, Cost: $0.0000
```

### Creative Writing (Haiku)
```bash
./tier-routing-enforcement.sh \
  --task "Write a short story" \
  --prompt "Write a story about a robot"
# → Routed to: haiku, Cost: $0.00081
```

### Force Model
```bash
./tier-routing-enforcement.sh \
  --task "What is 2+2?" \
  --prompt "2 + 2" \
  --model bitnet
# → Routed to: bitnet (forced), Cost: $0.0000
```

---

## Classification Rules

### 🟢 BitNet-Compatible (Free)
- Arithmetic, math, calculations
- Simple Q&A, greetings
- Bash scripting, shell commands
- Code syntax, debugging
- Data parsing (JSON, YAML, TOML)
- Boolean logic

### 🔴 Haiku-Required (Tracked Cost)
- Creative writing, stories, poetry
- Detailed explanations, analysis
- Research, academic work
- Specialized knowledge (medical, legal, financial)
- Complex multi-step reasoning
- Visual design, diagrams

### 🟡 Default
No match → **Haiku** (conservative fallback)

---

## Output Files

| File | Purpose |
|------|---------|
| `hard-stops-registry-YYYYMMDD.jsonl` | Cost ledger (queryable) |
| `tier-routing.log` | Execution logs |

## Query Results

```bash
# See today's decisions
cat hard-stops-registry-$(date +%Y%m%d).jsonl | jq '.'

# Total cost today
jq '.cost | tonumber' hard-stops-registry-*.jsonl | paste -sd+ | bc

# Count by model
jq -s 'group_by(.model) | map({model: .[0].model, count: length})' hard-stops-registry-*.jsonl
```

---

## Integration Code

```bash
# In your script:
OUTPUT=$(/root/.openclaw/workspace/tier-routing-enforcement.sh \
  --task "Your task" \
  --prompt "Your prompt")

MODEL=$(echo "$OUTPUT" | grep "Model:" | awk '{print $2}')
COST=$(echo "$OUTPUT" | grep "Cost:" | awk '{print $2}')
RESPONSE=$(echo "$OUTPUT" | tail -1)

echo "Routed to $MODEL (cost: $COST)"
echo "Response: $RESPONSE"
```

---

## Troubleshooting

| Problem | Solution |
|---------|----------|
| **Hangs during execution** | It has a 2s timeout; will fall back to Haiku |
| **Registry not created** | Check `/root/.openclaw/workspace/` is writable |
| **Task misclassified** | Use `--model` to override, or add pattern to script |
| **jq not found** | Install: `apt-get install jq` |
| **Permission denied** | Run: `chmod +x tier-routing-enforcement.sh` |

---

## Performance

| Operation | Time |
|-----------|------|
| Classification | ~5ms |
| Availability check | 0-2s |
| Total overhead | <2.1s |

---

## Cost Example

**100 daily tasks:**
- 80 → BitNet (free) = $0.00
- 20 → Haiku ($0.00081) = $0.0162

**Monthly: ~$0.49** (assuming 100 tasks/day)

---

## Key Features

✅ Intelligent classification  
✅ Cost tracking (JSONL)  
✅ Timeout protection  
✅ Graceful fallback  
✅ Zero dependencies (bash/curl/jq)  
✅ Production ready  

---

## Files

```
/root/.openclaw/workspace/
├── tier-routing-enforcement.sh           ← Main script
├── TIER-ROUTING-README.md                ← Full docs
├── tier-routing-integration-example.sh   ← How to integrate
├── test-tier-routing.sh                  ← Test harness
├── hard-stops-registry-YYYYMMDD.jsonl    ← Cost ledger
├── tier-routing.log                      ← Logs
├── QUICK-REFERENCE.md                    ← This file
└── DELIVERY-SUMMARY.md                   ← Full delivery summary
```

---

## Next Steps

1. Integrate into Official loop
2. Monitor cost daily
3. Adjust patterns if needed
4. Archive old registries monthly

---

**Version:** 1.0 | **Status:** Production Ready | **Last Updated:** 2026-03-14
