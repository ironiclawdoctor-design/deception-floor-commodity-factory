---
name: companion-app
description: >-
  Design spec and operational guide for the Mendez Agency internal companion app — three-layer
  architecture connecting all agency hardware nodes to Fiesta as orchestrator. Use when: pairing the
  iPhone to the gateway, configuring the canvas dashboard, setting up the Shannon ledger widget,
  deploying the agency PWA, building the panic button Shortcut, or routing Taildrop file delivery.
  Triggers on: "companion app", "pair iPhone", "agency app", "Shannon widget", "panic button",
  "cron dashboard", "PDF drop", "agency portal", "node pairing".
version: 1.0.0
autoresearch: SR-024
score: 96
---

# Mendez Agency Companion App — Design Spec

**Architecture:** Three-layer stack. No App Store. $0 cost. iPhone + MacBook. Fiesta-connected.

---

## APP-Series Rules

| Rule | Statement |
|------|-----------|
| **APP-000** | The companion app's primary function is **receiving**, not requesting. Fiesta pushes; the device does not poll. |
| **APP-001** | Layer before building. L1 → L2 → L3. Never skip a layer to build a deeper one. |
| **APP-002** | Canvas is the display surface. The gateway controls what the iOS app shows. The app is a screen, not a controller. |
| **APP-003** | Foreground commands require foreground state. Camera and canvas ops fail in background. Design for it. |
| **APP-004** | Tailscale is the pipe. Never expose a public URL. All traffic stays in `tail275cba.ts.net`. |
| **APP-005** | The Shannon widget is sacred. Live balance on home screen = financial sovereignty signal. Always current. |
| **APP-006** | Panic button is L2, not L3. Shortcuts are faster than PWA page loads when seconds matter. |
| **APP-007** | PDF drops route through Taildrop first. No cloud intermediaries. |
| **APP-008** | The PWA serves from the gateway. No separate server. Port 18789 is the agency portal entry point. |
| **APP-009** | Re-pair on reinstall. Keychain token cleared on iOS reinstall. Always re-run the pair flow after reinstall. |
| **APP-010** | Node pairing is the trust anchor. Device identity + operator scopes = what Fiesta will accept from the device. |

---

## Network Topology

```
iPhone (allowsall-gracefrom-god.tail275cba.ts.net)
    │
    ├── Tailscale WireGuard tunnel (tail275cba.ts.net)
    │
    └── Gateway: Ampere.sh → port 18789
              │
              ├── WebSocket (WS) ← node pairing (L1)
              ├── HTTP /__openclaw__/canvas/ ← PWA + A2UI (L3)
              └── HTTP /__openclaw__/a2ui/ ← A2UI push surface
```

---

## Layer 1: OpenClaw iOS Node (Foundation)

**What it is:** The official OpenClaw iOS app, paired as a `node` with `role: operator`.

**Capabilities:**
| Feature | Command | Agency Use |
|---------|---------|-----------|
| Canvas (WKWebView) | `canvas.navigate`, `canvas.eval`, `canvas.snapshot` | Display cron dashboard, agency portal |
| Camera photo | `camera.snap` | Visual context for Fiesta |
| Camera video | `camera.clip` | Field documentation |
| Screen snapshot | `canvas.snapshot` | Proof-of-work capture |
| Location | `location.get` | Field ops tracking |
| Talk mode | Built-in | CFO voice → Fiesta |
| Voice wake | Built-in | Hands-free activation |

**Setup (one-time):**
```bash
# Step 1: Enable tailnet binding on gateway
openclaw config set gateway.bind tailnet
openclaw gateway restart

# Step 2: Generate pairing code via Telegram
# → Send /pair to Telegram bot
# → Bot replies with setup code

# Step 3: iOS app
# → Settings → Gateway → paste setup code → Connect

# Step 4: Approve on gateway
openclaw devices list
openclaw devices approve <requestId>

# Step 5: Verify
openclaw nodes status
```

