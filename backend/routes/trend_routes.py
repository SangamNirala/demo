"""
Trend Analysis Routes
=====================

API routes for historical trend analysis.
"""

from flask import Blueprint, jsonify, request
from services.trend_service.trend_service import TrendService
import traceback

# Create blueprint
trend_bp = Blueprint('trend', __name__, url_prefix='/api/trends')

# Initialize service
trend_service = TrendService()


@trend_bp.route('/<roll_no>', methods=['GET'])
def get_student_trends(roll_no):
    """
    Get all trend data for a student
    
    Args:
        roll_no: Student roll number
        
    Returns:
        JSON with complete trend data
    """
    try:
        trends = trend_service.get_student_trends(roll_no)
        
        if not trends:
            return jsonify({
                'error': 'No historical data found for this student',
                'has_data': False
            }), 404
        
        return jsonify({
            'roll_no': roll_no,
            'has_data': True,
            'data': trends
        }), 200
        
    except Exception as e:
        print(f"Error in get_student_trends: {e}")
        traceback.print_exc()
        return jsonify({'error': f'Server error: {str(e)}'}), 500


@trend_bp.route('/<roll_no>/risk', methods=['GET'])
def get_risk_timeline(roll_no):
    """
    Get risk score timeline
    
    Args:
        roll_no: Student roll number
        
    Returns:
        JSON with risk timeline data
    """
    try:
        risk_history = trend_service.get_risk_timeline(roll_no)
        
        return jsonify({
            'roll_no': roll_no,
            'risk_timeline': risk_history
        }), 200
        
    except Exception as e:
        print(f"Error in get_risk_timeline: {e}")
        traceback.print_exc()
        return jsonify({'error': f'Server error: {str(e)}'}), 500


@trend_bp.route('/<roll_no>/attendance', methods=['GET'])
def get_attendance_trends(roll_no):
    """
    Get attendance trends
    
    Args:
        roll_no: Student roll number
        
    Returns:
        JSON with attendance trend data
    """
    try:
        attendance_history = trend_service.get_attendance_trends(roll_no)
        
        return jsonify({
            'roll_no': roll_no,
            'attendance_trends': attendance_history
        }), 200
        
    except Exception as e:
        print(f"Error in get_attendance_trends: {e}")
        traceback.print_exc()
        return jsonify({'error': f'Server error: {str(e)}'}), 500


@trend_bp.route('/<roll_no>/cgpa', methods=['GET'])
def get_cgpa_trajectory(roll_no):
    """
    Get CGPA trajectory
    
    Args:
        roll_no: Student roll number
        
    Returns:
        JSON with CGPA trajectory data
    """
    try:
        cgpa_history = trend_service.get_cgpa_trajectory(roll_no)
        
        return jsonify({
            'roll_no': roll_no,
            'cgpa_trajectory': cgpa_history
        }), 200
        
    except Exception as e:
        print(f"Error in get_cgpa_trajectory: {e}")
        traceback.print_exc()
        return jsonify({'error': f'Server error: {str(e)}'}), 500


@trend_bp.route('/<roll_no>/interventions', methods=['GET'])
def get_interventions(roll_no):
    """
    Get intervention history
    
    Args:
        roll_no: Student roll number
        
    Returns:
        JSON with intervention history
    """
    try:
        interventions = trend_service.get_interventions(roll_no)
        
        return jsonify({
            'roll_no': roll_no,
            'interventions': interventions
        }), 200
        
    except Exception as e:
        print(f"Error in get_interventions: {e}")
        traceback.print_exc()
        return jsonify({'error': f'Server error: {str(e)}'}), 500


@trend_bp.route('/<roll_no>/analysis', methods=['GET'])
def get_trend_analysis(roll_no):
    """
    Get comprehensive trend analysis
    
    Args:
        roll_no: Student roll number
        
    Returns:
        JSON with trend analysis metrics
    """
    try:
        analysis = trend_service.calculate_trend_analysis(roll_no)
        
        return jsonify({
            'roll_no': roll_no,
            'analysis': analysis
        }), 200
        
    except Exception as e:
        print(f"Error in get_trend_analysis: {e}")
        traceback.print_exc()
        return jsonify({'error': f'Server error: {str(e)}'}), 500


@trend_bp.route('/<roll_no>/interventions', methods=['POST'])
def add_intervention(roll_no):
    """
    Add a new intervention record
    
    Args:
        roll_no: Student roll number
        
    Request Body:
        {
            "date": "2024-01-30",
            "type": "Academic Counseling",
            "description": "Description of intervention",
            "impact": "positive|neutral|negative"
        }
        
    Returns:
        JSON with success status
    """
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        
        required_fields = ['date', 'type', 'description', 'impact']
        for field in required_fields:
            if field not in data:
                return jsonify({'error': f'Missing required field: {field}'}), 400
        
        success = trend_service.add_intervention(roll_no, data)
        
        if success:
            return jsonify({
                'success': True,
                'message': 'Intervention added successfully'
            }), 201
        else:
            return jsonify({
                'success': False,
                'error': 'Failed to add intervention'
            }), 500
        
    except Exception as e:
        print(f"Error in add_intervention: {e}")
        traceback.print_exc()
        return jsonify({'error': f'Server error: {str(e)}'}), 500
