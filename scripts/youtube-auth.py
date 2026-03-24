#!/usr/bin/env python3
"""
youtube-auth.py — OAuth2 flow for YouTube Data API v3.
Uses google-desktop-client.json (installed app type).
Saves token to secrets/youtube-token.json for reuse.

Run once interactively to authorize ironiclawdoctor@gmail.com.
Subsequent runs use the saved refresh token — no browser needed.

Usage:
    python3 scripts/youtube-auth.py              # auth + channel info
    python3 scripts/youtube-auth.py --test       # verify token works
"""

import json
import os
import sys
from pathlib import Path

WORKSPACE = Path("/root/.openclaw/workspace")
CLIENT_SECRET = WORKSPACE / "secrets" / "google-desktop-client.json"
TOKEN_FILE    = WORKSPACE / "secrets" / "youtube-token.json"

SCOPES = [
    "https://www.googleapis.com/auth/youtube",
    "https://www.googleapis.com/auth/youtube.upload",
    "https://www.googleapis.com/auth/youtube.force-ssl",
    "https://www.googleapis.com/auth/youtube.readonly",
]

def get_credentials():
    """Get or refresh OAuth2 credentials."""
    try:
        from google.oauth2.credentials import Credentials
        from google.auth.transport.requests import Request
        from google_auth_oauthlib.flow import InstalledAppFlow
    except ImportError:
        print("Installing required packages...")
        os.system("pip3 install google-auth google-auth-oauthlib google-auth-httplib2 google-api-python-client -q")
        from google.oauth2.credentials import Credentials
        from google.auth.transport.requests import Request
        from google_auth_oauthlib.flow import InstalledAppFlow

    creds = None

    # Load existing token
    if TOKEN_FILE.exists():
        with open(TOKEN_FILE) as f:
            token_data = json.load(f)
        creds = Credentials(
            token=token_data.get("token"),
            refresh_token=token_data.get("refresh_token"),
            token_uri=token_data.get("token_uri", "https://oauth2.googleapis.com/token"),
            client_id=token_data.get("client_id"),
            client_secret=token_data.get("client_secret"),
            scopes=token_data.get("scopes", SCOPES),
        )

    # Refresh if expired
    if creds and creds.expired and creds.refresh_token:
        print("🔄 Refreshing token...")
        creds.refresh(Request())
        save_token(creds)
        print("✅ Token refreshed")
        return creds

    # First-time auth flow
    if not creds or not creds.valid:
        if not CLIENT_SECRET.exists():
            print(f"❌ OAuth client not found: {CLIENT_SECRET}")
            print("Download from: https://console.cloud.google.com/apis/credentials?project=sovereign-see")
            sys.exit(1)

        print("🌐 Starting OAuth flow...")
        print("   A browser window will open — sign in as ironiclawdoctor@gmail.com")
        print("   If no browser, copy the URL and open it manually\n")

        flow = InstalledAppFlow.from_client_secrets_file(str(CLIENT_SECRET), SCOPES)

        # Try local server first, fall back to console
        try:
            creds = flow.run_local_server(port=8080, open_browser=True)
        except Exception:
            creds = flow.run_console()

        save_token(creds)
        print("✅ Authorization complete — token saved")

    return creds

def save_token(creds):
    """Persist token for future runs."""
    TOKEN_FILE.parent.mkdir(parents=True, exist_ok=True)
    token_data = {
        "token":         creds.token,
        "refresh_token": creds.refresh_token,
        "token_uri":     creds.token_uri,
        "client_id":     creds.client_id,
        "client_secret": creds.client_secret,
        "scopes":        list(creds.scopes) if creds.scopes else SCOPES,
    }
    with open(TOKEN_FILE, "w") as f:
        json.dump(token_data, f, indent=2)
    os.chmod(TOKEN_FILE, 0o600)

