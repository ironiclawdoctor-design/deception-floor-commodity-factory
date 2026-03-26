#!/usr/bin/env python3
"""
Research OpenRouter affiliate marketing opportunities using pyresearch cache.
"""
import sys
import json
import subprocess
from pathlib import Path
sys.path.insert(0, str(Path.home() / '.openclaw/workspace/skills/pyresearch'))
from cache import ResearchCache

def search_web(query, count=10):
    """Use web_search tool via exec? Actually we can use web_fetch for URLs, but search we need web_search.
    Since we can't call web_search from Python directly, we'll use exec with OpenClaw CLI? Let's think.
    Better to write a script that uses the tools available to subagent: web_search, web_fetch.
    We'll run this script via subagent, but we need to call web_search from Python? Not possible.
    Instead, we'll run searches via exec with openclaw web_search? Not available.
    Let's do a hybrid: write a script that outputs search queries, then run them via subagent's tool calls.
    But we need to keep caching.
    We'll use the cache to store search results; we can manually call web_search from subagent and store results in cache.
    This script will just read from cache and output missing queries.
    """
    pass

def main():
    rc = ResearchCache()
    print("📊 Research Cache Stats:")
    rc.stats()
    
    # Define search queries
    queries = [
        "OpenRouter affiliate program",
        "OpenRouter referral",
        "OpenRouter discount",
        "OpenRouter partner program",
        "OpenRouter promo code",
        "OpenRouter credits free",
        "OpenRouter affiliate link",
        "OpenRouter API credits",
        "OpenRouter pricing discount",
        "OpenRouter referral bonus"
    ]
    
    # We'll store results
    results = {}
    
    for q in queries:
        cached = rc.get(q)
        if cached:
            print(f"✅ Cache hit: {q}")
            results[q] = cached
        else:
            print(f"❌ Cache miss: {q}")
            results[q] = None
    
    # Output missing queries for manual search
    missing = [q for q, v in results.items() if v is None]
    if missing:
        print("\n🔍 Missing queries (need manual search):")
        for q in missing:
            print(f"  - {q}")
    else:
        print("\n🎉 All queries cached.")
    
    # Save summary
    summary = {
        "cached_queries": len(results) - len(missing),
        "missing_queries": len(missing),
        "missing": missing,
        "cached_results": {k: v for k, v in results.items() if v is not None}
    }
    with open('/root/.openclaw/workspace/research_summary.json', 'w') as f:
        json.dump(summary, f, indent=2)
    print(f"\n📝 Summary saved to research_summary.json")

if __name__ == '__main__':
    main()