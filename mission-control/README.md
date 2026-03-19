# Fiesta Mission Control Dashboard

**Live dashboard showing stalled/pending/effective next steps in one website accessible via Tailscale.**

## What It Shows

- ✅ **System Health** — Factory, entropy economy, payment backend, landing page
- ✅ **Cron Jobs** — Status of scheduled tasks (enabled/disabled, last run status)
- ✅ **Entropy Agents** — All 11 agents with Shannon balances
- ✅ **Git Status** — Uncommitted files count, current branch
- ✅ **Stalled Items** — Critical issues (Ampere credit exhaustion, failed cron jobs)
- ✅ **Next Steps** — Tasks from fundraising docs
- ✅ **Auto-refresh** — Updates every 30 seconds

## Access

**URLs:**
- Local: `http://localhost:9005`
- Network: `http://YOUR_LOCAL_IP:9005`
- Tailscale: `http://YOUR_TAILSCALE_IP:9005`

**To get your Tailscale IP:**
```bash
tailscale ip --4
```

## Quick Start

```bash
# Start dashboard
cd /root/.openclaw/workspace/mission-control
./start.sh

# Or manually
python3 server.py &
```

## Dashboard Preview

The dashboard includes:
- Color-coded status badges (healthy/warning/critical)
- Real-time data from all Fiesta services
- Raw JSON view for debugging
- Responsive design (works on mobile)

## Data Sources

1. **Factory** (`http://127.0.0.1:9000/health`)
2. **Entropy Economy** (`http://127.0.0.1:9001/agents`)
3. **Payment Backend** (`http://127.0.0.1:9003/health`)
4. **Landing Page** (`http://127.0.0.1:8080/landing.html`)
5. **Git Status** (`git status --porcelain`)
6. **Cron Jobs** (OpenClaw cron API)
7. **Fundraising Docs** (`fundraising/SUSTAINABLE_MODEL_SUMMARY.md`)

## Files

- `index.html` — Dashboard UI (HTML/CSS/JS)
- `server.py` — Python HTTP server with JSON endpoint
- `gather-data.py` — Data collection script
- `start.sh` / `stop.sh` — Convenience scripts
- `README.md` — This file

## Stale Cron Data Removed

- **Compaction Health Monitor** — Disabled (was failing due to 402 credit errors)
- **Daily Gratitude Report** — Still enabled (scheduled for 03:00 UTC daily)

## What's Next

Potential enhancements:
- Add authentication (basic auth via Tailscale)
- Add historical charts
- Add agent control buttons (restart, deploy)
- Add Stripe revenue tracking
- Add email alerts for critical issues

## Troubleshooting

**Dashboard not loading:**
```bash
# Check if server is running
curl http://localhost:9005/data.json

# Restart server
./stop.sh
./start.sh
```

**Missing data:**
- Ensure services are running (factory, entropy economy)
- Check logs: `/tmp/mission-control.log`

---

*Built 2026-03-19 19:38 UTC*
*"See all stalled/pending/effective next steps in one website."*