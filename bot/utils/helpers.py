from functools import wraps
from telegram import Update
from telegram.ext import ContextTypes
from bot.config import ADMIN_IDS

def admin_only(func):
    @wraps(func)
    async def wrapper(update: Update, context: ContextTypes.DEFAULT_TYPE):
        if update.effective_user.id not in ADMIN_IDS:
            await update.message.reply_text("⛔ Você não tem permissão.")
            return
        return await func(update, context)
    return wrapper