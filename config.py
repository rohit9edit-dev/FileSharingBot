# config.py
import os

# =========================================================
# BASIC APP INFO
# =========================================================
APP_NAME = "AdvancedFileSharingBot"
ENV = os.getenv("ENV", "production")
TIMEZONE = "Asia/Kolkata"

# =========================================================
# TELEGRAM CREDENTIALS
# =========================================================
API_ID = int(os.getenv("API_ID", "35136171"))
API_HASH = os.getenv("API_HASH", "2f4aa10016925f92bc74be7336c22502")
BOT_TOKEN = os.getenv("BOT_TOKEN", "8134715094:AAGpXFLIIrpFXZp8-cewJZd2T-ENGDwrZ6A")

# =========================================================
# OWNER / ADMINS
# =========================================================
OWNER_ID = int(os.getenv("OWNER_ID", "6774993771"))
ADMIN_IDS = list(map(int, os.getenv("ADMIN_IDS", "6774993771").split()))

# =========================================================
# FORCE SUBSCRIPTION (2 CHANNELS)
# =========================================================
FORCE_SUB_ENABLED = True
FORCE_SUB_CHANNELS = [
    int(os.getenv("FORCE_SUB_CHANNEL_1", "-1003373869483")),
    int(os.getenv("FORCE_SUB_CHANNEL_2", "-1003328487422")),
]
FORCE_SUB_MESSAGE = "🚫 Access denied!\n\nJoin 👇"

# =========================================================
# DATABASE & CACHE
# =========================================================
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "mongodb+srv://bigoleknobs_db_user:R6JXCZnbNSdNyfql@cluster0.drerrj4.mongodb.net/?appName=Cluster0"
)
REDIS_URL = os.getenv(
    "REDIS_URL",
    "redis://localhost:6379/0"
)

# =========================================================
# STORAGE (PRIVATE CHANNEL BACKEND)
# =========================================================
PRIVATE_STORAGE_CHANNELS = list(
    map(
        int,
        os.getenv(
            "PRIVATE_STORAGE_CHANNELS",
            "-1003621538224,-1003625716110"
        ).split(",")
    )
)

# =========================================================
# USER LIMITS
# =========================================================
MAX_FILE_SIZE_FREE = 10 * 1024 * 1024 * 1024      # 10 GB
MAX_FILE_SIZE_PAID = 50 * 1024 * 1024 * 1024     # 50 GB

FREE_DAILY_UPLOAD_LIMIT = 50
FREE_DAILY_DOWNLOAD_LIMIT = 100

PAID_DAILY_UPLOAD_LIMIT = 10000
PAID_DAILY_DOWNLOAD_LIMIT = 50000

# =========================================================
# SECURITY & RATE LIMIT
# =========================================================
RATE_LIMIT_ENABLED = True
RATE_LIMIT_PER_MINUTE = 20

CAPTCHA_ON_SUSPICIOUS = True
AUTO_TEMP_BAN = True
TEMP_BAN_DURATION_MINUTES = 60

# =========================================================
# LINK RULES
# =========================================================
DEFAULT_LINK_EXPIRY_MINUTES = 0        # 0 = permanent
MAX_DOWNLOADS_PER_LINK_FREE = 10
MAX_DOWNLOADS_PER_LINK_PAID = 0        # unlimited

# =========================================================
# PAYMENT SYSTEM (QR BASED)
# =========================================================
PAYMENTS_ENABLED = True
UPI_ID = "BHARATPE9I0L7J2X9O893091@yesbankltd"
PAYEE_NAME = "Rohit Kumar"
PAYMENT_QR_PATH = "assets/payment_qr.png"

# Subscription plans
PLANS = {
    "basic": {
        "price": 49,
        "duration_days": 20
    },
    "power": {
        "price": 149,
        "duration_days": 70
    },
    "business": {
        "price": 399,
        "duration_days": 180   # 6 months
    },
    "lifetime": {
        "price": 999,
        "duration_days": 365
    }
}

# =========================================================
# FEATURE FLAGS (CONTROLLED BY SUBSCRIPTION)
# =========================================================
FEATURE_PASSWORD_LINK = True
FEATURE_TIME_LIMIT_LINK = True
FEATURE_ONE_TIME_LINK = True

FEATURE_DEVICE_LOCK = True
FEATURE_IP_LOCK = True
FEATURE_VAULT = True
FEATURE_SELF_DESTRUCT = True
FEATURE_API_ACCESS = True

# =========================================================
# SUPPORT / MISC
# =========================================================
SUPPORT_CHAT = os.getenv("SUPPORT_CHAT", "https://t.me/suppme1")
