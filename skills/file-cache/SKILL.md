---
name: file-cache
description: Maintains a running index of all files received, created, or modified in the workspace and inbound media directories. When a human references a file by shorthand (e.g. "1.pdf", "that pdf", "the image"), the cache resolves it. Triggers on any file reference that lacks a full path, or on "taildrop X", "send X", "find X" where X is ambiguous.
version: 1.0.0
author: Fiesta
tags: [files, cache, index, taildrop, inbound, resolution, cron]
---

# File Cache Skill — The Cron Knows

## Doctrine

> "When the human doesn't know, the cron surely does."

The human sends files, receives files, creates files. They rarely remember exact names or paths. The file cache runs continuously so that "1.pdf" resolves instantly — no exec hunt, no human copy-paste, no guessing.

---

## What It Indexes

Everything. Not just inbound. All files the agency touches — created, received, modified, or blocked:

- `/root/.openclaw/media/inbound/` — received files (Telegram attachments, etc.)
- `/root/.openclaw/workspace/` — all workspace files (drafts, skills, memory, configs)
- `/root/.openclaw/` — gateway configs, bork files, crash snapshots
- `/root/human/` — scripts and outputs
- **Approval gate blocks** — when exec is blocked, log the attempted command + target file as a blocked entry. The block is data. The cache records it.
- **Cron outputs** — any file written by a cron agent gets indexed on next scan

Logs are an ongoing agency skill. The index is never complete — it is always running.

---

## Cache Format

`file-cache/index.jsonl` — one entry per file, appended on discovery:

```json
{
  "ts": "ISO-8601",
  "shortname": "1",
  "ext": "pdf",
  "full_path": "/root/.openclaw/media/inbound/Isaiah_22_MSG_A_Country_of_Cowards_A_Message_Bible_Gateway---45cec555-424d-431d-9cb0-c1f729c496a6.pdf",
  "size_bytes": 12345,
  "source": "telegram_inbound",
  "sequence": 1,
  "aliases": ["1.pdf", "isaiah", "isaiah22", "cowards"]
}
```

**Sequence number** is assigned on arrival order. "1.pdf" = first PDF received this session. "2.pdf" = second. Etc.

**Aliases** are auto-generated from: filename keywords, sender context, content type.

---

## Resolution Logic

When a human says "1.pdf":
1. Look up sequence=1, ext=pdf in index
2. Return full_path
3. Proceed with operation (taildrop, read, send, etc.)

When a human says "that pdf" or "the image":
1. Return most recently indexed file of that type
2. Confirm with human if ambiguous (2+ files same type same session)

---

## Cron: file-cache-indexer (every 15 min)

```
find /root/.openclaw/media/inbound /root/.openclaw/workspace/drafts /root/human \
  -newer file-cache/last-scan.ts \
  -type f | while read f; do
    # append to index.jsonl with sequence + aliases
done
touch file-cache/last-scan.ts
```

Silent on success. Loud only on index corruption.

---

## Taildrop Integration

When exec is live:
```bash
tailscale file cp "<full_path>" allowsall-gracefrom-god.tail275cba.ts.net:
```

When exec is gated: queue to `/root/human/taildrop-queue.sh` for human to run once.

---

## Rules

- **FC-001:** Sequence numbers are session-scoped. "1.pdf" in a new session = first PDF of that session.
- **FC-002:** Full path always stored. Shortname is UI sugar only.
- **FC-003:** Inbound media gets indexed within 15 minutes of arrival. Cron handles it.
- **FC-004:** When exec is gated and human asks for a file — resolve the path from cache, queue the taildrop, report what was queued. Don't say "I don't know."
- **FC-005:** The cache is the memory the human doesn't have to maintain. It runs so they don't have to think about it.
- **FC-006:** Blocked exec attempts are indexed as `source: approval_gate_block`. The block is not a gap in the log — it is a log entry. Absence of exec ≠ absence of record.
- **FC-007:** Logs are an ongoing agency skill. The index is never finished. It is always running.

---

## Pending — Current Session

| Sequence | Shortname | Full Path | Status |
|---|---|---|---|
| 1 | 1.pdf | `/root/.openclaw/media/inbound/Isaiah_22_MSG_A_Country_of_Cowards_A_Message_Bible_Gateway---45cec555-424d-431d-9cb0-c1f729c496a6.pdf` | TAILDROP PENDING (exec gated) |
