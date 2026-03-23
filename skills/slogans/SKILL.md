---
name: slogans
description: Political slogan generation and autoresearch. Generates, rates, and stores campaign slogans optimized for memorability, rhyme, emotional weight, and virality. Seed-based — provide one slogan, get 93 variations. Logs all slogans to agency.db for review.
version: 1.0.0
author: Fiesta
tags: [slogans, political, marketing, content, virality]
---

# Slogans Skill

Generate political slogans from a seed phrase. Rate by memorability (rhyme, rhythm, brevity, emotional hook).

## Usage
```
python3 /root/.openclaw/workspace/skills/slogans/generate.py --seed "Think some more and vote for Gore"
python3 /root/.openclaw/workspace/skills/slogans/generate.py --list  (show top rated)
python3 /root/.openclaw/workspace/skills/slogans/generate.py --export (markdown for articles)
```

## Slogan Anatomy (what makes >93% memorable)
1. Rhyme or near-rhyme
2. 4-8 words max
3. Action verb
4. Emotional anchor (hope, fear, pride, humor)
5. Name or brand embedded
6. Rhythm: iambic or trochaic patterns land best
