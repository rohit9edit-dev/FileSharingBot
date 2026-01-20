# cache/keys.py

# =========================================================
# USER KEYS
# =========================================================
USER_PREFIX = "user:"               # user:<user_id> -> store user info
USER_UPLOAD_COUNT = "user:{user_id}:uploads"  # daily uploads count
USER_DOWNLOAD_COUNT = "user:{user_id}:downloads"  # daily downloads count
USER_SUBSCRIPTION = "user:{user_id}:subscription"  # subscription info

# =========================================================
# FILE KEYS
# =========================================================
FILE_PREFIX = "file:"               # file:<file_id> -> file metadata
FILE_HASH = "file:hash:{hash}"     # hash -> file_id (for duplicate check)
FILE_DOWNLOAD_COUNT = "file:{file_id}:downloads"  # track downloads per file

# =========================================================
# LINK KEYS
# =========================================================
LINK_PREFIX = "link:"               # link:<link_id> -> link metadata
LINK_DOWNLOAD_COUNT = "link:{link_id}:downloads"

# =========================================================
# RATE LIMIT KEYS
# =========================================================
RATE_LIMIT_PREFIX = "rate:{user_id}"   # track requests per minute

# =========================================================
# CAPTCHA / TEMP BAN
# =========================================================
TEMP_BAN_PREFIX = "ban:{user_id}"
CAPTCHA_PREFIX = "captcha:{user_id}"

# =========================================================
# OTHER KEYS
# =========================================================
VAULT_PREFIX = "vault:{user_id}"     # if vault feature is enabled
