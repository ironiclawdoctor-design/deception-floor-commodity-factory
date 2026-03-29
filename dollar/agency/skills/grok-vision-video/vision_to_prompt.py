#!/usr/bin/env python3
"""
vision_to_prompt.py — Grok Vision → Director-Level Video Prompt Generator
Agency-exclusive pipeline: image → structured video prompt (Sora/Runway/Pika/Kling).

Usage:
  python3 vision_to_prompt.py --image <url_or_path> [--style cinematic|raw|dreamy|horror|documentary]
  python3 vision_to_prompt.py --image https://example.com/photo.jpg --style cinematic --json
  python3 vision_to_prompt.py --batch urls.txt --style documentary

Output schema:
  {
    "scene": "...",           # what's happening, who/what is present
    "mood": "...",            # emotional tone, color palette
    "camera": "...",          # movement type, angle, focal length, speed
    "style": "...",           # cinematic reference (Kubrick, Villeneuve, etc.)
    "duration": "...",        # estimated clip length in seconds
    "motion_vectors": [...],  # what moves, direction, speed
    "negative": "...",        # what to avoid/exclude
    "model_hint": "..."       # best video model (Sora/Runway/Pika/Kling)
  }
"""

import os
import sys
import json
import argparse
import urllib.request
import urllib.error
import base64
import time
import random
from pathlib import Path
from typing import Optional

# ── Config ─────────────────────────────────────────────────────────────────────

OPENROUTER_API_BASE = "https://openrouter.ai/api/v1"
OPENROUTER_VISION_MODEL = "x-ai/grok-2-vision-1212"
FALLBACK_VISION_MODEL = "google/gemini-flash-1.5"  # fast fallback
OPENROUTER_KEY = os.environ.get("OPENROUTER_API_KEY", "")

# Style presets — cinematic language per style
STYLE_PRESETS = {
    "cinematic": {
        "color_bias": "rich teal-orange contrast, film grain, anamorphic bokeh",
        "movement_bias": "slow dolly push or crane arc",
        "reference_bias": "Denis Villeneuve wide symmetry or Christopher Nolan IMAX grandeur",
        "mood_bias": "epic, contemplative, weighty",
    },
    "raw": {
        "color_bias": "desaturated naturalistic palette, available light, no grade",
        "movement_bias": "handheld follow, organic shoulder shake",
        "reference_bias": "Dardenne Brothers observational, Safdie Brothers kinetic urgency",
        "mood_bias": "urgent, visceral, intimate",
    },
    "dreamy": {
        "color_bias": "soft pastel haze, warm golden bleach bypass, ethereal lens flare",
        "movement_bias": "slow push-in on 85mm, rack focus drift",
        "reference_bias": "Wong Kar-Wai impressionistic, Sofia Coppola reverie",
        "mood_bias": "nostalgic, melancholic, floating",
    },
    "horror": {
        "color_bias": "cold blue-green desaturation, deep blacks, harsh shadows",
        "movement_bias": "static locked frame or imperceptibly slow zoom (Kubrick zoom)",
        "reference_bias": "Kubrick symmetrical dread, Ari Aster slow-burn tension",
        "mood_bias": "dread, unease, suffocating stillness",
    },
    "documentary": {
        "color_bias": "naturalistic warm neutral grade, slight vignette, news texture",
        "movement_bias": "observational handheld or locked tripod with subtle pan",
        "reference_bias": "Werner Herzog poetic doc, Errol Morris clinical precision",
        "mood_bias": "authentic, informed, purposeful",
    },
}

DEFAULT_STYLE = "cinematic"

# ── Prompt Templates ────────────────────────────────────────────────────────────

