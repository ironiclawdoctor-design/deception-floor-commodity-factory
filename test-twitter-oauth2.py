#!/usr/bin/env python3
import tweepy
import json

# OAuth 2.0 credentials from PDF
client_id = "SkFGVjJObmdWYkYteV9DRkR6WkM6MTpjaQ"
client_secret = "f95GkAm3WMh9FbmOWLsmzatyYKUrvr6id5I54DtoXdvESQu4Or"
access_token = "NE84OF85a1lqS200c1NteEZmUWFhS29CX0pjZkVrMXFCSGFaV1ROSTNKZFhuOjE3NzQ3NDAwNTQ2MzM6MTowOmF0OjE"
refresh_token = "NlAzWDNqRTV6Umx6WmZkT3BBRmZsdm01aURoVlFxRzdEQWlqbFVVTGFhVmhkOjE3NzQ3NDAwNTQ2MzM6MTowOnJ0OjE"

print("Testing Twitter OAuth 2.0 credentials...")
print(f"Client ID: {client_id[:10]}...")
print(f"Client Secret: {client_secret[:10]}...")
print(f"Access Token: {access_token[:20]}...")
print(f"Refresh Token: {refresh_token[:20]}...")

# Try v2 API with OAuth 2.0
try:
    client = tweepy.Client(
        bearer_token=None,  # OAuth 2.0 uses access_token
        consumer_key=client_id,
        consumer_secret=client_secret,
        access_token=access_token,
        access_token_secret=None,  # Not used in OAuth 2.0
        wait_on_rate_limit=True
    )
    
    # Test API call
    me = client.get_me()
    print(f"✓ Authenticated as: @{me.data.username} (ID: {me.data.id})")
    
    # Try posting a test tweet (dry run)
    # response = client.create_tweet(text="Test tweet from Fiesta Agency OAuth 2.0")
    # print(f"✓ Tweet posted: {response.data['id']}")
    
    print("✓ OAuth 2.0 credentials valid!")
    
except Exception as e:
    print(f"✗ Error: {e}")
    import traceback
    traceback.print_exc()