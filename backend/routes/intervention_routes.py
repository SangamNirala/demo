"""
Intervention Tracking Routes
=============================

API endpoints for managing student interventions.
"""

from flask import Blueprint, request, jsonify
import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from services.intervention_service.intervention_service import InterventionService

# Create blueprint
intervention_bp = Blueprint('interventions', __name__, url_prefix='/api/interventions')

# Initialize service
intervention_service = InterventionService()


@intervention_bp.route('', methods=['POST'])
def create_intervention():
    """
    Create a new intervention
    
    Request Body:
        {
            "student_id": "string",
            "type": "string",
            "status": "string",
            "assigned_to": "string",
            "scheduled_date": "string (ISO format)",
            "notes": "string",
            "outcome": "string"
        }
    
    Returns:
        Created intervention with ID
    """
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        
        # Validate required fields
        required_fields = ['student_id', 'type', 'status', 'assigned_to']
        missing_fields = [field for field in required_fields if field not in data]
        
        if missing_fields:
            return jsonify({
                'error': f'Missing required fields: {", ".join(missing_fields)}'
            }), 400
        
        intervention = intervention_service.create_intervention(data)
        
        if not intervention:
            return jsonify({'error': 'Failed to create intervention'}), 500
        
        return jsonify({
            'success': True,
            'intervention': intervention
        }), 201
        
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        print(f"Error creating intervention: {e}")
        return jsonify({'error': f'Server error: {str(e)}'}), 500


@intervention_bp.route('/<int:intervention_id>', methods=['GET'])
def get_intervention(intervention_id):
    """
    Get intervention by ID
    
    Args:
        intervention_id: Intervention ID
    
    Returns:
        Intervention data
    """
    try:
        intervention = intervention_service.get_intervention(intervention_id)
        
        if not intervention:
            return jsonify({'error': 'Intervention not found'}), 404
        
        return jsonify(intervention), 200
        
    except Exception as e:
        print(f"Error fetching intervention: {e}")
        return jsonify({'error': f'Server error: {str(e)}'}), 500


@intervention_bp.route('/student/<student_id>', methods=['GET'])
def get_student_interventions(student_id):
    """
    Get all interventions for a student
    
    Args:
        student_id: Student roll number
    
    Returns:
        List of interventions
    """
    try:
        interventions = intervention_service.get_student_interventions(student_id)
        
        return jsonify({
            'success': True,
            'total': len(interventions),
            'interventions': interventions
        }), 200
        
    except Exception as e:
        print(f"Error fetching student interventions: {e}")
        return jsonify({'error': f'Server error: {str(e)}'}), 500


@intervention_bp.route('/<int:intervention_id>', methods=['PUT'])
def update_intervention(intervention_id):
    """
    Update an intervention
    
    Args:
        intervention_id: Intervention ID
    
    Request Body:
        Fields to update (status, notes, outcome, etc.)
    
    Returns:
        Updated intervention
    """
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        
        intervention = intervention_service.update_intervention(intervention_id, data)
        
        if not intervention:
            return jsonify({'error': 'Intervention not found or update failed'}), 404
        
        return jsonify({
            'success': True,
            'intervention': intervention
        }), 200
        
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        print(f"Error updating intervention: {e}")
        return jsonify({'error': f'Server error: {str(e)}'}), 500


@intervention_bp.route('/<int:intervention_id>', methods=['DELETE'])
def delete_intervention(intervention_id):
    """
    Delete an intervention
    
    Args:
        intervention_id: Intervention ID
    
    Returns:
        Success status
    """
    try:
        success = intervention_service.delete_intervention(intervention_id)
        
        if not success:
            return jsonify({'error': 'Intervention not found or delete failed'}), 404
        
        return jsonify({
            'success': True,
            'message': 'Intervention deleted successfully'
        }), 200
        
    except Exception as e:
        print(f"Error deleting intervention: {e}")
        return jsonify({'error': f'Server error: {str(e)}'}), 500


@intervention_bp.route('/mark-contacted', methods=['POST'])
def mark_as_contacted():
    """
    Quick action: Mark student as contacted
    
    Request Body:
        {
            "student_id": "string",
            "contacted_by": "string",
            "notes": "string (optional)"
        }
    
    Returns:
        Created intervention
    """
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        
        # Validate required fields
        if 'student_id' not in data or 'contacted_by' not in data:
            return jsonify({
                'error': 'Missing required fields: student_id, contacted_by'
            }), 400
        
        intervention = intervention_service.mark_as_contacted(
            student_id=data['student_id'],
            contacted_by=data['contacted_by'],
            notes=data.get('notes', '')
        )
        
        if not intervention:
            return jsonify({'error': 'Failed to mark as contacted'}), 500
        
        return jsonify({
            'success': True,
            'intervention': intervention
        }), 201
        
    except Exception as e:
        print(f"Error marking as contacted: {e}")
        return jsonify({'error': f'Server error: {str(e)}'}), 500


@intervention_bp.route('/statistics/<student_id>', methods=['GET'])
def get_statistics(student_id):
    """
    Get intervention statistics for a student
    
    Args:
        student_id: Student roll number
    
    Returns:
        Statistics dictionary
    """
    try:
        stats = intervention_service.get_statistics(student_id)
        
        return jsonify({
            'success': True,
            'statistics': stats
        }), 200
        
    except Exception as e:
        print(f"Error fetching statistics: {e}")
        return jsonify({'error': f'Server error: {str(e)}'}), 500


@intervention_bp.route('/all', methods=['GET'])
def get_all_interventions():
    """
    Get all interventions with optional filters
    
    Query Parameters:
        status: Filter by status
        type: Filter by type
        assigned_to: Filter by assigned person
        student_id: Filter by student
    
    Returns:
        List of interventions
    """
    try:
        filters = {}
        
        # Get query parameters
        if request.args.get('status'):
            filters['status'] = request.args.get('status')
        if request.args.get('type'):
            filters['type'] = request.args.get('type')
        if request.args.get('assigned_to'):
            filters['assigned_to'] = request.args.get('assigned_to')
        if request.args.get('student_id'):
            filters['student_id'] = request.args.get('student_id')
        
        interventions = intervention_service.get_all_interventions(filters)
        
        return jsonify({
            'success': True,
            'total': len(interventions),
            'interventions': interventions
        }), 200
        
    except Exception as e:
        print(f"Error fetching all interventions: {e}")
        return jsonify({'error': f'Server error: {str(e)}'}), 500
