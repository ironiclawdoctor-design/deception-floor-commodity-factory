#!/usr/bin/env python3
import os
import json
import logging
from handler import handle_telegram_message
from telegram import Update
from telegram.ext import Application, MessageHandler, filters, ContextTypes

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
    
    output = f"Exit: {exit_code}\n"
    if stdout:
        output += f"OUT:\n{stdout}\n"
    if stderr:
        output += f"ERR:\n{stderr}"
    
    await update.message.reply_text(f"```\n{output}\n```", parse_mode='Markdown')

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Send welcome message."""
    await update.message.reply_text(
        "Bash Bridge ready. Send commands (no pipes, no redirects, no special chars).\n"
        "Rate limit: 10 commands/min per user."
    )

def main():
    if not TOKEN:
        print("ERROR: TELEGRAM_BOT_TOKEN not set")
        return
    
    app = Application.builder().token(TOKEN).build()
    app.add_handler(filters.COMMAND)
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    
    logger.info("Polling for messages...")
    app.run_polling()

if __name__ == '__main__':
    main()
