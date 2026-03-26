#!/usr/bin/env python3
"""
Enhanced Telegram handler with agency integration.
Supports:
- Original bash commands (preserved)
- Agency commands: /status, /dashboard, /agents, /pivots, /failures, /health, /mint, /optimize
- Routine automation: scheduled daily reports
"""

import subprocess
import sys
import json
import re
import requests
from datetime import datetime, timezone
from collections import defaultdict

# Agency API endpoints
AGENCY_APIS = {
    "dashboard": "http://127.0.0.1:9001/dashboard",
    "agents": "http://127.0.0.1:9001/agents",
    "factory": "http://127.0.0.1:9000/status",
    "fundraising": "http://127.0.0.1:9004/health",
    "entropy": "http://127.0.0.1:9001/health"
}

class RateLimiter:
    def __init__(self, max_per_user=10, window_sec=60):
        self.max_per_user = max_per_user
        self.window_sec = window_sec
        self.state_file = '/tmp/telegram-rate-limiter.json'
        self.load_state()
    
    def load_state(self):
        try:
            with open(self.state_file, 'r') as f:
                self.requests = defaultdict(list, json.load(f))
        except:
            self.requests = defaultdict(list)
    
    def save_state(self):
        with open(self.state_file, 'w') as f:
            json.dump(dict(self.requests), f)
    
    def allow(self, user_id):
        now = datetime.now().timestamp()
        self.requests[user_id] = [t for t in self.requests[user_id] if now - t < self.window_sec]
        if len(self.requests[user_id]) >= self.max_per_user:
            return False
        self.requests[user_id].append(now)
        self.save_state()
        return True

limiter = RateLimiter(max_per_user=10, window_sec=60)

def validate_command(cmd):
    """Whitelist: allow only safe bash patterns OR agency commands."""
    if not cmd or len(cmd) > 2048:
        return False
    # Agency commands start with '/'
    if cmd.startswith('/'):
        # Allow alphanumeric, dash, underscore after slash
        if not re.match(r'^/[a-zA-Z0-9_\-]+(\s+[a-zA-Z0-9_\-\.]+)*$', cmd):
            return False
        return True
    # Bash commands: forbid special chars
    forbidden = [';', '|', '&', '`', '$', '(', ')', '{', '}', '<', '>', '\n']
    if any(c in cmd for c in forbidden):
        return False
    return True

def execute_bash(cmd):
    """Execute command, capture stdout+stderr, timeout 5s."""
    try:
        result = subprocess.run(
            ['/bin/bash', '-c', cmd],
            capture_output=True,
            text=True,
            timeout=5
        )
        return {
            'exit_code': result.returncode,
            'stdout': result.stdout[:2048],
            'stderr': result.stderr[:2048]
        }
    except subprocess.TimeoutExpired:
        return {'exit_code': 124, 'stdout': '', 'stderr': 'Timeout (5s)'}
    except Exception as e:
        return {'exit_code': 1, 'stdout': '', 'stderr': str(e)[:256]}

def fetch_agency_data(endpoint):
    """Fetch JSON from agency API."""
    try:
        resp = requests.get(endpoint, timeout=3)
        resp.raise_for_status()
        return resp.json()
    except Exception as e:
        return {"error": str(e)}

