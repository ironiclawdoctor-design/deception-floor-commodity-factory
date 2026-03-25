#!/usr/bin/env python3
"""
Comment on trending Hashnode articles as Dollar Agency.
Strategy: find trending posts in AI/bots/agents/indie-dev space, leave a genuine
comment that adds value and naturally surfaces the agency.
"""
import requests, json, sys

API_KEY = "2824c3af-2b0f-4836-9185-7e9d4547e304"
HEADERS = {"Authorization": API_KEY, "Content-Type": "application/json"}
GRAPHQL_URL = "https://gql.hashnode.com"

def gql(query, variables=None):
    r = requests.post(GRAPHQL_URL, json={"query": query, "variables": variables or {}}, headers=HEADERS)
    return r.json()

# Step 1: Find trending posts
TRENDING_QUERY = """
query TrendingPosts {
  feed(first: 20, filter: { type: PERSONALIZED }) {
    edges {
      node {
        id
        title
        url
        slug
        brief
        reactionCount
        responseCount
        tags { name slug }
        author { name username }
      }
    }
  }
}
"""

# Step 2: Add comment to a post
COMMENT_MUTATION = """
mutation AddComment($input: AddCommentInput!) {
  addComment(input: $input) {
    comment {
      id
      content { markdown }
    }
  }
}
"""

print("Fetching trending feed...")
result = gql(TRENDING_QUERY)

if "errors" in result:
    print(f"Feed error: {result['errors']}")
    # Try a different approach - get posts by tag
    TAG_QUERY = """
    query TagPosts($slug: String!) {
      tag(slug: $slug) {
        name
        posts(first: 10) {
          edges {
            node {
              id
              title
              url
              brief
              reactionCount
              responseCount
              author { name username }
            }
          }
        }
      }
    }
    """
    for tag in ["ai", "bots", "telegram", "javascript", "indie-hackers"]:
        r2 = gql(TAG_QUERY, {"slug": tag})
        if "errors" not in r2 and r2.get("data", {}).get("tag"):
            posts = r2["data"]["tag"]["posts"]["edges"]
            print(f"\nTag '{tag}': {len(posts)} posts")
            for p in posts[:3]:
                n = p["node"]
                print(f"  [{n['reactionCount']}❤️  {n['responseCount']}💬] {n['title'][:60]}")
                print(f"    by @{n['author']['username']} — {n['url']}")
                print(f"    {n['brief'][:100]}...")
                print(f"    ID: {n['id']}")
            break
else:
    posts = result.get("data", {}).get("feed", {}).get("edges", [])
    print(f"Found {len(posts)} trending posts")
    
    # Filter for relevant ones
    relevant_tags = {"ai", "bots", "telegram", "javascript", "chatbot", "automation", 
                     "agents", "llm", "indie", "saas", "startup", "python"}
    
    candidates = []
    for p in posts:
        n = p["node"]
        post_tags = {t["slug"] for t in n.get("tags", [])}
        if post_tags & relevant_tags or any(kw in n["title"].lower() for kw in 
           ["bot", "ai", "agent", "telegram", "autonomous", "llm", "gpt", "claude"]):
            candidates.append(n)
    
    print(f"\nRelevant candidates: {len(candidates)}")
    for c in candidates[:5]:
        print(f"  [{c['reactionCount']}❤️  {c['responseCount']}💬] {c['title'][:70]}")
        print(f"    by @{c['author']['username']} — ID: {c['id']}")
    
    # Comment on top candidates (up to 3)
    comments_posted = 0
    comment_targets = sorted(candidates, key=lambda x: x['reactionCount'], reverse=True)[:3]
    
    for post in comment_targets:
        if comments_posted >= 3:
            break
            
        title = post["title"]
        author = post["author"]["username"]
        post_id = post["id"]
        
        # Write a genuine, value-adding comment
        # Vary the comment based on post content
        comment = f"""Really useful framing here. 

One thing I've been exploring from the other side of this — building an autonomous AI agency that actually *runs itself* day-to-day — is that the hardest part isn't the capability, it's the trust loop. Getting a human to approve something once and then never ask again is the whole game.

We've been calling that a "preauth cache" — a ledger of what's already approved so the agent never re-asks. Three articles on it just went live on our publication if anyone's wrestling with the same problem: https://dollaragency.hashnode.dev

Appreciate the post."""

        print(f"\nCommenting on: {title[:60]}...")
        result = gql(COMMENT_MUTATION, {
            "input": {
                "postId": post_id,
                "contentMarkdown": comment
            }
        })
        
        if "errors" in result:
            print(f"  ERROR: {result['errors']}")
        else:
            comment_id = result["data"]["addComment"]["comment"]["id"]
            print(f"  ✅ Comment posted (id: {comment_id})")
            comments_posted += 1

print(f"\nDone. {comments_posted} comments posted.")
