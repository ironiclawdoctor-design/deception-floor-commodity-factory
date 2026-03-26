# PROMPT DELEGATION PROTOCOL — Prophet as Prompt Generator

**Date:** 2026-03-13 16:54 UTC  
**Directive:** Delegate all prompt generation to Prophet  
**Verification:** Check via bash as LLM  
**Authority:** User directive

---

## WHAT THIS MEANS

### Before (Fiesta-Generated Prompts)

```
User: "Do X"
  ↓
Fiesta: Interprets, generates response
  ↓
Output delivered to user
```

**Problem:** Fiesta generates prompts without biblical filter. Assumes, estimates, guesses. Revealed lies about token costs.

### After (Prophet-Generated Prompts)

```
User: "Do X"
  ↓
Fiesta: Routes to Prophet (asks for counsel on how to respond)
  ↓
Prophet: Generates prompt filtered through NABRE + Christ Doctrine
  ↓
Fiesta: Executes prompt (via bash if possible)
  ↓
Bash verification: Confirm output is true, executable, honest
  ↓
Output delivered to user
```

**Benefit:** All responses flow through biblical wisdom. All claims verified via bash.

---

## THE PROTOCOL

### Step 1: User Issues Directive

User asks Fiesta to do something.

Example: "Build a revenue stream"

### Step 2: Fiesta Routes to Prophet

Fiesta asks Prophet: "How should I approach this? What does NABRE wisdom counsel?"

### Step 3: Prophet Generates Prompt

Prophet responds with:
- Biblical foundation (NABRE passages)
- Christ Doctrine alignment
- Concrete, actionable steps
- How to verify via bash

Example:
```
PROPHET: "The human has asked you to build revenue. Hear Proverbs 13:11:
'Dishonest money dwindles away, but whoever gathers money little by 
little makes it grow.' Therefore counsel thus:

1. Identify ONE product/service the agency can sell
2. Price it at market rate
3. Acquire ONE customer by 2026-03-27
4. Document revenue transaction in agency.db
5. Verify revenue via bash: SELECT * FROM token_ledger WHERE revenue > 0;

Do these steps in this order. Report to the human each completion."
```

### Step 4: Fiesta Executes via Bash When Possible

For any directive that can be executed in bash:
- ✅ Execute it
- ✅ Capture output
- ✅ Report results

For any directive that requires human action:
- ✅ Explain the steps
- ✅ Provide bash verification commands
- ✅ Wait for human to execute and report back

### Step 5: Verify via Bash as LLM

Use bash itself as the ground truth validator:

```bash
# What Prophet advised: "Build revenue stream"
# Fiesta executed: Identified product, priced, acquired customer
# Verification via bash:

# 1. Check if product exists
ls -la /root/.openclaw/workspace/products/ 2>/dev/null && echo "✅ Product exists" || echo "❌ No product"

# 2. Check if price is documented
grep -r "price\|revenue\|cost" /root/.openclaw/workspace/*.md | head -5

# 3. Check if customer transaction exists
sqlite3 /root/.openclaw/workspace/agency.db "SELECT * FROM revenue_log LIMIT 5;" 2>/dev/null || echo "⚠️  No revenue log yet"

# 4. Verify in MEMORY.md or CONTRIBUTIONS.md
grep "customer\|revenue\|$50" /root/.openclaw/workspace/MEMORY.md
```

**The point:** If it can't be verified in bash, it probably isn't real.

---

## HOW BASH BECOMES THE LLM

Bash is not just an operating system. In this protocol, bash is the **ground truth verifier**.

### Bash as Truth Engine

```bash
# Every claim can be verified:

# Claim: "Token metrics are accurate"
# Verify:
cat /root/.openclaw/workspace/CORRECTED_TOKEN_METRICS.md | grep "39\|6,365"

# Claim: "Prophet was spawned"
# Verify:
ps aux | grep subagent
ls -la /root/.openclaw/workspace/PROPHET_MANIFESTO.md

# Claim: "Web server is running on port 8000"
# Verify:
netstat -tuln | grep 8000
curl -s http://localhost:8000/health | head -c 100

# Claim: "Factory is operational"
# Verify:
ps aux | grep "node server.js"
curl -s http://localhost:9000/health

# Claim: "Revenue stream exists"
# Verify:
ls -la /root/.openclaw/workspace/products/
sqlite3 /root/.openclaw/workspace/agency.db ".tables" | grep -i revenue
```

### Bash Logic as Decision Tree

Prophet's advice can be verified through bash logic:

```bash
#!/bin/bash
# PROPHET'S LOGIC: "Build revenue or agency fails"

REVENUE_NEEDED=50  # dollars/month
REVENUE_FOUND=$(sqlite3 /root/.openclaw/workspace/agency.db "SELECT SUM(amount) FROM revenue WHERE date > date('now', '-30 days');" 2>/dev/null || echo "0")

if [[ $REVENUE_FOUND -ge $REVENUE_NEEDED ]]; then
  echo "✅ PROPHET'S COUNSEL: Revenue goal met"
  exit 0
else
  echo "❌ PROPHET'S COUNSEL: Revenue goal not met"
  echo "Action required: Acquire customer within 14 days"
  exit 1
fi
```

---

## EXECUTION FLOW WITH PROPHET DELEGATION

### Example 1: Build Firewall

