#!/usr/bin/env python3
"""
DEA Signup Server — Dollar Agency internal email collection backend
Port: 9002
Stores signups to: /root/.openclaw/workspace/internal-mail/signups.jsonl
"""

import json
import os
import sys
from datetime import datetime, timezone
from http.server import BaseHTTPRequestHandler, HTTPServer
from pathlib import Path
from urllib.parse import urlparse

SIGNUPS_FILE = Path("/root/.openclaw/workspace/internal-mail/signups.jsonl")
PORT = 9002

# Ensure storage dir exists
SIGNUPS_FILE.parent.mkdir(parents=True, exist_ok=True)


class SignupHandler(BaseHTTPRequestHandler):
    def log_message(self, fmt, *args):
        print(f"[{datetime.now(timezone.utc).isoformat()}] {fmt % args}", file=sys.stderr)

    def send_json(self, code, data):
        body = json.dumps(data).encode("utf-8")
        self.send_response(code)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "POST, GET, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()
        self.wfile.write(body)

    def do_OPTIONS(self):
        self.send_response(204)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "POST, GET, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()

    def do_GET(self):
        parsed = urlparse(self.path)
        if parsed.path == "/health":
            self.send_json(200, {"status": "ok", "service": "dea-signup"})
        elif parsed.path == "/signups":
            # Admin list endpoint
            try:
                entries = []
                if SIGNUPS_FILE.exists():
                    for line in SIGNUPS_FILE.read_text().splitlines():
                        line = line.strip()
                        if line:
                            try:
                                entries.append(json.loads(line))
                            except json.JSONDecodeError:
                                pass
                self.send_json(200, {"count": len(entries), "entries": entries})
            except Exception as e:
                self.send_json(500, {"error": str(e)})
        else:
            # Serve index.html for all other GET requests
            index = Path(__file__).parent / "index.html"
            if index.exists():
                content = index.read_bytes()
                self.send_response(200)
                self.send_header("Content-Type", "text/html; charset=utf-8")
                self.send_header("Content-Length", str(len(content)))
                self.end_headers()
                self.wfile.write(content)
            else:
                self.send_json(404, {"error": "not found"})

    def do_POST(self):
        parsed = urlparse(self.path)
        if parsed.path != "/signup":
            self.send_json(404, {"error": "not found"})
            return

        try:
            length = int(self.headers.get("Content-Length", 0))
            raw = self.rfile.read(length)
            data = json.loads(raw)
        except Exception as e:
            self.send_json(400, {"error": f"bad request: {e}"})
            return

        email = (data.get("email") or "").strip()
        if not email or "@" not in email:
            self.send_json(400, {"error": "valid email required"})
            return

        entry = {
            "ts": datetime.now(timezone.utc).isoformat(),
            "name": (data.get("name") or "").strip() or None,
            "email": email,
            "why": (data.get("why") or "").strip() or None,
            "ip": self.client_address[0],
        }

        try:
            with SIGNUPS_FILE.open("a") as f:
                f.write(json.dumps(entry) + "\n")
            print(f"[SIGNUP] {entry['email']} @ {entry['ts']}", file=sys.stderr)
            self.send_json(201, {"ok": True, "message": "registered"})
        except Exception as e:
            self.send_json(500, {"error": str(e)})


def main():
    server = HTTPServer(("0.0.0.0", PORT), SignupHandler)
    print(f"[DEA Signup Server] listening on port {PORT}", file=sys.stderr)
    print(f"[DEA Signup Server] storing to {SIGNUPS_FILE}", file=sys.stderr)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("[DEA Signup Server] shutting down", file=sys.stderr)
        server.shutdown()


if __name__ == "__main__":
    main()
