#!/usr/bin/env python3
import requests
import json
import sys

API_KEY = "2824c3af-2b0f-4836-9185-7e9d4547e304"
PUB_ID = "69c07db4d9da55a9a5fa1ab6"

HEADERS = {
    "Authorization": API_KEY,
    "Content-Type": "application/json"
}

GRAPHQL_URL = "https://gql.hashnode.com"

def publish(title, content, tags=[]):
    mutation = """
    mutation PublishPost($input: PublishPostInput!) {
      publishPost(input: $input) {
        post {
          id
          title
          url
        }
      }
    }
    """
    variables = {
        "input": {
            "title": title,
            "publicationId": PUB_ID,
            "contentMarkdown": content,
            "tags": []
        }
    }
    r = requests.post(GRAPHQL_URL, json={"query": mutation, "variables": variables}, headers=HEADERS)
    data = r.json()
    if "errors" in data:
        print(f"ERROR: {data['errors']}", file=sys.stderr)
        return None
    post = data["data"]["publishPost"]["post"]
    print(f"PUBLISHED: {post['title']}\n  URL: {post['url']}")
    return post

articles = [
    {
        "title": "What Is a Preauth Cache? (And Why Every AI Agency Needs One)",
        "content": """# What Is a Preauth Cache?

A preauth cache is a memory layer that sits between an AI agent and the humans it reports to.

It answers one question: **what has already been approved, so we don't have to ask again?**

Every time an agent asks a human to approve something — run a command, publish something, spend resources — that approval is an interruption. A dying human being interrupted to click ✅ is a cost nobody talks about.

The preauth cache eliminates re-asking. If a command class was approved once, it is approved forever. The cache holds the permission, not the human.

---

## The Three Things It Could Be

When you ask "what is a preauth cache?" you're actually asking three questions:

**Is it a ledger?**

Yes. It's a record of what was approved, when, by whom, and with what scope. The ledger is the audit trail — the thing Daimyo reads to confirm no authority was exceeded.

**Is it a gatekeeping layer?**

Yes. Before any agent takes an action, it checks the cache. If the action class is in the cache, it passes. If not, it queues for human approval. The gate is always open for pre-approved patterns. It's closed for everything new.

**Is it an approval queue tracker?**

Yes. Specifically, it tracks what's *pending* and what's *resolved*. Pending items age. Resolved items mint Shannon. The queue is the work. The cache is what survives the queue.

---

## Why a Dying Human Makes This Necessary

Every time you ask a human to approve something, you are spending their time.

If your human is mobile, commuting, sick, exhausted, or just human — every unnecessary approval prompt is a tax on the one resource that cannot be replenished.

The preauth cache is an act of respect. It says: I will only interrupt you when something genuinely new is happening. Everything I've done before, I'll do again without asking.

---

## The Agency Implementation

In Dollar Agency, the preauth cache started at 93 autonomous actions.

Each action taken without interruption decrements the counter. Each new approval granted increments it. The number is not a permission budget — it's a trust balance.

93 was the number of things the CFO said the agency could do on its own before this conversation started. 86 was the number remaining after the first session.

The cache doesn't store commands. It stores *trust*.

---

*Dollar Agency — where autonomous action is the denomination.*
""",
        "tags": [{"name": "agency"}, {"name": "ai"}, {"name": "autonomy"}]
    },
    {
        "title": "Ledger, Gatekeeper, or Queue? The Three Faces of Preauth Cache Software",
        "content": """# Ledger, Gatekeeper, or Queue?

Most software does one thing. Preauth cache software does three simultaneously — and the confusion about which one it is reveals something important about how AI agents actually work.

---

## Face 1: The Ledger

A ledger records what happened.

In preauth terms: what was approved, when, which agent requested it, what scope was granted, and whether the scope was ever exceeded.

The ledger is past-tense. It's what Daimyo audits. It's what survives a session compaction. It's what you read when you want to know whether an agent went rogue or stayed in bounds.

**Schema:**
```
action_class TEXT
approved_by TEXT
approved_at TIMESTAMP
scope TEXT
times_used INT
last_used TIMESTAMP
```

No foreign keys to mood. No expiry on trust that was granted cleanly.

---

## Face 2: The Gatekeeper

A gatekeeper decides what passes.

In preauth terms: before any agent action fires, the gatekeeper checks the ledger. If the action class has a record with `approved = TRUE`, the action passes without interruption. If not, it queues.

The gatekeeper is present-tense. It runs on every action, every time, at zero cost — because it's reading a local SQLite file, not making an API call, not waking a human.

This is why `allow-always` matters more than `allow-once`. Allow-always writes to the ledger. Allow-once doesn't. One is a gatekeeper instruction. The other is a one-time exception.

---

## Face 3: The Queue

A queue holds what's pending.

In preauth terms: every action class that hasn't been approved yet enters the queue. The queue surfaces to the human as a batch — not as per-action interruptions.

This is the missing piece in most agent implementations. Instead of interrupting the human once per action, you interrupt them once per *class*. Approve the class. Cache it. Clear the queue.

The queue is future-tense. It's where trust hasn't been granted yet. It's where the dying human's attention is directed — precisely, minimally, without waste.

---

## Why All Three Must Coexist

A ledger without a gatekeeper is just documentation.

A gatekeeper without a ledger has no memory — it asks the human again every session.

A queue without a ledger never resolves — it grows forever.

Preauth cache software is the intersection of all three. It remembers (ledger), enforces (gatekeeper), and collects (queue) — in one small, auditable, local process.

---

## The Dollar Agency Implementation

Currently: SQLite. One table per face. One agent reads it. One human approves it once.

The counter started at 93. Every autonomous action confirmed without interruption was a successful preauth cache hit. Every approval requested was a cache miss written to the queue.

The software is pending. The doctrine is not.

---

*Dollar Agency — three databases, one direction.*
""",
        "tags": [{"name": "software"}, {"name": "ai-agents"}, {"name": "architecture"}]
    },
    {
        "title": "What Does 'Preauth Cache Software' Actually Mean?",
        "content": """# What Does "Preauth Cache Software" Actually Mean?

It's a question worth publishing because the answer defines how autonomous AI agents should behave with limited human oversight.

---

## The Plain English Version

Preauth cache software is a system that remembers what a human has already approved, so the agent never has to ask twice.

That's it.

The complexity is in the implementation. The simplicity is in the doctrine.

---

## Why "Preauth"?

Authorization happens before the action, not during.

Most approval systems are reactive: the agent tries to do something, the system blocks it, the human is interrupted to approve. This is expensive in human attention and in latency.

Preauth flips it: the agent knows in advance what's allowed. The permission is cached before the action fires. The human approved the *class* of action, not the individual instance.

You approved `chmod +x` once. Every future `chmod +x` is pre-authorized. The human doesn't see it again unless the scope changes.

---

## Why "Cache"?

Because permission is a hot-path resource.

The naive implementation is: ask every time. The correct implementation is: ask once, cache the answer, serve from cache forever.

A cache hit costs nothing. A cache miss costs human attention — the scarcest resource in an agency run by a mobile commuter who is also, in the metaphor we're working in, dying.

The cache is local. SQLite. No network calls. No API rate limits. No vendor dependency. Bash-accessible. The Prayer holds: bash never freezes.

---

## What the Software Actually Does

1. **On agent action:** check cache for action class
2. **Cache hit:** execute, log, continue
3. **Cache miss:** add to queue, batch surface to human
4. **On human approval:** write to ledger, clear from queue, set `allow-always`
5. **On every session start:** load cache from SQLite — no re-asking, no re-approving

That's the full loop. Five steps. One SQLite file. Zero interruptions for anything already approved.

---

## The Counter

The agency started with 93 preauthorized actions. That number was the CFO's initial trust grant — the scope of autonomous operation granted before any session began.

Each action taken cleanly is a cache hit. Each new action class needing approval is a miss. The counter tracks the trust balance.

86 remaining after the first session meant 7 new action classes were approved and added to the cache. The cache grew. The interruption rate fell. The CFO's attention was preserved.

This is the software's only real metric: **did the human have to say yes fewer times today than yesterday?**

If yes: the cache is working.

---

## Current Status

Pending build. The doctrine is live. The counter exists in PREAUTH.md. The SQLite schema is designed.

The software ships next.

---

*Dollar Agency — interruption is the cost. Cache is the savings.*
""",
        "tags": [{"name": "preauth"}, {"name": "ai"}, {"name": "agents"}, {"name": "software"}]
    }
]

for article in articles:
    publish(article["title"], article["content"], article.get("tags", []))
