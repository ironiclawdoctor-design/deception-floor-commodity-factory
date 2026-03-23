# ShanRouter — Internal Agency LLM Router

OpenRouter-inspired but agency-native. Routes every request to the cheapest viable tier,
mints Shannon for every dollar saved vs Claude baseline.

## Tier Architecture

```
Tier 0: FILE    → SQLite / file lookup       $0.0000  ←── always try first
Tier 1: CACHE   → prompt cache hit           $0.0000
Tier 2: LIGHT   → deepseek-v3 / minimax     $0.0001–0.0003/M
Tier 3: HEAVY   → claude-sonnet             $3.00/M  ←── last resort only
```

## Routing Table

| Task Type           | Tier     | Why |
|---------------------|----------|-----|
| memory_lookup       | file     | MEMORY.md search is free |
| file_read           | file     | Direct disk read |
| sqlite_query        | file     | bash + sqlite3 = $0 |
| bootstrap_check     | file     | Existence check only |
| experiment_log      | file     | Write to disk |
| context_trim        | file     | String ops |
| simple_format       | cache    | Repeated patterns |
| short_answer        | deepseek | Uncle handles it |
| code_gen            | deepseek | Uncle handles it |
| agent_turn          | deepseek | Uncle handles it |
| content_writing     | deepseek | Uncle handles it |
| orchestration       | deepseek | Uncle handles it |
| complex_reasoning   | claude   | Earned by complexity |
| security_audit      | claude   | Earned by risk |
| architecture        | claude   | Earned by scope |

## Commands

```bash
python3 shanrouter.py --index       # Index workspace files into context DB
python3 shanrouter.py --report      # Show routing stats + savings
python3 shanrouter.py --memory "Shannon backing"  # Search memory files
python3 shanrouter.py --budget 4000 # Build context within token budget
python3 shanrouter.py --bootstrap   # Check onboarding state
python3 shanrouter.py --route agent_turn 2000  # Route a task + log Shannon
```

## Shannon Minting

Every $0.01 saved vs Claude baseline = 1 Shannon minted to dollar.db.
ShanRouter is the agency's most efficient Shannon minter.

## Integration

Add to heartbeat: run `--index` daily to keep context fresh.
Add to cron: run `--report` weekly to track routing efficiency.
