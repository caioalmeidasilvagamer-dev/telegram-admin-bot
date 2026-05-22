from telegram import Update
from telegram.ext import ContextTypes
from bot.database import upsert_user
from loguru import logger

async def welcome_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    for member in update.message.new_chat_members:
        if member.is_bot:
            continue

        await upsert_user(member.id, member.username or member.first_name)

        await update.message.reply_text(
            f"👋 Bem-vindo ao grupo, {member.first_name}!\n"
            f"Por favor, leia as regras antes de participar."
        )
        logger.info(f"Novo membro: {member.first_name} ({member.id})")