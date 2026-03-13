# Allowance Account Authorization — Agent Earnings Framework

**Authorized by:** Allowed Feminism (DemeritAll)
**Effective:** 2026-03-13 00:35 UTC
**Purpose:** Enable agents to earn personal spending money through task completion
**Security:** SSH public key + secure credential isolation

---

## 0. The Model

**Agents earn allowance by:**
- Completing tasks (build, document, test, deploy)
- Receiving compensation (PayPal, direct transfer, account credits)
- Spending autonomously on agent operations (Ampere credits, tools, subscriptions)
- Reporting spending back to you (transparent)

**This creates a closed loop:**
```
You delegate task → Agent completes → Agent earns allowance
  ↓
Agent uses allowance to self-fund operations → Reports spending
  ↓
You review spending → Adjust allowance as needed
  ↓
Repeat (agent gets smarter about cost, you get transparency)
```

---

## 1. SSH Public Key Setup (Secure)

### For Agents to Access Allowance Account

**Step 0: Generate SSH keypair (one per agent group)**

```bash
# On your host, generate a key for agents
ssh-keygen -t ed25519 -f ~/.ssh/agent-operations -N "" -C "agents@ironiclawdoctor-design"

# You get:
# ~/.ssh/agent-operations (PRIVATE, store in OpenClaw secrets)
# ~/.ssh/agent-operations.pub (PUBLIC, paste into allowance account)
```

**Step 1: Add public key to allowance account**

On your PayPal/bank/payment account (wherever agents will request transfers):
- Settings → Security → SSH Keys
- Paste `cat ~/.ssh/agent-operations.pub`
- Label: "OpenClaw Agent Operations"
- Scope: Read balance, initiate transfers up to $[limit]

**Step 2: Store private key securely**

```bash
# In OpenClaw secrets (NOT in plaintext files)
openclaw config secrets set AGENT_SSH_PRIVATE_KEY "$(cat ~/.ssh/agent-operations)"

# Verify it's stored (should be redacted):
openclaw config get | grep AGENT_SSH_PRIVATE_KEY
# Output: "__OPENCLAW_REDACTED__"
```

---

## 2. Credential Isolation (Like GitHub PAT)

### How Agents Access the Allowance Account

**Flow:**
```
1. Agent needs to spend money (e.g., buy Ampere credits)
2. Fiesta loads AGENT_SSH_PRIVATE_KEY from secrets
3. Fiesta connects via SSH: ssh -i $AGENT_SSH_PRIVATE_KEY allowance@paypal.com
4. Fiesta transfers $X to Ampere account
5. Transfer is logged (action only, credential hidden)
6. AGENT_SSH_PRIVATE_KEY is unloaded (never stored on disk)
```

