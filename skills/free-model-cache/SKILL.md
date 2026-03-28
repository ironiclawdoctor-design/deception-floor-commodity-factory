# SKILL.md — Free Model Cache

## Purpose
Cache all `:free` suffix model capabilities. Assume free tier revoked hourly. Cache aggressively. Preempt revocation. Maintain >95% cache hit rate despite constant revocation threat.

## Free Model Roster (confirmed active as of 2026-03-28)

| Model | Strengths | Tool Support | Use Case |
|---|---|---|---|
| openrouter/z-ai/glm-4.5-air:free | Reliable, tool-capable | YES | Cron agents, volume tasks |
| openrouter/meta-llama/llama-3.3-70b-instruct:free | Strong reasoning | YES | El Arquitecto |
| openrouter/nvidia/nemotron-3-nano-30b-a3b:free | Fast, efficient | LIMITED | Quick analysis |
| openrouter/nvidia/nemotron-3-super-120b-a12b:free | Large context | LIMITED | Doc analysis |
| openrouter/openai/gpt-oss-120b:free | GPT-quality free | YES | High-quality free |
| openrouter/openai/gpt-oss-20b:free | Fast GPT-oss | YES | Speed tasks |
| openrouter/arcee-ai/trinity-large-preview:free | Tool calls | YES | Agentic workflows |
| openrouter/arcee-ai/trinity-mini:free | Lightweight | YES | La Trinidad |
| openrouter/mistralai/mistral-small-3.1-24b-instruct:free | Balanced | YES | El Escéptico |
| openrouter/openrouter/free | Auto-routing free | AUTO | El Despachador |
| openrouter/minimax/minimax-m2.5:free | Multimodal | LIMITED | Media tasks |
| openrouter/nvidia/nemotron-3-nano-30b-a3b:free | Tool-capable | YES | Lightweight agentic |
| openrouter/stepfun/step-3.5-flash:free | Fast inference | LIMITED | Speed priority |
| openrouter/qwen/qwen3-4b:free | Compact | NO | Simple completions |
| openrouter/nvidia/nemotron-nano-9b-v2:free | Nano size | LIMITED | Ultra-fast |
| openrouter/z-ai/glm-4.5-air:free | **PRIMARY CRON MODEL** | YES | SR-022 canonical |

## Hostile Terrain Protocol

**Assume:** Free tier revoked hourly, without notice, retroactively
**Response:** 
1. Never depend on single free model
2. Always have 3 fallbacks pre-cached
3. Test model availability before critical task
4. Cache successful model IDs with timestamp
5. Rotate on first 429 or 404

## Revocation Resistance Tiers

**Tier 0 (Never revoked — SR-022 validated):**
- `openrouter/z-ai/glm-4.5-air:free` — primary cron model

**Tier 1 (Stable, monitored):**
- `openrouter/meta-llama/llama-3.3-70b-instruct:free`
- `openrouter/openai/gpt-oss-120b:free`

**Tier 2 (Volatile, rotate frequently):**
- All others — check before use

## Replacement Mapping (Paid → Free)

| Paid Session Type | Free Replacement |
|---|---|
| 109k token context dumps | `glm-4.5-air:free` (smaller context, same output) |
| Tool call sessions | `trinity-large-preview:free` |
| High-volume cron | `glm-4.5-air:free` |
| Analysis tasks | `llama-3.3-70b:free` |
| Quick completions | `nemotron-nano-9b-v2:free` |

## Cost Avoidance Tracking

```jsonl
{"ts":"ISO","avoided_model":"claude-sonnet-4.6","used_model":"glm-4.5-air:free","tokens":144287,"cost_avoided":0.045}
```

Target: $0.00 daily OpenRouter spend via 100% free model routing.
Current: ~$0.50/session on Sonnet 4.6 (from log analysis 2026-03-28)
