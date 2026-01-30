"""
PDF Report Routes
=================

Flask routes for PDF report generation endpoints.
"""

from flask import Blueprint, jsonify, request, send_file
import io
import traceback
from .pdf_service import PDFReportService

# Create blueprint
pdf_bp = Blueprint('pdf', __name__, url_prefix='/api/pdf')

# Initialize service
pdf_service = PDFReportService()


@pdf_bp.route('/generate/<roll_no>', methods=['POST'])
def generate_report(roll_no):
    """
    Generate PDF report for a student
    
    Args:
        roll_no: Student roll number
        
    Request Body:
        {
            "student_data": {...},
            "prediction_data": {...}
        }
        
    Returns:
        PDF file download
    """
    try:
        # Get data from request
        data = request.get_json()
        
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        
        student_data = data.get('student_data')
        prediction_data = data.get('prediction_data')
        
        if not student_data or not prediction_data:
            return jsonify({'error': 'Missing student_data or prediction_data'}), 400
        
        # Generate PDF
        pdf_bytes = pdf_service.generate_report(student_data, prediction_data)
        
        # Create filename
        student_name = student_data.get('name', 'Student').replace(' ', '_')
        filename = f"Risk_Report_{roll_no}_{student_name}.pdf"
        
        # Send PDF file
        return send_file(
            io.BytesIO(pdf_bytes),
            mimetype='application/pdf',
            as_attachment=True,
            download_name=filename
        )
        
    except Exception as e:
        print(f"❌ Error generating PDF report: {e}")
        traceback.print_exc()
        return jsonify({
            'error': f'Failed to generate PDF report: {str(e)}',
            'traceback': traceback.format_exc()
        }), 500


@pdf_bp.route('/health', methods=['GET'])
def health_check():
    """
    Check PDF service health
    
    Returns:
        Service status
    """
    try:
        return jsonify({
            'status': 'healthy',
            'service': 'PDF Report Generation',
            'gemini_available': pdf_service.is_available
        }), 200
        
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500
