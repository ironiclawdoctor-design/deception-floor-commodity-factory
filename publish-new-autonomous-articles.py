#!/usr/bin/env python3
"""
Script to publish new articles to Hashnode for Dollar Agency
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
        "publicationId": "dollaragency"
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
        
        if response.status_code == 200:
            data = response.json()
            if 'data' in data and 'createPublication' in data['data']:
                publication = data['data']['createPublication']['publication']
                print(f"✅ Successfully published: {publication['title']}")
                print(f"URL: {publication['url']}")
                print(f"Published At: {publication.get('publishedAt', 'N/A')}")
                return publication
            else:
                print(f"❌ Error in response: {data}")
                return None
        else:
            print(f"❌ HTTP Error: {response.status_code}")
            print(f"Response: {response.text}")
            return None
            
    except Exception as e:
        print(f"❌ Error publishing article: {e}")
        return None

def main():
    """Publish all three new articles"""
    
    # Article data - 3 unpublished high-quality articles
    articles = [
        {
            'title': 'The AI Agent That Thinks It\'s a Therapist (And Other Digital Delusions)',
            'content': open('article-ai-digital-delusions.md', 'r').read(),
            'tags': ['AI', 'Machine Learning', 'Humor', 'Technology', 'Psychology']
        },
        {
            'title': 'The Allocation Paradox: When You Have Too Many Ideas and Zero Resources',
            'content': open('article-allocation-paradox.md', 'r').read(),
            'tags': ['Productivity', 'Resource Management', 'Agency Life', 'Strategy', 'Decision Making']
        },
        {
            'title': 'The NYC Survival Algorithm: How to Win at Subway Roulette',
            'content': open('article-nyc-survival-algorithm.md', 'r').read(),
            'tags': ['NYC', 'Urban Life', 'Commuting', 'Humor', 'Life Hacks']
        }
    ]
    
    published_articles = []
    
    for i, article in enumerate(articles, 1):
        print(f"\n=== Publishing Article {i}/{len(articles)} ===")
        
        # Extract first 300 chars for preview to avoid huge logs
        content_preview = article['content'][:300] + "..." if len(article['content']) > 300 else article['content']
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
        
        # Small delay between requests to avoid rate limiting
        if i < len(articles):
            time.sleep(3)
    
    print(f"\n=== PUBLISHING SUMMARY ===")
    print(f"Successfully published: {len(published_articles)}/{len(articles)}")
    
    if published_articles:
        print("\n🎉 ARTICLES PUBLISHED:")
        for pub in published_articles:
            print(f"✅ {pub['title']}")
            print(f"   URL: {pub['url']}")
            print()
    
    print("Dollar Agency autonomous publishing complete!")

if __name__ == "__main__":
    main()