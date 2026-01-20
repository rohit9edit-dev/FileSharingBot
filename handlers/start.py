# handlers/start.py

from pyrogram import filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton

from core.client import get_client
from config import (
    APP_NAME,
    OWNER_ID,
    FORCE_SUB_ENABLED,
    FORCE_SUB_CHANNELS,
    FORCE_SUB_MESSAGE,
)

from database.queries.user_queries import (
    create_user_if_not_exists,
    is_user_banned,
)

from services.force_sub import check_force_subscription
from services.subscription import get_user_subscription

app = get_client()


@app.on_message(filters.command("start") & filters.private)
async def start_handler(_, message: Message):
    user = message.from_user

    # ✅ Save user
    await create_user_if_not_exists(user)

    # ❌ Check ban
    if await is_user_banned(user.id):
        return await message.reply_text(
            "🚫 You are banned from using this bot."
        )

    # 🔒 Force Subscription Check
    if FORCE_SUB_ENABLED:
        not_joined = await check_force_subscription(app, user.id)

        if not_joined:
            buttons = [
                [
                    InlineKeyboardButton(
                        "🔔 Join Channel",
                        url=f"https://t.me/{not_joined}"
                    )
                ],
                [
                    InlineKeyboardButton(
                        "✅ Joined",
                        callback_data="recheck_force_sub"
                    )
                ],
            ]

            return await message.reply_text(
                FORCE_SUB_MESSAGE,
                reply_markup=InlineKeyboardMarkup(buttons),
                disable_web_page_preview=True
            )

    # 💎 Subscription info
    subscription = await get_user_subscription(user.id)

    plan = "FREE"
    if subscription and subscription.is_active:
        plan = subscription.plan.upper()

    # 👑 Owner
    if user.id == OWNER_ID:
        plan = "OWNER"

    text = (
        f"👋 **Welcome to {APP_NAME}!**\n\n"
        f"🆔 **User ID:** `{user.id}`\n"
        f"💎 **Plan:** `{plan}`\n\n"
        "📤 Send me any file and I will generate a secure download link.\n"
        "⚡ Fast • Secure • Private"
    )

    buttons = [
        [
            InlineKeyboardButton("📤 Upload File", callback_data="upload"),
            InlineKeyboardButton("📥 My Files", callback_data="my_files"),
        ],
        [
            InlineKeyboardButton("💎 Upgrade Plan", callback_data="buy_plan"),
            InlineKeyboardButton("📞 Support", url="https://t.me/suppme1"),
        ],
    ]

    await message.reply_text(
        text,
        reply_markup=InlineKeyboardMarkup(buttons),
        disable_web_page_preview=True
    )
