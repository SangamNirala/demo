"""
Retrain Model with Better Distribution
=======================================

This script retrains with techniques to generate more realistic
probability distributions across the full 0-100% range, including
middle values (30-70%).
"""

import pandas as pd
import numpy as np
import pickle
import os
from datetime import datetime
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.calibration import CalibratedClassifierCV
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score, 
    f1_score, roc_auc_score, brier_score_loss
)

# Configuration
RANDOM_STATE = 42
np.random.seed(RANDOM_STATE)

print("\n" + "="*70)
print("🔄 RETRAINING WITH IMPROVED PROBABILITY DISTRIBUTION")
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

# Add synthetic noise to create more variation
print("🎲 Adding controlled noise for better distribution...")
X_augmented = X.copy()
noise_scale = 0.05  # 5% noise

for col in X.columns:
    if col not in ['hostel_day_scholar']:  # Don't add noise to categorical
        noise = np.random.normal(0, X[col].std() * noise_scale, len(X))
        X_augmented[col] = X[col] + noise

print(f"✅ Data augmented\n")

# Split data
X_train, X_test, y_train, y_test = train_test_split(
    X_augmented, y, test_size=0.2, random_state=RANDOM_STATE, stratify=y
)

# Scale
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# Train THREE different models and ensemble them
print("🎯 Training Ensemble of Models...")

# Model 1: Logistic Regression (naturally gives smooth probabilities)
print("  1️⃣  Training Logistic Regression...")
lr_model = LogisticRegression(
    C=0.1,  # Strong regularization
    max_iter=1000,
    class_weight='balanced',
    random_state=RANDOM_STATE
)
lr_model.fit(X_train_scaled, y_train)

# Model 2: Gradient Boosting (with low learning rate)
print("  2️⃣  Training Gradient Boosting...")
gb_model = GradientBoostingClassifier(
    n_estimators=50,
    learning_rate=0.05,  # Very low learning rate
    max_depth=3,
    min_samples_split=10,
    min_samples_leaf=5,
    subsample=0.8,
    random_state=RANDOM_STATE
)
gb_model.fit(X_train_scaled, y_train)

# Model 3: Random Forest (with strong regularization)
print("  3️⃣  Training Random Forest...")
rf_model = RandomForestClassifier(
    n_estimators=30,
    max_depth=4,
    min_samples_split=15,
    min_samples_leaf=8,
    max_features=0.4,
    class_weight='balanced',
    random_state=RANDOM_STATE,
    n_jobs=-1
)
rf_model.fit(X_train_scaled, y_train)

print("✅ All models trained\n")

# Calibrate each model
print("🎯 Calibrating Models...")
print("  Calibrating Logistic Regression...")
lr_calibrated = CalibratedClassifierCV(lr_model, method='sigmoid', cv=3)
lr_calibrated.fit(X_train_scaled, y_train)

print("  Calibrating Gradient Boosting...")
gb_calibrated = CalibratedClassifierCV(gb_model, method='sigmoid', cv=3)
gb_calibrated.fit(X_train_scaled, y_train)

print("  Calibrating Random Forest...")
rf_calibrated = CalibratedClassifierCV(rf_model, method='sigmoid', cv=3)
rf_calibrated.fit(X_train_scaled, y_train)

print("✅ All models calibrated\n")

# Create ensemble predictions
print("🔗 Creating Ensemble Predictions...")

# Get probabilities from each model
lr_proba = lr_calibrated.predict_proba(X_test_scaled)[:, 1]
gb_proba = gb_calibrated.predict_proba(X_test_scaled)[:, 1]
rf_proba = rf_calibrated.predict_proba(X_test_scaled)[:, 1]

# Weighted average (Logistic Regression gets more weight for smooth probabilities)
ensemble_proba = (0.4 * lr_proba + 0.3 * gb_proba + 0.3 * rf_proba)

# Predictions based on ensemble
ensemble_pred = (ensemble_proba >= 0.5).astype(int)

print("✅ Ensemble created\n")

# Evaluate
print("="*70)
print("📊 MODEL EVALUATION")
print("="*70 + "\n")

print("🔹 INDIVIDUAL MODELS:")
print(f"\n  Logistic Regression:")
print(f"    Accuracy: {accuracy_score(y_test, lr_calibrated.predict(X_test_scaled)):.4f}")
print(f"    ROC-AUC:  {roc_auc_score(y_test, lr_proba):.4f}")
print(f"    Range:    {lr_proba.min():.3f} - {lr_proba.max():.3f}")

print(f"\n  Gradient Boosting:")
print(f"    Accuracy: {accuracy_score(y_test, gb_calibrated.predict(X_test_scaled)):.4f}")
print(f"    ROC-AUC:  {roc_auc_score(y_test, gb_proba):.4f}")
print(f"    Range:    {gb_proba.min():.3f} - {gb_proba.max():.3f}")

