#!/usr/bin/env python3
"""Local Dollar Dashboard server — no GCP needed."""
import http.server, socketserver, os

PORT = 8888
DIR = os.path.dirname(os.path.abspath(__file__))

class Handler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *a, **kw):
        super().__init__(*a, directory=DIR, **kw)
    def log_message(self, fmt, *args):
        pass  # Silent

print(f"💰 Dollar Dashboard running at http://localhost:{PORT}")
print(f"   Open in browser to view live dashboard")
print(f"   Press Ctrl+C to stop")

with socketserver.TCPServer(("", PORT), Handler) as httpd:
    httpd.serve_forever()