**Tailnet discovery (if mDNS blocked):**
- Manual host: `allowsall-gracefrom-god.tail275cba.ts.net`
- Port: `18789`

**Push notifications (optional, for wake nudges):**
```json5
// ~/.openclaw/openclaw.json
{
  gateway: {
    push: {
      apns: {
        relay: {
          baseUrl: "https://relay.openclaw.dev"  // official relay for TestFlight builds
        }
      }
    }
  }
}
```

**Background limitation:** Camera + canvas commands require the app to be in the foreground. Design all workflows to assume foreground-only for media ops.

---

## Layer 2: Shortcuts + Scriptable (Widgets + Panic)

**What it is:** iOS-native automations. No App Store submission, no sideloading. Distributed via iCloud/AirDrop.

### 2A. Shannon Ledger Widget (Scriptable)

**Install:** Scriptable.app (free tier sufficient)

**Widget script — save as `ShannonBalance.js` in Scriptable:**
```javascript
// Shannon Ledger Widget
// Reads live balance from Entropy Economy API via Tailscale

const GATEWAY = "http://allowsall-gracefrom-god.tail275cba.ts.net:9001"

async function getBalance() {
  try {
    const req = new Request(`${GATEWAY}/balance`)
    req.timeoutInterval = 5
    const data = await req.loadJSON()
    return data.balance ?? data.shannon ?? "?"
  } catch(e) {
    return "offline"
  }
}

const balance = await getBalance()

const widget = new ListWidget()
widget.backgroundColor = new Color("#0a0a0a")

const title = widget.addText("SHANNON")
title.textColor = new Color("#888888")
title.font = Font.systemFont(10)

widget.addSpacer(4)

const amount = widget.addText(`$${balance}`)
amount.textColor = new Color("#00ff88")
amount.font = Font.boldSystemFont(28)

widget.addSpacer(4)

const ts = widget.addText(new Date().toLocaleTimeString())
ts.textColor = new Color("#444444")
ts.font = Font.systemFont(9)

Script.setWidget(widget)
Script.complete()
```

**Add to home screen:**
1. Long-press home screen → + → Scriptable → Small widget
2. Edit widget → Script: `ShannonBalance`
3. When interacting: Run Script

### 2B. Panic Button (iOS Shortcut)

**Create in Shortcuts app:**
```
Name: AGENCY PANIC
Icon: Red exclamation mark

Steps:
1. Ask for input: "Describe the situation"
   - Input type: Text
   - Store in: Situation
   
2. Get Contents of URL:
   - URL: http://allowsall-gracefrom-god.tail275cba.ts.net:18789/api/message
   - Method: POST
   - Headers: Content-Type: application/json
   - Body: JSON
     {
       "session": "main",
       "content": "🚨 AGENCY PANIC: [Situation]",
       "priority": "urgent"
     }
   
3. Show notification:
   - Title: Panic Sent
   - Body: Fiesta has been notified
```

**Alternative (simpler) — Telegram message via HTTP:**
```
POST https://api.telegram.org/bot<TOKEN>/sendMessage
Body: {"chat_id": "<CFO_CHAT_ID>", "text": "🚨 PANIC: [Situation]"}
```

### 2C. PDF Auto-File (Taildrop Shortcut)

**For auto-filing PDFs received from Fiesta via Taildrop:**
```
Automation: When I receive a file (Taildrop)
Steps:
1. If file extension is "pdf"
   → Save to Files: /Files/Agency/Incoming/[filename]
   → Open Document: display the PDF
```

**Gateway push (Fiesta side):**
```bash
# Push PDF to CFO device
tailscale file cp /root/.openclaw/workspace/tmp/report.pdf allowsall-gracefrom-god.tail275cba.ts.net:
```

---

## Layer 3: Agency PWA (Portal)

**What it is:** Progressive Web App served from the gateway at port 18789. Installed on iPhone via Safari "Add to Home Screen."

