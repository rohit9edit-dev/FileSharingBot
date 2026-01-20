# handlers/errors.py

import logging
import traceback

from pyrogram import filters
from pyrogram.types import Message

from core.client import get_client
from config import APP_NAME, SUPPORT_CHAT

app = get_client()

logger = logging.getLogger(APP_NAME)


# =========================================================
# GLOBAL ERROR HANDLER
# =========================================================
@app.on_message(filters.private)
async def global_error_handler(client, message: Message):
    try:
        await message.continue_propagation()
    except Exception as e:
        error_id = id(e)

        # Log full traceback
        logger.error(
            f"[ERROR_ID={error_id}]\n{traceback.format_exc()}"
        )

        # User-friendly message
        await message.reply_text(
            "⚠️ **Something went wrong!**\n\n"
            "Our system logged this error.\n"
            "Please try again later.\n\n"
            f"🆔 Error ID: `{error_id}`\n"
            f"💬 Support: {SUPPORT_CHAT}"
        )
