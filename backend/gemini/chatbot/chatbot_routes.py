"""
Chatbot Routes Module
=====================

Flask routes for chatbot API endpoints.
"""

from flask import Blueprint, request, jsonify
from .chatbot_service import chatbot_service
import json

# Create blueprint
chatbot_bp = Blueprint('chatbot', __name__, url_prefix='/api/chatbot')


@chatbot_bp.route('/chat', methods=['POST'])
def chat():
    """
    Handle chat message from faculty/admin
    
    Request JSON:
        {
            "message": "Why is this student at high risk?",
            "student_data": {...},
            "prediction_data": {...},
            "session_id": "optional-session-id"
        }
    
    Returns:
        JSON with chatbot response
    """
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        
        user_message = data.get('message', '').strip()
        student_data = data.get('student_data', {})
        prediction_data = data.get('prediction_data', {})
        session_id = data.get('session_id', 'default')
        
        if not user_message:
            return jsonify({'error': 'Message is required'}), 400
        
        if not student_data or not prediction_data:
            return jsonify({'error': 'Student and prediction data are required'}), 400
        
        # Process chat message
        response = chatbot_service.chat(
            user_message=user_message,
            student_data=student_data,
            prediction_data=prediction_data,
            session_id=session_id
        )
        
        if response.get('error'):
            return jsonify(response), 500
        
        return jsonify(response), 200
        
    except Exception as e:
        print(f"Error in chat endpoint: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({
            'error': True,
            'message': f'Server error: {str(e)}'
        }), 500


@chatbot_bp.route('/clear-history', methods=['POST'])
def clear_history():
    """
    Clear conversation history for a session
    
    Request JSON:
        {
            "session_id": "optional-session-id"
        }
    
    Returns:
        Success message
    """
    try:
        data = request.get_json() or {}
        session_id = data.get('session_id', 'default')
        
        chatbot_service.clear_history(session_id)
        
        return jsonify({
            'success': True,
            'message': 'Conversation history cleared'
        }), 200
        
    except Exception as e:
        print(f"Error clearing history: {e}")
        return jsonify({
            'error': True,
            'message': f'Server error: {str(e)}'
        }), 500


@chatbot_bp.route('/suggestions', methods=['GET'])
def get_suggestions():
    """
    Get suggested questions for faculty
    
    Returns:
        List of suggested questions
    """
    suggestions = [
        "Why is this student at high risk?",
        "What should I do first for this student?",
        "What are the main concerns for this student?",
        "How can we improve their attendance?",
        "What financial support options are available?",
        "How is their academic performance trending?",
        "What interventions have the highest priority?",
        "How can we address their engagement issues?"
    ]
    
    return jsonify({
        'suggestions': suggestions
    }), 200
