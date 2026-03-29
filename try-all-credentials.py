#!/usr/bin/env python3
import tweepy
import requests
import base64
import json

print("=== Testing All Twitter Credentials ===\n")

# OAuth 1.0a from first PDF
consumer_key = "C0YSGcxu0c2DoQFhrMozI3vC7"
consumer_secret = "DzKL6u8sEj28mWiLHoW2UNrpj439bXd4Oj51nHL8V3XMgnZkTb"
access_token_v1 = "AAAAAAAAAAAAAAAAAAAAAIx28gEAAAAA%2BDBsty%2Bm1goaq5xaEO4wUwXDwoc%3DVka7G9yFFUqJzumtlk5ldlxOFcqNgX96C0Ap7UXKBiXi4JCTM7"
access_token_secret_v1 = "k0TLhVmqHuWv2dDs4CmJM74YjQlPXUdfRanvYpp1iEVbWCH9rs"

# OAuth 2.0 from roof.pdf
client_id = "JAFV2NngVbF-y_CFDzZC:1:ci"
client_secret = "f95GkAm3WMh9FbmOWLsmzatyYKUrvr6id5I54DtoXdvESQu4Or"
access_token_v2 = "4O88_9kYjKm4sSmxFfQaaKoB_JcfEk1qBHaZWTNI3JdXn:1774740054633:1:0:at:1"
refresh_token = "6P3X3jE5zRlzZfdOpAFflvm5iDhVQqG7DAijlUULaaVhd:1774740054633:1:0:rt:1"

# Bearer token
bearer_token = "z_ekmPcCZkpoKv7ij3-I:1:ci"

print("1. Testing OAuth 1.0a with Access Token...")
try:
    auth = tweepy.OAuth1UserHandler(
        consumer_key,
        consumer_secret,
        access_token_v1,
        access_token_secret_v1
    )
    api = tweepy.API(auth)
    user = api.verify_credentials()
    print(f"   ✓ Authenticated as: @{user.screen_name}")
except Exception as e:
    print(f"   ✗ Failed: {type(e).__name__}: {e}")

print("\n2. Testing Bearer Token (App-only)...")
headers = {"Authorization": f"Bearer {bearer_token}"}
response = requests.get("https://api.twitter.com/2/tweets/search/recent?query=test", headers=headers)
print(f"   Status: {response.status_code}")
if response.status_code == 200:
    print(f"   ✓ Bearer token works!")
else:
    print(f"   ✗ Failed: {response.text[:100]}...")

print("\n3. Testing OAuth 2.0 Access Token (User Context)...")
access_token_part = access_token_v2.split(':')[0]
headers = {"Authorization": f"Bearer {access_token_part}"}
response = requests.get("https://api.twitter.com/2/users/me", headers=headers)
print(f"   Status: {response.status_code}")
if response.status_code == 200:
    print(f"   ✓ OAuth 2.0 User Context works!")
    data = response.json()
    print(f"   User: {data}")
else:
    print(f"   ✗ Failed: {response.text[:200]}...")

print("\n=== Summary ===")
print("OAuth 1.0a: Need PIN flow (stuck)")
print("OAuth 2.0: Invalid client or expired")
print("Bearer: App-only (can't post)")
print("\nSolution: Need fresh OAuth 1.0a PIN or new app registration")