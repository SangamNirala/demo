"""
Email Generation Module
=======================

AI-powered email generation for student outreach.
"""

from .email_service import email_service
from .email_routes import email_bp

__all__ = ['email_service', 'email_bp']
