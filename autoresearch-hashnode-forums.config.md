# Autoresearch Configuration — Hashnode Forums JS Posting

## Goal
Post to https://hashnode.com/forums/new?tag=vibe-coded via JavaScript automation,
bypassing the "no display" wall. Target: working post submission >93% reliability.

## Metric
- **Name**: post_success
- **Direction**: 1 (success) or 0 (failure)
- **Extract command**: grep "✅ Posted" run.log | wc -l
- **Target**: >0 (at least one successful post path discovered)

## Target Files
- /tmp/hashnode-forums-post.py (experiment script, create fresh each run)
- /tmp/hashnode-forums-post.js (node.js variant)

## Read-Only Files
- /tmp/hashnode-forum-wrapper.py (working baseline — do not modify)

## Run Command
python3 /tmp/hashnode-forums-post.py > run.log 2>&1
OR
node /tmp/hashnode-forums-post.js > run.log 2>&1

## Time Budget
- Per experiment: 30 seconds
- Kill timeout: 60 seconds

## Constraints
- No $DISPLAY (headless only)
- No Chromium sandbox (noSandbox: true set in gateway)
- Hashnode API key available: 2824c3af-2b0f-4836-9185-7e9d4547e304
- Must post to forums, not just dollaragency.hashnode.dev publication
- tag: vibe-coded

## Branch
autoresearch/hashnode-forums-js-20260326

## Approaches to Try (in order)
1. Playwright headless (no display needed) — pip install playwright + chromium
2. Puppeteer via node (headless) — npm install puppeteer
3. Selenium headless chrome with --no-sandbox --headless=new
4. Hashnode GraphQL with forum-specific mutation (if discovered)
5. Hashnode REST API undocumented endpoints (inspect network traffic via requests)
6. Cookie-based session auth + direct form POST
7. Hashnode community API (separate from gql.hashnode.com)

## Notes
- Target URL: https://hashnode.com/forums/new?tag=vibe-coded
- Content: "Emotion Needs a Hero" thread (already written)
- The wrapper script found publicationId is required for gql.hashnode.com
- Forums may use a different GraphQL endpoint or REST endpoint
- Inspect https://hashnode.com/community for alternate API surface
