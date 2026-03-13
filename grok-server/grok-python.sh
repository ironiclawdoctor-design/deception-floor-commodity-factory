#!/bin/bash

# Grok with Python HTTP Server + Bash Handler
# Uses Python's built-in http.server (always available)

PORT="${1:-8888}"
WORKSPACE="/root/.openclaw/workspace/grok-server"
HANDLER="$WORKSPACE/handler.sh"

# Create a Python wrapper that calls handler.sh
cat > "$WORKSPACE/server.py" <<'PYTHON_CODE'
#!/usr/bin/env python3
import http.server
import socketserver
import subprocess
import sys
import os
import json

PORT = int(sys.argv[1]) if len(sys.argv) > 1 else 8888
HANDLER = os.environ.get('HANDLER_SCRIPT', 'handler.sh')

class GrokHTTPHandler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        self.handle_request('GET', None)
    
    def do_POST(self):
        content_length = int(self.headers.get('Content-Length', 0))
        body = self.rfile.read(content_length).decode('utf-8')
        self.handle_request('POST', body)
    
    def handle_request(self, method, body):
        # Build HTTP request string for handler
        request = f"{method} {self.path} HTTP/1.1\r\n"
        
        for header, value in self.headers.items():
            request += f"{header}: {value}\r\n"
        
        request += "\r\n"
        if body:
            request += body
        
        # Call handler script
        try:
            proc = subprocess.Popen(
                ['bash', HANDLER],
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            stdout, stderr = proc.communicate(input=request, timeout=5)
            
            # Parse response (simple: find blank line separator)
            parts = stdout.split('\n\n', 1)
            response_headers = parts[0]
            response_body = parts[1] if len(parts) > 1 else ''
            
            # Send response
            self.wfile.write(response_body.encode('utf-8') if response_body else b'')
        
        except subprocess.TimeoutExpired:
            self.send_error(504, "Handler timeout")
        except Exception as e:
            self.send_error(500, f"Handler error: {str(e)}")
    
    def log_message(self, format, *args):
        # Suppress default logging, or log to file
        pass

if __name__ == '__main__':
    try:
        with socketserver.TCPServer(("", PORT), GrokHTTPHandler) as httpd:
            print(f"[{__import__('datetime').datetime.now().isoformat()}] Grok server starting on port {PORT}")
            httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nShutdown")
        sys.exit(0)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
PYTHON_CODE

# Make Python script executable
chmod +x "$WORKSPACE/server.py"

# Start server
export HANDLER_SCRIPT="$HANDLER"
exec python3 "$WORKSPACE/server.py" "$PORT"
