"""Telegram echo bot that only answers an allowlist of users; everyone else is turned away.

Requirements:
    - uv add python-telegram-bot python-dotenv
    - a bot token from @BotFather and the allowed Telegram user IDs (comma-separated)
      in the .env file next to this script:

        TELEGRAM_BOT_TOKEN=123456:ABC-your-token
        TELEGRAM_ALLOWED_USERS=11111111,22222222

    User IDs are used instead of usernames because usernames are optional and can
    be changed. To find your ID, run the bot, message it, and copy the number from
    the [reject] line in the console.

Run it with:
    uv run telegram_allowlist_bot.py

Stop it with Ctrl+C.
"""

import os
import sys

from dotenv import load_dotenv
from telegram import Update
from telegram.ext import Application, ContextTypes, MessageHandler, filters

sys.stdout.reconfigure(encoding="utf-8")

load_dotenv()


def load_allowed_users() -> set[int]:
    """Parse TELEGRAM_ALLOWED_USERS, e.g. "123456789,987654321"."""
    raw = os.environ.get("TELEGRAM_ALLOWED_USERS", "")
    users = set()
    for part in raw.split(","):
        part = part.strip()
        if not part:
            continue
        if not part.isdigit():
            sys.exit(f"TELEGRAM_ALLOWED_USERS contains a non-numeric id: {part!r}")
        users.add(int(part))
    return users


async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    text = update.message.text
    print(f"[echo] {update.effective_user.first_name}: {text}")
    await update.message.reply_text(f"you said: {text}")


async def reject(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user = update.effective_user
    print(f"[reject] {user.first_name} ({user.id}) is not on the allowlist")
    await update.message.reply_text("Sorry, this bot is currently not available")


def main() -> None:
    allowed_users = load_allowed_users()
    if not allowed_users:
        sys.exit("TELEGRAM_ALLOWED_USERS is empty - nobody could use the bot")

    allowed = filters.User(user_id=allowed_users)
    # UpdateType.MESSAGE keeps edited messages / channel posts out, where update.message is None
    new_message = filters.UpdateType.MESSAGE

    app = Application.builder().token(os.environ["TELEGRAM_BOT_TOKEN"]).build()
    app.add_handler(MessageHandler(allowed & new_message & filters.TEXT, echo))
    app.add_handler(MessageHandler(~allowed & new_message, reject))

    print(f"--- ALLOWED USERS: {sorted(allowed_users)} ---")
    print("--- BOT RUNNING (Ctrl+C to stop) ---")
    app.run_polling()


if __name__ == "__main__":
    main()