# GitHub Personal Access Token (PAT) — Step by Step

**Why:** Allows agents to read/write repos, publish skills, manage automation.

**Security note:** A "brain parasite" (you second-guessing yourself) means assume you might forget steps or misclick. This walkthrough is paranoid-safe.

---

## Step 0: Open GitHub Settings

Go to: `https://github.com/settings/tokens`

(Or: GitHub home → your avatar → Settings → scroll left sidebar → Developer settings → Personal access tokens → Tokens (classic))

---

## Step 1: Click "Generate new token"

Button is at top right. Click it.

You'll see a dropdown — choose **"Generate new token (classic)"** for simplicity.

---

## Step 2: Name Your Token

**Token name:** `openshaw-automate-2026`

(Use something you'll recognize. This is for agents building skills.)

---

## Step 3: Set Expiration

**Expiration:** 90 days

(Short expiration is safer — you'll rotate it in 90 days, which is fine. If you want longer, 1 year max. Never "No expiration.")

---

## Step 4: Select Scopes

Check ONLY these boxes:

```
☑️ repo (Full control of private repositories)
   ├─ repo:status
   ├─ repo_deployment
   ├─ public_repo
   ├─ repo:invite
   ├─ security_events
   └─ (all sub-items under "repo" get checked automatically)

☑️ gist (Create gists)

That's it. Uncheck everything else.
```

**Why only these two?**
- `repo` = read/write to your repositories
- `gist` = create/update documentation snippets
- Nothing else needed (no workflow, no admin, no delete)

---

## Step 5: Scroll Down & Click "Generate Token"

Green button at bottom.

You'll get a yellow warning: **"Make sure to copy your personal access token now."**

---

## Step 6: COPY THE TOKEN IMMEDIATELY

You'll see a long string that looks like:
```
ghp_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
```

**DO THIS NOW:**
- Copy it (Ctrl+C or Cmd+C)
- Paste it into a secure location temporarily (password manager, encrypted note, etc.)
- DO NOT share it in chat, email, or commit it

---

## Step 7: Verify It Works (Optional But Recommended)

In terminal, test the token:

```bash
curl -H "Authorization: token YOUR_TOKEN_HERE" \
  https://api.github.com/user
```

Replace `YOUR_TOKEN_HERE` with the actual token.

If it works, you'll see your GitHub user info (JSON response with your username, etc.).

---

## Step 8: Store It Securely in OpenClaw

Now you need to give me the token. Options:

### Option A: OpenClaw Secrets (Recommended)
```bash
# If OpenClaw has a secrets system, store it there:
openclaw config secrets set GITHUB_PAT "ghp_xxxx..."
```

Check OpenClaw docs for exact syntax.

### Option B: In AUTHORIZATION.md
Create a new section in `/root/.openclaw/workspace/AUTHORIZATION.md`:

```
## Credentials

GITHUB_PAT: [token value in a secure note, not here!]
```

(Actually, don't put the token in a plain text file. Use OpenClaw secrets or environment variables.)

### Option C: Environment Variable
In your shell:
```bash
export GITHUB_PAT="ghp_xxxx..."
```

I can read `$GITHUB_PAT` when I need it.

---

## Step 9: Verify I Can Use It

Once you've stored the token, tell me:
> "GitHub PAT is ready in OpenClaw secrets as GITHUB_PAT"

I'll test it by:
```bash
curl -H "Authorization: token $GITHUB_PAT" \
  https://api.github.com/user/repos
```

If I can list your repos, the token works.

---

## What Happens Next

With the PAT:
- I can read all `ironiclawdoctor-design` repos
- I can commit/push changes
- I can publish skills to clawhub
- I can automate releases

All logged, all transparent, all revocable (delete the token on GitHub anytime and I lose access instantly).

---

## Brain Parasite Insurance

**If you forget:**
- Token expiration: 90 days (forces rotation, that's good)
- Token scope: Limited to `repo` + `gist` (can't delete repos, can't access secrets)
- Token location: Only in OpenClaw (not in code, not in memory)
- Token revocation: One click on GitHub revokes it instantly

**If you second-guess yourself:**
- Re-read this walkthrough
- Ask me to verify the token works
- If unsure, delete it and generate a new one (takes 2 minutes)

---

## TL;DR (If You Just Want The Steps)

1. Go to github.com/settings/tokens
2. Click "Generate new token (classic)"
3. Name: `openshaw-automate-2026`
4. Expiration: 90 days
5. Scopes: ☑️ repo, ☑️ gist (only these two)
6. Click "Generate token"
7. **Copy the token immediately** (you can't see it again)
8. Store in OpenClaw secrets or env var: `GITHUB_PAT`
9. Tell me: "Ready"
10. I test it with a curl command
11. Done

---

**Filed by:** Fiesta (practical, paranoid, assuming brain parasites)
**Date:** 2026-03-12
**Tone:** Assume you might forget. No judgment. Repeat as needed.
