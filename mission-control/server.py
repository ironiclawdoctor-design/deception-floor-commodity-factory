#!/usr/bin/env python3
import http.server
import json
import subprocess
import time
import os
import threading
from pathlib import Path

PORT = 9005
DATA_FILE = "/tmp/mission-control-data.json"
GATHER_SCRIPT = "/root/.openclaw/workspace/mission-control/gather-data.py"

class MissionControlHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/data.json':
            self.serve_data_json()
        else:
            # Serve static files from current directory
            super().do_GET()
    
    def serve_data_json(self):
        # Run gather script to update data
        try:
            subprocess.run([GATHER_SCRIPT], check=True, capture_output=True, timeout=10)
        except Exception as e:
            print(f"Warning: gather script failed: {e}")
        
        # Read the JSON file
        try:
            with open(DATA_FILE, 'r') as f:
                data = f.read()
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.send_header('Cache-Control', 'no-cache')
            self.end_headers()
            self.wfile.write(data.encode())
        except Exception as e:
            self.send_response(500)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({'error': str(e)}).encode())
    
    def log_message(self, format, *args):
        # Suppress default log messages
        pass

def main():
    os.chdir(Path(__file__).parent)  # Serve from mission-control directory
    
    # Ensure gather script is executable
    os.chmod(GATHER_SCRIPT, 0o755)
    
    # Generate initial data
    subprocess.run([GATHER_SCRIPT], capture_output=True)
    
    server_address = ('', PORT)
    httpd = http.server.HTTPServer(server_address, MissionControlHandler)
    
    print(f"🎛️ Mission Control dashboard running on http://localhost:{PORT}")
    print(f"   (Accessible via Tailscale at your Tailscale IP:{PORT})")
    print("   Press Ctrl+C to stop")
    
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nShutting down Mission Control server")

if __name__ == '__main__':
    main()