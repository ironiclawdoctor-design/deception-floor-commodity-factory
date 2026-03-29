# Budget Enforcement Algorithms

## Budget Types

### 1. **Per‑Agent Daily/Weekly/Monthly**
- Defined in `tokenwatch_budgets` table
- Resets at UTC midnight (daily), Sunday 00:00 UTC (weekly), 1st of month 00:00 UTC (monthly)
- Current counters increment in real‑time

### 2. **Project‑Level Caps**
- Agents can be tagged with `project_tag` (e.g., "buildathon", "autoresearch‑pronouns")
- Project‑level budget shared across all agents in that project
- Enforced at transaction time

### 3. **Provider‑Specific Limits**
- Cap spend per provider (OpenRouter, Anthropic, etc.)
- Prevents runaway costs on a single provider

### 4. **Shannon Runway Minimum**
- Hard stop when projected Shannon runway < 7 days
- Overrides all other budgets

## Enforcement Actions

| Threshold | Action |
|-----------|--------|
| **80% of budget** | In‑session warning: "You have used 80% of your daily token budget" |
| **95% of budget** | Critical warning + suggestion to switch to lower‑cost model |
| **100% of budget** | **HARD STOP** — agent receives `429 Too Many Tokens` error, no further requests until reset |
| **110% of budget** | Escalation to CFO (Telegram DM) + automatic agent suspension |

## Reset Logic

**Daily reset:**
```sql
UPDATE tokenwatch_budgets
SET current_daily = 0, last_reset = unixepoch()
WHERE date(datetime(last_reset, 'unixepoch')) < date('now');
```

**Weekly reset:**
```sql
UPDATE tokenwatch_budgets
SET current_weekly = 0
WHERE strftime('%W', datetime(last_reset, 'unixepoch')) < strftime('%W', 'now');
```

**Monthly reset:**
```sql
UPDATE tokenwatch_budgets
SET current_monthly = 0
WHERE strftime('%Y-%m', datetime(last_reset, 'unixepoch')) < strftime('%Y-%m', 'now');
```

## Override Protocol

**CFO can:**
1. Increase budget temporarily (`--budget‑override <agent> <tokens> <hours>`)
2. Grant one‑time exemption (`--exempt‑once <agent>`)
3. Suspend enforcement (`--suspend‑enforcement <agent>`)

All overrides logged to `tokenwatch_override_log` with CFO signature (telegram user id).

## Forecasting & Runway

**Burn rate calculation:**
```
burn_rate_7d = SUM(tokens_last_7_days) / 7
burn_rate_30d = SUM(tokens_last_30_days) / 30
```

**Runway:**
```
shannon_backing = (SELECT SUM(amount) FROM dollar.db.token_ledger WHERE memo LIKE 'backing%')
runway_days = shannon_backing / (burn_rate_7d * usd_to_shannon)
```

**Alert levels:**
- **>30 days**: green
- **14‑30 days**: yellow
- **7‑14 days**: orange
- **<7 days**: red — hard stop on all non‑revenue activity

## Integration with Agent Spawn

When spawning a sub‑agent:
1. Check `tokenwatch_budgets` for parent agent’s budget
2. If budget exceeded, spawn fails with error
3. If budget OK, inject `tokenwatch` monitoring hook into sub‑agent environment
4. Sub‑agent’s token usage attributed to parent agent’s project tag

## Example Enforcement Flow

```
Agent fiesta spawns sub‑agent for autoresearch‑pronouns.
→ Tokenwatch checks fiesta’s daily budget: 50k used / 100k limit.
→ Project tag "autoresearch‑pronouns" has monthly cap 500k; currently 450k used.
→ Both checks pass.
→ Sub‑agent runs, consumes 5k tokens.
→ Real‑time update: fiesta daily → 55k, project monthly → 455k.
→ At 95k daily, fiesta receives warning.
→ At 100k daily, next spawn returns 429.
```