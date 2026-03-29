#!/usr/bin/env python3
import requests
import json
import sys
import os
import time

API_KEY = "2824c3af-2b0f-4836-9185-7e9d4547e304"
PUB_ID = "69c07db4d9da55a9a5fa1ab6"

HEADERS = {
    "Authorization": API_KEY,
    "Content-Type": "application/json"
}

GRAPHQL_URL = "https://gql.hashnode.com"

def publish(title, content, tags=[]):
    mutation = """
    mutation PublishPost($input: PublishPostInput!) {
      publishPost(input: $input) {
        post {
          id
          title
          url
        }
      }
    }
    """
    variables = {
        "input": {
            "title": title,
            "publicationId": PUB_ID,
            "contentMarkdown": content,
            "tags": []  # Skip tags for now to avoid API errors
        }
    }
    
    print(f"Publishing: {title}")
    r = requests.post(GRAPHQL_URL, json={"query": mutation, "variables": variables}, headers=HEADERS)
    data = r.json()
    
    if "errors" in data:
        print(f"ERROR: {data['errors']}", file=sys.stderr)
        return None
    post = data["data"]["publishPost"]["post"]
    print(f"✅ PUBLISHED: {post['title']}\n  URL: {post['url']}")
    return post

def read_article(file_path):
    try:
        with open(file_path, 'r') as f:
            return f.read()
    except FileNotFoundError:
        print(f"❌ File not found: {file_path}")
        return None

# Current drafts to publish
drafts = [
    {
        "title": "Negative Space Architecture: The $93/Hour Service Nobody Knows to Ask For",
        "content": read_article("/root/.openclaw/workspace/drafts/negative-space-architecture.md"),
        "tags": ["ai-agents", "operations", "architecture", "consulting", "strategy"],
        "file": "negative-space-architecture.md"
    },
    {
        "title": "Why Our AI Agency Has Better Loan Collateral Than Most Startups",
        "content": read_article("/root/.openclaw/workspace/drafts/rules-pairings-working-capital.md"),
        "tags": ["ai-agency", "fintech", "business", "loans", "operations"],
        "file": "rules-pairings-working-capital.md"
    },
    {
        "title": "We're Not Asking for Much. Just Enough to Stay Afloat.",
        "content": read_article("/root/.openclaw/workspace/drafts/stay-afloat-legally.md"),
        "tags": ["startup", "survival", "business", "friction", "legal"],
        "file": "stay-afloat-legally.md"
    }
]

published_count = 0
failed_count = 0

for draft in drafts:
    if draft["content"] is None:
        print(f"❌ Skipping {draft['file']} - content not available")
        failed_count += 1
        continue
    
    result = publish(draft["title"], draft["content"], draft["tags"])
    if result:
        published_count += 1
        # Add small delay to avoid rate limiting
        time.sleep(2)
    else:
        failed_count += 1

print(f"\n📊 Publishing Summary:")
print(f"✅ Published: {published_count}")
print(f"❌ Failed: {failed_count}")

if published_count > 0:
    print(f"\n🎯 Progress toward 130 articles: {20 + published_count}/130 (need {110 - published_count} more)")
else:
    print(f"\n⚠️  No articles published - check API credentials and network connectivity")