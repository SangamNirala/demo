"""
Student Dropout Risk Prediction System - Main Server
====================================================

This is the main Flask server that handles API requests for the
Student Dropout Risk Prediction System.

Endpoints:
    GET  /api/health              - Health check
    GET  /api/student/<roll_no>   - Get student data
    POST /api/predict/<roll_no>   - Get dropout prediction
    GET  /api/students            - List all students
"""

from flask import Flask, jsonify, request
from flask_cors import CORS
import json
import os
import sys
import traceback

# Add the backend directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Import prediction service with Gemini integration
from services.prediction_service.prediction_service import PredictionService

# Import chatbot routes
from gemini.chatbot.chatbot_routes import chatbot_bp

# Import PDF report routes
from gemini.pdf_generation.pdf_routes import pdf_bp

# Import email generation routes
from gemini.email_generation.email_routes import email_bp

# Import trend analysis routes
from routes.trend_routes import trend_bp

# Import intervention routes
from routes.intervention_routes import intervention_bp

# Initialize Flask app
app = Flask(__name__)
CORS(app)

# Register blueprints
app.register_blueprint(chatbot_bp)
app.register_blueprint(pdf_bp)
app.register_blueprint(email_bp, url_prefix='/api/email')
app.register_blueprint(trend_bp)
app.register_blueprint(intervention_bp)

# Initialize prediction service with Gemini AI enabled
print("\n" + "="*60)
print("🚀 Starting Student Dropout Prediction System")
print("="*60)

prediction_service = PredictionService(use_gemini=True)

if prediction_service.is_model_loaded():
    print("\n✅ ML Model loaded successfully!")
    if prediction_service.use_gemini:
        print("✅ Gemini AI integration enabled for personalized recommendations")
    print("   System ready to make predictions.")
else:
    print("\n⚠️  WARNING: ML Model not loaded!")
    print("   The system will run but predictions may not work correctly.")
    print("   Please ensure model files exist in backend/ml/saved_models/")

print("\n" + "="*60 + "\n")

# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def load_students():
    """Load student data from JSON file"""
    db_path = os.path.join(os.path.dirname(__file__), 'database', 'students_data.json')
    try:
        with open(db_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            return data
    except FileNotFoundError:
        print(f"❌ Error: Student database not found at {db_path}")
        return {'students': {}}
    except json.JSONDecodeError:
        print(f"❌ Error: Invalid JSON in student database")
        return {'students': {}}

# ============================================================================
# API ROUTES
# ============================================================================

@app.route('/api/health', methods=['GET'])
def health_check():
    """
    Health check endpoint
    
    Returns:
        JSON with server status and model loading status
    """
    try:
        model_loaded = False
        gemini_enabled = False
        try:
            model_loaded = prediction_service.is_model_loaded()
            gemini_enabled = prediction_service.use_gemini
        except Exception as pred_error:
            print(f"Error checking prediction service: {pred_error}")
            
        return jsonify({
            'status': 'healthy',
            'message': 'Server is running',
            'model_loaded': model_loaded,
            'gemini_enabled': gemini_enabled
        }), 200
    except Exception as e:
        print(f"Error in health check: {e}")
        traceback.print_exc()
        return jsonify({
            'status': 'error',
            'message': f'Health check failed: {str(e)}'
        }), 500


@app.route('/api/student/<roll_no>', methods=['GET'])
def get_student(roll_no):
    """
    Get student data by roll number
    
    Args:
        roll_no: Student roll number
        
    Returns:
        JSON with student data
    """
    try:
        students_data = load_students()
        students = students_data.get('students', {})
        
        if roll_no in students:
            return jsonify(students[roll_no]), 200
        else:
            return jsonify({'error': 'Student not found'}), 404
            
    except Exception as e:
        print(f"Error in get_student: {e}")
        traceback.print_exc()
        return jsonify({'error': f'Server error: {str(e)}'}), 500


@app.route('/api/students', methods=['GET'])
def list_students():
    """
    List all students with risk data
    
    Query Parameters:
        search: Optional search query
        
    Returns:
        JSON with list of all students including risk percentages
    """
    try:
        students_data = load_students()
        students = students_data.get('students', {})
        
        student_list = [
            {
                'roll_no': roll_no,
                'name': data.get('name', 'Unknown'),
                'course': data.get('course', 'N/A'),
                'year': data.get('year', 'N/A'),
                'risk_percentage': data.get('risk_percentage', 0),
                'risk_level': data.get('risk_level', 'UNKNOWN')
            }
            for roll_no, data in students.items()
        ]
        
        return jsonify({
            'total': len(student_list),
            'students': student_list
        }), 200
        
    except Exception as e:
        print(f"Error in list_students: {e}")
        traceback.print_exc()
        return jsonify({'error': f'Server error: {str(e)}'}), 500


@app.route('/api/predict/<roll_no>', methods=['POST'])
def predict_dropout(roll_no):
    """
    Predict dropout risk for a student with AI-powered recommendations
    
    Args:
        roll_no: Student roll number
        
    Returns:
        JSON with prediction results including personalized recommendations
    """
    try:
        students_data = load_students()
        students = students_data.get('students', {})
        
        if roll_no not in students:
            return jsonify({'error': 'Student not found'}), 404
        
        student_data = students[roll_no]
        
        # Make prediction using prediction service (with Gemini AI)
        prediction = prediction_service.predict_dropout_risk(student_data)
        
        if prediction.get('error'):
            return jsonify(prediction), 500
        
        return jsonify(prediction), 200
        
    except Exception as e:
        print(f"Error in predict_dropout: {e}")
        traceback.print_exc()
        return jsonify({
            'error': f'Prediction failed: {str(e)}',
            'traceback': traceback.format_exc()
        }), 500


# ============================================================================
# ERROR HANDLERS
# ============================================================================

@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors"""
    return jsonify({
        'error': 'Endpoint not found',
        'message': 'The requested endpoint does not exist'
    }), 404


@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors"""
    return jsonify({
        'error': 'Internal server error',
        'message': 'An unexpected error occurred on the server'
    }), 500


@app.errorhandler(400)
def bad_request(error):
    """Handle 400 errors"""
    return jsonify({
        'error': 'Bad request',
        'message': 'The request was invalid or malformed'
    }), 400


# ============================================================================
# MAIN
# ============================================================================

if __name__ == '__main__':
    print("="*60)
    print("🌐 Server starting on http://localhost:8001")
    print("="*60)
    print("\nAvailable endpoints:")
    print("  GET  /api/health                    - Health check")
    print("  GET  /api/student/<roll_no>         - Get student data")
    print("  GET  /api/students                  - List all students")
    print("  POST /api/predict/<roll_no>         - Get dropout prediction")
    print("  POST /api/chatbot/chat              - Chatbot conversation")
    print("  POST /api/pdf/generate/<roll_no>    - Generate PDF report")
    print("  POST /api/email/generate            - Generate personalized email")
    print("  GET  /api/trends/<roll_no>          - Get historical trends")
    print("  GET  /api/trends/<roll_no>/analysis - Get trend analysis")
    print("\n" + "="*60 + "\n")
    
    app.run(host='0.0.0.0', port=8001, debug=True)
