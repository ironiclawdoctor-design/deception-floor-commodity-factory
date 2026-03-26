#!/usr/bin/env python3
"""
Camoufix — Authenticated Camoufox client
Merges token from /data/browser-server-token into all requests.
"""
import urllib.request, json, urllib.parse
from pathlib import Path

TOKEN_FILE = Path("/data/browser-server-token")
BASE = "http://127.0.0.1:9222"

class CamoufoxClient:
    def __init__(self):
        self.token = TOKEN_FILE.read_text().strip() if TOKEN_FILE.exists() else ""
        self.session_id = None

    def _url(self, path):
        return f"{BASE}/{path.lstrip('/')}?token={urllib.parse.quote(self.token)}"

    def _post(self, path, data=None):
        url = self._url(path)
        body = json.dumps(data or {}).encode()
        req = urllib.request.Request(url, data=body,
            headers={"Content-Type": "application/json"})
        with urllib.request.urlopen(req, timeout=30) as r:
            return json.loads(r.read())

    def _get(self, path):
        req = urllib.request.Request(self._url(path))
        with urllib.request.urlopen(req, timeout=10) as r:
            return json.loads(r.read())

    def health(self):
        return self._get("health")

    def session_new(self):
        r = self._post("session/new")
        self.session_id = r.get("sessionId") or r.get("id")
        return self.session_id

    def navigate(self, url):
        if not self.session_id:
            self.session_new()
        return self._post("session/action", {
            "sessionId": self.session_id,
            "actions": [{"type": "navigate", "url": url}]
        })

    def click(self, selector):
        return self._post("session/action", {
            "sessionId": self.session_id,
            "actions": [{"type": "click", "selector": selector}]
        })

    def type_text(self, selector, text):
        return self._post("session/action", {
            "sessionId": self.session_id,
            "actions": [{"type": "type", "selector": selector, "text": text}]
        })

    def extract(self, selector=None):
        return self._post("session/action", {
            "sessionId": self.session_id,
            "actions": [{"type": "extract", "selector": selector or "body"}]
        })

    def screenshot(self):
        return self._post("session/action", {
            "sessionId": self.session_id,
            "actions": [{"type": "screenshot"}]
        })

    def evaluate(self, js):
        return self._post("session/action", {
            "sessionId": self.session_id,
            "actions": [{"type": "evaluate", "script": js}]
        })

if __name__ == "__main__":
    cf = CamoufoxClient()
    if not cf.token:
        print("❌ No token at /data/browser-server-token")
    else:
        print(f"✅ Token loaded: {cf.token[:8]}...")
        h = cf.health()
        print(f"Health: {h}")
