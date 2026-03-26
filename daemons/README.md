# LLM-Style Daemons

Two Python daemons for agency oversight and security monitoring.

## Daemons

### 1. raise-awareness
**Purpose:** Monitors system events and logs security anomalies.
**Features:**
- Checks core service health (Factory, Entropy, Gateway)
- Monitors file integrity in configured paths
- Verifies mutation detector is running
- Tracks token burn rate
- Mints entropy for security events
- Logs anomalies to `logs/anomalies.log`

**Configuration:** `raise-awareness-config.json`
```json
{
  "monitor_paths": [
    "/root/.openclaw/workspace/memory",
    "/root/.openclaw/workspace/logs",
    "/root/.openclaw/workspace/scripts"
  ],
  "alert_on_new_files": true,
  "alert_on_file_changes": true,
  "entropy_mint_threshold": 5,
  "anomaly_count": 0
}
```

### 2. proactive-supervisor
**Purpose:** Oversees agent operations and suggests improvements.
**Features:**
- Monitors cron jobs (count, failures)
- Checks agent/service health via `agency-auth.sh`
- Analyzes token burn patterns against $5/day threshold
- Monitors disk and memory usage
- Checks entropy economy health
- Generates improvement suggestions
- Mints entropy for valuable suggestions
- Stores suggestions in `suggestions/improvements.json`

**Configuration:** `proactive-supervisor-config.json`
```json
{
  "monitor_cron": true,
  "monitor_agents": true,
  "monitor_token_burn": true,
  "suggestion_cooldown_hours": 24,
  "max_suggestions_per_day": 5,
  "suggestions_today": 0,
  "last_suggestion_date": null
}
```

## Installation

### Quick Install (as root)
```bash
cd /root/.openclaw/workspace/daemons
./setup.sh
```

### Manual Installation
1. Ensure Python3 and requests module are installed
2. Copy service files to `/etc/systemd/system/`
3. Enable and start services:
```bash
sudo cp *.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable --now raise-awareness.service
sudo systemctl enable --now proactive-supervisor.service
```

## Logs
- `logs/raise-awareness.log`
- `logs/proactive-supervisor.log`
- `logs/anomalies.log` (security anomalies)
- `suggestions/improvements.json` (improvement suggestions)

## Integration

### Entropy Economy
Both daemons mint entropy for significant events:
- `raise-awareness`: Mints when anomaly threshold reached
- `proactive-supervisor`: Mints for high/medium priority suggestions

### Agency Auth
Uses `agency-auth.sh` for service health checks.

### Token Budget
Respects `$5/day` hard ceiling; alerts when exceeded.

## Systemd Services

### raise-awareness.service
- Restarts on failure (10s delay)
- Runs as root (monitors system)
- Protected with security flags

### proactive-supervisor.service
- Restarts on failure (30s delay)
- Runs as root (needs system access)
- Protected with security flags

## Status Checks
```bash
systemctl status raise-awareness
systemctl status proactive-supervisor
journalctl -u raise-awareness -f
journalctl -u proactive-supervisor -f
```

## Development

### Testing
```bash
cd /root/.openclaw/workspace/daemons
python3 raise-awareness.py  # Run in foreground
python3 proactive-supervisor.py  # Run in foreground
```

### Modifying
Edit Python files directly. Configuration files are auto-created with defaults.

## Requirements
- Python 3.6+
- `requests` module (auto-installed by setup)
- Systemd (for service management)
- Entropy economy running (port 9001)
- Factory running (port 9000)

## License
Part of OpenClaw agency infrastructure. Use freely.