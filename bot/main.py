from telegram.ext import ApplicationBuilder, MessageHandler, CommandHandler, filters
from bot.config import BOT_TOKEN
from bot.database import init_db
from bot.handlers.welcome import welcome_handler
from bot.handlers.admin import warn_handler, ban_handler, mute_handler, info_handler
from bot.handlers.moderation import anti_flood
from loguru import logger
import traceback
import asyncio
from telegram.error import RetryAfter, NetworkError

async def post_init(app):
    await init_db()

async def error_handler(update, context):
    error = context.error

    if isinstance(error, RetryAfter):
        logger.warning(f"Rate limit atingido. Esperando {error.retry_after}s")
        await asyncio.sleep(error.retry_after)
        return

    if isinstance(error, NetworkError):
        logger.warning("Erro de rede — reconectando...")
        return

    logger.error(f"Erro inesperado: {traceback.format_exc()}")

def main():
    app = (
        ApplicationBuilder()
        .token(BOT_TOKEN)
        .post_init(post_init)
        .build()
    )


    
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, anti_flood))
    app.add_handler(MessageHandler(filters.StatusUpdate.NEW_CHAT_MEMBERS, welcome_handler))
    app.add_handler(CommandHandler("warn", warn_handler))
    app.add_handler(CommandHandler("ban", ban_handler))
    app.add_handler(CommandHandler("mute",mute_handler))
    app.add_handler(CommandHandler("info",info_handler))
    app.add_error_handler(error_handler)

    logger.info("Bot iniciado.")
    app.run_polling()

if __name__ == "__main__":
    main()