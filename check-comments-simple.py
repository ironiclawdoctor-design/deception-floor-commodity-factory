#!/usr/bin/env python3
import requests
import json

API_KEY = "2824c3af-2b0f-4836-9185-7e9d4547e304"

HEADERS = {
    "Authorization": API_KEY,
    "Content-Type": "application/json"
}

GRAPHQL_URL = "https://gql.hashnode.com"

def check_comments():
    query = """
    query GetPosts($publicationId: String!) {
      publication(id: $publicationId) {
        posts(first: 5) {
          edges {
            node {
              id
              title
              url
              comments(first: 10) {
                edges {
                  node {
                    id
                    text
                    author {
                      name
                    }
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
        "publicationId": "69c07db4d9da55a9a5fa1ab6"
    }
    
    try:
        r = requests.post(GRAPHQL_URL, json={"query": query, "variables": variables}, headers=HEADERS)
        data = r.json()
        
        if "errors" in data:
            print(f"GraphQL Error: {data['errors']}")
            return False
        
        publication = data.get("data", {}).get("publication", {})
        posts = publication.get("posts", {}).get("edges", [])
        
        print("📝 Checking Dollar Agency posts for comments...")
        print("=" * 50)
        
        total_comments = 0
        
        for post_edge in posts:
            post = post_edge["node"]
            title = post["title"]
            url = post["url"]
            comments = post.get("comments", {}).get("edges", [])
            
            print(f"\n📄 Article: {title}")
            print(f"   URL: {url}")
            print(f"   Comments: {len(comments)}")
            
            if len(comments) > 0:
                print(f"   Recent comments:")
                
                for comment_edge in comments:
                    comment = comment_edge["node"]
                    author = comment["author"]["name"]
                    content = comment["text"][:200] + "..." if len(comment["text"]) > 200 else comment["text"]
                    
                    print(f"     - {author}: {content}")
                    total_comments += 1
        
        print(f"\n" + "=" * 50)
        print(f"📊 Total comments found: {total_comments}")
        
        if total_comments == 0:
            print("✅ No comments found - nothing to respond to")
            return True
        else:
            print("⚠️ Comments found - but responding requires additional API access")
            return True
            
    except Exception as e:
        print(f"Error checking comments: {e}")
        return False

if __name__ == "__main__":
    check_comments()