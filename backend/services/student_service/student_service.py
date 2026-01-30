"""
Student Service Module
======================

This module provides business logic for student-related operations.
"""

import json
import os
from typing import Dict, List, Optional


class StudentService:
    """Service class for student operations"""
    
    def __init__(self, db_path: Optional[str] = None):
        """Initialize student service"""
        if db_path is None:
            db_path = os.path.join(
                os.path.dirname(__file__), 
                '..', '..', 
                'database', 
                'students_data.json'
            )
        self.db_path = db_path
        self._students_cache = None
    
    def load_students(self) -> Dict:
        """Load student data from JSON file"""
        try:
            with open(self.db_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                self._students_cache = data
                return data
        except FileNotFoundError:
            return {'students': {}, 'metadata': {}}
        except json.JSONDecodeError:
            return {'students': {}, 'metadata': {}}
    
    def get_student_by_roll_no(self, roll_no: str) -> Optional[Dict]:
        """Get student by roll number"""
        students_data = self.load_students()
        students = students_data.get('students', {})
        return students.get(roll_no)
    
    def get_all_students(self) -> List[Dict]:
        """Get all students"""
        students_data = self.load_students()
        students = students_data.get('students', {})
        
        student_list = [
            {
                'roll_no': roll_no,
                'name': data.get('name', 'Unknown'),
                'course': data.get('course', 'N/A'),
                'year': data.get('year', 'N/A'),
                'year_string': data.get('year_string', 'N/A')
            }
            for roll_no, data in students.items()
        ]
        
        return student_list
    
    def search_students(self, query: str) -> List[Dict]:
        """Search students by name or roll number"""
        all_students = self.get_all_students()
        query_lower = query.lower()
        
        return [
            student for student in all_students
            if query_lower in student['name'].lower() or 
               query_lower in student['roll_no'].lower()
        ]
