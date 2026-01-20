# cache/redis_client.py

import os
import redis

REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379/0")

# Create Redis client
redis_client = redis.StrictRedis.from_url(
    REDIS_URL,
    decode_responses=True  # Automatically decode bytes to str
)

# =========================================================
# Helper functions
# =========================================================

def set_key(key: str, value: str, expire: int = None):
    """
    Set a key in Redis with optional expiration in seconds
    """
    return redis_client.set(name=key, value=value, ex=expire)

def get_key(key: str):
    """
    Get a key from Redis
    """
    return redis_client.get(key)

def delete_key(key: str):
    """
    Delete a key from Redis
    """
    return redis_client.delete(key)

def key_exists(key: str) -> bool:
    """
    Check if a key exists
    """
    return redis_client.exists(key) > 0
