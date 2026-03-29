#!/usr/bin/env python3
import json, urllib.request, os

# Load GH token
with open(os.path.expanduser("~/.openclaw/openclaw.json")) as f:
    config = json.load(f)

token = config.get("skills", {}).get("entries", {}).get("gh-issues", {}).get("apiKey", "")
print(f"Token: {token[:10]}...")

repos = [
    "ironiclawdoctor-design/deception-floor-commodity-factory",
    "ironiclawdoctor-design/precinct92-magical-feelings-enforcement",
    "ironiclawdoctor-design/disclaimer-parody-satire-all-feddit",
    "ironiclawdoctor-design/automate-nbm",
    "ironiclawdoctor-design/agency-install",
]

headers = {
    "Authorization": f"Bearer {token}",
    "Accept": "application/vnd.github+json",
    "User-Agent": "Fiesta-Agency"
}

total = 0
for repo in repos:
    url = f"https://api.github.com/repos/{repo}/issues?state=open&per_page=10"
    req = urllib.request.Request(url, headers=headers)
    try:
        with urllib.request.urlopen(req) as r:
            data = json.loads(r.read())
        issues = [i for i in data if "pull_request" not in i]
        print(f"\n=== {repo} ({len(issues)} issues) ===")
        if issues:
            for i in issues:
                labels = ", ".join(l["name"] for l in i.get("labels", []))
                print(f"  #{i['number']} {i['title']}" + (f" [{labels}]" if labels else ""))
            total += len(issues)
        else:
            print("  No open issues")
    except Exception as e:
        print(f"\n=== {repo} ===")
        print(f"  Error: {e}")

print(f"\nTotal open issues: {total}")
