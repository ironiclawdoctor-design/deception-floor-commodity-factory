#!/usr/bin/env python3
import sys
import json
import requests
import time
from urllib.parse import quote

USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"

def search_reddit(query, subreddit=None):
    """Search Reddit using JSON endpoint."""
    base = "https://www.reddit.com"
    if subreddit:
        url = f"{base}/r/{subreddit}/search.json?q={quote(query)}&restrict_sr=on&limit=10"
    else:
        url = f"{base}/search.json?q={quote(query)}&limit=10"
    headers = {"User-Agent": USER_AGENT}
    try:
        resp = requests.get(url, headers=headers, timeout=10)
        resp.raise_for_status()
        return resp.json()
    except Exception as e:
        print(f"Error searching Reddit: {e}")
        return None

def search_hackernews(query):
    """Search HackerNews via Algolia."""
    url = f"https://hn.algolia.com/api/v1/search?query={quote(query)}&tags=story,comment&hitsPerPage=10"
    try:
        resp = requests.get(url, timeout=10)
        resp.raise_for_status()
        return resp.json()
    except Exception as e:
        print(f"Error searching HN: {e}")
        return None

def main():
    queries = [
        "OpenRouter affiliate",
        "OpenRouter referral",
        "OpenRouter discount",
        "OpenRouter promo code",
        "OpenRouter partner program",
        "OpenRouter credits free",
        "OpenRouter coupon"
    ]
    
    results = {}
    
    for q in queries:
        print(f"Searching: {q}")
        # Reddit
        reddit_data = search_reddit(q, subreddit="OpenRouter")
        if reddit_data and 'data' in reddit_data:
            posts = reddit_data['data']['children']
            results[f"reddit:{q}"] = [p['data'] for p in posts if 'data' in p]
        
        # HackerNews
        hn_data = search_hackernews(q)
        if hn_data and 'hits' in hn_data:
            results[f"hn:{q}"] = hn_data['hits']
        
        time.sleep(1)  # be polite
    
    # Save results
    with open('/root/.openclaw/workspace/search_results.json', 'w') as f:
        json.dump(results, f, indent=2)
    print("Saved to search_results.json")
    
    # Print summary
    for key, val in results.items():
        print(f"{key}: {len(val)} items")

if __name__ == "__main__":
    main()