"""
Student Schema Module
=====================

This module defines data schemas for student-related operations.
"""

from typing import Optional, Dict, Any


class StudentSchema:
    """Schema for student data validation"""
    
    REQUIRED_FIELDS = [
        'student_id',
        'name',
        'roll_no',
        'course',
        'year'
    ]
    
    OPTIONAL_FIELDS = [
        'gender',
        'age',
        'family_income',
        'parent_education',
        'distance_from_college',
        'hostel_day_scholar',
        'attendance_percentage',
        'cgpa_current',
        'cgpa_previous',
        'cgpa_semester1',
        'cgpa_semester2',
        'units_enrolled_sem1',
        'units_approved_sem1',
        'units_enrolled_sem2',
        'units_approved_sem2',
        'assignments_submitted',
        'assignments_total',
        'assignment_submission_rate',
        'library_visits_monthly',
        'lms_last_login_days',
        'extracurricular_participation',
        'fee_payment_delay_months',
        'scholarship_holder',
        'tuition_fees_up_to_date',
        'debtor',
        'counselor_visits',
        'counselor_visit_reason'
    ]
    
    @staticmethod
    def validate(data: Dict[str, Any]) -> tuple[bool, Optional[str]]:
        """
        Validate student data
        
        Args:
            data: Student data dictionary
            
        Returns:
            Tuple of (is_valid, error_message)
        """
        # Check required fields
        for field in StudentSchema.REQUIRED_FIELDS:
            if field not in data:
                return False, f"Missing required field: {field}"
        
        # Validate data types
        if not isinstance(data.get('name'), str):
            return False, "Name must be a string"
        
        if not isinstance(data.get('roll_no'), str):
            return False, "Roll number must be a string"
        
        # All validations passed
        return True, None
    
    @staticmethod
    def format_for_display(data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Format student data for display
        
        Args:
            data: Raw student data
            
        Returns:
            Formatted student data
        """
        return {
            'student_id': data.get('student_id', 'N/A'),
            'name': data.get('name', 'Unknown'),
            'roll_no': data.get('roll_no', 'N/A'),
            'course': data.get('course', 'N/A'),
            'year': data.get('year_string', f"Year {data.get('year', 'N/A')}"),
            'gender': data.get('gender', 'N/A'),
            'age': data.get('age', 'N/A'),
            'family_income': data.get('family_income_formatted', f"₹{data.get('family_income', 0):,}"),
            'parent_education': data.get('parent_education', 'N/A'),
            'distance_from_college': f"{data.get('distance_from_college', 0)} km",
            'hostel_day_scholar': data.get('hostel_day_scholar', 'N/A'),
            'attendance_percentage': f"{data.get('attendance_percentage', 0)}%",
            'cgpa_current': data.get('cgpa_current', 'N/A'),
            'cgpa_previous': data.get('cgpa_previous', 'N/A'),
            'assignments_submitted': f"{data.get('assignments_submitted', 0)}/{data.get('assignments_total', 10)}",
            'library_visits': data.get('library_visits_monthly', 0),
            'lms_last_login': f"{data.get('lms_last_login_days', 0)} days ago",
            'extracurricular': 'Yes' if data.get('extracurricular_participation') else 'No',
            'fee_status': 'Delayed' if data.get('fee_payment_delay_months', 0) > 0 else 'Up to date',
            'counselor_visits': data.get('counselor_visits', 0)
        }
