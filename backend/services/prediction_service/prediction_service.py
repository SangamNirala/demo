"""
Prediction Service Module
=========================

This module provides business logic for prediction-related operations.
"""

import sys
import os
from typing import Dict, Optional

# Add parent directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

from ml.predict import DropoutPredictor


class PredictionService:
    """Service class for prediction operations"""
    
    def __init__(self):
        """Initialize prediction service"""
        self.predictor = DropoutPredictor()
    
    def predict_dropout_risk(self, student_data: Dict) -> Dict:
        """
        Predict dropout risk for a student
        
        Args:
            student_data: Dictionary containing student information
            
        Returns:
            Prediction result dictionary
        """
        if not self.predictor.is_loaded:
            return {
                'error': True,
                'message': 'ML model not loaded. Please check model files.'
            }
        
        return self.predictor.predict(student_data)
    
    def is_model_loaded(self) -> bool:
        """Check if ML model is loaded"""
        return self.predictor.is_loaded
    
    def get_model_info(self) -> Dict:
        """Get information about the loaded model"""
        if not self.predictor.is_loaded:
            return {
                'loaded': False,
                'message': 'Model not loaded'
            }
        
        return {
            'loaded': True,
            'feature_count': len(self.predictor.feature_names) if self.predictor.feature_names else 0,
            'model_type': type(self.predictor.model).__name__ if self.predictor.model else 'Unknown',
            'metadata': self.predictor.metadata or {}
        }
