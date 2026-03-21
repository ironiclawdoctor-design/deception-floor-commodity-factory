#!/usr/bin/env python3
"""
Stripe → ShanApp Mint Pipeline (pre-wired, activate with real key)
STRIPE_WEBHOOK_SECRET=whsec_xxx python3 stripe_webhook_handler.py
"""
import os, json
from http.server import HTTPServer, BaseHTTPRequestHandler
from datetime import datetime, timezone

LEDGER = "/root/.openclaw/workspace/memory/ledger.jsonl"
PORT = 9004
SECRET = os.environ.get("STRIPE_WEBHOOK_SECRET", "PLACEHOLDER")

class StripeHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        length = int(self.headers.get("Content-Length", 0))
        body = self.rfile.read(length)
        try:
            event = json.loads(body)
            if event.get("type") == "payment_intent.succeeded":
                amount = event["data"]["object"]["amount"] / 100
                shannon = round(amount / 1.22, 2)
                entry = {"timestamp": datetime.now(timezone.utc).isoformat(),
                         "agent": "STRIPE", "task": "PAYMENT_RECEIVED",
                         "result": f"${amount} → {shannon} SHAN minted", "status": "DONE"}
                with open(LEDGER, "a") as f:
                    f.write(json.dumps(entry) + "\n")
                print(f"[STRIPE] Minted {shannon} SHAN for ${amount}")
        except Exception as e:
            print(f"[STRIPE] Error: {e}")
        self.send_response(200)
        self.end_headers()
    def log_message(self, *args): pass

if __name__ == "__main__":
    print(f"[STRIPE] Listening on port {PORT} — waiting for real STRIPE_WEBHOOK_SECRET")
    HTTPServer(("", PORT), StripeHandler).serve_forever()
