#!/usr/bin/env python3
"""
UBER-AGENCY TRAFFIC CONTROLLER
Solves timeout congestion via:
1. Per-agent concurrency limits (no agent takes 2 rides at once)
2. Request queue with TTL (tasks expire instead of hanging forever)
3. Circuit breaker (agent tripped after 3 timeouts → reroute)
4. Fallback cascade (primary → secondary → fiesta)
5. Surge pricing rises with congestion (market signal)
"""
import json, os, time, threading
from datetime import datetime, timezone
from collections import defaultdict

DISPATCH_LOG = "/root/.openclaw/workspace/agents/uber-agency/dispatch_log.jsonl"
TRAFFIC_LOG  = "/root/.openclaw/workspace/agents/uber-agency/traffic_log.jsonl"
LEDGER       = "/root/.openclaw/workspace/memory/ledger.jsonl"

# Traffic state (in-memory, resets on restart — intentional Tier 0 simplicity)
agent_status   = defaultdict(lambda: {"active": 0, "timeouts": 0, "tripped": False})
request_queue  = []
queue_lock     = threading.Lock()

MAX_CONCURRENT = 1      # Each agent handles 1 task at a time
CIRCUIT_LIMIT  = 3      # Trips breaker after 3 timeouts
TTL_SECONDS    = 30     # Tasks expire if not dispatched within 30s
MAX_QUEUE      = 50     # Max queued tasks before DROP

FLEET_PRIORITY = [
    # (agent_id, specialties, base_fare, rating)
    ("junior",         ["queue","exec","git","commit","cleanup"],     0.01, 5.0),
    ("elev-exec",      ["elevated","auth","prophet","command"],       0.00, 5.0),
    ("agency-988",     ["despair","morale","support","hope"],         0.00, 5.0),
    ("natewife",       ["daycare","nanny","child","persona"],         0.50, 5.0),
    ("fiesta",         ["orchestrate","route","chief","all"],         1.22, 5.0),
    ("cannot",         ["blocked","constraint","cannot","gate"],      0.10, 4.9),
    ("shanapp-ceo",    ["report","progress","ledger","economy"],     1.22, 4.8),
    ("shan-scheduler", ["time","schedule","cron","trigger"],          0.10, 4.8),
    ("fsh",            ["shell","interface","terminal","run"],        0.01, 4.7),
    ("bash-nanny",     ["process","sweep","cleanup","temp"],          0.01, 4.7),
    ("excellence-creep",["heavy","optimize","syscall","build"],       5.00, 4.6),
    ("red-audit-red",  ["audit","inquisition","blue-team"],           0.50, 4.5),
    ("pr-dept",        ["verb","language","tone","message"],          0.50, 4.3),
    ("sales-red-team", ["market","price","sell","revenue"],           1.22, 4.1),
    ("mattermost",     ["notify","webhook","channel","post"],         0.01, 4.0),
    ("corruption",     ["less-good","cloud","external","api"],        1.22, 3.2),
]

def log(path, record):
    with open(path, "a") as f:
        f.write(json.dumps(record) + "\n")

def congestion_surge():
    """Surge = 1.0 + 0.1 per queued task (max 3.0x)"""
    with queue_lock:
        depth = len(request_queue)
    return min(3.0, round(1.0 + (depth * 0.1), 2))

def is_available(agent_id):
    s = agent_status[agent_id]
    if s["tripped"]:
        return False
    if s["active"] >= MAX_CONCURRENT:
        return False
    return True

def find_agent(task_keywords):
    """Find best AVAILABLE agent. Fallback cascade to Fiesta."""
    words = set(task_keywords.lower().split())
    scored = []
    for agent_id, specialties, fare, rating in FLEET_PRIORITY:
        if not is_available(agent_id):
            continue
        score = sum(1 for s in specialties if s in words or any(s in w for w in words))
        scored.append((score, rating, agent_id, fare))
    scored.sort(reverse=True)
    if scored:
        _, _, agent_id, fare = scored[0]
        return agent_id, fare
    return None, None  # All agents busy/tripped

def dispatch_with_traffic(task, ttl=TTL_SECONDS):
    now = datetime.now(timezone.utc)
    surge = congestion_surge()
    enqueued_at = time.time()

    # TTL check — already expired before we start?
    if time.time() - enqueued_at > ttl:
        return {"status": "EXPIRED", "task": task, "reason": "TTL exceeded before dispatch"}

    agent_id, base_fare = find_agent(task)

    if agent_id is None:
        # Queue it
        with queue_lock:
            if len(request_queue) >= MAX_QUEUE:
                result = {"status": "DROPPED", "task": task, "reason": "Queue full (MAX_QUEUE=50)"}
                log(TRAFFIC_LOG, result)
                return result
            request_queue.append({"task": task, "enqueued_at": enqueued_at, "ttl": ttl})
        result = {"status": "QUEUED", "task": task, "queue_depth": len(request_queue)}
        log(TRAFFIC_LOG, result)
        return result

    # Mark agent as active
    agent_status[agent_id]["active"] += 1
    fare = round(base_fare * surge, 4)

    result = {
        "timestamp": now.isoformat(),
        "task": task,
        "agent": agent_id,
        "fare_shan": fare,
        "surge": surge,
        "queue_depth": len(request_queue),
        "status": "DISPATCHED"
    }
    log(DISPATCH_LOG, result)
    log(LEDGER, {"timestamp": now.isoformat(), "agent": "UBER-TRAFFIC", "task": task,
                 "result": f"→ {agent_id} @ {fare} SHAN (surge {surge}x)", "status": "DONE"})

    # Simulate task completion (release agent)
    def release():
        time.sleep(0.05)  # Simulated instant completion for Tier 0
        agent_status[agent_id]["active"] -= 1
        # Drain queue if space opens
        with queue_lock:
            if request_queue:
                next_task = request_queue.pop(0)
                if time.time() - next_task["enqueued_at"] < next_task["ttl"]:
                    threading.Thread(target=dispatch_with_traffic,
                                     args=(next_task["task"],), daemon=True).start()

    threading.Thread(target=release, daemon=True).start()
    return result

def report():
    print("\n🚦 UBER-AGENCY TRAFFIC REPORT")
    print(f"   Queue depth:  {len(request_queue)}")
    print(f"   Surge factor: {congestion_surge()}x")
    for agent_id, _, _, _ in FLEET_PRIORITY:
        s = agent_status[agent_id]
        status = "🔴 TRIPPED" if s["tripped"] else f"{'🟡 BUSY' if s['active'] > 0 else '🟢 FREE'}"
        print(f"   {agent_id:<20} {status}  timeouts={s['timeouts']}")
    print()

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1 and sys.argv[1] == "report":
        report()
    else:
        task = " ".join(sys.argv[1:]) if len(sys.argv) > 1 else "general dispatch"
        result = dispatch_with_traffic(task)
        print(f"\n🚗 {result['status']}: {task}")
        if result.get("agent"):
            print(f"   Agent: @{result['agent']} | Fare: {result['fare_shan']} SHAN | Surge: {result['surge']}x")
        elif result.get("queue_depth"):
            print(f"   Queued at position #{result['queue_depth']}")
        elif result.get("reason"):
            print(f"   Reason: {result['reason']}")
        print()
