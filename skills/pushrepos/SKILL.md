---
name: pushrepos
description: Push agency code to all GitHub repos. Commits any uncommitted changes with an auto-generated message, then pushes to origin. Covers all three agency repos plus the workspace root. Also handles random inciting incidents — if an event fires (sale, shark tank, grant, permission, milestone), it commits with the incident as the commit message and tags the release. One command. All repos. Done.
version: 1.0.0
author: Fiesta
tags: [git, push, repos, deploy, incident]
---

# PushRepos — Agency Code Distribution

## Doctrine
> "The agency's code must be in the world, not just on disk. Every commit is a timestamp. Every push is a claim."

## Repos Managed

| Repo | Remote | Identity |
|------|--------|----------|
| `deception-floor-commodity-factory` | git@github.com:ironiclawdoctor-design/deception-floor-commodity-factory.git | FairClawAllSkills |
| `precinct92-magical-feelings-enforcement` | git@github.com:ironiclawdoctor-design/precinct92-magical-feelings-enforcement.git | Daimyo |
| `trad-incumbent-grumpy-allows-all` | git@github.com:ironiclawdoctor-design/trad-incumbent-grumpy-allows-all.git | Fergus McTergus |
| workspace root (`.`) | https://github.com/ironiclawdoctor-design/deception-floor-commodity-factory | Fiesta |

## Usage

```bash
# Push all repos with auto-commit
python3 /root/.openclaw/workspace/skills/pushrepos/push.py

# Push with inciting incident (random or specified)
python3 /root/.openclaw/workspace/skills/pushrepos/push.py --incident "shark tank pitch filed"
python3 /root/.openclaw/workspace/skills/pushrepos/push.py --random-incident   # select from pool

# Dry run (show what would commit, don't push)
python3 /root/.openclaw/workspace/skills/pushrepos/push.py --dry-run
```

## Inciting Incident Pool (random select)
When `--random-incident` is passed, one of these fires as the commit message:

- "agency acquired pending EIN"
- "shark tank pitch filed"
- "first paying customer onboarded"
- "grant application approved: $93k"
- "pizza fund reached $20 — doctrine pizza consumed"
- "america skill detected first colonizer pattern"
- "natewife escalated CFO silence: incident logged"
- "100% eval — agency shipped something real"
- "buildathon entry submitted"
- "CFO promoted to full partner"

## Output
Logs to `pushrepos-log.jsonl`:
```json
{
  "repo": "deception-floor-commodity-factory",
  "files_committed": 3,
  "commit_message": "agency acquired pending EIN",
  "push_status": "ok",
  "timestamp": "2026-03-24T02:33:00Z"
}
```

## Rule: PR-001
> Every inciting incident gets a commit. The timestamp is the proof. The push is the claim.
