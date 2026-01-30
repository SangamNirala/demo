"""
Prediction Service Server Module
=================================

This module provides server-side logic for prediction service operations.
It handles request processing, caching, and additional business logic.
"""

from typing import Dict, Optional
from datetime import datetime
from .prediction_service import PredictionService


class PredictionServiceServer:
    """Server-side wrapper for prediction service"""
    
    def __init__(self):
        """Initialize service server"""
        self.service = PredictionService()
        self._prediction_cache = {}
        self._cache_ttl = 300  # 5 minutes cache
    
    def process_prediction_request(self, student_data: Dict) -> Dict:
        """
        Process prediction request with caching and logging
        
        Args:
            student_data: Student data for prediction
            
        Returns:
            Prediction result
        """
        roll_no = student_data.get('roll_no', student_data.get('student_id'))
        
        # Check cache
        cached_result = self._get_from_cache(roll_no)
        if cached_result:
            cached_result['from_cache'] = True
            return cached_result
        
        # Make prediction
        prediction = self.service.predict_dropout_risk(student_data)
        
        # Add metadata
        prediction['timestamp'] = datetime.now().isoformat()
        prediction['from_cache'] = False
        
        # Cache result
        if not prediction.get('error'):
            self._add_to_cache(roll_no, prediction)
        
        return prediction
    
    def _get_from_cache(self, roll_no: str) -> Optional[Dict]:
        """Get prediction from cache if available and not expired"""
        if roll_no not in self._prediction_cache:
            return None
        
        cached_data = self._prediction_cache[roll_no]
        cache_time = cached_data.get('cache_time', 0)
        
        # Check if cache is expired
        if (datetime.now().timestamp() - cache_time) > self._cache_ttl:
            del self._prediction_cache[roll_no]
            return None
        
        return cached_data.get('prediction')
    
    def _add_to_cache(self, roll_no: str, prediction: Dict):
        """Add prediction to cache"""
        self._prediction_cache[roll_no] = {
            'prediction': prediction,
            'cache_time': datetime.now().timestamp()
        }
    
    def clear_cache(self, roll_no: Optional[str] = None):
        """
        Clear prediction cache
        
        Args:
            roll_no: Specific roll number to clear, or None to clear all
        """
        if roll_no:
            if roll_no in self._prediction_cache:
                del self._prediction_cache[roll_no]
        else:
            self._prediction_cache.clear()
    
    def get_service_status(self) -> Dict:
        """
        Get prediction service status
        
        Returns:
            Service status information
        """
        return {
            'model_loaded': self.service.is_model_loaded(),
            'cache_size': len(self._prediction_cache),
            'cache_ttl': self._cache_ttl,
            'model_info': self.service.get_model_info()
        }
    
    def batch_predict(self, students_data: list[Dict]) -> list[Dict]:
        """
        Process batch prediction requests
        
        Args:
            students_data: List of student data dictionaries
            
        Returns:
            List of prediction results
        """
        results = []
        
        for student_data in students_data:
            try:
                prediction = self.process_prediction_request(student_data)
                results.append({
                    'roll_no': student_data.get('roll_no'),
                    'prediction': prediction,
                    'success': not prediction.get('error', False)
                })
            except Exception as e:
                results.append({
                    'roll_no': student_data.get('roll_no'),
                    'error': str(e),
                    'success': False
                })
        
        return results


# Create singleton instance
prediction_service_server = PredictionServiceServer()
