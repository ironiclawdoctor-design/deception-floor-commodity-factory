#!/usr/bin/env python3
"""
Pizza Party Department — Morale, Celebration, and Shannon Minting
Triggered by milestones, permissions, and CFO generosity.
"""

import json
import argparse
from datetime import datetime
from pathlib import Path

WORKSPACE = Path("/root/.openclaw/workspace")
LOG_FILE = WORKSPACE / "pizza-party-log.jsonl"
FUND_FILE = WORKSPACE / "pizza-fund.json"

SHANNON_TABLE = {
    "100pct_eval":        {"shannon": 50,  "emoji": "🎯", "label": "100% eval hit"},
    "permission_granted": {"shannon": 25,  "emoji": "🔓", "label": "Permission granted"},
    "grant_submitted":    {"shannon": 100, "emoji": "📋", "label": "Grant submitted"},
    "first_payment":      {"shannon": 200, "emoji": "💵", "label": "First real payment (RETROACTIVE)"},
    "heart_reaction":     {"shannon": 10,  "emoji": "❤️",  "label": "CFO heart reaction"},
    "deadlock_free_24h":  {"shannon": 30,  "emoji": "🔓", "label": "24h deadlock-free"},
    "full_activation":    {"shannon": 500, "emoji": "🍕", "label": "CFO says pizza party"},
    "milestone":          {"shannon": 40,  "emoji": "🏆", "label": "Milestone reached"},
}

def load_fund():
    if FUND_FILE.exists():
        return json.loads(FUND_FILE.read_text())
    return {"total_shannon": 0, "pizza_fund_shannon": 0, "events": 0, "usd_equivalent": 0.0}

def save_fund(fund):
    FUND_FILE.write_text(json.dumps(fund, indent=2))

def mint_shannon(event_type: str, detail: str):
    config = SHANNON_TABLE.get(event_type, {"shannon": 20, "emoji": "🎉", "label": event_type})
    shannon = config["shannon"]
    emoji = config["emoji"]
    label = config["label"]

    fund = load_fund()
    pizza_cut = int(shannon * 0.05)  # 5% to pizza fund
    fund["total_shannon"] += shannon
    fund["pizza_fund_shannon"] += pizza_cut
    fund["events"] += 1
    fund["usd_equivalent"] = round(fund["pizza_fund_shannon"] / 10.0, 2)  # 10 Shannon = $1
    save_fund(fund)

    entry = {
        "event": event_type,
        "label": label,
        "detail": detail,
        "shannon_minted": shannon,
        "pizza_fund_contribution": pizza_cut,
        "pizza_fund_total": fund["pizza_fund_shannon"],
        "pizza_fund_usd": fund["usd_equivalent"],
        "message": f"{emoji} Pizza party: {label}. {shannon} Shannon minted. {pizza_cut} to pizza fund.",
        "timestamp": datetime.utcnow().isoformat() + "Z"
    }

    mode = "a" if LOG_FILE.exists() else "w"
    with open(LOG_FILE, mode) as f:
        f.write(json.dumps(entry) + "\n")

    return entry

def show_status():
    fund = load_fund()
    print(f"\n🍕 PIZZA PARTY DEPT — STATUS REPORT")
    print(f"{'='*40}")
    print(f"Total Shannon minted (morale): {fund['total_shannon']}")
    print(f"Pizza Fund balance:            {fund['pizza_fund_shannon']} Shannon")
    print(f"USD equivalent:                ${fund['usd_equivalent']:.2f}")
    print(f"Total events celebrated:       {fund['events']}")
    if fund['usd_equivalent'] >= 20:
        print(f"\n🚨 FUND THRESHOLD REACHED — CFO should buy actual pizza.")
    else:
        remaining = 20 - fund['usd_equivalent']
        print(f"\n${remaining:.2f} until real pizza is doctrine-required.")

def main():
    parser = argparse.ArgumentParser(description="Pizza Party Department")
    parser.add_argument("--event", help="Event type", default="milestone")
    parser.add_argument("--detail", help="Event detail", default="")
    parser.add_argument("--status", action="store_true", help="Show pizza fund status")
    args = parser.parse_args()

    if args.status:
        show_status()
        return

    entry = mint_shannon(args.event, args.detail)
    print(entry["message"])
    print(f"  Pizza fund: {entry['pizza_fund_total']} Shannon (${entry['pizza_fund_usd']:.2f})")

if __name__ == "__main__":
    main()
