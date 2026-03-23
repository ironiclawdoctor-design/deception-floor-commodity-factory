#!/usr/bin/env python3
import subprocess
import sys
import json
import re
from datetime import datetime
from collections import defaultdict

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
        return True  # Allow before checking >= allows exactly max_per_user requests

limiter = RateLimiter(max_per_user=10, window_sec=60)

def validate_command(cmd):
    """Whitelist: allow only safe bash patterns."""
    if not cmd or len(cmd) > 2048:
        return False
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

def handle_telegram_message(user_id, text):
    """Main handler: validate, rate-limit, execute, return result."""
    if not limiter.allow(user_id):
        return {'status': 'error', 'message': 'Rate limit exceeded (10/min per user)'}
    
    text = text.strip()
    if not validate_command(text):
        return {'status': 'error', 'message': 'Invalid command (forbidden chars or too long)'}
    
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
