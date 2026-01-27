from datetime import datetime, timedelta
import hashlib
import secrets
from typing import Any, Dict

def hash_password(password: str) -> str:
    """Hash password using SHA256"""
    return hashlib.sha256(password.encode()).hexdigest()

def verify_password(password: str, hashed: str) -> bool:
    """Verify password against hash"""
    return hash_password(password) == hashed

def generate_token(length: int = 32) -> str:
    """Generate random token"""
    return secrets.token_urlsafe(length)

def format_datetime(dt: datetime) -> str:
    """Format datetime to ISO string"""
    return dt.isoformat()

def parse_datetime(dt_string: str) -> datetime:
    """Parse ISO datetime string"""
    return datetime.fromisoformat(dt_string)

def paginate(items: list, page: int = 1, page_size: int = 10) -> Dict[str, Any]:
    """Paginate a list of items"""
    start = (page - 1) * page_size
    end = start + page_size
    
    return {
        "items": items[start:end],
        "total": len(items),
        "page": page,
        "page_size": page_size,
        "total_pages": (len(items) + page_size - 1) // page_size
    }

def calculate_age(birth_date: datetime) -> int:
    """Calculate age from birth date"""
    today = datetime.now()
    return today.year - birth_date.year - (
        (today.month, today.day) < (birth_date.month, birth_date.day)
    )
