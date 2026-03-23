#!/usr/bin/env python3
"""
Routine agency report sent to configured Telegram chat(s).
Run via cron (e.g., daily at 09:00 UTC).
"""

import os
import json
import logging
import requests
from datetime import datetime, timezone

# Configuration
CONFIG_FILE = os.path.join(os.path.dirname(__file__), 'config.json')
AGENCY_APIS = {
    "dashboard": "http://127.0.0.1:9001/dashboard",
    "entropy": "http://127.0.0.1:9001/agents"
}

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def load_config():
    """Load bot token and chat IDs."""
    if not os.path.exists(CONFIG_FILE):
        logger.warning(f"Config file not found: {CONFIG_FILE}")
        return {"token": "", "chat_ids": []}
    try:
        with open(CONFIG_FILE, 'r') as f:
            return json.load(f)
    except Exception as e:
        logger.error(f"Failed to load config: {e}")
        return {"token": "", "chat_ids": []}

def fetch_agency_data():
    """Fetch current agency metrics."""
    try:
        resp = requests.get(AGENCY_APIS['dashboard'], timeout=5)
        resp.raise_for_status()
        dashboard = resp.json()
        
        resp2 = requests.get(AGENCY_APIS['entropy'], timeout=5)
        agents_data = resp2.json() if resp2.status_code == 200 else {}
        
        return {
            "dashboard": dashboard,
            "agents": agents_data
        }
    except Exception as e:
        logger.error(f"Failed to fetch agency data: {e}")
        return {}

def generate_report(data):
    """Generate formatted report."""
    dashboard = data.get('dashboard', {})
    agents = data.get('agents', {}).get('agents', [])
    
    services = dashboard.get('services', {})
    operational = sum(1 for s in services.values() if s.get('status') in ['operational', 'running'])
    total_services = len(services)
    
    stability = dashboard.get('stability', {})
    raw_failures = stability.get('raw_failure_data_received', 0)
    
    pivots = dashboard.get('pivots', {})
    total_pivots = pivots.get('total_pivots_executed', 0)
    shannon_from_pivots = pivots.get('total_shannon_from_pivots', 0)
    
    # Count agents
    agent_count = len(agents)
    # Sum Shannon across all agents
    total_shannon = sum(a.get('balance_shannon', 0) for a in agents)
    
    timestamp = datetime.now(timezone.utc).strftime('%Y‑%m‑d %H:%M UTC')
    
    report = f"📊 *Daily Agency Report* ({timestamp})\n\n"
    report += f"*Infrastructure*\n"
    report += f"• Services: {operational}/{total_services} operational\n"
    report += f"• Raw failures tracked: {raw_failures}\n"
    report += f"• Pivots executed: {total_pivots}\n"
    report += f"• Shannon from pivots: {shannon_from_pivots}\n\n"
    
    report += f"*Economy*\n"
    report += f"• Agents: {agent_count}\n"
    report += f"• Total Shannon minted: {total_shannon}\n"
    
    # Top 3 agents by balance
    if agents:
        top = sorted(agents, key=lambda x: x.get('balance_shannon', 0), reverse=True)[:3]
        report += f"• Top agents:\n"
        for i, agent in enumerate(top, 1):
            name = agent.get('name', 'unknown')
            balance = agent.get('balance_shannon', 0)
            report += f"  {i}. {name}: {balance} Shannon\n"
    
    report += f"\n*Security*\n"
    https = '✅' if dashboard.get('https_available') else '❌'
    report += f"• HTTPS: {https}\n"
    report += f"• Mutation detector: {services.get('mutation_detector',{}).get('status','unknown')}\n"
    
    report += f"\n*Next Actions*\n"
    if raw_failures > 50:
        report += f"• High raw failures ({raw_failures}) – copier agent active\n"
    if not dashboard.get('https_available'):
        report += f"• HTTPS missing – consider Let's Encrypt\n"
    
    return report

def send_telegram_message(token, chat_id, text):
    """Send message via Telegram Bot API."""
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    payload = {
        "chat_id": chat_id,
        "text": text,
        "parse_mode": "Markdown",
        "disable_web_page_preview": True
    }
    try:
        resp = requests.post(url, json=payload, timeout=10)
        resp.raise_for_status()
        logger.info(f"Message sent to chat {chat_id}")
        return True
    except Exception as e:
        logger.error(f"Failed to send to chat {chat_id}: {e}")
        return False

def main():
    """Main routine."""
    logger.info("Starting routine agency report")
    
    # Load config
    config = load_config()
    token = config.get('token', '')
    chat_ids = config.get('chat_ids', [])
    
    if not token or not chat_ids:
        logger.warning("Token or chat IDs missing; skipping Telegram send")
        # Still generate report for logging
        chat_ids = []
    
    # Fetch data
    data = fetch_agency_data()
    if not data:
        logger.error("No agency data fetched")
        return
    
    # Generate report
    report = generate_report(data)
    
    # Send to each chat
    successes = 0
    for chat_id in chat_ids:
        if send_telegram_message(token, chat_id, report):
            successes += 1
    
    # Log locally
    log_file = os.path.join(os.path.dirname(__file__), 'routine_reports.log')
    with open(log_file, 'a') as f:
        timestamp = datetime.now(timezone.utc).isoformat()
        f.write(f"\n=== {timestamp} ===\n")
        f.write(report + '\n')
    
    logger.info(f"Routine report completed: sent to {successes}/{len(chat_ids)} chats")

if __name__ == '__main__':
    main()