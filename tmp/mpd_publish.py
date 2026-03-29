#!/usr/bin/env python3
"""
Matthew Paige Damon — Hashnode Publisher
Phase 4: Publish article to vol_1 series
"""

import urllib.request
import json
import sys

HASHNODE_API = "https://gql.hashnode.com/"
API_KEY = "2824c3af-2b0f-4836-9185-7e9d4547e304"
PUB_ID = "69c07db4d9da55a9a5fa1ab6"
SERIES_ID = "69c48b0a8cf65b19f462257d"  # vol_1: Field Notes from Matthew Paige Damon

def gql(query, variables):
    payload = json.dumps({"query": query, "variables": variables}).encode()
    req = urllib.request.Request(
        HASHNODE_API,
        data=payload,
        headers={
            "Content-Type": "application/json",
            "Authorization": API_KEY
        }
    )
    with urllib.request.urlopen(req, timeout=30) as resp:
        return json.loads(resp.read())

def check_series():
    query = """
    query GetSeries($pubId: ObjectId!, $seriesSlug: String!) {
      publication(id: $pubId) {
        series(slug: $seriesSlug) {
          id
          name
          slug
          posts(first: 50) {
            edges {
              node {
                id
                title
                publishedAt
              }
            }
          }
        }
      }
    }
    """
    data = gql(query, {"pubId": PUB_ID, "seriesSlug": "matthew-paige-damon"})
    series = data.get("data", {}).get("publication", {}).get("series", {})
    posts = series.get("posts", {}).get("edges", []) if series else []
    return len(posts), series.get("id"), series.get("name")

def publish_article(title, content_md, tags, cover_url=None):
    query = """
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
    
    input_obj = {
        "title": title,
        "publicationId": PUB_ID,
        "contentMarkdown": content_md,
        "tags": tags,
        "seriesId": SERIES_ID,
        "settings": {
            "scheduled": False,
            "enableTableOfContent": False,
            "slugOverride": None
        }
    }
    
    if cover_url:
        input_obj["coverImageOptions"] = {"coverImageURL": cover_url}
    
    data = gql(query, {"input": input_obj})
    
    if data.get("errors"):
        print(f"ERROR: {json.dumps(data['errors'])}")
        return None
    
    post = data.get("data", {}).get("publishPost", {}).get("post", {})
    return post

# ---- Check current state ----
try:
    count, sid, sname = check_series()
    print(f"SERIES: {sname} (id: {sid})")
    print(f"CURRENT COUNT: {count}/8")
    print(f"STATUS: {'AT CAPACITY' if count >= 8 else 'SPACE REMAINING'}")
except Exception as e:
    print(f"Series check failed: {e}")
    count = 0
    sid = SERIES_ID
    sname = "Field Notes from Matthew Paige Damon"

if len(sys.argv) > 1 and sys.argv[1] == "--check-only":
    sys.exit(0)

# ---- Proceed with publish ----
print("\n--- WRITING ARTICLE ---")
