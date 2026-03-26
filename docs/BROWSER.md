# 🦊 Browser Automation — Camoufox

Camoufox is a stealth Firefox browser running as a **persistent API server** on port 9222.
Sessions persist across calls — sign in once, stay signed in forever.

## ⚡ Best Practice: Text First, Screenshot Second

Always get text/HTML content first — it's faster and cheaper.
Only screenshot when you need to see visual layout.

## How to Use

The browser runs as an HTTP API. All requests need the auth token:

```bash
TOKEN=$(cat /data/browser-server-token)

# Browse a page and get screenshot
curl -X POST "http://localhost:9222/?token=$TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"url":"https://example.com","sessionId":"default"}'

# Extract text content
curl -X POST "http://localhost:9222/?token=$TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"url":"https://example.com","actions":[{"type":"getText","selector":"body"}],"screenshot":false}'

# Login (session persists for next calls)
curl -X POST "http://localhost:9222/?token=$TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"url":"https://site.com/login","sessionId":"mysite","actions":[{"type":"type","selector":"input[name=email]","text":"user@example.com"},{"type":"type","selector":"input[name=password]","text":"pass"},{"type":"click","selector":"button[type=submit]"},{"type":"waitForNavigation"}]}'

# Check proxy status
curl "http://localhost:9222/?token=$TOKEN"
```

## Desktop Proxy (Residential IP)

- **desktopProxy: true** → Traffic routes through user's residential IP
- **desktopProxy: false** → Using server IP

## Full Documentation
- SKILL docs: `/root/.openclaw/skills/camoufox-browser/SKILL.md`
- Examples: `/root/.openclaw/skills/camoufox-browser/EXAMPLES.md`
