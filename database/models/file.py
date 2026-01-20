# database/models/file.py

from datetime import datetime
from typing import Optional

class File:
    def __init__(
        self,
        file_id: str,
        user_id: int,
        file_name: str,
        file_size: int,
        file_hash: str,
        telegram_file_id: str,
        mime_type: Optional[str] = None,
        created_at: Optional[datetime] = None,
        updated_at: Optional[datetime] = None,
        is_deleted: bool = False
    ):
        self.file_id = file_id
        self.user_id = user_id
        self.file_name = file_name
        self.file_size = file_size
        self.file_hash = file_hash
        self.telegram_file_id = telegram_file_id
        self.mime_type = mime_type
        self.created_at = created_at or datetime.utcnow()
        self.updated_at = updated_at or datetime.utcnow()
        self.is_deleted = is_deleted

        # Human-readable size, calculated for UI/display
        self.size_readable = self._human_readable_size(file_size)

    def _human_readable_size(self, size: int) -> str:
        """
        Convert bytes into human-readable format
        """
        for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
            if size < 1024:
                return f"{size:.2f} {unit}"
            size /= 1024
        return f"{size:.2f} PB"

    def mark_deleted(self, soft: bool = True):
        """
        Soft delete (mark flag) or hard delete (can be handled in DB layer)
        """
        if soft:
            self.is_deleted = True
        else:
            # Hard delete logic can be added at DB/storage level
            pass

    def update_name(self, new_name: str):
        self.file_name = new_name
        self.updated_at = datetime.utcnow()
