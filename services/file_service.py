# services/file_service.py

import hashlib
from datetime import datetime
from typing import List, Tuple

from config import (
    MAX_FILE_SIZE_FREE,
    MAX_FILE_SIZE_PAID
)

from database.queries.file_queries import (
    create_file_record,
    get_file_by_hash,
    get_user_files_query,
    search_files_query,
    get_file_by_id_query,
    rename_file_query,
    delete_file_query
)

from storage.channel_manager import store_file_to_channel
from utils.formatter import human_readable_size


# =========================================================
# INTERNAL UTILS
# =========================================================
def calculate_file_hash(file_bytes: bytes) -> str:
    """
    SHA256 hash for duplicate detection
    """
    return hashlib.sha256(file_bytes).hexdigest()


# =========================================================
# UPLOAD FILE
# =========================================================
async def upload_file(
    user_id: int,
    file_name: str,
    file_size: int,
    file_bytes: bytes,
    mime_type: str,
    is_paid_user: bool = False
) -> Tuple[dict, bool]:
    """
    Upload file:
    - check size
    - check duplicate
    - store in Telegram private channel
    - save DB record

    Returns:
        (file_record, is_duplicate)
    """

    # File size limit check
    max_size = MAX_FILE_SIZE_PAID if is_paid_user else MAX_FILE_SIZE_FREE
    if file_size > max_size:
        raise ValueError("File size limit exceeded")

    # Hash
    file_hash = calculate_file_hash(file_bytes)

    # Duplicate check
    existing = await get_file_by_hash(file_hash)
    if existing:
        return existing, True

    # Store file in private channel
    telegram_file_id = await store_file_to_channel(
        file_bytes=file_bytes,
        file_name=file_name,
        mime_type=mime_type
    )

    # Save DB
    file_record = await create_file_record(
        user_id=user_id,
        file_name=file_name,
        file_size=file_size,
        file_hash=file_hash,
        telegram_file_id=telegram_file_id,
        mime_type=mime_type,
        created_at=datetime.utcnow()
    )

    return file_record, False


# =========================================================
# USER FILES
# =========================================================
async def get_user_files(
    user_id: int,
    limit: int = 10
) -> List[dict]:
    """
    Get recent files uploaded by user
    """
    files = await get_user_files_query(user_id=user_id, limit=limit)

    for f in files:
        f["size_readable"] = human_readable_size(f["file_size"])

    return files


# =========================================================
# SEARCH FILES
# =========================================================
async def search_files(
    user_id: int,
    query: str,
    limit: int = 10
) -> List[dict]:
    """
    Search files by name
    """
    results = await search_files_query(
        user_id=user_id,
        query=query,
        limit=limit
    )

    for f in results:
        f["size_readable"] = human_readable_size(f["file_size"])

    return results


# =========================================================
# SINGLE FILE OPERATIONS
# =========================================================
async def get_file_by_id(file_id: str):
    """
    Get single file by ID
    """
    return await get_file_by_id_query(file_id)


async def rename_file(file_id: str, new_name: str):
    """
    Rename file
    """
    return await rename_file_query(file_id, new_name)


async def delete_file(file_id: str, soft: bool = True):
    """
    Soft delete / hard delete
    """
    return await delete_file_query(file_id, soft=soft)
