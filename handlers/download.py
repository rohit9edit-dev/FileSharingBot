# handlers/download.py

from pyrogram import filters
from pyrogram.types import Message

from core.client import get_client
from config import (
    MAX_DOWNLOADS_PER_LINK_FREE,
    MAX_DOWNLOADS_PER_LINK_PAID,
)

from database.queries.user_queries import (
    is_user_banned,
)

from services.subscription import get_user_subscription
from services.storage import get_file_from_storage
from services.limits import (
    check_download_limit,
    increase_download_count,
)
from services.links import (
    get_link_data,
    increase_link_download_count,
)

app = get_client()


@app.on_message(filters.private & filters.regex(r"^/start\s+(.+)"))
async def download_handler(_, message: Message):
    user = message.from_user
    link_token = message.matches[0].group(1)

    # ❌ Ban check
    if await is_user_banned(user.id):
        return await message.reply_text("🚫 You are banned.")

    # 🔗 Link data
    link = await get_link_data(link_token)
    if not link:
        return await message.reply_text("❌ Invalid or expired link.")

    # 💎 Subscription
    sub = await get_user_subscription(user.id)
    is_paid = bool(sub and sub.is_active)

    # 🚦 Per-link download limit
    max_dl = (
        MAX_DOWNLOADS_PER_LINK_PAID
        if is_paid
        else MAX_DOWNLOADS_PER_LINK_FREE
    )

    if max_dl > 0 and link.download_count >= max_dl:
        return await message.reply_text(
            "🚫 This link has reached its download limit."
        )

    # 🚦 Daily download limit
    allowed = await check_download_limit(user.id, is_paid)
    if not allowed:
        return await message.reply_text(
            "🚫 Daily download limit reached.\n\n"
            "Upgrade your plan to increase limits."
        )

    # ⏳ Processing
    status = await message.reply_text("⏳ Fetching file...")

    # 📦 Get file
    file_message = await get_file_from_storage(
        storage_channel=link.storage_channel,
        message_id=link.message_id
    )

    if not file_message:
        return await status.edit_text("❌ File not found.")

    # 📤 Send file
    await file_message.copy(
        chat_id=message.chat.id,
        caption="✅ **Here is your file**"
    )

    # ➕ Increase counters
    await increase_download_count(user.id)
    await increase_link_download_count(link_token)

    await status.delete()
