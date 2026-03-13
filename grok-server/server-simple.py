#!/usr/bin/env python3
"""
Grok Server - Pure Python HTTP + Bash Inference
Simplest, most reliable version
No deprecation warnings.
"""

import http.server
import socketserver
import json
import sys
import os
from pathlib import Path
from datetime import datetime, timezone

PORT = int(sys.argv[1]) if len(sys.argv) > 1 else 8888
WORKSPACE = Path("/root/.openclaw/workspace/grok-server")
STATS_FILE = WORKSPACE / "stats.txt"

# Ensure directories exist
(WORKSPACE / "logs").mkdir(exist_ok=True)
if not STATS_FILE.exists():
    STATS_FILE.write_text("0\n0\n")

class GrokHandler(http.server.BaseHTTPRequestHandler):
    
    def read_stats(self):
        lines = STATS_FILE.read_text().strip().split('\n')
        return int(lines[0] or 0), int(lines[1] or 0)
    
    def write_stats(self, requests, inferences):
        STATS_FILE.write_text(f"{requests}\n{inferences}\n")
    
    def grok_infer(self, prompt):
        """Pure bash inference logic in Python"""
        requests, inferences = self.read_stats()
        inferences += 1
        self.write_stats(requests, inferences)
        
        prompt_lower = prompt.lower()
        
        if "bash" in prompt_lower:
            response = "bash is the firewall. everything else is shadow."
        elif "token" in prompt_lower:
            response = "zero tokens. infinite bash. victory."
        elif "time" in prompt_lower:
            response = f"time: {datetime.now(timezone.utc).strftime('%H:%M:%S UTC')}. stop procrastinating."
        elif "weather" in prompt_lower:
            import random
            response = f"{random.randint(5, 35)}°C outside. irrelevant to bash."
        else:
            response = "[grok thinking in bash mode...] your query has been acknowledged."
        
        return response
    
    def send_json(self, code, data):
        response = json.dumps(data)
        self.send_response(code)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", len(response))
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        self.wfile.write(response.encode())
    
    def send_text(self, code, text):
        response = text
        self.send_response(code)
        self.send_header("Content-Type", "text/plain")
        self.send_header("Content-Length", len(response))
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        self.wfile.write(response.encode())
    
    def send_html(self, code, html):
        response = html
        self.send_response(code)
        self.send_header("Content-Type", "text/html")
        self.send_header("Content-Length", len(response))
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        self.wfile.write(response.encode())
    
    def do_GET(self):
        requests, inferences = self.read_stats()
        
        if self.path == "/health":
            self.send_json(200, {
                "status": "healthy",
                "model": "grok-bash-1.0",
                "cost": "$0.00",
                "sovereignty": "100%"
            })
        elif self.path == "/status":
            self.send_json(200, {
                "requests": requests,
                "inferences": inferences,
                "port": PORT,
                "timestamp": datetime.now(timezone.utc).isoformat() + "Z"
            })
        elif self.path == "/metrics":
            metrics = f"""grok_requests_total {requests}
grok_inferences_total {inferences}
grok_cost_usd 0.00
grok_sovereignty_percent 100"""
            self.send_text(200, metrics)
        elif self.path == "/":
            html = """<html>
<head><title>Grok Bash Server</title></head>
<body>
<h1>⚡ Grok Bash Server</h1>
<p>Pure bash inference. Zero tokens. Maximum sovereignty.</p>
<h2>API Endpoints</h2>
<ul>
  <li><strong>GET /health</strong> - Health check</li>
  <li><strong>GET /status</strong> - Server metrics</li>
  <li><strong>POST /infer</strong> - Run inference (JSON: {"prompt": "..."})</li>
  <li><strong>GET /metrics</strong> - Prometheus metrics</li>
</ul>
<h2>Cost</h2>
<p><strong>$0.00</strong> — Pure bash, zero tokens, forever free.</p>
</body>
</html>"""
            self.send_html(200, html)
        else:
            self.send_json(404, {"error": "Not found"})
    
    def do_POST(self):
        requests, inferences = self.read_stats()
        
        if self.path == "/infer":
            content_len = int(self.headers.get("Content-Length", 0))
            body = self.rfile.read(content_len).decode()
            
            try:
                data = json.loads(body)
                prompt = data.get("prompt", "").strip()
            except:
                self.send_json(400, {"error": "Invalid JSON"})
                return
            
            if not prompt:
                self.send_json(400, {"error": "Missing prompt field"})
                return
            
            requests += 1
            self.write_stats(requests, inferences)
            
            response_text = self.grok_infer(prompt)
            self.send_json(200, {
                "response": response_text,
                "tokens_used": 0,
                "cost": "$0.00",
                "model": "grok-bash-1.0"
            })
        else:
            self.send_json(404, {"error": "Not found"})
    
    def log_message(self, format, *args):
        """Log to file instead of stdout"""
        log_file = WORKSPACE / "logs" / "access.log"
        msg = f"[{datetime.now(timezone.utc).isoformat()}] {format % args}\n"
        with open(log_file, "a") as f:
            f.write(msg)

def main():
    handler = GrokHandler
    
    with socketserver.TCPServer(("", PORT), handler) as httpd:
        print(f"[{datetime.now(timezone.utc).isoformat()}] Grok starting on port {PORT} (PID {os.getpid()})")
        print(f"Endpoints: /health /status /infer /metrics")
        print(f"Logs: {WORKSPACE / 'logs' / 'access.log'}")
        
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\n[Shutdown]")
            sys.exit(0)

if __name__ == "__main__":
    main()
