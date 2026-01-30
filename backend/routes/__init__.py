"""
Routes Package
==============

This package contains all API route definitions for the application.
"""

from .student_routes import student_bp
from .prediction_routes import prediction_bp

__all__ = ['student_bp', 'prediction_bp']
