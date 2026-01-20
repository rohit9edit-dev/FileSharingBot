# plugins/self_destruct.py

import asyncio
from datetime import datetime, timedelta
from config import FEATURE_SELF_DESTRUCT
from services.file_service import delete_file, get_file_by_id

class SelfDestructPlugin:
    """
    Self-destruct plugin: automatically deletes files after a time limit.
    """

    def __init__(self):
        self.enabled = FEATURE_SELF_DESTRUCT

    async def schedule_destruction(self, file_id: str, destroy_after_seconds: int):
        """
        Schedule file for self-destruction after given seconds.
        """
        if not self.enabled:
            return False, "Self-destruct feature is disabled."

        # Fetch file details
        file_record = await get_file_by_id(file_id)
        if not file_record:
            return False, "File not found."

        # Calculate destruction time
        destruction_time = datetime.utcnow() + timedelta(seconds=destroy_after_seconds)
        file_record.self_destruct_time = destruction_time
        # Save/update DB logic if needed

        # Schedule async deletion
        asyncio.create_task(self._destroy_after(file_id, destroy_after_seconds))
        return True, f"File will self-destruct in {destroy_after_seconds} seconds."

    async def _destroy_after(self, file_id: str, delay_seconds: int):
        """
        Async wait and delete the file
        """
        await asyncio.sleep(delay_seconds)
        await delete_file(file_id, soft=False)
