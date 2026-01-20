# core/middleware.py

import time
import logging
from pyrogram import filters
from pyrogram.types import Message, CallbackQuery

from config import (
    FORCE_SUB_ENABLED,
    FORCE_SUB_CHANNELS,
    FORCE_SUB_MESSAGE,
    RATE_LIMIT_ENABLED,
    RATE_LIMIT_PER_MINUTE,
    OWNER_ID,
    ADMIN_IDS,
)

logger = logging.getLogger(__name__)

# In-memory rate limit store
_USER_RATE_LIMIT = {}


async def is_admin(user_id: int) -> bool:
    return user_id == OWNER_ID or user_id in ADMIN_IDS


async def check_force_subscription(client, user_id: int) -> bool:
    """
    Check if user joined all required channels
    """
    if not FORCE_SUB_ENABLED:
        return True

    for channel_id in FORCE_SUB_CHANNELS:
        try:
            member = await client.get_chat_member(channel_id, user_id)
            if member.status not in ("member", "administrator", "creator"):
                return False
        except Exception:
            return False

    return True


async def rate_limit_check(user_id: int) -> bool:
    """
    Simple per-minute rate limit
    """
    if not RATE_LIMIT_ENABLED:
        return True

    now = int(time.time())
    window = 60

    timestamps = _USER_RATE_LIMIT.get(user_id, [])
    timestamps = [t for t in timestamps if now - t < window]

    if len(timestamps) >= RATE_LIMIT_PER_MINUTE:
        return False

    timestamps.append(now)
    _USER_RATE_LIMIT[user_id] = timestamps
    return True


async def pre_process_message(client, message: Message) -> bool:
    """
    Runs before every command / message
    Return False to block message
    """
    user = message.from_user
    if not user:
        return False

    user_id = user.id

    # Admin bypass
    if await is_admin(user_id):
        return True

    # Force subscription
    if not await check_force_subscription(client, user_id):
        await message.reply_text(FORCE_SUB_MESSAGE)
        return False

    # Rate limit
    if not await rate_limit_check(user_id):
        await message.reply_text("⏳ Slow down! Too many requests.")
        return False

    return True


async def pre_process_callback(client, callback: CallbackQuery) -> bool:
    """
    Runs before every callback query
    """
    user = callback.from_user
    if not user:
        return False

    user_id = user.id

    # Admin bypass
    if await is_admin(user_id):
        return True

    # Force subscription
    if not await check_force_subscription(client, user_id):
        await callback.answer("Join required channels first!", show_alert=True)
        return False

    # Rate limit
    if not await rate_limit_check(user_id):
        await callback.answer("Too many actions. Slow down!", show_alert=True)
        return False

    return True
