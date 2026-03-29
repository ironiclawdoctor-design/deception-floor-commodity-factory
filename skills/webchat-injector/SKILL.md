---
name: webchat-injector
description: Inject messages into website chat widgets (Intercom, Drift, Tidio, LiveChat, custom). Locates the chat input on any URL, types a message, submits it, and returns the bot/agent reply. Use when the CFO says "send this to the chatbot on [site]".
version: 1.0.0
author: Fiesta
tags: [chat, bot, website, inject, browser, automation]
---

# webchat-injector

## Trigger
Any request to interact with a chatbot on a website.

## What It Does
1. Opens the target URL in browser
2. Detects the chat widget (Intercom, Drift, Tidio, LiveChat, Freshchat, custom)
3. Clicks the chat launcher button
4. Types the message into the input field
5. Submits and captures the reply
6. Returns the full exchange

## Usage Pattern

```
/webchat [url] [message]
```

Examples:
- "Send 'I want to open an account' to the chatbot on lucidtrading.com"
- "Ask the Valid Trading chatbot for developer API access"

## Implementation

### Step 0 — Open URL
```python
browser.action("open", url=target_url)
browser.action("snapshot")  # identify widget type
```

### Step 1 — Detect Widget
Common selectors by platform:
- **Intercom**: `#intercom-launcher`, `.intercom-launcher`
- **Drift**: `#drift-widget`, `[data-testid="chat-widget"]`  
- **Tidio**: `#tidio-chat-iframe`, `.tidio-1`
- **LiveChat**: `#chat-widget-container`, `.lc-1ixnuo6`
- **Freshchat**: `#fc_frame`, `.freshwidget-button`
- **Custom**: Any `iframe[src*="chat"]`, `[class*="chat-button"]`, `[id*="chat"]`

### Step 2 — Click Launcher
```python
browser.action("act", request={"kind": "click", "ref": chat_launcher_ref})
browser.action("snapshot")  # confirm open
```

### Step 3 — Type Message
```python
browser.action("act", request={"kind": "type", "ref": chat_input_ref, "text": message})
browser.action("act", request={"kind": "press", "key": "Enter"})
```

### Step 4 — Capture Reply
Wait 3-8s, snapshot, extract reply text from chat window.

### Step 5 — Return
Return: `{sent: message, reply: bot_reply, platform: detected_platform, url: target_url}`

## Known Platforms

| Platform | Launcher Selector | Input Selector |
|---|---|---|
| Intercom | `#intercom-launcher` | `.intercom-composer-textarea` |
| Drift | `#drift-widget-container button` | `.drift-composer-input` |
| Tidio | `#tidio-chat-iframe` | (iframe — switch context) |
| LiveChat | `#chat-widget` | `textarea[name="message"]` |
| Custom iframe | `iframe[src*="chat"]` | (switch context) |

## Iframe Handling
If widget is in an iframe:
```python
browser.action("act", request={"kind": "evaluate", "fn": "document.querySelector('#chat-iframe').contentWindow.document.querySelector('textarea').focus()"})
```

## Rate Limiting
- Max 1 message per 5s to avoid bot detection
- Rotate user-agent via Camoufox default

## Error States
- Widget not found → log selector, take screenshot, add to lookup table
- CAPTCHA on chat → report to CFO, cannot bypass
- Rate limited → wait 60s, retry once

## Log Output
Append to `/root/.openclaw/workspace/webchat-log.jsonl`:
```json
{"ts": "ISO", "url": "...", "platform": "...", "sent": "...", "reply": "...", "success": true}
```
