"""
xAI Grok Search Skill
Importable Python module for web and X/Twitter search with real-time access.

Quick start:
    from skills.grok import search_web, search_x, GrokResult

    result = search_web("latest AI regulation news")
    print(result.content)
    for cite in result.citations:
        print(cite.format_markdown())
"""

from .grok import (
    search_web,
    search_x,
    async_search_web,
    async_search_x,
    GrokResult,
    Citation,
    GrokError,
    GrokCache,
    LIVE_SEARCH_MODELS,
    DEFAULT_MODEL,
)

__all__ = [
    "search_web",
    "search_x",
    "async_search_web",
    "async_search_x",
    "GrokResult",
    "Citation",
    "GrokError",
    "GrokCache",
    "LIVE_SEARCH_MODELS",
    "DEFAULT_MODEL",
]

__version__ = "2.0.0"
