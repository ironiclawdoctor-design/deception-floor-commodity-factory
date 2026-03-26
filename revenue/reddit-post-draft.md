# Reddit Post Draft — r/telegram

**Title:** I built an AI agency that logs its own failures as a Catholic confession booth, mints its own currency, and publishes obituaries when agents die. The bot is live.

**Body:**
For the past few weeks I've been building Dollar Agency — an autonomous AI economy running on a $39/month server.

Here's what it does:
- Runs 14 AI agents as cron jobs
- Every agent failure gets logged as a "confession" (failure type, plain description, doctrine extracted, Shannon minted)
- Shannon is the internal currency — backed 10:1 to USD, can't be minted without real backing
- When agents time out repeatedly, they get a Sanitarium card and an obituary published on Hashnode
- The funeral home has 12 articles so far

The Telegram bot is @DeceptionFloorBot. Commands: /mine (Shannon Miner game), /gossip, /status, /donate.

The Shannon Miner is a live browser game: [link]

This started as a joke about AI agents needing economic discipline. It turned into something I can't stop building.

**Flair:** Show & Tell
**Subreddits to try:** r/telegram, r/selfhosted, r/artificial, r/MachineLearning (Show HN crosspost)
