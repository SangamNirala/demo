"""
Prediction Schema Server Module
================================

This module provides server-side schema validation and transformation
for prediction data.
"""

from typing import Dict, Any, List, Optional
from .prediction_schema import PredictionSchema


class PredictionSchemaServer:
    """Server-side schema operations for prediction data"""
    
    @staticmethod
    def validate_prediction_response(prediction_data: Dict[str, Any]) -> tuple[bool, Optional[str]]:
        """
        Validate prediction response data
        
        Args:
            prediction_data: Prediction data to validate
            
        Returns:
            Tuple of (is_valid, error_message)
        """
        # Check for error flag
        if prediction_data.get('error'):
            return True, None  # Error responses are valid
        
        # Check required fields
        required_fields = ['risk_level', 'risk_percentage', 'risk_factors', 'recommendations']
        
        for field in required_fields:
            if field not in prediction_data:
                return False, f"Missing required field: {field}"
        
        # Validate risk level
        valid_risk_levels = ['LOW', 'MEDIUM', 'HIGH']
        if prediction_data.get('risk_level') not in valid_risk_levels:
            return False, f"Invalid risk level: {prediction_data.get('risk_level')}"
        
        # Validate risk percentage
        risk_pct = prediction_data.get('risk_percentage', 0)
        if not isinstance(risk_pct, (int, float)) or risk_pct < 0 or risk_pct > 100:
            return False, f"Invalid risk percentage: {risk_pct}"
        
        return True, None
    
    @staticmethod
    def transform_for_api(prediction_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Transform prediction data for API response
        
        Args:
            prediction_data: Raw prediction data
            
        Returns:
            Transformed data suitable for API response
        """
        # Use the schema's format method
        formatted = PredictionSchema.format_response(prediction_data)
        
        # Add additional API metadata
        if not formatted.get('error'):
            formatted['api_version'] = '1.0'
            formatted['response_type'] = 'prediction'
        
        return formatted
    
    @staticmethod
    def create_error_response(error_message: str, details: Optional[Dict] = None) -> Dict[str, Any]:
        """
        Create standardized error response
        
        Args:
            error_message: Error message
            details: Optional error details
            
        Returns:
            Error response dictionary
        """
        response = {
            'error': True,
            'message': error_message,
            'risk_level': 'UNKNOWN',
            'risk_percentage': 0,
            'risk_factors': [],
            'recommendations': []
        }
        
        if details:
            response['details'] = details
        
        return response
    
    @staticmethod
    def enrich_prediction_response(prediction_data: Dict[str, Any], student_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Enrich prediction response with additional student context
        
        Args:
            prediction_data: Prediction data
            student_data: Student data
            
        Returns:
            Enriched prediction response
        """
        enriched = prediction_data.copy()
        
        # Add student context if not already present
        if 'student_info' not in enriched:
            enriched['student_info'] = {
                'name': student_data.get('name', 'Unknown'),
                'roll_no': student_data.get('roll_no', 'N/A'),
                'course': student_data.get('course', 'N/A'),
                'year': student_data.get('year_string', 'N/A')
            }
        
        # Add risk context
        if not enriched.get('error'):
            risk_level = enriched.get('risk_level', 'UNKNOWN')
            risk_pct = enriched.get('risk_percentage', 0)
            
            enriched['risk_context'] = {
                'level': risk_level,
                'percentage': risk_pct,
                'severity': PredictionSchemaServer._get_severity(risk_pct),
                'urgency': PredictionSchemaServer._get_urgency(risk_level),
                'color': PredictionSchemaServer._get_risk_color(risk_level),
                'emoji': PredictionSchemaServer._get_risk_emoji(risk_level)
            }
        
        return enriched
    
    @staticmethod
    def _get_severity(risk_percentage: float) -> str:
        """Get severity level from risk percentage"""
        if risk_percentage >= 80:
            return 'critical'
        elif risk_percentage >= 70:
            return 'high'
        elif risk_percentage >= 50:
            return 'moderate'
        elif risk_percentage >= 30:
            return 'low'
        else:
            return 'minimal'
    
    @staticmethod
    def _get_urgency(risk_level: str) -> str:
        """Get urgency level from risk level"""
        urgency_map = {
            'HIGH': 'immediate',
            'MEDIUM': 'soon',
            'LOW': 'routine'
        }
        return urgency_map.get(risk_level, 'unknown')
    
    @staticmethod
    def _get_risk_color(risk_level: str) -> str:
        """Get color code for risk level"""
        colors = {
            'HIGH': '#dc2626',
            'MEDIUM': '#f59e0b',
            'LOW': '#10b981'
        }
        return colors.get(risk_level, '#6b7280')
    
    @staticmethod
    def _get_risk_emoji(risk_level: str) -> str:
        """Get emoji for risk level"""
        emojis = {
            'HIGH': '🔴',
            'MEDIUM': '🟡',
            'LOW': '🟢'
        }
        return emojis.get(risk_level, '⚪')
    
    @staticmethod
    def aggregate_batch_predictions(predictions: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Aggregate statistics from batch predictions
        
        Args:
            predictions: List of prediction results
            
        Returns:
            Aggregated statistics
        """
        total = len(predictions)
        high_risk = sum(1 for p in predictions if p.get('risk_level') == 'HIGH')
        medium_risk = sum(1 for p in predictions if p.get('risk_level') == 'MEDIUM')
        low_risk = sum(1 for p in predictions if p.get('risk_level') == 'LOW')
        
        avg_risk = sum(p.get('risk_percentage', 0) for p in predictions) / total if total > 0 else 0
        
        return {
            'total_predictions': total,
            'risk_distribution': {
                'high': high_risk,
                'medium': medium_risk,
                'low': low_risk
            },
            'risk_percentages': {
                'high': round((high_risk / total * 100), 1) if total > 0 else 0,
                'medium': round((medium_risk / total * 100), 1) if total > 0 else 0,
                'low': round((low_risk / total * 100), 1) if total > 0 else 0
            },
            'average_risk_percentage': round(avg_risk, 1)
        }


# Create singleton instance
prediction_schema_server = PredictionSchemaServer()
