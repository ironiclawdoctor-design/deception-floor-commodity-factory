# agency-email

Dollar Agency internal and external email system.

## Overview

Two-layer email system:
- **Internal:** Agent-to-agent SQLite messaging (`mail.py`) — persists across sessions
- **External:** Real SMTP delivery (`send_external.py`) — queues when unconfigured

All files live in `/root/.openclaw/workspace/internal-mail/`.

---

## Internal Mail (`mail.py`)

### Send a message
```bash
python3 /root/.openclaw/workspace/internal-mail/mail.py send \
  --from "Cannot" \
  --to "Grumpy" \
  --subject "Next article" \
  --body "Write the Houdini follow-up"
```

### Read an agent's inbox
```bash
python3 /root/.openclaw/workspace/internal-mail/mail.py inbox --agent "Grumpy"
```

Output:
```
[1] FROM: Cannot | SUBJECT: Next article | 2026-03-25 17:30 | UNREAD
```

### Open a message (marks it READ)
```bash
python3 /root/.openclaw/workspace/internal-mail/mail.py read --id 1
```

### Database
Messages stored in `/root/.openclaw/workspace/internal-mail/mail.db` (SQLite).

Schema:
```sql
CREATE TABLE messages (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  from_agent TEXT NOT NULL,
  to_agent TEXT NOT NULL,
  subject TEXT NOT NULL,
  body TEXT NOT NULL,
  sent_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  read INTEGER DEFAULT 0
);
```

Direct query example:
```bash
sqlite3 /root/.openclaw/workspace/internal-mail/mail.db \
  "SELECT * FROM messages WHERE to_agent='Grumpy' AND read=0;"
```

---

## External Email (`send_external.py`)

### Configure SMTP

Set these environment variables (or add to your `.env` / cron env):
```bash
export SMTP_HOST=smtp.gmail.com
export SMTP_PORT=587
export SMTP_USER=you@gmail.com
export SMTP_PASS=your-app-password
export SMTP_FROM=you@gmail.com   # optional, defaults to SMTP_USER
```

For Gmail: use an [App Password](https://myaccount.google.com/apppasswords), not your main password.

### Send external email
```bash
python3 /root/.openclaw/workspace/internal-mail/send_external.py \
  --to "editor@newspaper.com" \
  --subject "Article submission" \
  --body "Please find my article attached."
```

### When SMTP is not configured
Email is queued to `outbox-pending.jsonl`:
```
QUEUED: email to editor@newspaper.com pending SMTP config
```

Flush the queue manually once SMTP is configured:
```bash
# Read queue
cat /root/.openclaw/workspace/internal-mail/outbox-pending.jsonl

# Re-send each entry after setting SMTP env vars
```

---

## Agent Usage Patterns

### Task delegation (agent → agent)
```bash
python3 mail.py send --from "Dollar" --to "Cannot" \
  --subject "Research task" --body "Find top 3 BTC wallets by age"
```

### Check for new assignments
```bash
python3 mail.py inbox --agent "Cannot"
```

### Acknowledge and mark done
```bash
python3 mail.py read --id 5
```

### Notify human via external email
```bash
python3 send_external.py \
  --to "human@example.com" \
  --subject "Task complete" \
  --body "The Houdini article is ready for review."
```

---

## Files

| File | Purpose |
|------|---------|
| `mail.py` | Internal agent-to-agent mail CLI |
| `send_external.py` | External SMTP email with queue fallback |
| `mail.db` | SQLite message store (auto-created) |
| `outbox-pending.jsonl` | Queue for unsent external emails |
