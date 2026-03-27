#!/usr/bin/env python3
"""
Check for comments on Hashnode posts
"""

import requests
import json
import sys
from datetime import datetime, timezone

API_KEY = "2824c3af-2b0f-4836-9185-7e9d4547e304"
PUBLICATION_ID = "69c07db4d9da55a9a5fa1ab6"
BASE_URL = "https://gql.hashnode.com/"

HEADERS = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json"
}

def get_recent_posts():
    """Get recent posts from the publication"""
    query = """
    query GetPosts($publicationId: ID!, $first: Int!) {
        publication(id: $publicationId) {
            posts(first: $first) {
                edges {
                    node {
                        id
                        title
                        slug
                        url
                        publishedAt
                        comments(first: 10) {
                            edges {
                                node {
                                    id
                                    content
                                    author {
                                        name
                                    }
                                    createdAt
                                }
                            }
                        }
                    }
                }
            }
        }
    }
    """
    
    variables = {
        "publicationId": PUBLICATION_ID,
        "first": 10
    }
    
    try:
        response = requests.post(BASE_URL, json={"query": query, "variables": variables}, headers=HEADERS)
        response.raise_for_status()
        result = response.json()
        
        if "errors" in result:
            print(f"GraphQL errors: {result['errors']}", file=sys.stderr)
            return []
        
        posts = result["data"]["publication"]["posts"]["edges"]
        return [post["node"] for post in posts]
        
    except Exception as e:
        print(f"Error fetching posts: {str(e)}", file=sys.stderr)
        return []

def check_comments(posts):
    """Check comments on posts and prepare responses"""
    print(f"Checking comments on {len(posts)} posts...")
    
    comments_found = []
    
    for post in posts:
        post_title = post["title"]
        post_url = post["url"]
        comment_count = len(post["comments"]["edges"])
        
        if comment_count > 0:
            print(f"\n📝 Comments found on: {post_title}")
            print(f"   URL: {post_url}")
            print(f"   Comment count: {comment_count}")
            
            for comment_edge in post["comments"]["edges"]:
                comment = comment_edge["node"]
                print(f"   - {comment['author']['name']}: {comment['content'][:100]}...")
                comments_found.append({
                    "post_title": post_title,
                    "post_url": post_url,
                    "comment": comment
                })
        else:
            print(f"✅ No comments on: {post_title}")
    
    return comments_found

def main():
    """Main function"""
    print(f"Checking Hashnode comments at {datetime.now(timezone.utc).isoformat()}")
    print("-" * 50)
    
    posts = get_recent_posts()
    comments = check_comments(posts)
    
    print("\n" + "=" * 50)
    print(f"Comment check complete: {len(comments)} comments found")
    
    if comments:
        print("Comments found that may need responses:")
        for comment in comments:
            print(f"  - {comment['post_title']}: {comment['comment']['author']['name']} said: {comment['comment']['content'][:50]}...")
    else:
        print("No comments found requiring responses")

if __name__ == "__main__":
    main()