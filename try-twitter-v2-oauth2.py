#!/usr/bin/env python3
import requests
import base64
import json

# OAuth 2.0 credentials from roof.pdf
client_id = "JAFV2NngVbF-y_CFDzZC:1:ci"
client_secret = "f95GkAm3WMh9FbmOWLsmzatyYKUrvr6id5I54DtoXdvESQu4Or"
access_token_full = "4O88_9kYjKm4sSmxFfQaaKoB_JcfEk1qBHaZWTNI3JdXn:1774740054633:1:0:at:1"
refresh_token_full = "6P3X3jE5zRlzZfdOpAFflvm5iDhVQqG7DAijlUULaaVhd:1774740054633:1:0:rt:1"

# Extract just the token part (before first colon)
access_token = access_token_full.split(':')[0]
print(f"Access Token: {access_token[:30]}...")
print(f"Timestamp: {access_token_full.split(':')[1]}")

# Try Twitter API v2 with OAuth 2.0 User Context
headers = {
    "Authorization": f"Bearer {access_token}",
    "Content-Type": "application/json"
}

# Try to get user info
print("\n--- Testing User Lookup ---")
response = requests.get(
    "https://api.twitter.com/2/users/me",
    headers=headers,
    params={"user.fields": "id,name,username"}
)
print(f"Status: {response.status_code}")
print(f"Response: {response.text[:200]}...")

if response.status_code == 200:
    data = response.json()
    print(f"✓ Authenticated as: @{data['data']['username']} (ID: {data['data']['id']})")
    
    # Try to post a tweet
    print("\n--- Testing Tweet Creation ---")
    tweet_data = {"text": "Test tweet from Fiesta Agency using OAuth 2.0"}
    tweet_response = requests.post(
        "https://api.twitter.com/2/tweets",
        headers=headers,
        json=tweet_data
    )
    print(f"Status: {tweet_response.status_code}")
    print(f"Response: {tweet_response.text}")
else:
    print("✗ Failed to authenticate")
    
    # Maybe we need to use the full token with colon format
    print("\n--- Trying with full token ---")
    headers2 = {
        "Authorization": f"Bearer {access_token_full}",
        "Content-Type": "application/json"
    }
    response2 = requests.get(
        "https://api.twitter.com/2/users/me",
        headers=headers2,
        params={"user.fields": "id,name,username"}
    )
    print(f"Status: {response2.status_code}")
    print(f"Response: {response2.text[:200]}...")