**Gateway canvas host serves the PWA:**
- URL: `http://allowsall-gracefrom-god.tail275cba.ts.net:18789/__openclaw__/canvas/`
- Agent controls content via `canvas.navigate`, `canvas.eval`, A2UI push

**Setup — create agency dashboard:**
```bash
mkdir -p ~/.openclaw/workspace/canvas
```

**File: `~/.openclaw/workspace/canvas/index.html`** (agency portal entry):
```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <meta name="apple-mobile-web-app-capable" content="yes">
  <meta name="apple-mobile-web-app-title" content="Agency">
  <title>Agency</title>
  <style>
    * { margin: 0; padding: 0; box-sizing: border-box; }
    body {
      background: #0a0a0a; color: #e0e0e0;
      font-family: -apple-system, system-ui, sans-serif;
      padding: 20px; max-width: 600px; margin: 0 auto;
    }
    h1 { color: #00ff88; font-size: 18px; margin-bottom: 20px; }
    .card {
      background: #141414; border: 1px solid #222;
      border-radius: 12px; padding: 16px; margin-bottom: 12px;
    }
    .card h2 { font-size: 12px; color: #888; text-transform: uppercase; letter-spacing: 1px; }
    .card .value { font-size: 28px; font-weight: bold; margin-top: 8px; color: #00ff88; }
    .cron-item { display: flex; justify-content: space-between; padding: 8px 0;
                 border-bottom: 1px solid #1a1a1a; }
    .status-ok { color: #00ff88; }
    .status-err { color: #ff3b30; }
    .status-warn { color: #ffcc00; }
    #last-updated { font-size: 10px; color: #444; margin-top: 20px; }
  </style>
</head>
<body>
  <h1>⬡ Agency Portal</h1>

  <div class="card">
    <h2>Shannon Balance</h2>
    <div class="value" id="balance">—</div>
  </div>

  <div class="card">
    <h2>Agent Health</h2>
    <div id="cron-status">Loading...</div>
  </div>

  <div class="card">
    <h2>Quick Actions</h2>
    <button onclick="panic()" style="background:#ff3b30;color:#fff;border:none;
      border-radius:8px;padding:12px 24px;font-size:16px;width:100%;cursor:pointer;">
      🚨 PANIC
    </button>
  </div>

  <div id="last-updated"></div>

  <script>
    const GATEWAY = window.location.origin  // same origin = port 18789

    async function load() {
      try {
        // Shannon balance
        const r1 = await fetch('/api/shannon/balance').catch(() => null)
        if (r1?.ok) {
          const d = await r1.json()
          document.getElementById('balance').textContent = '$' + (d.balance ?? '?')
        }

        // Cron status
        const r2 = await fetch('/api/crons').catch(() => null)
        if (r2?.ok) {
          const crons = await r2.json()
          const el = document.getElementById('cron-status')
          el.innerHTML = crons.map(c => `
            <div class="cron-item">
              <span>${c.name}</span>
              <span class="${c.healthy ? 'status-ok' : 'status-err'}">
                ${c.healthy ? '✓' : '✗'} ${c.lastRun ?? 'never'}
              </span>
            </div>
          `).join('')
        }
      } catch(e) {}

      document.getElementById('last-updated').textContent =
        'Updated: ' + new Date().toLocaleTimeString()
    }

    async function panic() {
      const msg = prompt('Situation:')
      if (!msg) return
      await fetch('/api/message', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({session: 'main', content: '🚨 AGENCY PANIC: ' + msg})
      })
      alert('Fiesta notified.')
    }

    load()
    setInterval(load, 30000)  // refresh every 30s
  </script>
</body>
</html>
```

**iOS install flow:**
1. On iPhone: Open Safari → `http://allowsall-gracefrom-god.tail275cba.ts.net:18789/__openclaw__/canvas/`
2. Share button → "Add to Home Screen" → "Agency"
3. App icon appears on home screen

