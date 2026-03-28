#!/bin/bash
# Quick Twitter OAuth 1.0a test

CONSUMER_KEY="C0YSGcxu0c2DoQFhrMozI3vC7"
CONSUMER_SECRET="DzKL6u8sEj28mWiLHoW2UNrpj439bXd4Oj51nHL8V3XMgnZkTb"
ACCESS_TOKEN="1696597015902187520-S0M7v1DmuS4hm46Syxi8YXmt4SpQT3"
ACCESS_SECRET="placeholder"

echo "Testing bearer token..."
curl -s -H "Authorization: Bearer AAAAAAAAAAAAAAAAAAAAIx28gEAAAAA%2BDBsty%2Bm1goaq5xaEO4wUwXDwoc%3DVka7G9yFFUqJzumtlk5ldlxOFcqNgX96C0Ap7UXKBiXi4JCTM7" \
  "https://api.twitter.com/2/users/me" | jq .

echo -e "\nTesting GET /2/tweets/20 with bearer..."
curl -s -H "Authorization: Bearer AAAAAAAAAAAAAAAAAAAAIx28gEAAAAA%2BDBsty%2Bm1goaq5xaEO4wUwXDwoc%3DVka7G9yFFUqJzumtlk5ldlxOFcqNgX96C0Ap7UXKBiXi4JCTM7" \
  "https://api.twitter.com/2/tweets/20" | jq .

echo -e "\nTrying OAuth 1.0a GET with consumer key..."
TIMESTAMP=$(date +%s)
NONCE=$(openssl rand -hex 16)

# OAuth 1.0a signature generation would go here, but let's test simpler
echo "Consumer key: $CONSUMER_KEY"
echo "Consumer secret: $CONSUMER_SECRET"
echo "Access token: $ACCESS_TOKEN"
echo "Access secret: $ACCESS_SECRET"

echo -e "\n\nNeed OAuth 1.0a signing library. Installing oauth..."
apt-get update && apt-get install -y oauth

# If oauth installed
oauth --consumer-key "$CONSUMER_KEY" \
      --consumer-secret "$CONSUMER_SECRET" \
      --access-token "$ACCESS_TOKEN" \
      --access-secret "$ACCESS_SECRET" \
      --url "https://api.twitter.com/2/users/me" \
      --method GET \
      --include 2>&1 | head -20