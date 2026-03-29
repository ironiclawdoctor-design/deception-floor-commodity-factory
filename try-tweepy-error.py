#!/usr/bin/env python3
import tweepy
import json

consumer_key = "C0YSGcxu0c2DoQFhrMozI3vC7"
consumer_secret = "DzKL6u8sEj28mWiLHoW2UNrpj439bXd4Oj51nHL8V3XMgnZkTb"
request_token = "o5xcEAAAAAAB8naMAAABnTbeVhg"
request_token_secret = "9nBWzkfoaVQ44ZHoAxg2GqHMl7E0Xiw7"

print("Testing Twitter OAuth 1.0a flow...")
print(f"Consumer Key: {consumer_key}")
print(f"Request Token: {request_token}")

try:
    auth = tweepy.OAuth1UserHandler(
        consumer_key,
        consumer_secret,
        callback="oob"
    )
    
    auth.request_token = {
        'oauth_token': request_token,
        'oauth_token_secret': request_token_secret
    }
    
    # Try with dummy PIN to see error
    pin = "1234567"
    print(f"\nTrying with dummy PIN: {pin}")
    
    try:
        auth.get_access_token(pin)
        print("SUCCESS (unexpected!)")
    except tweepy.errors.TweepyException as e:
        print(f"Expected error (wrong PIN): {type(e).__name__}: {e}")
        
        # Check if it's a 401 unauthorized vs 403 forbidden
        if "401" in str(e):
            print("→ 401: Invalid/expired request token")
        elif "403" in str(e):
            print("→ 403: App permissions insufficient")
        else:
            print(f"→ Other error: {e}")
            
except Exception as e:
    print(f"Setup error: {e}")
    import traceback
    traceback.print_exc()