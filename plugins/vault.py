# plugins/vault.py

from config import FEATURE_VAULT
from services.file_service import get_file_by_id, delete_file
from typing import Optional

class VaultPlugin:
    """
    Vault plugin for storing files securely.
    """

    def __init__(self):
        self.enabled = FEATURE_VAULT

    async def store_file(self, user_id: int, file_id: str):
        """
        Store file in vault if feature enabled.
        """
        if not self.enabled:
            return None, "Vault feature is disabled."
        
        # Fetch file details
        file_record = await get_file_by_id(file_id)
        if not file_record:
            return None, "File not found."
        
        # Here you can add logic to mark file as 'vaulted' in DB
        file_record.vaulted = True
        # Save/update DB logic goes here

        return file_record, "File moved to Vault successfully."

    async def remove_file(self, user_id: int, file_id: str):
        """
        Remove file from vault.
        """
        if not self.enabled:
            return None, "Vault feature is disabled."

        file_record = await get_file_by_id(file_id)
        if not file_record or not getattr(file_record, "vaulted", False):
            return None, "File not found in Vault."
        
        # Delete file permanently or move out of vault
        await delete_file(file_id, soft=False)
        return True, "File removed from Vault successfully."
