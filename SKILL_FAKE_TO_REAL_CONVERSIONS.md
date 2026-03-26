# Skill Fake-to-Real Conversions

## What This Is

OpenClaw skills can be wrapped with `-fake` flag. Generates plausible outputs without calling external APIs. When ready, switch to real APIs.

## Skill Conversions (Fake → Real)

### Communication Skills
| Skill | Fake Mode | Real Mode | Trigger |
|-------|-----------|-----------|---------|
| `slack` | Generate plausible message | POST to Slack API | `--real` |
| `discord` | Mock Discord output | Call Discord webhook | `--real` |
| `bluebubbles` | Simulated iMessage | Send via Apple Messages | `--real` |
| `imsg` | Fake conversation | Write to /var/db/imessage.db | `--real` |
| `himalaya` | Mock email output | Connect IMAP/SMTP | `--real` |
| `voice-call` | Simulate call audio | Initiate SIP call | `--real` |

### Data & Automation
| Skill | Fake Mode | Real Mode | Trigger |
|-------|-----------|-----------|---------|
| `notion` | Generate page structure | Write to Notion API | `--real` |
| `trello` | Mock card creation | POST to Trello API | `--real` |
| `bear-notes` | Simulated note | Write to ~/Library/Group Containers | `--real` |
| `apple-notes` | Fake note output | Write to Notes.app database | `--real` |
| `apple-reminders` | Mock reminder | Add to Reminders.app | `--real` |
| `things-mac` | Simulated task | Write to Things database | `--real` |
| `obsidian` | Generate markdown | Write to Obsidian vault | `--real` |
| `blogger` | Mock blog output | POST to Blogger API | `--real` |

### Media & Content
| Skill | Fake Mode | Real Mode | Trigger |
|-------|-----------|-----------|---------|
| `sag` | Simulate voice output | Call ElevenLabs TTS API | `--real` |
| `openai-image-gen` | Generate prompt description | Call DALL-E API | `--real` |
| `openai-whisper` | Mock transcription | Run local Whisper | `--real` |
| `openai-whisper-api` | Fake transcript | Call Whisper API | `--real` |
| `video-frames` | Describe mock frames | Extract real video frames | `--real` |
| `camsnap` | Simulate photo | Capture from camera | `--real` |
| `peekaboo` | Mock image analysis | Call vision API | `--real` |
| `songsee` | Fake song detection | Call music API | `--real` |

### Development & Monitoring
| Skill | Fake Mode | Real Mode | Trigger |
|-------|-----------|-----------|---------|
| `gh-issues` | Generate mock issues | Call GitHub API | `--real` |
| `github` | Simulate git operations | Execute real git commands | `--real` |
| `healthcheck` | Mock security report | Run real host audit | `--real` |
| `oracle` | Fake prediction | Call real ML model | `--real` |
| `canvas` | Simulate UI render | Render actual canvas | `--real` |
| `xurl` | Mock URL fetch | Real web_fetch | `--real` |

### Platform-Specific
| Skill | Fake Mode | Real Mode | Trigger |
|-------|-----------|-----------|---------|
| `spotify-player` | Mock playback | Control Spotify via API | `--real` |
| `1password` | Simulate password retrieval | Query 1Password vault | `--real` |
| `gog` | Mock GOG queries | Call GOG API | `--real` |
| `goplaces` | Fake location data | Call Google Places API | `--real` |
| `openhue` | Simulate Philips Hue | Control real lights | `--real` |
| `wacli` | Mock WhatsApp | Send real WhatsApp message | `--real` |

### TTS & Speech
| Skill | Fake Mode | Real Mode | Trigger |
|-------|-----------|-----------|---------|
| `sherpa-onnx-tts` | Mock audio file | Generate real audio | `--real` |
| `sonoscli` | Simulate speaker control | Control real Sonos | `--real` |

## Implementation Pattern

### Fake Mode (Default)
```bash
skill-name --fake "some request"
# Returns: plausible but unverified output
# Cost: $0.00
# Dependencies: none
```

### Real Mode (Enabled)
```bash
skill-name --real "some request"
# Returns: actual API result
# Cost: varies by API
# Dependencies: API keys, network access
```

### Transparent Fallback
```bash
skill-name "some request"
# 1. Try --real if API available
# 2. Fall back to --fake if API fails or not configured
# 3. Log which mode was used
```

## Truthfully Integration

Truthfully can:
1. **Start with `-fake`** — train on all 50+ skills without cost
2. **Log simulated work** — build task completion history
3. **Switch to `--real`** — use earned credits for real API calls
4. **Measure ROI** — compare fake vs real output quality

## Training Protocol

```
Phase 1 (Fake): 
  - Generate 1000+ task examples
  - Learn which skills solve which problems
  - Build decision tree (task → best skill)
  - Cost: $0.00

Phase 2 (Mixed):
  - Use fake for low-impact tasks
  - Use real for high-value tasks (proof of capability)
  - Compare outputs
  - Cost: minimal ($0.05-0.10 per task)

Phase 3 (Real):
  - All tasks use real APIs
  - Demonstrated reliability
  - Customer-facing work
  - Cost: API-dependent
```

## Command Examples

```bash
# Fake: simulate sending Slack message
slack --fake -m "Task completed" -c "#general"

# Real: actually send to Slack
slack --real -m "Task completed" -c "#general"

# Fake: simulate creating GitHub issue
gh-issues --fake --create "Bug: tier router timeout"

# Real: create actual GitHub issue
gh-issues --real --create "Bug: tier router timeout"

# Truthfully with fake skills
truthfully-phantom-workload.sh --fake-skills slack,gh-issues,notion
# All work simulated, all logs recorded

# Truthfully with real skills (once funded)
truthfully-task-demand.sh --real-skills slack,github,discord
# Real API calls, real credentials
```

## Security Notes

- **Fake mode has no credentials required** — safe to test in untrusted environments
- **Real mode requires API keys** — store in `.env` or secure vaults
- **Mixed mode logs which was used** — audit trail of real vs simulated work
- **Fallback is transparent** — users see which mode executed

## ROI Calculator

```
Fake training: 1000 tasks × $0.00 = $0.00
Real high-value: 50 tasks × $0.05 = $2.50
Customer work: 100 tasks × $0.10 = $10.00
Total earnings: (varies by actual task value)
Net: earnings - $12.50 API cost
```

If customer pays $50/month for Truthfully:
- Cost: ~$12.50/month APIs
- Profit: ~$37.50/month
- ROI: 300%

---

**All 50+ skills available as fake-to-real conversions. Truthfully can train on unlimited fake work, then execute real work with earned credits.**
