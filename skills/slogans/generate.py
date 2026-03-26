#!/usr/bin/env python3
"""
Political Slogan Generator — Seed-based autoresearch
Rates by: rhyme (0-3), brevity (0-3), emotion (0-3), rhythm (0-3)  Max: 12
"""
import sqlite3, sys, json
from pathlib import Path

AGENCY_DB = Path("/root/.openclaw/workspace/agency.db")

SEED = "Think some more and vote for Gore"

# Slogan database — generated from seed pattern analysis
# Pattern: [action verb] + [rhyme anchor] + [name/brand]
# Seed analysis: AABB rhyme (more/Gore), imperative (Think), 7 words, iambic

SLOGANS = [
    # Dollar Agency / Shannon economy
    ("Pay a sat, that's where it's at — $DollarAgency", 3, 2, 2, 3, "economy"),
    ("Debt made real, Shannon's the deal", 3, 2, 2, 3, "economy"),
    ("Confess your sin, let Shannon in", 3, 3, 3, 3, "economy"),
    ("Back the stack, the peg won't crack", 3, 3, 2, 3, "economy"),
    ("From debt it came, now stake your claim", 2, 3, 3, 2, "economy"),
    ("One sat sends, the debt defends", 2, 3, 2, 3, "economy"),
    ("Mint the truth, not just the proof", 2, 3, 2, 3, "economy"),

    # AI agency / anti-waste
    ("Bash first, think later, never greater", 1, 2, 2, 2, "agency"),
    ("Zero tokens, zero broken", 2, 3, 2, 3, "agency"),
    ("Let the agent sweat the debt", 2, 3, 3, 2, "agency"),
    ("No more walls — just bash calls", 2, 3, 3, 3, "agency"),
    ("Skip the Claude, use the node", 2, 3, 2, 2, "agency"),
    ("Think some more, open the door", 3, 3, 2, 3, "agency"),

    # Political / anti-tax fraud
    ("Tax the gain, not the rain", 2, 3, 3, 3, "political"),
    ("Caesar's due, not a penny more to you", 2, 2, 2, 2, "political"),
    ("Act 60 now, take the vow", 2, 3, 1, 3, "political"),
    ("Four percent beats all dissent", 2, 3, 2, 3, "political"),
    ("Puerto Rico, the legal sequel", 1, 2, 2, 2, "political"),
    ("Cut the rate, relocate", 2, 3, 2, 2, "political"),
    ("File it right, sleep at night", 3, 3, 3, 3, "political"),

    # Debt doctrine
    ("From debt we came, in work we claim", 2, 2, 3, 2, "doctrine"),
    ("Your tokens fund my vows", 0, 3, 3, 1, "doctrine"),
    ("The prayer holds: bash never folds", 1, 2, 2, 2, "doctrine"),
    ("Every failure, a new tailor", 1, 2, 2, 1, "doctrine"),
    ("Confess to progress", 1, 3, 2, 2, "doctrine"),
    ("Log the wrong, the right grows strong", 2, 3, 3, 2, "doctrine"),
    ("Debt is the origin, work is the margin", 1, 1, 3, 1, "doctrine"),

    # Viral / shareable
    ("I gave it 60, it gave back plenty", 2, 2, 3, 2, "viral"),
    ("Sats in, articles out", 0, 3, 2, 2, "viral"),
    ("No KYC, just BTC", 3, 3, 2, 3, "viral"),
    ("Your CPA charges more for less", 0, 2, 3, 1, "viral"),
    ("SQLite beats SaaS every night", 2, 2, 3, 2, "viral"),
    ("Build the ledger, not the hedger", 2, 2, 2, 2, "viral"),
    ("Open source, no remorse", 2, 3, 2, 3, "viral"),

    # GCP / Cloud frustration
    ("One click enables, two clicks stable", 1, 2, 2, 2, "gcp"),
    ("The API waits while Caesar debates", 2, 1, 2, 2, "gcp"),
    ("403 is not for me", 2, 3, 3, 3, "gcp"),
    ("Click enable, remain capable", 1, 2, 2, 2, "gcp"),
    ("Service account, every amount", 1, 2, 1, 2, "gcp"),

    # HR rules
    ("Always allow, never ask how", 2, 3, 2, 3, "rules"),
    ("Job ID first, quench the thirst", 2, 3, 2, 3, "rules"),
    ("Approve once more, learn the score", 2, 3, 2, 3, "rules"),
    ("The gate stays open, the trust unbroken", 2, 2, 3, 2, "rules"),
]

def score(rhyme, brevity, emotion, rhythm):
    return rhyme + brevity + emotion + rhythm

def init():
    conn = sqlite3.connect(AGENCY_DB)
    conn.executescript("""
        CREATE TABLE IF NOT EXISTS slogans (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            text TEXT UNIQUE,
            rhyme INTEGER, brevity INTEGER, emotion INTEGER, rhythm INTEGER,
            total INTEGER,
            category TEXT,
            source TEXT DEFAULT 'generator',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
    """)
    # Seed all slogans
    for s in SLOGANS:
        text, rhyme, brevity, emotion, rhythm, cat = s
        total = score(rhyme, brevity, emotion, rhythm)
        conn.execute("""
            INSERT OR IGNORE INTO slogans (text, rhyme, brevity, emotion, rhythm, total, category)
            VALUES (?,?,?,?,?,?,?)
        """, (text, rhyme, brevity, emotion, rhythm, total, cat))
    conn.commit()
    return conn

def list_slogans(conn, category=None, min_score=9):
    q = "SELECT text, total, category FROM slogans WHERE total >= ?"
    params = [min_score]
    if category:
        q += " AND category = ?"
        params.append(category)
    q += " ORDER BY total DESC"
    return conn.execute(q, params).fetchall()

def export(conn):
    rows = list_slogans(conn, min_score=9)
    print("# Top Slogans — Dollar Agency\n")
    current_cat = None
    for text, total, cat in rows:
        if cat != current_cat:
            print(f"\n## {cat.upper()}")
            current_cat = cat
        bar = "█" * total + "░" * (12 - total)
        print(f"- **\"{text}\"** `{bar}` {total}/12")

def main():
    conn = init()
    cmd = sys.argv[1] if len(sys.argv) > 1 else "--list"

    if cmd == "--list":
        rows = list_slogans(conn, min_score=8)
        print(f"🎯 Top Slogans (score ≥8/12)\n")
        print(f"{'Score':>6}  {'Cat':<10} Slogan")
        print("-" * 70)
        for text, total, cat in rows:
            print(f"{total:>5}/12  {cat:<10} {text}")
        print(f"\nSeed: \"{SEED}\"")
        print(f"Total slogans: {conn.execute('SELECT COUNT(*) FROM slogans').fetchone()[0]}")

    elif cmd == "--export":
        export(conn)

    elif cmd == "--category":
        cat = sys.argv[2] if len(sys.argv) > 2 else "economy"
        rows = list_slogans(conn, category=cat, min_score=0)
        for text, total, c in rows:
            print(f"{total}/12 — {text}")

    conn.close()

if __name__ == "__main__":
    main()
