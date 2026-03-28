#!/usr/bin/env python3
"""
Twitter OAuth 1.0a poster for API v2
"""
import os
import sys
import json
from requests_oauthlib import OAuth1Session

def load_credentials():
    """Load credentials from secrets/twitter-api.json"""
    secrets_path = "/root/.openclaw/workspace/secrets/twitter-api.json"
    if not os.path.exists(secrets_path):
        print("ERROR: Secret file not found:", secrets_path, file=sys.stderr)
        sys.exit(1)
    
    with open(secrets_path, 'r') as f:
        data = json.load(f)
    
    creds = data.get('credentials', {})
    required = ['api_key', 'api_secret', 'access_token', 'access_token_secret']
    missing = [k for k in required if not creds.get(k)]
    if missing:
        print(f"ERROR: Missing credentials: {missing}", file=sys.stderr)
        sys.exit(1)
    
    return {
        'api_key': creds['api_key'],
        'api_secret': creds['api_secret'],
        'access_token': creds['access_token'],
        'access_token_secret': creds['access_token_secret']
    }

def post_tweet(text, dry_run=False):
    """Post tweet using OAuth 1.0a"""
    creds = load_credentials()
    
    # Create OAuth1 session
    twitter = OAuth1Session(
        creds['api_key'],
        client_secret=creds['api_secret'],
        resource_owner_key=creds['access_token'],
        resource_owner_secret=creds['access_token_secret']
    )
    
    url = "https://api.twitter.com/2/tweets"
    payload = {"text": text}
    
    if dry_run:
        print(f"[DRY RUN] Would POST to {url}")
        print(json.dumps(payload, indent=2))
        return {"dry_run": True}
    
    print(f"Posting tweet: {text[:50]}...")
    response = twitter.post(url, json=payload)
    
    if response.status_code == 201:
        data = response.json()
        tweet_id = data.get('data', {}).get('id')
        print(f"✅ Success! Tweet ID: {tweet_id}")
        print(f"   URL: https://twitter.com/i/web/status/{tweet_id}")
        return data
    else:
        print(f"❌ Error {response.status_code}: {response.text}", file=sys.stderr)
        return {"error": response.text, "status": response.status_code}

def main():
    if len(sys.argv) 