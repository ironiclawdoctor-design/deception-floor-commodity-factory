#!/usr/bin/env python3
"""
Matthew Paige Damon — vol_1 article 9 publisher
Queries series, publishes article, logs result.
"""
import requests
import json
import sys
from datetime import datetime

API_KEY = "2824c3af-2b0f-4836-9185-7e9d4547e304"
PUB_ID = "69c07db4d9da55a9a5fa1ab6"
GQL = "https://gql.hashnode.com"
HEADERS = {
    "Authorization": API_KEY,
    "Content-Type": "application/json"
}

# Step 1: Query series list
series_query = """
query {
  publication(host: "dollaragency.hashnode.dev") {
    seriesList(first: 10) {
      edges {
        node {
          id
          name
          slug
        }
      }
    }
  }
}
"""

print("[MPD] Phase 2: Querying series list...")
r = requests.post(GQL, json={"query": series_query}, headers=HEADERS)
data = r.json()
print(json.dumps(data, indent=2))

# Find vol_1 series
series_id = None
series_list = data.get("data", {}).get("publication", {}).get("seriesList", {}).get("edges", [])
for edge in series_list:
    node = edge.get("node", {})
    name = node.get("name", "").lower()
    slug = node.get("slug", "").lower()
    print(f"  Series: {node.get('name')} | slug: {slug} | id: {node.get('id')}")
    if "vol_1" in name or "vol_1" in slug or "vol 1" in name or "volume 1" in name:
        series_id = node.get("id")
        print(f"[MPD] Matched vol_1 series: {series_id}")

if not series_id and series_list:
    # Use first series if vol_1 not found
    series_id = series_list[0]["node"]["id"]
    print(f"[MPD] No vol_1 match. Using first series: {series_id}")

# Step 2: Read article content
with open("/root/.openclaw/workspace/article-mpd-vol1-09.md", "r") as f:
    content = f.read()

# Step 3: Publish
title = "The Bricks You Build Before the Block Shows Up"

mutation = """
mutation PublishPost($input: PublishPostInput!) {
  publishPost(input: $input) {
    post {
      id
      title
      url
      publishedAt
    }
  }
}
"""

variables = {
    "input": {
        "title": title,
        "publicationId": PUB_ID,
        "contentMarkdown": content,
        "tags": [],
        "seriesId": series_id
    }
}

# If no series_id, publish without it
if not series_id:
    del variables["input"]["seriesId"]

print(f"\n[MPD] Phase 3: Publishing article...")
print(f"  Title: {title}")
print(f"  Series ID: {series_id}")

r2 = requests.post(GQL, json={"query": mutation, "variables": variables}, headers=HEADERS)
result = r2.json()
print(json.dumps(result, indent=2))

if "errors" in result:
    print(f"\n[MPD] ERROR: {result['errors']}", file=sys.stderr)
    sys.exit(1)

post = result["data"]["publishPost"]["post"]
url = post["url"]
print(f"\n[MPD] PUBLISHED: {post['title']}")
print(f"  URL: {url}")
print(f"  ID: {post['id']}")

# Step 4: Log result
log_entry = {
    "ts": datetime.utcnow().isoformat() + "Z",
    "agent": "matthew-paige-damon",
    "phase": "vol_1",
    "article_index": 9,
    "title": title,
    "url": url,
    "post_id": post["id"],
    "series_id": series_id,
    "file": "article-mpd-vol1-09.md"
}

log_path = "/root/.openclaw/workspace/hashnode-log.jsonl"
with open(log_path, "a") as f:
    f.write(json.dumps(log_entry) + "\n")

print(f"\n[MPD] Phase 5: Logged to {log_path}")
print("[MPD] Total victory. Zero complaint tickets filed.")
