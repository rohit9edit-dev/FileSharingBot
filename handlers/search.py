# handlers/search.py

from pyrogram import filters
from pyrogram.types import Message

from core.client import get_client
from services.file_service import search_user_files
from utils.formatter import format_file_result

app = get_client()


# =========================================================
# /search COMMAND
# =========================================================
@app.on_message(filters.command("search") & filters.private)
async def search_files(client, message: Message):
    user_id = message.from_user.id

    # ❌ No keyword
    if len(message.command) < 2:
        await message.reply_text(
            "🔍 **Search Usage:**\n\n"
            "`/search movie`\n"
            "`/search pdf`\n"
            "`/search photo`"
        )
        return

    keyword = " ".join(message.command[1:]).lower()

    await message.reply_text("🔎 Searching your files...")

    results = await search_user_files(user_id, keyword)

    if not results:
        await message.reply_text("❌ No matching files found.")
        return

    text = "📁 **Search Results:**\n\n"

    for file in results[:20]:  # limit output
        text += format_file_result(file)

    await message.reply_text(text, disable_web_page_preview=True)
