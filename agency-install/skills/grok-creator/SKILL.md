# grok-creator

Generate images and videos using xAI's Grok generation models.

## What This Skill Does

Provides `grok-creator.py` — a standalone Python script for image and video generation via the xAI API. No external dependencies (stdlib only). Logs all generations to `grok-creator-log.jsonl`.

## Endpoints (Discovered 2026-03-25)

| Type  | Endpoint                                    | Behavior        |
|-------|---------------------------------------------|-----------------|
| Image | `POST /v1/images/generations`               | Synchronous     |
| Video | `POST /v1/videos/generations`               | Async (returns `request_id`) |
| Poll  | `GET  /v1/videos/{request_id}`              | Returns status/url when done |

## Available Models

| Model                  | Type  | Cost          | Rate Limit |
|------------------------|-------|---------------|------------|
| `grok-imagine-image`   | image | $0.02/image   | 300 RPM    |
| `grok-imagine-image-pro` | image | $0.07/image | 30 RPM     |
| `grok-imagine-video`   | video | $0.050/sec    | 60 RPM     |

## Prerequisites

- API key in `/root/.openclaw/workspace/secrets/xai-api.json`:
  ```json
  {"api_key": "xai-..."}
  ```

## Usage

```bash
# Generate image (saves to sunset.jpg)
python3 grok-creator.py --image "a sunset over NYC skyline" --out sunset.jpg

# Generate with pro model
python3 grok-creator.py --image "detailed portrait" --out portrait.jpg --model grok-imagine-image-pro

# Generate multiple images
python3 grok-creator.py --image "abstract art" --out art.jpg --n 3

# Generate video (async, polls until done)
python3 grok-creator.py --video "ocean waves crashing on rocks" --out ocean.mp4

# Video with options
python3 grok-creator.py --video "galaxy spiral" --out galaxy.mp4 --duration 10 --aspect-ratio 16:9

# List models
python3 grok-creator.py --list-models
```

## API Call Formats

### Image Generation (synchronous)

```json
POST https://api.x.ai/v1/images/generations
{
  "model": "grok-imagine-image",
  "prompt": "your prompt here",
  "n": 1,
  "response_format": "b64_json"
}
```

Response:
```json
{
  "data": [{"b64_json": "...", "mime_type": "image/jpeg", "revised_prompt": ""}],
  "usage": {"cost_in_usd_ticks": 200000000}
}
```

### Video Generation (async)

Step 1 — Submit:
```json
POST https://api.x.ai/v1/videos/generations
{
  "model": "grok-imagine-video",
  "prompt": "your prompt here",
  "n": 1,
  "duration": 8,
  "aspect_ratio": "16:9"
}
```
Response: `{"request_id": "uuid"}`

Step 2 — Poll:
```
GET https://api.x.ai/v1/videos/{request_id}
```
Response when done:
```json
{
  "status": "done",
  "progress": 100,
  "video": {"url": "https://vidgen.x.ai/...", "duration": 8},
  "usage": {"cost_in_usd_ticks": 4000000000}
}
```

## Log Format

Each generation appends to `grok-creator-log.jsonl`:
```jsonl
{"type": "image", "model": "grok-imagine-image", "prompt": "...", "status": "success", "paths": ["..."], "cost_usd": 0.02, "timestamp": "..."}
{"type": "video", "model": "grok-imagine-video", "prompt": "...", "request_id": "...", "status": "success", "path": "...", "duration_sec": 8, "cost_usd": 0.4, "timestamp": "..."}
```

## Notes

- Video generation is async — typical generation time: 30–120 seconds
- Poll timeout: 5 minutes (configurable via `VIDEO_POLL_TIMEOUT`)
- Video cost = $0.05 × duration_seconds (8s default = $0.40)
- Image response supports both `b64_json` and `url` formats; script prefers b64 to avoid extra download
- Script is stdlib-only (no pip installs needed)
- Discovered via live API probing on 2026-03-25; docs site is a SPA and doesn't serve static pages

## Trigger Phrases

- "generate an image with grok"
- "grok image generation"
- "grok video generation"
- "xAI create image/video"
- "aurora model"
- "grok-imagine"
