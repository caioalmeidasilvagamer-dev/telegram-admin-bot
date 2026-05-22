from telegram.ext import ApplicationBuilder, MessageHandler, filters
from bot.config import BOT_TOKEN
from bot.database import init_db
from bot.handlers.welcome import welcome_handler
from loguru import logger

async def post_init(app):
    await init_db()

def main():
    app = (
        ApplicationBuilder()
        .token(BOT_TOKEN)
        .post_init(post_init)
        .build()
    )

    app.add_handler(MessageHandler(
        filters.StatusUpdate.NEW_CHAT_MEMBERS,
        welcome_handler
    ))

    logger.info("Bot iniciado.")
    app.run_polling()

if __name__ == "__main__":
    main()