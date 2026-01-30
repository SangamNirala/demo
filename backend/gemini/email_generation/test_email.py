"""
Test Email Generation Service
==============================

Quick test script to verify email generation functionality.
"""

import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from gemini.email_generation.email_service import email_service


def test_student_email():
    """Test generating email to student"""
    print("\n" + "="*60)
    print("Testing: Email to Student")
    print("="*60)
    
    student_data = {
        'name': 'John Doe',
        'rollNo': '2023BT001',
        'course': 'B.Tech Computer Science',
        'year': '2nd Year'
    }
    
    prediction_data = {
        'riskLevel': 'MEDIUM',
        'riskPercentage': 45,
        'riskFactors': [
            {'name': 'Low Attendance', 'contribution': 35},
            {'name': 'Declining CGPA', 'contribution': 25},
            {'name': 'Low Library Visits', 'contribution': 20}
        ]
    }
    
    try:
        email = email_service.generate_email(
            email_type='student',
            student_data=student_data,
            prediction_data=prediction_data,
            additional_notes='Student has been struggling with time management'
        )
        
        print("\n✅ Email generated successfully!")
        print(f"\nSubject: {email['subject']}")
        print(f"\nBody:\n{email['body']}")
        
    except Exception as e:
        print(f"\n❌ Error: {e}")


def test_parent_email():
    """Test generating email to parents"""
    print("\n" + "="*60)
    print("Testing: Email to Parents")
    print("="*60)
    
    student_data = {
        'name': 'Jane Smith',
        'rollNo': '2023BT002',
        'course': 'B.Tech Electronics',
        'year': '3rd Year'
    }
    
    prediction_data = {
        'riskLevel': 'HIGH',
        'riskPercentage': 72,
        'riskFactors': [
            {'name': 'Very Low Attendance', 'contribution': 45},
            {'name': 'Poor Academic Performance', 'contribution': 30},
            {'name': 'No Counselor Visits', 'contribution': 15}
        ]
    }
    
    try:
        email = email_service.generate_email(
            email_type='parent',
            student_data=student_data,
            prediction_data=prediction_data
        )
        
        print("\n✅ Email generated successfully!")
        print(f"\nSubject: {email['subject']}")
        print(f"\nBody:\n{email['body']}")
        
    except Exception as e:
        print(f"\n❌ Error: {e}")


def test_meeting_invitation():
    """Test generating meeting invitation"""
    print("\n" + "="*60)
    print("Testing: Meeting Invitation")
    print("="*60)
    
    student_data = {
        'name': 'Alex Johnson',
        'rollNo': '2023BT003',
        'course': 'B.Tech Mechanical',
        'year': '1st Year'
    }
    
    prediction_data = {
        'riskLevel': 'LOW',
        'riskPercentage': 25,
        'riskFactors': [
            {'name': 'Moderate Attendance', 'contribution': 15},
            {'name': 'Average Engagement', 'contribution': 10}
        ]
    }
    
    meeting_details = {
        'date': '2024-02-15',
        'time': '10:00 AM',
        'location': 'Room 301, Admin Block'
    }
    
    try:
        email = email_service.generate_email(
            email_type='meeting',
            student_data=student_data,
            prediction_data=prediction_data,
            meeting_details=meeting_details
        )
        
        print("\n✅ Email generated successfully!")
        print(f"\nSubject: {email['subject']}")
        print(f"\nBody:\n{email['body']}")
        
    except Exception as e:
        print(f"\n❌ Error: {e}")


if __name__ == '__main__':
    print("\n" + "="*60)
    print("🧪 Email Generation Service Test Suite")
    print("="*60)
    
    if not email_service.is_available:
        print("\n❌ Email service is not available!")
        print("   Please set GEMINI_API_KEY in your .env file")
        sys.exit(1)
    
    print("\n✅ Email service is available")
    
    # Run tests
    test_student_email()
    test_parent_email()
    test_meeting_invitation()
    
    print("\n" + "="*60)
    print("✅ All tests completed!")
    print("="*60 + "\n")