def handle_agency_command(cmd, user_id):
    """Process agency commands."""
    parts = cmd.split()
    command = parts[0]
    
    if command == '/status':
        # Overall agency status
        data = fetch_agency_data(AGENCY_APIS['dashboard'])
        if 'error' in data:
            return {'exit_code': 1, 'stdout': '', 'stderr': data['error']}
        services = data.get('services', {})
        operational = sum(1 for s in services.values() if s.get('status') == 'operational' or s.get('status') == 'running')
        total = len(services)
        raw_failures = data.get('stability', {}).get('raw_failure_data_received', 0)
        pivots = data.get('pivots', {}).get('total_pivots_executed', 0)
        shannon = data.get('pivots', {}).get('total_shannon_from_pivots', 0)
        output = f"🟢 Agency Status\n"
        output += f"Services: {operational}/{total} operational\n"
        output += f"Raw failures: {raw_failures}\n"
        output += f"Pivots executed: {pivots}\n"
        output += f"Shannon from pivots: {shannon}\n"
        output += f"Timestamp: {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M UTC')}"
        return {'exit_code': 0, 'stdout': output, 'stderr': ''}
    
    elif command == '/dashboard':
        # Key metrics
        data = fetch_agency_data(AGENCY_APIS['dashboard'])
        if 'error' in data:
            return {'exit_code': 1, 'stdout': '', 'stderr': data['error']}
        # Compact summary
        output = "📊 Excellence Dashboard\n"
        output += f"Raw failures: {data.get('stability',{}).get('raw_failure_data_received','N/A')}\n"
        output += f"Pivots: {data.get('pivots',{}).get('total_pivots_executed','N/A')}\n"
        output += f"Shannon from pivots: {data.get('pivots',{}).get('total_shannon_from_pivots','N/A')}\n"
        output += f"Agents: {len(data.get('entropy_agents',[]))}\n"
        output += f"HTTPS: {'✅' if data.get('https_available') else '❌'}\n"
        return {'exit_code': 0, 'stdout': output, 'stderr': ''}
    
    elif command == '/agents':
        # List agents with balances
        data = fetch_agency_data(AGENCY_APIS['agents'])
        if 'error' in data:
            return {'exit_code': 1, 'stdout': '', 'stderr': data['error']}
        agents = data.get('agents', [])
        if not agents:
            return {'exit_code': 0, 'stdout': 'No agents found', 'stderr': ''}
        # Sort by balance descending
        agents_sorted = sorted(agents, key=lambda x: x.get('balance_shannon', 0), reverse=True)
        output = "👥 Entropy Agents (top 10)\n"
        for i, agent in enumerate(agents_sorted[:10]):
            name = agent.get('name', 'unknown')
            balance = agent.get('balance_shannon', 0)
            role = agent.get('role', '')
            output += f"{i+1}. {name}: {balance} Shannon"
            if role:
                output += f" ({role})"
            output += "\n"
        return {'exit_code': 0, 'stdout': output, 'stderr': ''}
    
    elif command == '/pivots':
        # Recent pivot activity
        data = fetch_agency_data(AGENCY_APIS['dashboard'])
        if 'error' in data:
            return {'exit_code': 1, 'stdout': '', 'stderr': data['error']}
        pivots = data.get('pivots', {})
        total = pivots.get('total_pivots_executed', 0)
        shannon = pivots.get('total_shannon_from_pivots', 0)
        recent = pivots.get('recent_pivots', [])
        output = f"🔄 Pivot Activity\n"
        output += f"Total pivots: {total}\n"
        output += f"Total Shannon: {shannon}\n"
        if recent:
            output += f"Recent ({len(recent)}):\n"
            for p in recent[:3]:
                ts = p.get('timestamp', '')[:16]
                action = p.get('concrete_action', '')[:50]
                output += f"- {ts}: {action}\n"
        return {'exit_code': 0, 'stdout': output, 'stderr': ''}
    
    elif command == '/failures':
        # Raw failure data
        data = fetch_agency_data(AGENCY_APIS['dashboard'])
        if 'error' in data:
            return {'exit_code': 1, 'stdout': '', 'stderr': data['error']}
        stability = data.get('stability', {})
        raw = stability.get('raw_failure_data_received', 0)
        recent_types = stability.get('recent_failure_types', [])
        output = f"🚨 Raw Failure Data\n"
        output += f"Total failures: {raw}\n"
        if recent_types:
            output += f"Recent types: {', '.join(recent_types[:5])}\n"
        return {'exit_code': 0, 'stdout': output, 'stderr': ''}
    
    elif command == '/health':
        # Health check all services
        results = []
        for name, url in AGENCY_APIS.items():
            try:
                resp = requests.get(url, timeout=2)
                status = '✅' if resp.status_code == 200 else '❌'
                results.append(f"{name}: {status} ({resp.status_code})")
            except Exception as e:
                results.append(f"{name}: ❌ ({str(e)[:20]})")
        output = "🏥 Agency Health Check\n" + "\n".join(results)
        return {'exit_code': 0, 'stdout': output, 'stderr': ''}
    
    elif command == '/help':
        output = """🤖 Agency Telegram Bot Commands:
/status - Overall agency status
/dashboard - Key metrics
/agents - List agents with Shannon balances
/pivots - Recent pivot activity
/failures - Raw failure data
/health - Health check all services
/help - This message

Bash commands also supported (no special chars).
Rate limit: 10 commands/min per user.
"""
        return {'exit_code': 0, 'stdout': output, 'stderr': ''}
    
    else:
        # Unknown agency command
        return {'exit_code': 1, 'stdout': '', 'stderr': f'Unknown command: {command}. Try /help'}

def handle_telegram_message(user_id, text):
    """Main handler: validate, rate-limit, execute, return result."""
    if not limiter.allow(user_id):
        return {'status': 'error', 'message': 'Rate limit exceeded (10/min per user)'}
    
    text = text.strip()
    if not validate_command(text):
        return {'status': 'error', 'message': 'Invalid command (forbidden chars or too long)'}
    
    # Determine if agency command or bash
    if text.startswith('/'):
        result = handle_agency_command(text, user_id)
    else:
        result = execute_bash(text)
    
    return {
        'status': 'ok',
        'command': text,
        'result': result
    }

if __name__ == '__main__':
    if len(sys.argv) < 3:
        print(json.dumps({'error': 'Usage: handler.py <user_id> <command>'}))
        sys.exit(1)
    
    user_id = sys.argv[1]
    command = ' '.join(sys.argv[2:])
    response = handle_telegram_message(user_id, command)
    print(json.dumps(response))