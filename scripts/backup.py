# scripts/backup.py

import os
import datetime
import subprocess
from config import DATABASE_URL

BACKUP_DIR = "backups"

def create_backup_dir():
    if not os.path.exists(BACKUP_DIR):
        os.makedirs(BACKUP_DIR)
        print(f"Created backup directory: {BACKUP_DIR}")


def backup_mongodb():
    """
    Creates a timestamped backup of the MongoDB database.
    """
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_path = os.path.join(BACKUP_DIR, f"mongo_backup_{timestamp}")

    os.makedirs(backup_path, exist_ok=True)

    # Assuming DATABASE_URL has format: mongodb+srv://user:pass@host/dbname
    # We extract dbname for mongodump
    db_name = DATABASE_URL.rsplit("/", 1)[-1].split("?")[0]

    cmd = f"mongodump --uri='{DATABASE_URL}' --db {db_name} --out {backup_path}"
    print(f"Running backup: {cmd}")
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)

    if result.returncode == 0:
        print(f"Backup successful! Stored in: {backup_path}")
    else:
        print(f"Backup failed: {result.stderr}")


if __name__ == "__main__":
    create_backup_dir()
    backup_mongodb()
