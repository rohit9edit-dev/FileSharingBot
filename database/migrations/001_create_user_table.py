# database/migrations/001_create_user_table.py

from database.connection import db

async def up():
    """
    Migration to create the 'users' collection/table
    """
    # Create 'users' collection if not exists
    if "users" not in await db.list_collection_names():
        await db.create_collection("users")
    
    # Ensure user_id is unique
    await db.users.create_index("user_id", unique=True)

async def down():
    """
    Rollback migration: Drop the 'users' collection
    """
    await db.users.drop()
