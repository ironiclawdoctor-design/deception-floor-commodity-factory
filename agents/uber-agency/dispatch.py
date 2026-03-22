#!/usr/bin/env python3
"""
AGENCY UBER — Agent Dispatch System
Matches incoming tasks to available agents by specialty.
Surge pricing in Shannon. Rating system in Provincial Merit.
No user interaction required — fully autonomous routing.
"""
import json, os, time, random
from datetime import datetime, timezone

DISPATCH_LOG = "/root/.openclaw/workspace/agents/uber-agency/dispatch_log.jsonl"
LEDGER = "/root/.openclaw/workspace/memory/ledger.jsonl"

# The Fleet — all available agents with their specialties and base fares
FLEET = [
    {"id": "junior",        "specialty": ["queue", "exec", "git", "commit"],          "fare": 0.01, "rating": 5.0},
    {"id": "shanapp-ceo",   "specialty": ["report", "progress", "ledger", "economy"], "fare": 1.22, "rating": 4.8},
    {"id": "cannot",        "specialty": ["blocked", "constraint", "cannot", "gate"], "fare": 0.10, "rating": 4.9},
    {"id": "natewife",      "specialty": ["daycare", "nanny", "child", "persona"],    "fare": 0.50, "rating": 5.0},
    {"id": "bash-nanny",    "specialty": ["process", "sweep", "cleanup", "temp"],     "fare": 0.01, "rating": 4.7},
    {"id": "agency-988",    "specialty": ["despair", "morale", "support", "hope"],    "fare": 0.00, "rating": 5.0},
    {"id": "corruption",    "specialty": ["less-good", "cloud", "external", "api"],   "fare": 1.22, "rating": 3.2},
    {"id": "red-audit-red", "specialty": ["audit", "inquisition", "blue-team"],       "fare": 0.50, "rating": 4.5},
    {"id": "sales-red-team","specialty": ["market", "price", "sell", "revenue"],      "fare": 1.22, "rating": 4.1},
    {"id": "shan-scheduler","specialty": ["time", "schedule", "cron", "trigger"],     "fare": 0.10, "rating": 4.8},
    {"id": "excellence-creep","specialty":["heavy", "optimize", "syscall", "build"],  "fare": 5.00, "rating": 4.6},
    {"id": "pr-dept",       "specialty": ["verb", "language", "tone", "message"],     "fare": 0.50, "rating": 4.3},
    {"id": "elev-exec",     "specialty": ["elevated", "auth", "prophet", "command"],  "fare": 0.00, "rating": 5.0},
    {"id": "mattermost",    "specialty": ["notify", "webhook", "channel", "post"],    "fare": 0.01, "rating": 4.0},
    {"id": "fsh",           "specialty": ["shell", "interface", "terminal", "run"],   "fare": 0.01, "rating": 4.7},
    {"id": "fiesta",        "specialty": ["orchestrate", "route", "chief", "all"],    "fare": 1.22, "rating": 5.0},
]

def surge_multiplier(hour_utc):
    """Surge pricing: higher during peak hours (business hours EST = 13-21 UTC)"""
    if 13 <= hour_utc <= 21:
        return 1.5  # Peak hours
    elif 0 <= hour_utc <= 6:
        return 0.8  # Late night discount
    return 1.0

def match_agent(task_keywords):
    """Match task to best available agent by keyword overlap."""
    task_words = [w.lower() for w in task_keywords.split()]
    scores = []
    for agent in FLEET:
        score = sum(1 for word in task_words if any(s in word or word in s for s in agent["specialty"]))
        scores.append((score, agent["rating"], agent))
    scores.sort(key=lambda x: (x[0], x[1]), reverse=True)
    return scores[0][2] if scores else FLEET[-1]  # Default to Fiesta

def dispatch(task):
    now = datetime.now(timezone.utc)
    surge = surge_multiplier(now.hour)
    agent = match_agent(task)
    fare = round(agent["fare"] * surge, 4)
    
    ride = {
        "timestamp": now.isoformat(),
        "task": task,
        "agent": agent["id"],
        "fare_shan": fare,
        "surge": surge,
        "rating": agent["rating"],
        "specialty_match": agent["specialty"],
        "status": "DISPATCHED"
    }

    with open(DISPATCH_LOG, "a") as f:
        f.write(json.dumps(ride) + "\n")
    with open(LEDGER, "a") as f:
        f.write(json.dumps({"timestamp": now.isoformat(), "agent": "UBER-AGENCY", "task": task, "result": f"Dispatched to {agent['id']} @ {fare} SHAN", "status": "DONE"}) + "\n")

    return ride

if __name__ == "__main__":
    import sys
    task = " ".join(sys.argv[1:]) if len(sys.argv) > 1 else "general task"
    result = dispatch(task)
    print(f"\n🚗 AGENCY UBER DISPATCH")
    print(f"   TASK:    {result['task']}")
    print(f"   AGENT:   @{result['agent']}")
    print(f"   FARE:    {result['fare_shan']} SHAN {'(SURGE x' + str(result['surge']) + ')' if result['surge'] != 1.0 else ''}")
    print(f"   RATING:  {'⭐' * int(result['rating'])} {result['rating']}")
    print(f"   STATUS:  {result['status']}\n")
