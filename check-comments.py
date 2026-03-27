#!/usr/bin/env python3
"""Check for recent posts on Hashnode publication."""
import json
import urllib.request
import urllib.error

API_KEY = "2824c3af-2b0f-4836-9185-7e9d4547e304"
GQL_URL = "https://gql.hashnode.com/"

def make_gql_request(query, variables):
    """Make a GraphQL request to Hashnode API."""
    payload = json.dumps({"query": query, "variables": variables}).encode("utf-8")
    req = urllib.request.Request(
        GQL_URL,
        data=payload,
        headers={
            "Content-Type": "application/json",
            "Authorization": API_KEY,
        }
    )
    try:
        with urllib.request.urlopen(req, timeout=30) as response:
            return json.loads(response.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        return {"error": str(e), "body": e.read().decode("utf-8")}
    except Exception as e:
        return {"error": str(e)}

# Query to get recent posts
posts_query = """
query GetRecentPosts($host: String!) {
  publication(host: $host) {
    posts(first: 10) {
      edges {
        node {
          id
          title
          url
          publishedAt
        }
      }
    }
  }
}
"""

print("Checking for recent posts...")
result = make_gql_request(posts_query, {"host": "dollaragency.hashnode.dev"})

if "errors" in result:
    print(f"ERROR: {result['errors']}")
elif "data" in result and result["data"] and "publication" in result["data"]:
    posts = result["data"]["publication"]["posts"]["edges"]
    print(f"📊 Found {len(posts)} recent posts:")
    
    for edge in posts:
        post = edge["node"]
        print(f"\n📝 {post['title']}")
        print(f"   URL: {post['url']}")
        print(f"   Published: {post['publishedAt']}")
else:
    print(f"UNEXPECTED: {result}")

print("\nNote: Comments checking requires additional GraphQL complexity that may not be available.")
print("Manual review of individual post URLs would be needed to check for comments.")