#!/usr/bin/env python3
"""
Push all unpublished articles to Hashnode.
Reads articles from workspace, posts via GraphQL API.
Series grouping via updatePost will be done after upload (CFO directive).
"""

import json, urllib.request, urllib.error, time, re

SECRETS = json.load(open('/root/.openclaw/workspace/secrets/hashnode.json'))
API_KEY = SECRETS['api_key']
PUB_ID = SECRETS['pub_id']
API_URL = 'https://gql.hashnode.com/'

HEADERS = {
    'Content-Type': 'application/json',
    'Authorization': API_KEY
}

ARTICLES = [
    {
        'file': '/root/.openclaw/workspace/article-2-draft.md',
        'title': 'The Debt Doctrine: How an AI Agency Turned $60 Into a Currency',
        'slug': 'the-debt-doctrine-ai-agency-60-dollars-currency',
        'tags': ['ai', 'database', 'sqlite', 'opensource'],
        'series': 'Confessions of Dollar',
    },
    {
        'file': '/root/.openclaw/workspace/article-3-draft.md',
        'title': 'I Gave an AI $60 and It Built a Tax Strategy, a Currency, and a Confession Booth',
        'slug': 'i-gave-ai-60-dollars-tax-strategy-currency-confession-booth',
        'tags': ['ai', 'programming', 'productivity', 'webdev'],
        'series': 'Confessions of Dollar',
    },
    {
        'file': '/root/.openclaw/workspace/article-4-underdog.md',
        'title': 'If You Have $0.07 in BTC, This AI Agent Will Count It as a Vote',
        'slug': 'if-you-have-007-btc-ai-agent-will-count-it-vote',
        'tags': ['ai', 'bitcoin', 'opensource', 'webdev'],
        'series': 'Confessions of Dollar',
    },
]

def strip_frontmatter(text):
    """Remove YAML frontmatter from markdown."""
    if text.startswith('---'):
        end = text.find('---', 3)
        if end != -1:
            return text[end+3:].lstrip('\n')
    return text

def gql(query, variables=None):
    payload = {'query': query}
    if variables:
        payload['variables'] = variables
    body = json.dumps(payload).encode()
    req = urllib.request.Request(API_URL, data=body, headers=HEADERS, method='POST')
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            result = json.loads(r.read())
            if 'errors' in result:
                raise Exception(f"GraphQL errors: {result['errors']}")
            return result
    except urllib.error.HTTPError as e:
        raise Exception(f"HTTP {e.code}: {e.read().decode()}")

def publish_article(article):
    content = open(article['file']).read()
    content = strip_frontmatter(content)
    
    # Map tag names to Hashnode tag slugs
    tag_map = {
        'ai': {'slug': 'artificial-intelligence', 'name': 'Artificial Intelligence'},
        'database': {'slug': 'database', 'name': 'Database'},
        'sqlite': {'slug': 'sqlite', 'name': 'SQLite'},
        'opensource': {'slug': 'open-source', 'name': 'Open Source'},
        'programming': {'slug': 'programming', 'name': 'Programming'},
        'productivity': {'slug': 'productivity', 'name': 'Productivity'},
        'webdev': {'slug': 'web-development', 'name': 'Web Development'},
        'bitcoin': {'slug': 'bitcoin', 'name': 'Bitcoin'},
    }
    
    tags = [tag_map[t] for t in article['tags'] if t in tag_map]
    
    mutation = """
    mutation PublishPost($input: PublishPostInput!) {
        publishPost(input: $input) {
            post {
                id
                slug
                title
                url
                publishedAt
            }
        }
    }
    """
    
    variables = {
        'input': {
            'title': article['title'],
            'slug': article['slug'],
            'contentMarkdown': content,
            'publicationId': PUB_ID,
            'tags': tags,
        }
    }
    
    result = gql(mutation, variables)
    return result['data']['publishPost']['post']

results = []
for article in ARTICLES:
    print(f"\nPublishing: {article['title'][:60]}...")
    try:
        post = publish_article(article)
        results.append({
            'status': 'ok',
            'title': article['title'],
            'url': post.get('url'),
            'id': post.get('id'),
            'slug': post.get('slug'),
        })
        print(f"  ✅ Published: {post.get('url')}")
        time.sleep(2)  # rate limit courtesy
    except Exception as e:
        err = str(e)
        results.append({
            'status': 'error',
            'title': article['title'],
            'error': err,
        })
        print(f"  ❌ Error: {err}")

# Save results
log_path = '/root/.openclaw/workspace/hashnode-push-log.json'
with open(log_path, 'w') as f:
    json.dump(results, f, indent=2)

print(f"\n--- SUMMARY ---")
ok = [r for r in results if r['status'] == 'ok']
fail = [r for r in results if r['status'] == 'error']
print(f"Published: {len(ok)}/{len(results)}")
for r in ok:
    print(f"  ✅ {r['url']}")
for r in fail:
    print(f"  ❌ {r['title'][:50]} — {r['error'][:100]}")

print(f"\nLog saved to {log_path}")
print("\nNOTE: Series grouping will be done in a follow-up pass after all posts are live.")
