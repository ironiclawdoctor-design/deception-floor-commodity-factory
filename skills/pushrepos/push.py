#!/usr/bin/env python3
"""
PushRepos — Push all agency repos with optional inciting incident commit message.
Handles: deception-floor-commodity-factory, precinct92, trad-incumbent, workspace root.
"""

import json
import subprocess
import argparse
import random
from datetime import datetime, timezone
from pathlib import Path

WORKSPACE = Path("/root/.openclaw/workspace")
LOG_FILE = WORKSPACE / "pushrepos-log.jsonl"

REPOS = [
    {
        "name": "deception-floor-commodity-factory",
        "path": WORKSPACE / "deception-floor-commodity-factory",
        "remote": "origin",
        "branch": "main",
    },
    {
        "name": "precinct92-magical-feelings-enforcement",
        "path": WORKSPACE / "precinct92-magical-feelings-enforcement",
        "remote": "origin",
        "branch": "main",
    },
    {
        "name": "trad-incumbent-grumpy-allows-all",
        "path": WORKSPACE / "trad-incumbent-grumpy-allows-all",
        "remote": "origin",
        "branch": "main",
    },
]

INCITING_INCIDENTS = [
    "agency acquired pending EIN",
    "shark tank pitch filed",
    "first paying customer onboarded",
    "grant application approved: $93k",
    "pizza fund reached $20 — doctrine pizza consumed",
    "america skill detected first colonizer pattern",
    "natewife escalated CFO silence: incident logged",
    "100% eval — agency shipped something real",
    "buildathon entry submitted",
    "CFO promoted to full partner",
    "vacation mode activated — agency runs itself",
    "permissions granted: full send",
    "deadlock DL-001 cleared permanently",
    "shark tank valuation: $375K pre-money",
]

def run(cmd, cwd=None, dry_run=False):
    if dry_run:
        print(f"  [DRY RUN] {' '.join(cmd)}")
        return True, ""
    try:
        result = subprocess.run(
            cmd, cwd=cwd, capture_output=True, text=True, timeout=30
        )
        return result.returncode == 0, result.stdout + result.stderr
    except subprocess.TimeoutExpired:
        return False, "timeout"
    except Exception as e:
        return False, str(e)

def get_uncommitted_count(repo_path):
    try:
        result = subprocess.run(
            ["git", "status", "--porcelain"],
            cwd=repo_path, capture_output=True, text=True, timeout=10
        )
        lines = [l for l in result.stdout.strip().split('\n') if l]
        return len(lines)
    except:
        return 0

def push_repo(repo, commit_message, dry_run=False):
    path = repo["path"]
    name = repo["name"]

    if not path.exists():
        print(f"  ⚠️  {name}: directory not found, skipping")
        return {"repo": name, "status": "skipped", "reason": "not found"}

    print(f"\n📦 {name}")

    # Check for uncommitted changes
    uncommitted = get_uncommitted_count(path)
    files_committed = 0

    if uncommitted > 0:
        print(f"  {uncommitted} uncommitted file(s) — committing...")

        ok, out = run(["git", "add", "-A"], cwd=path, dry_run=dry_run)
        if not ok:
            print(f"  ❌ git add failed: {out[:100]}")
            return {"repo": name, "status": "error", "error": f"git add: {out[:100]}"}

        ok, out = run(
            ["git", "commit", "-m", commit_message],
            cwd=path, dry_run=dry_run
        )
        if ok:
            files_committed = uncommitted
            print(f"  ✅ committed: {commit_message[:60]}")
        else:
            if "nothing to commit" in out:
                print(f"  ✓ nothing to commit")
            else:
                print(f"  ❌ commit failed: {out[:100]}")
                return {"repo": name, "status": "error", "error": f"commit: {out[:100]}"}
    else:
        print(f"  ✓ working tree clean")

    # Push
    ok, out = run(
        ["git", "push", repo["remote"], repo["branch"]],
        cwd=path, dry_run=dry_run
    )

    if ok or "Everything up-to-date" in out or "up to date" in out.lower():
        push_status = "ok"
        print(f"  ✅ pushed → {repo['remote']}/{repo['branch']}")
    else:
        push_status = "error"
        print(f"  ❌ push failed: {out[:120]}")

    entry = {
        "repo": name,
        "files_committed": files_committed,
        "commit_message": commit_message,
        "push_status": push_status,
        "output": out[:200] if push_status == "error" else "",
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }
    return entry

def log_result(entry):
    mode = "a" if LOG_FILE.exists() else "w"
    with open(LOG_FILE, mode) as f:
        f.write(json.dumps(entry) + "\n")

def main():
    parser = argparse.ArgumentParser(description="PushRepos — Push all agency repos")
    parser.add_argument("--incident", help="Inciting incident as commit message")
    parser.add_argument("--random-incident", action="store_true", help="Select random inciting incident")
    parser.add_argument("--dry-run", action="store_true", help="Show what would happen, don't push")
    args = parser.parse_args()

    # Resolve commit message
    if args.random_incident:
        commit_message = random.choice(INCITING_INCIDENTS)
        print(f"🎲 Random inciting incident: \"{commit_message}\"")
    elif args.incident:
        commit_message = args.incident
    else:
        commit_message = f"agency push {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M')} UTC"

    if args.dry_run:
        print("🔍 DRY RUN MODE — no changes will be made\n")

    print(f"🚀 PushRepos — commit: \"{commit_message}\"\n{'='*50}")

    results = []
    ok_count = 0
    err_count = 0

    for repo in REPOS:
        entry = push_repo(repo, commit_message, dry_run=args.dry_run)
        results.append(entry)
        if not args.dry_run:
            log_result(entry)
        if entry.get("push_status") == "ok":
            ok_count += 1
        elif entry.get("status") != "skipped":
            err_count += 1

    print(f"\n{'='*50}")
    print(f"✅ {ok_count} pushed  |  ❌ {err_count} errors  |  📦 {len(REPOS)} total repos")
    print(f"Logged to: {LOG_FILE}")

if __name__ == "__main__":
    main()