print(f"\n  Random Forest:")
print(f"    Accuracy: {accuracy_score(y_test, rf_calibrated.predict(X_test_scaled)):.4f}")
print(f"    ROC-AUC:  {roc_auc_score(y_test, rf_proba):.4f}")
print(f"    Range:    {rf_proba.min():.3f} - {rf_proba.max():.3f}")

print(f"\n🔸 ENSEMBLE MODEL:")
print(f"  Accuracy:  {accuracy_score(y_test, ensemble_pred):.4f}")
print(f"  Precision: {precision_score(y_test, ensemble_pred):.4f}")
print(f"  Recall:    {recall_score(y_test, ensemble_pred):.4f}")
print(f"  F1 Score:  {f1_score(y_test, ensemble_pred):.4f}")
print(f"  ROC-AUC:   {roc_auc_score(y_test, ensemble_proba):.4f}")
print(f"  Brier Score: {brier_score_loss(y_test, ensemble_proba):.4f}")
print(f"  Range:     {ensemble_proba.min():.3f} - {ensemble_proba.max():.3f}")

# Show distribution
print(f"\n📈 Probability Distribution (Ensemble):")
bins = [0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0]
hist, _ = np.histogram(ensemble_proba, bins=bins)
for i in range(len(bins)-1):
    bar = '█' * max(1, int(hist[i] / max(1, len(ensemble_proba)) * 50))
    print(f"  {bins[i]:.1f}-{bins[i+1]:.1f}: {hist[i]:3d} {bar}")

# Create a wrapper class for the ensemble
class EnsembleModel:
    """Wrapper class for ensemble of calibrated models"""
    
    def __init__(self, lr_model, gb_model, rf_model, weights=(0.4, 0.3, 0.3)):
        self.lr_model = lr_model
        self.gb_model = gb_model
        self.rf_model = rf_model
        self.weights = weights
    
    def predict(self, X):
        """Predict class labels"""
        proba = self.predict_proba(X)
        return (proba[:, 1] >= 0.5).astype(int)
    
    def predict_proba(self, X):
        """Predict class probabilities"""
        lr_proba = self.lr_model.predict_proba(X)
        gb_proba = self.gb_model.predict_proba(X)
        rf_proba = self.rf_model.predict_proba(X)
        
        # Weighted average
        ensemble_proba_1 = (
            self.weights[0] * lr_proba[:, 1] +
            self.weights[1] * gb_proba[:, 1] +
            self.weights[2] * rf_proba[:, 1]
        )
        
        ensemble_proba_0 = 1 - ensemble_proba_1
        
        return np.column_stack([ensemble_proba_0, ensemble_proba_1])

# Create ensemble model instance
ensemble_model = EnsembleModel(lr_calibrated, gb_calibrated, rf_calibrated)

# Save model
print("\n💾 Saving Ensemble Model...")
saved_models_path = os.path.join(os.path.dirname(__file__), 'saved_models')
os.makedirs(saved_models_path, exist_ok=True)

with open(os.path.join(saved_models_path, 'dropout_model.pkl'), 'wb') as f:
    pickle.dump(ensemble_model, f)
print(f"  ✅ Ensemble model saved")

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
    'model_type': 'Ensemble(LogisticRegression + GradientBoosting + RandomForest)',
    'ensemble_weights': {'lr': 0.4, 'gb': 0.3, 'rf': 0.3},
    'calibration_method': 'sigmoid',
    'noise_augmentation': f'{noise_scale*100}%',
    'n_features': len(X.columns),
    'feature_names': list(X.columns),
    'metrics': {
        'accuracy': accuracy_score(y_test, ensemble_pred),
        'precision': precision_score(y_test, ensemble_pred),
        'recall': recall_score(y_test, ensemble_pred),
        'f1_score': f1_score(y_test, ensemble_pred),
        'roc_auc': roc_auc_score(y_test, ensemble_proba),
        'brier_score': brier_score_loss(y_test, ensemble_proba),
    }
}

with open(os.path.join(saved_models_path, 'training_metadata.pkl'), 'wb') as f:
    pickle.dump(metadata, f)
print(f"  ✅ Metadata saved")

print("\n" + "="*70)
print("🎉 TRAINING COMPLETE!")
print("="*70)
print("\n✨ Key Improvements:")
print("   • Ensemble of 3 different model types")
print("   • Logistic Regression for smooth probabilities")
print("   • Gradient Boosting with low learning rate")
print("   • Random Forest with strong regularization")
print("   • All models calibrated with sigmoid method")
print("   • 5% noise augmentation for variation")
print("   • Weighted ensemble (40% LR, 30% GB, 30% RF)")
print("\n📝 Next: Run generate_risk_scores.py to see improved distribution\n")
