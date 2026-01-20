# handlers/upload.py

from pyrogram import filters
from pyrogram.types import Message

from core.client import get_client
from config import (
    MAX_FILE_SIZE_FREE,
    MAX_FILE_SIZE_PAID,
)

from database.queries.user_queries import (
    is_user_banned,
)

from services.subscription import get_user_subscription
from services.storage import save_file_to_storage
from services.limits import check_upload_limit, increase_upload_count
from utils.link_generator import generate_download_link

app = get_client()


@app.on_message(
    filters.private &
    (filters.document | filters.video | filters.audio | filters.photo)
)
async def upload_handler(_, message: Message):
    user = message.from_user

    # ❌ Ban check
    if await is_user_banned(user.id):
        return await message.reply_text("🚫 You are banned.")

    # 💎 Subscription
    sub = await get_user_subscription(user.id)
    is_paid = bool(sub and sub.is_active)

    # 📏 File object
    file = (
        message.document
        or message.video
        or message.audio
        or message.photo
    )

    if not file:
        return

    file_size = file.file_size or 0

    # 📦 Size limit
    max_size = MAX_FILE_SIZE_PAID if is_paid else MAX_FILE_SIZE_FREE
    if file_size > max_size:
        return await message.reply_text(
            f"❌ File too large.\n\n"
            f"Allowed: `{max_size // (1024**3)} GB`"
        )

    # 🚦 Daily upload limit
    allowed = await check_upload_limit(user.id, is_paid)
    if not allowed:
        return await message.reply_text(
            "🚫 Daily upload limit reached.\n\n"
            "Upgrade your plan to increase limits."
        )

    # ⏳ Processing
    status = await message.reply_text("⏳ Uploading file...")

    # 💾 Save to private channel
    file_id = await save_file_to_storage(message)

    # 🔗 Generate link
    link = await generate_download_link(
        user_id=user.id,
        file_id=file_id,
        is_paid=is_paid
    )

    # ➕ Increase count
    await increase_upload_count(user.id)

    # ✅ Done
    await status.edit_text(
        "✅ **File uploaded successfully!**\n\n"
        f"🔗 **Download Link:**\n{link}\n\n"
        "⚠️ Do not share publicly."
    )
