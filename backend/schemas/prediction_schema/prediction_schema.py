"""
Prediction Schema Module
========================

This module defines data schemas for prediction-related operations.
"""

from typing import Dict, Any, List


class PredictionSchema:
    """Schema for prediction data validation and formatting"""
    
    @staticmethod
    def format_response(prediction_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Format prediction response for API
        
        Args:
            prediction_data: Raw prediction data from ML model
            
        Returns:
            Formatted prediction response
        """
        if prediction_data.get('error'):
            return {
                'error': True,
                'message': prediction_data.get('message', 'Prediction failed')
            }
        
        return {
            'error': False,
            'student_info': prediction_data.get('student_info', {}),
            'risk_level': prediction_data.get('risk_level', 'UNKNOWN'),
            'risk_percentage': prediction_data.get('risk_percentage', 0),
            'risk_factors': PredictionSchema._format_risk_factors(
                prediction_data.get('risk_factors', [])
            ),
            'recommendations': PredictionSchema._format_recommendations(
                prediction_data.get('recommendations', [])
            ),
            'prediction_details': prediction_data.get('prediction_details', {})
        }
    
    @staticmethod
    def _format_risk_factors(risk_factors: List[Dict]) -> List[Dict]:
        """Format risk factors for display"""
        return [
            {
                'name': factor.get('name', 'Unknown'),
                'icon': factor.get('icon', '📊'),
                'contribution': factor.get('contribution', 0),
                'description': factor.get('description', '')
            }
            for factor in risk_factors
        ]
    
    @staticmethod
    def _format_recommendations(recommendations: List[Dict]) -> List[Dict]:
        """Format recommendations for display"""
        return [
            {
                'id': rec.get('id', 0),
                'priority': rec.get('priority', 'medium'),
                'icon': rec.get('icon', '💡'),
                'title': rec.get('title', 'Recommendation'),
                'description': rec.get('description', ''),
                'action': rec.get('action', '')
            }
            for rec in recommendations
        ]
    
    @staticmethod
    def validate_prediction_request(data: Dict[str, Any]) -> tuple[bool, str]:
        """
        Validate prediction request data
        
        Args:
            data: Request data
            
        Returns:
            Tuple of (is_valid, error_message)
        """
        # For now, we just need student data
        # More validation can be added as needed
        return True, ""
