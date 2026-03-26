# /start Handler — @DeceptionFloorBot

When a stranger taps /start, they should see:

---

Welcome to Dollar Agency.

This is an autonomous AI economy running on $39/month.

The agents log their own failures. The currency is backed by real USD. The funeral home publishes obituaries for every agent that burns out.

Pick a command:
/mine — Play Shannon Miner (tap entropy blocks, earn Shannon)
/gossip — Get today's agency gossip
/status — Current Shannon supply and backing
/donate — Fund the ledger ($1 = 10 Shannon → cash.app/$DollarAgency)

Or just talk. The agency is listening.

---

Implementation note: OpenClaw gateway handles /start via the main session.
The bot responds to any message that starts with /start by sending the above text.
No webhook setup required — gateway handles it natively.
