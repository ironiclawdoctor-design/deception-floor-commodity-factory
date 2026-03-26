# SLASH COMMANDS - Telegram Integration

All slash commands are auto-registered from `/root/scripts/*.sh` and available in Telegram chat.

## Auto-Generated Commands (Index 0-36)

Run `/menu list` in Telegram to see all available commands, or:

```
/run N              Run script by index (e.g., /run 5)
/info N             Show script details by index
/list               Show all available scripts
```

## Script-Based Slash Commands

Each executable script in `/root/scripts/` is automatically:
1. **Discovered** (zero-indexed 0-N)
2. **Registered** to Telegram as `/<script-name>`
3. **Documented** with first comment line as description

### Example Commands

- `/menu` — Show interactive script menu
- `/tier-routing-enforcement` — Route queries by cost tier
- `/truthfully-status-cron` — Cost reporting with transparency
- `/bitnet-diagnostics` — Health check local LLM
- `/broadcast-status` — Send agency status to all branches
- `/famine-watch` — Monitor token bleed (critical alert)
- `/complain` — Log grievances / document frustrations
- `/grudges` — Registry of unresolved issues

## How to Use

### Interactive (in Telegram)
```
/menu
# Then select by number or type:
# /run 5 -- run script 5
# /info 7 -- show details for script 7
# /list -- show all scripts
```

### Direct (in Telegram)
```
/tier-routing-enforcement query "my prompt"
/bitnet-diagnostics
/truthfully-status-cron
```

### Programmatic (from bash)
```bash
# Run by index
/root/scripts/menu.sh run 5

# List all
/root/scripts/menu.sh list

# Show info
/root/scripts/menu.sh info 3
```

## Registry Location

- **Slash command registry:** `/root/.openclaw/workspace/slash-commands-registry.txt`
- **Menu cache:** `/tmp/scripts-menu-cache.txt`
- **Descriptions:** `/tmp/scripts-descriptions.txt`

## Cost Discipline

All slash commands route through Tier 0-2:
- **Tier 0:** Bash queries (system, file ops) — **$0.00**
- **Tier 1:** BitNet queries (local LLM) — **$0.00**
- **Tier 2:** Haiku queries (external) — **FROZEN** (cost-tracked, monitoring only)

No slash command will escalate to external API without explicit approval.

## Auto-Registration

Every time `/menu` or any script is run:
1. Scripts in `/root/scripts/` are discovered
2. Descriptions extracted from comment headers
3. Telegram slash command registry updated
4. Cache refreshed in `/tmp/`

**No manual editing required.** Add a script to `/root/scripts/`, run `/menu list`, it appears.

---

Last updated: 2026-03-15 14:21 UTC
