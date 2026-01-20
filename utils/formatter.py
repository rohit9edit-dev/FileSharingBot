# utils/formatter.py

from datetime import datetime

def human_readable_size(size_bytes: int) -> str:
    """
    Convert file size in bytes to human readable format
    """
    if size_bytes == 0:
        return "0B"
    units = ["B", "KB", "MB", "GB", "TB", "PB"]
    i = 0
    while size_bytes >= 1024 and i < len(units)-1:
        size_bytes /= 1024.0
        i += 1
    return f"{size_bytes:.2f} {units[i]}"


def format_datetime(dt: datetime, fmt: str = "%Y-%m-%d %H:%M:%S") -> str:
    """
    Convert datetime object to formatted string
    """
    if dt is None:
        return ""
    return dt.strftime(fmt)


def truncate_string(s: str, max_len: int = 30) -> str:
    """
    Truncate string with ellipsis if longer than max_len
    """
    if not s:
        return ""
    return s if len(s) <= max_len else s[:max_len-3] + "..."
