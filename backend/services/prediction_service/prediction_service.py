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
from gemini.gemini_service import GeminiService


class PredictionService:
    """Service class for prediction operations"""
    
    def __init__(self, use_gemini: bool = True):
        """
        Initialize prediction service
        
        Args:
            use_gemini: Whether to use Gemini AI for recommendations (default: True)
        """
        self.predictor = DropoutPredictor()
        self.gemini_service = GeminiService() if use_gemini else None
        self.use_gemini = use_gemini and (self.gemini_service is not None)
    
    def predict_dropout_risk(self, student_data: Dict) -> Dict:
        """
        Predict dropout risk for a student with AI-powered recommendations
        
        Args:
            student_data: Dictionary containing student information
            
        Returns:
            Prediction result dictionary with personalized recommendations
        """
        if not self.predictor.is_loaded:
            return {
                'error': True,
                'message': 'ML model not loaded. Please check model files.'
            }
        
        # Get base prediction from ML model
        prediction = self.predictor.predict(student_data)
        
        if prediction.get('error'):
            return prediction
        
        # Generate personalized recommendations using Gemini AI
        if self.use_gemini and self.gemini_service:
            try:
                print("🤖 Generating personalized recommendations with Gemini AI...")
                
                personalized_recommendations = self.gemini_service.generate_personalized_recommendations(
                    student_data=student_data,
                    risk_percentage=prediction['risk_percentage'],
                    risk_factors=prediction['risk_factors'],
                    risk_level=prediction['risk_level']
                )
                
                # Replace static recommendations with AI-generated ones
                prediction['recommendations'] = personalized_recommendations
                prediction['recommendations_source'] = 'gemini_ai'
                
                print(f"✅ Generated {len(personalized_recommendations)} personalized recommendations")
                
            except Exception as e:
                print(f"⚠️  Gemini AI failed, using fallback recommendations: {e}")
                prediction['recommendations_source'] = 'fallback'
        else:
            prediction['recommendations_source'] = 'static'
        
        return prediction
    
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
