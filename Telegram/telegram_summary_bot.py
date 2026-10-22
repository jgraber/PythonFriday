import os
import sys

from dotenv import load_dotenv
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_openai import ChatOpenAI
from telegram import BotCommand, Update
from telegram.constants import ChatAction
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters

sys.stdout.reconfigure(encoding="utf-8")

load_dotenv()

llm = ChatOpenAI(
    model="qwen/qwen3.8-27b",
    openai_api_base="http://127.0.0.1:1234/v1",
    api_key="not-needed",  # LM Studio ignores this
    temperature=0.1,
)

SYSTEM_PROMPT = (
    "You are a concise assistant. Summarise the text the user sends in 2-4 sentences. "
    "Keep the language of the original text. Reply with the summary only, no preamble."
)

COMMANDS = [
    BotCommand("summary", "summarise text: /summary <text>, or reply to a message with /summary"),
    BotCommand("help", "show usage"),
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


def text_to_summarise(update: Update, context: ContextTypes.DEFAULT_TYPE) -> str | None:
    """Text after the command, or the text of the message the user replied to."""
    if context.args:
        return " ".join(context.args)
    replied = update.message.reply_to_message
    if replied and (replied.text or replied.caption):
        return replied.text or replied.caption
    return None


async def summarise(text: str) -> str:
    response = await llm.ainvoke([SystemMessage(content=SYSTEM_PROMPT), HumanMessage(content=text)])
    return response.content.strip()


# --- handlers ---------------------------------------------------------------

async def cmd_summary(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user = update.effective_user
    text = text_to_summarise(update, context)
    if not text:
        await update.message.reply_text(
            "Send the text after the command (/summary <text>) "
            "or reply to a message with /summary."
        )
        return

    print(f"[summary] {user.first_name}: {len(text)} chars")
    await update.message.chat.send_action(ChatAction.TYPING)
    try:
        summary = await summarise(text)
    except Exception as exc:
        print(f"[error] LLM call failed: {exc}")
        await update.message.reply_text("Could not reach the local LLM. Is LM Studio running?")
        return

    await update.message.reply_text(summary)


async def cmd_help(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    lines = [f"/{c.command} - {c.description}" for c in COMMANDS]
    await update.message.reply_text("\n".join(lines))


async def unknown(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("Unknown command, try /help")


async def reject(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user = update.effective_user
    print(f"[reject] {user.first_name} ({user.id}) is not on the allowlist")
    await update.message.reply_text("Sorry, this bot is currently not available")


async def register_commands(app: Application) -> None:
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

    app.add_handler(CommandHandler("summary", cmd_summary, filters=allowed & new_message))
    app.add_handler(CommandHandler(["help", "start"], cmd_help, filters=allowed & new_message))
    app.add_handler(MessageHandler(allowed & new_message & filters.COMMAND, unknown))
    app.add_handler(MessageHandler(~allowed & new_message, reject))

    print(f"--- ALLOWED USERS: {sorted(allowed_users)} ---")
    print("--- BOT RUNNING (Ctrl+C to stop) ---")
    app.run_polling()


if __name__ == "__main__":
    main()
