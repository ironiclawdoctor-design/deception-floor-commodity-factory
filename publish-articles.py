#!/usr/bin/env python3
"""
Script to publish articles to Hashnode
"""

import requests
import json
import sys
import time

def publish_article(title, content, tags):
    """Publish an article to Hashnode"""
    
    # GraphQL mutation for publishing
    mutation = """
    mutation CreatePublication($input: CreatePublicationInput!) {
      createPublication(input: $input) {
        publication {
          id
          title
          url
          publishedAt
        }
      }
    }
    """
    
    # Prepare the article content
    article_input = {
        "title": title,
        "content": content,
        "tags": tags,
        "isPublic": True,
        "publicationId": "dollaragency"  # Using the publication ID from memory
    }
    
    # GraphQL endpoint
    url = 'https://api.hashnode.com/graphql'
    
    headers = {
        'Content-Type': 'application/json',
        'User-Agent': 'DollarAgency/1.0'
    }
    
    try:
        response = requests.post(url, json={
            'query': mutation,
            'variables': {'input': article_input}
        }, headers=headers, timeout=30)
        
        print(f"Publishing '{title}'...")
        print(f"Response Status: {response.status_code}")
        print(f"Response: {response.text[:300]}...")
        
        if response.status_code == 200:
            data = response.json()
            if 'data' in data and 'createPublication' in data['data']:
                publication = data['data']['createPublication']['publication']
                print(f"Successfully published: {publication['title']}")
                print(f"URL: {publication['url']}")
                print(f"Published At: {publication.get('publishedAt', 'N/A')}")
                return publication
            else:
                print(f"Error in response: {data}")
                return None
        else:
            print(f"HTTP Error: {response.status_code}")
            print(f"Response: {response.text}")
            return None
            
    except Exception as e:
        print(f"Error publishing article: {e}")
        return None

def main():
    """Publish all three articles"""
    
    # Article data
    articles = [
        {
            'title': 'The AI Allocation Paradox: Why More Intelligence Sometimes Means Less Progress',
            'content': open('article-ai-allocation-paradox.md', 'r').read(),
            'tags': ['AI', 'Machine Learning', 'Optimization', 'Philosophy']
        },
        {
            'title': 'NYC Cognitive Patterns: 7 Mental Algorithms That Keep You Sane (or at least functional)',
            'content': open('article-nyc-cognitive-patterns.md', 'r').read(),
            'tags': ['NYC', 'Psychology', 'Urban Life', 'Cognitive Science']
        },
        {
            'title': 'Non-Profit Resource Alchemy: Turning $0.07 Into Impact (And Other Modern Miracles)',
            'content': open('article-nonprofit-resource-alchemy.md', 'r').read(),
            'tags': ['Nonprofit', 'Resource Management', 'Social Impact', 'Innovation']
        }
    ]
    
    published_articles = []
    
    for i, article in enumerate(articles, 1):
        print(f"\n=== Publishing Article {i}/{len(articles)} ===")
        
        # Extract first 500 chars for preview to avoid huge logs
        content_preview = article['content'][:500] + "..." if len(article['content']) > 500 else article['content']
        print(f"Title: {article['title']}")
        print(f"Content Preview: {content_preview}")
        print(f"Tags: {', '.join(article['tags'])}")
        
        # Try to publish
        result = publish_article(article['title'], article['content'], article['tags'])
        
        if result:
            published_articles.append(result)
            print(f"✅ SUCCESS: {result['title']}")
        else:
            print(f"❌ FAILED: {article['title']}")
        
        # Small delay between requests
        if i < len(articles):
            time.sleep(2)
    
    print(f"\n=== SUMMARY ===")
    print(f"Successfully published: {len(published_articles)}/{len(articles)}")
    
    for pub in published_articles:
        print(f"- {pub['title']}: {pub['url']}")

if __name__ == "__main__":
    main()