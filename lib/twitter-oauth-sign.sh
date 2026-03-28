#!/bin/bash
# Twitter OAuth 1.0a signature generator for API v2
# Based on: https://developer.twitter.com/en/docs/authentication/oauth-1-0a

set -euo pipefail

# Load credentials
source "$(dirname "$0")/secrets-loader.sh"

API_KEY=$(load_secret "twitter-api" "credentials.api_key")
API_SECRET=$(load_secret "twitter-api" "credentials.api_secret")
ACCESS_TOKEN=$(load_secret "twitter-api" "credentials.access_token")
ACCESS_TOKEN_SECRET=$(load_secret "twitter-api" "credentials.access_token_secret")

# Generate OAuth 1.0a signature
# $1 = HTTP method (GET, POST)
# $2 = URL
# $3 = POST data (JSON) - optional
generate_oauth_signature() {
    local method="$1"
    local url="$2"
    local post_data="${3:-}"
    
    # OAuth parameters
    local timestamp=$(date +%s)
    local nonce=$(head -c 32 /dev/urandom | base64 | tr -dc 'a-zA-Z0-9')
    
    # Percent encode everything
    local encoded_api_key=$(urlencode "$API_KEY")
    local encoded_api_secret=$(urlencode "$API_SECRET")
    local encoded_access_token=$(urlencode "$ACCESS_TOKEN")
    local encoded_access_token_secret=$(urlencode "$ACCESS_TOKEN_SECRET")
    
    # Generate signature (simplified - real implementation needs proper signature base string)
    echo "Authorization: OAuth oauth_consumer_key=\"$encoded_api_key\", oauth_nonce=\"$nonce\", oauth_signature=\"PLACEHOLDER\", oauth_signature_method=\"HMAC-SHA1\", oauth_timestamp=\"$timestamp\", oauth_token=\"$encoded_access_token\", oauth_version=\"1.0\""
}

# URL encode function
urlencode() {
    local string="$1"
    local length="${#string}"
    local result=""
    local i
    
    for ((i = 0; i 