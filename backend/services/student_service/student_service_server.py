"""
Student Service Server Module
==============================

This module provides server-side logic for student service operations.
It acts as a bridge between routes and the core service logic.
"""

from typing import Dict, List, Optional
from .student_service import StudentService


class StudentServiceServer:
    """Server-side wrapper for student service"""
    
    def __init__(self):
        """Initialize service server"""
        self.service = StudentService()
    
    def process_student_request(self, roll_no: str) -> Dict:
        """
        Process student data request with additional server-side logic
        
        Args:
            roll_no: Student roll number
            
        Returns:
            Processed student data
        """
        student = self.service.get_student_by_roll_no(roll_no)
        
        if student is None:
            return None
        
        # Add any server-side processing here
        # For example: logging, caching, additional data enrichment
        
        return student
    
    def process_students_list_request(self, filters: Optional[Dict] = None) -> List[Dict]:
        """
        Process students list request with filtering
        
        Args:
            filters: Optional filters to apply
            
        Returns:
            List of students
        """
        students = self.service.get_all_students()
        
        # Apply filters if provided
        if filters:
            # Example: filter by course, year, etc.
            if 'course' in filters:
                students = [s for s in students if s.get('course') == filters['course']]
            if 'year' in filters:
                students = [s for s in students if s.get('year') == filters['year']]
        
        return students
    
    def validate_and_process(self, student_data: Dict) -> tuple[bool, Optional[str], Optional[Dict]]:
        """
        Validate and process student data
        
        Args:
            student_data: Student data to validate
            
        Returns:
            Tuple of (is_valid, error_message, processed_data)
        """
        # Validation logic
        required_fields = ['student_id', 'name', 'roll_no']
        
        for field in required_fields:
            if field not in student_data:
                return False, f"Missing required field: {field}", None
        
        # Processing logic
        processed_data = student_data.copy()
        
        # Add any transformations here
        
        return True, None, processed_data


# Create singleton instance
student_service_server = StudentServiceServer()
