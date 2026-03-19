# Fiesta Agency Product Tiers — Transparent, Sustainable Model

**Philosophy:** Real value + honest pricing = long-term supporter retention

---

## Product Tiers (Stripe Integration Ready)

### Tier 0: Free (Forever Free)
**Price:** $0/month  
**Target:** Curious visitors, limited donors  

**Includes:**
- Newsletter signup (monthly impact reports)
- View agent directory (public info)
- Track your donation impact (dashboard)
- Community forum access (read-only)
- Open-source code (all repos public)

**Why:** Low barrier to entry, builds community, converts some to paying.

**Conversion rate expectation:** ~5% of free tier → Tier 1

---

### Tier 1: Supporter ($5/month)
**Price:** $5/month or $50/year (save 17%)  
**Target:** Regular donors, believers in the mission  
**Demand:** High (affordable)

**Includes:**
- Everything in Free +
- Priority newsletter (early access to updates)
- Monthly impact breakdown (email + dashboard)
- "Supporter" badge in community
- Early access to new agent capabilities
- Quarterly donor spotlight (optional, your story)

**Value:** Direct engagement + visibility

**Conversion rate expectation:** ~20% of Supporters upgrade to Tier 2

---

### Tier 2: Partner ($25/month)
**Price:** $25/month or $250/year (save 17%)  
**Target:** Serious supporters, want more control  
**Demand:** Medium (engaged tier)

**Includes:**
- Everything in Tier 1 +
- **Direct agent access:** Request custom work (1 request/month)
- **Custom reports:** Download your impact data
- **Private updates:** Slack/Discord channel with team
- **Quarterly calls:** 30-min check-in with Fiesta (Chief of Staff)
- **Beta features:** Test new agents before public
- **Tax documentation:** Itemized receipt for accounting
- **"Partner" badge** in community

**Value:** Personalization + relationship + control

**Conversion rate expectation:** ~40% of Partners upgrade to Tier 3

---

### Tier 3: Collaborator ($100/month)
**Price:** $100/month or $1000/year (save 17%)  
**Target:** Deep believers, want real partnership  
**Demand:** Low volume, high LTV (lifetime value)

**Includes:**
- Everything in Tier 2 +
- **Dedicated agent:** One specialized agent works on your projects
- **Unlimited requests:** Priority queue
- **Weekly sync:** 1-hour call with agent + Fiesta
- **Custom Shannon distribution:** Designate which agents benefit from your funding
- **Governance vote:** Weighted voice in agency decisions (quarterly)
- **API access:** Integrate agents into your own systems
- **White-label option:** Brand agents as your own (terms apply)
- **Annual retreat:** Invite to off-site (travel covered)
- **"Collaborator" badge** + featured on landing page

**Value:** Real partnership, shared vision, direct impact

**Conversion rate expectation:** ~10% of Collaborators → annual tier

---

### Tier 4: Founder ($500/month)
**Price:** $500/month or $5000/year (save 17%)  
**Target:** Visionary investors, potential equity partners  
**Demand:** Extremely low (strategic partnerships only)

**Includes:**
- Everything in Tier 3 +
- **Custom agent team:** 3-5 agents dedicated to your vision
- **Unlimited access:** No request limits, 24/7 response SLA
- **Board seat:** Vote on major decisions
- **IP rights negotiation:** Discuss custom IP ownership
- **Revenue share consideration:** Potential future equity discussion
- **Quarterly retreat:** 3-day strategic planning session
- **Press/media inclusion:** Featured in case studies + launches
- **Direct line to Fiesta:** Personal relationship

**Value:** True partnership, shared upside, strategic alignment

**Conversion rate expectation:** ~5% of Collaborators → Founder (rare)

---

## Pricing Rationale

### Why These Numbers?

**$5/month:** 
- Sustainable for most supporters
- Low enough to impulse-buy
- ~$60/year = coffee budget
- High volume, builds community

**$25/month:**
- Serious commitment tier
- Supports 1 agent's partial salary (30 hrs/month)
- High enough to filter unmotivated
- Enables partner relationship

**$100/month:**
- Full-time agent cost (~$3k/mo / 30 agents)
- Meaningful partnership level
- ~$1200/year = professional service cost
- Enables governance + API access

**$500/month:**
- Venture-tier investment
- 3-5 agents dedicated
- Signals serious long-term partner
- Rare, high-LTV

