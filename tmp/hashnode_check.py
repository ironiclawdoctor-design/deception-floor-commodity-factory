#!/usr/bin/env python3
"""Check Hashnode series and article counts."""

import urllib.request
import json

HASHNODE_API = "https://gql.hashnode.com/"
API_KEY = "2824c3af-2b0f-4836-9185-7e9d4547e304"
PUB_ID = "69c07db4d9da55a9a5fa1ab6"
SERIES_ID = "69c48b0a8cf65b19f462257d"  # vol_1: Field Notes from Matthew Paige Damon

query = """
query GetSeriesArticles($pubId: ObjectId!, $seriesSlug: String!) {
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
            url
          }
        }
      }
    }
  }
}
"""

variables = {
    "pubId": PUB_ID,
    "seriesSlug": "matthew-paige-damon"
}

payload = json.dumps({"query": query, "variables": variables}).encode()
req = urllib.request.Request(
    HASHNODE_API,
    data=payload,
    headers={
        "Content-Type": "application/json",
        "Authorization": API_KEY
    }
)

try:
    with urllib.request.urlopen(req, timeout=30) as resp:
        data = json.loads(resp.read())
    
    series = data.get("data", {}).get("publication", {}).get("series", {})
    if series:
        posts = series.get("posts", {}).get("edges", [])
        print(f"Series: {series.get('name')} (id: {series.get('id')})")
        print(f"Article count: {len(posts)}")
        for edge in posts:
            node = edge["node"]
            print(f"  - {node['title']} | {node.get('publishedAt', 'N/A')}")
    else:
        print("Series not found or empty")
        print(json.dumps(data, indent=2))
except Exception as e:
    print(f"Error: {e}")
    import traceback; traceback.print_exc()
