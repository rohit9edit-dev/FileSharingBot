# database/models/access_log.py

from datetime import datetime
from typing import Optional

class AccessLog:
    def __init__(
        self,
        log_id: Optional[str] = None,
        user_id: Optional[int] = None,
        file_id: Optional[str] = None,
        action: str = "download",  # or "upload"
        ip_address: Optional[str] = None,
        user_agent: Optional[str] = None,
        timestamp: Optional[datetime] = None
    ):
        import uuid
        self.log_id = log_id or str(uuid.uuid4())
        self.user_id = user_id
        self.file_id = file_id
        self.action = action
        self.ip_address = ip_address
        self.user_agent = user_agent
        self.timestamp = timestamp or datetime.utcnow()

    def to_dict(self):
        return {
            "log_id": self.log_id,
            "user_id": self.user_id,
            "file_id": self.file_id,
            "action": self.action,
            "ip_address": self.ip_address,
            "user_agent": self.user_agent,
            "timestamp": self.timestamp.isoformat(),
        }
