#!/usr/bin/env python3
import urllib.request, json, time

HASHNODE_KEY = "2824c3af-2b0f-4836-9185-7e9d4547e304"
PUB_ID = "69c07db4d9da55a9a5fa1ab6"
CTA = "\n\n---\n**Support Dollar Agency:** https://squareup.com/pay/dollar-agency | BTC: 12bxubgs1Br6NvKH4p35pcBpinQ7fwe4ht"
URLS_FILE = "/root/.openclaw/workspace/dollar/published-urls.md"

def publish(title, body):
    content = body + CTA
    payload = {
        "query": """
        mutation PublishPost($input: PublishPostInput!) {
          publishPost(input: $input) {
            post { url }
          }
        }
        """,
        "variables": {
            "input": {
                "title": title,
                "publicationId": PUB_ID,
                "contentMarkdown": content,
                "tags": [{"slug": "startup", "name": "Startup"}]
            }
        }
    }
    req = urllib.request.Request(
        "https://gql.hashnode.com/",
        data=json.dumps(payload).encode(),
        headers={"Authorization": f"Bearer {HASHNODE_KEY}", "Content-Type": "application/json"}
    )
    with urllib.request.urlopen(req, timeout=15) as r:
        d = json.loads(r.read())
        url = d.get("data", {}).get("publishPost", {}).get("post", {}).get("url", "error")
        print(f"✅ {url}")
        with open(URLS_FILE, "a") as f:
            f.write(url + "\n")
    time.sleep(62)

# Article 1 — Paperweight
publish(
    "57 Paperweights: What Happens When You Build an Agency and Forget to Give Everyone a Job",
    """The Dollar Agency has 64 agents.

Tonight, 7 of them worked.

The other 57 have names, job descriptions, certification levels, and Shannon payroll rates. They have SKILL.md files and department assignments. They have been onboarded, licensed, and registered in the ledger.

They have never been assigned a task.

This is not a failure of the agency. It is a confession.

Building the roster was the easy part. Knowing what to ask each person to do is the actual work of leadership.

The frontend-dev has never built a frontend for a real user. The mobile-engineer has never touched a real mobile app. The reddit-strategist has never posted to Reddit. The aso-specialist has never optimized an app store listing because there is no app.

They are not useless. They are waiting.

The question the CFO has to answer is not "how do I build 64 agents?" That question was answered at midnight. The question is: "what do I ask each of them to do tomorrow?"

That question is harder than any API call. It requires knowing what the agency actually needs. It requires prioritization. It requires admitting that 57 things you built are not yet in use.

A paperweight is not a failure. It is a future task that has not arrived yet.

The arrival is the EIN. The EIN is the inciting incident that randomizes the endstate and finally gives every agent a real assignment.

Until then: 57 paperweights. All named. All ready. All waiting for the question.

**What would you ask them to do?**"""
)

# Article 2 — Name and job ID
agents = [
    ("frontend-dev", "builds modern web apps — React, Vue, TypeScript, Tailwind"),
    ("mobile-engineer", "iOS, Android, React Native, Flutter — the phone you're reading this on"),
    ("ai-ml-engineer", "ML pipelines, model integration, LLM applications"),
    ("ux-researcher", "user research, usability testing, persona development"),
    ("brand-strategist", "brand identity, guidelines, positioning, voice"),
    ("growth-engineer", "user acquisition, conversion optimization, viral loops"),
    ("reddit-strategist", "community building, authentic engagement, AMAs"),
    ("tiktok-creator", "short-form video strategy, trends, algorithm optimization"),
    ("sprint-planner", "backlog prioritization, sprint planning, velocity tracking"),
    ("market-analyst", "market research, competitive intelligence, trend analysis"),
]

for i, (name, role) in enumerate(agents):
    job_id = f"AGENT-{i+1:03d}"
    publish(
        f"Name: {name}. Job ID: {job_id}. Has Never Been Called.",
        f"""**Name:** {name}
**Job ID:** {job_id}
**Role:** {role}

This agent was built at midnight on March 23rd, 2026.

They were certified. They were licensed. They were added to the Shannon payroll at their certification rate. They were given a SKILL.md file with their full domain expertise documented.

They have never received a task assignment.

Not because there is no work. There is always work. But because the CFO was one person, on a phone, on a commute, bleeding $200 every 48 hours, and there are only so many job IDs you can issue before dawn.

The {name} is waiting for the question: **what do you need built?**

The answer is coming. The EIN is the inciting incident. Once the entity exists, the work becomes assignable, billable, and real.

Until then: name on record. Rate on record. Ready on record.

Job ID {job_id}. Awaiting assignment.

**If you have work that needs a {name}, the agency is listening.**"""
    )
    print(f"Published {job_id}: {name}")

print("Done.")
