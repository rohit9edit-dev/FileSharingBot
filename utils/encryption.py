# utils/encryption.py

from cryptography.fernet import Fernet

# Generate a key once and store it safely; yaha example ke liye hardcoded
SECRET_KEY = Fernet.generate_key()
cipher = Fernet(SECRET_KEY)


def encrypt(data: str) -> str:
    """
    Encrypt a string and return as base64 encoded string
    """
    return cipher.encrypt(data.encode()).decode()


def decrypt(token: str) -> str:
    """
    Decrypt the encrypted string
    """
    return cipher.decrypt(token.encode()).decode()
