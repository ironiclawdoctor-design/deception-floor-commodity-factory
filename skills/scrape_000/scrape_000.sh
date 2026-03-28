#!/bin/bash
# scrape_000 — Cloudflare bypass scraper via cf_clearance injection
# Usage: scrape_000.sh [url] [cf_clearance_cookie]
# If no cookie provided: prompts CFO for Safari steps

TARGET_URL="${1:-https://lunaticoutpost.com}"
CF_COOKIE="${2:-}"
TOKEN=$(cat /data/browser-server-token 2>/dev/null)
DOMAIN=$(echo "$TARGET_URL" | sed -E 's|https?://([^/]+).*|\1|')
ROOT_DOMAIN=$(echo "$DOMAIN" | sed -E 's/^[^.]+\.//')

if [ -z "$TOKEN" ]; then
  echo "❌ Camoufox token not found at /data/browser-server-token"
  exit 1
fi

if [ -z "$CF_COOKIE" ]; then
  echo "🍎 SAFARI REQUIRED — cf_clearance cookie needed."
  echo ""
  echo "📱 On Mac Safari:"
  echo "  1. Open Safari → Preferences → Advanced → enable Develop menu"
  echo "  2. Visit: $TARGET_URL"
  echo "  3. Let page load fully (pass Cloudflare challenge)"
  echo "  4. Develop → Show Web Inspector → Storage → Cookies → $DOMAIN"
  echo "  5. Find: cf_clearance → copy the Value"
  echo ""
  echo "📲 On iPhone:"
  echo "  Connect to Mac → Safari Develop menu → [your iPhone] → inspect"
  echo "  OR use Mac Safari on same WiFi network as Ampere"
  echo ""
  echo "⚠️  IP WARNING: Safari and Camoufox must share the same IP."
  echo "   Mobile cellular ≠ Ampere IP → cookie won't work."
  echo "   Mac on WiFi = same network = works."
  echo ""
  echo "✅ Once you have the cookie, run:"
  echo "   /scrape_000 $TARGET_URL YOUR_COOKIE_VALUE"
  exit 0
fi

echo "🔑 Injecting cf_clearance cookie for $DOMAIN..."

# Navigate to blank first
curl -s -X POST "http://127.0.0.1:9222/navigate?token=$TOKEN" \
  -H "Content-Type: application/json" \
  -d "{\"url\":\"https://$DOMAIN\"}" > /dev/null

sleep 2

# Inject cookie
INJECT_JS="
document.cookie = 'cf_clearance=$CF_COOKIE; path=/; domain=.$ROOT_DOMAIN; SameSite=None; Secure';
document.cookie = 'cf_clearance=$CF_COOKIE; path=/; domain=$DOMAIN; SameSite=None; Secure';
'injected';
"

INJECT_RESULT=$(curl -s -X POST "http://127.0.0.1:9222/evaluate?token=$TOKEN" \
  -H "Content-Type: application/json" \
  -d "{\"js\":$(echo "$INJECT_JS" | python3 -c 'import json,sys; print(json.dumps(sys.stdin.read()))')}")

echo "Cookie injection: $INJECT_RESULT"

# Navigate to target
echo "🌐 Navigating to $TARGET_URL..."
NAV_RESULT=$(curl -s -X POST "http://127.0.0.1:9222/navigate?token=$TOKEN" \
  -H "Content-Type: application/json" \
  -d "{\"url\":\"$TARGET_URL\"}")

TITLE=$(echo "$NAV_RESULT" | python3 -c "import sys,json; d=json.load(sys.stdin); print(d.get('title','?'))" 2>/dev/null)

if echo "$TITLE" | grep -qi "access denied\|cloudflare\|just a moment"; then
  echo "❌ Still blocked — title: $TITLE"
  echo "   Cookie may be expired or IP mismatch. Try fresh cookie from same-network browser."
  exit 1
fi

echo "✅ Page loaded: $TITLE"

# Extract content
echo "📄 Extracting page content..."
EXTRACT=$(curl -s -X POST "http://127.0.0.1:9222/extract?token=$TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"selector":"body"}')

# Pull text from result
echo "$EXTRACT" | python3 -c "
import sys, json
d = json.load(sys.stdin)
text = d.get('text', d.get('results', ''))
if isinstance(text, list):
    for item in text[:50]:
        print(item)
else:
    lines = str(text).split('\n')
    for line in lines[:100]:
        line = line.strip()
        if len(line) > 10:
            print(line)
" 2>/dev/null | head -150

echo ""
echo "---"
echo "✅ scrape_000 complete — $TARGET_URL"
echo "📸 Title: $TITLE"
