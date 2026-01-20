# storage/channel_manager.py

from pyrogram import Client
from config import PRIVATE_STORAGE_CHANNELS
from core.client import get_client
import logging
import asyncio

logger = logging.getLogger("ChannelManager")


async def store_file_to_channel(file_bytes: bytes, file_name: str, mime_type: str) -> str:
    """
    Upload file to one of the private storage channels and return Telegram file_id
    """
    client: Client = get_client()

    for channel_id in PRIVATE_STORAGE_CHANNELS:
        try:
            async with client:
                message = await client.send_document(
                    chat_id=channel_id,
                    document=file_bytes,
                    file_name=file_name,
                    mime_type=mime_type
                )
                logger.info(f"Uploaded file {file_name} to channel {channel_id}")
                return message.document.file_id

        except Exception as e:
            logger.warning(f"Failed to upload to channel {channel_id}: {e}")
            continue

    raise Exception("All storage channels failed")


async def get_channel_files(channel_id: int, limit: int = 50):
    """
    List last `limit` files uploaded in a channel
    """
    client: Client = get_client()
    files = []

    try:
        async with client:
            async for message in client.get_chat_history(chat_id=channel_id, limit=limit):
                if message.document:
                    files.append(message.document)
    except Exception as e:
        logger.error(f"Error fetching files from channel {channel_id}: {e}")

    return files
