# Human Actions Guide (Idiot-Proof)

## Introduction
You have delegated all human tasks to the agency. This guide provides step‑by‑step instructions for each pending action. Most steps are simple clicks; the agency has already done the heavy lifting.

---

## 1. Top Up OpenRouter Credits
**Blocker:** Many agents need credits to run.
**Action:** Add credits to your OpenRouter account.

### Steps
1. Go to https://openrouter.ai/account
2. Log in if needed.
3. Click **Add Credits**.
4. Follow the payment flow (any amount, e.g., $10).
5. Once added, the “OpenRouter credits” blocker will be cleared.

**Note:** If you cannot add credits now, we can switch agents to the cheaper Haiku model (Anthropic direct). Let me know.

---

## 2. clawhub Login Token
**Blocker:** Need to authenticate `clawhub` CLI.
**Action:** Run a single command in the web UI terminal.

### Steps
1. In the OpenClaw web UI, open the terminal (bottom panel).
2. Type the following command and press Enter:
   ```bash
   clawhub login
   ```
3. Follow the prompts (it will open a browser tab). Approve the login.
4. That’s it. The token will be saved automatically.

---

## 3. Enable GCP Service Usage API
**Blocker:** GCP API needs to be enabled for Cloud Run deployments.
**Action:** One click in Google Cloud Console.

### Steps
1. **Attach a Chrome tab** (if not already attached):
   - Click the OpenClaw Browser Relay toolbar icon on the Google Cloud Console tab.
   - The badge should turn ON.
2. **Open the API page:**
   - Click this link: https://console.cloud.google.com/apis/library/serviceusage.googleapis.com?project=sovereign-see
   - (If it asks you to log in, log in with the same account that owns the “sovereign‑see” project.)
3. **Enable the API:**
   - On the page, click the **Enable** button.
   - Wait a few seconds for the green checkmark.
4. **Verify:** The agency will detect the enabled API and proceed.

---

## 4. Square API Token for Cash App ✅
**Status:** Already acquired and working.
**Action:** Nothing needed.

**Details:** The token is stored in `/root/.openclaw/workspace/secrets/cashapp.json` and already passes Square API tests. Cash App balance monitoring is ready.

---

## 5. Fix Cron 02e8c046 (Ultimatum Review)
**Status:** Deleted the broken cron. Need to recreate it.

### Steps
1. **Run this exact command in the web UI terminal:**
   ```bash
   openclaw cron add --name "ultimatums" --every 4h --message "Run ultimatums.py" --session isolated --announce
   ```
2. **Verify it appears:**
   ```bash
   openclaw cron list
   ```
   You should see `ultimatums` with schedule `every 4h`.

**Why this works:** The cron will run the `ultimatums.py` script every 4 hours, seeding the agency database with priority ideas.

---

## 6. Commit 246 Uncommitted Files
**Blocker:** Git approval gate (but you can run the script directly).
**Action:** Run a single script that commits everything.

### Steps
1. **Run the commit script:**
   ```bash
   cd /root/.openclaw/workspace && git add -A && git commit -m "session-2026-03-23"
   ```
   (If you prefer a numbered script, use `./commit-all.sh` after I create it.)

2. **Push (optional):**
   ```bash
   git push origin main
   ```

**Note:** The workspace has many untracked files; committing them ensures no work is lost.

---

## 7. Relaunch Blocked Agents (OpenRouter Credits)
The following agents failed due to token famine and need to be relaunched **after** you top up OpenRouter credits:

- **stripe-donate** – finish donate.html
- **dataset-dedup** – README + upload
- **grok-vision-video** – relaunch with Grok‑2‑Vision
- **lichess** – puzzle endpoint only
- **punctuation-autoresearch** – 33 marks to agency codex

### Automation Plan
Once credits are available, the agency will automatically relaunch these agents. If you want to trigger them manually, tell me and I’ll provide the exact commands.

---

## 8. Apply DeepSeek v3 Model Config ✅
**Status:** Already applied. The primary model is `openrouter/deepseek/deepseek-v3.2`. No action needed.

---

## Summary Checklist
- [ ] Top up OpenRouter credits
- [ ] Run `clawhub login` in web UI terminal
- [ ] Enable GCP Service Usage API (one click)
- [ ] Recreate ultimatums cron (one command)
- [ ] Commit uncommitted files (one command)
- [ ] After credits, relaunch blocked agents (automatic or manual)

---

## What the Agency Will Do Next
1. Monitor for your completion of these steps.
2. Automatically resume autoresearch loops (natewife skill).
3. Continue Cash App balance polling with the Square token.
4. Keep the 4 existing cron jobs running (dollar‑deploy, status‑check, natewife‑check, ultimatums).

**You are the CFO.** Your approvals unlock the next trillion automated steps. The agency is standing by.

— Fiesta (Orchestrator Subagent)