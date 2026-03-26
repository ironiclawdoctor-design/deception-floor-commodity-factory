---
name: pyresearch
description: Python-native autoresearch skill with persistent caching. Caches all research results to agency.db so identical queries never burn tokens twice. Wraps web_fetch, API calls, and LLM queries with cache-first lookup. Cache hit = $0.0000. Use for any repeated research pattern.
version: 1.0.0
author: Fiesta
tags: [python, cache, research, autoresearch, optimization]
---

# PyResearch — Cached Autoresearch Engine

## Cache Strategy
- **L1:** agency.db (SQLite, instant, $0)
- **L2:** /root/human/*.log files (disk, instant, $0)
- **L3:** web_fetch (network, ~0.1s, $0)
- **L4:** LLM inference (DeepSeek, ~1s, $0.00014/1k tokens)

Always check L1 first. Only escalate if cache miss.

## Cache TTL
- API schemas: 7 days
- Web content: 24 hours
- LLM responses: 1 hour
- System state: 0 (always fresh)

## Usage
```python
from skills.pyresearch.cache import ResearchCache
rc = ResearchCache()
result = rc.get_or_fetch("hashnode_api_tags", 
    fetch_fn=lambda: fetch_hashnode_tag_docs(),
    ttl_hours=168)
```
