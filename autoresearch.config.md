# Autoresearch Configuration

## Goal
Optimize Hashnode article publishing throughput while maintaining quality (no duplicates, proper formatting, consistent voice).

## Metric
- **Name**: articles_per_hour
- **Direction**: higher is better
- **Extract command**: Calculate from timestamps in memory/*.md files; count unique articles published per hour of operation

## Target Files
- `skills/gh-issues/SKILL.md` (main publishing logic)
- `memory/2026-03-26.md` (logs article publication timestamps)
- Any cron job scripts in workspace root that trigger publishing

## Read-Only Files
- `MEMORY.md` (long-term memory, not to be modified)
- `AGENTS.md` (core rules, not to be modified)
- `USER.md` (human context, not to be modified)

## Run Command
```
# Simulate one publishing cycle (would need actual API call)
python3 -c "
import datetime
print('Simulated publishing at', datetime.datetime.utcnow().isoformat())
print('articles_per_hour: 3.0')  # baseline
"
```

## Time Budget
- **Per experiment**: 30 seconds
- **Kill timeout**: 60 seconds

## Constraints
- No modification to Hashnode API tokens or credentials
- No spammy behavior (respect rate limits)
- Article quality must not degrade (no duplicate content, proper formatting)
- Maintain the CFO voice and agency doctrine

## Branch
autoresearch/hashnode-throughput-20260326

## Notes
Current baseline: ~3 articles per overnight cron cycle (8 hours) = ~0.375 articles/hour
Target: Increase to >1 article/hour while maintaining quality.
Experiments may include: batch generation, parallelization, template optimization, scheduling tweaks.