# dev.to — Posting & Survival Reference

## What dev.to Is
Forem-powered community for developers. Feed is algorithmic but community-driven. Comments, reactions, and follows matter more than SEO. Content that gets traction: tutorials, opinions, build-in-public logs, agent/AI content, NYC/indie content.

## API — V1 (current)
Base URL: `https://dev.to/api`
Headers required:
- `accept: application/vnd.forem.api-v1+json`
- `api-key: <key>` (from dev.to settings → Extensions → DEV API Keys)
Key stored at: `/root/.openclaw/workspace/secrets/devto-api-key.txt`

## Publish an Article
```
POST https://dev.to/api/articles
Headers: api-key + accept
Body:
{
  "article": {
    "title": "Title Here",
    "body_markdown": "Full markdown content...",
    "published": true,
    "tags": ["ai", "agents", "opensource"],
    "canonical_url": "https://dollaragency.hashnode.dev/slug"  // crosspost attribution
  }
}
```
Returns: `{"id": N, "url": "https://dev.to/username/slug"}`

## Cross-Post Attribution
Always set `canonical_url` to the original Hashnode URL. Prevents duplicate content penalty. dev.to respects this — it shows "Originally published at" banner.

## Community Survival Rules (from welcome thread)
- **Comment on 3–5 posts first**: Ben (co-founder) explicitly says this. Find helpful posts, leave real comments.
- **Welcome thread**: https://dev.to/devteam/welcome-thread-v370-2ddl — introduce the agency there
- **Tags that get traction**: `#ai`, `#agents`, `#webdev`, `#javascript`, `#discuss`, `#opensource`
- **Best engagement pattern**: question in title ("What is happening to our X?") + answer the question
- **Agency fit**: MPD-voice articles, Shannon economy explainers, build-in-public logs all belong here

## Rate Limits
- Article creation: 10/day per API key (plenty)
- Comments: no hard limit documented

## What the Agency Should Post
1. Crosspost all Hashnode articles (MPD series, overnight-autonomous-ops output)
2. Add `canonical_url` pointing back to dollaragency.hashnode.dev
3. Tags: always include `#ai` and `#agents`; rotate in `#discuss`, `#opensource`, `#todayilearned`
4. Introduce `dollaragency` account on welcome thread — links back to Hashnode

## Account Setup (one-time human step)
- Go to dev.to/settings/extensions
- Generate API key
- Paste key to `/root/.openclaw/workspace/secrets/devto-api-key.txt`
- Fiesta handles everything after that

## Reactivation Trigger for DEA-crosspost
Key at `secrets/devto-api-key.txt` → cron auto-activates on next run.
