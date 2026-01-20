# storage/mirror_manager.py

from pyrogram import Client
from core.client import get_client
from storage.channel_manager import store_file_to_channel
from config import PRIVATE_STORAGE_CHANNELS
import logging
import asyncio

logger = logging.getLogger("MirrorManager")


async def mirror_file_to_channels(file_id: str, source_channel_id: int):
    """
    Mirror a file from source channel to all other private storage channels.
    """
    client: Client = get_client()
    mirrored_file_ids = {}

    async with client:
        try:
            # Download file from source channel
            message = await client.get_messages(chat_id=source_channel_id, message_ids=file_id)
            if not message or not message.document:
                raise Exception("File not found or not a document.")

            file_bytes = await message.download(file_name=f"/tmp/{message.document.file_name}")
            file_name = message.document.file_name
            mime_type = message.document.mime_type

            # Mirror to all private storage channels except the source
            for channel_id in PRIVATE_STORAGE_CHANNELS:
                if channel_id == source_channel_id:
                    continue
                try:
                    tg_file_id = await store_file_to_channel(file_bytes, file_name, mime_type)
                    mirrored_file_ids[channel_id] = tg_file_id
                    logger.info(f"Mirrored {file_name} to channel {channel_id}")
                except Exception as e:
                    logger.warning(f"Failed to mirror to channel {channel_id}: {e}")
                    continue

        except Exception as e:
            logger.error(f"Error mirroring file {file_id}: {e}")

    return mirrored_file_ids
