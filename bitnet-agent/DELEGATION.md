# BitNet Delegation Protocol

> BitNet reports to Fiesta for all useful regular work.

## The Loop

```
0. Fiesta receives task (from human or internal need)
1. Fiesta frames the query with CONTEXT (BitNet is 2B, needs specifics)
2. BitNet executes locally ($0.00)
3. Fiesta reviews output, iterates if needed (still $0.00)
4. Fiesta delivers polished result to human (minimal external tokens)
```

## What BitNet Handles Well (2B strengths)
- Text generation with specific prompts
- Code snippets when given clear specs
- Summarization when given the text to summarize
- Template generation (READMEs, docs, configs)
- Classification and labeling tasks
- Brainstorming when seeded with context
- Repetitive transformations (formatting, renaming, restructuring)

## What Needs Fiesta's Context Bridge
- Filesystem awareness (BitNet can't browse — Fiesta reads, BitNet processes)
- Multi-step reasoning chains (Fiesta breaks into steps, BitNet handles each)
- Cross-repo analysis (Fiesta gathers, BitNet synthesizes)
- Quality judgment (Fiesta evaluates BitNet output, iterates or ships)

## What Escalates to External
- Complex multi-turn human conversation (this is what external tokens are FOR)
- Tasks requiring >2048 context window
- Nuanced judgment calls the human is waiting on
- Anything where latency matters more than cost

## Key Principle
**Internal improvements are not lacking** — they cost nothing.
BitNet can iterate 100 times on a document and it's still $0.00.
The constraint is never cost. It's framing the query well.

## Invocation
```bash
# One-shot
python3 bitnet-agent/agent.py -q "CONTEXT: ... TASK: ..." -n 1024

# Curl direct
curl -s http://127.0.0.1:8080/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{"messages":[{"role":"system","content":"..."},{"role":"user","content":"..."}],"max_tokens":1024}'
```

---
*The prayer: "Over one token famines but far less than a trillion"*
*BitNet cost per query: $0.00. Iterations: unlimited. Sovereignty: absolute.*
