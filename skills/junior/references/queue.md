# 📋 JUNIOR COMMAND QUEUE

Items are executed top-to-bottom. Junior takes the first unchecked item only.

---

- [x] Verify git status of /root/.openclaw/workspace
- [x] Run report_optimizer.py and confirm cache is operational
- [x] Confirm all agents in /root/.openclaw/workspace/agents/ have OPERATIONS.md or REIGN.md
- [x] Audit /root/.openclaw/workspace/skills/ for publishable vendpoints
- [x] Check memory/ledger.jsonl for any missed Shannon transactions
- [x] Verify mattermost/POST.sh is executable and secrets are in place
- [x] Confirm fsh.sh is executable and cache_optimizer.py is operational
- [x] Stage all new files for git commit
- [ ] Read webhooks.md and confirm all outbound targets are configured
- [ ] Test Mattermost webhook (requires MATTERMOST_WEBHOOK_URL in secrets)
- [ ] Wire Discord webhook URL for ClawHub publish alert
- [ ] Test Stripe → ShanApp mint pipeline on port 9004
- [ ] Log all webhook configs to memory/ledger.jsonl
