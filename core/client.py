# core/client.py

import asyncio
import logging
from typing import Optional

from pyrogram import Client
from pyrogram.errors import FloodWait

from config import API_ID, API_HASH, BOT_TOKEN, APP_NAME

logger = logging.getLogger(APP_NAME)

_app: Optional[Client] = None


def get_client() -> Client:
    """
    Returns singleton Pyrogram Client
    """
    global _app

    if _app is not None:
        return _app

    _app = Client(
        name=APP_NAME,          # Bot session name
        api_id=API_ID,          # From config.py
        api_hash=API_HASH,      # From config.py
        bot_token=BOT_TOKEN,    # From config.py
        in_memory=True,
        workers=50,
    )

    _patch_floodwait(_app)
    return _app


def _patch_floodwait(app: Client):
    """
    Auto-handle FloodWait errors
    """
    original_invoke = app.invoke

    async def invoke_with_floodwait(*args, **kwargs):
        while True:
            try:
                return await original_invoke(*args, **kwargs)
            except FloodWait as e:
                wait_time = int(e.value)
                logger.warning(f"FloodWait detected. Sleeping for {wait_time}s")
                await asyncio.sleep(wait_time + 1)

    app.invoke = invoke_with_floodwait
