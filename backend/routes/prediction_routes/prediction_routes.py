"""
Prediction Routes Module
========================

This module defines routes for prediction-related operations.
"""

from flask import Blueprint, jsonify, request
import json
import os
import sys

# Add parent directory to path to import ml module
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

from ml.predict import DropoutPredictor

# Create blueprint
prediction_bp = Blueprint('prediction', __name__)

# Initialize predictor (singleton)
_predictor = None

def get_predictor():
    """Get or create predictor instance"""
    global _predictor
    if _predictor is None:
        _predictor = DropoutPredictor()
    return _predictor

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

@prediction_bp.route('/<roll_no>', methods=['POST'])
def predict_dropout(roll_no):
    """
    Predict dropout risk for a student
    
    Args:
        roll_no: Student roll number
        
    Returns:
        JSON with prediction results
    """
    try:
        students_data = load_students()
        students = students_data.get('students', {})
        
        if roll_no not in students:
            return jsonify({'error': 'Student not found'}), 404
        
        student_data = students[roll_no]
        
        # Get predictor and make prediction
        predictor = get_predictor()
        prediction = predictor.predict(student_data)
        
        if prediction.get('error'):
            return jsonify(prediction), 500
        
        return jsonify(prediction), 200
        
    except Exception as e:
        import traceback
        return jsonify({
            'error': f'Prediction failed: {str(e)}',
            'traceback': traceback.format_exc()
        }), 500