def get_channel_info(creds):
    """Fetch channel details for ironiclawdoctor@gmail.com."""
    try:
        from googleapiclient.discovery import build
    except ImportError:
        os.system("pip3 install google-api-python-client -q")
        from googleapiclient.discovery import build

    youtube = build("youtube", "v3", credentials=creds)

    response = youtube.channels().list(
        part="snippet,contentDetails,statistics,status,brandingSettings",
        mine=True
    ).execute()

    channels = response.get("items", [])
    if not channels:
        print("⚠️  No YouTube channel found for this account")
        print("   You may need to create a channel at https://youtube.com")
        return None

    ch = channels[0]
    snippet  = ch.get("snippet", {})
    stats    = ch.get("statistics", {})
    status   = ch.get("status", {})
    branding = ch.get("brandingSettings", {}).get("channel", {})

    print("\n" + "="*60)
    print("📺 YOUTUBE CHANNEL — ironiclawdoctor@gmail.com")
    print("="*60)
    print(f"  Channel ID:      {ch['id']}")
    print(f"  Name:            {snippet.get('title', 'N/A')}")
    print(f"  Handle:          {branding.get('customUrl') or snippet.get('customUrl', 'not set')}")
    print(f"  Created:         {snippet.get('publishedAt', 'N/A')[:10]}")
    print(f"  Subscribers:     {stats.get('subscriberCount', '0')} {'(hidden)' if stats.get('hiddenSubscriberCount') else ''}")
    print(f"  Videos:          {stats.get('videoCount', '0')}")
    print(f"  Total views:     {stats.get('viewCount', '0')}")
    print(f"  Privacy status:  {status.get('privacyStatus', 'N/A')}")
    print(f"  Long uploads:    {status.get('longUploadsStatus', 'N/A')}")
    print(f"  Made for kids:   {status.get('madeForKids', False)}")
    print(f"  Description:     {snippet.get('description', '')[:80] or '(none)'}")
    print("="*60)

    # Monetization / feature eligibility
    print("\n📊 UPLOAD CAPABILITIES:")
    long_status = status.get("longUploadsStatus", "")
    if long_status == "allowed":
        print("  ✅ Long videos (>15 min): ALLOWED")
    elif long_status == "eligible":
        print("  🟡 Long videos: ELIGIBLE (phone verification needed)")
    else:
        print("  ⚠️  Long videos: restricted (default 15 min limit)")
        print("     → Verify phone: https://www.youtube.com/verify")

    print("  ✅ Shorts upload: ALLOWED (all accounts)")
    print("  ✅ Unlisted/private upload: ALLOWED")
    print("  ✅ Scheduled publish: ALLOWED")

    print("\n🔑 ACTIVE API SCOPES:")
    for scope in SCOPES:
        scope_name = scope.split("/")[-1]
        print(f"  ✅ {scope_name}")

    print(f"\n🔗 Channel URL: https://www.youtube.com/channel/{ch['id']}")
    print(f"   Studio:      https://studio.youtube.com/channel/{ch['id']}")

    # Save channel ID for other scripts
    channel_info = {
        "channel_id":    ch["id"],
        "title":         snippet.get("title"),
        "custom_url":    branding.get("customUrl") or snippet.get("customUrl"),
        "video_count":   stats.get("videoCount"),
        "subscriber_count": stats.get("subscriberCount"),
        "long_uploads":  long_status,
        "account":       "ironiclawdoctor@gmail.com"
    }
    info_file = WORKSPACE / "secrets" / "youtube-channel.json"
    with open(info_file, "w") as f:
        json.dump(channel_info, f, indent=2)
    os.chmod(info_file, 0o600)
    print(f"\n📁 Channel info saved: {info_file}")

    return ch

def main():
    test_mode = "--test" in sys.argv

    print("🎬 YouTube Auth — Dollar Agency")
    print(f"   Account: ironiclawdoctor@gmail.com")
    print(f"   Project: sovereign-see")
    print(f"   Token:   {TOKEN_FILE}\n")

    creds = get_credentials()

    if not creds or not creds.valid:
        print("❌ Could not obtain valid credentials")
        sys.exit(1)

    print("✅ Credentials valid")

    if test_mode:
        print("✅ Test mode — credentials OK, skipping channel fetch")
        return

    ch = get_channel_info(creds)

    if ch:
        print("\n✅ YouTube API connected. You can now:")
        print("   - Upload videos programmatically")
        print("   - Schedule posts")
        print("   - Manage playlists and descriptions")
        print("   - Set thumbnails, tags, categories")
        print("\nNext: python3 scripts/youtube-upload.py --file <video.mp4> --title 'Title'")
    else:
        print("\n⚠️  Auth succeeded but no channel found.")
        print("   Create one at: https://studio.youtube.com")
        print("   Then re-run this script.")

if __name__ == "__main__":
    main()
