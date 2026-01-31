"""
Schemas Package
===============

This package contains data validation schemas for the application.
"""

from .student_schema import StudentSchema
from .prediction_schema import PredictionSchema

__all__ = ['StudentSchema', 'PredictionSchema']