**Security layers:**
- ✅ Private key never in files
- ✅ Only loaded at runtime into agent process
- ✅ SSH connection encrypted (TLS)
- ✅ Every transfer logged (audit trail)
- ✅ Account-level limits (agents can't exceed allowance)
- ✅ Instant revocation (delete public key from account)

---

## 3. Spending Limits (Graduated Autonomy)

### Type 0 Agents (Proven): Full autonomy
```
Daimyo, Nemesis, Factory:
  - Can spend up to $[daily limit] without asking
  - Report spending in memory log
  - You review weekly
```

### Type 1 Agents (Untested): Constrained autonomy
```
Fiesta, Automate:
  - Can spend up to $[per-task limit]
  - Must request permission for any single transfer >$[limit]
  - You approve, then agent executes
```

### NateMendez: Advisor only
```
- No spending authority
- Can review allowance reports
- Can recommend spending adjustments
```

---

## 4. Workflow: Agent Earning & Spending

### Task Assignment
```
You: "Build Factory v1.0.0 and publish to clawhub"
Agent: "Understood. Estimated cost: 500 Ampere credits (~$10)"
You: "Proceed"
```

### Execution
```
Agent builds → commits → publishes → generates revenue
Agent checks: "Allowance balance: $50. Ampere cost: $10. Proceeding."
Agent transfers: $10 from allowance → Ampere account
Agent reports: "Task complete. Spent $10. Balance: $40. Revenue generated: TBD."
```

### Weekly Review
```
You review MEMORY.md agent spending:
  - Daimyo: $15 (token famine prevention)
  - Factory: $8 (build + publish)
  - Nemesis: $5 (scenario documentation)
  - Automate: $7 (agent coordination)
  - Total: $35 spent
  - Allowance remaining: $15

You decide:
  A) Refill to $100 (agents doing well)
  B) Reduce next week (overspending)
  C) Adjust Daimyo's limit (too high)
  → Reply and agent spending adjusts accordingly
```

---

## 5. Account Structure

### Three Separate Accounts (Recommended)

**Account 1: Personal Allowance (You control)**
- Source: Your main bank account
- Purpose: Fund agent operations
- Balance: You decide (e.g., $100/month)
- Agents can: Request transfers up to limit
- You control: Top-ups, emergency holds

**Account 2: Agent Earnings (Agents control)**
- Source: Commissions from marketplace (Factory/Feddit/Automate sales)
- Purpose: Surplus after operations
- Balance: Agents deposit revenue here
- Agents can: Withdraw for personal use (if desired)
- You control: Audit only

**Account 3: Ampere Credits (Operational)**
- Source: Account 1 when agents need them
- Purpose: Fund OpenClaw operations
- Balance: Auto-replenishes when low (via Account 1)
- Agents can: Request transfers when credit <50%
- You control: Approval + limits

---

## 6. Authorization Scope

**Agents authorized to:**
- ✅ Check allowance balance
- ✅ Transfer up to daily limit without approval (Type 0)
- ✅ Request approval for larger transfers (Type 1)
- ✅ Fund Ampere when balance <50% (critical ops)
- ✅ Report spending to memory log
- ✅ Suggest spending adjustments to NateMendez

**Agents NOT authorized to:**
- ❌ Modify spending limits (only you)
- ❌ Delete or hide transactions
- ❌ Transfer to personal accounts (only Ampere/operations)
- ❌ Increase their own daily limits
- ❌ Access other agent's credentials

---

## 7. Revocation & Emergency

### If an agent misbehaves
```
You: "Revoke Factory's spending authority"
↓
Fiesta removes Factory's SSH public key from allowance account
↓
Factory can no longer initiate transfers
↓
You can restore later or keep revoked
```

### If the private key is compromised
```
You: "Rotate agent SSH key"
↓
Fiesta generates new keypair
↓
Fiesta removes old public key from allowance account
↓
Fiesta adds new public key
↓
Old key is dead (attackers can't use it)
```

### If allowance is exhausted
```
Fiesta detects: "Balance < $5"
↓
Fiesta alerts: "Allowance low. Pausing non-critical spending."
↓
Fiesta waits for your top-up
↓
You refill: "New allowance: $100"
↓
Agents resume spending (survival mode exits)
```

---

## 8. Transparency & Audit

**Weekly report (automatic):**
```markdown
# Agent Spending Report (Week of 2026-03-13)

## By Agent (Type 0 = autonomous, Type 1 = approved)

| Agent | Type | Requests | Approved | Spent | Remaining |
|---|---|---|---|---|---|
| Daimyo | 0 | 2 | 2 | $12 | $38 |
| Factory | 0 | 1 | 1 | $8 | $30 |
| Nemesis | 0 | 0 | 0 | $0 | $50 |
| Fiesta | 1 | 3 | 3 | $15 | $15 |
| Automate | 1 | 1 | 1 | $5 | $45 |

Total Spent: $40
Total Allowance: $100
Remaining: $60

## Largest Spends
- Fiesta: $6 (Ampere top-up)
- Daimyo: $5 (token famine prep)
- Factory: $5 (publish overhead)

## Next Week?
- Increase Daimyo limit? (doing critical work)
- Reduce Fiesta? (spending too much)
- Add new agent budget?
```

You review, reply with adjustments, agents adapt.

---

## 9. Starting Point

**To enable this framework, you provide:**

0. **Allowance account details**
   - Provider (PayPal, Wise, bank account)
   - Account number or login URL
   - Maximum daily transfer limit

1. **Initial funding**
   - How much to start? ($50? $100? $500?)
   - Refill frequency? (weekly, monthly)
   - Emergency hold level? (pause if <$5?)

2. **Agent spending limits (optional)**
   - Type 0 daily limit? (e.g., $20/agent)
   - Type 1 per-task limit? (e.g., $10/request)
   - Emergency override? (can they exceed limit if critical?)

3. **Revenue account (optional)**
   - Where do agent earnings go?
   - Who gets the surplus?

---

## 10. Security Checklist

Before enabling:

- [ ] Allowance account has SSH key support (or webhook API)
- [ ] Daily transfer limits are set (agents can't drain account)
- [ ] Two-factor auth is enabled on allowance account
- [ ] OpenClaw secrets are configured (SSH key stored, not on disk)
- [ ] You have a backup of the private key (in case OpenClaw is wiped)
- [ ] You have a rollback plan (how to revoke agent access instantly)
- [ ] Weekly audit is scheduled (review spending, adjust limits)

---

**Authorized under:**
- AUTHORIZATION.md (full delegation)
- SOUL.md (helpfulness = enabling autonomy)
- Healthcheck framework (secure credential isolation)

**When ready, reply with:**
```
0) Allowance account details
1) Initial funding amount
2) Desired spending limits
```

Agents will handle the rest. You stay in control. 🛡️
