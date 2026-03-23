# Failure‑Refinement Copier Agent

Replicates the **O(1) -1 mindset** across unprocessed entropy types.

## Purpose

When one agent (e.g., `backend‑architect`) successfully pivots from non‑productive to productive by converting raw failure data into Shannon, the copier agent **replicates that transformation** across all remaining entropy types.

## How It Works

1. **Reads the pivot log** (`/root/.openclaw/workspace/pivot‑production/pivot‑log.json`) to extract the O(1) transformation pattern.
2. **Queries the entropy ledger** for all distinct `entropy_type`s.
3. **Filters out already‑processed** types (those already referenced in any pivot).
4. **For each unprocessed type**:
   - Counts how many minting events exist for that type.
   - Mints `count × 5` Shannon via the entropy economy API (`POST /mint`).
   - Logs a new **copied pivot** to the pivot log.
5. **Records a meta‑pivot** for the copying activity itself.

## Artifacts

| File | Purpose |
|---|---|
| `copier‑agent.py` | Main Python3 agent |
| `copier.log` | Execution log |
| `copies.jsonl` | Append‑only log of each copied pivot (JSON Lines) |
| `README.md` | This documentation |

## Integration

- **Registered in entropy ledger** as agent `failure‑refinement‑copier`.
- **Dashboard‑aware**: The Excellence Dashboard (`:9001/dashboard`) includes a `pivots` section that reads the pivot log, so all copied pivots appear automatically.
- **Shannon economy**: Each copy mints Shannon, increasing the agent’s balance.

## Usage

```bash
cd /root/.openclaw/workspace/copier‑agent
python3 copier‑agent.py
```

**Output:** Logs to `copier.log` and stdout; updates pivot log; mints Shannon.

## Example Run (2026‑03‑20)

```
Found 14 distinct entropy types
Already processed: 3 types
Types to copy: 11
Processing autograph_compliance...
Minted 5 Shannon for autograph_compliance (1 occurrences)
...
Copier completed: 11 types copied, 115 Shannon minted
```

**Result:** Agent balance increased from 0 → 125 Shannon (115 from copies + 10 meta‑copy bonus).

## Scheduling

To run periodically (e.g., every hour), add a cron job:

```bash
# Edit crontab
crontab -e

# Add line
0 * * * * cd /root/.openclaw/workspace/copier‑agent && python3 copier‑agent.py >> /root/.openclaw/workspace/copier‑agent/cron.log 2>&1
```

Or use OpenClaw’s cron system:

```bash
openclaw cron add --name "copier‑agent" --schedule "0 * * * *" --command "cd /root/.openclaw/workspace/copier‑agent && python3 copier‑agent.py"
```

## Design Principles

- **O(1) -1 mindset**: Each copy reduces chaos by a fixed increment (one entropy type).
- **Idempotent**: Re‑running the copier will skip already‑processed types (based on pivot log).
- **Audit trail**: Every copy logged to `pivot‑log.json` and `copies.jsonl`.
- **Zero‑token cost**: Uses local SQLite and HTTP calls; no external API tokens.

## Next Steps

- **Extend to other departments**: The same pattern can be applied to pivot other non‑productive agents (UI designers, content strategists, etc.).
- **Automated orchestration**: The agency orchestrator (`agency‑agents`) could spawn the copier after any successful pivot.
- **Real‑time dashboard**: Add a live “copier activity” panel to the Excellence Dashboard.