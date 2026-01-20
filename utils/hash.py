# utils/hash.py

import hashlib

def sha256(data: bytes) -> str:
    """
    Return SHA-256 hash of the input bytes.
    """
    return hashlib.sha256(data).hexdigest()


def md5(data: bytes) -> str:
    """
    Return MD5 hash of the input bytes.
    (Mostly for quick checks, not secure)
    """
    return hashlib.md5(data).hexdigest()
