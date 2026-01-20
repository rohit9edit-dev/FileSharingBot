# core/scheduler.py

import asyncio
import logging
from datetime import datetime, timedelta

from config import (
    AUTO_TEMP_BAN,
    TEMP_BAN_DURATION_MINUTES,
)

from database.queries.user_queries import (
    get_expired_temp_bans,
    remove_temp_ban,
)

from database.queries.subscription_queries import (
    get_expired_subscriptions,
    deactivate_subscription,
)

logger = logging.getLogger(__name__)


class Scheduler:
    """
    Background scheduler for cleanup jobs
    """

    def __init__(self):
        self.tasks = []

    async def start(self):
        """
        Start all background jobs
        """
        logger.info("Scheduler started")

        self.tasks.append(asyncio.create_task(self._temp_ban_cleanup()))
        self.tasks.append(asyncio.create_task(self._subscription_cleanup()))

    async def stop(self):
        """
        Stop all background jobs
        """
        for task in self.tasks:
            task.cancel()

        logger.info("Scheduler stopped")

    async def _temp_ban_cleanup(self):
        """
        Auto remove expired temporary bans
        """
        if not AUTO_TEMP_BAN:
            return

        while True:
            try:
                expired_users = await get_expired_temp_bans()
                for user in expired_users:
                    await remove_temp_ban(user.user_id)
                    logger.info(f"Temp ban removed: {user.user_id}")

            except Exception as e:
                logger.error(f"Temp ban cleanup error: {e}")

            await asyncio.sleep(60)

    async def _subscription_cleanup(self):
        """
        Disable expired subscriptions
        """
        while True:
            try:
                expired = await get_expired_subscriptions()
                for sub in expired:
                    await deactivate_subscription(sub.user_id)
                    logger.info(f"Subscription expired: {sub.user_id}")

            except Exception as e:
                logger.error(f"Subscription cleanup error: {e}")

            await asyncio.sleep(300)
