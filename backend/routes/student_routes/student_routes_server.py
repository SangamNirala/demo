"""
Student Route Handlers
======================

This module contains handler functions for student routes.
These handlers process requests and return responses.
"""

from flask import jsonify, request
from typing import Dict, Any
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

from services.student_service.student_service import StudentService
from schemas.student_schema.student_schema import StudentSchema


class StudentRouteHandler:
    """Handler class for student routes"""
    
    def __init__(self):
        """Initialize handler with service"""
        self.service = StudentService()
    
    def get_student_handler(self, roll_no: str) -> tuple:
        """
        Handle get student request
        
        Args:
            roll_no: Student roll number
            
        Returns:
            Tuple of (response_data, status_code)
        """
        try:
            student = self.service.get_student_by_roll_no(roll_no)
            
            if student is None:
                return {'error': 'Student not found'}, 404
            
            # Validate student data
            is_valid, error_msg = StudentSchema.validate(student)
            if not is_valid:
                return {'error': f'Invalid student data: {error_msg}'}, 500
            
            return student, 200
            
        except Exception as e:
            return {'error': f'Server error: {str(e)}'}, 500
    
    def list_students_handler(self) -> tuple:
        """
        Handle list students request
        
        Returns:
            Tuple of (response_data, status_code)
        """
        try:
            students = self.service.get_all_students()
            
            return {
                'total': len(students),
                'students': students
            }, 200
            
        except Exception as e:
            return {'error': f'Server error: {str(e)}'}, 500
    
    def search_students_handler(self, query: str) -> tuple:
        """
        Handle search students request
        
        Args:
            query: Search query
            
        Returns:
            Tuple of (response_data, status_code)
        """
        try:
            students = self.service.search_students(query)
            
            return {
                'total': len(students),
                'students': students,
                'query': query
            }, 200
            
        except Exception as e:
            return {'error': f'Server error: {str(e)}'}, 500


# Create singleton instance
student_handler = StudentRouteHandler()
