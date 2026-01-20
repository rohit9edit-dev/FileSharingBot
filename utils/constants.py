# utils/constants.py

# =========================================================
# Status / Types
# =========================================================
FILE_STATUS_ACTIVE = "active"
FILE_STATUS_DELETED = "deleted"

USER_TYPE_FREE = "free"
USER_TYPE_PAID = "paid"

LINK_TYPE_DEFAULT = "default"
LINK_TYPE_ONE_TIME = "one_time"
LINK_TYPE_TIME_LIMIT = "time_limit"

# =========================================================
# Default messages
# =========================================================
MSG_ACCESS_DENIED = "🚫 Access denied!\n\nPlease join the required channels to use the bot."
MSG_FILE_UPLOADED = "✅ File uploaded successfully!"
MSG_FILE_EXISTS = "⚠️ This file already exists."
MSG_FILE_DELETED = "🗑️ File deleted successfully."
MSG_FILE_NOT_FOUND = "❌ File not found."

# =========================================================
# Misc / Limits
# =========================================================
DEFAULT_DAILY_UPLOAD_LIMIT_FREE = 50
DEFAULT_DAILY_DOWNLOAD_LIMIT_FREE = 100

DEFAULT_DAILY_UPLOAD_LIMIT_PAID = 10000
DEFAULT_DAILY_DOWNLOAD_LIMIT_PAID = 50000

MAX_FILE_SIZE_FREE = 10 * 1024 * 1024 * 1024      # 10 GB
MAX_FILE_SIZE_PAID = 50 * 1024 * 1024 * 1024      # 50 GB
