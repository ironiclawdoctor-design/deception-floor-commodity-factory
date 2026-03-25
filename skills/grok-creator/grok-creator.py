#!/usr/bin/env python3
"""
grok-creator.py — Agency-only image/video generation via xAI Grok API.

Endpoints discovered 2026-03-25:
  Image: POST https://api.x.ai/v1/images/generations        (synchronous, returns URL or b64)
  Video: POST https://api.x.ai/v1/videos/generations        (async, returns request_id)
  Poll:  GET  https://api.x.ai/v1/videos/{request_id}       (returns status/url when done)

Models:
  grok-imagine-image      — $0.02/image, 300 RPM
  grok-imagine-image-pro  — $0.07/image, 30 RPM
  grok-imagine-video      — $0.050/sec, 60 RPM (async, ~8s default duration)
"""

import argparse
import base64
import json
import os
import sys
import time
import urllib.request
import urllib.error
from datetime import datetime, timezone
from pathlib import Path

# ── Config ──────────────────────────────────────────────────────────────────
SECRETS_PATH = Path(__file__).parent.parent.parent / "secrets" / "xai-api.json"
LOG_PATH = Path(__file__).parent.parent.parent / "grok-creator-log.jsonl"
BASE_URL = "https://api.x.ai/v1"
DEFAULT_IMAGE_MODEL = "grok-imagine-image"
DEFAULT_VIDEO_MODEL = "grok-imagine-video"
VIDEO_POLL_INTERVAL = 5    # seconds
VIDEO_POLL_TIMEOUT  = 300  # seconds (5 min max)


# ── Auth ─────────────────────────────────────────────────────────────────────
def load_api_key() -> str:
    """Load xAI API key from secrets file."""
    try:
        with open(SECRETS_PATH) as f:
            data = json.load(f)
        key = data.get("api_key", "")
        if not key:
            raise ValueError("api_key is empty in secrets file")
        return key
    except FileNotFoundError:
        print(f"[grok-creator] ERROR: secrets file not found at {SECRETS_PATH}", file=sys.stderr)
        print("Create it with: {\"api_key\": \"xai-...\"}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"[grok-creator] ERROR loading API key: {e}", file=sys.stderr)
        sys.exit(1)


# ── HTTP ─────────────────────────────────────────────────────────────────────
def xai_post(endpoint: str, payload: dict, api_key: str) -> dict:
    """POST to xAI API, return parsed JSON."""
    url = f"{BASE_URL}/{endpoint}"
    body = json.dumps(payload).encode()
    req = urllib.request.Request(
        url, data=body,
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {api_key}",
            "User-Agent": "curl/7.88.1",
        },
        method="POST"
    )
    try:
        with urllib.request.urlopen(req, timeout=60) as resp:
            return json.loads(resp.read())
    except urllib.error.HTTPError as e:
        err_body = e.read().decode()
        try:
            return json.loads(err_body)
        except Exception:
            print(f"[grok-creator] HTTP {e.code}: {err_body}", file=sys.stderr)
            sys.exit(1)


def xai_get(endpoint: str, api_key: str) -> dict:
    """GET from xAI API, return parsed JSON."""
    url = f"{BASE_URL}/{endpoint}"
    req = urllib.request.Request(
        url,
        headers={
            "Authorization": f"Bearer {api_key}",
            "User-Agent": "curl/7.88.1",
        },
        method="GET"
    )
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            return json.loads(resp.read())
    except urllib.error.HTTPError as e:
        err_body = e.read().decode()
        try:
            return json.loads(err_body)
        except Exception:
            print(f"[grok-creator] HTTP {e.code}: {err_body}", file=sys.stderr)
            sys.exit(1)


def download_url(url: str, out_path: Path):
    """Download a URL to a local file."""
    req = urllib.request.Request(url, headers={"User-Agent": "grok-creator/1.0"})
    with urllib.request.urlopen(req, timeout=120) as resp:
        out_path.write_bytes(resp.read())


# ── Logging ──────────────────────────────────────────────────────────────────
def log_generation(record: dict):
    """Append a generation record to the JSONL log."""
    LOG_PATH.parent.mkdir(parents=True, exist_ok=True)
    with open(LOG_PATH, "a") as f:
        f.write(json.dumps(record) + "\n")


