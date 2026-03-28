#!/usr/bin/env python3
"""
Exchange Twitter OAuth PIN for Access Token
"""
import json
import sys
from requests_oauthlib import OAuth1Session

def main():
    if len(sys.argv) 