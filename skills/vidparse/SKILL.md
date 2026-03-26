---
name: vidparse
description: Parse any YouTube channel's videos into JSONL — metadata, transcripts, chat logs, engagement signals. Agency-built, MIT licensed. Use for @AllAloneServesYouRight or any channel.
license: MIT
author: $DollarAgency
---

# vidparse

Renders a YouTube channel's full video catalog into parseable JSONL.

## What it produces

Each video → one JSONL line:
```json
{
  "video_id": "abc123",
  "title": "...",
  "published_at": "2026-01-01T00:00:00Z",
  "duration_seconds": 3600,
  "view_count": 430,
  "like_count": 12,
  "description": "...",
  "transcript": ["line 1", "line 2"],
  "transcript_language": "en",
  "tags": [],
  "channel_id": "UCxxx",
  "channel_name": "@AllAloneServesYouRight",
  "thumbnail_url": "...",
  "live_stream": false,
  "parsed_at": "2026-03-24T23:31:00Z"
}
```

## Usage

```bash
python3 skills/vidparse/vidparse.py --channel @AllAloneServesYouRight --out channel.jsonl
python3 skills/vidparse/vidparse.py --video VIDEO_ID --out single.jsonl
python3 skills/vidparse/vidparse.py --channel @AllAloneServesYouRight --transcripts --out full.jsonl
```

## Auth
Uses /root/.gog/token.json (YouTube Data API v3).
Transcript fetches via youtube-transcript-api (no auth needed).

## MIT License
Copyright 2026 $DollarAgency. Free to use, modify, distribute.
No warranty. No VC required.
