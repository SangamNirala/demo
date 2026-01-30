"""
Email Generation Routes
=======================

Flask routes for email generation endpoints.
"""

from flask import Blueprint, request, jsonify
from .email_service import email_service

email_bp = Blueprint('email', __name__)


@email_bp.route('/generate', methods=['POST'])
def generate_email():
    """
    Generate personalized email using Gemini AI
    
    Request Body:
    {
        "emailType": "student" | "parent" | "meeting",
        "studentData": {...},
        "predictionData": {...},
        "additionalNotes": "optional custom notes",
        "meetingDetails": {
            "date": "2024-02-15",
            "time": "10:00 AM",
            "location": "Room 301"
        }
    }
    
    Response:
    {
        "success": true,
        "email": {
            "subject": "...",
            "body": "..."
        }
    }
    """
    
    try:
        data = request.get_json()
        
        # Validate required fields
        if not data:
            return jsonify({
                'success': False,
                'error': 'Request body is required'
            }), 400
        
        email_type = data.get('emailType')
        student_data = data.get('studentData')
        prediction_data = data.get('predictionData')
        
        if not email_type:
            return jsonify({
                'success': False,
                'error': 'emailType is required'
            }), 400
        
        if email_type not in ['student', 'parent', 'meeting']:
            return jsonify({
                'success': False,
                'error': 'emailType must be one of: student, parent, meeting'
            }), 400
        
        if not student_data:
            return jsonify({
                'success': False,
                'error': 'studentData is required'
            }), 400
        
        if not prediction_data:
            return jsonify({
                'success': False,
                'error': 'predictionData is required'
            }), 400
        
        # Validate meeting details if meeting type
        if email_type == 'meeting':
            meeting_details = data.get('meetingDetails')
            if not meeting_details:
                return jsonify({
                    'success': False,
                    'error': 'meetingDetails is required for meeting invitation'
                }), 400
            
            if not meeting_details.get('date') or not meeting_details.get('time') or not meeting_details.get('location'):
                return jsonify({
                    'success': False,
                    'error': 'meetingDetails must include date, time, and location'
                }), 400
        
        # Generate email
        additional_notes = data.get('additionalNotes')
        meeting_details = data.get('meetingDetails')
        
        email_content = email_service.generate_email(
            email_type=email_type,
            student_data=student_data,
            prediction_data=prediction_data,
            additional_notes=additional_notes,
            meeting_details=meeting_details
        )
        
        return jsonify({
            'success': True,
            'email': email_content
        }), 200
        
    except Exception as e:
        print(f"❌ Error in generate_email route: {e}")
        import traceback
        traceback.print_exc()
        
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@email_bp.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'success': True,
        'service': 'Email Generation',
        'available': email_service.is_available
    }), 200
