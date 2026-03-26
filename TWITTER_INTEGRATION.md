# Twitter/X Integration — Complete Setup

**Status:** Infrastructure ready for credentials  
**Cost:** $0.00 (Twitter free tier)  
**Doctrine:** Tier 0-2 only, all agents can participate

---

## What's Built

### 1. **Secure Credential Vault** ✅
- `secrets/twitter-api-template.json` — Template file
- `secrets/twitter-api.json` — YOUR credentials (YOU create this)
- `lib/secrets-loader.sh` — Safe credential loader (bash)
- `secrets/.gitignore` — Never commits credentials to git

### 2. **Twitter Poster (Tier 0-2)** ✅
- `lib/twitter-post.sh` — Main posting script
  - Tier 0: Bash validation (280 char limit, empty check)
  - Tier 1: SQLite audit logging + rate limits
  - Tier 2: curl + jq → Twitter API v2
- `data/twitter-posts.db` — SQLite audit trail
- `logs/twitter-posts.log` — Plain text log file

### 3. **Agency Orchestrator** ✅
- `lib/agency-twitter-orchestrator.sh` — Multi-agent coordinator
- Separate methods for: Automate, Official, Daimyo branches
- Queue management (JSON-based)
- Status reporting
- Cron integration

### 4. **Skill File** ✅
- `skills/twitter-posts/SKILL.md` — Full documentation
- Examples for all three branches
- Troubleshooting guide
- Database query templates

---

## Next Step: Add Your Credentials

### Get Twitter API v2 Credentials

1. **Go to:** https://developer.twitter.com/en/portal/dashboard
2. **Sign in** with your X/Twitter account
3. **Create or select an app**
4. **Go to Keys & Tokens tab**
5. **Generate (or copy) these values:**
   - API Key (consumer_key)
   - API Secret (consumer_secret)
   - Bearer Token (OAuth 2.0)

### Create Actual Credential File

```bash
# From your workspace:
cp secrets/twitter-api-template.json secrets/twitter-api.json

# Edit with your credentials (nano, vim, or editor of choice):
nano secrets/twitter-api.json
```

Fill in these fields with your real values:
```json
{
  "credentials": {
    "api_key": "YOUR_REAL_API_KEY_HERE",
    "api_secret": "YOUR_REAL_API_SECRET_HERE",
    "bearer_token": "YOUR_REAL_BEARER_TOKEN_HERE"
  }
}
```

### Secure the File

```bash
chmod 600 secrets/twitter-api.json
```

---

## Test the Setup

### Test 1: Dry Run (No API Call)
```bash
/root/.openclaw/workspace/lib/twitter-post.sh "Test tweet" --dry-run
```

**Expected output:**
```
═══════════════════════════════════════════
  Twitter Post Agent (Tier 0-2, Cost: $0.00)
═══════════════════════════════════════════

Tweet (11 chars):
  Test tweet

📋 [DRY RUN] Would POST to Twitter:
{
  "text": "Test tweet"
}
```

### Test 2: Real Post (After Credentials Added)
```bash
/root/.openclaw/workspace/lib/twitter-post.sh "🚀 Agency infrastructure live. Deception Floor Commodity Factory v2.1 — zero cost, full autonomy. #AgencyOps"
```

**Expected output:**
```
✓ Posted! Tweet ID: 1234567890123456789
  View: https://twitter.com/i/web/status/1234567890123456789
```

---

## Use Cases by Agent

### Automate Branch (Strategy & Policy)
```bash
# Queue strategy tweets
/root/.openclaw/workspace/lib/agency-twitter-orchestrator.sh --automate

# Custom:
/root/.openclaw/workspace/lib/twitter-post.sh "📋 New agency policy: Tier routing enforced. All tokens routed through BitNet first."
```

### Official Branch (Production & Releases)
```bash
# Queue release tweets
/root/.openclaw/workspace/lib/agency-twitter-orchestrator.sh --official

# Custom:
/root/.openclaw/workspace/lib/twitter-post.sh "✅ Production release: Commodity Factory now 100% autonomous. 50 floors/hour, $0 cost."
```

