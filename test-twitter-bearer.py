#!/usr/bin/env python3
import tweepy
import json

# App-only auth with Bearer Token
bearer_token = "z_ekmPcCZkpoKv7ij3-I:1:ci"  # Decoded from PDF

print("Testing Twitter Bearer Token (App-only auth)...")
print(f"Bearer Token: {bearer_token}")

try:
    client = tweepy.Client(bearer_token=bearer_token)
    
    # Try to get a tweet (rate limited but should work)
    # tweet_id = "1774740054633"  # From timestamp in access token
    # tweet = client.get_tweet(id=tweet_id)
    # print(f"Tweet fetched: {tweet.data.text[:50]}...")
    
    # Get rate limits
    limits = client.get_rate_limit_status()
    print(f"Rate limits: {limits}")
    
    print("✓ Bearer token valid!")
    
except Exception as e:
    print(f"✗ Error: {e}")
    import traceback
    traceback.print_exc()