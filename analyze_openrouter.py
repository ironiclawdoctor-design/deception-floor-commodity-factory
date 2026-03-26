#!/usr/bin/env python3
import sys
import re
import json
import subprocess
from pathlib import Path

def fetch_url(url):
    """Fetch URL via curl and return HTML."""
    cmd = ["curl", "-s", "-L", url]
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=10)
        return result.stdout
    except Exception as e:
        print(f"Error fetching {url}: {e}")
        return ""

def search_keywords(html, keywords):
    lines = html.split('\n')
    matches = {}
    for kw in keywords:
        pattern = re.compile(kw, re.IGNORECASE)
        matched_lines = [line.strip() for line in lines if pattern.search(line)]
        matches[kw] = matched_lines[:10]  # limit
    return matches

def main():
    urls = [
        "https://openrouter.ai/pricing",
        "https://openrouter.ai/docs",
        "https://openrouter.ai/announcements",
    ]
    keywords = ["discount", "coupon", "promo", "referral", "affiliate", "partner", "credit", "free", "bonus", "offer"]
    
    all_results = {}
    for url in urls:
        print(f"Fetching {url}...")
        html = fetch_url(url)
        if html:
            matches = search_keywords(html, keywords)
            all_results[url] = matches
    
    # Save results
    output_path = Path("/root/.openclaw/workspace/openrouter_analysis.json")
    with open(output_path, 'w') as f:
        json.dump(all_results, f, indent=2)
    print(f"Results saved to {output_path}")
    
    # Print summary
    for url, matches in all_results.items():
        print(f"\n--- {url} ---")
        for kw, lines in matches.items():
            if lines:
                print(f"  {kw}: {len(lines)} matches")
                for line in lines[:2]:
                    print(f"    - {line[:200]}...")
            else:
                print(f"  {kw}: none")

if __name__ == "__main__":
    main()