# handlers/admin.py

from pyrogram import filters
from pyrogram.types import Message

from core.client import get_client
from config import OWNER_ID, ADMIN_IDS
from services.analytics_service import get_bot_stats
from services.user_service import ban_user, unban_user

app = get_client()


# =========================================================
# ADMIN CHECK
# =========================================================
def is_admin(user_id: int) -> bool:
    return user_id == OWNER_ID or user_id in ADMIN_IDS


# =========================================================
# /admin COMMAND
# =========================================================
@app.on_message(filters.command("admin") & filters.private)
async def admin_panel(client, message: Message):
    if not is_admin(message.from_user.id):
        await message.reply_text("🚫 You are not authorized.")
        return

    await message.reply_text(
        "🛠 **Admin Panel**\n\n"
        "/stats – Bot statistics\n"
        "/ban user_id – Ban user\n"
        "/unban user_id – Unban user\n"
    )


# =========================================================
# /stats COMMAND
# =========================================================
@app.on_message(filters.command("stats") & filters.private)
async def bot_stats(client, message: Message):
    if not is_admin(message.from_user.id):
        await message.reply_text("🚫 Unauthorized.")
        return

    stats = await get_bot_stats()

    await message.reply_text(
        "📊 **Bot Statistics**\n\n"
        f"👥 Users: {stats['users']}\n"
        f"📁 Files: {stats['files']}\n"
        f"⬇️ Downloads: {stats['downloads']}"
    )


# =========================================================
# /ban COMMAND
# =========================================================
@app.on_message(filters.command("ban") & filters.private)
async def ban_user_cmd(client, message: Message):
    if not is_admin(message.from_user.id):
        await message.reply_text("🚫 Unauthorized.")
        return

    if len(message.command) < 2:
        await message.reply_text("Usage: `/ban user_id`")
        return

    user_id = int(message.command[1])
    await ban_user(user_id)

    await message.reply_text(f"🚫 User `{user_id}` banned.")


# =========================================================
# /unban COMMAND
# =========================================================
@app.on_message(filters.command("unban") & filters.private)
async def unban_user_cmd(client, message: Message):
    if not is_admin(message.from_user.id):
        await message.reply_text("🚫 Unauthorized.")
        return

    if len(message.command) < 2:
        await message.reply_text("Usage: `/unban user_id`")
        return

    user_id = int(message.command[1])
    await unban_user(user_id)

    await message.reply_text(f"✅ User `{user_id}` unbanned.")
