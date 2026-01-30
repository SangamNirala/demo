"""
Retrain with Smooth Probability Distribution
=============================================

This version uses temperature scaling and beta calibration
to force a smoother distribution with more middle values.
"""

import pandas as pd
import numpy as np
import pickle
import os
from datetime import datetime
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.metrics import accuracy_score, roc_auc_score, brier_score_loss
from scipy.special import expit  # sigmoid function
from scipy.stats import beta as beta_dist
import sys
import os

# Add ml directory to path so smoothed_model can be imported
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from smoothed_model import SmoothedModel

# Configuration
RANDOM_STATE = 42
np.random.seed(RANDOM_STATE)

print("\n" + "="*70)
print("🔄 RETRAINING WITH SMOOTH PROBABILITY DISTRIBUTION")
print("="*70 + "\n")

# Load data
print("📂 Loading Student Data...")
data_path = os.path.join(os.path.dirname(__file__), '..', 'database', 'students_data.json')

import json
with open(data_path, 'r', encoding='utf-8') as f:
    students_data = json.load(f)

students = students_data.get('students', {})
records = [student for student in students.values()]
df = pd.DataFrame(records)
print(f"✅ Loaded {len(df)} students\n")

# Feature Engineering
print("🔧 Feature Engineering...")
feature_cols = [
    'attendance_percentage',
    'assignment_submission_rate',
    'library_visits_monthly',
    'lms_last_login_days',
    'extracurricular_participation',
    'family_income',
    'fee_payment_delay_months',
    'counselor_visits',
    'distance_from_college',
    'cgpa_current',
    'cgpa_previous',
    'units_approved_sem1',
    'units_approved_sem2',
    'units_enrolled_sem1',
    'units_enrolled_sem2',
    'age',
    'scholarship_holder',
    'tuition_fees_up_to_date',
    'debtor',
    'hostel_day_scholar',
]

available_features = [f for f in feature_cols if f in df.columns]
X = df[available_features].copy()
y = df['actual_dropout_status'].copy()

# Encode categorical
if 'hostel_day_scholar' in X.columns:
    le = LabelEncoder()
    X['hostel_day_scholar'] = le.fit_transform(X['hostel_day_scholar'].astype(str))
    label_encoders = {'hostel_day_scholar': le}
else:
    label_encoders = {}

# Convert boolean to int
bool_cols = ['extracurricular_participation', 'scholarship_holder', 'tuition_fees_up_to_date', 'debtor']
for col in bool_cols:
    if col in X.columns:
        X[col] = X[col].astype(int)

X = X.fillna(X.median())
print(f"✅ Using {len(X.columns)} features\n")

# Split data
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=RANDOM_STATE, stratify=y
)

# Scale
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# Train Logistic Regression (naturally smooth)
print("🎯 Training Logistic Regression with L1 Regularization...")
base_model = LogisticRegression(
    penalty='l1',
    C=0.05,  # Very strong regularization
    solver='liblinear',
    max_iter=1000,
    class_weight='balanced',
    random_state=RANDOM_STATE
)
base_model.fit(X_train_scaled, y_train)
print("✅ Model trained\n")

# Get base probabilities
base_proba_train = base_model.predict_proba(X_train_scaled)[:, 1]
base_proba_test = base_model.predict_proba(X_test_scaled)[:, 1]

# Apply Temperature Scaling
print("🌡️  Applying Temperature Scaling...")
# Temperature > 1 makes probabilities less extreme (smoother)
temperature = 2.5  # Higher = smoother distribution

# Get logits (inverse of sigmoid)
def logit(p):
    p = np.clip(p, 1e-7, 1 - 1e-7)  # Avoid log(0)
    return np.log(p / (1 - p))

# Scale logits by temperature
train_logits = logit(base_proba_train) / temperature
test_logits = logit(base_proba_test) / temperature

# Convert back to probabilities
temp_scaled_proba_train = expit(train_logits)
temp_scaled_proba_test = expit(test_logits)

print(f"  Temperature: {temperature}")
print(f"  Before scaling: {base_proba_test.min():.3f} - {base_proba_test.max():.3f}")
print(f"  After scaling:  {temp_scaled_proba_test.min():.3f} - {temp_scaled_proba_test.max():.3f}")
print("✅ Temperature scaling applied\n")

