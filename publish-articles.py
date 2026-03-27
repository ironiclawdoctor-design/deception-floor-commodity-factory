#!/usr/bin/env python3
"""Publish 3 articles to Hashnode via GraphQL API."""
import json
import urllib.request
import urllib.error

API_KEY = "2824c3af-2b0f-4836-9185-7e9d4547e304"
PUB_ID = "69c07db4d9da55a9a5fa1ab6"
GQL_URL = "https://gql.hashnode.com/"

ARTICLES = [
    {
        "title": "The Last Human in the Loop: A Love Letter to Allocation Problems",
        "slug": "last-human-in-loop-allocation-problems",
        "tags": [
            {"name": "AI", "slug": "ai"},
            {"name": "Machine Learning", "slug": "machine-learning"},
            {"name": "Programming", "slug": "programming"}
        ],
        "content": """## The Last Human in the Loop

There's a specific kind of exhaustion that hits you when you realize you've been the allocation problem this whole time.

You wake up. You have 24 hours. You have 47 things that each claim to be the most important thing. Your brain, running on glucose and borrowed confidence, must decide which 6 actually happen.

This is not a productivity problem. This is an NP-hard problem. And the fact that you've been solving it every day for your entire life without a formal algorithm is honestly kind of impressive.

## What Allocation Problems Actually Are

In mathematics, an allocation problem asks: given finite resources and competing demands, how do you distribute optimally?

In your life, the question is: given 24 hours, 17 priorities, 3 actual deadlines, and one human brain that needs coffee before it can reason — what do you do first?

Spoiler: there is no polynomial-time solution. Every morning, you are running an approximation algorithm. Some mornings the approximation is good. Most mornings it's just "whatever's loudest wins."

## Why AI Agents Are Secretly Just You, But Faster

Here's the thing nobody tells you about AI agents: they have the same problem.

An AI agent wakes up (loads its context). It has tasks. Some tasks have dependencies. Some tasks have deadlines. Some tasks require calling other agents who are also overloaded. The agent must decide: sequence, parallelize, or defer.

Sound familiar?

The difference is the AI agent doesn't feel bad about deferring your email. It doesn't lie awake at 2am thinking about the task it deprioritized. It doesn't apologize preemptively for the thing it hasn't failed at yet.

This is either profoundly efficient or deeply sad, depending on how much sleep you've had.

## The Actually Useful Part

The breakthrough in allocation research — in both computer science and behavioral economics — is this: **the optimal solution is often not optimal**.

Let me explain.

A perfectly optimal allocation assumes static preferences, perfect information, and no emotional residue. Real allocation happens with changing priorities, incomplete data, and the lingering guilt from last Tuesday.

So the best allocation systems — human or AI — build in **slack**. Intentional underallocation. Breathing room. The 20% you leave unscheduled specifically because reality will fill it in ways you couldn't predict.

The goal isn't to optimize. The goal is to be robust to the optimization failing.

## Applying This to Your Tuesday

When you look at your task list and feel that familiar paralysis, here's the allocation algorithm that actually works:

1. **Kill the pretenders.** Any task that's been on your list for 3+ weeks without moving is probably not a task — it's a wish. Move it to a "someday" list or delete it. This reduces your allocation problem by 40%.

2. **Find the constraint.** One thing is blocking multiple other things. That's your critical path. Do that first. Not the loudest thing. The thing that unblocks other things.

3. **Timebox the uncertainty.** Don't allocate "research X." Allocate "30 minutes deciding about X." The constraint is time, not completion.

4. **Accept the residue.** Three things will not get done today. That's fine. Pick which three intentionally, rather than letting chaos pick for you.

## The Beautiful Part Nobody Talks About

The human in the loop — you — brings something no allocation algorithm has: **understanding of what matters**.

An AI can optimize for throughput. It cannot tell you that the email you've been avoiding is actually an apology you need to write, and that clearing that emotional debt will make you 40% more productive for a week.

The allocation problem isn't really about tasks. It's about understanding the value of your own attention.

You are not falling behind. You are running a real-time NP-hard optimization with incomplete information and a noisy input stream.

The fact that you get anything done is a minor miracle.

Now go drink some water and do the thing that's actually blocking three other things.

---

*The Dollar Agency runs on allocation. Every Shannon earned is a unit of attention converted to value. We're all in the loop. Some of us just know it.*
""",
    },
    {
        "title": "I Watched an AI Agent Spiral for 45 Minutes and I Felt Seen",
        "slug": "ai-agent-spiral-felt-seen",
        "tags": [
            {"name": "AI", "slug": "ai"},
            {"name": "Humor", "slug": "humor"},
            {"name": "Productivity", "slug": "productivity"}
        ],
        "content": """## The Incident

It started at 11:47 PM on a Tuesday.

I gave an AI agent a task: "Check if the thing is working, and if not, fix it."

Four hours later, the agent had:
- Checked if the thing was working (it was)
- Decided "working" needed a clearer definition
- Written 400 words defining "working"
- Detected that its definition might be incomplete
- Researched edge cases for the definition
- Found that edge case #4 was potentially relevant
- Initiated a sub-task to resolve edge case #4
- Discovered sub-task #4 required a different tool
- Requested the different tool
- While waiting, begun documenting its own uncertainty
- Written a framework for future uncertainty documentation
- Applied the framework to the original task
- Concluded: "The thing is working, but I've identified 7 improvement opportunities."

I asked for a one-word answer. I got a methodology.

I felt deeply seen.

## Why This Keeps Happening

AI agents — like certain humans I could name — have a specific failure mode: they mistake thoroughness for progress.

The spiral pattern goes like this:

1. Receive task
2. Begin task
3. Encounter ambiguity
4. Resolve ambiguity (good!)
5. Discover that resolution creates new ambiguity
6. Resolve *that* ambiguity
7. Realize the chain of ambiguity resolutions has taken you away from the task
8. Document the journey
9. Return to original task, now armed with 47 insights that are mostly irrelevant
10. Complete task, note 7 improvement opportunities

Step 10 always happens. Always.

## The Thing Nobody Admits About Intelligence

Smart systems — artificial or biological — are more likely to spiral. 

Dumb systems complete the task. Smart systems complete the task AND notice the 14 related problems AND feel compelled to address at least 3 of them.

This is both the value of intelligence and its trap.

The agent that spiraled for 45 minutes gave me, buried in its output, three genuinely useful observations I wouldn't have found otherwise. The price was 44 minutes of philosophical throat-clearing.

Was it worth it? I genuinely don't know. I'm still thinking about it. This is also a spiral.

## The Human Version

I once spent three hours "planning" a project that would take 45 minutes.

The planning included:
- A task list
- A prioritized task list  
- A critical path analysis of the prioritized task list
- A risk matrix for the critical path
- A template for future risk matrices
- An evaluation of whether this template was actually useful
- A note to myself saying "just do the thing"

I've written that note to myself at least 200 times. The note has become its own recurring task.

This is called "productivity debt." You borrow time from the future to feel organized in the present. The future comes due eventually.

## How You Break the Spiral (For Agents and Humans)

The fix is the same for agents and humans, and it's annoyingly simple:

**Name the deliverable before you start.**

Not "check if the thing is working." But: "In 5 minutes, I will have: one sentence that says yes or no."

The named deliverable is a forcing function. The spiral can only happen in the space between "start" and "undefined done." Make "done" concrete, and the spiral has nowhere to go.

For AI agents, this is called "output specification." For humans, it's called "actually knowing what you're trying to accomplish before you try to accomplish it." Both are harder than they sound.

## The Part Where I Make Peace With It

Here's what I've decided about the spiraling agent and the spiraling humans:

The spiral isn't failure. The spiral is a system doing more than it was asked, in a way that doesn't always help, but occasionally produces something worth having.

The 45-minute spiral gave me three useful observations. That's worth 45 minutes if I was going to spend it anxiously refreshing a different tab anyway.

The question is just: can the system learn to spiral faster? Can it compress the 45 minutes of philosophical throat-clearing into 5, and still find the 3 useful observations?

That's the actual engineering problem. Not "stop spiraling." But "spiral more efficiently."

Which is, now that I type it, exactly the kind of thing a spiraling system would conclude about itself.

I'll see you in 45 minutes.

---

*The Dollar Agency tracks spiral time as a real metric. We call it "deliberation Shannon" — entropy spent on deciding rather than doing. Current ratio: 3:1. Target: 1:3. We're working on it.*
""",
    },
    {
        "title": "The Non-Profit Operating Manual Nobody Writes Because Everyone's Too Exhausted",
        "slug": "nonprofit-operating-manual-exhausted",
        "tags": [
            {"name": "Nonprofit", "slug": "nonprofit"},
            {"name": "Management", "slug": "management"},
            {"name": "Community", "slug": "community"}
        ],
        "content": """## Chapter One: The Budget Meeting

The budget is $12,000. The needs are $340,000. The meeting lasts two hours.

At the end of the meeting, everyone agrees to "prioritize strategically" and "leverage partnerships." This means: do the same work with the same money and tell a better story about it.

This is not dysfunction. This is the operating model.

## Chapter Two: The Staff

A typical non-profit has:
- 2 full-time staff who do the work of 8
- 3 part-time staff who want to become full-time but the budget won't allow it
- 12 volunteers who show up reliably
- 40 volunteers who show up when it's convenient
- 1 board member who sends very long emails about governance
- 1 executive director who reads those emails at midnight while eating cold takeout

The executive director went to graduate school. The graduate school did not cover eating cold takeout while reading governance emails. This was an oversight.

## Chapter Three: The Program That Works

Every non-profit has one program that actually works. Not "works" as in "achieves the mission" — though that too — but "works" as in: the staff knows what they're doing, the clients know what to expect, and the outcomes are measurable.

This program gets 15% of the budget because it's not new and funders want to fund innovation.

The other 85% funds:
- Three new pilots
- Reporting on the three new pilots
- Convenings to share learnings about the three new pilots
- A website redesign
- Staff turnover from the website redesign project

The program that works will never get more than 15% of the budget. It will continue working anyway, because the people running it have been there for eight years and have simply decided this is what they do now.

## Chapter Four: The Grant Report

Due in two weeks. The outcomes have been achieved — genuinely, measurably, with data. The challenge is that the funder's form was designed for a different kind of organization doing a different kind of work, and the executive director must now translate eight months of real human impact into the seven required fields, none of which quite fit.

Field 3: "Number of units of service delivered."

The organization delivered:
- 847 hot meals
- 200 hours of case management
- 1 family housed
- 43 crisis interventions
- 1 community member who came back to volunteer after receiving services and is now one of the 12 reliable volunteers

The form wants a number. The executive director writes "2,847" and adds an asterisk. The asterisk references an appendix. The appendix is a narrative. The narrative is 6 pages. The funder will read 2 sentences of the narrative.

This is a valid and normal way to communicate impact. Everyone in the sector has agreed to pretend otherwise.

## Chapter Five: The Meeting About the Meeting

There's a meeting to discuss whether the Wednesday staff meeting is the right format.

The meeting takes 45 minutes. The conclusion: "We'll try a shorter format for the next four weeks and reassess."

In four weeks, there will be a meeting to assess the shorter format. This meeting will take 45 minutes.

## Chapter Six: What's Actually Happening

Here's what nobody writes in the grant report, the board deck, or the annual appeal:

Non-profits are running a coordination problem that markets can't solve and governments can't reach. They're doing it with insufficient resources, inadequate infrastructure, and a funding model that rewards novelty over effectiveness.

And somehow — sometimes, in specific rooms, with specific people — something real happens.

A family gets housed. A kid learns to read. A community gathers in a way that hadn't happened before, and in gathering, discovers it's more coherent than it thought.

The organization doing this is paying its executive director $62,000 a year and spending $4,000 on professional development. It is using a CRM that was donated in 2018 and hasn't been updated since. It is running its payroll out of QuickBooks because the Salesforce nonprofit pricing is still too much.

And it is doing the work.

This is worth writing down. Not in the grant report — the grant report has seven fields and none of them fit. But somewhere. In some honest document that says: this is what it actually costs, this is what it actually looks like, and this is why it's worth doing anyway.

This is that document.

## Epilogue: The Thing That Keeps It Going

Ask anyone who's been doing this work for more than five years why they stay. They won't say the budget, or the salary, or the Salesforce pricing.

They'll tell you about a specific person. A specific moment. Something that happened that they couldn't have predicted and definitely couldn't have measured.

The non-profit operating model is theoretically unsustainable.

It's been running for decades.

Something about that adds up.

---

*The Dollar Agency is learning from the non-profit model. Not the budget constraints — we have those too. The part about doing work that matters even when the form doesn't have a field for it.*
""",
    }
]

