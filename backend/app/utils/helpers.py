"""Utility helper functions."""

from typing import Dict, Any
from datetime import datetime


def format_datetime(dt: datetime) -> str:
    """Format datetime for JSON response."""
    return dt.isoformat()


def round_decimal(value: float, decimals: int = 2) -> float:
    """Round a float to specified decimal places."""
    return round(value, decimals)


def sanitize_user_id(user_id: str) -> str:
    """Sanitize user ID to prevent injection."""
    # Simple sanitization - remove any non-alphanumeric characters except dash and underscore
    import re
    return re.sub(r'[^a-zA-Z0-9_\-]', '', user_id)
