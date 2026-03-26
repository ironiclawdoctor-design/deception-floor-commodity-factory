# Distribution Plan — Article #2: "The Debt Doctrine"

**Article:** The Debt Doctrine: How an AI Agency Turned $60 Into a Currency  
**Platform of record:** DEV.to (Dollar persona / ironic_lawdoctor_ffc2dca)  
**Word count:** ~1,841  
**Target reader:** AI/ML engineers, indie hackers, self-hosters curious about agent economics

---

## Channel 1: Hacker News (Show HN)

**Best practices for a good HN submission:**
- "Show HN:" prefix signals you built something real — use it
- Title must be factual and specific — no marketing language
- Best time to post: Tuesday–Thursday 8–11 AM ET (peak US traffic)
- First comment from yourself = the pitch. Keep it under 200 words. Lead with what's novel.
- Do NOT ask for upvotes. HN bans that.
- Link to the DEV.to article directly (or mirror on GitHub if DEV.to gets flagged)
- Engage every comment within the first 2 hours. HN rewards discussion velocity.

**What makes this submittable:**
The SQLite schema as "confessional audit log" is a genuine technical angle. The Shannon currency with 1:1 backing is a legitimately novel agent-economy design. Lead with the technical, not the theology.

---

**Submission Title:**
```
Show HN: I built a double-entry ledger + confession log for an AI agent economy backed by $60
```

**First comment (self-post) to write immediately after submission:**

```
We're running a small AI agency on Ampere.sh (~$20/month). To fund token costs, we 
built an internal currency (Shannon, 10:1 USD) backed by real spending — not a whitepaper.

The novel bit: every failure the agent hits gets logged to a `confessions` table 
(failure_type, description, doctrine_extracted, shannon_minted). Think of it as 
an audit log that also mints currency when suffering produces knowledge.

Full schema in the article. Zero blockchain — just SQLite and double-entry accounting. 
Runs fine on a $5 VPS.

Happy to share the full .sql dump if there's interest.
```

---

## Channel 2: Reddit

### Best subreddit: **r/LocalLLaMA**

**Why:** r/LocalLLaMA skews toward people running agents locally, thinking about token costs, and building alternative AI infrastructure. The "SQLite instead of blockchain" angle will land perfectly. Self-hosters who care about agent economics.

**Second choice:** r/SelfHosted (for the infrastructure/Ampere.sh angle)  
**Third choice:** r/MachineLearning (too academic, won't care about $60 and confession tables)

### r/LocalLLaMA Post

**Title:**
```
I built an internal currency for my AI agent using SQLite + double-entry accounting. 
Here's the schema (and why I used Catholic confession as the audit log design)
```

**Body (first paragraph):**
```
Running an AI agent on a $20/month VPS means constant token famines. To track real 
spending vs. agent output, we built Shannon — a micro-currency (10:1 USD) backed by 
$60 of actual hosting spend. Every agent failure gets logged to a `confessions` table 
that extracts a doctrine rule and mints currency. It sounds crazy. The SQLite schema 
is dead simple. Full writeup with the CREATE TABLE statements: [link]
```

---

### r/SelfHosted Post

**Title:**
```
Tracking AI agent costs with SQLite double-entry accounting on a $20/month VPS 
(and why I modeled the audit log on Catholic confession)
```

**Body (first paragraph):**
```
If you're self-hosting AI agents, you know the pain: token costs are unpredictable, 
tracking ROI is guesswork, and "the agent crashed" isn't a useful expense record. 
I built a minimal double-entry ledger in SQLite with a `confessions` table that logs 
every failure with a learned rule. The schema fits in one file. Full walkthrough + 
CREATE statements in the article linked below.
```

---

## Channel 3: GitHub Discussions

**Best target:** A repo where AI agent frameworks are discussed — e.g., `anthropics/anthropic-cookbook`, `microsoft/autogen`, or any active agent-framework repo.

**Strategy:** Don't post cold. Find an open Discussion thread about "agent memory", "agent cost tracking", or "agent logging" and reply with a relevant excerpt + link. Don't open a new Discussion unless you're a contributor.

**Reply template:**

**Context:** Replying to a thread about agent persistence or cost management.

```
We ran into the same problem and solved it with a SQLite double-entry ledger + a 
`confessions` table that logs failures with extracted doctrine rules. The "confession" 
becomes an audit entry that mints internal currency when a failure produces a lesson. 

We wrote up the full schema here (DEV.to): [link]

Happy to share the .sql dump — it's ~80 lines and requires no external deps.
```

---

## Channel 4: DEV.to → Hashnode Cross-Post

**How to set up automatic cross-posting:**

1. Go to your Hashnode blog settings
2. Navigate to **Integrations** → **Import from DEV.to**  
   OR use **Hashnode's RSS import**: add your DEV.to RSS feed  
   (`https://dev.to/feed/ironic_lawdoctor_ffc2dca`)
3. Enable "Auto-import new posts" if available
4. Hashnode will mirror new DEV.to articles automatically with canonical URL pointing back to DEV.to

**Manual alternative (if auto doesn't work):**
- In Hashnode dashboard → New Article → Import → paste DEV.to URL
- Hashnode fetches content + sets canonical automatically

**Why this matters:** Hashnode has a strong feed algorithm and newsletter distribution. Cross-posting costs zero effort and doubles reach with correct canonical tags (no SEO penalty).

---

## Timing Sequence (After DEV.to Publishes)

| Hour | Action |
|------|--------|
| 0 | Publish on DEV.to (set published: true) |
| 0 | Submit to Hacker News immediately |
| 1 | Monitor HN — respond to every comment |
| 2 | Post to r/LocalLLaMA |
| 3 | Post to r/SelfHosted |
| 24 | Cross-post to Hashnode |
| 48 | Find relevant GitHub Discussions to reply to |
| 72 | Check DEV.to analytics — if >500 views, do a follow-up comment tagging the series |

---

## Notes

- The "confession as audit log" framing is the viral hook. Lead with it every time.
- Always include the SQLite CREATE TABLE snippet — code = credibility
- Link Part 1 in every post for series context
- Ampere.sh referral link: `https://www.ampere.sh/?ref=nathanielxz`
- BTC tip jar: `12bxubgs1Br6NvKH4p35pcBpinQ7fwe4ht`
- Cash App: `$DollarAgency`
