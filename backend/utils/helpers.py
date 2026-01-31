"""
Helper Utilities Module
=======================

This module contains helper functions used across the application.
"""

import json
import os
from typing import Dict, Any, Optional
from datetime import datetime


def load_json_file(file_path: str) -> Dict:
    """
    Load JSON file safely
    
    Args:
        file_path: Path to JSON file
        
    Returns:
        Dictionary with JSON data or empty dict on error
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"Warning: File not found - {file_path}")
        return {}
    except json.JSONDecodeError:
        print(f"Warning: Invalid JSON in file - {file_path}")
        return {}
    except Exception as e:
        print(f"Error loading JSON file: {e}")
        return {}


def save_json_file(file_path: str, data: Dict) -> bool:
    """
    Save data to JSON file
    
    Args:
        file_path: Path to JSON file
        data: Data to save
        
    Returns:
        True if successful, False otherwise
    """
    try:
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        return True
    except Exception as e:
        print(f"Error saving JSON file: {e}")
        return False


def format_currency(amount: float, currency: str = '₹') -> str:
    """
    Format amount as currency
    
    Args:
        amount: Amount to format
        currency: Currency symbol
        
    Returns:
        Formatted currency string
    """
    if amount >= 100000:
        return f"{currency}{amount/100000:.1f} Lakh"
    elif amount >= 1000:
        return f"{currency}{amount/1000:.1f}K"
    else:
        return f"{currency}{amount:,.0f}"


def format_percentage(value: float, decimals: int = 1) -> str:
    """
    Format value as percentage
    
    Args:
        value: Value to format (0-100)
        decimals: Number of decimal places
        
    Returns:
        Formatted percentage string
    """
    return f"{value:.{decimals}f}%"


def calculate_age_from_year(birth_year: int) -> int:
    """
    Calculate age from birth year
    
    Args:
        birth_year: Year of birth
        
    Returns:
        Current age
    """
    current_year = datetime.now().year
    return current_year - birth_year


def safe_get(dictionary: Dict, key: str, default: Any = None) -> Any:
    """
    Safely get value from dictionary
    
    Args:
        dictionary: Dictionary to get value from
        key: Key to look up
        default: Default value if key not found
        
    Returns:
        Value or default
    """
    return dictionary.get(key, default)


def validate_roll_number(roll_no: str) -> bool:
    """
    Validate roll number format
    
    Args:
        roll_no: Roll number to validate
        
    Returns:
        True if valid, False otherwise
    """
    if not roll_no or not isinstance(roll_no, str):
        return False
    
    # Basic validation - can be enhanced based on actual format
    return len(roll_no) >= 4 and any(c.isdigit() for c in roll_no)


def get_risk_color(risk_level: str) -> str:
    """
    Get color code for risk level
    
    Args:
        risk_level: Risk level (HIGH, MEDIUM, LOW)
        
    Returns:
        Color code
    """
    colors = {
        'HIGH': '#dc2626',      # red-600
        'MEDIUM': '#f59e0b',    # amber-500
        'LOW': '#10b981'        # green-500
    }
    return colors.get(risk_level.upper(), '#6b7280')  # gray-500 as default


def get_risk_emoji(risk_level: str) -> str:
    """
    Get emoji for risk level
    
    Args:
        risk_level: Risk level (HIGH, MEDIUM, LOW)
        
    Returns:
        Emoji string
    """
    emojis = {
        'HIGH': '🔴',
        'MEDIUM': '🟡',
        'LOW': '🟢'
    }
    return emojis.get(risk_level.upper(), '⚪')


def truncate_text(text: str, max_length: int = 100, suffix: str = '...') -> str:
    """
    Truncate text to maximum length
    
    Args:
        text: Text to truncate
        max_length: Maximum length
        suffix: Suffix to add if truncated
        
    Returns:
        Truncated text
    """
    if len(text) <= max_length:
        return text
    return text[:max_length - len(suffix)] + suffix


def parse_boolean(value: Any) -> bool:
    """
    Parse various boolean representations
    
    Args:
        value: Value to parse
        
    Returns:
        Boolean value
    """
    if isinstance(value, bool):
        return value
    
    if isinstance(value, str):
        return value.lower() in ['true', 'yes', '1', 'y', 't']
    
    if isinstance(value, (int, float)):
        return value != 0
    
    return False
