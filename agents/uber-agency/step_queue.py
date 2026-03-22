#!/usr/bin/env python3
"""
93-STEP TRAFFIC TIMEOUT SOLUTION QUEUE
Step 1: Execute immediately.
Steps 2-93: Stored in SQLite queue for async execution.
"""
import sqlite3, json, time
from datetime import datetime, timezone

DB = "/root/.openclaw/workspace/agents/uber-agency/step_queue.db"
LEDGER = "/root/.openclaw/workspace/memory/ledger.jsonl"

STEPS = [
    # === PERSISTENCE LAYER (1-10) ===
    "Create SQLite DB 'uber_traffic.db' with tables: tasks, agents, circuit_state, dead_letter, metrics",
    "Add table 'tasks': id, task_text, status, created_at, dispatched_at, completed_at, agent_id, ttl, retries, priority",
    "Add table 'agents': id, name, specialties, base_fare, rating, active_count, is_tripped, trip_count, last_tripped_at",
    "Add table 'circuit_state': agent_id, trip_count, tripped_at, auto_reset_seconds (default 300)",
    "Add table 'dead_letter': task_id, reason, dropped_at, retry_count",
    "Add table 'metrics': timestamp, agent_id, event_type, value",
    "Seed 'agents' table from FLEET_PRIORITY on first run using INSERT OR IGNORE",
    "Persist agent_status dict to SQLite on every state change (not just in-memory)",
    "Add startup routine: load circuit_state from DB into memory to survive restarts",
    "Add shutdown hook: flush in-memory queue to tasks table with status='PENDING'",

    # === CIRCUIT BREAKER AUTO-RESET (11-20) ===
    "Add column 'auto_reset_at' to circuit_state: computed as tripped_at + auto_reset_seconds",
    "Add function check_auto_reset(agent_id): query DB, if now > auto_reset_at set tripped=False",
    "Call check_auto_reset() at top of is_available() before returning False",
    "Add exponential backoff to auto_reset_seconds: 300s → 600s → 1200s per consecutive trip",
    "Add function manually_reset_circuit(agent_id): admin override via CLI arg --reset-agent",
    "Log circuit trip events to metrics table with event_type='circuit_trip'",
    "Log circuit reset events to metrics table with event_type='circuit_reset'",
    "Add --circuit-report CLI arg: show all tripped agents + reset ETAs",
    "Alert via local_relay.py when any agent trips circuit (write to webhook_queue.jsonl)",
    "Auto-reset all circuits on clean startup (assume clean slate if no task was in-flight)",

    # === REAL TIMEOUT MEASUREMENT (21-30) ===
    "Replace 0.05s simulated sleep with actual task_start_time = time.time() in dispatch",
    "Add task_end_time = time.time() in release() and compute elapsed = end - start",
    "If elapsed > TTL_SECONDS: increment agent_status[agent_id]['timeouts']",
    "Write elapsed time to tasks table column 'duration_seconds' on completion",
    "Add percentile tracking: p50, p95, p99 latency per agent in metrics table",
    "Add function get_agent_latency_stats(agent_id): query metrics for last 100 tasks",
    "Display latency stats in --report output next to each agent",
    "If agent p95 latency > TTL * 0.8: auto-reduce that agent's concurrency limit to 0 (rest mode)",
    "Add rest_mode to agent_status: agent accepts no new tasks until p95 recovers",
    "Log timeout events to dead_letter table with reason='TTL_EXCEEDED'",

    # === DEAD LETTER QUEUE (31-38) ===
    "On TTL expiry: insert task to dead_letter table with reason, drop_time, retry_count=0",
    "Add function retry_dead_letter(task_id): increment retry_count, re-enqueue if < MAX_RETRIES (3)",
    "Add background thread: every 60s scan dead_letter for retry_count < MAX_RETRIES, re-enqueue",
    "Add --dead-letter CLI arg: display all DLQ entries with retry counts",
    "Add --retry-all CLI arg: force retry all DLQ entries immediately",
    "On DROP (queue full): also write to dead_letter with reason='QUEUE_FULL'",
    "Add DLQ size to --report output",
    "Alert via local_relay.py if DLQ depth > 10",

    # === AGENT HEALTH CHECKS (39-46) ===
    "Add function health_check(agent_id): ping agent by running a no-op task, measure response time",
    "Add background thread: every 30s run health_check on all FREE agents",
    "If health_check fails 3 times: mark agent as tripped in circuit_state",
    "Add column 'last_health_check' to agents table: timestamp of last successful check",
    "Add column 'health_status' to agents table: HEALTHY / DEGRADED / DOWN",
    "Show health_status in --report output",
    "Add --health-check CLI arg: run immediate health check on all agents",
    "Log health check results to metrics table with event_type='health_check'",

    # === LOAD BALANCING (47-54) ===
    "Add weighted round-robin selection: agents with lower active_count get preference",
    "Add least-connections routing: always dispatch to agent with fewest active tasks",
    "Add sticky routing option: same task_type always goes to same agent (session affinity)",
    "Add agent capacity weights: excellence-creep max_concurrent=1, junior max_concurrent=3",
    "Store per-agent concurrency limits in agents table column 'max_concurrent'",
    "Modify is_available() to check agent-specific max_concurrent instead of global constant",
    "Add spread factor: if 2+ agents equally available, pick the one with highest rating",
    "Add geographic/priority zones: CRITICAL tasks bypass queue entirely",

    # === PRIORITY QUEUE (55-62) ===
    "Replace list-based queue with heapq: priority = (urgency_score, enqueued_at)",
    "Add urgency scoring: 'elevated'/'auth' tasks get priority=0, general tasks priority=5",
    "Add task priority field to tasks table column 'priority' (0=highest, 9=lowest)",
    "Implement heappush/heappop for enqueue/dequeue operations",
    "Add --priority flag to dispatch: python3 traffic.py --priority 0 'critical task'",
    "VIP tasks (priority=0) bypass TTL: they wait indefinitely until dispatched",
    "Add priority escalation: task priority increases by 1 every 10s in queue",
    "Log priority changes to metrics table with event_type='priority_escalated'",

    # === RETRY LOGIC (63-70) ===
    "Add retry_count column to tasks table (default 0, max 3)",
    "On task failure/timeout: increment retry_count, re-enqueue with same priority",
    "Add exponential backoff for retries: wait 2^retry_count seconds before re-enqueue",
    "On retry: prefer different agent than original (avoid same failure mode)",
    "Add jitter to retry backoff: random 0-5s to prevent thundering herd",
    "After MAX_RETRIES (3): move to dead_letter with reason='MAX_RETRIES_EXCEEDED'",
    "Log retry events to metrics table with event_type='task_retry'",
    "Add --no-retry flag: some tasks should fail fast without retry",

    # === METRICS AND OBSERVABILITY (71-80) ===
    "Add Prometheus-compatible /metrics endpoint on port 9225 (simple HTTP server)",
    "Expose metrics: tasks_dispatched_total, tasks_failed_total, queue_depth, surge_factor",
    "Expose per-agent metrics: agent_active_tasks, agent_timeout_count, agent_rating",
    "Add structured logging: all events as JSON to agents/uber-agency/uber.log",
    "Add log rotation: max 10MB per log file, keep 5 rotations",
    "Add --metrics CLI arg: dump current metrics snapshot to stdout as JSON",
    "Add dashboard view: python3 traffic.py dashboard (curses-based live view)",
    "Track task throughput: tasks_per_minute rolling average in metrics table",
    "Alert when throughput drops >50% from baseline (write to webhook_queue.jsonl)",
    "Add trace_id to every task: UUID for end-to-end tracking across logs",

    # === SURGE PRICING IMPROVEMENTS (81-86) ===
    "Add surge ceiling: max surge = 3.0x regardless of queue depth",
    "Add surge floor: min surge = 0.5x during idle periods (reward early users)",
    "Add time-of-day surge schedule: load from JSON config file",
    "Add per-agent surge: high-demand agents (junior) get independent surge multiplier",
    "Add surge prediction: if queue growing >5 tasks/min, pre-announce surge",
    "Log surge changes to metrics table with event_type='surge_change'",

    # === STABILITY AND OPS (87-93) ===
    "Add graceful shutdown: SIGTERM handler drains in-flight tasks before exit",
    "Add config file: uber_config.json with all tunable constants (TTL, MAX_QUEUE, etc.)",
    "Add --config CLI arg: load alternate config file for testing",
    "Add integration with Junior queue: completed tasks auto-update queue.md",
    "Add Mattermost notification: daily digest of dispatch metrics via local_relay.py",
    "Add self-healing: if all agents tripped, auto-reset oldest-tripped after 60s",
    "Write all 93 steps as completed tasks back to Junior's queue.md with checkboxes",
]

