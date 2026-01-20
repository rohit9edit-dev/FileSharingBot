# services/user_service.py

from datetime import datetime, timedelta
from typing import Optional

from config import (
    FREE_DAILY_UPLOAD_LIMIT,
    FREE_DAILY_DOWNLOAD_LIMIT,
    PAID_DAILY_UPLOAD_LIMIT,
    PAID_DAILY_DOWNLOAD_LIMIT,
    PLANS,
)

from database.queries.user_queries import (
    get_user_by_id_query,
    create_user_query,
    update_user_query,
    increment_upload_count_query,
    increment_download_count_query,
    reset_daily_limits_query,
)

from database.queries.subscription_queries import (
    get_active_subscription_query,
    create_subscription_query,
)


# =========================================================
# GET OR CREATE USER
# =========================================================
async def get_or_create_user(user_id: int, username: Optional[str] = None):
    """
    Fetch user from DB or create new
    """
    user = await get_user_by_id_query(user_id)

    if not user:
        user = await create_user_query(
            user_id=user_id,
            username=username,
            created_at=datetime.utcnow(),
        )

    return user


# =========================================================
# CHECK IF USER IS PAID
# =========================================================
async def is_paid_user(user_id: int) -> bool:
    subscription = await get_active_subscription_query(user_id)

    if not subscription:
        return False

    # Lifetime
    if subscription.get("expires_at") is None:
        return True

    return datetime.utcnow() < subscription["expires_at"]


# =========================================================
# USER LIMITS
# =========================================================
async def get_user_limits(user_id: int):
    paid = await is_paid_user(user_id)

    if paid:
        return {
            "upload": PAID_DAILY_UPLOAD_LIMIT,
            "download": PAID_DAILY_DOWNLOAD_LIMIT,
        }

    return {
        "upload": FREE_DAILY_UPLOAD_LIMIT,
        "download": FREE_DAILY_DOWNLOAD_LIMIT,
    }


# =========================================================
# DAILY LIMIT CHECKS
# =========================================================
async def can_upload(user_id: int) -> bool:
    user = await get_or_create_user(user_id)
    limits = await get_user_limits(user_id)

    if user["daily_uploads"] >= limits["upload"]:
        return False

    return True


async def can_download(user_id: int) -> bool:
    user = await get_or_create_user(user_id)
    limits = await get_user_limits(user_id)

    if user["daily_downloads"] >= limits["download"]:
        return False

    return True


# =========================================================
# REGISTER ACTIVITY
# =========================================================
async def register_upload(user_id: int):
    await increment_upload_count_query(user_id)


async def register_download(user_id: int):
    await increment_download_count_query(user_id)


# =========================================================
# DAILY RESET (CRON)
# =========================================================
async def reset_daily_limits():
    """
    Reset daily upload/download counts (run once per day)
    """
    await reset_daily_limits_query()


# =========================================================
# SUBSCRIPTION
# =========================================================
async def activate_subscription(
    user_id: int,
    plan_key: str,
):
    """
    Activate subscription after payment
    """
    plan = PLANS.get(plan_key)
    if not plan:
        raise ValueError("Invalid plan")

    duration = plan["duration_days"]

    expires_at = None
    if duration > 0:
        expires_at = datetime.utcnow() + timedelta(days=duration)

    subscription = await create_subscription_query(
        user_id=user_id,
        plan=plan_key,
        price=plan["price"],
        expires_at=expires_at,
        created_at=datetime.utcnow(),
    )

    return subscription
