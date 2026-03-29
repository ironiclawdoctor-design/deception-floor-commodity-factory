# Autoresearch Configuration: Dashboard Replication Cost — Free Stack Optimization

## Goal
Find the minimum viable stack to replicate the Dollar Dashboard at $0.00 cost, past 93% feature parity, without conceited over-engineering.

## Metric
- **Name**: feature_parity_score (0–100)
- **Direction**: Higher is better (target >93, ceiling ~96 — conceit starts at 97+)
- **Extract command**: python3 score-dashboard.py → reads score from stdout
- **Constraint**: cost must remain $0.00/month above the $39 floor

## Target Files
- `dashboard-replica/index.html` — Replication of dashboard.html
- `dashboard-replica/serve.py` — Serving layer
- `score-dashboard.py` — Scoring script (features present vs original)

## Read-Only Files
- `dashboard.html` — Original (reference only, do not modify)
- `dollar.db` — Production database (read only for schema)

## Run Command
```
python3 score-dashboard.py
```

## Time Budget
- **Per experiment**: 30 seconds
- **Kill timeout**: 60 seconds

## Constraints
- $0.00 cost above $39 floor (no new paid services)
- No GCP required (must work on Ampere.sh container)
- Feature parity target: >93%, ceiling 96% (not 100% — 100% is the original)
- Free models only for any LLM calls
- Must serve live data from dollar.db
- Must complete deploy in <5 minutes

## Branch
autoresearch/dashboard-replica-2026-03-29

## Notes
- Original: 481 lines HTML, Cloud Run hosted, dollar.db backend
- Hypothesis: same dashboard can run on Ampere.sh container directly, no GCP needed
- "Not too conceited" = stop at 96%, document why 97%+ is waste
- Conceit threshold: adding features the CFO didn't ask for
