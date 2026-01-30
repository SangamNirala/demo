from flask import Flask, jsonify, request
from flask_cors import CORS
import json
import os

app = Flask(__name__)
CORS(app)

# Load student data
def load_students():
    db_path = os.path.join(os.path.dirname(__file__), 'database', 'students_data.json')
    with open(db_path, 'r', encoding='utf-8') as f:
        return json.load(f)

# Mock prediction logic
def calculate_risk(student_data):
    risk_score = 0
    factors = []
    
    # Attendance factor
    if student_data['attendance'] < 60:
        contribution = 35
        risk_score += contribution
        factors.append({
            'name': 'Academic Decline',
            'contribution': contribution
        })
    elif student_data['attendance'] < 75:
        contribution = 20
        risk_score += contribution
        factors.append({
            'name': 'Low Attendance',
            'contribution': contribution
        })
    
    # CGPA decline factor
    if student_data['currentCGPA'] < student_data['previousCGPA']:
        contribution = 25
        risk_score += contribution
        factors.append({
            'name': 'Grade Decline',
            'contribution': contribution
        })
    
    # Financial stress
    if 'delayed' in student_data['feeStatus'].lower():
        contribution = 20
        risk_score += contribution
        factors.append({
            'name': 'Financial Stress',
            'contribution': contribution
        })
    
    # Mental health
    if 'stress' in student_data['counselorVisits'].lower() or 'anxiety' in student_data['counselorVisits'].lower():
        contribution = 15
        risk_score += contribution
        factors.append({
            'name': 'Mental Health Concern',
            'contribution': contribution
        })
    
    # Low engagement
    if student_data['extracurricular'] == 'No participation':
        contribution = 5
        risk_score += contribution
        factors.append({
            'name': 'Low Engagement',
            'contribution': contribution
        })
    
    # Determine risk level
    if risk_score >= 70:
        risk_level = 'HIGH'
    elif risk_score >= 40:
        risk_level = 'MEDIUM'
    else:
        risk_level = 'LOW'
    
    # Generate recommendations
    recommendations = []
    
    if any('Academic' in f['name'] or 'Grade' in f['name'] for f in factors):
        recommendations.append({
            'icon': '📞',
            'text': 'Schedule a meeting with academic advisor'
        })
        recommendations.append({
            'icon': '📚',
            'text': 'Assign a peer mentor for academic support'
        })
    
    if any('Financial' in f['name'] for f in factors):
        recommendations.append({
            'icon': '💰',
            'text': 'Connect with Financial Aid office for scholarship/fee waiver options'
        })
    
    if any('Mental Health' in f['name'] for f in factors):
        recommendations.append({
            'icon': '🧠',
            'text': 'Refer to mental health counselor for follow-up session'
        })
    
    if any('Attendance' in f['name'] for f in factors):
        recommendations.append({
            'icon': '📊',
            'text': 'Monitor attendance closely and send regular reminders'
        })
    
    if any('Engagement' in f['name'] for f in factors):
        recommendations.append({
            'icon': '🎯',
            'text': 'Encourage participation in extracurricular activities'
        })
    
    recommendations.append({
        'icon': '👨‍👩‍👦',
        'text': 'Contact parents for a discussion'
    })
    
    return {
        'riskLevel': risk_level,
        'riskPercentage': min(risk_score, 100),
        'riskFactors': factors,
        'recommendations': recommendations
    }

@app.route('/api/student/<roll_no>', methods=['GET'])
def get_student(roll_no):
    students = load_students()
    
    if roll_no in students:
        return jsonify(students[roll_no]), 200
    else:
        return jsonify({'error': 'Student not found'}), 404

@app.route('/api/predict/<roll_no>', methods=['POST'])
def predict_dropout(roll_no):
    students = load_students()
    
    if roll_no in students:
        student_data = students[roll_no]
        prediction = calculate_risk(student_data)
        return jsonify(prediction), 200
    else:
        return jsonify({'error': 'Student not found'}), 404

@app.route('/api/health', methods=['GET'])
def health_check():
    return jsonify({'status': 'healthy', 'message': 'Server is running'}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)
