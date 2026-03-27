# TOOLS.md - Local Notes

Skills define _how_ tools work. This file is for _your_ specifics — the stuff that's unique to your setup.

## What Goes Here

Things like:

- Camera names and locations
- SSH hosts and aliases
- Preferred voices for TTS
- Speaker/room names
- Device nicknames
- Anything environment-specific

## Taildrop

- **CFO device:** `allowsall-gracefrom-god.tail275cba.ts.net`
- Command: `tailscale file cp <file> allowsall-gracefrom-god.tail275cba.ts.net:`
- All PDF snapshots (TRUMP.md, anomaly status, daily status) route here

## OpenClaw Diagnostic Commands (Pentagon — SR-026)

Run these before touching config. All read-only. All free.

- `openclaw /commands` → lists all slash commands
- `openclaw /models` → shows default model, auth status, configured models
- `openclaw /status` → gateway health, sessions, channels, security warnings
- `openclaw gateway status` → gateway reachability, port, mode
- `openclaw config get tools.exec` → reads exec host config without patching
- `openclaw health` → full system diagnostic

**Pentagon order (exec blocked):**
1. `/commands`
2. `/models`
3. `/status`
4. Read `.bork.bak`
5. Spawn subagent

Config patch is not on the list. (SR-026)

## Examples

```markdown
### Cameras

- living-room → Main area, 180° wide angle
- front-door → Entrance, motion-triggered

### SSH

- home-server → 192.168.1.100, user: admin

### TTS

- Preferred voice: "Nova" (warm, slightly British)
- Default speaker: Kitchen HomePod
```

## Why Separate?

Skills are shared. Your setup is yours. Keeping them apart means you can update skills without losing your notes, and share skills without leaking your infrastructure.

---

Add whatever helps you do your job. This is your cheat sheet.
