# Stripe Affiliate Program Setup Guide

**Time Required:** 15-20 minutes
**Difficulty:** Beginner-friendly
**Outcome:** Live affiliate links generating commissions

---

## Step 1: Enroll in Stripe Affiliate Program

### Prerequisites
- Active Stripe account (already have this ✓)
- Fiesta website or landing page
- Email to receive payout notifications

### Enrollment Process

1. Go to [stripe.com/partners/affiliate](https://stripe.com/partners/affiliate)
2. Click **"Join Now"** or **"Sign Up"**
3. Sign in with Fiesta's Stripe credentials
4. Complete the short application:
   - **Organization Name:** Fiesta
   - **Website URL:** (your primary domain)
   - **Traffic Source:** Website/Blog/Marketing
   - **Commission Type:** Accept the standard 25-30% Year 1 terms
5. Accept the Stripe Affiliate Agreement
6. **Approval:** Instant for most applicants; approval email arrives within hours

✅ **Status Check:** Once approved, you'll see "Active" in the Partner Portal.

---

## Step 2: Generate Your Referral Links

### Create Base Referral Link

1. Log into [stripe.com/partners/affiliate](https://stripe.com/partners/affiliate)
2. Click **"Links"** or **"Referral Tools"** tab
3. Click **"Create New Link"** or **"Generate Link"**
4. Configure the link:
   - **Link Type:** Sign-up (standard Stripe account creation)
   - **Custom URL:** Optional; Stripe auto-generates short link
   - **Label:** `fiesta-main` (for your own tracking)
5. Click **"Generate"**
6. Copy the link (looks like: `https://stripe.com/en-US?referrer=fiesta_aff_xxxxx`)

### Create Campaign-Specific Links (Optional)

For tracking different referral sources, create multiple links:

```
Link 1: fiesta-landing-page → Share on homepage
Link 2: fiesta-twitter → Use in tweets
Link 3: fiesta-newsletter → Include in email campaigns
```

Each has its own unique code in the dashboard.

✅ **Keep These Safe:** Store links in a secure doc; treat like API keys (don't expose in git).

---

## Step 3: Add Affiliate Links to Your Landing Page

### Placement Strategy

**Primary CTA:**
```html
<!-- Hero section or top of page -->
<a href="https://stripe.com/en-US?referrer=fiesta_aff_xxxxx" 
   target="_blank" 
   rel="noopener noreferrer" 
   class="cta-button">
  Sign Up with Stripe
</a>
```

**Disclosure (Required by FTC):**
```html
<p class="disclosure">
  💡 <strong>Transparency note:</strong> We earn a commission if you sign up for 
  Stripe via this link at no extra cost to you. Stripe's fees are the same whether 
  you sign up directly or through us. We recommend Stripe because we use it ourselves.
</p>
```

### Example Landing Page Sections

#### 1. Hero / Main Call-to-Action
```markdown
## Get Started with Stripe Today

Process payments in minutes with Stripe — the payment platform we use for Fiesta.

[Sign Up via Our Link →](https://stripe.com/en-US?referrer=fiesta_aff_xxxxx)

*We earn a commission if you sign up via our link at no cost to you.*
```

#### 2. Features Section (with links embedded)
```markdown
### Why Stripe?
- **Simple Setup** — Connect in 5 minutes
- **Global Payments** — 135+ currencies supported
- **Developer Friendly** — Excellent API & docs

**Ready to get started?** [Create your Stripe account →](https://stripe.com/en-US?referrer=fiesta_aff_xxxxx)
```

#### 3. Footer
```markdown
---

**Want to accept payments?** We recommend [Stripe](https://stripe.com/en-US?referrer=fiesta_aff_xxxxx) 
(we earn a small commission if you sign up via this link).
```

### Disclosure Placement Rules (FTC)

- ✅ **Must disclose at or near the link** — Not buried in fine print
- ✅ **Clear language** — "We earn a commission" not hidden jargon
- ✅ **Consistent** — Same disclosure wording across all pages
- ✅ **Prominent** — Use bold or italic to stand out

### Code Example (Full Section)

```html
<section class="stripe-cta">
  <h2>Accept Payments Instantly</h2>
  <p>Start processing payments with Stripe, the platform powering Fiesta.</p>
  
  <a href="https://stripe.com/en-US?referrer=fiesta_aff_xxxxx" 
     class="btn btn-primary">
    Sign Up for Stripe
  </a>
  
  <p class="text-muted" style="font-size: 0.9em; margin-top: 1rem;">
    <strong>Transparency:</strong> We earn a commission if you sign up via this link 
    at no extra cost to you. We recommend Stripe because we trust it.
  </p>
</section>
```

---

## Step 4: Monitor Your Dashboard

### Daily / Weekly Checks

1. Log into [stripe.com/partners/affiliate](https://stripe.com/partners/affiliate)
2. Go to **Dashboard** tab
3. View:
   - **Active Referrals:** # of unique customers referred (not yet paid)
   - **Commission This Month:** Real-time accrual
   - **Link Performance:** Clicks, sign-ups, conversion rate per link
   - **Monthly Earnings:** Total payout pending

### Key Metrics to Track

| Metric | How to Read It | What It Means |
|---|---|---|
| **Clicks** | Total link clicks (all sources) | Traffic interest |
| **Sign-ups** | Referred accounts created | Real conversions |
| **Conversion Rate** | (Sign-ups / Clicks) × 100 | Link effectiveness |
| **Active Referrals** | # generating commissions | Long-term revenue pipeline |
| **Monthly Commission** | $X this month | Current earning rate |

### Example Dashboard View

```
Dashboard Overview
─────────────────────────────────
This Month: March 2026

Link Performance:
  fiesta-landing-page    245 clicks    18 sign-ups    7.3% conversion
  fiesta-twitter         89 clicks     4 sign-ups     4.5% conversion
  fiesta-newsletter      156 clicks    14 sign-ups    9.0% conversion

Total This Month:
  Commission Accrued: $487.50
  Payout Pending: (Will be paid April 15)

Active Referrals: 36 merchants (generating ongoing commission)
```

---

## Step 5: Optimize & Best Practices

### A/B Testing Your Links

1. Create 2-3 variations of your landing page CTA
2. Use different referral links for each variant
3. Monitor conversion rates in the dashboard
4. Keep the highest-converting variant

**Example Variations:**
- **Variant A:** "Sign Up for Stripe"
- **Variant B:** "Get Stripe's Payment Platform"
- **Variant C:** "Start Accepting Payments Now"

Track which drives highest conversion rate.

### Content Strategy

**High-Conversion Topics:**
- "How to accept payments with Stripe" ← Include your referral link
- "Stripe vs PayPal: which is better?" ← Comparison with affiliate link
- "Setting up your first payment processor" ← Step-by-step with link
- "Building a SaaS: payments, taxes, banking" ← Real advice + link

**Do:**
- ✅ Link naturally in helpful content
- ✅ Disclose every time
- ✅ Focus on user benefit first
- ✅ Share genuine reviews/tutorials

**Don't:**
- ❌ Spam affiliate links everywhere
- ❌ Hide disclosures
- ❌ Promote only for commission
- ❌ Use misleading anchor text

### Email Campaigns

**Newsletter Mention Example:**

```
---

💳 Recommendation: If you're building a product and need to accept payments, 
we highly recommend Stripe (that's what we use for Fiesta). 

You can sign up here: [stripe.com/partners/affiliate link]

We earn a small commission if you sign up via our link — thanks for supporting us! 
Stripe's pricing is identical whether you sign up directly or through us.

---
```

### Social Media Posts

**Twitter/X Example:**

```
Just finished integrating Stripe for our payment processing. 
Took literally 5 minutes. If you're building something that needs payments, 
I highly recommend it.

(We earn a small commission if you sign up via our link 👇 no extra cost to you!)

[link]
```

---

## Troubleshooting

| Issue | Solution |
|---|---|
| **Link not generating** | Ensure you're logged in and affiliate program is "Active" |
| **No conversions showing** | Check that disclosure is clear; users may be hesitant if hidden |
| **Commissions not accruing** | Referral customer must actually process payments; takes 24-48h to reflect |
| **Payout delayed** | Minimum threshold not met (~$100); wait for next month or more referrals |

---

## Next Steps

1. ✅ Enroll in Stripe Affiliate Program (Step 1)
2. ✅ Generate referral links (Step 2)
3. ✅ Add to landing page with clear disclosure (Step 3)
4. ✅ Start monitoring dashboard weekly (Step 4)
5. ✅ Optimize based on conversion rates (Step 5)

**Expected Timeline to First Payout:**
- Day 1-3: Referral sign-ups arrive
- Day 4-30: Commissions accrue as they process payments
- Day 30-45: First payout (typically mid-month following activity month)

**Revenue Impact:** See COMBINED_REVENUE_CALCULATOR.md for projections.
