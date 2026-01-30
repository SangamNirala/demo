"""
Generate Risk Scores for All Students
======================================

This script runs all student data through the trained model
and adds a risk_percentage column to the dataset.
"""

import json
import os
import sys
from typing import Dict, List

# Add backend directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from ml.predict import DropoutPredictor


def load_students_data(file_path: str) -> Dict:
    """Load students data from JSON file"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        print(f"❌ Error loading students data: {e}")
        return None


def save_students_data(file_path: str, data: Dict) -> bool:
    """Save updated students data to JSON file"""
    try:
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        return True
    except Exception as e:
        print(f"❌ Error saving students data: {e}")
        return False


def generate_risk_scores():
    """Main function to generate risk scores for all students"""
    
    print("\n" + "="*70)
    print("🎯 GENERATING RISK SCORES FOR ALL STUDENTS")
    print("="*70 + "\n")
    
    # Initialize predictor
    print("📊 Step 1: Loading ML Model...")
    predictor = DropoutPredictor()
    
    if not predictor.is_loaded:
        print("\n❌ ERROR: Model not loaded!")
        print("   Please ensure model files exist in backend/ml/saved_models/")
        print("   Run the training script first if models don't exist.")
        return False
    
    print("✅ Model loaded successfully!\n")
    
    # Load students data
    print("📂 Step 2: Loading Students Data...")
    data_path = os.path.join(os.path.dirname(__file__), 'database', 'students_data.json')
    students_data = load_students_data(data_path)
    
    if not students_data:
        print("❌ Failed to load students data!")
        return False
    
    students = students_data.get('students', {})
    total_students = len(students)
    print(f"✅ Loaded {total_students} students\n")
    
    # Process each student
    print("🔄 Step 3: Generating Risk Scores...")
    print("-" * 70)
    
    successful = 0
    failed = 0
    risk_distribution = {'HIGH': 0, 'MEDIUM': 0, 'LOW': 0}
    
    for idx, (roll_no, student_data) in enumerate(students.items(), 1):
        try:
            # Make prediction
            prediction = predictor.predict(student_data)
            
            if prediction.get('error'):
                print(f"   ⚠️  {idx}/{total_students} - {roll_no}: Prediction failed")
                failed += 1
                continue
            
            # Extract risk percentage (note: key is 'risk_percentage' not 'riskPercentage')
            risk_percentage = prediction.get('risk_percentage', 0)
            risk_level = prediction.get('risk_level', 'UNKNOWN')
            
            # Add risk_percentage to student data
            student_data['risk_percentage'] = round(risk_percentage, 2)
            student_data['risk_level'] = risk_level
            student_data['prediction_generated'] = True
            
            # Update distribution
            if risk_level in risk_distribution:
                risk_distribution[risk_level] += 1
            
            successful += 1
            
            # Print progress
            status_emoji = '🔴' if risk_level == 'HIGH' else '🟡' if risk_level == 'MEDIUM' else '🟢'
            print(f"   {status_emoji} {idx}/{total_students} - {roll_no}: {risk_percentage:.1f}% ({risk_level})")
            
        except Exception as e:
            print(f"   ❌ {idx}/{total_students} - {roll_no}: Error - {str(e)}")
            failed += 1
    
    print("-" * 70)
    print(f"\n✅ Processing Complete!")
    print(f"   Successful: {successful}/{total_students}")
    print(f"   Failed: {failed}/{total_students}")
    
    # Print risk distribution
    print(f"\n📊 Risk Distribution:")
    print(f"   🔴 HIGH RISK:   {risk_distribution['HIGH']} students ({risk_distribution['HIGH']/total_students*100:.1f}%)")
    print(f"   🟡 MEDIUM RISK: {risk_distribution['MEDIUM']} students ({risk_distribution['MEDIUM']/total_students*100:.1f}%)")
    print(f"   🟢 LOW RISK:    {risk_distribution['LOW']} students ({risk_distribution['LOW']/total_students*100:.1f}%)")
    
    # Save updated data
    print(f"\n💾 Step 4: Saving Updated Data...")
    if save_students_data(data_path, students_data):
        print(f"✅ Data saved successfully to: {data_path}")
    else:
        print(f"❌ Failed to save data!")
        return False
    
    # Create a summary CSV file
    print(f"\n📄 Step 5: Creating Summary CSV...")
    try:
        import csv
        csv_path = os.path.join(os.path.dirname(__file__), 'database', 'risk_scores_summary.csv')
        
        with open(csv_path, 'w', newline='', encoding='utf-8') as csvfile:
            fieldnames = ['roll_no', 'name', 'course', 'year', 'risk_percentage', 'risk_level', 
                         'attendance_percentage', 'cgpa_current', 'actual_dropout_status']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            
            writer.writeheader()
            for roll_no, student_data in students.items():
                writer.writerow({
                    'roll_no': roll_no,
                    'name': student_data.get('name', ''),
                    'course': student_data.get('course', ''),
                    'year': student_data.get('year', ''),
                    'risk_percentage': student_data.get('risk_percentage', 0),
                    'risk_level': student_data.get('risk_level', ''),
                    'attendance_percentage': student_data.get('attendance_percentage', 0),
                    'cgpa_current': student_data.get('cgpa_current', 0),
                    'actual_dropout_status': student_data.get('actual_dropout_status', 0)
                })
        
        print(f"✅ Summary CSV created: {csv_path}")
    except Exception as e:
        print(f"⚠️  Warning: Could not create CSV summary - {e}")
    
    print("\n" + "="*70)
    print("🎉 RISK SCORE GENERATION COMPLETE!")
    print("="*70 + "\n")
    
    return True


if __name__ == '__main__':
    success = generate_risk_scores()
    sys.exit(0 if success else 1)
