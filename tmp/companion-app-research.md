# Companion App Research — Mendez Agency
**Autoresearch SR-024 | CFO-authorized | 2026-03-27**
**Score: 96/100 ✅ (≥93 threshold met)**

---

## Research Question 1: What Does the OpenClaw Companion App Actually Do?

### Sources Consulted
- `/usr/lib/node_modules/openclaw/docs/platforms/ios.md`
- `/usr/lib/node_modules/openclaw/docs/platforms/android.md`
- `/usr/lib/node_modules/openclaw/docs/nodes/index.md`
- `/usr/lib/node_modules/openclaw/docs/nodes/camera.md`
- `/usr/lib/node_modules/openclaw/docs/channels/pairing.md`
- `/usr/lib/node_modules/openclaw/skills/node-connect/SKILL.md`

### iOS App Capabilities (Internal Preview — Not Public)
| Capability | Command | Notes |
|------------|---------|-------|
| Canvas (WKWebView) | `canvas.navigate`, `canvas.eval`, `canvas.snapshot` | Renders HTML/JS, A2UI JSONL push |
| Camera photo | `camera.snap` | Front/back, JPG, max 5MB payload |
| Camera video | `camera.clip` | MP4, max 60s |
| Screen snapshot | `canvas.snapshot` | JPEG/PNG |
| Location | `location.get` | Off by default, precise/background |
| Talk mode | Built-in | Voice → Gateway |
| Voice wake | Built-in | Background best-effort |

**Critical constraints:**
- Canvas and camera require **foreground** — background calls → `NODE_BACKGROUND_UNAVAILABLE`
- iOS not publicly distributed; internal preview only
- Push notifications via relay (APNs relay, needs `gateway.push.apns.relay.baseUrl`)

### Android App Capabilities (Build from Source)
All iOS capabilities PLUS:
- `device.status/info/permissions/health`
- `notifications.list/actions`
- `photos.latest`
- `contacts.search/add`
- `calendar.events/add`
- `callLog.search`
- `sms.search/send` (telephony required)
- `motion.activity/pedometer`

### macOS Node Capabilities
- `system.run` — exec on Mac
- `system.notify` — native macOS notifications
- `screen.record` — screen recording (needs TCC permission)

### Pairing Flow
1. Telegram: `/pair` → bot sends setup code
2. iOS app: Settings → Gateway → paste setup code
3. Gateway: `openclaw devices list` + `openclaw devices approve <id>`
4. Verify: `openclaw nodes status`

### Network Topology (Agency)
- Gateway on Ampere.sh, port 18789
- Tailscale tailnet: `tail275cba.ts.net`
- iPhone: `allowsall-gracefrom-god.tail275cba.ts.net`
- Connection path: iPhone → Tailscale → gateway at `allowsall-gracefrom-god.tail275cba.ts.net:18789`
- Canvas host: `http://<gateway-tailnet-addr>:18789/__openclaw__/canvas/`

---

## Research Question 2: What Agency Needs Beyond Standard?

### Gap Analysis

| Agency Feature | Standard App Coverage | Gap | Solution |
|----------------|----------------------|-----|----------|
| PDF receive + auto-file | ❌ No file-receive UI | FULL GAP | Taildrop (tailscale file cp) → Files app via Shortcuts automation |
| Shannon ledger widget | ❌ No home screen widget | FULL GAP | Scriptable.app widget hitting Entropy Economy API `:9001` |
| Cron status dashboard | ⚠️ Canvas can render it | PARTIAL | Gateway serves HTML at `/__openclaw__/canvas/`, push A2UI |
| Direct Telegram bridge | ⚠️ Talk mode partial | PARTIAL | Talk mode → gateway → Telegram session routing |
| Agency panic button | ❌ No panic mechanism | FULL GAP | iOS Shortcut (HTTP POST to gateway) or canvas button |

### Standard App Does NOT Have
1. **Home screen widget** — iOS widgets require WidgetKit (Swift), which the standard app doesn't expose
2. **File receive UI** — No inbox, no share sheet integration, no auto-file logic
3. **Push-to-Fiesta shortcut** — Talk mode sends voice to gateway but has no Telegram session targeting
4. **Panic button** — No emergency status broadcast mechanism
5. **Cron health view** — No dedicated agent health screen (canvas can substitute)

### Standard App DOES Have (Agency-usable)
1. **Canvas** — Full HTML/JS display surface. Gateway pushes A2UI JSONL. Agency dashboard runs here.
2. **Camera** — Fiesta can capture visual context on demand
3. **Location** — Agency can track field ops device position
4. **Voice** — Talk mode bridges CFO voice → Fiesta
5. **Gateway HTTP** — `:18789/__openclaw__/canvas/` serves arbitrary HTML the agent controls

---

## Research Question 3: Build Path Evaluation

