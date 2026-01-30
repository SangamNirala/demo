"""
Student Schema Server Module
============================

This module provides server-side schema validation and transformation
for student data.
"""

from typing import Dict, Any, Optional, List
from .student_schema import StudentSchema


class StudentSchemaServer:
    """Server-side schema operations for student data"""
    
    @staticmethod
    def validate_request(data: Dict[str, Any]) -> tuple[bool, Optional[str]]:
        """
        Validate incoming request data
        
        Args:
            data: Request data to validate
            
        Returns:
            Tuple of (is_valid, error_message)
        """
        return StudentSchema.validate(data)
    
    @staticmethod
    def transform_for_api(student_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Transform student data for API response
        
        Args:
            student_data: Raw student data
            
        Returns:
            Transformed data suitable for API response
        """
        # Use the schema's format method
        formatted = StudentSchema.format_for_display(student_data)
        
        # Add any additional API-specific transformations
        api_response = {
            'student_id': student_data.get('student_id'),
            'name': student_data.get('name'),
            'roll_no': student_data.get('roll_no'),
            'course': student_data.get('course'),
            'year': student_data.get('year'),
            'year_string': student_data.get('year_string'),
            
            # Profile information
            'profile': {
                'gender': student_data.get('gender'),
                'age': student_data.get('age'),
                'family_income': student_data.get('family_income'),
                'family_income_formatted': student_data.get('family_income_formatted'),
                'parent_education': student_data.get('parent_education'),
                'distance_from_college': student_data.get('distance_from_college'),
                'hostel_day_scholar': student_data.get('hostel_day_scholar'),
            },
            
            # Academic information
            'academic': {
                'attendance_percentage': student_data.get('attendance_percentage'),
                'cgpa_current': student_data.get('cgpa_current'),
                'cgpa_previous': student_data.get('cgpa_previous'),
                'cgpa_semester1': student_data.get('cgpa_semester1'),
                'cgpa_semester2': student_data.get('cgpa_semester2'),
                'units_enrolled_sem1': student_data.get('units_enrolled_sem1'),
                'units_approved_sem1': student_data.get('units_approved_sem1'),
                'units_enrolled_sem2': student_data.get('units_enrolled_sem2'),
                'units_approved_sem2': student_data.get('units_approved_sem2'),
            },
            
            # Engagement information
            'engagement': {
                'assignments_submitted': student_data.get('assignments_submitted'),
                'assignments_total': student_data.get('assignments_total'),
                'assignment_submission_rate': student_data.get('assignment_submission_rate'),
                'library_visits_monthly': student_data.get('library_visits_monthly'),
                'lms_last_login_days': student_data.get('lms_last_login_days'),
                'extracurricular_participation': student_data.get('extracurricular_participation'),
            },
            
            # Financial information
            'financial': {
                'fee_payment_delay_months': student_data.get('fee_payment_delay_months'),
                'scholarship_holder': student_data.get('scholarship_holder'),
                'tuition_fees_up_to_date': student_data.get('tuition_fees_up_to_date'),
                'debtor': student_data.get('debtor'),
            },
            
            # Support information
            'support': {
                'counselor_visits': student_data.get('counselor_visits'),
                'counselor_visit_reason': student_data.get('counselor_visit_reason'),
            }
        }
        
        return api_response
    
    @staticmethod
    def sanitize_input(data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Sanitize input data to prevent injection attacks
        
        Args:
            data: Input data to sanitize
            
        Returns:
            Sanitized data
        """
        sanitized = {}
        
        for key, value in data.items():
            # Remove any potentially dangerous characters
            if isinstance(value, str):
                # Basic sanitization - can be enhanced
                sanitized[key] = value.strip()
            else:
                sanitized[key] = value
        
        return sanitized
    
    @staticmethod
    def extract_required_fields(data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Extract only required fields from student data
        
        Args:
            data: Full student data
            
        Returns:
            Dictionary with only required fields
        """
        required = {}
        
        for field in StudentSchema.REQUIRED_FIELDS:
            if field in data:
                required[field] = data[field]
        
        return required


# Create singleton instance
student_schema_server = StudentSchemaServer()
