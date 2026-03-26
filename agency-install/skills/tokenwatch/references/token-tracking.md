# Token Tracking Methodology

## Data Sources

### 1. OpenClaw Gateway Logs
- Path: `/var/log/openclaw/gateway.log` (if accessible)
- Pattern: `"tokens"` JSON fields in request/response logs
- Capture: input_tokens, output_tokens, cache_tokens, model_id, provider, session_key

### 2. Model Provider APIs (OpenRouter, Anthropic, etc.)
- OpenRouter response headers: `x‑openrouter‑tokens‑used`
- Anthropic response: `usage.input_tokens`, `usage.output_tokens`
- Fallback: estimate using `tiktoken` (cl100k_base) for known models

### 3. Agent Session Metadata
- Each sub‑agent spawned includes `agent_id`, `project_tag`
- Parent session can inject token‑tracking hooks before yielding

## Token Counting Rules

### Input Tokens
- System prompt + user message + context window contents
- Include images (vision models): flat multiplier per image (configurable)
- Include tool calls: serialized JSON counted as text

### Output Tokens
- Assistant response text
- Tool call JSON responses
- Any reasoning tokens (if reasoning model)

### Cache Tokens
- **Cache read**: tokens retrieved from KV cache (free or reduced cost)
- **Cache write**: tokens stored into KV cache (one‑time cost)
- Not all providers expose these; estimate as 0 if unknown

## Cost Estimation

### Provider‑Specific Pricing
| Provider | Model | Input ($/1M) | Output ($/1M) | Cache Read ($/1M) | Cache Write ($/1M) |
|----------|-------|--------------|---------------|-------------------|-------------------|
| OpenRouter | anthropic/claude‑sonnet‑4.6 | 3.00 | 15.00 | 0.00 | 0.00 |
| OpenRouter | deepseek/deepseek‑v3.2 | 0.10 | 0.10 | 0.00 | 0.00 |
| Anthropic direct | claude‑3‑opus‑20240229 | 15.00 | 75.00 | 0.30 | 1.50 |
| **Default** | *unknown* | 5.00 | 25.00 | 0.00 | 0.00 |

### Shannon Conversion
1. Query `dollar.db` `exchange_rates` table for latest `usd_to_shannon` rate.
2. `shannon_minted = round(estimated_usd_cost * usd_to_shannon)`
3. Insert into `token_ledger` with `memo: "token spend for <agent_id> on <model>"`

## Real‑Time Aggregation

**Streaming aggregation** via SQLite `INSERT` triggers:
- On each token event, update `tokenwatch_usage` and `tokenwatch_budgets.current_*`
- Trigger `tokenwatch_alerts` if thresholds crossed
- Update `dollar.db` `token_ledger` once per minute (batch)

**Rollups:**
- Hourly: aggregate by agent, model
- Daily: roll up into `tokenwatch_daily` table
- Weekly/Monthly: materialized views for reporting

## Missing Data Handling

### Scenario 1: No token counts in logs
- Estimate using `tiktoken` for known model families
- Log warning with confidence score (0‑100%)
- Flag row as `estimated: 1`

### Scenario 2: Provider price unknown
- Use default pricing (5¢/1K input, 25¢/1K output)
- Alert to CFO to update price table

### Scenario 3: Network outage (no dollar.db access)
- Buffer token events in local SQLite `tokenwatch_buffer`
- Retry every 5 minutes, up to 24h
- After 24h, write to `tokenwatch_failed` for manual reconciliation

## Accuracy Targets

- **≥95%** token count accuracy (vs provider billing)
- **≥99%** Shannon minting accuracy (vs actual spend)
- **<5 min** latency from token use to ledger entry
- **Zero** unaccounted spend after 7‑day reconciliation window