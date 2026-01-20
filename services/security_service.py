# services/security_service.py

from datetime import datetime, timedelta

from config import (
    RATE_LIMIT_ENABLED,
    RATE_LIMIT_PER_MINUTE,
    CAPTCHA_ON_SUSPICIOUS,
    AUTO_TEMP_BAN,
    TEMP_BAN_DURATION_MINUTES,
)

from cache.redis_client import (
    get_redis,
    incr_key,
    get_key,
    set_key,
    delete_key,
)


# =========================================================
# RATE LIMIT
# =========================================================
async def check_rate_limit(user_id: int) -> bool:
    """
    Returns True if allowed, False if rate limited
    """
    if not RATE_LIMIT_ENABLED:
        return True

    redis = get_redis()
    key = f"rate:{user_id}"

    count = await incr_key(key, expire=60)

    if count > RATE_LIMIT_PER_MINUTE:
        if AUTO_TEMP_BAN:
            await temp_ban_user(user_id)
        return False

    return True


# =========================================================
# TEMP BAN
# =========================================================
async def temp_ban_user(user_id: int):
    """
    Temporarily ban user
    """
    until = datetime.utcnow() + timedelta(minutes=TEMP_BAN_DURATION_MINUTES)
    key = f"ban:{user_id}"

    await set_key(key, until.isoformat(), expire=TEMP_BAN_DURATION_MINUTES * 60)


async def is_user_banned(user_id: int) -> bool:
    key = f"ban:{user_id}"
    return await get_key(key) is not None


# =========================================================
# SUSPICIOUS ACTIVITY
# =========================================================
async def mark_suspicious(user_id: int):
    """
    Flag user as suspicious (captcha later)
    """
    if not CAPTCHA_ON_SUSPICIOUS:
        return

    key = f"suspicious:{user_id}"
    await set_key(key, "1", expire=3600)


async def is_suspicious(user_id: int) -> bool:
    key = f"suspicious:{user_id}"
    return await get_key(key) is not None


# =========================================================
# CLEANUP
# =========================================================
async def clear_security_flags(user_id: int):
    """
    Clear all security flags
    """
    await delete_key(f"rate:{user_id}")
    await delete_key(f"suspicious:{user_id}")
    await delete_key(f"ban:{user_id}")
