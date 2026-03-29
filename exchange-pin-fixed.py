#!/usr/bin/env python3
import tweepy
import json
import sys

consumer_key = "C0YSGcxu0c2DoQFhrMozI3vC7"
consumer_secret = "DzKL6u8sEj28mWiLHoW2UNrpj439bXd4Oj51nHL8V3XMgnZkTb"
request_token = "ihvrgQAAAAAB8naMAAABnTbjuDM"
request_token_secret = "arFdDiw1lq070t0TRgWGi35naBYZxPxA"

def exchange_pin(pin):
    """Exchange PIN for Access Token"""
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
        
        auth.get_access_token(pin)
        
        access_token = auth.access_token
        access_token_secret = auth.access_token_secret
        
        print(f"✓ Access Token: {access_token}")
        print(f"✓ Access Token Secret: {access_token_secret}")
        
        # Test
        api = tweepy.API(auth)
        user = api.verify_credentials()
        print(f"✓ Authenticated as: @{user.screen_name} (ID: {user.id})")
        
        # Save to config
        config = {
            "platform": "twitter",
            "provider": "x.com",
            "api_version": "1.1",
            "credentials": {
                "api_key": consumer_key,
                "api_secret": consumer_secret,
                "access_token": access_token,
                "access_token_secret": access_token_secret
            },
            "created_at": "2026-03-28T23:57:00Z"
        }
        
        with open('/root/.openclaw/workspace/secrets/twitter-api-working.json', 'w') as f:
            json.dump(config, f, indent=2)
        
        print(f"✓ Saved to secrets/twitter-api-working.json")
        
        return access_token, access_token_secret
        
    except Exception as e:
        print(f"✗ Error: {e}")
        import traceback
        traceback.print_exc()
        return None, None

if __name__ == "__main__":
    if len(sys.argv) 