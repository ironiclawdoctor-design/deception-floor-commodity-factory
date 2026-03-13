#!/usr/bin/env python3
"""
Fiesta Web Server - Simple, honest, auditable via Tailscale
Token cost: $0.00 (all local bash/python)
Doctrine: Tier 0-2 only
"""

import http.server
import socketserver
import json
import os
from datetime import datetime
from pathlib import Path

PORT = 8000
WORKSPACE = Path("/root/.openclaw/workspace/web-server")
LOGS_DIR = WORKSPACE / "logs"
CHATS_DIR = WORKSPACE / "chats"

# Create directories
LOGS_DIR.mkdir(exist_ok=True)
CHATS_DIR.mkdir(exist_ok=True)

class ChatHandler(http.server.BaseHTTPRequestHandler):
    
    def log_access(self, method, path, status):
        log_file = LOGS_DIR / "access.log"
        timestamp = datetime.utcnow().isoformat()
        msg = f"[{timestamp}] {method} {path} {status}\n"
        with open(log_file, "a") as f:
            f.write(msg)
    
    def do_GET(self):
        """Handle GET requests"""
        
        if self.path == "/":
            self.serve_portal()
        elif self.path == "/health":
            self.serve_health()
        elif self.path == "/chats":
            self.serve_chat_list()
        else:
            self.serve_404()
    
    def do_POST(self):
        """Handle POST requests"""
        
        if self.path == "/chats":
            self.create_chat()
        elif self.path.startswith("/chats/"):
            chat_id = self.path.split("/")[2]
            self.add_message(chat_id)
        else:
            self.serve_404()
    
    def serve_portal(self):
        """Portal page: "Watch me try" """
        
        html = """<!DOCTYPE html>
<html>
<head>
    <title>Fiesta — Watch me try</title>
    <style>
        body { font-family: monospace; margin: 40px; background: #0a0a0a; color: #00ff00; }
        h1 { color: #ffff00; }
        .container { max-width: 800px; margin: 0 auto; }
        button { background: #004400; color: #00ff00; padding: 10px 20px; border: 1px solid #00ff00; cursor: pointer; }
        button:hover { background: #006600; }
        #chat-box { height: 300px; overflow-y: auto; border: 1px solid #00ff00; padding: 10px; margin: 20px 0; background: #000000; }
        .message { margin: 5px 0; padding: 5px; border-left: 2px solid #00ff00; }
        input { width: 100%; padding: 10px; background: #001100; color: #00ff00; border: 1px solid #00ff00; }
    </style>
</head>
<body>
    <div class="container">
        <h1>⚡ Fiesta Web Server</h1>
        <p><strong>Portal:</strong> Watch me try</p>
        <p><strong>Status:</strong> <span id="status">Connecting...</span></p>
        <p><strong>Cost:</strong> $0.00 (Tier 0-2 only)</p>
        <p><strong>Access:</strong> Audit via Tailscale (100.76.206.82:8000)</p>
        
        <h2>Chat Interface</h2>
        <button onclick="createChat()">Start New Chat</button>
        <button onclick="loadChats()">Load Chats</button>
        
        <div id="chat-box"></div>
        
        <input type="text" id="message-input" placeholder="Type message..." onkeypress="handleKeyPress(event)">
        <button onclick="sendMessage()">Send</button>
        
        <div id="output"></div>
    </div>
    
    <script>
        let currentChatId = null;
        
        async function checkHealth() {
            try {
                const resp = await fetch('/health');
                const data = await resp.json();
                document.getElementById('status').innerText = 'Healthy: ' + data.status;
            } catch (e) {
                document.getElementById('status').innerText = 'Error: ' + e.message;
            }
        }
        
        async function createChat() {
            try {
                const resp = await fetch('/chats', { method: 'POST' });
                const data = await resp.json();
                currentChatId = data.id;
                document.getElementById('chat-box').innerHTML = '<div class="message">Chat created: ' + data.id + '</div>';
                loadChats();
            } catch (e) {
                alert('Error: ' + e.message);
            }
        }
        
        async function loadChats() {
            try {
                const resp = await fetch('/chats');
                const data = await resp.json();
                let html = '<div class="message">Chats: ' + data.count + '</div>';
                data.chats.forEach(chat => {
                    html += '<div class="message" onclick="loadChat(\'' + chat + '\')">📝 ' + chat + '</div>';
                });
                document.getElementById('chat-box').innerHTML = html;
            } catch (e) {
                alert('Error: ' + e.message);
            }
        }
        
        async function loadChat(chatId) {
            currentChatId = chatId;
            try {
                const resp = await fetch('/chats');
                const data = await resp.json();
                const chat = data.chats.find(c => c.id === chatId);
                if (chat && chat.messages) {
                    let html = '';
                    chat.messages.forEach(msg => {
                        html += '<div class="message">[' + msg.timestamp + '] ' + msg.sender + ': ' + msg.text + '</div>';
                    });
                    document.getElementById('chat-box').innerHTML = html;
                }
            } catch (e) {
                alert('Error: ' + e.message);
            }
        }
        
        async function sendMessage() {
            if (!currentChatId) {
                alert('Create a chat first');
                return;
            }
            
            const msg = document.getElementById('message-input').value;
            if (!msg.trim()) return;
            
            try {
                const resp = await fetch('/chats/' + currentChatId, {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ text: msg })
                });
                const data = await resp.json();
                document.getElementById('message-input').value = '';
                loadChat(currentChatId);
            } catch (e) {
                alert('Error: ' + e.message);
            }
        }
        
        function handleKeyPress(event) {
            if (event.key === 'Enter') {
                sendMessage();
            }
        }
        
        // Initial load
        checkHealth();
        loadChats();
    </script>
</body>
</html>"""
        
        self.send_response(200)
        self.send_header("Content-Type", "text/html")
        self.send_header("Content-Length", len(html))
        self.end_headers()
        self.wfile.write(html.encode())
        self.log_access("GET", "/", 200)
    
    def serve_health(self):
        """Health endpoint"""
        resp = json.dumps({
            "status": "healthy",
            "timestamp": datetime.utcnow().isoformat(),
            "cost": "$0.00",
            "doctrine": "Tier 0-2 only"
        })
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", len(resp))
        self.end_headers()
        self.wfile.write(resp.encode())
        self.log_access("GET", "/health", 200)
    
    def serve_chat_list(self):
        """List all chats"""
        chats = []
        for chat_file in CHATS_DIR.glob("*.json"):
            try:
                with open(chat_file) as f:
                    chat = json.load(f)
                chats.append({
                    "id": chat["id"],
                    "created": chat["created"],
                    "messages": chat.get("messages", [])
                })
            except:
                pass
        
        resp = json.dumps({
            "count": len(chats),
            "chats": chats
        })
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", len(resp))
        self.end_headers()
        self.wfile.write(resp.encode())
        self.log_access("GET", "/chats", 200)
    
    def create_chat(self):
        """Create new chat"""
        chat_id = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
        chat = {
            "id": chat_id,
            "created": datetime.utcnow().isoformat(),
            "messages": []
        }
        
        chat_file = CHATS_DIR / f"{chat_id}.json"
        with open(chat_file, "w") as f:
            json.dump(chat, f)
        
        resp = json.dumps({"id": chat_id, "created": chat["created"]})
        self.send_response(201)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", len(resp))
        self.end_headers()
        self.wfile.write(resp.encode())
        self.log_access("POST", "/chats", 201)
    
    def add_message(self, chat_id):
        """Add message to chat"""
        content_len = int(self.headers.get("Content-Length", 0))
        body = self.rfile.read(content_len).decode()
        
        try:
            msg_data = json.loads(body)
            text = msg_data.get("text", "")
        except:
            text = ""
        
        chat_file = CHATS_DIR / f"{chat_id}.json"
        if chat_file.exists():
            with open(chat_file) as f:
                chat = json.load(f)
            
            chat["messages"].append({
                "timestamp": datetime.utcnow().isoformat(),
                "sender": "user",
                "text": text
            })
            
            with open(chat_file, "w") as f:
                json.dump(chat, f)
            
            resp = json.dumps({"added": True, "message_count": len(chat["messages"])})
            self.send_response(200)
        else:
            resp = json.dumps({"error": "Chat not found"})
            self.send_response(404)
        
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", len(resp))
        self.end_headers()
        self.wfile.write(resp.encode())
        self.log_access("POST", f"/chats/{chat_id}", 200 if chat_file.exists() else 404)
    
    def serve_404(self):
        """404 response"""
        resp = json.dumps({"error": "Not found"})
        self.send_response(404)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", len(resp))
        self.end_headers()
        self.wfile.write(resp.encode())
        self.log_access("GET", self.path, 404)
    
    def log_message(self, *args, **kwargs):
        """Suppress default logging"""
        pass

def run():
    handler = ChatHandler
    with socketserver.TCPServer(("", PORT), handler) as httpd:
        print(f"Fiesta Web Server starting on port {PORT}")
        print(f"Access: http://127.0.0.1:{PORT}")
        print(f"Tailscale: http://100.76.206.82:{PORT}")
        print(f"Status: Watch me try")
        print(f"Cost: $0.00 (Tier 0-2 only)")
        httpd.serve_forever()

if __name__ == "__main__":
    run()
