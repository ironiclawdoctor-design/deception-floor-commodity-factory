# Autoresearch Configuration — Agency Status Monitor

## Goal
Continuous autonomous status reporting across all agency systems. No human input required. Results delivered via Telegram announce.

## Metric
- **Name**: systems_healthy
- **Direction**: higher is better (0–10 scale, 10 = all green)
- **Extract command**: sqlite3 /root/.openclaw/workspace/agency.db "SELECT COUNT(*) FROM shanrouter_log WHERE ts > datetime('now','-1 hour');"

## Target Files
- /root/.openclaw/workspace/dollar/dollar.db (ledger health)
- /root/.openclaw/workspace/agency.db (routing + ultimatums)
- /root/human/last-run.log (deploy pipeline)
- /root/human/btc-status.json (wallet)
- /root/.openclaw/workspace/AUTONOMOUS.md (mission state)

## Read-Only Files
- /root/.openclaw/workspace/MEMORY.md (source of truth)
- /root/.openclaw/workspace/AGENTS.md (rules)

## Run Command
```
python3 /root/.openclaw/workspace/shanrouter/shanrouter.py --report
sqlite3 /root/.openclaw/workspace/dollar/dollar.db "SELECT '💰 $'||total_backing_usd||' → '||total_shannon_supply||' Shannon | Confessions: '||(SELECT COUNT(*) FROM confessions) FROM exchange_rates ORDER BY date DESC LIMIT 1;"
cat /root/human/btc-status.json 2>/dev/null | python3 -c "import sys,json; d=json.load(sys.stdin); print(f'₿ {d[\"balance_satoshi\"]} sat = \${d[\"balance_usd\"]:.2f}')" 2>/dev/null || echo "₿ btc-status.json not found"
tail -3 /root/human/last-run.log 2>/dev/null
```

## Time Budget
- **Per experiment**: 2 minutes
- **Kill timeout**: 5 minutes

## Constraints
- No subagent spawning in status checks
- SQLite queries only for data retrieval
- Bash tier for all reads
- Report must fit in 10 lines

## Branch
autoresearch/status-monitor

## Cron
Every 4 hours, isolated session, announce to Telegram on any WARN or FAIL.

## Notes
Stage 0 (doctor) only — the one verifiable knife.
Stage 1 (systems_healthy) deferred: IRL values (BTC, ledger, deploy log) are stale until
a live data source is confirmed. Scoring them is theater. Smaller half is mine.
