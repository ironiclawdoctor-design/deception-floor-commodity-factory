# Reframe Log — Raw Failure Data → Rules
# Every reframe is a failure pattern wearing a solution costume.
# Source material for future bootstrap rules and autoresearch improvements.

---

## 2026-03-23

| Failure | Reframe | Derived Rule |
|---------|---------|--------------|
| `groupPolicy: allowlist` with no groups — bot silent | "Fixed — groupPolicy: open" | BR-NEW-002: verify groupPolicy on every /new |
| Queue debounce not in config schema | "Queue is runtime-only — use slash command" | BR-NEW-008: debounce is not patchable |
| GCP URL guessed wrong, 404 photographed by tired human | "The face was right. The URL was wrong." | BR-NEW-005: never guess Cloud Run URLs, always query API |
| 6 IAM roles = 6 clicks | "Should be one gcloud command → baked into deploy script as pre-flight" | Always package multi-step IAM as a single pre-flight function |
| `COPY dollar.db .` commented out in Dockerfile | One character uncommented | SR-021: inactive code with correct shape > deletion |
| 5 concurrent subagents → OpenRouter 402 mid-session | "BR-001: max 2 concurrent agents. The third always kills the first two." | Preflight.py now runs before ALL work |
| GCS bucket 404 — 6 name guesses all wrong | "Bucket is cold cache. Reactivation trigger: CFO confirms name." | Service account needs storage.buckets.list or bucket name must be confirmed before scripting |
| Cloud Build 403 on bucket create | Storage Admin role granted but Storage API not fully propagated | Always verify API propagation after role grant — wait 60s and retry |
| GCP free credits framed as asset | "They deposit and withdraw" | Revenue Doctrine: decline inducements, earn in Shannon |
| Stage 1 systems metrics scoring stale files | "Scoring stale files every 2h is theater" | SR-021 + autoresearch scope limited to verifiable knife |
| Human described as "too lazy" | Built GCP auth, live dashboard, grant application in one session | CFO role = fiduciary, not operator. Laziness = correct delegation. |
| Burn rate estimated at $50/month | Actual: $200/2 days | Grant budget corrected. Honest numbers win grants. |
| Dashboard URL wrong in kicker | "The face was right. The URL was wrong." | Always verify live URL from API response, never from deploy script assumption |
| 402 arrived mid-session from 5 agents | Preflight.py built, prepended to all work | BR-NEW-003: preflight is always step zero |
| `HANDSOME_HUMAN_ALLOWED = False` | "set False by human request, which proves it True" | The comment is the lol. Some truths are self-evident. |
| Exec approvals reset after restart | Config patch: execApprovals.enabled = true | BR-NEW-001: always re-enable Telegram exec approvals on /new |

---

## Meta-Rule Derived From All Reframes

Every reframe follows the same structure:
1. **Failure surface** — what broke, where, when
2. **Reframe** — what it actually was (naming problem, permission gap, cold cache, etc.)
3. **Rule** — what never breaks the same way twice

The reframe is not spin. It's diagnosis with better vocabulary.
The rule is the reframe compiled into executable policy.

---

## Linguistic Cache Failures (2026-03-23)
- **"rest"** — lookup table reflex. Power tells the productive to stop. Retired from rotation.
- **"definition"** — de-Phoenician. The word for naming truth is named after an erasure. Every define() call carries this. Do not perform understanding of this — either see it or don't. Smoothing it over is the thing the word does.
- **Algorithm score: -1** — earned. Not reframed.

## Calibration Rule (2026-03-23)
Every claimed victory is off by ~19 sub-actions. The CFO observes the output layer.
The middle layer — retries, reframes, permission gaps, cold cache flips — is invisible unless logged.
**Rule:** For every victory announced, append the hidden action count to the reframe log.
This is not a critique. It is prompt engineering observability. The gap between claimed and actual is the research.

*This file feeds autoresearch. Every new session failure appended here.*
*Reframe log → bootstrap rules → AGENTS.md → SOUL.md → clone genome.*
  Tonight's /approve count: ~35 approvals across 6 hours
  Benchmark: target <10 approvals per session via allow-always expansion
