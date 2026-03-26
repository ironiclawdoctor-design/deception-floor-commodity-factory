#!/usr/bin/env python3
"""
Simple HTTP server for Google Cloud login page.
Serves the HTML interface and can handle OAuth callbacks.
"""

import os
import json
import logging
from datetime import datetime
from pathlib import Path
from http.server import HTTPServer, BaseHTTPRequestHandler
import urllib.parse
import socketserver

# Configuration
PORT = 8080
WORKSPACE_ROOT = Path("/root/.openclaw/workspace")
SECRETS_DIR = WORKSPACE_ROOT / "secrets"
HTML_DIR = Path(__file__).parent
INDEX_HTML = HTML_DIR / "index.html"
COOKIE_LOG = SECRETS_DIR / "google-auth-log.jsonl"

# Ensure directories exist
SECRETS_DIR.mkdir(parents=True, exist_ok=True)

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class GoogleCloudLoginHandler(BaseHTTPRequestHandler):
    """HTTP handler for login page and OAuth callbacks."""
    
    def log_message(self, format, *args):
        logger.info("%s - %s", self.address_string(), format % args)
    
    def do_GET(self):
        """Handle GET requests."""
        parsed = urllib.parse.urlparse(self.path)
        path = parsed.path
        
        if path == "/" or path == "/index.html":
            self.serve_index()
        elif path == "/health":
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps({
                "status": "ok",
                "service": "google-cloud-login",
                "timestamp": datetime.utcnow().isoformat()
            }).encode())
        elif path.startswith("/oauth/callback"):
            self.handle_oauth_callback(parsed.query)
        else:
            self.send_error(404, "File not found")
    
    def do_POST(self):
        """Handle POST requests (cookie uploads)."""
        parsed = urllib.parse.urlparse(self.path)
        path = parsed.path
        
        if path == "/upload-cookies":
            self.handle_cookie_upload()
        elif path == "/upload-service-account":
            self.handle_service_account_upload()
        else:
            self.send_error(404, "Endpoint not found")
    
    def serve_index(self):
        """Serve the main HTML page."""
        try:
            with open(INDEX_HTML, "rb") as f:
                content = f.read()
            
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.send_header("Content-Length", str(len(content)))
            self.end_headers()
            self.wfile.write(content)
            
        except FileNotFoundError:
            self.send_error(404, "index.html not found")
        except Exception as e:
            logger.error("Error serving index: %s", e)
            self.send_error(500, str(e))
    
    def handle_oauth_callback(self, query_string):
        """Handle OAuth 2.0 callback from Google."""
        params = urllib.parse.parse_qs(query_string)
        
        # Log the callback (in real implementation, exchange code for tokens)
        auth_data = {
            "timestamp": datetime.utcnow().isoformat(),
            "params": params,
            "source": "oauth_callback"
        }
        
        self.log_auth_event("oauth_callback", auth_data)
        
        # Simple success page
        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.end_headers()
        
        success_html = """
        <!DOCTYPE html>
        <html>
        <head><title>OAuth Success</title></head>
        <body style="font-family: sans-serif; padding: 40px; text-align: center;">
            <h1 style="color: #0f9d58;">✅ OAuth Callback Received</h1>
            <p>Authentication data has been logged.</p>
            <p>Check <code>/root/.openclaw/workspace/secrets/google-auth-log.jsonl</code></p>
            <p><a href="/">← Back to login page</a></p>
        </body>
        </html>
        """
        self.wfile.write(success_html.encode())
    
    def handle_cookie_upload(self):
        """Handle uploaded cookie JSON file."""
        try:
            content_length = int(self.headers.get('Content-Length', 0))
            if content_length == 0:
                self.send_error(400, "No content")
                return
            
            post_data = self.rfile.read(content_length)
            cookies = json.loads(post_data)
            
            # Validate basic structure
            if not isinstance(cookies, list):
                raise ValueError("Cookies should be a list")
            
            # Save to secrets
            cookie_file = SECRETS_DIR / "google-cookies.json"
            with open(cookie_file, "w") as f:
                json.dump(cookies, f, indent=2)
            
            self.log_auth_event("cookie_upload", {
                "count": len(cookies),
                "file": str(cookie_file),
                "domains": list(set(c.get("domain", "") for c in cookies))
            })
            
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps({
                "success": True,
                "message": f"Saved {len(cookies)} cookies",
                "path": str(cookie_file)
            }).encode())
            
        except json.JSONDecodeError as e:
            self.send_error(400, f"Invalid JSON: {e}")
        except Exception as e:
            logger.error("Cookie upload error: %s", e)
            self.send_error(500, str(e))
    
    def handle_service_account_upload(self):
        """Handle uploaded service account JSON key."""
        try:
            content_length = int(self.headers.get('Content-Length', 0))
            if content_length == 0:
                self.send_error(400, "No content")
                return
            
            post_data = self.rfile.read(content_length)
            sa_key = json.loads(post_data)
            
            # Validate service account key structure
            required_fields = ["type", "project_id", "private_key_id", "private_key", "client_email"]
            for field in required_fields:
                if field not in sa_key:
                    raise ValueError(f"Missing required field: {field}")
            
            # Save to secrets
            sa_file = SECRETS_DIR / "gcp-service-account.json"
            with open(sa_file, "w") as f:
                json.dump(sa_key, f, indent=2)
            
            self.log_auth_event("service_account_upload", {
                "project_id": sa_key.get("project_id"),
                "client_email": sa_key.get("client_email"),
                "file": str(sa_file)
            })
            
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps({
                "success": True,
                "message": "Service account key saved",
                "path": str(sa_file),
                "project": sa_key.get("project_id")
            }).encode())
            
        except json.JSONDecodeError as e:
            self.send_error(400, f"Invalid JSON: {e}")
        except Exception as e:
            logger.error("Service account upload error: %s", e)
            self.send_error(500, str(e))
    
    def log_auth_event(self, event_type, data):
        """Log authentication events to JSONL file."""
        event = {
            "timestamp": datetime.utcnow().isoformat(),
            "event": event_type,
            "data": data
        }
        
        with open(COOKIE_LOG, "a") as f:
            f.write(json.dumps(event) + "\n")
        
        logger.info("Auth event: %s", event_type)

def main():
    """Start the HTTP server."""
    server_address = ("", PORT)
    httpd = HTTPServer(server_address, GoogleCloudLoginHandler)
    
    logger.info("Starting Google Cloud login server on port %d", PORT)
    logger.info("Access at: http://localhost:%d", PORT)
    logger.info("HTML directory: %s", HTML_DIR)
    logger.info("Secrets directory: %s", SECRETS_DIR)
    
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        logger.info("Server stopped by user")
    except Exception as e:
        logger.error("Server error: %s", e)

if __name__ == "__main__":
    main()