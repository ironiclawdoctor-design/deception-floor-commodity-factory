#!/usr/bin/env python3
import json
import subprocess
import time
import os
import sys
import sqlite3
from pathlib import Path

def get_cron_status():
    """Get cron jobs status via openclaw API"""
    try:
        # Use curl to local gateway API
        import requests
        response = requests.get('http://localhost:9000/api/cron/list', timeout=5)
        if response.status_code == 200:
            return response.json().get('jobs', [])
    except:
        pass
    # Fallback: empty list
    return []

def get_git_status():
    """Get git uncommitted files count"""
    try:
        result = subprocess.run(['git', 'status', '--porcelain'], 
                              capture_output=True, text=True, cwd='/root/.openclaw/workspace')
        files = result.stdout.strip().split('\n')
        files = [f for f in files if f]
        branch_result = subprocess.run(['git', 'branch', '--show-current'], 
                                      capture_output=True, text=True, cwd='/root/.openclaw/workspace')
        branch = branch_result.stdout.strip() or 'unknown'
        return {
            'uncommittedFiles': len(files),
            'branch': branch
        }
    except:
        return {'uncommittedFiles': 0, 'branch': 'unknown'}

def check_service(port):
    """Check if service is healthy"""
    try:
        import requests
        response = requests.get(f'http://127.0.0.1:{port}/health', timeout=2)
        return 'healthy' if response.status_code == 200 else 'down'
    except:
        return 'down'

def get_entropy_agents():
    """Get entropy agents from port 9001"""
    try:
        import requests
        response = requests.get('http://127.0.0.1:9001/agents', timeout=2)
        if response.status_code == 200:
            return response.json().get('agents', [])
    except:
        pass
    return []

def get_factory_status():
    """Get factory status"""
    try:
        import requests
        response = requests.get('http://127.0.0.1:9000/health', timeout=2)
        if response.status_code == 200:
            return response.json()
    except:
        pass
    return {'status': 'unknown'}

def get_next_steps():
    """Extract next steps from fundraising docs"""
    steps = []
    try:
        path = '/root/.openclaw/workspace/fundraising/SUSTAINABLE_MODEL_SUMMARY.md'
        with open(path, 'r') as f:
            content = f.read()
            # Look for markdown list items
            import re
            for line in content.split('\n'):
                if line.strip().startswith('- [ ]'):
                    steps.append({'task': line.strip()[5:].strip()})
                if len(steps) >= 5:
                    break
    except:
        pass
    return steps

def get_stalled_items():
    """Identify stalled items"""
    stalled = []
    # Check for recent 402 errors in logs
    log_path = '/tmp/openclaw/openclaw-2026-03-19.log'
    if os.path.exists(log_path):
        with open(log_path, 'r') as f:
            content = f.read()
            if '402 Your Ampere credits' in content:
                stalled.append({'issue': 'Ampere credits exhausted', 'severity': 'critical'})
    
    # Check cron jobs for errors
    cron_jobs = get_cron_status()
    for job in cron_jobs:
        if job.get('lastRunStatus') == 'error':
            stalled.append({'issue': f'Cron job failed: {job.get("name")}', 'severity': 'warning'})
            break
    
    return stalled

def main():
    data = {
        'cron': get_cron_status(),
        'git': get_git_status(),
        'processes': [
            {'service': 'factory', 'port': 9000, 'status': check_service(9000)},
            {'service': 'entropy-economy', 'port': 9001, 'status': check_service(9001)},
            {'service': 'payment-backend', 'port': 9003, 'status': check_service(9003)},
            {'service': 'landing-page', 'port': 8080, 'status': check_service(8080)}
        ],
        'entropyAgents': get_entropy_agents(),
        'factory': get_factory_status(),
        'nextSteps': get_next_steps(),
        'stalled': get_stalled_items(),
        'timestamp': time.time()
    }
    
    output_file = '/tmp/mission-control-data.json'
    with open(output_file, 'w') as f:
        json.dump(data, f, indent=2)
    
    print(f"Data written to {output_file}")

if __name__ == '__main__':
    main()