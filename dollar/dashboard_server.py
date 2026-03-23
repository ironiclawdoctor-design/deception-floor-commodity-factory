#!/usr/bin/env python3
"""
Dollar Agency Dashboard Server
GMRC/BA-001 — backend-architect
Flask app, port 8080
Serves dashboard.html + /api/status from dollar.db
"""

import os
import sqlite3
import json
from pathlib import Path
from flask import Flask, send_file, jsonify

app = Flask(__name__)

# ── CONFIG ──
HERE = Path(__file__).parent
DB_PATH = HERE / "dollar.db"
DASHBOARD_HTML = HERE / "dashboard.html"
PORT = int(os.environ.get("PORT", 8080))


def get_db():
    """Open a read-only SQLite connection. Returns None if DB missing."""
    if not DB_PATH.exists():
        return None
    conn = sqlite3.connect(str(DB_PATH))
    conn.row_factory = sqlite3.Row
    return conn


# ── ROUTES ──

@app.route("/")
def index():
    """Serve the dashboard HTML."""
    if DASHBOARD_HTML.exists():
        return send_file(str(DASHBOARD_HTML))
    return "<h1>Dashboard not found</h1>", 404


@app.route("/api/status")
def api_status():
    """
    Return JSON:
    {
      total_shannon_supply: int,
      total_backing_usd: float,
      exchange_rate: float,
      shannon_per_usd: float,
      usd_per_shannon: float,
      confessions: [ { agent, failure_type, description, doctrine_extracted, date, shannon_minted } x5 ]
    }
    Graceful fallback if dollar.db is missing.
    """
    conn = get_db()

    if conn is None:
        # Graceful fallback — DB not present
        return jsonify({
            "total_shannon_supply": 0,
            "total_backing_usd": 0.0,
            "exchange_rate": None,
            "shannon_per_usd": None,
            "usd_per_shannon": None,
            "confessions": [],
            "db_status": "offline",
            "message": "dollar.db not found — ledger is cold."
        })

    try:
        # ── Latest exchange rate ──
        rate_row = conn.execute(
            """
            SELECT total_shannon_supply, total_backing_usd,
                   shannon_per_usd, usd_per_shannon
            FROM exchange_rates
            ORDER BY date DESC
            LIMIT 1
            """
        ).fetchone()

        if rate_row:
            total_shannon_supply = int(rate_row["total_shannon_supply"])
            total_backing_usd    = float(rate_row["total_backing_usd"])
            shannon_per_usd      = float(rate_row["shannon_per_usd"])
            usd_per_shannon      = float(rate_row["usd_per_shannon"])
        else:
            total_shannon_supply = 0
            total_backing_usd    = 0.0
            shannon_per_usd      = None
            usd_per_shannon      = None

        # ── Last 5 confessions ──
        confession_rows = conn.execute(
            """
            SELECT agent, failure_type, description, doctrine_extracted,
                   date, shannon_minted, platform, error_code
            FROM confessions
            ORDER BY created_at DESC
            LIMIT 5
            """
        ).fetchall()

        confessions = [
            {
                "agent":              row["agent"],
                "failure_type":       row["failure_type"],
                "description":        row["description"],
                "doctrine_extracted": row["doctrine_extracted"],
                "date":               row["date"],
                "shannon_minted":     int(row["shannon_minted"] or 0),
                "platform":           row["platform"],
                "error_code":         row["error_code"],
            }
            for row in confession_rows
        ]

        return jsonify({
            "total_shannon_supply": total_shannon_supply,
            "total_backing_usd":    total_backing_usd,
            "exchange_rate":        usd_per_shannon,   # legacy compat
            "shannon_per_usd":      shannon_per_usd,
            "usd_per_shannon":      usd_per_shannon,
            "confessions":          confessions,
            "db_status":            "online",
        })

    except Exception as e:
        return jsonify({
            "total_shannon_supply": 0,
            "total_backing_usd":    0.0,
            "exchange_rate":        None,
            "shannon_per_usd":      None,
            "usd_per_shannon":      None,
            "confessions":          [],
            "db_status":            "error",
            "message":              str(e),
        }), 500

    finally:
        conn.close()


@app.route("/api/mint", methods=["POST"])
def api_mint():
    """
    Stub mint endpoint.
    Real minting logic lives in dollar-init.sh / dollar-market.sh.
    Returns current supply as confirmation.
    """
    conn = get_db()
    if conn is None:
        return jsonify({"ok": False, "message": "Ledger offline"}), 503

    try:
        row = conn.execute(
            "SELECT total_shannon_supply FROM exchange_rates ORDER BY date DESC LIMIT 1"
        ).fetchone()
        supply = int(row["total_shannon_supply"]) if row else 0
        return jsonify({"ok": True, "total_shannon_supply": supply, "message": "Mint acknowledged. Add a confession to earn supply."})
    finally:
        conn.close()


@app.route("/health")
def health():
    """Health check for container orchestration."""
    db_ok = DB_PATH.exists()
    return jsonify({"status": "ok", "db": "online" if db_ok else "offline"}), 200


if __name__ == "__main__":
    print(f"[Dollar Agency] Dashboard server starting on port {PORT}")
    print(f"[Dollar Agency] DB path: {DB_PATH} ({'found' if DB_PATH.exists() else 'MISSING — fallback mode'})")
    app.run(host="0.0.0.0", port=PORT, debug=False)