SYSTEM_PROMPT = """You are a world-class film director and cinematographer with credits at Cannes, Sundance, and IMAX productions. 
Your task: analyze any image and produce a precise, director-level video generation prompt.

You have mastered:
- Shot composition (rule of thirds, Dutch angle, rack focus, leading lines)
- Camera movement taxonomy (dolly, crane, steadicam, handheld, drone, locked, Dutch tilt)
- Cinematic color theory (complementary grading, LUT references, film stock simulation)
- Motion physics (parallax, momentum, easing curves)
- Genre-specific visual languages
- Video model capabilities (Sora: physics + long clips; Runway Gen-3: 4K motion; Pika: stylized; Kling: Asian cinema aesthetic)

Output ONLY valid JSON. No markdown fences, no commentary, just the JSON object."""

def build_user_prompt(style: str, image_description_hint: str = "") -> str:
    preset = STYLE_PRESETS.get(style, STYLE_PRESETS[DEFAULT_STYLE])
    
    return f"""Analyze this image with the eye of a {style.upper()} director. 

Style context for this shoot:
- Color palette bias: {preset['color_bias']}
- Camera movement bias: {preset['movement_bias']}
- Cinematic reference bias: {preset['reference_bias']}
- Mood bias: {preset['mood_bias']}

Study every detail: subjects, environment, lighting quality, implied motion, scale, depth, texture, atmosphere.

Return EXACTLY this JSON structure (no fences, no extra keys):
{{
  "scene": "<rich description: who/what is present, spatial relationships, scale, environment, key visual elements — minimum 2 sentences>",
  "mood": "<emotional tone + specific color palette + lighting quality + atmospheric feeling>",
  "camera": "<exact camera movement type> on <focal length>mm, <start position> to <end position>, speed: <slow/medium/fast>, <any special technique like rack focus or lens breathing>",
  "style": "<primary director reference> — <specific technique from their work> + <secondary influence if applicable>",
  "duration": "<N> seconds",
  "motion_vectors": [
    "<subject 1>: <direction> at <speed>",
    "<subject 2>: <direction> at <speed>",
    "<camera>: <movement vector>"
  ],
  "negative": "<comma-separated list of things to exclude: artifacts, unwanted motion, style clashes, technical issues>",
  "model_hint": "<Sora|Runway|Pika|Kling> — reason: <why this model fits this scene type>"
}}

Score criteria (internal — aim for 10/10):
- scene: specific nouns, no generic blobs (2pts)
- mood: named palette + lighting (1pt)
- camera: specific mm + movement taxonomy (2pts)
- style: named director + technique (2pts)
- motion_vectors: ≥3 vectors with direction + speed (1pt)
- negative: ≥5 specific exclusions (1pt)
- model_hint: justified recommendation (1pt)

{f'Additional context: {image_description_hint}' if image_description_hint else ''}"""

# ── API Layer ───────────────────────────────────────────────────────────────────