# ── Image Generation ─────────────────────────────────────────────────────────
def generate_image(
    prompt: str,
    out_path: Path,
    model: str = DEFAULT_IMAGE_MODEL,
    n: int = 1,
    api_key: str = "",
):
    """Generate image(s) with Grok and save to out_path."""
    print(f"[grok-creator] Generating image: model={model}, prompt={prompt!r}")

    payload = {
        "model": model,
        "prompt": prompt,
        "n": n,
        "response_format": "b64_json",  # no external download dependency
    }

    resp = xai_post("images/generations", payload, api_key)

    if "error" in resp or "code" in resp:
        print(f"[grok-creator] API error: {resp}", file=sys.stderr)
        log_generation({
            "type": "image", "model": model, "prompt": prompt,
            "status": "error", "error": str(resp),
            "timestamp": datetime.now(timezone.utc).isoformat(),
        })
        sys.exit(1)

    data = resp.get("data", [])
    if not data:
        print(f"[grok-creator] No data in response: {resp}", file=sys.stderr)
        sys.exit(1)

    saved_paths = []
    for i, item in enumerate(data):
        if "b64_json" in item:
            img_bytes = base64.b64decode(item["b64_json"])
            # Handle multiple images
            if n > 1 and i > 0:
                stem = out_path.stem
                suffix = out_path.suffix or ".jpg"
                save_path = out_path.parent / f"{stem}_{i}{suffix}"
            else:
                save_path = out_path
            save_path.parent.mkdir(parents=True, exist_ok=True)
            save_path.write_bytes(img_bytes)
            print(f"[grok-creator] ✅ Image saved: {save_path} ({len(img_bytes):,} bytes)")
            saved_paths.append(str(save_path))
        elif "url" in item:
            # Fallback: download from URL
            save_path = out_path if i == 0 else out_path.parent / f"{out_path.stem}_{i}{out_path.suffix}"
            download_url(item["url"], save_path)
            print(f"[grok-creator] ✅ Image downloaded: {save_path}")
            saved_paths.append(str(save_path))

    cost = resp.get("usage", {}).get("cost_in_usd_ticks", 0) / 1e9
    log_generation({
        "type": "image",
        "model": model,
        "prompt": prompt,
        "status": "success",
        "paths": saved_paths,
        "revised_prompt": data[0].get("revised_prompt", ""),
        "cost_usd": round(cost, 6),
        "timestamp": datetime.now(timezone.utc).isoformat(),
    })
    print(f"[grok-creator] Cost: ${cost:.4f}")
    return saved_paths


# ── Video Generation ─────────────────────────────────────────────────────────
def generate_video(
    prompt: str,
    out_path: Path,
    model: str = DEFAULT_VIDEO_MODEL,
    duration: int = None,
    aspect_ratio: str = None,
    api_key: str = "",
):
    """Generate video with Grok (async) and save to out_path."""
    print(f"[grok-creator] Generating video: model={model}, prompt={prompt!r}")
    print(f"[grok-creator] ⚠ Video generation is async — polling for completion...")

    payload = {"model": model, "prompt": prompt, "n": 1}
    if duration:
        payload["duration"] = duration
    if aspect_ratio:
        payload["aspect_ratio"] = aspect_ratio

    resp = xai_post("videos/generations", payload, api_key)

    if "error" in resp or "code" in resp:
        print(f"[grok-creator] API error: {resp}", file=sys.stderr)
        log_generation({
            "type": "video", "model": model, "prompt": prompt,
            "status": "error", "error": str(resp),
            "timestamp": datetime.now(timezone.utc).isoformat(),
        })
        sys.exit(1)

    request_id = resp.get("request_id")
    if not request_id:
        print(f"[grok-creator] No request_id in response: {resp}", file=sys.stderr)
        sys.exit(1)

    print(f"[grok-creator] request_id: {request_id}")

    # Poll for completion
    start = time.time()
    while True:
        elapsed = time.time() - start
        if elapsed > VIDEO_POLL_TIMEOUT:
            print(f"[grok-creator] ⏰ Timeout after {VIDEO_POLL_TIMEOUT}s", file=sys.stderr)
            log_generation({
                "type": "video", "model": model, "prompt": prompt,
                "request_id": request_id, "status": "timeout",
                "timestamp": datetime.now(timezone.utc).isoformat(),
            })
            sys.exit(1)

        poll = xai_get(f"videos/{request_id}", api_key)
        status = poll.get("status", "unknown")
        progress = poll.get("progress", 0)
        print(f"[grok-creator]   status={status} progress={progress}% ({elapsed:.0f}s)")

        if status == "done":
            video_info = poll.get("video", {})
            video_url = video_info.get("url")
            vid_duration = video_info.get("duration", 0)
            if not video_url:
                print(f"[grok-creator] No video URL in response: {poll}", file=sys.stderr)
                sys.exit(1)

            out_path.parent.mkdir(parents=True, exist_ok=True)
            print(f"[grok-creator] Downloading video...")
            download_url(video_url, out_path)

            cost = poll.get("usage", {}).get("cost_in_usd_ticks", 0) / 1e9
            print(f"[grok-creator] ✅ Video saved: {out_path} ({vid_duration}s)")
            print(f"[grok-creator] Cost: ${cost:.4f}")

            log_generation({
                "type": "video",
                "model": model,
                "prompt": prompt,
                "request_id": request_id,
                "status": "success",
                "path": str(out_path),
                "duration_sec": vid_duration,
                "cost_usd": round(cost, 6),
                "timestamp": datetime.now(timezone.utc).isoformat(),
            })
            return str(out_path)

        elif status in ("failed", "error"):
            print(f"[grok-creator] ❌ Video generation failed: {poll}", file=sys.stderr)
            log_generation({
                "type": "video", "model": model, "prompt": prompt,
                "request_id": request_id, "status": "failed",
                "error": str(poll),
                "timestamp": datetime.now(timezone.utc).isoformat(),
            })
            sys.exit(1)

        time.sleep(VIDEO_POLL_INTERVAL)


