# utils/validators.py

import re

def is_valid_upi(upi_id: str) -> bool:
    """
    Check if UPI ID is valid
    Example: user@bank
    """
    pattern = r'^[\w.-]{2,256}@[a-zA-Z]{2,64}$'
    return bool(re.match(pattern, upi_id))


def is_valid_url(url: str) -> bool:
    """
    Check if URL is valid
    """
    pattern = r'^(https?://)?[\w.-]+\.[a-zA-Z]{2,6}(/[\w.-]*)*/?$'
    return bool(re.match(pattern, url))


def is_valid_file_size(size: int, max_size: int) -> bool:
    """
    Check if file size is within allowed limit
    """
    return 0 < size <= max_size


def is_non_empty_string(s: str) -> bool:
    """
    Check if string is not empty and not just spaces
    """
    return bool(s and s.strip())
