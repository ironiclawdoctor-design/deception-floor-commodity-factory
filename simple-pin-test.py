#!/usr/bin/env python3
import tweepy
import json
import sys

consumer_key = "C0YSGcxu0c2DoQFhrMozI3vC7"
consumer_secret = "DzKL6u8sEj28mWiLHoW2UNrpj439bXd4Oj51nHL8V3XMgnZkTb"
request_token = "ihvrgQAAAAAB8naMAAABnTbjuDM"
request_token_secret = "arFdDiw1lq070t0TRgWGi35naBYZxPxA"

pin = "0000000"
print(f"Testing PIN: {pin}")

try:
    auth = tweepy.OAuth1UserHandler(consumer_key, consumer_secret, callback="oob")
    auth.request_token = {'oauth_token': request_token, 'oauth_token_secret': request_token_secret}
    auth.get_access_token(pin)
    print(f"Success! Access Token: {auth.access_token[:20]}...")
    print(f"Access Token Secret: {auth.access_token_secret[:20]}...")
except Exception as e:
    print(f"Error: {e}")