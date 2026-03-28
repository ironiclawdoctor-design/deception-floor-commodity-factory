#!/usr/bin/env python3
import tweepy
import json

# Load OAuth 1.0a credentials from PDF
api_key = "C0YSGcxu0c2DoQFhrMozI3vC7"
api_secret = "DzKL6u8sEj28mWiLHoW2UNrpj439bXd4Oj51nHL8V3XMgnZkTb"
bearer_token = "el9la21QY0Naa3BvS3Y3aWozLUk6MTpjaQ"
access_token = "AAAAAAAAAAAAAAAAAAAAAIx28gEAAAAA%2BDBsty%2Bm1goaq5xaEO4wUwXDwoc%3DVka7G9yFFUqJzumtlk5ldlxOFcqNgX96C0Ap7UXKBiXi4JCTM7"
access_token_secret = "k0TLhVmqHuWv2dDs4CmJM74YjQlPXUdfRanvYpp1iEVbWCH9rs"

print("Testing Twitter OAuth 1.0a credentials...")
print(f"API Key: {api_key[:10]}...")
print(f"API Secret: {api_secret[:10]}...")
print(f"Bearer Token: {bearer_token[:20]}...")
print(f"Access Token: {access_token[:20]}...")
print(f"Access Token Secret: {access_token_secret[:20]}...")

try:
    # OAuth 1.0a client
    auth = tweepy.OAuth1UserHandler(
        consumer_key=api_key,
        consumer_secret=api_secret,
        access_token=access_token,
        access_token_secret=access_token_secret
    )
    
    api = tweepy.API(auth)
    me = api.verify_credentials()
    print(f"✓ Authenticated as: @{me.screen_name} (ID: {me.id})")
    print("✓ OAuth 1.0a credentials valid!")
    
    # Try posting
    # tweet = api.update_status("Test tweet from Fiesta Agency OAuth 1.0a")
    # print(f"✓ Tweet posted: {tweet.id}")
    
except Exception as e:
    print(f"✗ Error: {e}")
    import traceback
    traceback.print_exc()