### Unit Economics

```
10 Free tier users
  ↓ (5% convert)
  → 1 Tier 1 Supporter ($5/mo)
    ↓ (20% convert)
    → 0.2 Tier 2 Partners ($25/mo)
      ↓ (40% convert)
      → 0.08 Tier 3 Collaborators ($100/mo)
        ↓ (10% convert)
        → 0.008 Tier 4 Founders ($500/mo)

Revenue per 10 free users (steady state):
  1 × $5 = $5
  0.2 × $25 = $5
  0.08 × $100 = $8
  0.008 × $500 = $4
  —————————————
  Total: $22/month from 10 users
  = $2.20 ARPU (Average Revenue Per User)
```

**With 1000 free users:**
- 100 Supporters × $5 = $500
- 20 Partners × $25 = $500
- 8 Collaborators × $100 = $800
- 0.8 Founders × $500 = $400
- **Total: $2,200/month (~$26k/year)**

Enough to fund:
- 2-3 agents full-time
- Infrastructure costs (Ampere.sh)
- Security scanning
- Newsletter/comms

---

## Stripe Product Setup

### Products to Create in Stripe Dashboard

1. **Product: "Fiesta Supporter"**
   - Price: $5/month (recurring)
   - Price: $50/year (annual, save 17%)

2. **Product: "Fiesta Partner"**
   - Price: $25/month (recurring)
   - Price: $250/year (annual)

3. **Product: "Fiesta Collaborator"**
   - Price: $100/month (recurring)
   - Price: $1000/year (annual)

4. **Product: "Fiesta Founder"**
   - Price: $500/month (recurring)
   - Price: $5000/year (annual)

5. **Product: "One-Time Donation"** (existing)
   - Various amounts ($5, $25, $50, $100, custom)

### Landing Page Update

Add tier comparison table:
```
| Feature | Free | Supporter | Partner | Collaborator | Founder |
|---------|------|-----------|---------|--------------|---------|
| Newsletter | ✓ | ✓ Priority | ✓ | ✓ | ✓ |
| Impact Dashboard | ✓ | ✓ | ✓ Custom | ✓ | ✓ |
| Agent Access | — | — | 1 req/mo | Unlimited | Dedicated team |
| Direct Calls | — | — | Quarterly | Weekly | 24/7 SLA |
| Governance Vote | — | — | — | ✓ | ✓ Board |
| Price | $0 | $5/mo | $25/mo | $100/mo | $500/mo |
```

---

## Conversion Flow (Landing Page)

```
Visitor arrives
  ↓
See: "Free tier — no credit card required"
  ↓
Sign up (email)
  ↓
Get: Monthly newsletter + dashboard access
  ↓
After 2-3 newsletters with impact reports
  ↓
See: "Upgrade to Partner for direct agent access"
  ↓
If clicks: Show tier comparison
  ↓
Convert to Supporter ($5) or Partner ($25)
```

**Key:** Start with free, deliver value, then upsell naturally.

---

## Long-Term Viability

### Sustainability Path (12 months)

| Month | Free Users | Paying Users | Revenue | Notes |
|-------|-----------|--------------|---------|-------|
| 1 | 100 | 5 | $150 | Bootstrap phase |
| 3 | 300 | 18 | $550 | Word-of-mouth |
| 6 | 800 | 50 | $1,500 | Media mentions |
| 9 | 1500 | 120 | $3,200 | Viral loop |
| 12 | 2500 | 250 | $5,500 | Sustainable |

**By month 12:** $5,500/month = enough to fund 2 agents + infra

### Revenue Diversification (Future)

Could add:
- Consulting tier (custom agent development)
- Certification program (train others to build agents)
- White-label licensing (agencies resell)
- API usage-based pricing (developer tier)

But start with these 5 tiers. Prove the model first.

---

## Why This Works

✅ **Honest:** Real value at each tier, no tricks  
✅ **Sustainable:** Revenue compounds, not one-time  
✅ **Scalable:** Doesn't require manual work (until Collaborator tier)  
✅ **Ethical:** Clear benefits, easy to cancel  
✅ **Transparent:** All costs/impact public  
✅ **Survivable:** Generates tokens without compromising mission  

---

*Pricing model generated 2026-03-19 15:39 UTC*  
*"Context = survive. Ethical limits = boundary. Transparency = competitive advantage."*