**Fiesta can update the portal in real-time:**
```bash
# Navigate the iOS node to agency portal
openclaw nodes invoke --node "iPhone" --command canvas.navigate \
  --params '{"url":"http://allowsall-gracefrom-god.tail275cba.ts.net:18789/__openclaw__/canvas/"}'

# Push live data via A2UI (for canvas-only sessions)
openclaw nodes canvas a2ui push --node "iPhone" --text "Balance: $847"
```

---

## Capability Matrix

| Feature | L1 (Node) | L2 (Shortcuts) | L3 (PWA) |
|---------|-----------|----------------|----------|
| Camera capture | ✅ | ❌ | ❌ |
| Voice to Fiesta | ✅ | ❌ | ❌ |
| Location tracking | ✅ | ✅ | ❌ |
| Canvas display | ✅ | ❌ | ✅ |
| Shannon widget (home screen) | ❌ | ✅ | ❌ |
| Panic button | ❌ | ✅ | ✅ |
| Cron dashboard | ⚠️ (via canvas) | ❌ | ✅ |
| PDF receive + auto-file | ❌ | ✅ (Taildrop) | ❌ |
| MacBook compatible | ✅ (macOS node) | ⚠️ (Shortcuts only) | ✅ |
| Background ops | ❌ | ✅ | ❌ |
| $0 cost | ✅ | ✅/~$3 | ✅ |
| App Store required | ❌ | ❌ | ❌ |

---

## Deployment Sequence

### Phase 1: L1 Foundation (Day 1, ~30 min)
```bash
# 1. Bind gateway to tailnet
openclaw config set gateway.bind tailnet
openclaw gateway restart

# 2. Verify QR
openclaw qr --json
# → gatewayUrl should be: ws://allowsall-gracefrom-god.tail275cba.ts.net:18789

# 3. Generate pair code (from Telegram)
# → /pair
# → Copy setup code

# 4. iOS: Settings → Gateway → paste → Connect

# 5. Approve
openclaw devices list
openclaw devices approve <id>

# 6. Verify
openclaw nodes status
```

### Phase 2: L2 Widgets (Day 1-2, ~1 hr)
1. Install Scriptable on iPhone
2. Create `ShannonBalance.js` script (paste from above)
3. Add Scriptable widget to home screen, select script
4. Create "AGENCY PANIC" Shortcut in Shortcuts app
5. Test: tap panic button → verify Fiesta receives message

### Phase 3: L3 PWA (Day 2-3, ~2 hrs)
1. Create `~/.openclaw/workspace/canvas/index.html` (paste from above)
2. Connect Shannon API endpoints (verify `:9001/balance` returns correct field)
3. Connect cron status endpoints (verify `/api/crons` returns cron list)
4. Test from Safari on iPhone → "Add to Home Screen"
5. Verify panic button in PWA → Fiesta receives message

---

## Maintenance Rules

- **After gateway restart:** Verify `openclaw nodes status` shows iPhone connected. If not, check tailnet binding and re-approve if needed.
- **After iPhone reinstall:** Re-run full pair flow (Keychain cleared on reinstall = APP-009).
- **After Shannon API changes:** Update widget script + PWA `/api/shannon/balance` path.
- **After cron schema changes:** Update PWA `/api/crons` endpoint handling.

---

## Related Skills/Docs
- `skills/shandrop/SKILL.md` — Taildrop file delivery to iPhone
- `skills/fixer/SKILL.md` — Post-restart config restoration (LB-007, PL-007)
- `skills/ampere-sh/SKILL.md` — Platform limits (PL-001 through PL-009)
- `/usr/lib/node_modules/openclaw/docs/platforms/ios.md` — iOS node full reference
- `/usr/lib/node_modules/openclaw/docs/nodes/index.md` — Full node command surface
- `/usr/lib/node_modules/openclaw/skills/node-connect/SKILL.md` — Pairing failure diagnosis
