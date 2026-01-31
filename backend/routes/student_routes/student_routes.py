"""
Student Routes Module
====================

This module defines routes for student-related operations.
"""

from flask import Blueprint, jsonify, request
import json
import os

# Create blueprint
student_bp = Blueprint('student', __name__)

def load_students():
    """Load student data from JSON file"""
    db_path = os.path.join(os.path.dirname(__file__), '..', '..', 'database', 'students_data.json')
    try:
        with open(db_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            return data
    except FileNotFoundError:
        return {'students': {}}
    except json.JSONDecodeError:
        return {'students': {}}

@student_bp.route('/<roll_no>', methods=['GET'])
def get_student(roll_no):
    """
    Get student data by roll number
    
    Args:
        roll_no: Student roll number
        
    Returns:
        JSON with student data
    """
    try:
        students_data = load_students()
        students = students_data.get('students', {})
        
        if roll_no in students:
            return jsonify(students[roll_no]), 200
        else:
            return jsonify({'error': 'Student not found'}), 404
            
    except Exception as e:
        return jsonify({'error': f'Server error: {str(e)}'}), 500

@student_bp.route('', methods=['GET'])
def list_students():
    """
    List all students
    
    Returns:
        JSON with list of all students
    """
    try:
        students_data = load_students()
        students = students_data.get('students', {})
        
        student_list = [
            {
                'roll_no': roll_no,
                'name': data.get('name', 'Unknown'),
                'course': data.get('course', 'N/A'),
                'year': data.get('year', 'N/A')
            }
            for roll_no, data in students.items()
        ]
        
        return jsonify({
            'total': len(student_list),
            'students': student_list
        }), 200
        
    except Exception as e:
        return jsonify({'error': f'Server error: {str(e)}'}), 500