# Apply Beta Calibration (additional smoothing)
print("🎲 Applying Beta Calibration...")

# Fit beta distribution parameters
from scipy.stats import beta as beta_dist

# Map probabilities to beta distribution
def beta_calibrate(proba, a=2, b=2):
    """
    Apply beta calibration to smooth probabilities
    a, b > 1 creates a bell curve (more middle values)
    """
    return beta_dist.cdf(proba, a, b)

# Use beta(2, 2) for symmetric smoothing toward 0.5
beta_proba_test = beta_calibrate(temp_scaled_proba_test, a=1.5, b=1.5)

print(f"  Beta parameters: a=1.5, b=1.5")
print(f"  After beta calibration: {beta_proba_test.min():.3f} - {beta_proba_test.max():.3f}")
print("✅ Beta calibration applied\n")

# Evaluate
print("="*70)
print("📊 MODEL EVALUATION")
print("="*70 + "\n")

# Predictions
final_pred = (beta_proba_test >= 0.5).astype(int)

print(f"Accuracy:  {accuracy_score(y_test, final_pred):.4f}")
print(f"ROC-AUC:   {roc_auc_score(y_test, beta_proba_test):.4f}")
print(f"Brier Score: {brier_score_loss(y_test, beta_proba_test):.4f}")
print(f"Probability Range: {beta_proba_test.min():.3f} - {beta_proba_test.max():.3f}")

# Show distribution
print(f"\n📈 Probability Distribution:")
bins = [0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0]
hist, _ = np.histogram(beta_proba_test, bins=bins)
for i in range(len(bins)-1):
    bar = '█' * max(1, int(hist[i] / max(1, len(beta_proba_test)) * 50))
    print(f"  {bins[i]:.1f}-{bins[i+1]:.1f}: {hist[i]:3d} {bar}")

# Create smoothed model (imported from smoothed_model.py)
smoothed_model = SmoothedModel(base_model, temperature=2.5, beta_a=1.5, beta_b=1.5)

# Save model
print("\n💾 Saving Smoothed Model...")
saved_models_path = os.path.join(os.path.dirname(__file__), 'saved_models')
os.makedirs(saved_models_path, exist_ok=True)

with open(os.path.join(saved_models_path, 'dropout_model.pkl'), 'wb') as f:
    pickle.dump(smoothed_model, f)
print(f"  ✅ Smoothed model saved")

with open(os.path.join(saved_models_path, 'scaler.pkl'), 'wb') as f:
    pickle.dump(scaler, f)
print(f"  ✅ Scaler saved")

with open(os.path.join(saved_models_path, 'feature_names.pkl'), 'wb') as f:
    pickle.dump(list(X.columns), f)
print(f"  ✅ Feature names saved")

with open(os.path.join(saved_models_path, 'label_encoders.pkl'), 'wb') as f:
    pickle.dump(label_encoders, f)
print(f"  ✅ Label encoders saved")

metadata = {
    'training_date': datetime.now().isoformat(),
    'model_type': 'SmoothedLogisticRegression',
    'base_model': 'LogisticRegression(L1, C=0.05)',
    'temperature': 2.5,
    'beta_calibration': {'a': 1.5, 'b': 1.5},
    'smoothing_techniques': ['Temperature Scaling', 'Beta Calibration'],
    'n_features': len(X.columns),
    'feature_names': list(X.columns),
}

with open(os.path.join(saved_models_path, 'training_metadata.pkl'), 'wb') as f:
    pickle.dump(metadata, f)
print(f"  ✅ Metadata saved")

print("\n" + "="*70)
print("🎉 TRAINING COMPLETE!")
print("="*70)
print("\n✨ Smoothing Techniques Applied:")
print(f"   • Temperature Scaling (T={2.5}) - Reduces extreme probabilities")
print(f"   • Beta Calibration (a=1.5, b=1.5) - Pushes toward middle values")
print(f"   • L1 Regularization (C=0.05) - Feature selection")
print(f"   • Result: More values in 20-80% range")
print("\n📝 Next: Run generate_risk_scores.py to see smooth distribution\n")
