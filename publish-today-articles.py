#!/usr/bin/env python3
import requests
import json
import sys

API_KEY = "2824c3af-2b0f-4836-9185-7e9d4547e304"
PUB_ID = "69c07db4d9da55a9a5fa1ab6"

HEADERS = {
    "Authorization": API_KEY,
    "Content-Type": "application/json"
}

GRAPHQL_URL = "https://gql.hashnode.com"

def publish(title, content, tags=[]):
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
            "tags": [{"name": tag} for tag in tags]
        }
    }
    
    print(f"Publishing: {title}")
    r = requests.post(GRAPHQL_URL, json={"query": mutation, "variables": variables}, headers=HEADERS)
    data = r.json()
    
    if "errors" in data:
        print(f"ERROR: {data['errors']}", file=sys.stderr)
        return None
    
    post = data["data"]["publishPost"]["post"]
    print(f"✅ SUCCESSFULLY PUBLISHED: {post['title']}")
    print(f"   URL: {post['url']}")
    print(f"   Published: {post['publishedAt']}")
    return post

# Read the new articles
def read_article(file_path):
    with open(file_path, 'r') as f:
        return f.read()

print("🚀 Starting Dollar Agency article publishing...")
print("=" * 50)

articles = [
    {
        "title": "The AI Agent Paradox: Why Your Perfect Algorithm Creates Perfect Problems",
        "content": read_article("/root/.openclaw/workspace/article-ai-agents-paradox.md"),
        "tags": ["ai-agents", "humor", "technology", "philosophy"]
    },
    {
        "title": "NYC Mathematical Survival Guide: The Equations That Keep You Sane",
        "content": read_article("/root/.openclaw/workspace/article-nyc-mathematical-survival.md"),
        "tags": ["nyc-life", "mathematics", "humor", "urban-living"]
    },
    {
        "title": "Non-Profit Magic Math: How to Achieve World Change with $0.07 and Good Intentions",
        "content": read_article("/root/.openclaw/workspace/article-nonprofit-magic-math.md"),
        "tags": ["nonprofit", "mathematics", "social-impact", "humor"]
    }
]

published_count = 0
for i, article in enumerate(articles, 1):
    print(f"\n📝 Publishing article {i}/3...")
    result = publish(article["title"], article["content"], article.get("tags", []))
    if result:
        published_count += 1

print("\n" + "=" * 50)
print(f"🎉 Publishing complete! {published_count}/3 articles successfully published")
print("📈 Dollar Agency continues toward 130+ article target")