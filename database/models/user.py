# database/models/user.py

from datetime import datetime
from typing import Optional

class User:
    def __init__(
        self,
        user_id: int,
        username: Optional[str] = None,
        full_name: Optional[str] = None,
        is_admin: bool = False,
        plan: str = "free",  # free / basic / power / business / lifetime
        plan_expiry: Optional[datetime] = None,
        daily_upload: int = 0,
        daily_download: int = 0,
        created_at: Optional[datetime] = None,
        updated_at: Optional[datetime] = None
    ):
        self.user_id = user_id
        self.username = username
        self.full_name = full_name
        self.is_admin = is_admin
        self.plan = plan
        self.plan_expiry = plan_expiry
        self.daily_upload = daily_upload
        self.daily_download = daily_download
        self.created_at = created_at or datetime.utcnow()
        self.updated_at = updated_at or datetime.utcnow()

    def reset_daily_limits(self, free_limits, paid_limits):
        """
        Daily upload/download counters reset at midnight
        """
        if self.plan == "free":
            self.daily_upload = 0
            self.daily_download = 0
            self.max_upload = free_limits["upload"]
            self.max_download = free_limits["download"]
        else:
            self.daily_upload = 0
            self.daily_download = 0
            self.max_upload = paid_limits["upload"]
            self.max_download = paid_limits["download"]

    def is_plan_active(self) -> bool:
        """
        Check if current plan is still active
        """
        if self.plan == "free":
            return True
        if self.plan_expiry is None:
            return True  # lifetime plan
        return datetime.utcnow() < self.plan_expiry

    def upgrade_plan(self, new_plan: str, expiry: Optional[datetime] = None):
        """
        Upgrade user's plan
        """
        self.plan = new_plan
        self.plan_expiry = expiry
        self.reset_daily_limits(
            free_limits={"upload": 50, "download": 100},   # same as config.py
            paid_limits={"upload": 10000, "download": 50000}  # same as config.py
        )
