from telegram import Update
from telegram.ext import ContextTypes
from bot.database import upsert_user, add_warn, log_action
from bot.utils.helpers import admin_only
from loguru import logger

@admin_only
async def warn_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message.reply_to_message:
        await update.message.reply_text("↩️ Responda a mensagem do usuário que deseja advertir.")
        return

    target = update.message.reply_to_message.from_user
    await upsert_user(target.id, target.username or target.first_name)
    warns = await add_warn(target.id)
    await log_action("warn", update.effective_user.id, target.id)

    await update.message.reply_text(
        f"⚠️ {target.first_name} recebeu uma advertência. Total: {warns}/3"
    )
    logger.info(f"Warn: {target.first_name} ({target.id}) — {warns}/3")

    if warns >= 3:
        await update.message.chat.ban_member(target.id)
        await update.message.reply_text(f"🔨 {target.first_name} foi banido por atingir 3 advertências.")
        await log_action("auto_ban", update.effective_user.id, target.id, "3 warns")
        logger.info(f"Auto-ban: {target.first_name} ({target.id})")

@admin_only
async def ban_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message.reply_to_message:
        await update.message.reply_text("↩️ Responda a mensagem do usuário que deseja banir.")
        return

    target = update.message.reply_to_message.from_user
    reason = " ".join(context.args) if context.args else "Sem motivo"

    await update.message.chat.ban_member(target.id)
    await log_action("ban", update.effective_user.id, target.id, reason)

    await update.message.reply_text(f"🔨 {target.first_name} foi banido. Motivo: {reason}")
    logger.info(f"Ban: {target.first_name} ({target.id}) — {reason}")