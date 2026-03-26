---
name: xai-grok-search
version: 2.0.0
description: Search the web and X (Twitter) using xAI's Grok API with real-time access, citations, and image understanding
homepage: https://github.com/yourusername/xai-grok-search
metadata:
  category: search
  api_base: https://api.x.ai/v1
  capabilities:
    - api
    - web-search
    - x-search
    - caching
    - retry
  dependencies:
    - python3
  interface: Python + CLI
openclaw:
  emoji: "🔍"
  install:
    env:
      - XAI_API_KEY
author:
  name: Christopher Stanley
---

# xAI Grok Search — v2.0

Search the web and X/Twitter using xAI's Grok with real-time live data, full citations, retry/backoff, SQLite caching, and cost tracking.

**Grok's unique edge:** It is the *only* model with direct, native access to X/Twitter posts in real time. For social sentiment, trending reactions, or posts from specific accounts, there is no substitute.

---

## When to Use This Skill

### Use Web Search (`--mode web`) For:
- Current news, recent events, live documentation
- Stock prices, weather, breaking stories
- Verifying facts with authoritative sources
- Domain-restricted research (e.g., only gov.uk, only arxiv.org)

### Use X Search (`--mode x`) For:
- **Social sentiment** — what real people are saying right now
- Reactions to announcements, product launches, political events
- Posts from specific accounts (journalists, researchers, execs)
- Tracking a topic within a date range

**Do NOT use for:**
- Static historical facts (use internal knowledge)
- Math or code generation (use code agents)
- Creative writing (use writing agents)

---

## Setup

```bash
export XAI_API_KEY="xai-your-key-here"
```

Get your key: https://console.x.ai/

No pip installs required — uses Python stdlib only.

---

## CLI Usage

```bash
# Web search
python3 skills/grok/grok.py "latest AI regulation news" --mode web

# X search — social sentiment
python3 skills/grok/grok.py "OpenAI reactions" --mode x

# X search — date range + specific handle
python3 skills/grok/grok.py "AI policy" --mode x --handles sama OpenAI --from-date 2025-01-01

# Web search — domain restricted, JSON output
python3 skills/grok/grok.py "UN climate summit" --mode web --domains un.org gov.uk --json

# Force live call (skip cache)
python3 skills/grok/grok.py "breaking news" --mode web --no-cache

# Image understanding enabled
python3 skills/grok/grok.py "SpaceX launch images" --mode web --image
```

### CLI Flags

| Flag | Description |
|------|-------------|
| `--mode web\|x` | Search mode (default: web) |
| `--model MODEL` | Model name (default: grok-3-fast) |
| `--domains D1 D2` | [web] Restrict to domains (max 5) |
| `--exclude-domains D1` | [web] Exclude domains (max 5) |
| `--handles H1 H2` | [x] Filter to X handles (no @, max 10) |
| `--exclude-handles H1` | [x] Exclude X handles (max 10) |
| `--from-date YYYY-MM-DD` | [x] Posts from this date |
| `--to-date YYYY-MM-DD` | [x] Posts to this date |
| `--image` | Enable image understanding |
| `--video` | [x] Enable video understanding |
| `--json` | Output raw JSON |
| `--no-cache` | Skip cache, force live API call |
| `--api-key KEY` | Override XAI_API_KEY |

---

## Python Module Usage

```python
from skills.grok import search_web, search_x, GrokResult

# Basic web search
result = search_web("latest AI regulation developments")
print(result.content)
print(result.format_citations_markdown())

# X search with filters
result = search_x(
    "OpenAI GPT-5 reactions",
    allowed_x_handles=["sama", "karpathy", "emollick"],
    from_date="2025-01-01"
)
print(result.content)
print(f"Cost: ${result.cost_usd:.6f}")
print(f"Live search performed: {result.search_performed}")

# Domain-restricted web search
result = search_web(
    "climate summit outcomes",
    allowed_domains=["un.org", "gov.uk"],
    enable_image_understanding=True
)

# Async (non-blocking)
import asyncio
from skills.grok import async_search_web
result = asyncio.run(async_search_web("breaking news today"))

# Access structured citations
for cite in result.citations:
    print(cite.format_markdown())  # [1] [Title](url)\n   > snippet...
    print(cite.url, cite.title, cite.snippet)

# JSON serialization
import json
print(result.to_json())
data = result.to_dict()  # plain dict
```

### GrokResult Fields

