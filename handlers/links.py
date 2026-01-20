# services/links.py

import secrets
from datetime import datetime, timedelta

from config import DEFAULT_LINK_EXPIRY_MINUTES
from database import db


# 📌 Collection
links_col = db.links


# =========================================================
# CREATE LINK
# =========================================================
async def create_link(
    user_id: int,
    storage_channel: int,
    message_id: int,
    expiry_minutes: int | None = None,
    one_time: bool = False
):
    token = secrets.token_urlsafe(12)

    if expiry_minutes is None:
        expiry_minutes = DEFAULT_LINK_EXPIRY_MINUTES

    expires_at = None
    if expiry_minutes > 0:
        expires_at = datetime.utcnow() + timedelta(minutes=expiry_minutes)

    data = {
        "token": token,
        "user_id": user_id,
        "storage_channel": storage_channel,
        "message_id": message_id,
        "created_at": datetime.utcnow(),
        "expires_at": expires_at,
        "one_time": one_time,
        "download_count": 0,
        "is_active": True
    }

    await links_col.insert_one(data)
    return token


# =========================================================
# GET LINK DATA
# =========================================================
async def get_link_data(token: str):
    link = await links_col.find_one({"token": token})

    if not link:
        return None

    # ❌ Disabled
    if not link.get("is_active", True):
        return None

    # ⏳ Expired
    expires_at = link.get("expires_at")
    if expires_at and datetime.utcnow() > expires_at:
        await disable_link(token)
        return None

    return SimpleNamespace(**link)


# =========================================================
# INCREASE DOWNLOAD COUNT
# =========================================================
async def increase_link_download_count(token: str):
    link = await links_col.find_one({"token": token})
    if not link:
        return

    new_count = link.get("download_count", 0) + 1

    update = {"download_count": new_count}

    # 🔥 One-time link auto disable
    if link.get("one_time"):
        update["is_active"] = False

    await links_col.update_one(
        {"token": token},
        {"$set": update}
    )


# =========================================================
# DISABLE LINK
# =========================================================
async def disable_link(token: str):
    await links_col.update_one(
        {"token": token},
        {"$set": {"is_active": False}}
    )


# =========================================================
# USER LINKS (OPTIONAL)
# =========================================================
async def get_user_links(user_id: int):
    cursor = links_col.find({"user_id": user_id})
    return [SimpleNamespace(**doc) async for doc in cursor]


# =========================================================
# UTILS
# =========================================================
from types import SimpleNamespace
