#!/usr/bin/env python3
import tweepy
import json

# App-only auth with Bearer Token
bearer_token = "z_ekmPcCZkpoKv7ij3-I:1:ci"  # Decoded from PDF

print("Testing Twitter Bearer Token (App-only auth)...")
print(f"Bearer Token: {bearer_token}")

try:
    client = tweepy.Client(bearer_token=bearer_token)
    
    # Get user by username
    user = client.get_user(username="DemeritAll")
    print(f"User fetched: @{user.data.username} (ID: {user.data.id})")
    
    # Try to post (will fail with app-only)
    # response = client.create_tweet(text="Test from bearer token")
    # print(f"Tweet posted: {response.data['id']}")
    
    print("✓ Bearer token valid!")
    
except tweepy.errors.Unauthorized as e:
    print(f"✗ Unauthorized: {e}")
except tweepy.errors.Forbidden as e:
    print(f"✗ Forbidden (app-only can't post): {e}")
except Exception as e:
    print(f"✗ Error: {e}")
    import traceback
    traceback.print_exc()