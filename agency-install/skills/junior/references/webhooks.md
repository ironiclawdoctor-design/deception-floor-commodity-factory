# 📡 JUNIOR WEBHOOK REFERENCE
## Agency Interests: Inbound & Outbound Webhook Catalog

---

## WHAT IS A WEBHOOK (Junior Edition)
A webhook is a POST request that fires automatically when an event happens.
- **Inbound:** Someone else POSTs to us → we react
- **Outbound:** We POST to someone else → they react
- **Cost:** $0.00 (Tier 0 Bash + curl)

---

## TIER 1: OUTBOUND WEBHOOKS (We Send)

### 1. Mattermost
```bash
curl -X POST "$MATTERMOST_WEBHOOK_URL" \
  -H 'Content-Type: application/json' \
  -d '{"text": "Agency Report: All systems nominal."}'
```
**Agency Use:** Mission Control reports, Junior task completions, ShanApp ledger updates.

### 2. Slack-Compatible (Mattermost uses same format)
```bash
curl -X POST "$SLACK_WEBHOOK_URL" \
  -H 'Content-Type: application/json' \
  -d '{"text": "Fiesta Agency: $1.22 vendpoint staged."}'
```
**Agency Use:** External partner notifications, RealWife Network updates.

### 3. Discord
```bash
curl -X POST "$DISCORD_WEBHOOK_URL" \
  -H 'Content-Type: application/json' \
  -d '{"content": "Shannon Economy: TX-141 confirmed."}'
```
**Agency Use:** Focus Group announcements, YouTube drop alerts, ClawHub publish confirmations.

### 4. Telegram Bot API
```bash
curl -X POST "https://api.telegram.org/bot$TELEGRAM_TOKEN/sendMessage" \
  -d "chat_id=$CHAT_ID&text=JUNIOR+REPORT:+Queue+cleared."
```
**Agency Use:** Prophet (Elevated Exec) mission reports.

### 5. Stripe Webhook (Outbound Listener Registration)
```bash
stripe listen --forward-to localhost:9004/webhook
```
**Agency Use:** Payment confirmation → ShanApp mint trigger → Affiliate payout.

### 6. Generic POST (Any Target)
```bash
curl -X POST "$WEBHOOK_URL" \
  -H 'Content-Type: application/json' \
  -d "{\"event\": \"agency\", \"value\": \"$1\", \"shannon\": \"$2\"}"
```
**Agency Use:** Ampere.sh affiliate signups, Shanbase.fia trade confirmations.

---

## TIER 2: INBOUND WEBHOOKS (We Receive)

### 1. Stripe Payment Hook
- **Port:** 9004
- **Event:** `payment_intent.succeeded`
- **Action:** Mint Shannon, credit Prophet's ledger, notify Mattermost

### 2. ClawHub Publish Hook (Future — post 14-day gate)
- **Port:** TBD
- **Event:** `skill.published`
- **Action:** Log TX to ledger, announce on Discord

### 3. GitHub Actions Hook
- **Port:** TBD
- **Event:** `push`, `pull_request`
- **Action:** Trigger Excellence Creep audit, update Provincial status

### 4. Custom ShanApp Trigger
- **Port:** 8000
- **Event:** Any POST to `/shan`
- **Action:** Process Shannon transaction, update `memory/ledger.jsonl`

---

## AGENT ROUTING MAP
```
EVENT                    → HANDLER              → CHANNEL
---------------------------------------------------------------------------
Payment received         → Stripe → Port 9004  → Mattermost + Shannon Mint
ClawHub skill published  → GitHub → Port TBD   → Discord + Ledger
Junior task complete     → FSH → execute_queue  → Telegram (Prophet)
ShanApp transaction      → Port 8000            → Shanbase.fia + Ledger
Affiliate signup         → Ampere.sh            → RealWife Network + Ledger
```

---

## SECURITY (SR-001/002)
- All inbound webhooks must verify a `X-Agency-Signature` header
- Store all secrets in `~/.openclaw/secrets/` (chmod 600)
- Log all events to `memory/ledger.jsonl` with `[WEBHOOK]` tag
- Never expose raw webhook payloads to external logs

---

## NEXT JUNIOR TASKS
- [ ] Set MATTERMOST_WEBHOOK_URL in secrets
- [ ] Wire Discord webhook for ClawHub publish alerts
- [ ] Test Stripe → ShanApp mint pipeline on port 9004
