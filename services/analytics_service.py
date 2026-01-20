# services/analytics_service.py

from datetime import datetime
from typing import Optional

from cache.redis_client import (
    incr_key,
    get_key,
    set_key
)

from database.connection import get_db


# =========================================================
# BASIC COUNTERS (REDIS FAST STATS)
# =========================================================

async def log_user_action(user_id: int, action: str):
    """
    Track user actions like:
    upload, download, link_create, search
    """
    key = f"analytics:user:{user_id}:{action}"
    await incr_key(key, expire=86400)  # daily stats


async def increment_global(action: str):
    """
    Global counters
    """
    key = f"analytics:global:{action}"
    await incr_key(key)


# =========================================================
# FILE / DOWNLOAD ANALYTICS
# =========================================================

async def log_file_upload(user_id: int, file_size: int):
    await log_user_action(user_id, "upload")
    await increment_global("uploads")

    await incr_key("analytics:global:upload_size", amount=file_size)


async def log_file_download(user_id: int):
    await log_user_action(user_id, "download")
    await increment_global("downloads")


async def log_link_created(user_id: int):
    await log_user_action(user_id, "link_create")
    await increment_global("links")


# =========================================================
# DB LOGS (LONG TERM)
# =========================================================

async def save_event(
    user_id: int,
    event: str,
    meta: Optional[dict] = None
):
    """
    Save permanent event in DB (audit / analytics)
    """
    db = get_db()
    await db.analytics.insert_one({
        "user_id": user_id,
        "event": event,
        "meta": meta or {},
        "created_at": datetime.utcnow()
    })


# =========================================================
# STATS READERS
# =========================================================

async def get_user_daily_stat(user_id: int, action: str) -> int:
    key = f"analytics:user:{user_id}:{action}"
    val = await get_key(key)
    return int(val) if val else 0


async def get_global_stat(action: str) -> int:
    key = f"analytics:global:{action}"
    val = await get_key(key)
    return int(val) if val else 0