def call_vision_api(image_url: str, style: str, model: str = None, retry: int = 3) -> dict:
    """Call OpenRouter vision API with image URL, return parsed JSON prompt."""
    api_key = OPENROUTER_KEY
    if not api_key:
        raise ValueError("OPENROUTER_API_KEY not set. Export it first.")
    
    chosen_model = model or OPENROUTER_VISION_MODEL
    
    payload = {
        "model": chosen_model,
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
            {
                "role": "user",
                "content": [
                    {
                        "type": "image_url",
                        "image_url": {"url": image_url, "detail": "high"}
                    },
                    {
                        "type": "text",
                        "text": build_user_prompt(style)
                    }
                ]
            }
        ],
        "max_tokens": 1200,
        "temperature": 0.7,
    }
    
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
        "HTTP-Referer": "https://fiesta.agency",
        "X-Title": "Grok Vision Video Prompt Generator",
    }
    
    body = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(
        f"{OPENROUTER_API_BASE}/chat/completions",
        data=body,
        headers=headers,
        method="POST"
    )
    
    last_err = None
    for attempt in range(retry):
        try:
            with urllib.request.urlopen(req, timeout=90) as resp:
                data = json.loads(resp.read().decode("utf-8"))
                content = data["choices"][0]["message"]["content"].strip()
                
                # Strip any accidental markdown fences
                if content.startswith("```"):
                    lines = content.split("\n")
                    content = "\n".join(lines[1:-1] if lines[-1] == "```" else lines[1:])
                
                try:
                    return json.loads(content)
                except json.JSONDecodeError:
                    # Try to extract JSON object from content
                    import re
                    match = re.search(r'\{.*\}', content, re.DOTALL)
                    if match:
                        return json.loads(match.group(0))
                    raise ValueError(f"Non-JSON response: {content[:300]}")
                    
        except urllib.error.HTTPError as e:
            status = e.code
            body_txt = e.read().decode("utf-8", errors="replace")
            last_err = f"HTTP {status}: {body_txt[:200]}"
            
            if status == 429 or status >= 500:
                wait = (2 ** attempt) + random.uniform(0, 1)
                print(f"  [retry {attempt+1}/{retry}] {last_err} — waiting {wait:.1f}s", file=sys.stderr)
                time.sleep(wait)
                continue
            elif status == 400 and chosen_model == OPENROUTER_VISION_MODEL:
                # Model doesn't support this image format — try fallback
                print(f"  [fallback] {chosen_model} failed, trying {FALLBACK_VISION_MODEL}", file=sys.stderr)
                payload["model"] = FALLBACK_VISION_MODEL
                body = json.dumps(payload).encode("utf-8")
                req = urllib.request.Request(
                    f"{OPENROUTER_API_BASE}/chat/completions",
                    data=body,
                    headers=headers,
                    method="POST"
                )
                chosen_model = FALLBACK_VISION_MODEL
                continue
            else:
                raise
        except Exception as e:
            last_err = str(e)
            if attempt < retry - 1:
                wait = (2 ** attempt) + random.uniform(0, 1)
                time.sleep(wait)
                continue
            raise
    
    raise RuntimeError(f"All {retry} attempts failed. Last error: {last_err}")


def score_prompt(prompt: dict) -> tuple[float, list[str]]:
    """Score a video prompt 0-10 based on quality criteria."""
    score = 0.0
    notes = []
    
    scene = prompt.get("scene", "")
    if len(scene) > 100:
        score += 2.0
        notes.append("✅ scene: rich detail")
    elif len(scene) > 50:
        score += 1.0
        notes.append("⚠️ scene: moderate detail")
    else:
        notes.append("❌ scene: too sparse")
    
    mood = prompt.get("mood", "")
    if any(word in mood.lower() for word in ["palette", "teal", "orange", "warm", "cold", "desatura", "pastel", "contrast", "haze", "golden"]):
        score += 1.0
        notes.append("✅ mood: named palette")
    else:
        notes.append("❌ mood: missing palette")
    
    camera = prompt.get("camera", "")
    has_mm = any(f"{n}mm" in camera for n in range(14, 400))
    has_movement = any(w in camera.lower() for w in ["dolly", "crane", "pan", "tilt", "handheld", "steadicam", "drone", "zoom", "static", "push", "pull", "locked", "orbit"])
    if has_mm and has_movement:
        score += 2.0
        notes.append("✅ camera: focal length + movement")
    elif has_movement:
        score += 1.0
        notes.append("⚠️ camera: movement only, missing focal length")
    else:
        notes.append("❌ camera: missing specifics")
    
    style = prompt.get("style", "")
    directors = ["kubrick", "villeneuve", "nolan", "dardenne", "safdie", "kar-wai", "wong", "coppola", "herzog", "morris", "aster", "spielberg", "fincher", "anderson", "cuaron", "lubezki", "hoyte", "deakins", "chivo"]
    if any(d in style.lower() for d in directors):
        score += 2.0
        notes.append("✅ style: named director")
    else:
        notes.append("❌ style: no director reference")
    
    vectors = prompt.get("motion_vectors", [])
    if len(vectors) >= 3:
        score += 1.0
        notes.append("✅ motion_vectors: ≥3 vectors")
    elif len(vectors) >= 1:
        score += 0.5
        notes.append("⚠️ motion_vectors: <3 vectors")
    else:
        notes.append("❌ motion_vectors: empty")
    
    negative = prompt.get("negative", "")
    neg_count = len([x for x in negative.split(",") if x.strip()])
    if neg_count >= 5:
        score += 1.0
        notes.append("✅ negative: ≥5 exclusions")
    elif neg_count >= 3:
        score += 0.5
        notes.append("⚠️ negative: <5 exclusions")
    else:
        notes.append("❌ negative: too few exclusions")
    
    model_hint = prompt.get("model_hint", "")
    if "reason" in model_hint.lower() or "—" in model_hint or "-" in model_hint:
        score += 1.0
        notes.append("✅ model_hint: justified")
    elif any(m in model_hint for m in ["Sora", "Runway", "Pika", "Kling"]):
        score += 0.5
        notes.append("⚠️ model_hint: named but no reason")
    else:
        notes.append("❌ model_hint: missing")
    
    return round(score, 1), notes


