#!/usr/bin/env python3
"""
Fix: move published post to correct vol_1 series.
vol_1 = "Field Notes from Matthew Paige Damon" = 69c48b0a8cf65b19f462257d
"""
import requests
import json

API_KEY = "2824c3af-2b0f-4836-9185-7e9d4547e304"
PUB_ID = "69c07db4d9da55a9a5fa1ab6"
GQL = "https://gql.hashnode.com"
HEADERS = {
    "Authorization": API_KEY,
    "Content-Type": "application/json"
}

POST_ID = "69c847f67780190b9b62ae45"
VOL1_SERIES_ID = "69c48b0a8cf65b19f462257d"

# Check how many posts are already in vol_1
query_series_posts = """
query {
  publication(host: "dollaragency.hashnode.dev") {
    series(slug: "matthew-paige-damon") {
      id
      name
      posts(first: 20) {
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

print("Checking vol_1 series posts...")
r = requests.post(GQL, json={"query": query_series_posts}, headers=HEADERS)
data = r.json()
series = data.get("data", {}).get("publication", {}).get("series", {})
posts = series.get("posts", {}).get("edges", [])
print(f"Series: {series.get('name')} | Posts: {len(posts)}")
for i, edge in enumerate(posts):
    n = edge["node"]
    print(f"  [{i+1}] {n['title']} | {n['publishedAt'][:10]}")

# Update the post to move it to vol_1 series
update_mutation = """
mutation UpdatePost($input: UpdatePostInput!) {
  updatePost(input: $input) {
    post {
      id
      title
      url
    }
  }
}
"""

update_vars = {
    "input": {
        "id": POST_ID,
        "seriesId": VOL1_SERIES_ID
    }
}

print(f"\nMoving post {POST_ID} to vol_1 series {VOL1_SERIES_ID}...")
r2 = requests.post(GQL, json={"query": update_mutation, "variables": update_vars}, headers=HEADERS)
result = r2.json()
print(json.dumps(result, indent=2))
