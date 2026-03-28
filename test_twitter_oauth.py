#!/usr/bin/env python3
"""
Test Twitter OAuth 1.0a authentication with the credentials from PDF
"""
import os
import sys
import json
from requests_oauthlib import OAuth1Session

# Load credentials
with open('/root/.openclaw/workspace/secrets/twitter-api.json', 'r') as f:
    creds = json.load(f)['credentials']

API_KEY = creds['api_key']
API_SECRET = creds['api_secret']
ACCESS_TOKEN = creds['access_token']
ACCESS_TOKEN_SECRET = creds['access_token_secret']

# Create OAuth1 session
twitter = OAuth1Session(
    API_KEY,
    client_secret=API_SECRET,
    resource_owner_key=ACCESS_TOKEN,
    resource_owner_secret=ACCESS_TOKEN_SECRET
)

# Test GET /2/users/me
print("Testing OAuth 1.0a GET /2/users/me...")
response = twitter.get("https://api.twitter.com/2/users/me")
print(f"Status: {response.status_code}")
if response.status_code == 200:
    data = response.json()
    print(json.dumps(data, indent=2))
else:
    print(f"Error: {response.text}")

# Test POST /2/tweets (dry run)
print("\n\nTesting OAuth 1.0a POST /2/tweets (dry run)...")
payload = {"text": "Testing Twitter API v2 OAuth 1.0a from agency automation"}
response = twitter.post("https://api.twitter.com/2/tweets", json=payload)
print(f"Status: {response.status_code}")
if response.status_code == 201:
    data = response.json()
    print(json.dumps(data, indent=2))
else:
    print(f"Error: {response.text}")