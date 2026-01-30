# Prediction function
"""
Prediction Module for Student Dropout Prediction System
========================================================

File Location: backend/ml/predict.py

This module loads the trained model and makes predictions
for individual students.

Usage:
    from ml.predict import DropoutPredictor
    
    predictor = DropoutPredictor()
    result = predictor.predict(student_data)
"""

import pandas as pd
import numpy as np
import pickle
import os
from typing import Dict, List, Any, Optional


# ============================================================================
# CONFIGURATION
# ============================================================================

class PredictConfig:
    """Configuration for prediction module"""

    # Get the directory where this file (predict.py) is located
    # This will be: backend/ml/
    BASE_PATH = os.path.dirname(os.path.abspath(__file__))
    
    # Model paths relative to this file
    # Models are in: backend/ml/saved_models/
    SAVED_MODELS_PATH = os.path.join(BASE_PATH, 'saved_models')
    
    MODEL_PATH = os.path.join(SAVED_MODELS_PATH, 'dropout_model.pkl')
    SCALER_PATH = os.path.join(SAVED_MODELS_PATH, 'scaler.pkl')
    FEATURE_NAMES_PATH = os.path.join(SAVED_MODELS_PATH, 'feature_names.pkl')
    LABEL_ENCODERS_PATH = os.path.join(SAVED_MODELS_PATH, 'label_encoders.pkl')
    METADATA_PATH = os.path.join(SAVED_MODELS_PATH, 'training_metadata.pkl')

    # Risk level thresholds
    HIGH_RISK_THRESHOLD = 70
    MEDIUM_RISK_THRESHOLD = 40


# ============================================================================
# DROPOUT PREDICTOR CLASS
# ============================================================================

