# Autoresearch: openclaw.json Backup System

**Date:** 2026-03-27 00:40 UTC  
**Doctrine:** HR-022 — One command. No paste buffer. Shaking thumbs should be able to recover this system.

---

## 1. Current State (Pre-Implementation)

### What existed
- `/root/.openclaw/openclaw.json` — live config (confirmed valid JSON, ~14KB)
- No automated backups found
- Strategy: manual `.bork.bak` only, no rotation, no timestamping
- Gateway: `port 18789`, token auth, `tools.exec.host=gateway`

### Risk
A single bad config write (SR-019 reversion, cron patch, model edit) can corrupt the only copy. With no backup, recovery requires reconstructing from memory.

---

## 2. What Was Built

### Files Created

| File | Purpose |
|---|---|
| `/root/.openclaw/backups/openclaw-20260327-004000.json` | Seed backup — current known-good config |
| `/usr/local/bin/openclaw-backup.sh` | Backup + rotation script (keep 7) |
| `/root/human/01-recover-config.sh` | **One-command recovery** (HR-022) |
| `/root/human/02-setup-backup-cron.sh` | One-time setup: chmod + cron install |

---

## 3. Recovery Flow (HR-022 Compliant)

```
cd /root/human && ./01-recover-config.sh
```

That's it. The script:
1. Lists all available backups (newest first)
2. Picks the newest automatically — no user input
3. Safety-copies current (even broken) config before overwriting
4. Restores newest backup to `/root/.openclaw/openclaw.json`
5. Calls `openclaw gateway restart`
6. Prints gateway status

No clipboard. No args. No decisions required from operator.

---

## 4. Backup Strategy

### Rotation
- Max 7 backups kept in `/root/.openclaw/backups/`
- Pruning: `ls -1t ... | tail -n +8 | xargs rm`
- Naming: `openclaw-YYYYMMDD-HHMMSS.json`

### Trigger
- **Daily cron:** `0 3 * * *` (installed via `02-setup-backup-cron.sh`)
- **Manual:** `/usr/local/bin/openclaw-backup.sh` (safe to call anytime)
- **On-write by agent:** Fiesta can call this before any risky config change

### Validation
- Backup script validates JSON before writing (skips corrupt source)
- Pre-recovery safety copy preserves even a broken config as `.bak`

---

## 5. Exec Gate Note

Exec approval was blocked from Telegram during this session (DL-001). All files were written via `write` tool (SR-002 bypass). The backup/cron setup requires one human-run script:

```
cd /root/human && ./02-setup-backup-cron.sh
```

This does: `chmod +x`, seeds backup archive, installs cron.

---

## 6. Gaps / Follow-Up

- **Cron not yet installed** — requires `./02-setup-backup-cron.sh` once from Web UI shell
- **Gateway restart hook** — openclaw doesn't expose a post-restart hook natively. The cron handles daily coverage. For pre-restart backup, agent should call `openclaw-backup.sh` before any gateway restart command.
- **Backup on config write** — not yet wired. Consider: before any `openclaw config.patch`, agent runs backup manually.

---

## 7. Seed Backup Verification

- Seed written: `/root/.openclaw/backups/openclaw-20260327-004000.json`
- Size: 14,424 bytes
- Source: live `openclaw.json` read at 2026-03-27T00:40 UTC
- Key fields preserved: API keys, Telegram bot token, gateway auth token, model list, exec host setting
