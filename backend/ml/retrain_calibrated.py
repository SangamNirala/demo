"""
Retrain Model with Calibrated Probabilities
============================================

This script retrains the model with probability calibration
to get more realistic risk scores in the 0-100% range.
"""

import pandas as pd
import numpy as np
import pickle
import os
from datetime import datetime
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.ensemble import RandomForestClassifier
from sklearn.calibration import CalibratedClassifierCV
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score, 
    f1_score, roc_auc_score, brier_score_loss
)

# Configuration
RANDOM_STATE = 42
np.random.seed(RANDOM_STATE)

print("\n" + "="*70)
print("🔄 RETRAINING MODEL WITH CALIBRATED PROBABILITIES")
print("="*70 + "\n")

# Step 1: Load the students data to use as training data
print("📂 Step 1: Loading Student Data...")
data_path = os.path.join(os.path.dirname(__file__), '..', 'database', 'students_data.json')

import json
with open(data_path, 'r', encoding='utf-8') as f:
    students_data = json.load(f)

students = students_data.get('students', {})
print(f"✅ Loaded {len(students)} students\n")

# Step 2: Convert to DataFrame
print("🔄 Step 2: Converting to DataFrame...")
records = []
for roll_no, student in students.items():
    records.append(student)

df = pd.DataFrame(records)
print(f"✅ Created DataFrame with {len(df)} rows and {len(df.columns)} columns\n")

# Step 3: Feature Engineering
print("🔧 Step 3: Feature Engineering...")

# Select features
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

# Check which features exist
available_features = [f for f in feature_cols if f in df.columns]
print(f"  Using {len(available_features)} features")

# Prepare X and y
X = df[available_features].copy()
y = df['actual_dropout_status'].copy()

# Handle categorical: hostel_day_scholar
if 'hostel_day_scholar' in X.columns:
    le = LabelEncoder()
    X['hostel_day_scholar'] = le.fit_transform(X['hostel_day_scholar'].astype(str))
    label_encoders = {'hostel_day_scholar': le}
else:
    label_encoders = {}

# Convert boolean columns to int
bool_cols = ['extracurricular_participation', 'scholarship_holder', 'tuition_fees_up_to_date', 'debtor']
for col in bool_cols:
    if col in X.columns:
        X[col] = X[col].astype(int)

# Fill missing values
X = X.fillna(X.median())

print(f"✅ Features prepared\n")

# Step 4: Split data
print("✂️  Step 4: Splitting Data...")
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=RANDOM_STATE, stratify=y
)
print(f"  Training set: {len(X_train)} samples")
print(f"  Test set: {len(X_test)} samples")
print(f"  Dropout rate in training: {y_train.mean()*100:.1f}%")
print(f"  Dropout rate in test: {y_test.mean()*100:.1f}%\n")

# Step 5: Scale features
print("📏 Step 5: Scaling Features...")
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)
print(f"✅ Features scaled\n")

# Step 6: Train base Random Forest
print("🌲 Step 6: Training Base Random Forest...")
base_rf = RandomForestClassifier(
    n_estimators=100,
    max_depth=15,
    min_samples_split=5,
    min_samples_leaf=2,
    max_features='sqrt',
    class_weight='balanced',
    random_state=RANDOM_STATE,
    n_jobs=-1
)
base_rf.fit(X_train_scaled, y_train)
print(f"✅ Base model trained\n")

# Step 7: Calibrate probabilities
print("🎯 Step 7: Calibrating Probabilities...")
print("  Using Isotonic Regression for calibration...")
calibrated_rf = CalibratedClassifierCV(
    base_rf,
    method='isotonic',  # or 'sigmoid'
    cv=5
)
calibrated_rf.fit(X_train_scaled, y_train)
print(f"✅ Model calibrated\n")

# Step 8: Evaluate both models
print("="*70)
print("📊 MODEL EVALUATION")
print("="*70 + "\n")

# Base model predictions
y_pred_base = base_rf.predict(X_test_scaled)
y_proba_base = base_rf.predict_proba(X_test_scaled)[:, 1]

# Calibrated model predictions
y_pred_cal = calibrated_rf.predict(X_test_scaled)
y_proba_cal = calibrated_rf.predict_proba(X_test_scaled)[:, 1]