### Daimyo Branch (Security & Enforcement)
```bash
# Queue enforcement tweets
/root/.openclaw/workspace/lib/agency-twitter-orchestrator.sh --daimyo

# Custom:
/root/.openclaw/workspace/lib/twitter-post.sh "🔒 Security: All token leaks blocked. Cost control tier enforced. Zero bleed."
```

---

## Monitor & Audit

### View All Posts
```bash
sqlite3 /root/.openclaw/workspace/data/twitter-posts.db \
  "SELECT created_at, status, text FROM posts ORDER BY created_at DESC LIMIT 20;"
```

### View Posts by Agent
```bash
sqlite3 /root/.openclaw/workspace/data/twitter-posts.db \
  "SELECT posted_by, COUNT(*) as count FROM posts GROUP BY posted_by;"
```

### View Success Rate
```bash
sqlite3 /root/.openclaw/workspace/data/twitter-posts.db \
  "SELECT status, COUNT(*) as count FROM posts GROUP BY status;"
```

### View Audit Log
```bash
tail -n 50 /root/.openclaw/workspace/logs/twitter-posts.log
```

---

## Cron Integration (Optional)

### Auto-Post from Cron

Create a cron job to process the queue every 30 minutes:

```bash
# Edit your crontab:
crontab -e

# Add this line:
0,30 * * * * /root/.openclaw/workspace/lib/agency-twitter-orchestrator.sh --schedule >> /root/.openclaw/workspace/logs/twitter-cron.log 2>&1
```

This will:
- Check for queued tweets every 30 minutes
- Post any pending tweets
- Log results to `logs/twitter-cron.log`
- Cost: $0.00 (uses free tier)

---

## Rate Limits

- **Free Tier Limits:**
  - 300 posts per 15 minutes
  - 10,000 posts per day
- **Script Behavior:**
  - Pre-validates before posting (no 429 errors)
  - Logs all attempts (success + failure)
  - Supports retry via cron (queue-based)

---

## Cost Discipline

✅ **Zero external tokens consumed**  
✅ **Twitter free tier only**  
✅ **Tier 0-2 stack: Bash, SQLite, curl, jq**  
✅ **Cost: $0.00 forever**

This respects the prayer: *"Over one token famine, but bash never freezes."*

---

## Architecture Diagram

```
Three Branches
    ├── Automate (Strategy)
    ├── Official (Production)
    └── Daimyo (Enforcement)
         ↓
agency-twitter-orchestrator.sh (Tier 0-2)
    ├── Queue management (JSON)
    ├── Agent routing
    └── Batch posting
         ↓
twitter-post.sh (Main Script)
    ├── Tier 0: Bash validation
    ├── Tier 1: SQLite audit log
    └── Tier 2: curl + jq → Twitter API v2
         ↓
secrets-loader.sh
    └── Safe credential access (600 perms)
         ↓
secrets/twitter-api.json (YOUR CREDENTIALS)
    └── Bearer token authentication
         ↓
https://api.twitter.com/2/tweets
    └── Twitter API v2 endpoint
```

---

## Files

| File | Purpose | Permissions |
|------|---------|-------------|
| `secrets/twitter-api.json` | YOUR credentials | 600 (secret) |
| `secrets/twitter-api-template.json` | Reference template | 600 |
| `secrets/.gitignore` | Prevent credential leaks | - |
| `lib/twitter-post.sh` | Main poster (Tier 0-2) | 755 |
| `lib/agency-twitter-orchestrator.sh` | Multi-agent coordinator | 755 |
| `lib/secrets-loader.sh` | Credential loader | 755 |
| `data/twitter-posts.db` | SQLite audit trail | - |
| `logs/twitter-posts.log` | Plain text log | - |
| `skills/twitter-posts/SKILL.md` | Full documentation | - |

---

## Next: Your Move

1. **Get credentials** from Twitter Developer Portal
2. **Fill in** `secrets/twitter-api.json`
3. **Run test:** `./lib/twitter-post.sh "Test" --dry-run`
4. **Post first tweet:** `./lib/twitter-post.sh "Your announcement here"`
5. **Monitor:** Check database + logs

**All agents can now post. All posts are logged. Cost remains $0.00.**

---

*Built for the Deception Floor Agency.*  
*Infrastructure complete. Awaiting credentials.*
