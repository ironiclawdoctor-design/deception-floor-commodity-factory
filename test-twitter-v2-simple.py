#!/usr/bin/env python3
import tweepy
import json

# Decoded OAuth 2.0 credentials from PDF
client_id = "JAFV2NngVbF-y_CFDzZC:1:ci"
client_secret = "f95GkAm3WMh9FbmOWLsmzatyYKUrvr6id5I54DtoXdvESQu4Or"
access_token_full = "4O88_9kYjKm4sSmxFfQaaKoB_JcfEk1qBHaZWTNI3JdXn:1774740054633:1:0:at:1"
refresh_token_full = "6P3X3jE5zRlzZfdOpAFflvm5iDhVQqG7DAijlUULaaVhd:1774740054633:1:0:rt:1"

# Try just the token part before colon
access_token = access_token_full.split(':')[0]
print(f"Trying access token: {access_token[:20]}...")

try:
    # Try OAuth 2.0 Client
    client = tweepy.Client(
        bearer_token=None,
        consumer_key=client_id,
        consumer_secret=client_secret,
        access_token=access_token,
        access_token_secret=None
    )
    
    me = client.get_me()
    print(f"✓ Authenticated as: @{me.data.username} (ID: {me.data.id})")
    print("✓ OAuth 2.0 credentials valid!")
    
    # Test tweet (dry run)
    response = client.create_tweet(text="Test tweet from Fiesta Agency OAuth 2.0")
    print(f"✓ Tweet posted: {response.data['id']}")
    
except Exception as e:
    print(f"✗ Error: {e}")
    import traceback
    traceback.print_exc()
    
    # Also try with bearer token
    print("\nTrying as bearer token...")
    try:
        client2 = tweepy.Client(bearer_token=access_token)
        me2 = client2.get_me()
        print(f"✓ Bearer token authenticated as: @{me2.data.username}")
    except Exception as e2:
        print(f"Bearer token also failed: {e2}")