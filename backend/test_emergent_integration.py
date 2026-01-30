"""
Test script to verify Emergent LLM integration with all three services
"""

import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from gemini.gemini_service import GeminiService
from gemini.email_generation.email_service import EmailGenerationService
from gemini.pdf_generation.pdf_service import PDFReportService

def test_gemini_service():
    """Test recommendation generation"""
    print("\n" + "="*60)
    print("Testing Recommendation Generation Service")
    print("="*60)
    
    service = GeminiService()
    
    if not service.is_available:
        print("❌ Service not available - check EMERGENT_LLM_KEY")
        return False
    
    # Test data
    student_data = {
        'name': 'Test Student',
        'course': 'Computer Science',
        'year': '2nd Year',
        'cgpa_current': 7.5,
        'attendance_percentage': 75
    }
    
    risk_factors = [
        {'name': 'Low Attendance', 'contribution': 35, 'category': 'low_attendance', 'description': 'Attendance below 80%'},
        {'name': 'Academic Decline', 'contribution': 25, 'category': 'academic_decline', 'description': 'CGPA decreased'}
    ]
    
    try:
        print("🔄 Generating recommendations...")
        recommendations = service.generate_personalized_recommendations(
            student_data=student_data,
            risk_percentage=65,
            risk_factors=risk_factors,
            risk_level='HIGH'
        )
        print(f"✅ Successfully generated {len(recommendations)} recommendations")
        print(f"   Sample: {recommendations[0]['title']}")
        return True
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_email_service():
    """Test email generation"""
    print("\n" + "="*60)
    print("Testing Email Generation Service")
    print("="*60)
    
    service = EmailGenerationService()
    
    if not service.is_available:
        print("❌ Service not available - check EMERGENT_LLM_KEY")
        return False
    
    # Test data
    student_data = {
        'name': 'Test Student',
        'rollNo': 'CS2023001',
        'course': 'Computer Science',
        'year': '2nd Year'
    }
    
    prediction_data = {
        'riskLevel': 'HIGH',
        'riskPercentage': 65,
        'riskFactors': [
            {'name': 'Low Attendance', 'contribution': 35}
        ]
    }
    
    try:
        print("🔄 Generating student email...")
        email = service.generate_email(
            email_type='student',
            student_data=student_data,
            prediction_data=prediction_data
        )
        print(f"✅ Successfully generated email")
        print(f"   Subject: {email['subject'][:50]}...")
        return True
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_pdf_service():
    """Test PDF generation (AI content only, not full PDF)"""
    print("\n" + "="*60)
    print("Testing PDF Report Service (AI Content)")
    print("="*60)
    
    service = PDFReportService()
    
    if not service.is_available:
        print("❌ Service not available - check EMERGENT_LLM_KEY")
        return False
    
    # Test data
    student_data = {
        'name': 'Test Student',
        'rollNo': 'CS2023001',
        'course': 'Computer Science',
        'year': '2nd Year',
        'attendance': 75,
        'currentCGPA': 7.5
    }
    
    prediction_data = {
        'riskLevel': 'HIGH',
        'riskPercentage': 65,
        'risk_factors': [
            {'name': 'Low Attendance', 'contribution': 35}
        ]
    }
    
    try:
        print("🔄 Generating AI content for PDF...")
        ai_content = service._generate_ai_content(student_data, prediction_data)
        print(f"✅ Successfully generated AI content")
        print(f"   Executive Summary: {ai_content['executive_summary']['overview'][:60]}...")
        return True
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("\n" + "="*60)
    print("🧪 Testing Emergent LLM Integration")
    print("="*60)
    
    results = {
        'Recommendation Generation': test_gemini_service(),
        'Email Generation': test_email_service(),
        'PDF Generation': test_pdf_service()
    }
    
    print("\n" + "="*60)
    print("📊 Test Results Summary")
    print("="*60)
    
    for service, result in results.items():
        status = "✅ PASSED" if result else "❌ FAILED"
        print(f"{service}: {status}")
    
    all_passed = all(results.values())
    
    print("\n" + "="*60)
    if all_passed:
        print("🎉 All tests passed! Emergent LLM integration is working correctly.")
    else:
        print("⚠️  Some tests failed. Please check the errors above.")
    print("="*60)
    
    sys.exit(0 if all_passed else 1)
