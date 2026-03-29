#!/usr/bin/env python3
import tweepy
import json
import sys

# Consumer key/secret from PDF
consumer_key = "C0YSGcxu0c2DoQFhrMozI3vC7"
consumer_secret = "DzKL6u8sEj28mWiLHoW2UNrpj439bXd4Oj51nHL8V3XMgnZkTb"

# Request token from generation
request_token = "o5xcEAAAAAAB8naMAAABnTbeVhg"
request_token_secret = "9nBWzkfoaVQ44ZHoAxg2GqHMl7E0Xiw7"

def get_access_token(pin):
    """Exchange PIN for Access Token"""
    try:
        auth = tweepy.OAuth1UserHandler(
            consumer_key,
            consumer_secret,
            callback="oob"
        )
        
        # Set request token
        auth.request_token = {
            'oauth_token': request_token,
            'oauth_token_secret': request_token_secret
        }
        
        # Get access token
        auth.get_access_token(pin)
        
        access_token = auth.access_token
        access_token_secret = auth.access_token_secret
        
        print(f"✓ Access Token: {access_token}")
        print(f"✓ Access Token Secret: {access_token_secret}")
        
        # Test credentials
        api = tweepy.API(auth)
        user = api.verify_credentials()
        print(f"✓ Authenticated as: @{user.screen_name} (ID: {user.id})")
        
        return access_token, access_token_secret
        
    except Exception as e:
        print(f"✗ Error: {e}")
        import traceback
        traceback.print_exc()
        return None, None

if __name__ == "__main__":
    if len(sys.argv) 