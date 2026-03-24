#!/usr/bin/env python3
"""
youtube-upload.py — Upload videos to ironiclawdoctor@gmail.com YouTube channel.
Requires: youtube-auth.py to have been run first (token in secrets/youtube-token.json)

Usage:
    python3 scripts/youtube-upload.py --file video.mp4 --title "Title" [options]

Options:
    --file          Path to video file (mp4, mov, avi, mkv)
    --title         Video title (required)
    --description   Video description (default: agency description)
    --tags          Comma-separated tags
    --category      YouTube category ID (default: 28 = Science & Tech)
    --privacy       public|unlisted|private (default: unlisted)
    --schedule      ISO timestamp to publish (e.g. 2026-03-27T14:00:00Z)
    --thumbnail     Path to thumbnail image (jpg/png)
    --shorts        Flag for YouTube Shorts (adds #Shorts to description)
"""

import argparse
import json
import os
import sys
from pathlib import Path
from datetime import datetime, timezone

WORKSPACE = Path("/root/.openclaw/workspace")
TOKEN_FILE = WORKSPACE / "secrets" / "youtube-token.json"
CHANNEL_FILE = WORKSPACE / "secrets" / "youtube-channel.json"

CATEGORY_IDS = {
    "tech":         "28",
    "education":    "27",
    "entertainment":"24",
    "news":         "25",
    "howto":        "26",
    "finance":      "25",  # News & Politics
    "people":       "22",
}

AGENCY_DESCRIPTION = """Dollar Agency — Autonomous AI Operations

Built on Shannon economy principles. Running on Ampere.sh.
Sovereign, self-funding, and getting better every cycle.

🔗 Donate: https://cash.app/$DollarAgency
📚 Skills: https://clawhub.com/ironiclawdoctor-design
📖 Articles: https://dollaragency.hashnode.dev
🤖 Bot: https://t.me/DeceptionFloorBot"""

def get_credentials():
    if not TOKEN_FILE.exists():
        print("❌ No token found. Run: python3 scripts/youtube-auth.py")
        sys.exit(1)

    try:
        from google.oauth2.credentials import Credentials
        from google.auth.transport.requests import Request
    except ImportError:
        os.system("pip3 install google-auth google-auth-oauthlib google-api-python-client -q")
        from google.oauth2.credentials import Credentials
        from google.auth.transport.requests import Request

    with open(TOKEN_FILE) as f:
        token_data = json.load(f)

    creds = Credentials(
        token=token_data.get("token"),
        refresh_token=token_data.get("refresh_token"),
        token_uri=token_data.get("token_uri", "https://oauth2.googleapis.com/token"),
        client_id=token_data.get("client_id"),
        client_secret=token_data.get("client_secret"),
        scopes=token_data.get("scopes"),
    )

    if creds.expired and creds.refresh_token:
        creds.refresh(Request())
        # Save refreshed token
        token_data["token"] = creds.token
        with open(TOKEN_FILE, "w") as f:
            json.dump(token_data, f, indent=2)

    return creds

def upload_video(args):
    from googleapiclient.discovery import build
    from googleapiclient.http import MediaFileUpload

    creds = get_credentials()
    youtube = build("youtube", "v3", credentials=creds)

    video_path = Path(args.file)
    if not video_path.exists():
        print(f"❌ File not found: {video_path}")
        sys.exit(1)

    file_size_mb = video_path.stat().st_size / 1024 / 1024
    print(f"📁 File: {video_path} ({file_size_mb:.1f} MB)")

    # Build description
    description = args.description or AGENCY_DESCRIPTION
    if args.shorts:
        description = "#Shorts\n\n" + description

    # Build tags
    tags = []
    if args.tags:
        tags = [t.strip() for t in args.tags.split(",")]
    tags += ["DollarAgency", "AIAgency", "ShannonEconomy", "AutonomousAI"]

    # Category
    category = CATEGORY_IDS.get(args.category, args.category or "28")

    body = {
        "snippet": {
            "title":       args.title,
            "description": description,
            "tags":        tags,
            "categoryId":  category,
        },
        "status": {
            "privacyStatus":          args.privacy or "unlisted",
            "selfDeclaredMadeForKids": False,
        }
    }

    # Scheduled publish
    if args.schedule:
        body["status"]["publishAt"] = args.schedule
        body["status"]["privacyStatus"] = "private"  # Required for scheduled
        print(f"⏰ Scheduled for: {args.schedule}")

    print(f"📤 Uploading: {args.title}")
    print(f"   Privacy: {body['status']['privacyStatus']}")
    print(f"   Category: {category}")
    print(f"   Tags: {', '.join(tags[:5])}...")

    media = MediaFileUpload(
        str(video_path),
        mimetype="video/*",
        resumable=True,
        chunksize=10 * 1024 * 1024  # 10MB chunks
    )

    request = youtube.videos().insert(
        part="snippet,status",
        body=body,
        media_body=media
    )

    # Upload with progress
    response = None
    while response is None:
        status, response = request.next_chunk()
        if status:
            pct = int(status.progress() * 100)
            print(f"   ↑ {pct}% uploaded...", end="\r")

    video_id = response["id"]
    print(f"\n✅ Upload complete!")
    print(f"   Video ID:  {video_id}")
    print(f"   URL:       https://www.youtube.com/watch?v={video_id}")
    print(f"   Studio:    https://studio.youtube.com/video/{video_id}/edit")

    # Upload thumbnail if provided
    if args.thumbnail:
        thumb_path = Path(args.thumbnail)
        if thumb_path.exists():
            print(f"🖼  Setting thumbnail: {thumb_path}")
            youtube.thumbnails().set(
                videoId=video_id,
                media_body=MediaFileUpload(str(thumb_path))
            ).execute()
            print("✅ Thumbnail set")

    # Log to agency
    log_entry = {
        "ts":       datetime.now(timezone.utc).isoformat(),
        "video_id": video_id,
        "title":    args.title,
        "privacy":  body["status"]["privacyStatus"],
        "url":      f"https://www.youtube.com/watch?v={video_id}",
        "file":     str(video_path),
        "size_mb":  round(file_size_mb, 2)
    }
    log_file = WORKSPACE / "logs" / "youtube-uploads.jsonl"
    log_file.parent.mkdir(exist_ok=True)
    with open(log_file, "a") as f:
        f.write(json.dumps(log_entry) + "\n")

    return video_id

def main():
    parser = argparse.ArgumentParser(description="Upload video to Dollar Agency YouTube")
    parser.add_argument("--file",        required=True,  help="Path to video file")
    parser.add_argument("--title",       required=True,  help="Video title")
    parser.add_argument("--description", default=None,   help="Video description")
    parser.add_argument("--tags",        default=None,   help="Comma-separated tags")
    parser.add_argument("--category",    default="28",   help="Category ID or name")
    parser.add_argument("--privacy",     default="unlisted", choices=["public","unlisted","private"])
    parser.add_argument("--schedule",    default=None,   help="Publish time (ISO 8601 UTC)")
    parser.add_argument("--thumbnail",   default=None,   help="Thumbnail image path")
    parser.add_argument("--shorts",      action="store_true", help="Mark as YouTube Short")

    args = parser.parse_args()
    upload_video(args)

if __name__ == "__main__":
    main()