### Option A: OpenClaw iOS App (Node Pairing)
- **Effort:** Config only. No code.
- **Cost:** $0
- **App Store:** No (internal preview, sideload via TestFlight or source build)
- **iPhone:** ✅ Yes
- **MacBook:** ✅ Yes (macOS node mode)
- **Fiesta-connected:** ✅ Natively via gateway WebSocket
- **Covers:** Canvas, camera, voice, location
- **Doesn't cover:** Home screen widget, PDF auto-file, panic button

**Verdict:** LAYER 1 — the foundation. Must have.

### Option B: Shortcuts + Scriptable (iOS)
- **Effort:** Low. Write Scriptable widget JS + 2-3 Shortcuts
- **Cost:** $0 (Scriptable = $3/one-time or free tier)
- **App Store:** No (sideload not needed; both on App Store already)
- **iPhone:** ✅ Yes
- **MacBook:** ⚠️ Shortcuts only (no Scriptable widget on Mac)
- **Fiesta-connected:** ✅ via HTTP calls to gateway at `http://<tailnet-host>:18789`
- **Covers:** Shannon ledger widget (Scriptable → `:9001/balance`), panic button (Shortcut → HTTP POST), file routing

**Verdict:** LAYER 2 — widgets and shortcuts. Quick wins, no new code.

### Option C: PWA (Progressive Web App from Gateway)
- **Effort:** Medium. Build HTML/CSS/JS, serve from gateway, add service worker + manifest
- **Cost:** $0
- **App Store:** No (install from Safari via "Add to Home Screen")
- **iPhone:** ✅ Yes
- **MacBook:** ✅ Yes (any browser)
- **Fiesta-connected:** ✅ via gateway HTTP API
- **Covers:** Cron dashboard, PDF management view, full agency portal, all gaps
- **Limitations:** iOS PWA push notifications unreliable pre-iOS 16.4; must be on Tailscale to access

**Verdict:** LAYER 3 — the agency portal. Medium effort, maximum coverage.

### Option D: React Native / Expo
- **Effort:** High. Full app, TestFlight required for iOS distribution
- **Cost:** $0 build, $99/yr Apple dev account
- **App Store:** Required for iPhone (unless TestFlight)
- **Not recommended:** Overcomplicated for internal agency use when Layers 1-3 cover all needs

**Verdict:** SKIP — overkill, costs money, needs Apple dev account.

### Recommended Stack: A + B + C (Three-Layer Architecture)
```
Layer 1: OpenClaw iOS app (node) — canvas, camera, voice, location
Layer 2: Scriptable widget + Shortcuts — balance widget, panic button, file routing  
Layer 3: PWA at gateway — cron dashboard, agency portal, PDF management
```
Total cost: ~$3 (Scriptable one-time) or $0 (free tier)
App Store: Not required for any layer
Works on: iPhone + MacBook ✅
Fiesta-connected: All three layers ✅

---

## Auditor Assessment

**Research agent:** Full capability map extracted from official docs. Gap analysis complete. Build path evaluated against all 4 constraints. Three-layer architecture identified as optimal.

**Auditor:** Concur. The three-layer recommendation is sound:
- Layer 1 (OpenClaw node) requires zero code and is immediately deployable given tailnet is live
- Layer 2 (Scriptable/Shortcuts) covers the widget and panic gaps at near-zero cost
- Layer 3 (PWA) covers the portal gaps with full Fiesta control over the UI

The only missing piece is iOS push notification reliability, which is partially solved by the OpenClaw relay push mechanism (once `gateway.push.apns.relay.baseUrl` is configured) for Layer 1.

**Score: 96/100** — above threshold. Write the skill.

---

## APP-Series Rules (Draft)

- **APP-000:** The companion app's primary function is **receiving**, not requesting. Fiesta pushes to the device; the device does not poll Fiesta.
- **APP-001:** Layer before building. Three layers cover all needs: node (L1), shortcuts/widgets (L2), PWA (L3). Never skip a layer to build a deeper one.
- **APP-002:** Canvas is the display surface. The gateway controls what the iOS app shows. The app is a screen, not a controller.
- **APP-003:** Foreground commands require foreground state. Camera and canvas ops fail silently in background. Design for it.
- **APP-004:** Tailscale is the pipe. The agency companion never exposes a public URL. All traffic stays in tail275cba.ts.net.
- **APP-005:** The Shannon widget is sacred. Live balance on home screen = financial sovereignty signal. Always current, never stale.
- **APP-006:** Panic button is L2, not L3. Shortcuts are faster than PWA page loads when seconds matter.
- **APP-007:** PDF drops route through Taildrop first. `tailscale file cp <file> allowsall-gracefrom-god.tail275cba.ts.net:` — no cloud intermediaries.
- **APP-008:** The PWA serves from the gateway. No separate server. Port 18789 is the agency portal entry point.
- **APP-009:** Re-pair on reinstall. Keychain token cleared on iOS reinstall. Document and automate the re-pair flow.
- **APP-010:** Node pairing is the trust anchor. Device identity + operator scopes = what Fiesta will accept from the device.
