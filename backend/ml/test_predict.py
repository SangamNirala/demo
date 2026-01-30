"""
Simple test script for prediction module
"""

import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

print("=" * 60)
print("🔮 Testing Dropout Prediction System")
print("=" * 60)
print()

try:
    print("Step 1: Importing predict module...")
    from ml.predict import DropoutPredictor
    print("✅ Import successful!")
    print()

    print("Step 2: Initializing predictor...")
    predictor = DropoutPredictor()
    print()

    if not predictor.is_loaded:
        print("❌ Model failed to load!")
        print("Please run 'python train.py' first to train the model.")
        sys.exit(1)

    print("✅ Model loaded successfully!")
    print()

    # Test with a simple student
    print("Step 3: Testing prediction with sample student...")
    print()

    test_student = {
        'student_id': 'TEST001',
        'name': 'Test Student',
        'roll_no': 'TEST001',
        'course': 'B.Tech Computer Science',
        'year': 2,
        'year_string': '2nd Year',
        'gender': 'Male',
        'age': 20,
        'attendance_percentage': 55.0,
        'assignment_submission_rate': 40.0,
        'library_visits_monthly': 1,
        'lms_last_login_days': 10,
        'extracurricular_participation': False,
        'family_income': 300000,
        'fee_payment_delay_months': 2,
        'scholarship_holder': False,
        'tuition_fees_up_to_date': False,
        'debtor': True,
        'counselor_visits': 2,
        'distance_from_college': 40.0,
        'hostel_day_scholar': 'Day Scholar',
        'cgpa_current': 5.5,
        'cgpa_previous': 6.5,
        'cgpa_semester1': 6.5,
        'cgpa_semester2': 5.5,
        'units_enrolled_sem1': 6,
        'units_approved_sem1': 4,
        'units_enrolled_sem2': 6,
        'units_approved_sem2': 3,
    }

    result = predictor.predict(test_student)

    if result.get('error'):
        print(f"❌ Prediction failed: {result.get('message')}")
        if 'traceback' in result:
            print("\nError details:")
            print(result['traceback'])
    else:
        print("✅ Prediction successful!")
        print()
        print(f"Student: {result['student_info']['name']}")
        print(f"Risk Level: {result['risk_level_info']['emoji']} {result['risk_level']}")
        print(f"Risk Percentage: {result['risk_percentage']}%")
        print()
        print("Risk Factors:")
        for factor in result['risk_factors']:
            print(f"  - {factor['name']}: {factor['contribution']}%")
        print()
        print("Recommendations:")
        for i, rec in enumerate(result['recommendations'], 1):
            print(f"  {i}. {rec['icon']} {rec['title']}")

    print()
    print("=" * 60)
    print("✅ Test complete!")
    print("=" * 60)

except ImportError as e:
    print(f"❌ Import error: {e}")
    print("\nMake sure you're running this from the backend/ml directory:")
    print("  cd backend/ml")
    print("  python test_predict.py")

except Exception as e:
    print(f"❌ Unexpected error: {e}")
    import traceback
    traceback.print_exc()
