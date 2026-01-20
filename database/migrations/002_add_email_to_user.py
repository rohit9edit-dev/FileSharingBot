# database/migrations/002_add_email_to_user.py

from database.connection import db

async def up():
    """
    Add 'email' field to all users (optional, can be empty)
    """
    # MongoDB me email field default empty string add karenge
    await db.users.update_many(
        {},
        {"$set": {"email": ""}}
    )

async def down():
    """
    Remove 'email' field from all users
    """
    await db.users.update_many(
        {},
        {"$unset": {"email": ""}}
    )
