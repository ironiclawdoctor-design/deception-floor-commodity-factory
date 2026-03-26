#!/usr/bin/env python3
"""
Dollar Agency Training Data Generator
======================================
Fetches all articles from dollaragency.hashnode.dev via GraphQL
and converts them into instruction-tuning JSONL format for LLM fine-tuning.

Output: /root/.openclaw/workspace/training/agency-instruct.jsonl

Format per line:
  {"instruction": "...", "input": "", "output": "..."}

Also includes doctrine files from the workspace.
"""

import requests
import json
import os
import glob
import re
import time
from pathlib import Path

HASHNODE_GQL = "https://gql.hashnode.com/"
BLOG_HOST = "dollaragency.hashnode.dev"
OUTPUT_FILE = Path(__file__).parent / "agency-instruct.jsonl"
WORKSPACE = Path("/root/.openclaw/workspace")

FETCH_QUERY = """
query GetPosts($host: String!, $after: String) {
  publication(host: $host) {
    title
    posts(first: 20, after: $after) {
      pageInfo {
        hasNextPage
        endCursor
      }
      edges {
        node {
          title
          brief
          publishedAt
          tags { name }
          content {
            text
          }
        }
      }
    }
  }
}
"""


def fetch_all_posts():
    """Paginate through all posts on the Hashnode blog."""
    posts = []
    cursor = None
    page = 1

    while True:
        variables = {"host": BLOG_HOST}
        if cursor:
            variables["after"] = cursor

        try:
            resp = requests.post(
                HASHNODE_GQL,
                json={"query": FETCH_QUERY, "variables": variables},
                timeout=20,
            )
            resp.raise_for_status()
            data = resp.json()
        except Exception as e:
            print(f"  [!] GraphQL fetch failed (page {page}): {e}")
            break

        if "errors" in data:
            print(f"  [!] GraphQL errors: {data['errors']}")
            break

        pub = data.get("data", {}).get("publication")
        if not pub:
            print("  [!] No publication found for host:", BLOG_HOST)
            break

        edges = pub["posts"]["edges"]
        page_info = pub["posts"]["pageInfo"]

        for edge in edges:
            posts.append(edge["node"])

        print(f"  Page {page}: fetched {len(edges)} posts (total: {len(posts)})")

        if page_info["hasNextPage"]:
            cursor = page_info["endCursor"]
            page += 1
            time.sleep(0.5)  # polite rate limiting
        else:
            break

    return posts


def clean_text(text):
    """Remove markdown artifacts, normalize whitespace."""
    if not text:
        return ""
    # Remove excessive blank lines
    text = re.sub(r'\n{3,}', '\n\n', text)
    text = text.strip()
    return text


def article_to_instructions(post):
    """Convert a single article into multiple training examples."""
    title = post.get("title", "").strip()
    brief = clean_text(post.get("brief", ""))
    content_text = clean_text(post.get("content", {}).get("text", ""))
    tags = [t["name"] for t in post.get("tags", [])]

    if not title or not content_text:
        return []

    examples = []

    # Example 1: Direct question from title
    examples.append({
        "instruction": f"What is '{title}'? Explain this concept from the Dollar Agency.",
        "input": "",
        "output": content_text[:2000] if len(content_text) > 2000 else content_text
    })

    # Example 2: Summarize the article
    if brief:
        examples.append({
            "instruction": f"Summarize the Dollar Agency article titled: {title}",
            "input": "",
            "output": brief
        })

    # Example 3: Tag-based retrieval (if tags exist)
    if tags:
        tag_str = ", ".join(tags)
        examples.append({
            "instruction": f"What Dollar Agency content relates to the topics: {tag_str}?",
            "input": "",
            "output": f"The article '{title}' covers these topics. Summary: {brief or content_text[:500]}"
        })

    return examples


def load_workspace_doctrines():
    """Load key doctrine/markdown files from workspace as training data."""
    doctrine_files = [
        WORKSPACE / "AGENTS.md",
        WORKSPACE / "SOUL.md",
        WORKSPACE / "USER.md",
        WORKSPACE / "MEMORY.md",
    ]
    # Also grab any training/*.md files
    doctrine_files += list((WORKSPACE / "training").glob("*.md"))

    examples = []
    for fpath in doctrine_files:
        if not fpath.exists():
            continue
        try:
            content = fpath.read_text(encoding="utf-8", errors="replace")
            content = clean_text(content)
            if len(content) < 100:
                continue

            fname = fpath.name
            # Split into chunks of ~1500 chars to stay within token limits
            chunks = [content[i:i+1500] for i in range(0, min(len(content), 6000), 1500)]

            for i, chunk in enumerate(chunks):
                examples.append({
                    "instruction": f"What does the Dollar Agency's {fname} say? (part {i+1})",
                    "input": "",
                    "output": chunk
                })
        except Exception as e:
            print(f"  [!] Failed to read {fpath}: {e}")

    return examples


def generate():
    print("=" * 60)
    print("Dollar Agency Training Data Generator")
    print("=" * 60)

    all_examples = []

    # --- Fetch Hashnode articles ---
    print(f"\n[1/2] Fetching articles from {BLOG_HOST}...")
    posts = fetch_all_posts()
    print(f"  Total articles fetched: {len(posts)}")

    for post in posts:
        examples = article_to_instructions(post)
        all_examples.extend(examples)

    print(f"  Training examples from articles: {len(all_examples)}")

    # --- Load workspace doctrines ---
    print(f"\n[2/2] Loading workspace doctrine files...")
    doctrine_examples = load_workspace_doctrines()
    all_examples.extend(doctrine_examples)
    print(f"  Training examples from doctrines: {len(doctrine_examples)}")

    # --- Write output ---
    print(f"\nWriting {len(all_examples)} examples to {OUTPUT_FILE}...")
    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        for example in all_examples:
            f.write(json.dumps(example, ensure_ascii=False) + "\n")

    size_kb = OUTPUT_FILE.stat().st_size / 1024
    print(f"\n✓ Done! {len(all_examples)} examples → {OUTPUT_FILE}")
    print(f"  File size: {size_kb:.1f} KB")
    print(f"\nSample (first example):")
    if all_examples:
        print(json.dumps(all_examples[0], indent=2, ensure_ascii=False)[:500])

    return len(all_examples)


if __name__ == "__main__":
    generate()
