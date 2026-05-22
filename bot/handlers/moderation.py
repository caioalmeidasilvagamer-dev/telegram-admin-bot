from collections import defaultdict
from datetime import datetime
from telegram import Update
from telegram.ext import ContextTypes
from telegram import ChatPermissions
from bot.database import log_action
from loguru import logger

# Memória temporária — reseta quando o bot reinicia
message_tracker = defaultdict(list)

FLOOD_LIMIT = 5       # mensagens
FLOOD_WINDOW = 10     # segundos

async def anti_flood(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message or not update.effective_user:
        return

    user = update.effective_user
    agora = datetime.now()

    # Adiciona horário atual e filtra só os últimos 10 segundos
    message_tracker[user.id].append(agora)
    message_tracker[user.id] = [
        t for t in message_tracker[user.id]
        if (agora - t).seconds < FLOOD_WINDOW
    ]

    if len(message_tracker[user.id]) >= FLOOD_LIMIT:
        await update.message.chat.restrict_member(
            user.id,
            permissions=ChatPermissions(can_send_messages=False),
            until_date=int(agora.timestamp()) + 60
        )
        await update.message.reply_text(
            f"🚫 {user.first_name} foi silenciado por 60s por flood."
        )
        message_tracker[user.id].clear()
        await log_action("mute_flood", 0, user.id, "anti-flood")
        logger.info(f"Flood detectado: {user.first_name} ({user.id})")