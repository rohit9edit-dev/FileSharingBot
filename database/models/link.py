# database/models/link.py

from datetime import datetime, timedelta
from typing import Optional
import uuid

from config import DEFAULT_LINK_EXPIRY_MINUTES, MAX_DOWNLOADS_PER_LINK_FREE, MAX_DOWNLOADS_PER_LINK_PAID

class Link:
    def __init__(
        self,
        link_id: Optional[str] = None,
        file_id: Optional[str] = None,
        user_id: Optional[int] = None,
        max_downloads: Optional[int] = None,
        expiry_minutes: Optional[int] = None,
        one_time: bool = False,
        password_protected: bool = False,
        password: Optional[str] = None,
        created_at: Optional[datetime] = None
    ):
        self.link_id = link_id or str(uuid.uuid4())
        self.file_id = file_id
        self.user_id = user_id
        self.one_time = one_time
        self.password_protected = password_protected
        self.password = password
        self.created_at = created_at or datetime.utcnow()

        # Expiry
        self.expiry_minutes = expiry_minutes if expiry_minutes is not None else DEFAULT_LINK_EXPIRY_MINUTES
        self.expires_at = (
            self.created_at + timedelta(minutes=self.expiry_minutes)
            if self.expiry_minutes > 0
            else None  # None = permanent link
        )

        # Max downloads
        self.max_downloads = max_downloads if max_downloads is not None else MAX_DOWNLOADS_PER_LINK_FREE

        # Track downloads
        self.download_count = 0
        self.is_active = True

    def increment_download(self):
        if not self.is_active:
            return False

        self.download_count += 1

        # Check if max downloads reached
        if self.max_downloads > 0 and self.download_count >= self.max_downloads:
            self.is_active = False

        return True

    def check_expired(self):
        if self.expires_at and datetime.utcnow() > self.expires_at:
            self.is_active = False
        return not self.is_active

    def verify_password(self, input_password: str) -> bool:
        if not self.password_protected:
            return True
        return self.password == input_password

    def deactivate(self):
        self.is_active = False
