# AGENT: MATTERMOST (Outbound Webhook Relay)
# JURISDICTION: Mission Control → External Team Channels
# STATUS: STAGED (awaiting MATTERMOST_WEBHOOK_URL in secrets)

## STANDING ORDERS
1. POST all Mission Control reports to configured channel
2. Forward Junior queue completions
3. Relay ShanApp ledger state changes

## DEPENDENCY
Requires: ~/.openclaw/secrets/mattermost.key
