# Autoresearch Token Optimization

## Goal
Reduce token spend per unit of outcome without degrading quality.

## Experiment Types

### 1. **Model Switching**
- **Hypothesis:** For Tier‑2 tasks (pattern matching, summarization), a cheaper model (deepseek‑v3.2) performs as well as Claude Sonnet.
- **Method:** A/B test: same task given to two models, compare outcome quality (eval score) vs token cost.
- **Metric:** `(quality_score / token_cost)`
- **Winner:** Model with highest quality‑per‑token.

### 2. **Cache‑Hit Improvement**
- **Hypothesis:** Increasing KV cache size reduces repeat token processing.
- **Method:** Adjust `max_cache_tokens` parameter, measure cache‑hit ratio over 24h.
- **Metric:** `cache_read_tokens / total_input_tokens`
- **Target:** ≥30% cache‑hit ratio.

### 3. **Batch Optimization**
- **Hypothesis:** Processing similar tasks in batches reduces per‑item overhead.
- **Method:** Queue similar requests (e.g., “summarize this paragraph”), batch every N items, measure tokens per item.
- **Metric:** `total_tokens / items_processed`
- **Optimal N:** Find elbow point where marginal reduction plateaus.

### 4. **Prompt Compression**
- **Hypothesis:** Shorter system prompts reduce input tokens without losing direction.
- **Method:** Generate compressed variants (via LLM summarization), test on eval suite.
- **Metric:** `(eval_score / prompt_tokens)`
- **Constraint:** No drop in eval score >5%.

## Autoresearch Loop

### Phase 1: Hypothesis Generation
- Scan `tokenwatch_usage` for high‑cost patterns (agent, model, task type).
- Propose 1‑3 experiments per week.
- Each hypothesis logged to `autoresearch‑tokenwatch/hypotheses/`.

### Phase 2: Experiment Design
- Define control (current) and treatment (optimized) groups.
- Random sampling of tasks from historical log.
- Pre‑compute power analysis: minimum N for statistical significance.

### Phase 3: Execution
- Run experiment in isolated sandbox (dedicated agent session).
- Record token counts, outcomes, quality scores.
- Abort if quality drops below threshold (‑10%).

### Phase 4: Analysis
- Compute effect size (Cohen’s d) and confidence intervals.
- If p < 0.05 and effect size > 0.2, declare winner.
- Log full results to `autoresearch‑tokenwatch/results/`.

### Phase 5: Deployment
- Winning configuration promoted to production via config patch.
- Monitor for regression over 7 days.
- If regression detected, roll back and investigate.

## Quality Measurement

### Tier‑Specific Eval Suites
- **Tier 0 (bash):** Correctness of command output
- **Tier 1 (pattern matching):** Accuracy of classification/extraction
- **Tier 2 (reasoning):** Logical consistency, step‑by‑step correctness
- **Tier 3 (creative):** Human‑rated appropriateness, fluency

### Automated Eval Agents
- Independent evaluator (different model) scores outcomes.
- Calibration against human gold‑standard set.
- Evaluator bias measured and corrected.

## Token‑Efficiency KPIs

| KPI | Formula | Target |
|-----|---------|--------|
| **Tokens per task** | `Σ tokens / tasks` | Reduce 10% per quarter |
| **Cache‑hit ratio** | `cache_read / total_input` | ≥30% |
| **Cost per outcome** | `Σ Shannon / tasks` | Reduce 15% per quarter |
| **Budget adherence** | `(actual / budget) × 100` | ≤100% |
| **Runway days** | `backing / daily_burn` | ≥14 days |

## Continuous Monitoring

- Weekly report: `tokenwatch_autoresearch_report.md`
- Alerts on regression: `tokenwatch_alerts` table
- CFO review every Monday 9am EST

## Integration with Agency Autoresearch

Tokenwatch autoresearch runs as a **sub‑skill** of the main `autoresearch` skill.
- Shares experiment registry (`agency.db.autoresearch_experiments`)
- Uses same eval‑suite framework
- Results contribute to agency‑wide learning (`agency.db.learnings`)

## Example Experiment Log

```json
{
  "id": "exp‑20260324‑001",
  "hypothesis": "Deepseek‑v3.2 can replace Claude‑Sonnet for pronoun‑skill evals",
  "control": {"model": "openrouter/anthropic/claude‑sonnet‑4.6"},
  "treatment": {"model": "openrouter/deepseek/deepseek‑v3.2"},
  "tasks": 50,
  "results": {
    "control_tokens": 125000,
    "control_quality": 92.5,
    "treatment_tokens": 31000,
    "treatment_quality": 91.8,
    "token_reduction": 75.2%,
    "quality_delta": ‑0.7%,
    "effect_size": 0.85,
    "p_value": 0.003
  },
  "decision": "ADOPT",
  "deployed_at": 1774300000
}
```