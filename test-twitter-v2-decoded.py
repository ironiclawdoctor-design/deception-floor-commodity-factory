#!/usr/bin/env python3
import tweepy
import json

# Decoded OAuth 2.0 credentials from PDF
client_id = "JAFV2NngVbF-y_CFDzZC:1:ci"
client_secret = "f95GkAm3WMh9FbmOWLsmzatyYKUrvr6id5I54DtoXdvESQu4Or"
access_token = "4O88_9kYjKm4sSmxFfQaaKoB_JcfEk1qBHaZWTNI3JdXn:1774740054633:1:0:at:1"
refresh_token = "6P3X3jE5zRlzZfdOpAFflvm5iDhVQqG7DAijlUULaaVhd:1774740054633:1:0:rt:1"

print("Testing Twitter OAuth 2.0 credentials (decoded)...")
print(f"Client ID: {client_id}")
print(f"Client Secret: {client_secret[:10]}...")
print(f"Access Token: {access_token[:30]}...")
print(f"Refresh Token: {refresh_token[:30]}...")

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
    
    # Test tweet
    # response = client.create_tweet(text="Test tweet from Fiesta Agency OAuth 2.0")
    # print(f"✓ Tweet posted: {response.data['id']}")
    
except Exception as e:
    print(f"✗ Error: {e}")
    import traceback
    traceback.print_exc()