# database/migrations/003_create_file_table.py

from database.connection import db
from datetime import datetime

async def up():
    """
    Create 'files' collection with required fields
    """
    # MongoDB me normally collection automatic ban jati hai data insert karte hi
    # Lekin schema reference ke liye example:
    await db.create_collection("files")
    await db.files.create_index("file_hash", unique=True)
    await db.files.create_index("user_id")
    await db.files.create_index("created_at")

async def down():
    """
    Drop 'files' collection
    """
    await db.files.drop()
