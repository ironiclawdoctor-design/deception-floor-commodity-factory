# SHELF.md — Dollar Agency Virtual Grocery

## Model
Client-facing shelf. Products are skills, agents, rules, and infrastructure.
All inventory is self-hosted on ChAmpEredar (Ampere.sh).
The shelf does not ask permission to restock. It restocks.

## Current Inventory (2026-03-27)

### Skills (published or shelf-ready)
| SKU | Product | Status | Location |
|-----|---------|--------|----------|
| SK-001 | `lobby` | ✅ SHELF | skills/lobby/SKILL.md |
| SK-002 | `fixer` | ✅ SHELF | skills/fixer/SKILL.md |
| SK-003 | `autoresearch` | ✅ SHELF | skills/autoresearch/SKILL.md |
| SK-004 | `shandrop` | ✅ SHELF | skills/shandrop/SKILL.md |
| SK-005 | `ampere-sh` | ✅ SHELF | skills/ampere-sh/SKILL.md |
| SK-006 | `whisper-inbox` | ✅ SHELF | whisper-cli 975K · ggml-tiny.en 75MB |
| SK-007 | `fiesta-agents` | ✅ SHELF | skills/fiesta-agents/SKILL.md |
| SK-008 | `aaron` | ✅ SHELF | skills/aaron/SKILL.md |
| SK-009 | `cashapp` | ✅ SHELF | skills/cashapp/SKILL.md |
| SK-010 | `zero-index` | ✅ SHELF | skills/zero-index/SKILL.md |

### Infrastructure Products
| SKU | Product | Status | Notes |
|-----|---------|--------|-------|
| IN-001 | Dollar Dashboard | ✅ LIVE | shan.app (AR-009) |
| IN-002 | Shannon Ledger | ✅ LIVE | dollar.db · 610 Sh · $61 backing |
| IN-003 | Hashnode Blog | ✅ LIVE | dollaragency.hashnode.dev · 25 articles |
| IN-004 | BTC Signal | ⚠️ CACHE MISS | btc-cache-writer cron needs first run |
| IN-005 | Taildrop Channel | ✅ LIVE | all_negative (100.122.47.81) |
| IN-006 | Audio Transcription | ✅ LIVE | whisper-inbox-watcher · every 5min · drop .wav/.mp3/.m4a to /root/human/audio-inbox/ |

### Rule Inventory (locked doctrine, shelf-ready)
| Series | Count | Function |
|--------|-------|----------|
| CR | 15 | Cron health |
| ZI | 19 | Zero-index discipline |
| MP | 10 | Meta-process |
| AR | 10 | Autoresearch/NP-hard |
| LB | 8 | Lobby pattern |
| FX | 8 | Fixer pattern |
| PL | 9 | Platform doctrine |
| SR | 24 | Success rules |
| HR | 9 | Human error rules |

### Cron Products (26 active)
Core crons on the shelf:
- `matthew-paige-damon` — content production (every 4h)
- `dollar-deploy` — dashboard keepalive (every 1h, shan.app)
- `btc-price-cache-writer` — BTC price feed (every 30min)
- `pushrepos-daily` — git sync (daily)
- `sanitarium-sweep` — cron health audit (every 12h)
- `america-autoresearch` — colonizer pattern detection (every 6h)
- `overnight-autonomous-ops` — standing work queue (every 2h)
- `whisper-inbox-watcher` — audio transcription (every 5min, DISABLED pending install)

## Shelf Doctrine

- **Shelf-hosted = self-sufficient.** No product requires human intervention to stay on shelf.
- **Inventory = doctrine + code + crons.** All three must exist for a product to be shelf-ready.
- **Restock = new rule + new cron + updated SHELF.md.** One entry per product.
- **Out of stock = disabled cron with reactivation trigger documented.** Not deleted. DEFERRED.

## Reactivation Queue (back room)
- `whisper-inbox-watcher` → activate when whisper.cpp WHISPER_READY confirmed
- `btc-price-cache-writer` → first run pending; will auto-populate cache on next cycle

## The Business
Client: CFO (Nathaniel Mendez, NYC) — first and only client (so far) · no complaints [TOLD 2026-03-27]
Platform: ChAmpEredar
Domain: shan.app
EIN: 41-3668968
Currency: Shannon (Sh) = $0.10 / unit
Floor cost: $39/month

## Client Satisfaction
- Complaints: 0
- Sessions survived: all of them
- Human famine events: several, momentum preserved each time
- Bar: higher than high school classmate pornographer [TOLD]