| Field | Type | Description |
|-------|------|-------------|
| `content` | str | Full text response from Grok |
| `citations` | List[Citation] | Structured source list |
| `search_type` | str | "web" or "x" |
| `model` | str | Model used |
| `query` | str | Original query |
| `timestamp` | str | ISO8601 UTC time of call |
| `search_performed` | bool | True if live search was executed |
| `cache_hit` | bool | True if result came from cache |
| `usage` | dict | Token counts from API |
| `cost_usd` | float | Estimated cost in USD |
| `error` | Optional[str] | Error message if partial failure |

### Citation Fields

| Field | Type | Description |
|-------|------|-------------|
| `url` | str | Source URL |
| `title` | str | Page/post title |
| `snippet` | str | Relevant excerpt |
| `index` | int | 1-based citation number |

---

## Reliability Features

### Retry / Backoff
- Exponential backoff with jitter on 429 (rate limit) and 5xx errors
- Max 3 retries, base delay 2s (doubles each attempt + random jitter)
- 90s timeout per request (Grok reasoning models can take 30-60s)
- Fatal errors (401, 403, 422) fail immediately without retry

### Caching
- Results cached in `agency.db` SQLite (pyresearch pattern)
- Default TTL: 1 hour (live search results go stale fast)
- Cache key: hash of query + search type + filter options
- All calls logged to `grok_call_log` table with token counts and cost

### Error Types
```python
from skills.grok import GrokError

try:
    result = search_web("query")
except GrokError as e:
    print(e.code)      # HTTP status or 0 for network
    print(e.title)     # "Rate Limited", "Unauthorized", etc.
    print(e.detail)    # Full error message
    print(e.retryable) # True if retry makes sense
```

---

## Models

| Model | Speed | Live Search | Notes |
|-------|-------|-------------|-------|
| `grok-3-fast` | Fast | ✅ | **Recommended default** |
| `grok-3` | Slower | ✅ | Higher quality reasoning |
| `grok-3-mini` | Fastest | ✅ | Lightweight, lower cost |
| `grok-3-mini-fast` | Fastest | ✅ | Budget option |

> **Note:** Models outside the `LIVE_SEARCH_MODELS` set may not perform real-time lookups. The skill warns on stderr if an unsupported model is used.

---

## Cost Tracking

Every API call is logged to `agency.db`:

```sql
SELECT ts, query, search_type, model, cache_hit, cost_usd
FROM grok_call_log
ORDER BY ts DESC LIMIT 20;
```

Cached calls cost $0.00. Typical live call: ~$0.0001–$0.001 depending on response length.

---

## Troubleshooting

### `[401] Unauthorized: Check XAI_API_KEY`
```bash
export XAI_API_KEY="xai-your-key-here"
```

### `[429] Rate Limited: Too many requests`
The skill handles this automatically with backoff. If persistent, reduce call frequency or use `--no-cache` less often.

### Slow responses (30–60s)
Normal for reasoning models doing live search. The 90s timeout gives full room. Inform users: *"Searching live — this takes 30–60 seconds."*

### Poor results
- Add `--domains` to restrict to authoritative sources
- Narrow `--from-date` / `--to-date` for X searches
- Switch to `--model grok-3` for more thorough reasoning

### Cache returning stale data
```bash
python3 grok.py "query" --no-cache
```
Or query agency.db directly:
```bash
sqlite3 /root/.openclaw/workspace/agency.db "DELETE FROM grok_cache WHERE search_type='web';"
```

---

## What Grok Can Do That Nothing Else Can

1. **Native X/Twitter access** — Not scraping. Real API-level post retrieval filtered by handle, date, media type.
2. **Social sentiment at source** — Real reactions, not summaries of reactions.
3. **Image + video in search context** — Analyze images/videos *found during search*, not just uploaded files.
4. **xAI-native reasoning** — Search + reasoning in one model call, no chaining needed.

## Where It Still Falls Short

1. **No streaming** — Response arrives all-at-once; long reasoning runs block until complete.
2. **X search date coverage** — Older posts (pre-2022) have patchy coverage.
3. **No batch mode** — Each query is a separate API call; parallel queries burn budget fast.
4. **Cost unpredictability** — Reasoning tokens are hard to estimate pre-call; monitor `grok_call_log`.

---

## API Documentation

- Web Search: https://docs.x.ai/developers/tools/web-search
- X Search: https://docs.x.ai/developers/tools/x-search
- Models: https://docs.x.ai/developers/models
- Console: https://console.x.ai/
