#!/usr/bin/env python3
import tweepy
import json

# Consumer key/secret from PDF
consumer_key = "C0YSGcxu0c2DoQFhrMozI3vC7"
consumer_secret = "DzKL6u8sEj28mWiLHoW2UNrpj439bXd4Oj51nHL8V3XMgnZkTb"

print("Generating new Twitter OAuth 1.0a request token...")
print(f"Consumer Key: {consumer_key}")
print(f"Consumer Secret: {consumer_secret[:10]}...")

try:
    # OAuth 1.0a
    auth = tweepy.OAuth1UserHandler(
        consumer_key,
        consumer_secret,
        callback="oob"  # out-of-band (PIN)
    )
    
    # Get request token
    request_token_url = auth.get_authorization_url()
    print(f"\n1. Request Token URL: {request_token_url}")
    print("2. Visit this URL in browser")
    print("3. Authorize the app")
    print("4. You'll get a 7-digit PIN")
    print("5. Send PIN to complete auth")
    
    # Save for later
    request_token = auth.request_token["oauth_token"]
    request_token_secret = auth.request_token["oauth_token_secret"]
    print(f"\nRequest Token: {request_token}")
    print(f"Request Token Secret: {request_token_secret}")
    
except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()