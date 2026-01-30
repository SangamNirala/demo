"""
Test Chatbot Context Building
==============================

Test script to verify chatbot correctly reads student and prediction data.
"""

import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from gemini.chatbot.chatbot_service import chatbot_service


def test_context_building():
    """Test that context is built correctly from student and prediction data"""
    
    print("\n" + "="*60)
    print("Testing: Chatbot Context Building")
    print("="*60)
    
    # Sample data matching frontend format (camelCase)
    student_data = {
        'name': 'Ekta Reddy',
        'rollNo': '2022CS179',
        'roll_no': '2022CS179',  # Also include snake_case for compatibility
        'course': 'B.Tech Computer Science',
        'year': '2',
        'attendance': 65,
        'currentCGPA': 5.7,
        'previousCGPA': 6.2,
        'libraryVisits': 0,
        'lastLMSLogin': '30 days ago',
        'feeStatus': 'Delayed by 3 months',
        'counselorVisits': 2,
        'familyIncome': 'Low',
        'parentEducation': 'High School',
        'accommodation': 'Hostel',
        'extracurricular': 'None'
    }
    
    prediction_data = {
        'riskLevel': 'MEDIUM',
        'riskPercentage': 54.5,
        'riskFactors': [
            {
                'name': 'Academic Decline',
                'contribution': 28.6,
                'description': 'CGPA dropped from 6.2 to 5.7'
            },
            {
                'name': 'Low Attendance',
                'contribution': 19,
                'description': 'Attendance at 65%'
            },
            {
                'name': 'Mental Health Concern',
                'contribution': 19,
                'description': 'Visited counselor 2 times'
            },
            {
                'name': 'Low Engagement',
                'contribution': 19,
                'description': 'No library visits, LMS inactive for 30 days'
            },
            {
                'name': 'Financial Stress',
                'contribution': 14.3,
                'description': 'Fee payment delayed by 3 months'
            }
        ],
        'recommendations': [
            {
                'title': 'Prioritize Mental Well-being',
                'priority': 'URGENT',
                'description': 'Follow up with counseling center for continued support'
            },
            {
                'title': 'Resolve Outstanding Fee Payment',
                'priority': 'URGENT',
                'description': 'Connect with financial aid office'
            },
            {
                'title': 'Re-engage with Classes & LMS',
                'priority': 'HIGH',
                'description': 'Develop realistic attendance plan'
            }
        ]
    }
    
    # Build context
    context = chatbot_service._build_context(student_data, prediction_data)
    
    print("\n✅ Context built successfully!")
    print("\n" + "="*60)
    print("GENERATED CONTEXT:")
    print("="*60)
    print(context)
    print("="*60)
    
    # Verify key information is present
    checks = [
        ('Student Name', 'Ekta Reddy' in context),
        ('Roll Number', '2022CS179' in context),
        ('Risk Level', 'MEDIUM' in context),
        ('Risk Percentage', '54.5' in context),
        ('Academic Decline', 'Academic Decline' in context),
        ('Attendance', '65' in context),
        ('CGPA Current', '5.7' in context),
        ('CGPA Previous', '6.2' in context),
        ('Fee Status', 'Delayed' in context or '3 months' in context),
        ('Recommendations', 'Mental Well-being' in context or 'Prioritize' in context)
    ]
    
    print("\n" + "="*60)
    print("VERIFICATION CHECKS:")
    print("="*60)
    
    all_passed = True
    for check_name, result in checks:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status}: {check_name}")
        if not result:
            all_passed = False
    
    print("="*60)
    
    if all_passed:
        print("\n✅ All checks passed! Context includes all required information.")
    else:
        print("\n❌ Some checks failed. Context may be missing information.")
    
    return all_passed


def test_chatbot_response():
    """Test actual chatbot response with sample data"""
    
    print("\n" + "="*60)
    print("Testing: Chatbot Response")
    print("="*60)
    
    if not chatbot_service.is_available:
        print("\n⚠️  Chatbot service not available (EMERGENT_LLM_KEY not set)")
        print("   Skipping response test")
        return
    
    student_data = {
        'name': 'Ekta Reddy',
        'rollNo': '2022CS179',
        'course': 'B.Tech Computer Science',
        'year': '2',
        'attendance': 65,
        'currentCGPA': 5.7,
        'previousCGPA': 6.2,
        'feeStatus': 'Delayed by 3 months'
    }
    
    prediction_data = {
        'riskLevel': 'MEDIUM',
        'riskPercentage': 54.5,
        'riskFactors': [
            {'name': 'Academic Decline', 'contribution': 28.6},
            {'name': 'Low Attendance', 'contribution': 19}
        ],
        'recommendations': [
            {'title': 'Prioritize Mental Well-being', 'priority': 'URGENT'}
        ]
    }
    
    # Test question
    question = "Why is this student at medium risk?"
    
    print(f"\n📝 Question: {question}")
    print("\n⏳ Generating response...")
    
    try:
        response = chatbot_service.chat(
            user_message=question,
            student_data=student_data,
            prediction_data=prediction_data,
            session_id="test_session"
        )
        
        if response.get('error'):
            print(f"\n❌ Error: {response.get('message')}")
        else:
            print("\n✅ Response generated successfully!")
            print("\n" + "="*60)
            print("CHATBOT RESPONSE:")
            print("="*60)
            print(response.get('response'))
            print("="*60)
            
            # Check if response mentions key data points
            response_text = response.get('response', '').lower()
            mentions_risk_level = 'medium' in response_text
            mentions_percentage = '54' in response_text or 'percentage' in response_text
            mentions_factors = 'academic' in response_text or 'attendance' in response_text
            
            print("\n" + "="*60)
            print("RESPONSE QUALITY CHECKS:")
            print("="*60)
            print(f"{'✅' if mentions_risk_level else '❌'} Mentions risk level")
            print(f"{'✅' if mentions_percentage else '❌'} References risk percentage")
            print(f"{'✅' if mentions_factors else '❌'} Discusses risk factors")
            print("="*60)
            
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()


if __name__ == '__main__':
    print("\n" + "="*60)
    print("🧪 Chatbot Context Test Suite")
    print("="*60)
    
    # Test 1: Context building
    context_passed = test_context_building()
    
    # Test 2: Actual chatbot response (if API key available)
    test_chatbot_response()
    
    print("\n" + "="*60)
    print("✅ Tests completed!")
    print("="*60 + "\n")
