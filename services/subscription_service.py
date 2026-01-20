# services/subscription_service.py

from datetime import datetime, timedelta
from typing import Optional

from config import PLANS
from database.queries.user_queries import (
    get_user_by_id_query,
    update_user_plan_query
)


# =========================================================
# SUBSCRIPTION LOGIC
# =========================================================

async def get_user_plan(user_id: int) -> Optional[dict]:
    """
    Return current plan info for user
    """
    user = await get_user_by_id_query(user_id)
    if not user or not user.subscription:
        return None

    plan = user.subscription.get("plan")
    expires_at = user.subscription.get("expires_at")

    return {
        "plan": plan,
        "expires_at": expires_at,
        "active": expires_at is None or expires_at > datetime.utcnow()
    }


async def activate_plan(user_id: int, plan_name: str) -> dict:
    """
    Activate / Upgrade a plan for user
    """
    if plan_name not in PLANS:
        raise ValueError(f"Plan '{plan_name}' does not exist")

    plan_info = PLANS[plan_name]

    # calculate expiry
    if plan_info["duration_days"] == 0:
        expires_at = None  # lifetime
    else:
        expires_at = datetime.utcnow() + timedelta(days=plan_info["duration_days"])

    # update DB
    await update_user_plan_query(
        user_id=user_id,
        plan=plan_name,
        expires_at=expires_at
    )

    return {
        "plan": plan_name,
        "expires_at": expires_at
    }


async def is_user_paid(user_id: int) -> bool:
    """
    Check if user has an active paid plan
    """
    plan_data = await get_user_plan(user_id)
    if not plan_data:
        return False

    plan_name = plan_data["plan"]
    if plan_name == "basic" and plan_data["active"]:
        return True
    elif plan_name in ["power", "business", "lifetime"] and plan_data["active"]:
        return True

    return False
