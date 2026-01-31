"""
Prediction Route Handlers
=========================

This module contains handler functions for prediction routes.
These handlers process prediction requests and return responses.
"""

from flask import jsonify, request
from typing import Dict, Any
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

from services.student_service.student_service import StudentService
from services.prediction_service.prediction_service import PredictionService
from schemas.prediction_schema.prediction_schema import PredictionSchema


class PredictionRouteHandler:
    """Handler class for prediction routes"""
    
    def __init__(self):
        """Initialize handler with services"""
        self.student_service = StudentService()
        self.prediction_service = PredictionService()
    
    def predict_dropout_handler(self, roll_no: str) -> tuple:
        """
        Handle dropout prediction request
        
        Args:
            roll_no: Student roll number
            
        Returns:
            Tuple of (response_data, status_code)
        """
        try:
            # Get student data
            student = self.student_service.get_student_by_roll_no(roll_no)
            
            if student is None:
                return {'error': 'Student not found'}, 404
            
            # Make prediction
            prediction = self.prediction_service.predict_dropout_risk(student)
            
            if prediction.get('error'):
                return prediction, 500
            
            # Format response
            formatted_response = PredictionSchema.format_response(prediction)
            
            return formatted_response, 200
            
        except Exception as e:
            import traceback
            return {
                'error': f'Prediction failed: {str(e)}',
                'traceback': traceback.format_exc()
            }, 500
    
    def get_model_info_handler(self) -> tuple:
        """
        Handle model info request
        
        Returns:
            Tuple of (response_data, status_code)
        """
        try:
            model_info = self.prediction_service.get_model_info()
            return model_info, 200
            
        except Exception as e:
            return {'error': f'Server error: {str(e)}'}, 500


# Create singleton instance
prediction_handler = PredictionRouteHandler()
