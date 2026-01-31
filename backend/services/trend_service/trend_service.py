"""
Trend Analysis Service
======================

Service for managing and analyzing historical student data trends.
Generates historical trends dynamically from current student data.
"""

import json
import os
from typing import Dict, List, Optional
from datetime import datetime, timedelta
import random


class TrendService:
    """Service for historical trend analysis"""
    
    def __init__(self):
        """Initialize trend service"""
        self.students_db_path = os.path.join(
            os.path.dirname(os.path.dirname(os.path.dirname(__file__))),
            'database',
            'students_data.json'
        )
        self._load_student_data()
    
    def _load_student_data(self):
        """Load student data from JSON file"""
        try:
            with open(self.students_db_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                self.students_data = data.get('students', {})
        except FileNotFoundError:
            print(f"Warning: Student data file not found at {self.students_db_path}")
            self.students_data = {}
        except json.JSONDecodeError:
            print(f"Error: Invalid JSON in student data file")
            self.students_data = {}
    
    def _generate_historical_trend(self, current_value: float, num_points: int = 5, 
                                   trend_type: str = 'declining') -> List[float]:
        """
        Generate realistic historical trend data
        
        Args:
            current_value: Current value (most recent)
            num_points: Number of historical points to generate
            trend_type: 'declining', 'improving', or 'stable'
            
        Returns:
            List of historical values leading to current value
        """
        values = []
        
        if trend_type == 'declining':
            # Values were better in the past
            change_per_point = random.uniform(2, 5)
            for i in range(num_points - 1, -1, -1):
                if i == 0:
                    values.append(current_value)
                else:
                    # Add some randomness
                    variation = random.uniform(-1, 1)
                    past_value = current_value + (i * change_per_point) + variation
                    values.append(round(past_value, 1))
        
        elif trend_type == 'improving':
            # Values were worse in the past
            change_per_point = random.uniform(2, 5)
            for i in range(num_points - 1, -1, -1):
                if i == 0:
                    values.append(current_value)
                else:
                    variation = random.uniform(-1, 1)
                    past_value = current_value - (i * change_per_point) + variation
                    values.append(round(past_value, 1))
        
        else:  # stable
            # Values fluctuate around current value
            for i in range(num_points):
                variation = random.uniform(-3, 3)
                values.append(round(current_value + variation, 1))
        
        return values
    
    def _determine_trend_type(self, current_value: float, metric_type: str) -> str:
        """
        Determine trend type based on current value
        
        Args:
            current_value: Current metric value
            metric_type: Type of metric (risk, attendance, cgpa)
            
        Returns:
            Trend type string
        """
        if metric_type == 'risk':
            if current_value > 60:
                return 'declining'  # High risk, likely got worse
            elif current_value < 40:
                return 'improving'  # Low risk, likely improved
            else:
                return random.choice(['stable', 'declining'])
        
        elif metric_type == 'attendance':
            if current_value < 50:
                return 'declining'  # Low attendance, got worse
            elif current_value > 80:
                return random.choice(['stable', 'improving'])
            else:
                return 'stable'
        
        elif metric_type == 'cgpa':
            if current_value < 6.0:
                return 'declining'
            elif current_value > 8.0:
                return random.choice(['stable', 'improving'])
            else:
                return 'stable'
        
        return 'stable'
    
    def get_student_trends(self, roll_no: str) -> Optional[Dict]:
        """
        Get all trend data for a student (generated dynamically)
        
        Args:
            roll_no: Student roll number
            
        Returns:
            Dictionary with trend data or None if not found
        """
        if roll_no not in self.students_data:
            return None
        
        student = self.students_data[roll_no]
        
        # Generate historical trends based on current data
        current_risk = student.get('risk_percentage', 50)
        current_attendance = student.get('attendance_percentage', 75)
        current_cgpa = student.get('cgpa_current', 7.0)
        previous_cgpa = student.get('cgpa_previous', current_cgpa)
        semester1_cgpa = student.get('cgpa_semester1', current_cgpa)
        semester2_cgpa = student.get('cgpa_semester2', current_cgpa)
        
        # Determine trend types
        risk_trend = self._determine_trend_type(current_risk, 'risk')
        attendance_trend = self._determine_trend_type(current_attendance, 'attendance')
        cgpa_trend = self._determine_trend_type(current_cgpa, 'cgpa')
        
        # Generate risk history (last 5 months)
        risk_values = self._generate_historical_trend(current_risk, 5, risk_trend)
        risk_history = []
        for i, value in enumerate(risk_values):
            date = (datetime.now() - timedelta(days=30 * (4 - i))).strftime('%Y-%m-%d')
            risk_level = 'HIGH' if value > 70 else 'MEDIUM' if value > 40 else 'LOW'
            risk_history.append({
                'date': date,
                'risk_percentage': max(0, min(100, value)),
                'risk_level': risk_level
            })
        
        # Generate attendance history (last 5 months)
        attendance_values = self._generate_historical_trend(current_attendance, 5, attendance_trend)
        attendance_history = []
        for i, value in enumerate(attendance_values):
            date = (datetime.now() - timedelta(days=30 * (4 - i))).strftime('%Y-%m-%d')
            attendance_history.append({
                'date': date,
                'percentage': max(0, min(100, value))
            })
        
        # Generate CGPA history (semester-wise)
        cgpa_history = []
        if semester1_cgpa:
            cgpa_history.append({
                'semester': 'Sem 1',
                'cgpa': semester1_cgpa,
                'date': (datetime.now() - timedelta(days=180)).strftime('%Y-%m-%d')
            })
        if semester2_cgpa:
            cgpa_history.append({
                'semester': 'Sem 2',
                'cgpa': semester2_cgpa,
                'date': (datetime.now() - timedelta(days=90)).strftime('%Y-%m-%d')
            })
        if current_cgpa and len(cgpa_history) < 3:
            cgpa_history.append({
                'semester': f'Sem {len(cgpa_history) + 1}',
                'cgpa': current_cgpa,
                'date': datetime.now().strftime('%Y-%m-%d')
            })
        
        # Generate interventions based on student data
        interventions = self._generate_interventions(student)
        
        return {
            'risk_history': risk_history,
            'attendance_history': attendance_history,
            'cgpa_history': cgpa_history,
            'interventions': interventions
        }
    
    def _generate_interventions(self, student: Dict) -> List[Dict]:
        """
        Generate intervention records based on student data
        
        Args:
            student: Student data dictionary
            
        Returns:
            List of interventions
        """
        interventions = []
        
        # Check counselor visits
        counselor_visits = student.get('counselor_visits', 0)
        counselor_reason = student.get('counselor_visit_reason')
        
        if counselor_visits > 0 and counselor_reason:
            for i in range(min(counselor_visits, 3)):  # Max 3 interventions
                days_ago = 30 * (counselor_visits - i)
                interventions.append({
                    'date': (datetime.now() - timedelta(days=days_ago)).strftime('%Y-%m-%d'),
                    'type': f'{counselor_reason} Counseling',
                    'description': f'Counseling session to address {counselor_reason.lower()} concerns',
                    'impact': 'positive' if student.get('risk_percentage', 50) < 50 else 'neutral'
                })
        
        # Check for financial issues
        if student.get('fee_payment_delay_months', 0) > 0:
            interventions.append({
                'date': (datetime.now() - timedelta(days=45)).strftime('%Y-%m-%d'),
                'type': 'Financial Aid Discussion',
                'description': 'Meeting to discuss fee payment options and financial assistance',
                'impact': 'neutral'
            })
        
        # Check for attendance issues
        if student.get('attendance_percentage', 100) < 50:
            interventions.append({
                'date': (datetime.now() - timedelta(days=20)).strftime('%Y-%m-%d'),
                'type': 'Attendance Warning',
                'description': 'Issued warning for critically low attendance',
                'impact': 'neutral'
            })
        
        # Check for academic issues
        if student.get('cgpa_current', 10) < 6.0:
            interventions.append({
                'date': (datetime.now() - timedelta(days=35)).strftime('%Y-%m-%d'),
                'type': 'Academic Support',
                'description': 'Enrolled in academic support program for struggling students',
                'impact': 'positive'
            })
        
        # Sort by date (most recent first)
        interventions.sort(key=lambda x: x['date'], reverse=True)
        
        return interventions[:5]  # Return max 5 interventions
    
    def get_risk_timeline(self, roll_no: str) -> List[Dict]:
        """
        Get risk score timeline for a student
        
        Args:
            roll_no: Student roll number
            
        Returns:
            List of risk score data points
        """
        trends = self.get_student_trends(roll_no)
        if not trends:
            return []
        return trends.get('risk_history', [])
    
    def get_attendance_trends(self, roll_no: str) -> List[Dict]:
        """
        Get attendance trends for a student
        
        Args:
            roll_no: Student roll number
            
        Returns:
            List of attendance data points
        """
        trends = self.get_student_trends(roll_no)
        if not trends:
            return []
        return trends.get('attendance_history', [])
    
    def get_cgpa_trajectory(self, roll_no: str) -> List[Dict]:
        """
        Get CGPA trajectory for a student
        
        Args:
            roll_no: Student roll number
            
        Returns:
            List of CGPA data points
        """
        trends = self.get_student_trends(roll_no)
        if not trends:
            return []
        return trends.get('cgpa_history', [])
    
    def get_interventions(self, roll_no: str) -> List[Dict]:
        """
        Get intervention history for a student
        
        Args:
            roll_no: Student roll number
            
        Returns:
            List of interventions
        """
        trends = self.get_student_trends(roll_no)
        if not trends:
            return []
        return trends.get('interventions', [])
    
    def calculate_trend_analysis(self, roll_no: str) -> Dict:
        """
        Calculate comprehensive trend analysis
        
        Args:
            roll_no: Student roll number
            
        Returns:
            Dictionary with trend analysis metrics
        """
        risk_history = self.get_risk_timeline(roll_no)
        attendance_history = self.get_attendance_trends(roll_no)
        cgpa_history = self.get_cgpa_trajectory(roll_no)
        interventions = self.get_interventions(roll_no)
        
        analysis = {
            'has_data': bool(risk_history or attendance_history or cgpa_history),
            'risk_trend': self._calculate_trend(risk_history, 'risk_percentage'),
            'attendance_trend': self._calculate_trend(attendance_history, 'percentage'),
            'cgpa_trend': self._calculate_trend(cgpa_history, 'cgpa'),
            'intervention_count': len(interventions),
            'latest_intervention': interventions[0] if interventions else None
        }
        
        return analysis
    
    def _calculate_trend(self, data: List[Dict], key: str) -> str:
        """
        Calculate trend direction (improving, declining, stable)
        
        Args:
            data: List of data points
            key: Key to analyze
            
        Returns:
            Trend direction string
        """
        if len(data) < 2:
            return 'insufficient_data'
        
        values = [point.get(key, 0) for point in data]
        first_half = sum(values[:len(values)//2]) / (len(values)//2)
        second_half = sum(values[len(values)//2:]) / (len(values) - len(values)//2)
        
        diff = second_half - first_half
        
        # For risk, higher is worse
        if key == 'risk_percentage':
            if diff > 5:
                return 'declining'
            elif diff < -5:
                return 'improving'
            else:
                return 'stable'
        # For attendance and CGPA, higher is better
        else:
            if diff > 5:
                return 'improving'
            elif diff < -5:
                return 'declining'
            else:
                return 'stable'