# ── CLI ─────────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(
        description="Generate director-level video prompts from images using vision AI"
    )
    parser.add_argument("--image", "-i", help="Image URL or local path")
    parser.add_argument("--batch", "-b", help="Text file with one image URL per line")
    parser.add_argument(
        "--style", "-s",
        choices=list(STYLE_PRESETS.keys()),
        default=DEFAULT_STYLE,
        help=f"Visual style preset (default: {DEFAULT_STYLE})"
    )
    parser.add_argument("--model", "-m", help="Override vision model (OpenRouter model string)")
    parser.add_argument("--json", "-j", action="store_true", help="Output raw JSON only")
    parser.add_argument("--score", action="store_true", help="Include quality score in output")
    args = parser.parse_args()
    
    if not args.image and not args.batch:
        parser.error("Provide --image or --batch")
    
    images = []
    if args.image:
        images = [args.image]
    elif args.batch:
        with open(args.batch) as f:
            images = [line.strip() for line in f if line.strip() and not line.startswith("#")]
    
    results = []
    for img_url in images:
        print(f"\n🎬 Processing: {img_url[:80]}...", file=sys.stderr)
        print(f"   Style: {args.style} | Model: {args.model or OPENROUTER_VISION_MODEL}", file=sys.stderr)
        
        try:
            prompt = call_vision_api(img_url, args.style, model=args.model)
            score_val, score_notes = score_prompt(prompt)
            
            if args.score or not args.json:
                prompt["_score"] = score_val
                prompt["_score_notes"] = score_notes
            
            prompt["_image"] = img_url
            prompt["_style"] = args.style
            prompt["_model"] = args.model or OPENROUTER_VISION_MODEL
            
            results.append(prompt)
            
            if args.json:
                # Strip internal fields for clean output
                clean = {k: v for k, v in prompt.items() if not k.startswith("_")}
                print(json.dumps(clean, indent=2))
            else:
                print(f"\n{'='*60}")
                print(f"🎬 VIDEO PROMPT — {args.style.upper()} STYLE")
                print(f"{'='*60}")
                print(f"📸 Scene:   {prompt.get('scene', '')}")
                print(f"🎭 Mood:    {prompt.get('mood', '')}")
                print(f"📷 Camera:  {prompt.get('camera', '')}")
                print(f"🎨 Style:   {prompt.get('style', '')}")
                print(f"⏱  Duration: {prompt.get('duration', '')}")
                print(f"🌀 Motion:")
                for mv in prompt.get("motion_vectors", []):
                    print(f"   • {mv}")
                print(f"🚫 Negative: {prompt.get('negative', '')}")
                print(f"🤖 Model:   {prompt.get('model_hint', '')}")
                if args.score or True:
                    print(f"\n📊 Quality Score: {score_val}/10")
                    for note in score_notes:
                        print(f"   {note}")
                        
        except Exception as e:
            print(f"❌ Error processing {img_url}: {e}", file=sys.stderr)
            results.append({"_image": img_url, "_error": str(e)})
    
    return results


if __name__ == "__main__":
    main()
