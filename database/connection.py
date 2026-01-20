# database/connection.py

from motor.motor_asyncio import AsyncIOMotorClient
from config import DATABASE_URL

class Database:
    """
    MongoDB connection manager.
    """
    _client = None
    _db = None

    @classmethod
    def get_client(cls):
        if cls._client is None:
            cls._client = AsyncIOMotorClient(DATABASE_URL)
        return cls._client

    @classmethod
    def get_db(cls, db_name: str = "AdvancedFileSharingBot"):
        """
        Return the database instance.
        """
        if cls._db is None:
            cls._db = cls.get_client()[db_name]
        return cls._db

# Example usage:
# from database.connection import Database
# db = Database.get_db()
# await db.users.find_one({"user_id": 12345})
