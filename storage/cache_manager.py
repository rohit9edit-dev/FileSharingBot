# storage/cache_manager.py

import aioredis
import asyncio
from config import REDIS_URL
import logging

logger = logging.getLogger("CacheManager")

_redis = None


async def get_redis():
    """
    Initialize Redis client if not already done
    """
    global _redis
    if _redis is None:
        _redis = await aioredis.from_url(REDIS_URL, decode_responses=True)
        logger.info("Connected to Redis")
    return _redis


# ------------------------------
# BASIC CACHE HELPERS
# ------------------------------
async def set_cache(key: str, value, expire_seconds: int = 0):
    """
    Set a value in Redis with optional expiry
    """
    r = await get_redis()
    if expire_seconds > 0:
        await r.set(key, value, ex=expire_seconds)
    else:
        await r.set(key, value)


async def get_cache(key: str):
    """
    Get a value from Redis
    """
    r = await get_redis()
    return await r.get(key)


async def delete_cache(key: str):
    """
    Delete a key from Redis
    """
    r = await get_redis()
    await r.delete(key)


# ------------------------------
# LINK / USER SPECIFIC HELPERS
# ------------------------------
async def increment_counter(key: str, expire_seconds: int = 0):
    """
    Increment a counter and optionally set expiry
    """
    r = await get_redis()
    value = await r.incr(key)
    if expire_seconds > 0:
        await r.expire(key, expire_seconds)
    return value


async def decrement_counter(key: str):
    """
    Decrement a counter
    """
    r = await get_redis()
    value = await r.decr(key)
    return value


async def exists(key: str):
    """
    Check if a key exists
    """
    r = await get_redis()
    return await r.exists(key)
