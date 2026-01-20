# services/link_service.py

from datetime import datetime, timedelta
from typing import Optional

from config import (
    DEFAULT_LINK_EXPIRY_MINUTES,
    MAX_DOWNLOADS_PER_LINK_FREE,
    MAX_DOWNLOADS_PER_LINK_PAID,
    FEATURE_PASSWORD_LINK,
    FEATURE_TIME_LIMIT_LINK,
    FEATURE_ONE_TIME_LINK
)

from database.queries.link_queries import (
    create_link_record,
    get_link_by_code,
    increment_download_count,
    disable_link_query
)

from database.queries.file_queries import get_file_by_id_query
from utils.hash import generate_short_code
from utils.encryption import hash_password


# =========================================================
# CREATE DOWNLOAD LINK
# =========================================================
async def create_download_link(
    file_id: str,
    user_id: int,
    is_paid_user: bool = False,
    password: Optional[str] = None,
    expiry_minutes: Optional[int] = None,
    one_time: bool = False
):
    """
    Create secure download link for a file
    """

    # Feature checks
    if password and not FEATURE_PASSWORD_LINK:
        raise ValueError("Password protected links disabled")

    if expiry_minutes and not FEATURE_TIME_LIMIT_LINK:
        raise ValueError("Timed links disabled")

    if one_time and not FEATURE_ONE_TIME_LINK:
        raise ValueError("One time links disabled")

    # File exists check
    file = await get_file_by_id_query(file_id)
    if not file:
        raise ValueError("File not found")

    # Expiry handling
    if expiry_minutes is None:
        expiry_minutes = DEFAULT_LINK_EXPIRY_MINUTES

    expires_at = None
    if expiry_minutes > 0:
        expires_at = datetime.utcnow() + timedelta(minutes=expiry_minutes)

    # Download limits
    max_downloads = (
        MAX_DOWNLOADS_PER_LINK_PAID
        if is_paid_user
        else MAX_DOWNLOADS_PER_LINK_FREE
    )

    # Password hashing
    password_hash = None
    if password:
        password_hash = hash_password(password)

    # Generate unique short code
    code = generate_short_code()

    link = await create_link_record(
        code=code,
        file_id=file_id,
        owner_id=user_id,
        password_hash=password_hash,
        expires_at=expires_at,
        max_downloads=max_downloads,
        one_time=one_time,
        created_at=datetime.utcnow()
    )

    return link


# =========================================================
# VALIDATE LINK
# =========================================================
async def validate_link(code: str, password: Optional[str] = None):
    """
    Validate link before download
    """

    link = await get_link_by_code(code)
    if not link:
        raise ValueError("Invalid link")

    # Disabled
    if link.get("disabled"):
        raise ValueError("Link disabled")

    # Expiry check
    if link.get("expires_at"):
        if datetime.utcnow() > link["expires_at"]:
            await disable_link_query(code)
            raise ValueError("Link expired")

    # Download limit check
    if link.get("max_downloads", 0) > 0:
        if link.get("download_count", 0) >= link["max_downloads"]:
            await disable_link_query(code)
            raise ValueError("Download limit reached")

    # Password check
    if link.get("password_hash"):
        if not password:
            raise ValueError("Password required")

        if hash_password(password) != link["password_hash"]:
            raise ValueError("Incorrect password")

    return link


# =========================================================
# REGISTER DOWNLOAD
# =========================================================
async def register_download(code: str):
    """
    Increase download count and auto-disable if needed
    """

    link = await get_link_by_code(code)
    if not link:
        return

    await increment_download_count(code)

    # One-time link
    if link.get("one_time"):
        await disable_link_query(code)
