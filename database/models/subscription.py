# database/models/subscription.py

from datetime import datetime, timedelta
from typing import Optional

class Subscription:
    def __init__(
        self,
        user_id: int,
        plan_name: str,
        start_date: Optional[datetime] = None,
        duration_days: Optional[int] = None,
        is_active: bool = True
    ):
        self.user_id = user_id
        self.plan_name = plan_name
        self.start_date = start_date or datetime.utcnow()
        self.duration_days = duration_days or 0  # 0 = lifetime
        self.is_active = is_active

    @property
    def expiry_date(self) -> Optional[datetime]:
        if self.duration_days == 0:
            return None  # lifetime
        return self.start_date + timedelta(days=self.duration_days)

    def check_active(self) -> bool:
        if not self.is_active:
            return False
        if self.duration_days == 0:
            return True  # lifetime subscription
        return datetime.utcnow() < self.expiry_date

    def to_dict(self):
        return {
            "user_id": self.user_id,
            "plan_name": self.plan_name,
            "start_date": self.start_date.isoformat(),
            "duration_days": self.duration_days,
            "expiry_date": self.expiry_date.isoformat() if self.expiry_date else None,
            "is_active": self.is_active,
        }