def init_db():
    conn = sqlite3.connect(DB)
    c = conn.cursor()
    c.execute("""CREATE TABLE IF NOT EXISTS step_queue (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        step_number INTEGER,
        description TEXT,
        status TEXT DEFAULT 'PENDING',
        created_at TEXT,
        completed_at TEXT
    )""")
    conn.commit()
    return conn

def load_steps(conn):
    c = conn.cursor()
    c.execute("SELECT COUNT(*) FROM step_queue")
    count = c.fetchone()[0]
    if count == 0:
        now = datetime.now(timezone.utc).isoformat()
        for i, step in enumerate(STEPS, 1):
            c.execute("INSERT INTO step_queue (step_number, description, created_at) VALUES (?,?,?)",
                      (i, step, now))
        conn.commit()
        print(f"✅ Loaded {len(STEPS)} steps into SQLite queue")

def execute_step_1(conn):
    """Execute ONLY step 1 immediately. Rest stay queued."""
    c = conn.cursor()
    c.execute("SELECT step_number, description FROM step_queue WHERE step_number=1")
    row = c.fetchone()
    if not row:
        return

    step_num, desc = row
    print(f"\n🚀 EXECUTING STEP 1 NOW:")
    print(f"   {desc}\n")

    # Actually do it: create the uber_traffic SQLite DB
    uber_db = sqlite3.connect("/root/.openclaw/workspace/agents/uber-agency/uber_traffic.db")
    ub = uber_db.cursor()
    ub.execute("""CREATE TABLE IF NOT EXISTS tasks (
        id TEXT PRIMARY KEY, task_text TEXT, status TEXT, created_at TEXT,
        dispatched_at TEXT, completed_at TEXT, agent_id TEXT,
        ttl INTEGER, retries INTEGER DEFAULT 0, priority INTEGER DEFAULT 5,
        duration_seconds REAL, trace_id TEXT
    )""")
    ub.execute("""CREATE TABLE IF NOT EXISTS agents (
        id TEXT PRIMARY KEY, name TEXT, specialties TEXT, base_fare REAL,
        rating REAL, active_count INTEGER DEFAULT 0, is_tripped INTEGER DEFAULT 0,
        trip_count INTEGER DEFAULT 0, last_tripped_at TEXT, max_concurrent INTEGER DEFAULT 1,
        health_status TEXT DEFAULT 'HEALTHY', last_health_check TEXT
    )""")
    ub.execute("""CREATE TABLE IF NOT EXISTS circuit_state (
        agent_id TEXT PRIMARY KEY, trip_count INTEGER DEFAULT 0,
        tripped_at TEXT, auto_reset_seconds INTEGER DEFAULT 300, auto_reset_at TEXT
    )""")
    ub.execute("""CREATE TABLE IF NOT EXISTS dead_letter (
        id INTEGER PRIMARY KEY AUTOINCREMENT, task_id TEXT, reason TEXT,
        dropped_at TEXT, retry_count INTEGER DEFAULT 0
    )""")
    ub.execute("""CREATE TABLE IF NOT EXISTS metrics (
        id INTEGER PRIMARY KEY AUTOINCREMENT, timestamp TEXT, agent_id TEXT,
        event_type TEXT, value REAL
    )""")
    uber_db.commit()
    uber_db.close()
    print("   ✅ uber_traffic.db created with 5 tables")

    # Mark step 1 as done
    now = datetime.now(timezone.utc).isoformat()
    c.execute("UPDATE step_queue SET status='DONE', completed_at=? WHERE step_number=1", (now,))
    conn.commit()

def show_queue_status(conn):
    c = conn.cursor()
    c.execute("SELECT status, COUNT(*) FROM step_queue GROUP BY status")
    rows = c.fetchall()
    print("\n📋 STEP QUEUE STATUS:")
    for status, count in rows:
        print(f"   {status}: {count} steps")
    c.execute("SELECT step_number, description FROM step_queue WHERE status='PENDING' ORDER BY step_number LIMIT 5")
    print("\n   NEXT 5 PENDING:")
    for row in c.fetchall():
        print(f"   {row[0]:2d}. {row[1][:80]}...")

if __name__ == "__main__":
    conn = init_db()
    load_steps(conn)
    execute_step_1(conn)
    show_queue_status(conn)
    conn.close()
