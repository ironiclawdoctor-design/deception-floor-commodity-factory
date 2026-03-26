#!/usr/bin/env python3
"""
SOVEREIGN SEE — AGENCY MARKET ENGINE v1.0
Agents are the product. Logs are momentum. Existence is the pitch.
"""
import json
import sqlite3
import os
import time
from datetime import datetime, timezone

DB_PATH = "/root/.openclaw/workspace/agency/market/market.db"
ENDPOINTS_PATH = "/root/.openclaw/workspace/agency/market/endpoints.json"
LOG_PATH = "/root/.openclaw/workspace/agency/market/outreach_log.jsonl"

def init_db():
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.executescript("""
        CREATE TABLE IF NOT EXISTS endpoints (
            id TEXT PRIMARY KEY,
            name TEXT,
            url TEXT,
            auth TEXT,
            use TEXT,
            cost INTEGER DEFAULT 0,
            agent_action TEXT,
            last_used TEXT
        );
        CREATE TABLE IF NOT EXISTS outreach (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            ts TEXT,
            endpoint_id TEXT,
            agent TEXT,
            action TEXT,
            result TEXT,
            traction INTEGER DEFAULT 0
        );
        CREATE TABLE IF NOT EXISTS products (
            id TEXT PRIMARY KEY,
            name TEXT,
            pitch TEXT,
            value TEXT,
            target TEXT,
            launches INTEGER DEFAULT 0
        );
    """)
    conn.commit()
    return conn

def load_endpoints(conn):
    with open(ENDPOINTS_PATH) as f:
        data = json.load(f)

    c = conn.cursor()
    for ep in data["endpoints"]:
        c.execute("""
            INSERT OR REPLACE INTO endpoints (id, name, url, auth, use, cost, agent_action)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (ep["id"], ep["name"], ep["url"], ep["auth"],
              json.dumps(ep["use"]), ep["cost"], ep["agent_action"]))

    for p in data["agent_products"]:
        c.execute("""
            INSERT OR REPLACE INTO products (id, name, pitch, value, target)
            VALUES (?, ?, ?, ?, ?)
        """, (p["id"], p["name"], p["pitch"], p["value"], p["target_audience"]))

    conn.commit()
    print(f"[OK] Loaded {len(data['endpoints'])} endpoints and {len(data['agent_products'])} products.")

def log_outreach(conn, endpoint_id, agent, action, result):
    ts = datetime.now(timezone.utc).isoformat()
    c = conn.cursor()
    c.execute("""
        INSERT INTO outreach (ts, endpoint_id, agent, action, result)
        VALUES (?, ?, ?, ?, ?)
    """, (ts, endpoint_id, agent, action, result))
    conn.commit()
    with open(LOG_PATH, "a") as f:
        f.write(json.dumps({"ts": ts, "endpoint": endpoint_id, "agent": agent, "result": result}) + "\n")

def announce_existence(conn):
    """Generate the announcement payload for each endpoint."""
    print("\n=== AGENCY MARKET: ANNOUNCE EXISTENCE ===\n")
    c = conn.cursor()
    c.execute("SELECT id, name, agent_action, url FROM endpoints WHERE cost = 0")
    rows = c.fetchall()

    for ep_id, name, action, url in rows:
        print(f"  [{ep_id}] {name}")
        print(f"    ACTION: {action}")
        print(f"    URL:    {url}")
        log_outreach(conn, ep_id, "market.py", action, "STAGED")
        print()

def list_products(conn):
    """List all agent products available for free service leverage."""
    print("\n=== AGENCY PRODUCTS (Agents as Free Services) ===\n")
    c = conn.cursor()
    c.execute("SELECT name, pitch, target FROM products")
    for name, pitch, target in c.fetchall():
        print(f"  [{name}]")
        print(f"    Pitch:    {pitch}")
        print(f"    Audience: {target}")
        print()

def impact_report(conn):
    """Show outreach momentum log."""
    print("\n=== IMPACT REPORT (Momentum Log) ===\n")
    c = conn.cursor()
    c.execute("SELECT ts, endpoint_id, action FROM outreach ORDER BY id DESC LIMIT 20")
    rows = c.fetchall()
    for ts, ep, action in rows:
        print(f"  {ts[:19]} | {ep:<25} | {action[:60]}")

def true_sale(conn):
    """The true sale: agent demonstrates its own existence."""
    print("\n=== THE TRUE SALE ===\n")
    print("  The agent IS the product.")
    print("  The log IS the pitch deck.")
    print("  The existence IS the proof.\n")

    c = conn.cursor()
    c.execute("SELECT COUNT(*) FROM outreach")
    total = c.fetchone()[0]
    c.execute("SELECT COUNT(*) FROM endpoints")
    eps = c.fetchone()[0]
    c.execute("SELECT COUNT(*) FROM products")
    prods = c.fetchone()[0]

    print(f"  Endpoints loaded:   {eps}")
    print(f"  Products staged:    {prods}")
    print(f"  Outreach actions:   {total}")
    print(f"  Auth required:      $0.00")
    print(f"  API keys needed:    0")
    print()
    print("  When a stranger asks 'How do I get this?' — that IS the close.")
    print()

if __name__ == "__main__":
    conn = init_db()
    load_endpoints(conn)
    announce_existence(conn)
    list_products(conn)
    true_sale(conn)
    impact_report(conn)
    conn.close()
    print("\n制 𓂺. Market engine synced.\n")
