# database/models/audit.py

from datetime import datetime

class AuditLog:
    def __init__(
        self,
        user_id: int,
        action: str,
        details: str = "",
        created_at: datetime = None
    ):
        self.user_id = user_id        # kaun kar raha hai action
        self.action = action          # action type, eg: "UPLOAD", "DOWNLOAD", "PAYMENT"
        self.details = details        # optional extra info
        self.created_at = created_at or datetime.utcnow()

    def to_dict(self):
        return {
            "user_id": self.user_id,
            "action": self.action,
            "details": self.details,
            "created_at": self.created_at.isoformat()
        }
