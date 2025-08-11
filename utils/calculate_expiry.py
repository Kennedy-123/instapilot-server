# utils/token_utils.py
from datetime import datetime, timezone, timedelta

def calculate_expiry(expires_in: int):
    """
    Convert Facebook's expires_in seconds into a UTC datetime.
    
    :param expires_in: Number of seconds until expiry
    :return: UTC datetime object for expiry or None if invalid
    """
    if not expires_in or not isinstance(expires_in, (int, float)):
        return None
    return datetime.now(timezone.utc) + timedelta(seconds=expires_in)