# ── CLI ───────────────────────────────────────────────────────────────────────
def main():
    parser = argparse.ArgumentParser(
        description="grok-creator — xAI image/video generation (agency-only)",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python3 grok-creator.py --image "a sunset over NYC skyline" --out sunset.jpg
  python3 grok-creator.py --image "futuristic robot" --out robot.png --model grok-imagine-image-pro
  python3 grok-creator.py --video "ocean waves crashing" --out ocean.mp4
  python3 grok-creator.py --video "galaxy spiral" --out galaxy.mp4 --duration 10 --aspect-ratio 16:9
  python3 grok-creator.py --list-models
        """
    )

    mode = parser.add_mutually_exclusive_group()
    mode.add_argument("--image", metavar="PROMPT", help="Generate an image from a text prompt")
    mode.add_argument("--video", metavar="PROMPT", help="Generate a video from a text prompt")
    mode.add_argument("--list-models", action="store_true", help="List available generation models")

    parser.add_argument("--out", metavar="PATH", default=None,
                        help="Output file path (default: grok-out.jpg or grok-out.mp4)")
    parser.add_argument("--model", default=None,
                        help=f"Model to use (default: {DEFAULT_IMAGE_MODEL} / {DEFAULT_VIDEO_MODEL})")
    parser.add_argument("--n", type=int, default=1, metavar="N",
                        help="Number of images to generate (image only, default: 1)")
    parser.add_argument("--duration", type=int, default=None,
                        help="Video duration in seconds (video only)")
    parser.add_argument("--aspect-ratio", default=None, metavar="WxH",
                        help="Aspect ratio e.g. 16:9 (video only)")

    args = parser.parse_args()

    if not any([args.image, args.video, args.list_models]):
        parser.print_help()
        sys.exit(0)

    api_key = load_api_key()

    if args.list_models:
        print("Available xAI generation models:")
        print(f"  Image (standard): {DEFAULT_IMAGE_MODEL}      $0.02/image, 300 RPM")
        print(f"  Image (pro):      grok-imagine-image-pro  $0.07/image, 30 RPM")
        print(f"  Video:            {DEFAULT_VIDEO_MODEL}      $0.050/sec, 60 RPM (async)")
        return

    if args.image:
        model = args.model or DEFAULT_IMAGE_MODEL
        ext = ".jpg"
        out = Path(args.out) if args.out else Path(f"grok-out{ext}")
        generate_image(args.image, out, model=model, n=args.n, api_key=api_key)

    elif args.video:
        model = args.model or DEFAULT_VIDEO_MODEL
        out = Path(args.out) if args.out else Path("grok-out.mp4")
        generate_video(
            args.video, out, model=model,
            duration=args.duration,
            aspect_ratio=args.aspect_ratio,
            api_key=api_key,
        )


if __name__ == "__main__":
    main()
