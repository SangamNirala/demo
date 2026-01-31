"""
Test script for Gemini AI integration
======================================

This script tests the Gemini service with sample student data.
"""

import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from gemini_service import GeminiService


def test_gemini_service():
    """Test Gemini service with sample data"""
    
    print("=" * 70)
    print("🤖 TESTING GEMINI AI INTEGRATION")
    print("=" * 70)
    
    # Initialize service
    gemini_service = GeminiService()
    
    if not gemini_service.is_available:
        print("\n❌ Gemini API key not found!")
        print("   Please set GEMINI_API_KEY in backend/.env file")
        return False
    
    print("\n✅ Gemini service initialized successfully")
    print(f"   API Key: {gemini_service.api_key[:10]}...{gemini_service.api_key[-4:]}")
    
    # Sample high-risk student data
    student_data = {
        'name': 'Rahul Sharma',
        'roll_no': '2023CS001',
        'course': 'B.Tech Computer Science',
        'year': 2,
        'year_string': '2nd Year',
        'gender': 'Male',
        'age': 20,
        'attendance_percentage': 42.3,
        'assignment_submission_rate': 35.0,
        'library_visits_monthly': 0,
        'lms_last_login_days': 18,
        'extracurricular_participation': False,
        'family_income': 280000,
        'fee_payment_delay_months': 3,
        'scholarship_holder': False,
        'tuition_fees_up_to_date': False,
        'debtor': True,
        'counselor_visits': 3,
        'counselor_visit_reason': 'Stress',
        'distance_from_college': 45.0,
        'hostel_day_scholar': 'Day Scholar',
        'cgpa_current': 5.2,
        'cgpa_previous': 6.8,
        'cgpa_semester1': 6.8,
        'cgpa_semester2': 5.2,
    }
    
    # Sample risk factors
    risk_factors = [
        {
            'category': 'academic_decline',
            'name': 'Academic Decline',
            'icon': '📚',
            'description': 'Declining grades and poor academic performance',
            'contribution': 35.5
        },
        {
            'category': 'low_attendance',
            'name': 'Low Attendance',
            'icon': '📅',
            'description': 'Irregular class attendance and LMS activity',
            'contribution': 28.2
        },
        {
            'category': 'financial_stress',
            'name': 'Financial Stress',
            'icon': '💰',
            'description': 'Fee payment delays and financial difficulties',
            'contribution': 22.1
        }
    ]
    
    print("\n📊 Test Student Profile:")
    print(f"   Name: {student_data['name']}")
    print(f"   Course: {student_data['course']}")
    print(f"   Risk Level: HIGH (78.5%)")
    print(f"   Top Risk Factors:")
    for rf in risk_factors:
        print(f"      - {rf['name']}: {rf['contribution']}%")
    
    print("\n🔄 Calling Gemini API to generate recommendations...")
    print("   (This may take a few seconds...)")
    
    try:
        recommendations = gemini_service.generate_personalized_recommendations(
            student_data=student_data,
            risk_percentage=78.5,
            risk_factors=risk_factors,
            risk_level='HIGH'
        )
        
        print("\n✅ Successfully generated recommendations!")
        print(f"\n💡 PERSONALIZED RECOMMENDATIONS ({len(recommendations)}):")
        print("=" * 70)
        
        for i, rec in enumerate(recommendations, 1):
            print(f"\n{i}. {rec['icon']} {rec['title']}")
            print(f"   Priority: {rec['priority'].upper()}")
            print(f"   Description: {rec['description']}")
        
        print("\n" + "=" * 70)
        print("✅ GEMINI INTEGRATION TEST PASSED!")
        print("=" * 70)
        
        return True
        
    except Exception as e:
        print(f"\n❌ Error during Gemini API call: {e}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    success = test_gemini_service()
    sys.exit(0 if success else 1)