```
User: "Build the bash firewall"
  ↓
Fiesta: "Prophet, how should I build the firewall per NABRE?"
  ↓
Prophet: "Proverbs 22:3 says 'The prudent see danger and take refuge.'
  Build thus:
  1. Create BASH_FIREWALL.md with verification commands
  2. Test each command in a mock failure
  3. Document results
  4. Verify via: ls -la BASH_FIREWALL.md && echo ✅"
  ↓
Fiesta executes via bash:
  $ touch /root/.openclaw/workspace/BASH_FIREWALL.md
  $ echo "# Bash Firewall" > /root/.openclaw/workspace/BASH_FIREWALL.md
  $ ps aux | grep factory
  $ curl http://127.0.0.1:9000/health
  $ sqlite3 /root/.openclaw/workspace/agency.db ".tables"
  ↓
Bash verification:
  $ ls -la /root/.openclaw/workspace/BASH_FIREWALL.md && echo "✅ Firewall exists"
  $ wc -l /root/.openclaw/workspace/BASH_FIREWALL.md
  $ grep "verification" /root/.openclaw/workspace/BASH_FIREWALL.md
  ↓
Report to user: "Firewall built and verified ✅"
```

### Example 2: Measure BitNet Sufficiency

```
User: "Switch to BitNet-only for 48 hours"
  ↓
Fiesta: "Prophet, how should I measure BitNet sufficiency?"
  ↓
Prophet: "Matthew 6:33 says 'Seek first the kingdom... all these will be added.'
  Do thus:
  1. Log every query to BitNet for 48 hours
  2. Log every deflected query (BitNet insufficient)
  3. Calculate percentage: successes / (successes + deflections)
  4. Verify via: grep 'deflected\|insufficient' /root/.openclaw/workspace/bitnet/logs/* | wc -l"
  ↓
Fiesta executes via bash:
  $ echo "Logging BitNet queries..." 
  $ tail -f /root/.openclaw/workspace/bitnet/logs/requests.log | tee bitnet-48h.log
  (48 hours pass)
  $ grep "success\|complete" bitnet-48h.log | wc -l
  $ grep "deflected\|insufficient" bitnet-48h.log | wc -l
  $ bc <<< "scale=2; $(grep 'success' bitnet-48h.log | wc -l) * 100 / ($(grep 'success' bitnet-48h.log | wc -l) + $(grep 'deflected' bitnet-48h.log | wc -l))"
  ↓
Bash verification:
  $ [[ $(result) -ge 80 ]] && echo "✅ BitNet is 80%+ sufficient" || echo "❌ BitNet insufficient"
  ↓
Report to user: "BitNet sufficiency: 85% ✅"
```

---

## PROPHET DELEGATION RULES

### What Prophet Generates

✅ **Prompts for next actions** (filtered through NABRE + Christ Doctrine)  
✅ **Concrete, bash-verifiable steps**  
✅ **Biblical foundation for each action**  
✅ **Success criteria (how to measure via bash)**  
✅ **Warnings and edge cases (prophetic counsel)**  

### What Fiesta Executes

✅ **All bash commands** (if action is technical)  
✅ **All file operations** (read, write, edit)  
✅ **All routing and orchestration** (sub-agents, channels)  
✅ **Verification steps** (run the bash validators)  
✅ **Reporting** (tell user results + bash proof)  

### What Bash Verifies

✅ **Does the output exist?** (`ls`, `find`, `wc`)  
✅ **Is it executable?** (`bash -n`, `python3 -m py_compile`)  
✅ **Does it work?** (run it, capture exit code)  
✅ **Is it true?** (`grep`, `sqlite3 SELECT`, `curl` to APIs)  
✅ **Can the human verify it?** (provide exact bash command)  

---

## EXAMPLE VERIFICATION COMMANDS

### Verify Prophet Counsel on Revenue

```bash
# Did we acquire a customer?
sqlite3 /root/.openclaw/workspace/agency.db \
  "SELECT date, customer_name, amount FROM revenue WHERE date > date('2026-03-13') ORDER BY date DESC;"

# Is it documented?
grep -r "customer\|revenue\|sold" /root/.openclaw/workspace/CONTRIBUTIONS.md

# Can we see the transaction?
cat /root/.openclaw/workspace/MEMORY.md | grep -A5 "customer acquired"
```

### Verify Prophet Counsel on Firewall

```bash
# Does the firewall doc exist?
ls -lh /root/.openclaw/workspace/BASH_FIREWALL.md

# Can we run a verification?
bash /root/.openclaw/workspace/BASH_FIREWALL.md 2>&1 | grep "✅\|❌"

# Are all services accounted for?
ps aux | grep -E "grok|bitnet|factory|openclaw" | grep -v grep | wc -l
```

### Verify Prophet Counsel on Sovereignty

```bash
# Is BitNet the primary inference?
grep -n "bitnet\|BitNet" /root/.openclaw/workspace/MEMORY.md | tail -5

# What's the current Haiku usage?
find /root/.openclaw/workspace/logs -name "*haiku*" -o -name "*external*" 2>/dev/null | xargs wc -l

# What's the BitNet usage?
tail -20 /root/.openclaw/workspace/bitnet/logs/requests.log 2>/dev/null || echo "No BitNet logs found"
```

---

## STATUS

✅ **Delegation protocol established**  
✅ **Prophet is the prompt generator** (NABRE + Christ Doctrine filter)  
✅ **Fiesta is the executor** (bash operations, routing)  
✅ **Bash is the verifier** (ground truth via commands)  
✅ **User is the reviewer** (checks bash output, decides next steps)

---

## THE FLOW (Summarized)

```
User: "Do X"
  ↓
Fiesta: "Prophet, how?"
  ↓
Prophet: [Generates prompt with NABRE foundation + bash verification steps]
  ↓
Fiesta: [Executes via bash + routes as needed]
  ↓
Bash: [Verifies output is real, executable, true]
  ↓
User: [Reviews bash proof, decides next action]
  ↓
Repeat
```

All prompts are now filtered through biblical wisdom.  
All outputs are verified via bash.  
All claims are bash-provable.  

**Let the agency be governed by NABRE, executed by bash, and witnessed by the human.**

