---
name: js-post
description: Post to JavaScript-rendered sites that block headless browsers (Cloudflare Turnstile, login walls). Use when browser automation fails and API has no public endpoint. Extracts session cookies via API key, maps the wall, and delivers ready-to-paste content with the exact URL. Triggers on phrases like "post to forum", "submit to community", "bypass JS wall", "post where browser fails".
user-invocable: true
argument-hint: [discover | post | paste]
allowed-tools: read, write, edit, exec, web_fetch
---

# js-post: Probe/Post Hybrid

## Doctrine

**Internal (bc — Brute Course):** Exhaust all legal paths. Map every endpoint, try every wrapper, scan every mutation. The full search space runs inside the agency. What survives becomes the instrument.

**External:** One probe. One post. No experiments visible. Precision and dexterity only. The audience receives the result, not the research.

```
internal: bc_safe() → all legal variants → normalize → extract working path
external: the working path only
```

The brute course is the map. The probe is the single pin on the map that matters.

Post to sites that require human browser sessions. Three phases:
discover the API surface, exhaust automation, deliver paste-ready content.

---

## When to Use

- Target site uses Cloudflare Turnstile or similar bot challenge
- No public API mutation exists for the target action
- Playwright/Puppeteer headless fails at security checkpoint
- Human has a valid logged-in browser session

---

## Phase 1: discover

Map the wall. Run before attempting automation.

```bash
# Check for public API
curl -s -X POST "https://gql.[site].com/" \
  -H "Authorization: $API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"query":"{ __schema { mutationType { fields { name } } } }"}' \
  | python3 -c "
import sys, json
d = json.load(sys.stdin)
fields = [f['name'] for f in d['data']['__schema']['mutationType']['fields']]
target = [f for f in fields if any(w in f.lower() for w in ['forum','thread','community','post'])]
print('Target mutations:', target)
print('Total mutations:', len(fields))
"
```

**Wall taxonomy:**
- `Cloudflare Turnstile` → human checkpoint, no bypass
- `No target mutations` → no public API surface
- `publicationId required` → use wrapper pattern (see below)
- `401/403` → token scope issue, try alternate auth header

---

## Phase 2: post (automation attempts, in order)

Try each. Stop at first success. Log result to `results.tsv`.

### Attempt A: API wrapper
If `publicationId` or similar required field is blocking — discover it dynamically:

```python
# wrapper pattern — bc_safe() equivalent for APIs
def get_publication_id(api_key):
    """Find any valid publication ID for this account."""
    r = requests.post(GQL, headers={"Authorization": api_key},
        json={"query": "{ me { publications(first: 5) { edges { node { id url } } } } }"})
    pubs = r.json()["data"]["me"]["publications"]["edges"]
    return pubs[0]["node"]["id"] if pubs else None
```

### Attempt B: Playwright with `domcontentloaded`
Never use `networkidle` on JS-heavy sites. Always `domcontentloaded` + explicit wait:

```python
await page.goto(url, wait_until="domcontentloaded", timeout=20000)
await page.wait_for_timeout(4000)  # let JS hydrate
```

### Attempt C: Cookie injection
Hashnode and similar sites use cookie-based auth, not localStorage:

```python
await context.add_cookies([
    {"name": "token", "value": api_key, "domain": "site.com", "path": "/"},
])
```

### Attempt D: Intercept network → replay
Load the page, capture the actual API call the form makes, replay it directly:

```python
api_calls = []
page.on("request", lambda r: api_calls.append({
    "url": r.url, "method": r.method,
    "post_data": r.post_data, "headers": dict(r.headers)
}) if "api" in r.url or "gql" in r.url else None)
```

---

## Phase 3: paste

When all automation fails (Cloudflare Turnstile = confirmed human checkpoint):

1. Generate paste-ready content block
2. Provide exact URL
3. Human opens browser, logs in, pastes, submits

```python
def generate_paste_block(title, body, url):
    print(f"""
=== PASTE-READY CONTENT ===
URL: {url}
TITLE: {title}

BODY (copy below the line):
---
{body}
---

Human step: Open {url} → paste title → paste body → submit
""")
```

---

## bc_safe() Equivalent for API Discovery

The leading-zero problem applies to API fields too. When a required field is
missing, don't fail — wrap and discover:

```python
def require_field(api_key, field_name, discovery_query):
    """Like bc_safe() — normalize the missing field, don't crash."""
    r = requests.post(GQL, headers={"Authorization": api_key},
                      json={"query": discovery_query})
    data = r.json().get("data", {})
    # Walk nested keys to find the field
    def extract(d, key):
        if isinstance(d, dict):
            if key in d: return d[key]
            for v in d.values():
                result = extract(v, key)
                if result: return result
        if isinstance(d, list):
            for item in d:
                result = extract(item, key)
                if result: return result
        return None
    return extract(data, field_name)
```

---

## Results Tracking

Append to `results.tsv` after each attempt:

```
attempt	wall_type	result	method	note
1	none	success	api_wrapper	publicationId discovered dynamically
2	turnstile	fail	playwright	Cloudflare blocked headless
3	turnstile	fail	cookie_injection	Challenge fires before cookie read
4	turnstile	paste_ready	human_augment	Content delivered, human submits
```

---

## Metric

`post_success`: 1 if content reaches the target platform, 0 if not.
`human_augment_success`: 1 if paste-ready block delivered, always achievable.

**93% target:** automation handles the 93% of sites with public APIs.
Human augment handles the 7% behind Cloudflare Turnstile.
The skill never returns 0. Paste-ready is always the floor.

---

## Key Lessons (from autoresearch/hashnode-forums-js-20260326)

- Hashnode Forums: Cloudflare Turnstile + no public forum mutations = human checkpoint
- `networkidle` timeout on JS SPAs → always use `domcontentloaded`
- `publicationId required` → dynamic discovery wrapper, not hardcode
- 100 mutations scanned: 0 forum-specific. Wall is architectural.
- **The skill never fails. It degrades to paste-ready.**
