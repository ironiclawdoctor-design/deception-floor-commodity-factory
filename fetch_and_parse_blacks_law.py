#!/usr/bin/env python3
"""
fetch_and_parse_blacks_law.py

Fetches Black's Law Dictionary from Internet Archive djvu.txt,
parses entries by first letter, outputs JSONL.

Output format per line:
  {"letter": "A", "count": N, "words": [...]}

SOURCES:
  2nd Ed (1910) — PUBLIC, no auth: URL_2ND_ED
  1st Ed (1891) — PUBLIC, no auth: URL_1ST_ED
  4th Ed (1951) — BORROW REQUIRED: URL_4TH_ED_TEMPLATE
    (use archive_borrow_auth.py first, save djvu.txt, set LOCAL_FILE)

Author: Fiesta subagent (2026-03-25)
"""

import re
import json
import sys
import urllib.request
from collections import defaultdict

# ==============================================================================
# CONFIGURATION
# ==============================================================================

URL_2ND_ED = (
    "https://ia601808.us.archive.org/18/items/"
    "blacks-law-dictionary-2nd-edition-1910/"
    "Black%27s%20Law%20Dictionary%20%282nd%20Edition%29_djvu.txt"
)

URL_1ST_ED = (
    "https://ia600104.us.archive.org/26/items/"
    "blacks-law-dictionary-1st-edition-1891_Petition-of-Right/"
    "Black%27s%20Law%20Dictionary%2C%201st%20Edition%20%281891%29_djvu.txt"
)

# 4th Edition — after borrowing via archive_borrow_auth.py
URL_4TH_ED = (
    "https://ia600604.us.archive.org/5/items/"
    "blackslawdiction0000henr_t1a5/"
    "blackslawdiction0000henr_t1a5_djvu.txt"
)

# Set LOCAL_FILE to path of pre-downloaded djvu.txt, or None to fetch URL
LOCAL_FILE = None

OUTPUT_JSONL = "blacks_law_entries.jsonl"
OUTPUT_SUMMARY = "blacks_law_summary.json"


# ==============================================================================
# FETCH
# ==============================================================================

def fetch_text(url: str, local_file: str = None) -> str:
    if local_file:
        print(f"[+] Reading: {local_file}", file=sys.stderr)
        with open(local_file, "r", encoding="utf-8", errors="replace") as f:
            return f.read()

    print(f"[+] Fetching: {url}", file=sys.stderr)
    req = urllib.request.Request(url, headers={
        "User-Agent": "Mozilla/5.0 (compatible; research/agency-intelligence)"
    })
    with urllib.request.urlopen(req, timeout=180) as resp:
        raw = resp.read()
    print(f"[+] Downloaded {len(raw):,} bytes", file=sys.stderr)
    return raw.decode("utf-8", errors="replace")


# ==============================================================================
# PARSE
# ==============================================================================

