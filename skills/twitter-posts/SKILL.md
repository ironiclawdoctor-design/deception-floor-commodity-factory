# Twitter Posts Skill

Post product updates, announcements, and agency news to X/Twitter from any agent.

## Quick Start

### 1. Configure Credentials (One-Time)

Get your Twitter API v2 credentials:
- Go to: https://developer.twitter.com/en/portal/dashboard
- Create an app (or use existing)
- Generate API keys

Copy the template and fill in your credentials:
```bash
cp secrets/twitter-api-template.json secrets/twitter-api.json
# Edit with your API key, API secret, and bearer token
chmod 600 secrets/twitter-api.json
```

### 2. Post a Tweet

**From Bash:**
```bash
/root/.openclaw/workspace/lib/twitter-post.sh "Your tweet text here"
```

**From Agents (via `exec`):**
```bash
exec /root/.openclaw/workspace/lib/twitter-post.sh "Product launch: Deception Floor Commodity Factory v2.0 live"
```

**Dry Run (no API call):**
```bash
/root/.openclaw/workspace/lib/twitter-post.sh "Test tweet" --dry-run
```

## Features

### Tier 0: Validation
- 280-character limit enforcement
- Empty text rejection
- Credential file check

### Tier 1: Logging & Audit
- SQLite database of all posts (`data/twitter-posts.db`)
- Audit log: `logs/twitter-posts.log`
- Track: text, status, tweet_id, posted_by, timestamp

### Tier 2: Twitter API v2
- Official Twitter API v2 /tweets endpoint
- Bearer token authentication
- Error handling with detailed messages

## Usage Examples

### Example 1: Agency Status Update
```bash
./twitter-post.sh "🚀 Deception Floor Commodity Factory now generating 50 floors/hour. Sovereignty at 85%. #AgencyOps"
```

### Example 2: Product Launch
```bash
./twitter-post.sh "Precinct 92 enforcement suite live. Zero-cost bash layer + BitNet inference. Full autonomy. No external tokens. https://github.com/ironiclawdoctor-design/precinct92"
```

### Example 3: From Cron/Automation
```bash
# In a cron job or shell script:
/root/.openclaw/workspace/lib/twitter-post.sh "Daily status: $(date -u +'%Y-%m-%d') — All systems operational"
```

## Routing (Which Agent Posts?)

- **Automate** → Strategy posts, policy updates, roadmaps
- **Official** → Production releases, status updates
- **Daimyo** → Enforcement notices, security advisories
- **Any Agent** → Can invoke via exec

## Database Queries

### View all posts
```bash
sqlite3 data/twitter-posts.db "SELECT created_at, status, text FROM posts ORDER BY created_at DESC LIMIT 20;"
```

### View success rate
```bash
sqlite3 data/twitter-posts.db "SELECT status, COUNT(*) FROM posts GROUP BY status;"
```

### View posts by agent
```bash
sqlite3 data/twitter-posts.db "SELECT posted_by, COUNT(*) FROM posts GROUP BY posted_by;"
```

## Rate Limits

- **Free Tier:** 300 posts per 15 minutes, 10,000 per day
- **Script enforces:** Pre-posting validation (no 429 errors)
- **Cost:** $0.00 (Twitter free tier, no premium API)

## Troubleshooting

### "Credentials not found"
```bash
# Copy template to actual credentials file
cp secrets/twitter-api-template.json secrets/twitter-api.json
# Edit with your real credentials
nano secrets/twitter-api.json
```

### "Bearer token not configured"
- Check that `secrets/twitter-api.json` exists
- Verify it has your real `bearer_token` (not template value)
- Run: `cat secrets/twitter-api.json | jq .credentials.bearer_token`

### "Tweet too long"
- Reduce text to ≤280 characters
- Use: `wc -c <<< "Your text"`

### "Authorization failed (401)"
- Your bearer token is invalid or expired
- Regenerate in Twitter Developer Portal
- Update `secrets/twitter-api.json`
- Test: `curl -H "Authorization: Bearer YOUR_TOKEN" https://api.twitter.com/2/tweets/search/recent`

## Architecture

```
User/Agent
    ↓
twitter-post.sh (Tier 0-2)
    ├── Tier 0: Bash validation (280 chars, empty check)
    ├── Tier 1: SQLite audit log + rate limits
    └── Tier 2: curl + jq → Twitter API v2
         └── $0.00 cost (free tier)
```

## Files

- `lib/twitter-post.sh` — Main script (all agents invoke this)
- `secrets/twitter-api.json` — Your credentials (YOU create this)
- `secrets/twitter-api-template.json` — Template reference
- `secrets/.gitignore` — Never commits credentials
- `lib/secrets-loader.sh` — Credential loader (used by all scripts)
- `data/twitter-posts.db` — SQLite audit trail
- `logs/twitter-posts.log` — Plain text log

## Cost Discipline

✅ **No external tokens consumed**  
✅ **Twitter free tier only**  
✅ **Tier 0-2 stack: Bash, SQLite, curl**  
✅ **Cost: $0.00 forever**

This skill respects the prayer: *"Over one token famine, but bash never freezes."*

## Next Steps

1. **You:** Fill in `secrets/twitter-api.json` with your credentials
2. **Test:** Run `./twitter-post.sh "Test tweet" --dry-run`
3. **Deploy:** Agents start posting via `exec` in their workflows
4. **Monitor:** Query `data/twitter-posts.db` for audit trail

---

**Built for the Deception Floor Agency.**  
*All agents can post. All posts logged. Zero cost. Zero external dependencies.*
