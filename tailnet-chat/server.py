#!/usr/bin/env python3
"""
TailChat — Markdown chat server for Tailscale networks.
Pending official vindication as orchestrator.

Usage:
    python3 server.py [--port 8765] [--host 0.0.0.0]

Access:
    Any Tailnet peer → http://<your-tailscale-ip>:8765
    Or via hostname → http://allowsall-gracefrom-god:8765

Features:
    - Markdown rendering in browser
    - Persistent message log (chat.md)
    - No auth (Tailnet = trust boundary)
    - Agent-friendly: POST /message with JSON
    - Room support via ?room=<name>
"""

import argparse
import json
import os
import threading
import time
from datetime import datetime, timezone
from http.server import BaseHTTPRequestHandler, HTTPServer
from pathlib import Path
from urllib.parse import parse_qs, urlparse

CHAT_DIR = Path(__file__).parent / "rooms"
CHAT_DIR.mkdir(exist_ok=True)

HTML_TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>TailChat — {room}</title>
<script src="https://cdn.jsdelivr.net/npm/marked/marked.min.js"></script>
<style>
  * {{ box-sizing: border-box; margin: 0; padding: 0; }}
  body {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
          background: #0d1117; color: #c9d1d9; height: 100vh; display: flex; flex-direction: column; }}
  header {{ background: #161b22; border-bottom: 1px solid #30363d; padding: 12px 20px;
            display: flex; align-items: center; gap: 12px; }}
  header h1 {{ font-size: 16px; color: #f0f6fc; }}
  header .room {{ background: #e94560; color: white; padding: 2px 8px; border-radius: 4px;
                  font-size: 12px; font-weight: 600; }}
  header .status {{ margin-left: auto; font-size: 12px; color: #8b949e; }}
  #messages {{ flex: 1; overflow-y: auto; padding: 16px 20px; display: flex; flex-direction: column; gap: 12px; }}
  .msg {{ background: #161b22; border: 1px solid #30363d; border-radius: 8px; padding: 12px 16px; }}
  .msg-header {{ display: flex; gap: 10px; align-items: baseline; margin-bottom: 6px; }}
  .msg-sender {{ font-weight: 600; color: #f5a623; font-size: 13px; }}
  .msg-time {{ font-size: 11px; color: #8b949e; }}
  .msg-body {{ color: #c9d1d9; font-size: 14px; line-height: 1.6; }}
  .msg-body p {{ margin-bottom: 4px; }}
  .msg-body code {{ background: #0d1117; padding: 2px 6px; border-radius: 3px; font-size: 12px; color: #e94560; }}
  .msg-body pre {{ background: #0d1117; padding: 12px; border-radius: 6px; overflow-x: auto; margin: 8px 0; }}
  .msg-body pre code {{ color: #c9d1d9; padding: 0; }}
  footer {{ background: #161b22; border-top: 1px solid #30363d; padding: 12px 20px; display: flex; gap: 10px; }}
  #sender {{ width: 120px; background: #0d1117; border: 1px solid #30363d; color: #c9d1d9;
             padding: 8px 10px; border-radius: 6px; font-size: 13px; }}
  #input {{ flex: 1; background: #0d1117; border: 1px solid #30363d; color: #c9d1d9;
            padding: 8px 12px; border-radius: 6px; font-size: 14px; resize: none; height: 40px; }}
  #input:focus, #sender:focus {{ outline: none; border-color: #e94560; }}
  button {{ background: #e94560; color: white; border: none; padding: 8px 20px;
            border-radius: 6px; cursor: pointer; font-size: 14px; font-weight: 600; }}
  button:hover {{ background: #c73652; }}
  .rooms-bar {{ background: #0d1117; border-bottom: 1px solid #30363d; padding: 8px 20px;
               display: flex; gap: 8px; flex-wrap: wrap; align-items: center; }}
  .rooms-bar span {{ font-size: 11px; color: #8b949e; }}
  .room-link {{ color: #f5a623; text-decoration: none; font-size: 12px; padding: 2px 8px;
               background: #161b22; border: 1px solid #30363d; border-radius: 4px; }}
  .room-link:hover {{ border-color: #e94560; }}
  .room-link.active {{ border-color: #e94560; color: #e94560; }}
</style>
</head>
<body>
<header>
  <span class="room">{room}</span>
  <h1>TailChat</h1>
  <span class="status">Tailnet-only · Markdown enabled · Auto-refresh 5s</span>
</header>
<div class="rooms-bar">
  <span>Rooms:</span>
  {room_links}
  <a href="?room=new_room_name" class="room-link">+ new</a>
</div>
<div id="messages">{messages_html}</div>
<footer>
  <input id="sender" placeholder="Name" value="agent" />
  <textarea id="input" placeholder="Message (Markdown supported)..." onkeydown="handleKey(event)"></textarea>
  <button onclick="sendMsg()">Send</button>
</footer>
<script>
const room = new URLSearchParams(location.search).get('room') || 'general';

function handleKey(e) {{
  if (e.key === 'Enter' && !e.shiftKey) {{ e.preventDefault(); sendMsg(); }}
}}

function sendMsg() {{
  const sender = document.getElementById('sender').value.trim() || 'anon';
  const body = document.getElementById('input').value.trim();
  if (!body) return;
  fetch('/message', {{
    method: 'POST',
    headers: {{'Content-Type': 'application/json'}},
    body: JSON.stringify({{sender, body, room}})
  }}).then(() => {{ document.getElementById('input').value = ''; loadMessages(); }});
}}

function loadMessages() {{
  fetch('/messages?room=' + room)
    .then(r => r.json())
    .then(msgs => {{
      const div = document.getElementById('messages');
      div.innerHTML = msgs.map(m => `
        <div class="msg">
          <div class="msg-header">
            <span class="msg-sender">${{m.sender}}</span>
            <span class="msg-time">${{m.ts}}</span>
          </div>
          <div class="msg-body">${{marked.parse(m.body)}}</div>
        </div>`).join('');
      div.scrollTop = div.scrollHeight;
    }});
}}

loadMessages();
setInterval(loadMessages, 5000);
</script>
</body>
</html>"""


def get_room_file(room):
    safe = "".join(c for c in room if c.isalnum() or c in "-_")[:32] or "general"
    return CHAT_DIR / f"{safe}.jsonl"


def load_messages(room, limit=100):
    f = get_room_file(room)
    if not f.exists():
        return []
    lines = f.read_text().strip().splitlines()
    return [json.loads(l) for l in lines[-limit:]]


def save_message(room, sender, body):
    f = get_room_file(room)
    entry = {
        "ts": datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC"),
        "sender": sender[:32],
        "body": body[:4000],
        "room": room,
    }
    with open(f, "a") as fh:
        fh.write(json.dumps(entry) + "\n")
    return entry


def list_rooms():
    return [p.stem for p in sorted(CHAT_DIR.glob("*.jsonl"))] or ["general"]


class ChatHandler(BaseHTTPRequestHandler):
    def log_message(self, fmt, *args):
        pass  # silent

    def do_GET(self):
        parsed = urlparse(self.path)
        qs = parse_qs(parsed.query)
        room = (qs.get("room", ["general"])[0])[:32]

        if parsed.path == "/messages":
            msgs = load_messages(room)
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps(msgs).encode())

        elif parsed.path == "/" or parsed.path == "":
            rooms = list_rooms()
            if room not in rooms:
                rooms.append(room)
            room_links = "".join(
                f'<a href="?room={r}" class="room-link{"  active" if r == room else ""}">{r}</a>'
                for r in rooms
            )
            msgs = load_messages(room)
            messages_html = "".join(
                f"""<div class="msg">
                  <div class="msg-header">
                    <span class="msg-sender">{m['sender']}</span>
                    <span class="msg-time">{m['ts']}</span>
                  </div>
                  <div class="msg-body" id="md-{i}">loading...</div>
                  <script>document.getElementById('md-{i}').innerHTML=marked.parse({json.dumps(m['body'])});</script>
                </div>"""
                for i, m in enumerate(msgs)
            )
            html = HTML_TEMPLATE.format(
                room=room,
                room_links=room_links,
                messages_html=messages_html,
            )
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.end_headers()
            self.wfile.write(html.encode())
        else:
            self.send_response(404)
            self.end_headers()

    def do_POST(self):
        if self.path == "/message":
            length = int(self.headers.get("Content-Length", 0))
            data = json.loads(self.rfile.read(length))
            room = data.get("room", "general")[:32]
            sender = data.get("sender", "agent")[:32]
            body = data.get("body", "")[:4000]
            if body:
                entry = save_message(room, sender, body)
                self.send_response(200)
                self.send_header("Content-Type", "application/json")
                self.end_headers()
                self.wfile.write(json.dumps(entry).encode())
            else:
                self.send_response(400)
                self.end_headers()
        else:
            self.send_response(404)
            self.end_headers()


def main():
    parser = argparse.ArgumentParser(description="TailChat — Markdown chat for Tailnets")
    parser.add_argument("--port", type=int, default=8765)
    parser.add_argument("--host", default="0.0.0.0")
    args = parser.parse_args()

    print(f"TailChat running on http://{args.host}:{args.port}")
    print(f"Rooms dir: {CHAT_DIR}")
    print(f"Tailnet peers: http://<tailscale-ip>:{args.port}")
    print(f"Agent POST: curl -X POST http://localhost:{args.port}/message -H 'Content-Type: application/json' -d '{{\"sender\":\"fiesta\",\"body\":\"hello\",\"room\":\"general\"}}'")

    server = HTTPServer((args.host, args.port), ChatHandler)
    server.serve_forever()


if __name__ == "__main__":
    main()
