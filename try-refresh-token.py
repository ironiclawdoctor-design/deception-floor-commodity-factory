#!/usr/bin/env python3
import requests
import base64
import json

client_id = "JAFV2NngVbF-y_CFDzZC:1:ci"
client_secret = "f95GkAm3WMh9FbmOWLsmzatyYKUrvr6id5I54DtoXdvESQu4Or"
refresh_token = "6P3X3jE5zRlzZfdOpAFflvm5iDhVQqG7DAijlUULaaVhd:1774740054633:1:0:rt:1"

# Extract token part
refresh_token_part = refresh_token.split(':')[0]
print(f"Refresh Token: {refresh_token_part[:30]}...")

# Twitter OAuth 2.0 token endpoint
token_url = "https://api.twitter.com/2/oauth2/token"

# Basic auth with client credentials
auth_str = base64.b64encode(f"{client_id}:{client_secret}".encode()).decode()

headers = {
    "Authorization": f"Basic {auth_str}",
    "Content-Type": "application/x-www-form-urlencoded"
}

data = {
    "grant_type": "refresh_token",
    "refresh_token": refresh_token_part,
    "client_id": client_id
}

print("Attempting refresh token flow...")
response = requests.post(token_url, headers=headers, data=data)
print(f"Status: {response.status_code}")
print(f"Response: {response.text}")

if response.status_code == 200:
    tokens = response.json()
    print(f"New Access Token: {tokens.get('access_token', '')[:30]}...")
    print(f"Refresh Token: {tokens.get('refresh_token', '')[:30]}...")
    print(f"Expires in: {tokens.get('expires_in', '')} seconds")
else:
    print("✗ Refresh failed")
    
    # Maybe need full refresh token with colons
    print("\n--- Trying with full refresh token ---")
    data2 = {
        "grant_type": "refresh_token",
        "refresh_token": refresh_token,
        "client_id": client_id
    }
    response2 = requests.post(token_url, headers=headers, data=data2)
    print(f"Status: {response2.status_code}")
    print(f"Response: {response2.text[:200]}...")