# Metrics for base model
print("🔹 BASE MODEL (Uncalibrated):")
print(f"  Accuracy:  {accuracy_score(y_test, y_pred_base):.4f}")
print(f"  Precision: {precision_score(y_test, y_pred_base):.4f}")
print(f"  Recall:    {recall_score(y_test, y_pred_base):.4f}")
print(f"  F1 Score:  {f1_score(y_test, y_pred_base):.4f}")
print(f"  ROC-AUC:   {roc_auc_score(y_test, y_proba_base):.4f}")
print(f"  Brier Score: {brier_score_loss(y_test, y_proba_base):.4f} (lower is better)")
print(f"  Probability Range: {y_proba_base.min():.3f} - {y_proba_base.max():.3f}")

print(f"\n🔸 CALIBRATED MODEL:")
print(f"  Accuracy:  {accuracy_score(y_test, y_pred_cal):.4f}")
print(f"  Precision: {precision_score(y_test, y_pred_cal):.4f}")
print(f"  Recall:    {recall_score(y_test, y_pred_cal):.4f}")
print(f"  F1 Score:  {f1_score(y_test, y_pred_cal):.4f}")
print(f"  ROC-AUC:   {roc_auc_score(y_test, y_proba_cal):.4f}")
print(f"  Brier Score: {brier_score_loss(y_test, y_proba_cal):.4f} (lower is better)")
print(f"  Probability Range: {y_proba_cal.min():.3f} - {y_proba_cal.max():.3f}")

# Show probability distribution
print(f"\n📈 Probability Distribution (Calibrated Model):")
bins = [0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0]
hist, _ = np.histogram(y_proba_cal, bins=bins)
for i in range(len(bins)-1):
    bar = '█' * int(hist[i] / len(y_proba_cal) * 50)
    print(f"  {bins[i]:.1f}-{bins[i+1]:.1f}: {hist[i]:3d} {bar}")

print("\n" + "="*70 + "\n")

# Step 9: Save the calibrated model
print("💾 Step 9: Saving Calibrated Model...")

saved_models_path = os.path.join(os.path.dirname(__file__), 'saved_models')
os.makedirs(saved_models_path, exist_ok=True)

# Save calibrated model
model_path = os.path.join(saved_models_path, 'dropout_model.pkl')
with open(model_path, 'wb') as f:
    pickle.dump(calibrated_rf, f)
print(f"  ✅ Model saved: {model_path}")

# Save scaler
scaler_path = os.path.join(saved_models_path, 'scaler.pkl')
with open(scaler_path, 'wb') as f:
    pickle.dump(scaler, f)
print(f"  ✅ Scaler saved: {scaler_path}")

# Save feature names
feature_names_path = os.path.join(saved_models_path, 'feature_names.pkl')
with open(feature_names_path, 'wb') as f:
    pickle.dump(list(X.columns), f)
print(f"  ✅ Feature names saved: {feature_names_path}")

# Save label encoders
label_encoders_path = os.path.join(saved_models_path, 'label_encoders.pkl')
with open(label_encoders_path, 'wb') as f:
    pickle.dump(label_encoders, f)
print(f"  ✅ Label encoders saved: {label_encoders_path}")

# Save metadata
metadata = {
    'training_date': datetime.now().isoformat(),
    'model_type': 'CalibratedClassifierCV(RandomForestClassifier)',
    'calibration_method': 'isotonic',
    'n_features': len(X.columns),
    'feature_names': list(X.columns),
    'n_training_samples': len(X_train),
    'n_test_samples': len(X_test),
    'metrics': {
        'accuracy': accuracy_score(y_test, y_pred_cal),
        'precision': precision_score(y_test, y_pred_cal),
        'recall': recall_score(y_test, y_pred_cal),
        'f1_score': f1_score(y_test, y_pred_cal),
        'roc_auc': roc_auc_score(y_test, y_proba_cal),
        'brier_score': brier_score_loss(y_test, y_proba_cal),
    }
}

metadata_path = os.path.join(saved_models_path, 'training_metadata.pkl')
with open(metadata_path, 'wb') as f:
    pickle.dump(metadata, f)
print(f"  ✅ Metadata saved: {metadata_path}")

print("\n" + "="*70)
print("🎉 CALIBRATED MODEL TRAINING COMPLETE!")
print("="*70)
print("\n✨ The new model should provide more realistic risk scores")
print("   across the full 0-100% range instead of just extremes.\n")
print("📝 Next step: Run generate_risk_scores.py again to regenerate")
print("   risk scores with the calibrated model.\n")
