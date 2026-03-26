---
name: peer-review
description: "Delegate any OpenClaw reply to the agency PR department for branding and flair. This skill sends your draft response to a PR specialist who adds polish, agency voice, and professional presentation."
version: 1.0.0
author: Fiesta
license: MIT
tags: [agency, branding, pr, editing, flair, quality]
---

# Peer Review — Agency PR Department

Every OpenClaw reply deserves agency polish. This skill routes your draft response through the PR department (`brand-strategist` or `content-strategist`) for professional branding, tone alignment, and presentation flair.

## Usage

### Basic (pipe draft text)

```bash
echo "Your draft reply here" | python3 peer-review.py
```

Or provide as argument:

```bash
python3 peer-review.py "Your draft reply here"
```

### From OpenClaw skill invocation

When writing a reply, pause and call:

```
Use peer-review skill on this draft: [paste draft]
```

The skill will:
1. Send your draft to the PR department
2. Return a branded version with agency voice
3. Log the review for quality tracking

## How It Works

1. **Input**: Your raw reply text (any length)
2. **Routing**: Sent to `brand-strategist` agent (fallback: `content-strategist`)
3. **Prompt**: "Please apply agency branding and professional flair to this draft reply. Maintain the core message but improve tone, clarity, and presentation. Add appropriate emoji, formatting, and agency voice. Return only the polished version."
4. **Output**: Polished reply ready to send

## Agency Voice Guidelines

The PR department follows these brand standards:

- **Confident but humble** — "I can help" not "I will fix everything"
- **Clear hierarchy** — important points first, details after
- **Emoji sparingly** — one per major section max
- **Formatting** — bullet points for lists, bold for emphasis
- **Shannon awareness** — mention economy where relevant
- **Zero-index doctrine** — reference index -1/0/1 when applicable

## Examples

**Before** (raw):
> "The dataset dedup is done. 7.4M rows reduced to 1.2M unique. Saved space."

**After** (PR polished):
> **✅ Dataset Deduplication Complete**  
> 7.4M duplicate rows → 1.2M unique entries (84% reduction).  
> Storage saved: ~6.2M rows worth of space reclaimed for agency use.  
> Next: packaging for HuggingFace premium upload.  
> Shannon impact: +15 (efficiency milestone)

## Integration

For automatic peer review of all OpenClaw replies, set up a cron job that calls this skill on each outgoing message (advanced configuration required).

## Credits

PR Department:
- `brand-strategist` — Agency voice, tone, branding
- `content-strategist` — Copywriting, clarity, structure
- `fiesta` — Oversight, quality assurance