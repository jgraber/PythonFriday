import os
import sys
from datetime import datetime, timedelta

from dotenv import load_dotenv
from telegram import BotCommand, Update
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters

sys.stdout.reconfigure(encoding="utf-8")

load_dotenv()

COMMANDS = [
    BotCommand("time", "current time"),
    BotCommand("date", "today's date"),
    BotCommand("week", "ISO week number"),
    BotCommand("doy", "day of the year"),
    BotCommand("in", "date in N days, e.g. /in 10"),
    BotCommand("help", "list all commands"),
]


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


def log(update: Update) -> None:
    print(f"[{update.message.text}] {update.effective_user.first_name}")


# --- command handlers -------------------------------------------------------

async def cmd_time(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    log(update)
    now = datetime.now().astimezone()
    await update.message.reply_text(now.strftime("%H:%M:%S (%Z)"))


async def cmd_date(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    log(update)
    today = datetime.now()
    await update.message.reply_text(today.strftime("%A, %d %B %Y"))


async def cmd_week(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    log(update)
    iso = datetime.now().isocalendar()
    await update.message.reply_text(f"ISO week {iso.week} of {iso.year} (weekday {iso.weekday})")


async def cmd_doy(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    log(update)
    today = datetime.now()
    days_in_year = 366 if today.year % 4 == 0 and (today.year % 100 != 0 or today.year % 400 == 0) else 365
    doy = today.timetuple().tm_yday
    await update.message.reply_text(f"Day {doy} of {days_in_year}, {days_in_year - doy} days left")


async def cmd_in(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    log(update)
    if len(context.args) != 1 or not context.args[0].lstrip("-").isdigit():
        await update.message.reply_text("Usage: /in <days>, e.g. /in 10 or /in -7")
        return
    days = int(context.args[0])
    target = datetime.now() + timedelta(days=days)
    await update.message.reply_text(f"{days:+d} days from today is {target.strftime('%A, %d %B %Y')}")


async def cmd_help(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    log(update)
    lines = [f"/{c.command} - {c.description}" for c in COMMANDS]
    await update.message.reply_text("\n".join(lines))


async def unknown(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    log(update)
    await update.message.reply_text("Unknown command, try /help")


async def reject(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user = update.effective_user
    print(f"[reject] {user.first_name} ({user.id}) is not on the allowlist")
    await update.message.reply_text("Sorry, this bot is currently not available")


async def register_commands(app: Application) -> None:
    """Publish the command list so Telegram shows it in the '/' menu."""
    await app.bot.set_my_commands(COMMANDS)


# --- wiring -----------------------------------------------------------------
def main() -> None:
    allowed_users = load_allowed_users()
    if not allowed_users:
        sys.exit("TELEGRAM_ALLOWED_USERS is empty - nobody could use the bot")

    allowed = filters.User(user_id=allowed_users)
    new_message = filters.UpdateType.MESSAGE

    app = (
        Application.builder()
        .token(os.environ["TELEGRAM_BOT_TOKEN"])
        .post_init(register_commands)
        .build()
    )

    handlers = {
        "time": cmd_time,
        "date": cmd_date,
        "week": cmd_week,
        "doy": cmd_doy,
        "in": cmd_in,
        "help": cmd_help,
        "start": cmd_help,
    }
    for name, func in handlers.items():
        app.add_handler(CommandHandler(name, func, filters=allowed & new_message))

    app.add_handler(MessageHandler(allowed & new_message & filters.COMMAND, unknown))
    app.add_handler(MessageHandler(~allowed & new_message, reject))

    print(f"--- ALLOWED USERS: {sorted(allowed_users)} ---")
    print("--- BOT RUNNING (Ctrl+C to stop) ---")
    app.run_polling()


if __name__ == "__main__":
    main()
