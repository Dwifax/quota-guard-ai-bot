import asyncio
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters

from app.config import settings
from app.providers import ask_ai
from app.storage import init_db, list_cooldowns, reset_cooldowns
from app.rate_limiter import human_duration


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(
        "Halo! Aku QuotaGuard AI Bot. Kirim pesan apa saja, aku akan coba provider AI yang tersedia."
    )


async def status(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    cooldowns = list_cooldowns()
    if not cooldowns:
        await update.message.reply_text("Semua model tersedia. Tidak ada cooldown aktif.")
        return

    lines = ["Status cooldown:"]
    for item in cooldowns:
        lines.append(
            f"- {item['provider']}: {human_duration(item['remaining_seconds'])} ({item['reason']})"
        )
    await update.message.reply_text("\n".join(lines))


async def reset(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    reset_cooldowns()
    await update.message.reply_text("Cooldown lokal sudah direset.")


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    prompt = update.message.text or ""
    await update.message.chat.send_action("typing")
    answer = await ask_ai(prompt)
    await update.message.reply_text(answer[:4000])


def main() -> None:
    if not settings.telegram_bot_token:
        raise RuntimeError("TELEGRAM_BOT_TOKEN belum diisi di .env")

    init_db()
    app = Application.builder().token(settings.telegram_bot_token).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("status", status))
    app.add_handler(CommandHandler("reset", reset))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    app.run_polling()


if __name__ == "__main__":
    main()
