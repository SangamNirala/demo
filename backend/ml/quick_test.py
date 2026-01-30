"""
Quick test - just run this to see if prediction works
"""

print("Starting quick test...")
print()

try:
    from predict import DropoutPredictor, format_prediction_output
    
    print("✅ Imports successful")
    print()
    
    # Create predictor
    print("Loading model...")
    predictor = DropoutPredictor()
    print()
    
    if not predictor.is_loaded:
        print("❌ Model not loaded. Run train.py first!")
        exit(1)
    
    # Simple test student
    student = {
        'name': 'Test Student',
        'roll_no': '12345',
        'course': 'B.Tech CS',
        'year_string': '2nd Year',
        'attendance_percentage': 50,
        'cgpa_current': 5.0,
        'cgpa_previous': 6.5,
        'fee_payment_delay_months': 2,
    }
    
    print("Making prediction...")
    result = predictor.predict(student)
    
    if result.get('error'):
        print(f"Error: {result['message']}")
    else:
        print(format_prediction_output(result))
        
except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()