def parse_entries(text: str) -> dict:
    """
    Parse Black's Law Dictionary djvu.txt into entries by first letter.

    Black's Law entry headwords in djvu.txt are typically:
      ALL-CAPS on their own line, often followed by a period
      e.g. "ABANDONMENT." or "AB INITIO." or "A FORTIORI."

    Strategy:
      1. Find all lines matching ALL-CAPS headword pattern
      2. Filter out page headers, numbers, scanner artifacts
      3. Bucket by first letter
    """
    entries_by_letter = defaultdict(set)

    # Primary pattern: ALL-CAPS line (standalone headword)
    # Allows: spaces, hyphens, apostrophes, periods in multi-word entries
    # Requires: starts with capital, ends with capital or period
    HEADWORD_LINE = re.compile(
        r"^[ \t]*([A-Z][A-Z\s\-\'\(\)]{0,70}[A-Z])\.?\s*$",
        re.MULTILINE
    )

    # Secondary: "WORD. definition..." inline pattern
    INLINE_ENTRY = re.compile(
        r"^([A-Z][A-Z\s\-\']{1,60}[A-Z])\.\s+[A-Z\(]",
        re.MULTILINE
    )

    # Noise filter: known non-entry caps lines
    NOISE = re.compile(
        r"^(DIGITIZED|GOOGLE|THIS IS|THE |A |AN |SEE |NOTE|PAGE |"
        r"WEST PUB|BLACK'S|DICTIONARY|DEFINITIONS|AMERICAN|ENGLISH|"
        r"JURISPRUDENCE|EDITION|PREFACE|CONTENTS|INDEX|TABLE|VOLUME|"
        r"CHAPTER|SECTION|PART |BOOK |TITLE |COPYRIGHT|PUBLISHED|"
        r"PRINTED|ALL RIGHTS|RESERVED|ST\. PAUL|MINN).*",
        re.IGNORECASE
    )

    raw_words = set()
    for m in HEADWORD_LINE.finditer(text):
        raw_words.add(m.group(1).strip())
    for m in INLINE_ENTRY.finditer(text):
        raw_words.add(m.group(1).strip())

    for word in raw_words:
        word = word.strip()
        # Min 2 chars, max 80 chars
        if len(word) < 2 or len(word) > 80:
            continue
        # Skip pure numbers
        if re.match(r"^\d+$", word):
            continue
        # Skip noise patterns
        if NOISE.match(word):
            continue
        # Skip single repeated char (e.g. "AAAAA")
        if len(set(word.replace(" ", ""))) < 2:
            continue

        first = word[0].upper()
        if first.isalpha():
            entries_by_letter[first].add(word)

    return {
        letter: {
            "count": len(words),
            "words": sorted(list(words))
        }
        for letter, words in sorted(entries_by_letter.items())
    }


# ==============================================================================
# OUTPUT
# ==============================================================================

def write_jsonl(entries: dict, path: str):
    with open(path, "w", encoding="utf-8") as f:
        for letter in sorted(entries.keys()):
            f.write(json.dumps({
                "letter": letter,
                "count": entries[letter]["count"],
                "words": entries[letter]["words"]
            }) + "\n")
    print(f"[+] JSONL written: {path}", file=sys.stderr)


def write_summary(entries: dict, path: str):
    total = sum(v["count"] for v in entries.values())
    summary = {
        "total_entries": total,
        "letters_covered": len(entries),
        "by_letter": {k: v["count"] for k, v in sorted(entries.items())}
    }
    with open(path, "w", encoding="utf-8") as f:
        json.dump(summary, f, indent=2)
    print(f"[+] Summary written: {path}", file=sys.stderr)
    print(f"[+] Total entries: {total:,}", file=sys.stderr)
    print(f"    {'Letter':<8} {'Count':>6}", file=sys.stderr)
    print(f"    {'-'*16}", file=sys.stderr)
    for letter, count in sorted(summary["by_letter"].items()):
        print(f"    {letter:<8} {count:>6}", file=sys.stderr)
    return summary


# ==============================================================================
# MAIN
# ==============================================================================

def main():
    import argparse
    parser = argparse.ArgumentParser(description="Parse Black's Law Dictionary")
    parser.add_argument("--edition", choices=["1st", "2nd", "4th"], default="2nd",
                        help="Edition to fetch (default: 2nd, public domain)")
    parser.add_argument("--local", help="Path to local djvu.txt file")
    parser.add_argument("--output-jsonl", default=OUTPUT_JSONL)
    parser.add_argument("--output-summary", default=OUTPUT_SUMMARY)
    args = parser.parse_args()

    url_map = {"1st": URL_1ST_ED, "2nd": URL_2ND_ED, "4th": URL_4TH_ED}
    url = url_map[args.edition]
    local = args.local or LOCAL_FILE

    text = fetch_text(url, local)
    print(f"[+] Text length: {len(text):,} chars", file=sys.stderr)

    entries = parse_entries(text)
    write_jsonl(entries, args.output_jsonl)
    summary = write_summary(entries, args.output_summary)

    # Print summary to stdout for piping
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
