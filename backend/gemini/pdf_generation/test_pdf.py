"""
Test Script for PDF Report Generation
======================================

This script tests the PDF report generation functionality.
"""

import sys
import os

# Add backend to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../..'))

from pdf_service import PDFReportService


def test_pdf_generation():
    """Test PDF generation with sample data"""
    
    print("\n" + "="*60)
    print("🧪 Testing PDF Report Generation")
    print("="*60 + "\n")
    
    # Sample student data
    student_data = {
        "name": "Rahul Sharma",
        "rollNo": "2023CS101",
        "roll_no": "2023CS101",
        "course": "B.Tech Computer Science",
        "year": "2nd Year",
        "familyIncome": "₹3,00,000/year",
        "parentEducation": "High School",
        "distanceFromCollege": "45 km",
        "accommodation": "Day Scholar",
        "attendance": 58,
        "currentCGPA": 4.8,
        "previousCGPA": 6.2,
        "assignmentsSubmitted": "4 out of 10",
        "libraryVisits": "0 visits in 2 months",
        "feeStatus": "2 months delayed",
        "counselorVisits": "Visited 2 times for stress",
        "extracurricular": "No participation",
        "lastLMSLogin": "15 days ago"
    }
    
    # Sample prediction data
    prediction_data = {
        "riskLevel": "HIGH",
        "risk_level": "HIGH",
        "riskPercentage": 82,
        "risk_percentage": 82,
        "riskFactors": [
            {
                "name": "Academic Decline",
                "factor": "Academic Decline",
                "contribution": 35,
                "description": "Significant drop in CGPA from 6.2 to 4.8"
            },
            {
                "name": "Low Attendance",
                "factor": "Low Attendance",
                "contribution": 25,
                "description": "Attendance at 58%, below minimum requirement"
            },
            {
                "name": "Financial Stress",
                "factor": "Financial Stress",
                "contribution": 20,
                "description": "Fee payment delayed by 2 months"
            },
            {
                "name": "Mental Health Concern",
                "factor": "Mental Health Concern",
                "contribution": 15,
                "description": "Multiple counselor visits for stress"
            },
            {
                "name": "Low Engagement",
                "factor": "Low Engagement",
                "contribution": 5,
                "description": "No library visits, no extracurricular participation"
            }
        ],
        "risk_factors": [
            {
                "name": "Academic Decline",
                "factor": "Academic Decline",
                "contribution": 35,
                "description": "Significant drop in CGPA from 6.2 to 4.8"
            },
            {
                "name": "Low Attendance",
                "factor": "Low Attendance",
                "contribution": 25,
                "description": "Attendance at 58%, below minimum requirement"
            },
            {
                "name": "Financial Stress",
                "factor": "Financial Stress",
                "contribution": 20,
                "description": "Fee payment delayed by 2 months"
            },
            {
                "name": "Mental Health Concern",
                "factor": "Mental Health Concern",
                "contribution": 15,
                "description": "Multiple counselor visits for stress"
            },
            {
                "name": "Low Engagement",
                "factor": "Low Engagement",
                "contribution": 5,
                "description": "No library visits, no extracurricular participation"
            }
        ]
    }
    
    try:
        # Initialize service
        print("1️⃣  Initializing PDF Report Service...")
        service = PDFReportService()
        print(f"   ✅ Service initialized (Gemini available: {service.is_available})\n")
        
        # Generate PDF
        print("2️⃣  Generating PDF report...")
        pdf_bytes = service.generate_report(student_data, prediction_data)
        print(f"   ✅ PDF generated successfully ({len(pdf_bytes)} bytes)\n")
        
        # Save to file
        output_file = "test_report.pdf"
        print(f"3️⃣  Saving PDF to {output_file}...")
        with open(output_file, 'wb') as f:
            f.write(pdf_bytes)
        print(f"   ✅ PDF saved successfully\n")
        
        print("="*60)
        print("✅ ALL TESTS PASSED!")
        print("="*60)
        print(f"\n📄 Test report saved as: {output_file}")
        print("   You can open this file to verify the PDF content.\n")
        
        return True
        
    except Exception as e:
        print(f"\n❌ TEST FAILED: {e}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    success = test_pdf_generation()
    sys.exit(0 if success else 1)