class DropoutPredictor:
    """
    Main class for predicting student dropout risk
    """

    def __init__(self, config: Optional[PredictConfig] = None):
        """
        Initialize the predictor by loading model artifacts
        """
        self.config = config or PredictConfig()
        self.model = None
        self.scaler = None
        self.feature_names = None
        self.label_encoders = None
        self.metadata = None
        self.is_loaded = False

        # Print paths for debugging
        print(f"\n📁 Predict.py Configuration:")
        print(f"   BASE_PATH: {self.config.BASE_PATH}")
        print(f"   SAVED_MODELS_PATH: {self.config.SAVED_MODELS_PATH}")
        print(f"   MODEL_PATH: {self.config.MODEL_PATH}")

        # Load model artifacts
        self._load_artifacts()

    def _load_artifacts(self):
        """Load all model artifacts from saved files"""
        try:
            print("\n🔄 Loading model artifacts...")

            # Check if saved_models directory exists
            if not os.path.exists(self.config.SAVED_MODELS_PATH):
                print(f"❌ Error: saved_models directory not found at {self.config.SAVED_MODELS_PATH}")
                self.is_loaded = False
                return

            # Load model
            if not os.path.exists(self.config.MODEL_PATH):
                print(f"❌ Error: Model file not found at {self.config.MODEL_PATH}")
                self.is_loaded = False
                return
                
            with open(self.config.MODEL_PATH, 'rb') as f:
                self.model = pickle.load(f)
            print(f"   ✓ Model loaded from {self.config.MODEL_PATH}")

            # Load scaler
            if not os.path.exists(self.config.SCALER_PATH):
                print(f"❌ Error: Scaler file not found at {self.config.SCALER_PATH}")
                self.is_loaded = False
                return
                
            with open(self.config.SCALER_PATH, 'rb') as f:
                self.scaler = pickle.load(f)
            print(f"   ✓ Scaler loaded")

            # Load feature names
            if not os.path.exists(self.config.FEATURE_NAMES_PATH):
                print(f"❌ Error: Feature names file not found at {self.config.FEATURE_NAMES_PATH}")
                self.is_loaded = False
                return
                
            with open(self.config.FEATURE_NAMES_PATH, 'rb') as f:
                self.feature_names = pickle.load(f)
            print(f"   ✓ Feature names loaded ({len(self.feature_names)} features)")

            # Load label encoders
            if not os.path.exists(self.config.LABEL_ENCODERS_PATH):
                print(f"❌ Error: Label encoders file not found at {self.config.LABEL_ENCODERS_PATH}")
                self.is_loaded = False
                return
                
            with open(self.config.LABEL_ENCODERS_PATH, 'rb') as f:
                self.label_encoders = pickle.load(f)
            print(f"   ✓ Label encoders loaded")

            # Load metadata (optional - won't fail if missing)
            try:
                if os.path.exists(self.config.METADATA_PATH):
                    with open(self.config.METADATA_PATH, 'rb') as f:
                        self.metadata = pickle.load(f)
                    print(f"   ✓ Metadata loaded")
                else:
                    self.metadata = {}
                    print(f"   ⚠ Metadata file not found (optional)")
            except:
                self.metadata = {}

            self.is_loaded = True
            print("✅ All model artifacts loaded successfully!\n")

        except FileNotFoundError as e:
            print(f"❌ Error: Model file not found - {e}")
            print("   Please ensure all model files exist in backend/ml/saved_models/")
            self.is_loaded = False
        except Exception as e:
            print(f"❌ Error loading model artifacts: {e}")
            self.is_loaded = False

    def _convert_to_numeric(self, value: Any, feature_name: str) -> float:
        """
        Convert a value to numeric format
        
        Args:
            value: The value to convert
            feature_name: Name of the feature (for context)
            
        Returns:
            Numeric value
        """
        # If already numeric, return as float
        if isinstance(value, (int, float)):
            return float(value)
        
        # If None, return 0
        if value is None:
            return 0.0
        
        # Convert string values
        if isinstance(value, str):
            value_lower = value.lower().strip()
            
            # Gender conversion
            if value_lower in ['male', 'm', '1']:
                return 1.0
            elif value_lower in ['female', 'f', '0']:
                return 0.0
            
            # Boolean-like strings
            if value_lower in ['true', 'yes', '1']:
                return 1.0
            elif value_lower in ['false', 'no', '0']:
                return 0.0
            
            # Hostel/Day Scholar
            if value_lower in ['hostel', 'hosteler']:
                return 1.0
            elif value_lower in ['day scholar', 'day-scholar', 'dayscholar']:
                return 0.0
            
            # Try to convert to float
            try:
                return float(value)
            except ValueError:
                return 0.0
        
        # Convert boolean
        if isinstance(value, bool):
            return 1.0 if value else 0.0
        
        # Default
        return 0.0

    def _prepare_features(self, student_data: Dict) -> pd.DataFrame:
        """
        Prepare student data for prediction
        
        Args:
            student_data: Dictionary containing student information
            
        Returns:
            DataFrame with features ready for prediction
        """
        # Create a DataFrame with a single row
        features = {}

        # Map student_data keys to feature names
        feature_mapping = {
            # Engagement metrics
            'attendance_percentage': 'attendance_percentage',
            'assignment_submission_rate': 'assignment_submission_rate',
            'library_visits_monthly': 'library_visits_monthly',
            'lms_last_login_days': 'lms_last_login_days',
            'extracurricular_participation': 'extracurricular_participation',

            # Financial
            'family_income': 'family_income',
            'fee_payment_delay_months': 'fee_payment_delay_months',

            # Support & Logistics
            'counselor_visits': 'counselor_visits',
            'distance_from_college': 'distance_from_college_km',
            'distance_from_college_km': 'distance_from_college_km',
            'hostel_day_scholar': 'hostel_day_scholar',

            # Academic (from curricular units)
            'units_approved_sem1': 'Curricular units 1st sem (approved)',
            'units_approved_sem2': 'Curricular units 2nd sem (approved)',
            'units_enrolled_sem1': 'Curricular units 1st sem (enrolled)',
            'units_enrolled_sem2': 'Curricular units 2nd sem (enrolled)',
            'cgpa_semester1': 'Curricular units 1st sem (grade)',
            'cgpa_semester2': 'Curricular units 2nd sem (grade)',

            # Original UCI features
            'age': 'Age at enrollment',
            'scholarship_holder': 'Scholarship holder',
            'tuition_fees_up_to_date': 'Tuition fees up to date',
            'debtor': 'Debtor',
            'gender': 'Gender',
            'marital_status': 'Marital status',
        }

        # Fill in features from student_data
        for feature in self.feature_names:
            value = None

            # Try to find the value from student_data using mapping
            for key, mapped_feature in feature_mapping.items():
                if mapped_feature == feature and key in student_data:
                    value = student_data[key]
                    break

            # If still None, try direct key match
            if value is None:
                potential_keys = [
                    feature,
                    feature.lower().replace(' ', '_').replace('(', '').replace(')', ''),
                    feature.replace(' ', '_'),
                ]

                for key in potential_keys:
                    if key in student_data:
                        value = student_data[key]
                        break

            # Use default values if still None
            if value is None:
                value = self._get_default_value(feature, student_data)

            # Convert to numeric
            features[feature] = self._convert_to_numeric(value, feature)

        # Create DataFrame
        df = pd.DataFrame([features])

        # Handle hostel_day_scholar encoding using label encoder if exists
        if 'hostel_day_scholar' in df.columns and 'hostel_day_scholar' in self.label_encoders:
            encoder = self.label_encoders['hostel_day_scholar']
            original_value = student_data.get('hostel_day_scholar', 'Day Scholar')
            
            try:
                if isinstance(original_value, str):
                    df['hostel_day_scholar'] = encoder.transform([original_value])[0]
                else:
                    df['hostel_day_scholar'] = float(original_value)
            except:
                df['hostel_day_scholar'] = 0.0

        # Ensure column order matches training
        df = df[self.feature_names]

        # Ensure all values are numeric
        for col in df.columns:
            df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0)

        # Scale features
        df_scaled = pd.DataFrame(
            self.scaler.transform(df),
            columns=self.feature_names
        )

        return df_scaled

    def _get_default_value(self, feature: str, student_data: Dict) -> float:
        """Get default value for a missing feature"""
        
        # Get values from student_data with defaults
        cgpa_sem1 = student_data.get('cgpa_semester1', student_data.get('cgpa_previous', 7))
        cgpa_sem2 = student_data.get('cgpa_semester2', student_data.get('cgpa_current', 7))
        
        # Handle None values
        if cgpa_sem1 is None:
            cgpa_sem1 = 7
        if cgpa_sem2 is None:
            cgpa_sem2 = 7
        
        # Convert CGPA (0-10) to grade (0-20 scale used in UCI dataset)
        grade_sem1 = cgpa_sem1 * 2 if cgpa_sem1 <= 10 else cgpa_sem1
        grade_sem2 = cgpa_sem2 * 2 if cgpa_sem2 <= 10 else cgpa_sem2

        # Helper function to handle None values
        def get_value_or_default(key, default):
            value = student_data.get(key, default)
            return default if value is None else value

        # Default values based on feature type
        defaults = {
            # Curricular units defaults
            'Curricular units 1st sem (credited)': 0,
            'Curricular units 1st sem (enrolled)': get_value_or_default('units_enrolled_sem1', 6),
            'Curricular units 1st sem (evaluations)': 6,
            'Curricular units 1st sem (approved)': get_value_or_default('units_approved_sem1', 5),
            'Curricular units 1st sem (grade)': grade_sem1,
            'Curricular units 1st sem (without evaluations)': 0,
            'Curricular units 2nd sem (credited)': 0,
            'Curricular units 2nd sem (enrolled)': get_value_or_default('units_enrolled_sem2', 6),
            'Curricular units 2nd sem (evaluations)': 6,
            'Curricular units 2nd sem (approved)': get_value_or_default('units_approved_sem2', 5),
            'Curricular units 2nd sem (grade)': grade_sem2,
            'Curricular units 2nd sem (without evaluations)': 0,

            # Personal defaults
            'Age at enrollment': get_value_or_default('age', 18),
            'Admission grade': 120,
            'Previous qualification (grade)': 120,

            # Binary defaults
            'Displaced': 0,
            'Gender': 1 if student_data.get('gender', 'Male') in ['Male', 'M', 'm', 'male', 1, '1', True] else 0,
            'Scholarship holder': 1 if student_data.get('scholarship_holder', False) in [True, 1, '1', 'true', 'True', 'yes', 'Yes'] else 0,
            'Tuition fees up to date': 1 if student_data.get('tuition_fees_up_to_date', True) in [True, 1, '1', 'true', 'True', 'yes', 'Yes'] else 0,
            'Debtor': 1 if student_data.get('debtor', False) in [True, 1, '1', 'true', 'True', 'yes', 'Yes'] else 0,
            'Marital status': 1,
            'Daytime/evening attendance': 1,

            # Default for hostel
            'hostel_day_scholar': 0 if student_data.get('hostel_day_scholar', 'Day Scholar') in ['Day Scholar', 'day scholar', 'Day scholar', 0, '0'] else 1,
            
            # Engagement defaults
            'attendance_percentage': get_value_or_default('attendance_percentage', 75),
            'assignment_submission_rate': get_value_or_default('assignment_submission_rate', 70),
            'library_visits_monthly': get_value_or_default('library_visits_monthly', 2),
            'lms_last_login_days': get_value_or_default('lms_last_login_days', 3),
            'extracurricular_participation': 1 if student_data.get('extracurricular_participation', False) in [True, 1, '1'] else 0,
            
            # Financial defaults
            'family_income': get_value_or_default('family_income', 500000),
            'fee_payment_delay_months': get_value_or_default('fee_payment_delay_months', 0),
            
            # Support defaults
            'counselor_visits': get_value_or_default('counselor_visits', 0),
            'distance_from_college_km': get_value_or_default('distance_from_college', get_value_or_default('distance_from_college_km', 15)),
        }

        return defaults.get(feature, 0)

    def _calculate_risk_factors(self, student_data: Dict, prediction_proba: float) -> List[Dict]:
        """
        Calculate the contribution of each risk factor category
        """
        # Calculate scores for each category
        scores = {
            'academic_decline': self._calculate_academic_score(student_data),
            'low_attendance': self._calculate_attendance_score(student_data),
            'financial_stress': self._calculate_financial_score(student_data),
            'mental_health': self._calculate_mental_health_score(student_data),
            'low_engagement': self._calculate_engagement_score(student_data),
        }

        # Normalize scores to get contributions
        total_score = sum(scores.values())

        if total_score > 0:
            contributions = {k: (v / total_score) * 100 for k, v in scores.items()}
        else:
            contributions = {k: 20 for k in scores.keys()}

        # Create risk factor objects
        factor_info = {
            'academic_decline': {
                'name': 'Academic Decline',
                'icon': '📚',
                'description': 'Declining grades and poor academic performance'
            },
            'low_attendance': {
                'name': 'Low Attendance',
                'icon': '📅',
                'description': 'Irregular class attendance and LMS activity'
            },
            'financial_stress': {
                'name': 'Financial Stress',
                'icon': '💰',
                'description': 'Fee payment delays and financial difficulties'
            },
            'mental_health': {
                'name': 'Mental Health Concern',
                'icon': '🧠',
                'description': 'Counselor visits indicating stress or personal issues'
            },
            'low_engagement': {
                'name': 'Low Engagement',
                'icon': '📉',
                'description': 'Lack of participation in activities and resources'
            }
        }

        risk_factors = []
        for category, contribution in sorted(contributions.items(), key=lambda x: x[1], reverse=True):
            info = factor_info[category]
            risk_factors.append({
                'category': category,
                'name': info['name'],
                'icon': info['icon'],
                'description': info['description'],
                'contribution': round(contribution, 1),
                'score': round(scores[category], 2)
            })

        return risk_factors

    def _calculate_academic_score(self, data: Dict) -> float:
        """Calculate academic decline risk score"""
        score = 0

        # Assignment submission rate
        submission_rate = data.get('assignment_submission_rate', 50)
        if submission_rate is None:
            submission_rate = 50
        if submission_rate < 40:
            score += 3
        elif submission_rate < 60:
            score += 2
        elif submission_rate < 80:
            score += 1

        # CGPA decline
        cgpa_current = data.get('cgpa_current', 7)
        cgpa_previous = data.get('cgpa_previous', 7)
        
        if cgpa_current is None:
            cgpa_current = 7
        if cgpa_previous is None:
            cgpa_previous = 7

        if cgpa_current < cgpa_previous:
            decline = cgpa_previous - cgpa_current
            if decline > 2:
                score += 3
            elif decline > 1:
                score += 2
            else:
                score += 1

        # Low CGPA
        if cgpa_current < 5:
            score += 3
        elif cgpa_current < 6:
            score += 2
        elif cgpa_current < 7:
            score += 1

        # Units approved
        units_approved = data.get('units_approved_sem2', data.get('units_approved_sem1', 5))
        units_enrolled = data.get('units_enrolled_sem2', data.get('units_enrolled_sem1', 6))
        
        if units_approved is None:
            units_approved = 5
        if units_enrolled is None:
            units_enrolled = 6

        if units_enrolled > 0:
            approval_rate = units_approved / units_enrolled
            if approval_rate < 0.5:
                score += 3
            elif approval_rate < 0.7:
                score += 2
            elif approval_rate < 0.9:
                score += 1

        return score

    def _calculate_attendance_score(self, data: Dict) -> float:
        """Calculate attendance risk score"""
        score = 0

        # Attendance percentage
        attendance = data.get('attendance_percentage', 75)
        if attendance is None:
            attendance = 75
        if attendance < 40:
            score += 4
        elif attendance < 50:
            score += 3
        elif attendance < 65:
            score += 2
        elif attendance < 75:
            score += 1

        # LMS last login days
        lms_days = data.get('lms_last_login_days', 1)
        if lms_days is None:
            lms_days = 1
        if lms_days > 30:
            score += 3
        elif lms_days > 14:
            score += 2
        elif lms_days > 7:
            score += 1

        return score

    def _calculate_financial_score(self, data: Dict) -> float:
        """Calculate financial stress risk score"""
        score = 0

        # Fee payment delay
        delay = data.get('fee_payment_delay_months', 0)
        if delay is None:
            delay = 0
        if delay > 3:
            score += 4
        elif delay > 2:
            score += 3
        elif delay > 1:
            score += 2
        elif delay > 0:
            score += 1

        # Debtor status
        debtor = data.get('debtor', False)
        if debtor in [True, 1, '1', 'true', 'True', 'yes', 'Yes']:
            score += 2

        # Tuition fees not up to date
        tuition_up_to_date = data.get('tuition_fees_up_to_date', True)
        if tuition_up_to_date in [False, 0, '0', 'false', 'False', 'no', 'No']:
            score += 2

        # Low family income
        income = data.get('family_income', 500000)
        if income is None:
            income = 500000
        if income < 200000:
            score += 2
        elif income < 300000:
            score += 1

        # No scholarship despite low income
        scholarship = data.get('scholarship_holder', False)
        if income < 300000 and scholarship in [False, 0, '0', 'false', 'False', 'no', 'No']:
            score += 1

        return score

    def _calculate_mental_health_score(self, data: Dict) -> float:
        """Calculate mental health risk score"""
        score = 0

        # Counselor visits
        visits = data.get('counselor_visits', 0)
        if visits is None:
            visits = 0
        if visits > 4:
            score += 4
        elif visits > 2:
            score += 3
        elif visits > 1:
            score += 2
        elif visits > 0:
            score += 1

        # Counselor visit reason
        reason = data.get('counselor_visit_reason', '')
        if reason is None:
            reason = ''
        if reason in ['Stress', 'Personal', 'stress', 'personal']:
            score += 1

        return score

    def _calculate_engagement_score(self, data: Dict) -> float:
        """Calculate engagement risk score"""
        score = 0

        # Library visits
        library = data.get('library_visits_monthly', 0)
        if library is None:
            library = 0
        if library == 0:
            score += 2
        elif library < 2:
            score += 1

        # Extracurricular participation
        extracurricular = data.get('extracurricular_participation', False)
        if extracurricular in [False, 0, '0', 'false', 'False', 'no', 'No']:
            score += 2

        # LMS login
        lms_days = data.get('lms_last_login_days', 1)
        if lms_days is None:
            lms_days = 1
        if lms_days > 14:
            score += 2
        elif lms_days > 7:
            score += 1

        return score

    def _get_risk_level(self, risk_percentage: float) -> Dict:
        """Determine risk level based on percentage"""
        if risk_percentage >= self.config.HIGH_RISK_THRESHOLD:
            return {
                'level': 'HIGH',
                'color': 'red',
                'emoji': '🔴',
                'description': 'Immediate intervention required'
            }
        elif risk_percentage >= self.config.MEDIUM_RISK_THRESHOLD:
            return {
                'level': 'MEDIUM',
                'color': 'orange',
                'emoji': '🟡',
                'description': 'Close monitoring recommended'
            }
        else:
            return {
                'level': 'LOW',
                'color': 'green',
                'emoji': '🟢',
                'description': 'Student appears to be on track'
            }

    def _get_recommendations(self, risk_factors: List[Dict], risk_percentage: float) -> List[Dict]:
        """Generate intervention recommendations based on risk factors"""
        recommendations = []

        # Get top risk categories
        top_factors = [rf['category'] for rf in risk_factors[:3]]

        # Recommendation templates
        all_recommendations = {
            'academic_decline': [
                {
                    'id': 1,
                    'priority': 'high',
                    'icon': '📚',
                    'title': 'Assign Academic Mentor',
                    'description': 'Pair student with a peer mentor for academic support and study guidance.',
                    'action': 'assign_mentor'
                },
                {
                    'id': 2,
                    'priority': 'medium',
                    'icon': '📝',
                    'title': 'Academic Counseling Session',
                    'description': 'Schedule a session with academic advisor to discuss study strategies.',
                    'action': 'schedule_academic_counseling'
                }
            ],
            'low_attendance': [
                {
                    'id': 3,
                    'priority': 'high',
                    'icon': '📞',
                    'title': 'Contact Student',
                    'description': 'Reach out to understand reasons for low attendance.',
                    'action': 'contact_student'
                },
                {
                    'id': 4,
                    'priority': 'medium',
                    'icon': '👨‍👩‍👦',
                    'title': 'Parent Meeting',
                    'description': 'Schedule a meeting with parents to discuss attendance concerns.',
                    'action': 'schedule_parent_meeting'
                }
            ],
            'financial_stress': [
                {
                    'id': 5,
                    'priority': 'high',
                    'icon': '💰',
                    'title': 'Financial Aid Review',
                    'description': 'Connect with Financial Aid office for scholarship or fee waiver options.',
                    'action': 'financial_aid_review'
                },
                {
                    'id': 6,
                    'priority': 'medium',
                    'icon': '📋',
                    'title': 'Payment Plan',
                    'description': 'Discuss flexible payment plan options with accounts department.',
                    'action': 'setup_payment_plan'
                }
            ],
            'mental_health': [
                {
                    'id': 7,
                    'priority': 'high',
                    'icon': '🧠',
                    'title': 'Counselor Referral',
                    'description': 'Refer to mental health counselor for follow-up session.',
                    'action': 'counselor_referral'
                },
                {
                    'id': 8,
                    'priority': 'medium',
                    'icon': '🤝',
                    'title': 'Peer Support Group',
                    'description': 'Connect with peer support group or student wellness program.',
                    'action': 'peer_support'
                }
            ],
            'low_engagement': [
                {
                    'id': 9,
                    'priority': 'medium',
                    'icon': '🎯',
                    'title': 'Activity Recommendation',
                    'description': 'Encourage participation in clubs or extracurricular activities.',
                    'action': 'recommend_activities'
                },
                {
                    'id': 10,
                    'priority': 'low',
                    'icon': '📖',
                    'title': 'Library Resources',
                    'description': 'Introduce student to library resources and study groups.',
                    'action': 'library_orientation'
                }
            ]
        }

        # Add recommendations based on top risk factors
        for factor in top_factors:
            if factor in all_recommendations:
                recommendations.extend(all_recommendations[factor])

        # Add general high-risk recommendation
        if risk_percentage >= self.config.HIGH_RISK_THRESHOLD:
            recommendations.insert(0, {
                'id': 0,
                'priority': 'urgent',
                'icon': '🚨',
                'title': 'Immediate Intervention Required',
                'description': 'Schedule urgent meeting with student, advisor, and support team.',
                'action': 'urgent_intervention'
            })

        # Remove duplicates and limit to top 5
        seen_ids = set()
        unique_recommendations = []
        for rec in recommendations:
            if rec['id'] not in seen_ids:
                seen_ids.add(rec['id'])
                unique_recommendations.append(rec)

        return unique_recommendations[:5]

    def predict(self, student_data: Dict) -> Dict:
        """
        Predict dropout risk for a student
        
        Args:
            student_data: Dictionary containing student information
            
        Returns:
            Prediction result dictionary
        """
        if not self.is_loaded:
            return {
                'error': True,
                'message': 'Model not loaded. Please ensure all model files exist in backend/ml/saved_models/'
            }

        try:
            # Prepare features
            features = self._prepare_features(student_data)

            # Get prediction probability
            proba = self.model.predict_proba(features)[0]
            dropout_probability = proba[1]  # Probability of class 1 (dropout)

            # Convert to percentage
            risk_percentage = round(dropout_probability * 100, 1)

            # Get risk level
            risk_level_info = self._get_risk_level(risk_percentage)

            # Calculate risk factors
            risk_factors = self._calculate_risk_factors(student_data, dropout_probability)

            # Get recommendations
            recommendations = self._get_recommendations(risk_factors, risk_percentage)

            # Prepare student info for display
            student_info = {
                'name': student_data.get('name', 'Unknown'),
                'roll_no': student_data.get('roll_no', student_data.get('student_id', 'N/A')),
                'course': student_data.get('course', 'N/A'),
                'year': student_data.get('year_string', f"Year {student_data.get('year', 'N/A')}"),
            }

            # Build result
            result = {
                'error': False,
                'student_info': student_info,
                'risk_level': risk_level_info['level'],
                'risk_level_info': risk_level_info,
                'risk_percentage': risk_percentage,
                'risk_factors': risk_factors,
                'recommendations': recommendations,
                'prediction_details': {
                    'dropout_probability': round(dropout_probability, 4),
                    'safe_probability': round(proba[0], 4),
                    'model_confidence': round(max(proba) * 100, 1)
                }
            }

            return result

        except Exception as e:
            import traceback
            return {
                'error': True,
                'message': f'Prediction failed: {str(e)}',
                'traceback': traceback.format_exc()
            }

    def predict_from_roll_no(self, roll_no: str, students_data: Dict) -> Dict:
        """Predict dropout risk using roll number"""
        if roll_no in students_data.get('students', {}):
            student_data = students_data['students'][roll_no]
            return self.predict(student_data)
        else:
            return {
                'error': True,
                'message': f'Student with roll number {roll_no} not found.'
            }


