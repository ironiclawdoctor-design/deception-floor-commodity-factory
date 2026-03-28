#!/usr/bin/env python3
import requests
import json
import sys
from datetime import datetime, timezone

API_KEY = "2824c3af-2b0f-4836-9185-7e9d4547e304"
PUB_ID = "69c07db4d9da55a9a5fa1ab6"
SERIES_ID = "69c48b0a8cf65b19f462257d"  # vol_1

HEADERS = {
    "Authorization": API_KEY,
    "Content-Type": "application/json"
}

GRAPHQL_URL = "https://gql.hashnode.com"

def publish_mpd(title, content, series_id):
    mutation = """
    mutation PublishPost($input: PublishPostInput!) {
      publishPost(input: $input) {
        post {
          id
          title
          url
          slug
        }
      }
    }
    """
    variables = {
        "input": {
            "title": title,
            "publicationId": PUB_ID,
            "contentMarkdown": content,
            "seriesId": series_id,
            "tags": [
                {"slug": "productivity", "name": "Productivity"},
                {"slug": "humor", "name": "Humor"},
                {"slug": "ai", "name": "AI"},
                {"slug": "agency", "name": "Agency"}
            ]
        }
    }
    r = requests.post(GRAPHQL_URL, json={"query": mutation, "variables": variables}, headers=HEADERS)
    data = r.json()
    if "errors" in data:
        print(f"ERROR: {json.dumps(data['errors'], indent=2)}", file=sys.stderr)
        return None
    post = data["data"]["publishPost"]["post"]
    print(f"PUBLISHED: {post['title']}")
    print(f"URL: {post['url']}")
    print(f"ID: {post['id']}")
    return post

def read_article(path):
    with open(path, 'r') as f:
        return f.read()

# Publish
title = "Field Notes #9: The Cron That Didn't Know It Was Therapy"
content = read_article("/root/.openclaw/workspace/mpd-article-003.md")

post = publish_mpd(title, content, SERIES_ID)

if post:
    # Log to mpd-series.json (update article_count)
    with open("/root/.openclaw/workspace/mpd-series.json", 'r') as f:
        series = json.load(f)
    series["article_count"] = series.get("article_count", 8) + 1
    with open("/root/.openclaw/workspace/mpd-series.json", 'w') as f:
        json.dump(series, f, indent=2)
    
    # Log to mpd-log.jsonl
    entry = {
        "ts": datetime.now(timezone.utc).isoformat(),
        "title": post["title"],
        "url": post["url"],
        "id": post["id"],
        "vol": "vol_1",
        "series_id": SERIES_ID,
        "article_count": series["article_count"]
    }
    with open("/root/.openclaw/workspace/mpd-log.jsonl", 'a') as f:
        f.write(json.dumps(entry) + "\n")
    
    print(f"\nSeries count updated to: {series['article_count']}")
    print(f"Logged to mpd-log.jsonl")
else:
    print("FAILED: No post returned", file=sys.stderr)
    sys.exit(1)
