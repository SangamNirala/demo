"""
Test script for Chatbot service
================================

This script tests the chatbot with sample student data.
"""

import sys
import os

# Add parent directories to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

from chatbot_service import ChatbotService


def test_chatbot():
    """Test chatbot service with sample data"""
    
    print("=" * 70)
    print("💬 TESTING CHATBOT SERVICE")
    print("=" * 70)
    
    # Initialize service
    chatbot = ChatbotService()
    
    if not chatbot.is_available:
        print("\n❌ Chatbot service not available!")
        print("   Please set GEMINI_API_KEY in backend/.env file")
        return False
    
    print("\n✅ Chatbot service initialized successfully")
    
    # Sample student data
    student_data = {
        'name': 'Rahul Sharma',
        'roll_no': '2023CS001',
        'course': 'B.Tech Computer Science',
        'year': 2,
        'year_string': '2nd Year',
        'attendance_percentage': 42.3,
        'assignment_submission_rate': 35.0,
        'library_visits_monthly': 0,
        'lms_last_login_days': 18,
        'cgpa_current': 5.2,
        'cgpa_previous': 6.8,
        'fee_payment_delay_months': 3,
        'counselor_visits': 3,
        'family_income': 280000,
    }
    
    # Sample prediction data
    prediction_data = {
        'risk_level': 'HIGH',
        'risk_percentage': 78.5,
        'risk_factors': [
            {
                'name': 'Academic Decline',
                'contribution': 35.5,
                'description': 'Declining grades and poor academic performance'
            },
            {
                'name': 'Low Attendance',
                'contribution': 28.2,
                'description': 'Irregular class attendance and LMS activity'
            },
            {
                'name': 'Financial Stress',
                'contribution': 22.1,
                'description': 'Fee payment delays and financial difficulties'
            }
        ],
        'recommendations': [
            {
                'title': 'Urgent Financial Aid Support',
                'priority': 'urgent'
            },
            {
                'title': 'Academic Recovery Plan',
                'priority': 'high'
            }
        ]
    }
    
    # Test questions
    test_questions = [
        "Why is Rahul at high risk?",
        "What should I do first for this student?",
        "How can we improve his attendance?"
    ]
    
    session_id = "test_session"
    
    for i, question in enumerate(test_questions, 1):
        print(f"\n{'=' * 70}")
        print(f"TEST {i}: {question}")
        print('=' * 70)
        
        response = chatbot.chat(
            user_message=question,
            student_data=student_data,
            prediction_data=prediction_data,
            session_id=session_id
        )
        
        if response.get('error'):
            print(f"\n❌ Error: {response.get('message')}")
            return False
        
        print(f"\n🤖 Assistant Response:")
        print(response.get('response', ''))
    
    print(f"\n{'=' * 70}")
    print("✅ CHATBOT TEST PASSED!")
    print('=' * 70)
    
    return True


if __name__ == "__main__":
    success = test_chatbot()
    sys.exit(0 if success else 1)
