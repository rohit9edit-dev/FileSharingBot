# scripts/cleanup.py

import asyncio
import logging
from datetime import datetime, timedelta

from cache.redis_client import get_redis
from cache.keys import LINK_PREFIX, LINK_DOWNLOAD_COUNT, TEMP_BAN_PREFIX

logger = logging.getLogger("CleanupScript")


async def cleanup_expired_links():
    """
    Remove expired links and their download counters
    """
    redis = await get_redis()
    keys = await redis.keys(f"{LINK_PREFIX}*")
    
    for key in keys:
        link_data = await redis.hgetall(key)
        if not link_data:
            continue

        expiry = link_data.get("expiry")
        if expiry:
            expiry_dt = datetime.fromisoformat(expiry)
            if expiry_dt < datetime.utcnow():
                # delete link and its download counter
                link_id = key.split(":")[1]
                await redis.delete(key)
                await redis.delete(LINK_DOWNLOAD_COUNT.format(link_id=link_id))
                logger.info(f"Deleted expired link {link_id}")


async def cleanup_temp_bans():
    """
    Remove expired temporary bans
    """
    redis = await get_redis()
    keys = await redis.keys(f"{TEMP_BAN_PREFIX}*")

    for key in keys:
        ban_data = await redis.hgetall(key)
        if not ban_data:
            continue
        
        expire_at = ban_data.get("expire_at")
        if expire_at and datetime.fromisoformat(expire_at) < datetime.utcnow():
            await redis.delete(key)
            user_id = key.split(":")[1]
            logger.info(f"Removed temporary ban for user {user_id}")


async def main():
    await cleanup_expired_links()
    await cleanup_temp_bans()
    logger.info("Cleanup finished.")


if __name__ == "__main__":
    asyncio.run(main())
