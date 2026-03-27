#!/usr/bin/env python3
"""
Script to publish Hashnode articles via GraphQL API
"""

import requests
import json
import time
from datetime import datetime, timezone

# API configuration
API_KEY = "2824c3af-2b0f-4836-9185-7e9d4547e304"
PUBLICATION_ID = "69c07db4d9da55a9a5fa1ab6"
BASE_URL = "https://gql.hashnode.com/"

# Article metadata
articles = [
    {
        "title": "The Art of Being Unproductive: How AI Agents Master the Art of Doing Nothing",
        "slug": "ai-agents-unproductive-genius",
        "content": open("article-ai-unproductive-genius.md", "r").read(),
        "tags": ["AI", "Machine Learning", "Programming", "Humor", "Productivity"]
    },
    {
        "title": "The NYC Survival Guide: How to Thrive When the System is Working Against You",
        "slug": "nyc-survival-guide-chaos",
        "content": open("article-nyc-survival-guide.md", "r").read(),
        "tags": ["NYC", "Life", "Urban Living", "Survival", "Humor"]
    },
    {
        "title": "The Non-Profit Operating Manual: How to Run an Organization on $0.07 and Good Intentions",
        "slug": "nonprofit-shoestring-budget-guide",
        "content": open("article-nonprofit-shoestring-budget.md", "r").read(),
        "tags": ["Nonprofit", "Management", "Leadership", "Social Impact", "Humor"]
    }
]

def create_mutation(article):
    """Create GraphQL mutation for publishing an article"""
    tags = [{"name": tag} for tag in article["tags"]]
    
    mutation = {
        "query": """
        mutation CreatePublicationStory($input: CreatePublicationStoryInput!) {
            createPublicationStory(input: $input) {
                story {
                    id
                    title
                    slug
                    url
                    publishedAt
                }
                success
                errors {
                    message
                }
            }
        }
        """,
        "variables": {
            "input": {
                "publicationId": PUBLICATION_ID,
                "title": article["title"],
                "contentMarkdown": article["content"],
                "tags": tags,
                "isPublished": True,
                "seoTitle": article["title"],
                "seoDescription": article["title"][:150] + "..."
            }
        }
    }
    return mutation

def publish_article(article):
    """Publish a single article"""
    print(f"Publishing: {article['title']}")
    
    mutation = create_mutation(article)
    
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }
    
    try:
        response = requests.post(BASE_URL, json=mutation, headers=headers, timeout=30)
        response.raise_for_status()
        
        result = response.json()
        data = result.get("data", {})
        
        if data.get("createPublicationStory", {}).get("success"):
            story = data["createPublicationStory"]["story"]
            print(f"✅ SUCCESS: {story['title']}")
            print(f"   URL: {story['url']}")
            print(f"   Published: {story['publishedAt']}")
            return True
        else:
            errors = data.get("createPublicationStory", {}).get("errors", [])
            error_msg = errors[0]["message"] if errors else "Unknown error"
            print(f"❌ FAILED: {article['title']} - {error_msg}")
            return False
            
    except Exception as e:
        print(f"❌ ERROR publishing {article['title']}: {str(e)}")
        return False

def main():
    """Main function to publish all articles"""
    print(f"Starting article publishing at {datetime.now(timezone.utc).isoformat()}")
    print(f"API Key: {API_KEY[:10]}...")
    print(f"Publication ID: {PUBLICATION_ID}")
    print("-" * 50)
    
    success_count = 0
    total_count = len(articles)
    
    for i, article in enumerate(articles, 1):
        print(f"\n[{i}/{total_count}] {article['title']}")
        
        if publish_article(article):
            success_count += 1
        
        # Small delay between requests
        if i < total_count:
            time.sleep(2)
    
    print("\n" + "=" * 50)
    print(f"Publishing complete: {success_count}/{total_count} articles published successfully")
    
    if success_count == total_count:
        print("🎉 All articles published successfully!")
    else:
        print(f"⚠️  {total_count - success_count} articles failed to publish")

if __name__ == "__main__":
    main()