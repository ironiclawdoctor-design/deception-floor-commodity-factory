#!/usr/bin/env python3
"""Check if giraffe article is already published."""

import urllib.request
import json

HASHNODE_API = "https://gql.hashnode.com/"
API_KEY = "2824c3af-2b0f-4836-9185-7e9d4547e304"
PUB_ID = "69c07db4d9da55a9a5fa1ab6"

query = """
query GetPosts($pubId: ObjectId!) {
  publication(id: $pubId) {
    posts(first: 20) {
      edges {
        node {
          id
          title
          url
          publishedAt
          series {
            id
            name
          }
        }
      }
    }
  }
}
"""

payload = json.dumps({"query": query, "variables": {"pubId": PUB_ID}}).encode()
req = urllib.request.Request(
    HASHNODE_API,
    data=payload,
    headers={
        "Content-Type": "application/json",
        "Authorization": API_KEY
    }
)

with urllib.request.urlopen(req, timeout=30) as resp:
    data = json.loads(resp.read())

posts = data.get("data", {}).get("publication", {}).get("posts", {}).get("edges", [])
print(f"Total recent posts: {len(posts)}")
for edge in posts:
    node = edge["node"]
    series_name = (node.get("series") or {}).get("name", "no series")
    print(f"  [{series_name}] {node['title']}")
    print(f"    {node.get('url', 'N/A')}")
