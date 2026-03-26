#!/usr/bin/env python3
"""
Setup Telegram bot token and chat IDs.
"""

import os
import json
import sys

CONFIG_FILE = os.path.join(os.path.dirname(__file__), 'config.json')

def load_config():
    """Load existing config."""
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, 'r') as f:
            return json.load(f)
    return {"token": "", "chat_ids": []}

def save_config(config):
    """Save config."""
    with open(CONFIG_FILE, 'w') as f:
        json.dump(config, f, indent=2)
    print(f"Config saved to {CONFIG_FILE}")

def main():
    print("=== Telegram Bot Setup ===\n")
    
    config = load_config()
    
    # Token
    current_token = config.get('token', '')
    if current_token:
        print(f"Current token: {current_token[:8]}...{current_token[-4:]}")
        change = input("Change token? (y/N): ").strip().lower()
        if change == 'y':
            new_token = input("New bot token: ").strip()
            if new_token:
                config['token'] = new_token
                print("Token updated.")
        else:
            print("Keeping existing token.")
    else:
        token = input("Bot token (from @BotFather): ").strip()
        if token:
            config['token'] = token
        else:
            print("No token provided; bot will not start.")
    
    # Chat IDs
    current_chats = config.get('chat_ids', [])
    if current_chats:
        print(f"\nCurrent chat IDs: {current_chats}")
        action = input("(a)dd, (r)emove, (k)eep? ").strip().lower()
        if action == 'a':
            new_id = input("New chat ID (numeric, can be negative for groups): ").strip()
            if new_id and new_id not in current_chats:
                current_chats.append(new_id)
                config['chat_ids'] = current_chats
                print(f"Added {new_id}")
        elif action == 'r':
            remove_id = input("Chat ID to remove: ").strip()
            if remove_id in current_chats:
                current_chats.remove(remove_id)
                config['chat_ids'] = current_chats
                print(f"Removed {remove_id}")
    else:
        print("\nNo chat IDs configured.")
        add_first = input("Add a chat ID now? (y/N): ").strip().lower()
        if add_first == 'y':
            chat_id = input("Chat ID (numeric, can be negative for groups): ").strip()
            if chat_id:
                config['chat_ids'] = [chat_id]
                print(f"Added {chat_id}")
    
    # Save
    save_config(config)
    
    # Environment variable suggestion
    token = config.get('token', '')
    if token:
        print(f"\nTo run the bot, set environment variable:")
        print(f"export TELEGRAM_BOT_TOKEN='{token}'")
        print(f"Or add to systemd service file.")
    
    # Systemd service
    service_path = "/etc/systemd/system/telegram-bot.service"
    if not os.path.exists(service_path):
        print(f"\nSystemd service not installed. Run:")
        print(f"sudo cp {os.path.dirname(__file__)}/telegram-bot.service /etc/systemd/system/")
        print(f"sudo systemctl daemon-reload")
        print(f"sudo systemctl enable telegram-bot")
        print(f"sudo systemctl start telegram-bot")
    
    print("\nSetup complete.")

if __name__ == '__main__':
    main()