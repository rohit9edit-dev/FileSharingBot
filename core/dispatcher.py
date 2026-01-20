# core/dispatcher.py

import logging
from pyrogram import filters
from pyrogram.handlers import MessageHandler, CallbackQueryHandler

from core.client import get_client
from handlers import (
    start,
    upload,
    download,
    links,
    search,
    user,
    admin,
    errors,
)

logger = logging.getLogger(__name__)


def setup_dispatcher():
    """
    Register all bot handlers here
    """
    app = get_client()

    # ===============================
    # BASIC COMMANDS
    # ===============================
    app.add_handler(MessageHandler(start.start_handler, filters.command("start")))

    # ===============================
    # FILE HANDLING
    # ===============================
    app.add_handler(MessageHandler(upload.upload_handler, filters.document | filters.video | filters.audio))
    app.add_handler(MessageHandler(download.download_handler, filters.command("get")))

    # ===============================
    # LINK FEATURES
    # ===============================
    app.add_handler(MessageHandler(links.links_handler, filters.command("link")))
    app.add_handler(CallbackQueryHandler(links.link_callback_handler, filters.regex("^link_")))

    # ===============================
    # SEARCH
    # ===============================
    app.add_handler(MessageHandler(search.search_handler, filters.command("search")))

    # ===============================
    # USER COMMANDS
    # ===============================
    app.add_handler(MessageHandler(user.user_handler, filters.command("me")))

    # ===============================
    # ADMIN COMMANDS
    # ===============================
    app.add_handler(MessageHandler(admin.admin_handler, filters.command("admin")))

    # ===============================
    # ERROR HANDLER (LAST)
    # ===============================
    app.add_handler(MessageHandler(errors.error_handler, filters.all))

    logger.info("✅ Dispatcher setup completed")
