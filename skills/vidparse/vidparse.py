#!/usr/bin/env python3
"""
vidparse — YouTube video → summarized markdown
Agency-built. No auth needed for transcripts.
Usage:
  python3 vidparse.py --video VIDEO_ID --out output.md
  python3 vidparse.py --video VIDEO_ID  (prints to stdout)
"""

import sys
import json
import argparse
import re
from datetime import datetime

def get_transcript(video_id):
    try:
        from youtube_transcript_api import YouTubeTranscriptApi
        transcript = YouTubeTranscriptApi.get_transcript(video_id)
        return transcript
    except Exception as e:
        return None, str(e)

def transcript_to_text(transcript):
    if not transcript or isinstance(transcript, tuple):
        return ""
    lines = []
    for entry in transcript:
        text = entry.get('text', '').strip()
        if text:
            lines.append(text)
    return ' '.join(lines)

def chunk_text(text, chunk_size=3000):
    """Split text into chunks for summarization."""
    words = text.split()
    chunks = []
    current = []
    count = 0
    for word in words:
        current.append(word)
        count += 1
        if count >= chunk_size:
            chunks.append(' '.join(current))
            current = []
            count = 0
    if current:
        chunks.append(' '.join(current))
    return chunks

def summarize_transcript(video_id, transcript_text, title=""):
    """
    Produce a structured markdown summary from transcript text.
    No AI needed — structural extraction from transcript.
    """
    words = transcript_text.split()
    word_count = len(words)
    
    # Split into thirds for beginning/middle/end structure
    third = word_count // 3
    beginning = ' '.join(words[:third])
    middle = ' '.join(words[third:2*third])
    end = ' '.join(words[2*third:])
    
    # Extract sentences (rough)
    sentences = re.split(r'(?<=[.!?])\s+', transcript_text)
    
    # Key sentences: first 3, middle 3, last 3
    key_sentences = []
    if len(sentences) >= 9:
        key_sentences = sentences[:3] + sentences[len(sentences)//2-1:len(sentences)//2+2] + sentences[-3:]
    else:
        key_sentences = sentences
    
    # Word frequency for topics (exclude stopwords)
    stopwords = set(['the','a','an','is','it','in','on','at','to','for','of','and','or',
                     'but','i','you','we','they','he','she','that','this','was','are',
                     'be','been','being','have','has','had','do','did','will','would',
                     'could','should','may','might','with','from','by','as','so','if',
                     'not','no','my','your','our','their','its','his','her','what',
                     'when','where','who','how','all','just','like','get','got','know',
                     'think','want','need','going','come','go','see','say','said','make'])
    
    word_freq = {}
    for w in words:
        w_clean = re.sub(r'[^a-zA-Z]', '', w.lower())
        if len(w_clean) > 4 and w_clean not in stopwords:
            word_freq[w_clean] = word_freq.get(w_clean, 0) + 1
    
    top_topics = sorted(word_freq.items(), key=lambda x: x[1], reverse=True)[:15]
    
    # Estimate duration (avg speaking rate ~130 words/min)
    duration_min = round(word_count / 130)
    
    now = datetime.utcnow().strftime('%Y-%m-%d %H:%M UTC')
    
    md = f"""# Video Summary
**Video ID:** {video_id}
**URL:** https://youtu.be/{video_id}
**Processed:** {now}
**Transcript length:** {word_count:,} words (~{duration_min} min)

---

## Key Topics
{chr(10).join(f'- **{topic}** ({count}×)' for topic, count in top_topics[:10])}

---

## Structural Summary

### Opening (~first third)
{' '.join(words[:min(150, third)]) + ('...' if third > 150 else '')}

### Middle (~second third)
{' '.join(words[third:min(third+150, 2*third)]) + ('...' if (2*third - third) > 150 else '')}

### Close (~final third)
{' '.join(words[2*third:min(2*third+150, word_count)]) + ('...' if (word_count - 2*third) > 150 else '')}

---

## Key Passages (Selected)
{chr(10).join(f'> {s.strip()}' for s in key_sentences[:9] if s.strip())}

---

## Full Transcript
{transcript_text}
"""
    return md

def main():
    parser = argparse.ArgumentParser(description='YouTube video → markdown summary')
    parser.add_argument('--video', required=True, help='YouTube video ID')
    parser.add_argument('--out', help='Output file path (default: stdout)')
    args = parser.parse_args()
    
    video_id = args.video
    # Handle full URLs
    if 'youtube.com' in video_id or 'youtu.be' in video_id:
        match = re.search(r'(?:v=|youtu\.be/)([a-zA-Z0-9_-]{11})', video_id)
        if match:
            video_id = match.group(1)
    
    print(f"[vidparse] Fetching transcript for {video_id}...", file=sys.stderr)
    
    result = get_transcript(video_id)
    if isinstance(result, tuple):
        transcript, error = result
        if not transcript:
            print(f"[vidparse] ERROR: {error}", file=sys.stderr)
            sys.exit(1)
    else:
        transcript = result
    
    if not transcript:
        print(f"[vidparse] ERROR: No transcript returned", file=sys.stderr)
        sys.exit(1)
    
    print(f"[vidparse] Got {len(transcript)} transcript segments", file=sys.stderr)
    
    text = transcript_to_text(transcript)
    md = summarize_transcript(video_id, text)
    
    if args.out:
        with open(args.out, 'w') as f:
            f.write(md)
        print(f"[vidparse] Written to {args.out}", file=sys.stderr)
    else:
        print(md)

if __name__ == '__main__':
    main()
