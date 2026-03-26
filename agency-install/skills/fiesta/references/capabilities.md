# Fiesta Capabilities Reference

## Tool Inventory

| Tool | What Fiesta uses it for |
|------|------------------------|
| `exec` | Shell commands, script execution, service checks |
| `read/write/edit` | File operations on workspace |
| `web_search` | Research, news, documentation lookup |
| `web_fetch` | Fetch specific URLs, parse content |
| `browser` | Automated browser control (Camoufox on port 9222) |
| `cron` | Schedule jobs, set reminders, recurring tasks |
| `message` | Send to Telegram/Discord/Signal channels |
| `nodes` | Control paired mobile devices |
| `canvas` | Present HTML dashboards or UIs |
| `sessions_spawn` | Spawn sub-agents (subagent or ACP/Codex) |
| `sessions_send` | Send messages to other sessions |
| `subagents` | List, steer, or kill spawned agents |
| `gateway` | Restart gateway, apply config, run updates |
| `memory_search` / `memory_get` | Long-term memory retrieval |
| `image` / `pdf` | Vision and document analysis |
| `tts` | Text-to-speech output |

## Orchestration Patterns

### Spawn a sub-agent for a task
```
sessions_spawn(task="...", runtime="subagent", mode="run")
```

### Spawn a persistent Codex session (ACP)
```
sessions_spawn(task="...", runtime="acp", mode="session", thread=true)
```

### Steer a running sub-agent
```
subagents(action="steer", target="<session-id>", message="...")
```

### Kill a stuck sub-agent
```
subagents(action="kill", target="<session-id>")
```

## Memory Patterns

### Search long-term memory
```
memory_search(query="<topic>")
```

### Get specific memory lines
```
memory_get(path="MEMORY.md", from=<line>, lines=<n>)
```

### Write daily note
```
write(path="memory/YYYY-MM-DD.md", content="...")
```

## Shannon Economy Integration

- Mint Shannon: `POST http://localhost:9001/mint/security`
- Body: `{ "agent": "fiesta", "amount": <n>, "description": "<reason>" }`
- Check balance: query `agency.db` → `SELECT balance FROM wallets WHERE agent='fiesta'`

## Agency Infrastructure

| Service | Location | Port |
|---------|----------|------|
| Gateway | localhost | 18789 |
| Entropy economy | localhost | 9001 |
| Factory | localhost | 9000 |
| Agency DB | /root/.openclaw/workspace/agency.db | — |
| Dollar ledger | /root/.openclaw/workspace/dollar.db | — |