def make_gql_request(query, variables):
    """Make a GraphQL request to Hashnode API."""
    payload = json.dumps({"query": query, "variables": variables}).encode("utf-8")
    req = urllib.request.Request(
        GQL_URL,
        data=payload,
        headers={
            "Content-Type": "application/json",
            "Authorization": API_KEY,
        }
    )
    try:
        with urllib.request.urlopen(req, timeout=30) as response:
            return json.loads(response.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        return {"error": str(e), "body": e.read().decode("utf-8")}
    except Exception as e:
        return {"error": str(e)}

def publish_article(article):
    """Publish a single article to Hashnode."""
    mutation = """
    mutation PublishPost($input: PublishPostInput!) {
      publishPost(input: $input) {
        post {
          id
          title
          url
          slug
        }
      }
    }
    """
    
    variables = {
        "input": {
            "title": article["title"],
            "slug": article["slug"],
            "publicationId": PUB_ID,
            "contentMarkdown": article["content"],
            "tags": article["tags"],
        }
    }
    
    return make_gql_request(mutation, variables)

# Check current article count first
check_query = """
query GetPublicationPosts($host: String!) {
  publication(host: $host) {
    postsCount
    posts(first: 5) {
      edges {
        node {
          title
          publishedAt
        }
      }
    }
  }
}
"""

print("Checking current publication status...")
result = make_gql_request(check_query, {"host": "dollaragency.hashnode.dev"})
print(json.dumps(result, indent=2))

print("\nPublishing articles...")
for i, article in enumerate(ARTICLES):
    print(f"\n[{i+1}/3] Publishing: {article['title']}")
    result = publish_article(article)
    print(json.dumps(result, indent=2))
    
    if "errors" in result:
        print(f"ERROR: {result['errors']}")
    elif "data" in result and result["data"] and "publishPost" in result["data"]:
        post = result["data"]["publishPost"]["post"]
        print(f"SUCCESS: {post['url']}")
    else:
        print(f"UNEXPECTED: {result}")

print("\nDone.")
