# Stripe Products Setup — Create All Tiers

## Prerequisites
- Stripe account created (live mode)
- User authenticated (you)

## Products to Create (In Order)

### Product 1: Fiesta Supporter Tier

**In Stripe Dashboard:**
1. Go: https://dashboard.stripe.com/products
2. Click: "+ New"
3. Name: `Fiesta Supporter`
4. Description: `Priority newsletter, monthly impact reports, supporter community`

**Add Pricing:**
- Monthly: $5/month (recurring)
- Annual: $50/year (recurring, save 17%)

**Advanced:**
- Billing period: Monthly or Annual
- Enable: Recurring

---

### Product 2: Fiesta Partner Tier

**In Stripe Dashboard:**
1. Create new product
2. Name: `Fiesta Partner`
3. Description: `Direct agent access (1 request/month), custom reports, quarterly calls with Fiesta`

**Add Pricing:**
- Monthly: $25/month (recurring)
- Annual: $250/year (recurring)

---

### Product 3: Fiesta Collaborator Tier

**In Stripe Dashboard:**
1. Create new product
2. Name: `Fiesta Collaborator`
3. Description: `Dedicated agent, unlimited requests, weekly syncs, governance vote, API access`

**Add Pricing:**
- Monthly: $100/month (recurring)
- Annual: $1000/year (recurring)

---

### Product 4: Fiesta Founder Tier

**In Stripe Dashboard:**
1. Create new product
2. Name: `Fiesta Founder`
3. Description: `Agent team (3-5 dedicated), unlimited access, board seat, strategic partnership`

**Add Pricing:**
- Monthly: $500/month (recurring)
- Annual: $5000/year (recurring)

---

### Product 5: One-Time Donation

**In Stripe Dashboard:**
1. Create new product
2. Name: `Fiesta Donation (One-Time)`
3. Description: `Support open AI infrastructure with a one-time contribution`

**Add Pricing (Standard Prices):**
- $5 (one-time)
- $25 (one-time)
- $50 (one-time)
- $100 (one-time)
- $500 (one-time)
- Custom amount (manual entry)

---

## After Creating Products

### Get Product IDs
Stripe automatically generates:
- `prod_xxx...` (Product ID)
- `price_xxx...` (Price ID for each plan)

**Where to find them:**
1. Dashboard → Products
2. Click each product
3. Copy Product ID and Price IDs

### Update Landing Page

Replace hardcoded Stripe links with actual price IDs:

```javascript
// Option A: Direct link (simple)
const tiers = {
  supporter_monthly: 'https://checkout.stripe.com/pay/price_xxx...',
  partner_monthly: 'https://checkout.stripe.com/pay/price_yyy...',
  collaborator_monthly: 'https://checkout.stripe.com/pay/price_zzz...',
  founder_monthly: 'https://checkout.stripe.com/pay/price_www...',
};

// Option B: Embedded form (advanced)
// Requires Stripe.js initialization
```

### Configure Webhook

1. Go: Stripe Dashboard → Developers → Webhooks
2. Add endpoint: `http://127.0.0.1:9003/webhook` (or ngrok URL)
3. Select events:
   - `customer.subscription.created`
   - `customer.subscription.updated`
   - `customer.subscription.deleted`
   - `charge.succeeded`
   - `charge.failed`
4. Copy signing secret → add to backend config

---

## Testing

### Test Subscriptions

Use Stripe test mode:
- Test card: `4242 4242 4242 4242`
- Expiry: Any future date (12/26)
- CVC: Any 3 digits (123)

### Test Webhook

Use Stripe CLI (if available):
```bash
stripe listen --forward-to localhost:9003/webhook
# Returns webhook signing secret
```

Then make test charge:
```bash
curl https://api.stripe.com/v1/charges \
  -u sk_test_xxx: \
  -d amount=5000 \
  -d currency=usd \
  -d source=tok_visa
```

---

## Checklist

- [ ] Created 5 products in Stripe
- [ ] Recorded all Product IDs
- [ ] Recorded all Price IDs
- [ ] Updated landing page with live price IDs
- [ ] Configured webhook endpoint
- [ ] Tested with test card (4242...)
- [ ] Verified webhook fires on charge
- [ ] Set up email on successful subscription

---

## Files to Update After Setup

1. **Landing Page:** `www/landing.html`
   - Add tier cards with pricing
   - Link to Stripe checkout (using price IDs)

2. **Backend:** `projects/entropy-economy/src/server.js`
   - Add webhook handler for subscriptions
   - Track subscriber tier in database
   - Send welcome email on subscription.created

3. **Database:** Add `subscriptions` table
   ```sql
   CREATE TABLE subscriptions (
     id TEXT PRIMARY KEY,
     customer_email TEXT,
     tier TEXT,  -- 'supporter', 'partner', 'collaborator', 'founder'
     status TEXT, -- 'active', 'past_due', 'canceled'
     amount_monthly INT,
     started_at TIMESTAMP,
     renewed_at TIMESTAMP
   );
   ```

---

*Setup instructions generated 2026-03-19 15:40 UTC*