# ============================================================================
# STANDALONE TESTING
# ============================================================================

if __name__ == "__main__":
    """Test the predictor when running this file directly"""
    
    print("=" * 60)
    print("🔮 DROPOUT PREDICTION - STANDALONE TEST")
    print("=" * 60)
    
    # Initialize predictor
    predictor = DropoutPredictor()
    
    if not predictor.is_loaded:
        print("\n❌ Cannot run test - model not loaded")
        print("\nPlease ensure these files exist:")
        print("  - backend/ml/saved_models/dropout_model.pkl")
        print("  - backend/ml/saved_models/scaler.pkl")
        print("  - backend/ml/saved_models/feature_names.pkl")
        print("  - backend/ml/saved_models/label_encoders.pkl")
        exit(1)
    
    # Test with high risk student
    high_risk_student = {
        'student_id': '2023CS001',
        'name': 'Rahul Sharma',
        'roll_no': '2023CS001',
        'course': 'B.Tech Computer Science',
        'year': 2,
        'year_string': '2nd Year',
        'gender': 'Male',
        'age': 20,
        'attendance_percentage': 42.3,
        'assignment_submission_rate': 35.0,
        'library_visits_monthly': 0,
        'lms_last_login_days': 18,
        'extracurricular_participation': False,
        'family_income': 280000,
        'fee_payment_delay_months': 3,
        'scholarship_holder': False,
        'tuition_fees_up_to_date': False,
        'debtor': True,
        'counselor_visits': 3,
        'counselor_visit_reason': 'Stress',
        'distance_from_college': 45.0,
        'hostel_day_scholar': 'Day Scholar',
        'cgpa_current': 5.2,
        'cgpa_previous': 6.8,
        'cgpa_semester1': 6.8,
        'cgpa_semester2': 5.2,
        'units_enrolled_sem1': 6,
        'units_approved_sem1': 4,
        'units_enrolled_sem2': 6,
        'units_approved_sem2': 2,
    }
    
    # Test with low risk student
    low_risk_student = {
        'student_id': '2022EC045',
        'name': 'Priya Patel',
        'roll_no': '2022EC045',
        'course': 'B.Tech Electronics',
        'year': 3,
        'year_string': '3rd Year',
        'gender': 'Female',
        'age': 21,
        'attendance_percentage': 88.5,
        'assignment_submission_rate': 92.0,
        'library_visits_monthly': 6,
        'lms_last_login_days': 1,
        'extracurricular_participation': True,
        'family_income': 650000,
        'fee_payment_delay_months': 0,
        'scholarship_holder': True,
        'tuition_fees_up_to_date': True,
        'debtor': False,
        'counselor_visits': 0,
        'distance_from_college': 12.0,
        'hostel_day_scholar': 'Day Scholar',
        'cgpa_current': 8.4,
        'cgpa_previous': 8.1,
        'cgpa_semester1': 8.1,
        'cgpa_semester2': 8.4,
        'units_enrolled_sem1': 6,
        'units_approved_sem1': 6,
        'units_enrolled_sem2': 6,
        'units_approved_sem2': 6,
    }
    
    # Run predictions
    print("\n" + "=" * 60)
    print("TEST 1: HIGH RISK STUDENT")
    print("=" * 60)
    
    result1 = predictor.predict(high_risk_student)
    
    if result1.get('error'):
        print(f"\n❌ Error: {result1.get('message')}")
    else:
        print(f"\n👤 Student: {result1['student_info']['name']} ({result1['student_info']['roll_no']})")
        print(f"📚 Course: {result1['student_info']['course']} - {result1['student_info']['year']}")
        print(f"\n🎯 Risk Level: {result1['risk_level_info']['emoji']} {result1['risk_level']} ({result1['risk_percentage']}%)")
        print(f"\n📊 Risk Factors:")
        for factor in result1['risk_factors']:
            print(f"   {factor['icon']} {factor['name']}: {factor['contribution']}%")
        print(f"\n💡 Recommendations:")
        for i, rec in enumerate(result1['recommendations'], 1):
            print(f"   {i}. {rec['icon']} {rec['title']}")
    
    print("\n" + "=" * 60)
    print("TEST 2: LOW RISK STUDENT")
    print("=" * 60)
    
    result2 = predictor.predict(low_risk_student)
    
    if result2.get('error'):
        print(f"\n❌ Error: {result2.get('message')}")
    else:
        print(f"\n👤 Student: {result2['student_info']['name']} ({result2['student_info']['roll_no']})")
        print(f"📚 Course: {result2['student_info']['course']} - {result2['student_info']['year']}")
        print(f"\n🎯 Risk Level: {result2['risk_level_info']['emoji']} {result2['risk_level']} ({result2['risk_percentage']}%)")
        print(f"\n📊 Risk Factors:")
        for factor in result2['risk_factors']:
            print(f"   {factor['icon']} {factor['name']}: {factor['contribution']}%")
    
    print("\n" + "=" * 60)
    print("✅ STANDALONE TEST COMPLETE!")
    print("=" * 60)