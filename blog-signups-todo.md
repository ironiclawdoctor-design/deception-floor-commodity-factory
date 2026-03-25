# Blog & Signup Platform Research
_DEA Autoresearch — 2026-03-25_

---

## ✅ DEPLOYED: Listmonk (PREFERRED — self-hosted)

**Status: LIVE on port 9003**

- **URL:** http://localhost:9003 (internal only — see HR-009, no public ports on Ampere)
- **Admin:** `admin` / `dollaragency2026`
- **Database:** PostgreSQL 16 (running on same VPS)
- **Install path:** `/opt/listmonk/`
- **Config:** `/opt/listmonk/config.toml`
- **Service:** `systemctl status listmonk` (enabled, starts on boot)
- **API health:** `curl http://localhost:9003/api/health` → `{"message":"invalid session"}` (auth required = working)

### What it does
- Full newsletter/mailing list manager
- REST API for all operations (subscribers, campaigns, templates)
- Handles millions of subscribers at ~57MB RAM
- Transactional mail support
- Webhooks, SMS, WhatsApp via Messenger interfaces
- Zero cost, no free tier to close, runs forever on VPS

### Next steps for Listmonk
1. Configure SMTP (Resend free tier recommended — see below)
2. Create a mailing list via API: `POST /api/lists`
3. Wire the signup page (`/workspace/signup/index.html`) to POST to listmonk's subscriber API
4. Subscribe endpoint: `POST http://localhost:9003/api/public/subscription`

---

## ✅ BUILT: Internal Signup Page

- **Location:** `/root/.openclaw/workspace/signup/index.html`
- **Backend:** `/root/.openclaw/workspace/signup/server.py` (port 9002)
- **Storage:** `/root/.openclaw/workspace/internal-mail/signups.jsonl`
- **Static fallback:** Yes — works without server via localStorage + JSON export button
- **Style:** Monospace, dark, green text (miner aesthetic)

---

## Platform Research Results

### Buttondown.email ✅ FREE TIER OPEN
- **Free:** Up to 100 subscribers, no credit card
- **API:** Yes — full REST API
- **Signup:** email + password (no Google OAuth)
- **Best for:** Simple newsletter, low subscriber count
- **2-min steps:** Go to buttondown.com → click "Start for free" → email/pass signup

### Loops.so ✅ FREE TIER OPEN
- **Free:** Up to 1,000 subscribed contacts
- **API:** Yes — full REST API, good docs
- **Signup:** Standard email registration at app.loops.so/register
- **Best for:** SaaS-style transactional + marketing email
- **Note:** No Google OAuth required — email/pass works

### Resend.com ✅ FREE TIER OPEN (RECOMMENDED for SMTP)
- **Free:** 3,000 emails/month, 100/day
- **API:** Excellent REST API, developer-first
- **Auth:** Email/password signup
- **Best for:** Wiring Listmonk's SMTP — set as outbound mail provider
- **2-min steps:** resend.com/signup → verify domain or use shared → get API key

### Tally.so ✅ FREE TIER OPEN — UNLIMITED
- **Free:** Unlimited forms, unlimited submissions (fair use)
- **API:** Full programmatic API (free)
- **No backend needed:** Embeds directly in HTML, webhooks to your endpoint
- **Best for:** Drop-in signup form replacement if server goes down
- **2-min steps:** tally.so → signup → create form → embed or use webhook URL

### Brevo (Sendinblue) ⚠️ FREE TIER EXISTS BUT DEGRADED
- **Free:** Was 300 emails/day — page now shows "Starter from 5,000/mo" (paid)
- **Status:** Free tier may still exist but not prominently shown; likely requires verification
- **API:** Yes — REST API with good docs
- **Verdict:** Use Resend instead — cleaner, no logo requirements, better DX

### Write.as ⚠️ ANONYMOUS POSTS WORK, IP RATE-LIMITED
- **Status:** 4/10 Hashnode articles cross-posted successfully
- **Issue:** Temporary IP block after 429; remaining 6 in retry queue
- **Retry:** Next DEA cron run (6h) will clear queue
- **Published posts:** See `writeas-posts.jsonl`

---

## Self-Hostable Priority Stack (Port Map)

| Port | Service | Status |
|------|---------|--------|
| 9002 | Signup server (Python http.server) | BUILT, start manually |
| 9003 | Listmonk newsletter manager | **LIVE** ✅ |
| 9004 | Reserved (Formbricks if needed) | — |
| 9005 | Reserved (Ghost/Plausible if needed) | — |

---

## Programmatic Blog Posting — Platform Status

| Platform | API | Free Tier | Notes |
|----------|-----|-----------|-------|
| Hashnode | ✅ GraphQL | ✅ Open | Already active — `dollaragency.hashnode.dev` |
| Write.as | ✅ REST | ✅ Anonymous posts | 4/10 articles posted; 6 in retry queue |
| Dev.to | ✅ REST | ✅ Open | API key at `secrets/devto-api.json` — ready |
| Buttondown | ✅ REST | ✅ 100 subs | Register at buttondown.com |
| Loops | ✅ REST | ✅ 1k contacts | Register at app.loops.so/register |

---

## Action Items

- [ ] Register Resend.com — set as Listmonk SMTP provider
- [ ] Register Loops.so — secondary email capture
- [ ] Register Buttondown.com — tertiary newsletter
- [ ] Wire signup page to Listmonk subscriber API (replace localStorage fallback)
- [ ] Start signup server: `python3 /root/.openclaw/workspace/signup/server.py &`
- [ ] Write.as retry queue: 6 posts pending, will clear on next cron

— DEA, Democratic Expansion Autoapprove
