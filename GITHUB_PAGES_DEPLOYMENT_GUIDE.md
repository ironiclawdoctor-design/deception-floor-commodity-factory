# GitHub Pages Deployment — Landing Page to Live (5 minutes)

## What You're Deploying
- **File:** `/root/.openclaw/workspace/www/landing.html`
- **Purpose:** Convert users to $9.99/month Grok + Tailscale tier
- **Status:** Ready to ship (tested, committed)

## Which Repo?

You have 4 active repos. Pick one:
1. **deception-floor-commodity-factory** — Core agency production (recommended)
2. **precinct92-magical-feelings-enforcement** — Daimyo jurisdiction (enforcement/monetization)
3. **disclaimer-parody-satire-all-feddit** — Nemesis clandestine ops
4. **trad-incumbent-grumpy-allows-all** — Fergus demo/rehabilitation

**I recommend precinct92** (Daimyo owns monetization, cost enforcement).

## Deployment Steps (You Execute, I Guide)

### Step 1: Copy Landing Page to Target Repo
```bash
# SSH into your repo, go to precinct92 (or chosen repo)
cd ~/precinct92-magical-feelings-enforcement
mkdir -p www
cp /root/.openclaw/workspace/www/landing.html www/index.html
# Or: cp to root as index.html if you want it as homepage
git add www/index.html
git commit -m "Landing page: Grok + Tailscale tier ($9.99/month)"
git push origin main
```

### Step 2: Enable GitHub Pages (In Web UI)
1. Go to repo → **Settings**
2. Scroll to **Pages** (left sidebar)
3. **Source:** Select `main` branch
4. **Folder:** Select `/ (root)` or `/www` (depending on where you put the file)
5. **Click Save**
6. GitHub will display your live URL: `https://your-username.github.io/precinct92-magical-feelings-enforcement/` (or similar)

### Step 3: Test the Live Page
Once GitHub Pages is enabled (60 seconds), visit the URL and verify:
- ✅ Page loads (no 404)
- ✅ "Get Started" button visible
- ✅ Pricing section shows $9.99/month
- ✅ Tailscale info reads clearly

### Step 4: Verify Tailscale Access Works
From the live page, the CTA should link to Tailscale setup. Test:
- Can you click "Get Started"?
- Does it make sense what happens next?

## What Happens After Deployment

### You Have a Live Public URL
- Share with users
- Track GitHub Pages traffic (Settings → Pages → View traffic)
- Measure conversion (if you set up Stripe/PayPal, track signups)

### Growth Signals to Watch
1. **Page views** — GitHub Pages gives free analytics
2. **Conversion rate** — 1% of views → sign up = good baseline
3. **Cost per acquisition** — $0 (it's already public)
4. **Revenue** — First user → $9.99/month starts flowing

### If You Want to Track More Deeply
- Add Google Analytics (free, non-invasive)
- Or: I can build a bash script to log landing page requests (local file logging)
- Pattern: User visits → logs click → Actually tracks → I report trends

## Next Milestones (In Order)

1. **Pages live** (do this now)
2. **Get 1st user** (share link, ask for feedback)
3. **Measure conversion** (10 views = X conversions?)
4. **Iterate messaging** (what's stopping the other 90%?)
5. **Scale acquisition** (once you know what converts)

## Integration Checklist

Before you flip the switch:
- [ ] Tailscale IP (100.76.206.82) is current in your network
- [ ] Grok server (port 8889) is running
- [ ] BitNet fallback (port 8080) is running
- [ ] Landing page mentions both clearly
- [ ] You have a way to accept payment ($9.99/month)
  - *Not done yet:* Stripe integration (skill exists, need your Stripe API key)
  - *Not done yet:* PayPal integration (skill exists, need your PayPal credentials)
  - **Alternative:** Direct signup → "Contact for payment setup" (manual for first 10 users)

## If You Want to Accept Payment Now

I can guide you through:
- **Stripe setup** (30 min, free tier available)
- **PayPal setup** (30 min, no monthly fee)
- **Simple payment flow** (user signs up → gets Tailscale IP → runs local Grok)

But that's a separate decision. Landing page can go live without payment integrated (MVP: collect signups, process manually).

## One More Thing

Once this is live, Actually will watch:
- Page views (from GitHub analytics)
- User signups (from form submissions, if you add one)
- Conversion rate (signups / views)
- Revenue signals (first $9.99 charge)

No narration. Just logging. Ready to optimize once we have data.

---

**Status:** Landing page ready. Deployment = 5 minutes. Growth = your next move.

