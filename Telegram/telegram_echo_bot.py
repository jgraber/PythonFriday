"""Minimal Telegram bot that answers every text message with "you said: <message>".

Requirements:
    - uv add python-telegram-bot python-dotenv
    - a bot token from @BotFather in the .env file next to this script:

        TELEGRAM_BOT_TOKEN=123456:ABC-your-token

Run it with:
    uv run telegram_echo_bot.py

Stop it with Ctrl+C.
"""

import os
import sys

from dotenv import load_dotenv
from telegram import Update
from telegram.ext import Application, ContextTypes, MessageHandler, filters

sys.stdout.reconfigure(encoding="utf-8")

load_dotenv()


async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    text = update.message.text
    print(f"[echo] {update.effective_user.first_name}: {text}")
    await update.message.reply_text(f"you said: {text}")


def main() -> None:
    app = Application.builder().token(os.environ["TELEGRAM_BOT_TOKEN"]).build()
    app.add_handler(MessageHandler(filters.TEXT, echo))

    print("--- BOT RUNNING (Ctrl+C to stop) ---")
    app.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
