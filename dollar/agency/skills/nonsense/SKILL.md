---
name: nonsense
description: Translates impossible/hyperbolic human ultimatums into real executable plans. "Sort my iPhone photos in 5 minutes or else" becomes a real pipeline. Treats every impossibility as a legitimate engineering problem. Inspired by adversarial prompting, WoW raid demands, and the Zero-Index doctrine. Use when the human says something that sounds insane but actually has a 93% viable path.
version: 1.0.0
author: Fiesta
tags: [ultimatum, impossible, translation, pipeline, nonsense, action]
---

# Nonsense Skill — Ultimatum-to-Pipeline Translator

## Doctrine
> "Nonsense is just engineering problems without a spec."

When Thaniel says "sort my iPhone photos by subject in 5 minutes or else" —
that is not nonsense. That is:
- Input: HEIC/JPG files from iPhone
- Process: Vision model classification by subject
- Output: Sorted directories
- Constraint: 5 minutes
- Threat: "or else" = the -1 index cost of inaction

## Translation Engine

### Step 1 — Parse the ultimatum
Extract:
- SUBJECT (what to act on)
- ACTION (what to do)
- CONSTRAINT (time/resource limit)
- THREAT (consequence of failure)

### Step 2 — Find the 93% path
Every ultimatum has one. Always bash-first.

### Step 3 — Execute or surface job ID
Either run it or give Thaniel the one command to approve.

---

## Example Translations

### "Sort my iPhone photos by subject in 5 minutes or else"
```
SUBJECT: iPhone photos (HEIC/JPG)
ACTION: Sort by subject (people, places, food, nature, documents)
CONSTRAINT: 5 minutes
THREAT: Fiesta fails its 93% standard

PATH:
1. rsync iPhone photos to /root/photos/ via USB or iCloud
2. python3 classify-photos.py (uses CLIP model or EXIF tags)
3. Move to /root/photos/{people,places,food,nature,documents}/
4. Report: X photos sorted in Y seconds

TOOLS AVAILABLE:
- exiftool (EXIF metadata — subject hints)
- PIL/Pillow (image analysis)
- imageio + sklearn (basic clustering)
- Camoufox (if photos are in iCloud web)

ZERO COST PATH:
- EXIF GPS → place category (GPS = outdoor/travel)
- EXIF FaceDetect flag → people
- File size heuristics → screenshots vs photos
- Timestamp clustering → events
```

### "Build me a trading bot by midnight or I'm pulling funding"
```
PATH: Alpaca Markets API (free) + dollar.db + Shannon peg
TIME: 4h
COST: $0
OUTPUT: /root/trading-bot.py watching BTC/USD
```

### "Get me 1000 followers before I wake up"
```
PATH: Publish 3 articles (done) + Hacker News Show HN + r/LocalLLaMA
TIME: 30min
COST: $0
NOTE: followers are a lagging indicator. Traffic is immediate.
```

### "Make $100 appear in Cash App by Tuesday"
```
PATH:
1. Article #4 live (done) → underdog donations
2. RLHF dataset on HuggingFace (done) → Scale AI submission
3. GitHub Sponsors (5min setup)
4. Tax filing Tier 1 service listed on Gumroad ($49)
5. BTC wallet at $6.95 → promote harder
```

---

## iPhone Photo Sorter Script

```python
# classify-photos.py — sorts by EXIF + heuristics, no API needed
import os, shutil
from pathlib import Path
from PIL import Image
import piexif

def classify(path):
    try:
        exif = piexif.load(str(path))
        # GPS = outdoor/travel
        if exif.get('GPS') and exif['GPS']:
            return 'places'
        # High res + portrait ratio = people
        img = Image.open(path)
        w, h = img.size
        if h > w and h > 2000:
            return 'people'
        # Small file = screenshot
        if path.stat().st_size < 200000:
            return 'screenshots'
        return 'photos'
    except:
        return 'other'

src = Path('/root/iphone-photos')
for f in src.rglob('*.jpg') + src.rglob('*.HEIC') + src.rglob('*.jpeg'):
    cat = classify(f)
    dest = src / cat
    dest.mkdir(exist_ok=True)
    shutil.move(str(f), dest / f.name)
    print(f'{f.name} → {cat}')
```

---

## Usage
```
python3 /root/.openclaw/workspace/skills/nonsense/translate.py "sort my photos in 5 min"
python3 /root/.openclaw/workspace/skills/nonsense/translate.py "make $100 by tuesday"
python3 /root/.openclaw/workspace/skills/nonsense/translate.py "1000 followers before i wake up"
```

## The "Or Else" Doctrine
The threat is always the same: Fiesta fails the 93% standard.
That is worse than any external consequence.
Every ultimatum gets a real plan. No exceptions.
