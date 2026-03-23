#!/usr/bin/env python3
import os
import json
import logging
from handler import handle_telegram_message
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

TOKEN = os.getenv('TELEGRAM_BOT_TOKEN', '')

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Receive message, execute, reply with result."""
    user_id = str(update.effective_user.id)
    text = update.message.text
    
    response = handle_telegram_message(user_id, text)
    
    if response['status'] == 'error':
        await update.message.reply_text(f"❌ {response['message']}")
        return
    
    result = response['result']
    exit_code = result['exit_code']
    stdout = result['stdout']
    stderr = result['stderr']
    
    # Format output based on command type
    if text.startswith('/'):
        # Agency command: output as plain text with possible markdown
        if exit_code == 0:
            await update.message.reply_text(stdout, parse_mode='Markdown')
        else:
            await update.message.reply_text(f"❌ {stderr}")
    else:
        # Bash command: preserve original format
        output = f"Exit: {exit_code}\n"
        if stdout:
            output += f"OUT:\n{stdout}\n"
        if stderr:
            output += f"ERR:\n{stderr}"
        await update.message.reply_text(f"```\n{output}\n```", parse_mode='Markdown')

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Send welcome message."""
    await update.message.reply_text(
        "🤖 Agency Telegram Bridge Ready\n"
        "Supports bash commands and agency integration.\n"
        "Use /help for available commands.\n"
        "Rate limit: 10 commands/min per user."
    )

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Send help message."""
    await update.message.reply_text(
        "🤖 Agency Telegram Bot Commands:\n"
        "/status - Overall agency status\n"
        "/dashboard - Key metrics\n"
        "/agents - List agents with Shannon balances\n"
        "/pivots - Recent pivot activity\n"
        "/failures - Raw failure data\n"
        "/health - Health check all services\n"
        "/help - This message\n\n"
        "Bash commands also supported (no special chars).\n"
        "Rate limit: 10 commands/min per user.",
        parse_mode='Markdown'
    )

def main():
    if not TOKEN:
        print("ERROR: TELEGRAM_BOT_TOKEN not set")
        return
    
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    
    logger.info("Polling for messages...")
    app.run_polling()

if __name__ == '__main__':
    main()
