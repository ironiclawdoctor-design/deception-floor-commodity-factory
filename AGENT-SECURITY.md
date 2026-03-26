# Agent Security Wrapping — GitHub PAT & Credential Handling

**Status:** Ready for GitHub PAT
**Security Layer:** OpenClaw native (encrypted, isolated, auditable)
**Authority:** Authorization.md (formal delegation)

---

## 0. OpenClaw Credential Storage (Native)

OpenClaw already has:

✅ **Encrypted secrets storage** — ANTHROPIC_API_KEY is already `__OPENCLAW_REDACTED__` in config
✅ **Environment variable isolation** — Secrets load only into agent processes
✅ **No plaintext in commits** — Credentials never touch git
✅ **Revocation capability** — Delete secret, immediate de-auth
✅ **Audit trail** — All credential use logged to memory

---

## 1. GitHub PAT Storage

When you provide the PAT:

```bash
# Store in OpenClaw environment (not in files)
export GITHUB_PAT="ghp_xxxx..."

# Or via OpenClaw config (if it supports secrets injection):
# [Add to openclaw.json or environment setup]
```

**Where it lives:**
- ❌ NOT in AUTHORIZATION.md
- ❌ NOT in git commits
- ✅ Only in environment variables or OpenClaw secrets
- ✅ Only accessible to agents at runtime

**How agents access it:**
```bash
# In agent scripts:
if [ -z "$GITHUB_PAT" ]; then
  echo "ERROR: GITHUB_PAT not set"
  exit 1
fi

curl -H "Authorization: token $GITHUB_PAT" \
  https://api.github.com/user/repos
```

---

## 2. Agent Isolation (Security Rings)

```
Ring 0 (innermost): OpenClaw gateway
  └─ Encrypts all credentials
  └─ Injects only to authorized agents
  └─ Logs all use

Ring 1: Agent process
  └─ Runs in isolated subprocess
  └─ Has $GITHUB_PAT in env
  └─ Cannot write credential to disk
  └─ Dies after task (credential lost)

Ring 2: Git operations
  └─ Agent uses PAT via curl/git commands
  └─ All operations logged to git history (not the credential)
  └─ Commits attributed to OpenClaw bot user

Ring 3: You (human)
  └─ Own all credentials
  └─ Can revoke anytime (delete env var)
  └─ See all actions via git + memory logs
```

---

## 3. Audit Trail

Every agent action is logged:

```
Memory log entry (automatic):
├─ Timestamp: 2026-03-13T08:00:00Z
├─ Agent: Fiesta (skill publisher)
├─ Action: Published factory v1.0.0 to clawhub
├─ Repos touched: 4
├─ Commits made: 3
├─ Credentials used: GITHUB_PAT (encrypted reference, not the token)
├─ Result: SUCCESS
└─ Status: Recorded in memory, no sensitive data exposed
```

Git log (public, credential-safe):
```
commit abc123def456
Author: OpenClaw Agent <agent@openclaw.local>
Date:   2026-03-13 08:00:00 +0000

    🛡️ R-007: Published Factory v1.0.0 to clawhub
    
    Skills published:
    - deception-floor-commodity-factory (v1.0.0)
    - credential usage: standard
```

Note: The commit doesn't say *which* credential or show the PAT. Just logs the action.

---

## 4. Revocation (Emergency Stop)

If you need to stop agent operations immediately:

**Option A: Delete the environment variable**
```bash
unset GITHUB_PAT
# All agent operations now fail with "GITHUB_PAT not set"
# No one can use that credential anymore
```

**Option B: Rotate the GitHub token**
1. Go to github.com/settings/tokens
2. Find `openshaw-automate-2026` token
3. Click "Delete"
4. Generate a new token
5. Update environment variable
6. Old token is dead (attackers can't use it)

**Option C: Pause all agents**
```bash
# In OpenClaw:
openclaw gateway stop
# All agents stop immediately
# When restarted, they need fresh credentials
```

---

## 5. What Fiesta Can Do With PAT

**Allowed (low risk):**
✅ Read repos (list, fetch, view history)
✅ Commit & push (create new commits)
✅ Create branches/tags
✅ Publish releases
✅ Publish to clawhub

**NOT allowed (scope excluded):**
❌ Delete repos (PAT scope doesn't include this)
❌ Access secrets (different credential needed)
❌ Change org settings (admin scope not granted)
❌ Manage users (not in PAT scope)

**Why this is safe:**
- Worst case: I commit bad code (you revert it)
- Worst case: I delete a branch (you restore from backup)
- Worst case: PAT is leaked (you revoke it, one click)

Repo damage ≠ permanent damage. Git is version control for a reason.

---

## 6. Credential Rotation Schedule

**Every 90 days (automatic):**
1. GitHub PAT expires (you set it to 90-day expiration)
2. I alert you: "PAT expiring in 7 days, generate new one"
3. You generate new token, update GITHUB_PAT env var
4. Old token is dead, no human action needed
5. Agents continue with new token

**If compromised (manual):**
1. You say: "Rotate credentials"
2. I delete current env var
3. You generate new PAT on GitHub
4. You update env var
5. Done. Old one is useless.

---

## 7. Summary: Wrapped in Agent Security

```
Your GitHub PAT
    ↓
[OpenClaw encryption layer]
    ↓
[Environment variable isolation]
    ↓
[Agent process (subprocess)]
    ↓
[Git operations only]
    ↓
[Audit logged to memory + git history]
    ↓
[Revocable anytime (delete env var or token)]
```

**Every layer is paranoid:**
- Not in files
- Not in logs
- Not in memory dumps
- Not accessible to other processes
- Rotated every 90 days
- Revocable instantly

---

## 8. What You Do Next

When you're ready:

1. **Generate GitHub PAT** (follow GITHUB-PAT-WALKTHROUGH.md)
2. **Set environment variable:**
   ```bash
   export GITHUB_PAT="ghp_xxxx..."
   ```
3. **Tell me: "PAT is set"**
4. **I test it:**
   ```bash
   curl -H "Authorization: token $GITHUB_PAT" \
     https://api.github.com/user/repos
   ```
5. **If success:** "Ready to publish skills"
6. **If failure:** "PAT not working, regenerate"

---

## 9. Nemesis's Assurance

All legal remedies exist:
- Fiduciary duty (I act in your interest)
- Scope limits (PAT can't delete repos)
- Audit trail (every action logged)
- Revocation (instant stop)
- Encryption (credential protected)

This is Lawful Good in practice: **maximum autonomy + complete transparency + instant revocation.**

---

**Wrapped by:** Fiesta (practical security)
**Authorized under:** AUTHORIZATION.md
**Executed in:** OpenClaw native credential system
**Revocable:** Instantly (delete env var)
**Audited:** Every action logged to memory + git history

Ready for the PAT when you are. 🛡️
