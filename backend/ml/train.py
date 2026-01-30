# Model training script
import pandas as pd
import numpy as np
import pickle
import os
import warnings
from datetime import datetime

# Scikit-learn imports
from sklearn.model_selection import train_test_split, cross_val_score, GridSearchCV
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    roc_auc_score,
    classification_report,
    confusion_matrix
)

# Suppress warnings
warnings.filterwarnings('ignore')

# Set random seed for reproducibility
RANDOM_STATE = 42
np.random.seed(RANDOM_STATE)


# ============================================================================
# CONFIGURATION
# ============================================================================

class Config:
    """Configuration settings for training"""

    # File paths
    DATA_PATH = 'training_data_enhanced.csv' # Corrected path
    MODEL_PATH = 'saved_models/dropout_model.pkl'
    SCALER_PATH = 'saved_models/scaler.pkl'
    FEATURE_NAMES_PATH = 'saved_models/feature_names.pkl'
    LABEL_ENCODERS_PATH = 'saved_models/label_encoders.pkl'

    # Model settings
    TEST_SIZE = 0.2
    RANDOM_STATE = 42

    # Features to use for training
    NUMERIC_FEATURES = [
        # New synthetic features (Engagement)
        'attendance_percentage',
        'assignment_submission_rate',
        'library_visits_monthly',
        'lms_last_login_days',
        'extracurricular_participation',

        # New synthetic features (Financial)
        'family_income',
        'fee_payment_delay_months',

        # New synthetic features (Support & Logistics)
        'counselor_visits',
        'distance_from_college_km',

        # Original UCI features (Academic)
        'Curricular units 1st sem (credited)',
        'Curricular units 1st sem (enrolled)',
        'Curricular units 1st sem (evaluations)',
        'Curricular units 1st sem (approved)',
        'Curricular units 1st sem (grade)',
        'Curricular units 1st sem (without evaluations)',
        'Curricular units 2nd sem (credited)',
        'Curricular units 2nd sem (enrolled)',
        'Curricular units 2nd sem (evaluations)',
        'Curricular units 2nd sem (approved)',
        'Curricular units 2nd sem (grade)',
        'Curricular units 2nd sem (without evaluations)',

        # Original UCI features (Personal)
        'Age at enrollment',
        'Admission grade',
        'Previous qualification (grade)',

        # Original UCI features (Financial - from UCI)
        'Tuition fees up to date',
        'Scholarship holder',
        'Debtor',

        # Original UCI features (Other)
        'Displaced',
        'Gender',
        'Marital status',
        'Daytime/evening attendance',
    ]

    CATEGORICAL_FEATURES = [
        'hostel_day_scholar',
    ]

    TARGET = 'dropout_status'


# ============================================================================
# DATA LOADING & PREPROCESSING
# ============================================================================

def load_data(filepath):
    """
    Load the dataset from CSV file

    Args:
        filepath: Path to the CSV file

    Returns:
        DataFrame
    """
    print(f"Loading data from: {filepath}")
    df = pd.read_csv(filepath)
    print(f"Loaded {len(df)} records with {len(df.columns)} columns")
    return df


def preprocess_data(df, config):
    """
    Preprocess the data for training

    Steps:
        1. Select relevant features
        2. Handle missing values
        3. Encode categorical variables
        4. Scale numeric features

    Args:
        df: DataFrame
        config: Config object

    Returns:
        X: Feature matrix
        y: Target vector
        scaler: Fitted StandardScaler
        label_encoders: Dictionary of fitted LabelEncoders
        feature_names: List of feature names
    """
    print("\nPreprocessing data...")

    # Initialize containers
    label_encoders = {}

    # 1. Create a copy with selected features
    all_features = config.NUMERIC_FEATURES + config.CATEGORICAL_FEATURES

    # Check which features exist in the dataset
    available_features = [f for f in all_features if f in df.columns]
    missing_features = [f for f in all_features if f not in df.columns]

    if missing_features:
        print(f"  ⚠️ Missing features (will be skipped): {missing_features}")

    print(f"  Using {len(available_features)} features")

    # 2. Select features and target
    X = df[available_features].copy()
    y = df[config.TARGET].copy()

    # 3. Handle missing values
    print("  Handling missing values...")

    # For numeric columns: fill with median
    numeric_cols = [col for col in available_features if col in config.NUMERIC_FEATURES]
    for col in numeric_cols:
        if X[col].isnull().sum() > 0:
            X[col].fillna(X[col].median(), inplace=True)

    # For categorical columns: fill with mode
    categorical_cols = [col for col in available_features if col in config.CATEGORICAL_FEATURES]
    for col in categorical_cols:
        if X[col].isnull().sum() > 0:
            X[col].fillna(X[col].mode()[0], inplace=True)

    # 4. Encode categorical variables
    print("  Encoding categorical variables...")

    for col in categorical_cols:
        le = LabelEncoder()
        X[col] = le.fit_transform(X[col].astype(str))
        label_encoders[col] = le
        print(f"    {col}: {list(le.classes_)}")

    # 5. Scale numeric features
    print("  Scaling numeric features...")

    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    # Convert back to DataFrame for feature names
    X_scaled = pd.DataFrame(X_scaled, columns=X.columns)

    # Get feature names
    feature_names = list(X.columns)

    print(f"\n  ✅ Preprocessing complete!")
    print(f"  Final feature count: {len(feature_names)}")

    return X_scaled, y, scaler, label_encoders, feature_names


# ============================================================================
# MODEL TRAINING
# ============================================================================

def train_random_forest(X_train, y_train, config):
    """
    Train a Random Forest Classifier

    Args:
        X_train: Training features
        y_train: Training target
        config: Config object

    Returns:
        Trained model
    """
    print("\nTraining Random Forest Classifier...")

    # Define hyperparameter grid for tuning
    param_grid = {
        'n_estimators': [100, 200],
        'max_depth': [10, 20, None],
        'min_samples_split': [2, 5],
        'min_samples_leaf': [1, 2],
        'class_weight': ['balanced']
    }

    # Initialize base model
    rf_base = RandomForestClassifier(random_state=config.RANDOM_STATE)

    # Perform Grid Search with Cross-Validation
    print("  Performing hyperparameter tuning (this may take a few minutes)...")

    grid_search = GridSearchCV(
        estimator=rf_base,
        param_grid=param_grid,
        cv=5,
        scoring='f1',
        n_jobs=-1,
        verbose=0
    )

    grid_search.fit(X_train, y_train)

    # Get best model
    best_model = grid_search.best_estimator_

    print(f"\n  Best Parameters: {grid_search.best_params_}")
    print(f"  Best CV F1 Score: {grid_search.best_score_:.4f}")

    return best_model


def train_simple_random_forest(X_train, y_train, config):
    """
    Train a simple Random Forest Classifier (faster, no grid search)

    Use this if you want faster training.
    """
    print("\nTraining Random Forest Classifier (Simple)...")

    model = RandomForestClassifier(
        n_estimators=200,
        max_depth=20,
        min_samples_split=2,
        min_samples_leaf=1,
        class_weight='balanced',
        random_state=config.RANDOM_STATE,
        n_jobs=-1
    )

    model.fit(X_train, y_train)

    # Cross-validation score
    cv_scores = cross_val_score(model, X_train, y_train, cv=5, scoring='f1')
    print(f"  Cross-validation F1 Score: {cv_scores.mean():.4f} (+/- {cv_scores.std() * 2:.4f})")

    return model


# ============================================================================
# MODEL EVALUATION
# ============================================================================

def evaluate_model(model, X_test, y_test, feature_names):
    """
    Evaluate the trained model

    Args:
        model: Trained model
        X_test: Test features
        y_test: Test target
        feature_names: List of feature names

    Returns:
        Dictionary of evaluation metrics
    """
    print("\n" + "=" * 60)
    print("MODEL EVALUATION")
    print("=" * 60)

    # Make predictions
    y_pred = model.predict(X_test)
    y_pred_proba = model.predict_proba(X_test)[:, 1]

    # Calculate metrics
    accuracy = accuracy_score(y_test, y_pred)
    precision = precision_score(y_test, y_pred)
    recall = recall_score(y_test, y_pred)
    f1 = f1_score(y_test, y_pred)
    roc_auc = roc_auc_score(y_test, y_pred_proba)

    # Print metrics
    print(f"\n📊 Performance Metrics:")
    print(f"  ├── Accuracy:  {accuracy:.4f}  ({accuracy*100:.2f}%)")
    print(f"  ├── Precision: {precision:.4f}  ({precision*100:.2f}%)")
    print(f"  ├── Recall:    {recall:.4f}  ({recall*100:.2f}%)")
    print(f"  ├── F1 Score:  {f1:.4f}  ({f1*100:.2f}%)")
    print(f"  └── ROC-AUC:   {roc_auc:.4f}  ({roc_auc*100:.2f}%)")

    # Classification Report
    print(f"\n📋 Classification Report:")
    print("-" * 60)
    print(classification_report(y_test, y_pred, target_names=['Not Dropout', 'Dropout']))

    # Confusion Matrix
    cm = confusion_matrix(y_test, y_pred)
    print(f"📊 Confusion Matrix:")
    print("-" * 60)
    print(f"                  Predicted")
    print(f"                  No    Yes")
    print(f"  Actual No    [{cm[0][0]:5d}  {cm[0][1]:5d}]")
    print(f"         Yes   [{cm[1][0]:5d}  {cm[1][1]:5d}]")

    # Feature Importance
    print(f"\n🎯 Top 15 Most Important Features:")
    print("-" * 60)

    feature_importance = pd.DataFrame({
        'feature': feature_names,
        'importance': model.feature_importances_
    }).sort_values('importance', ascending=False)

    for i, row in feature_importance.head(15).iterrows():
        bar_length = int(row['importance'] * 50)
        bar = '█' * bar_length
        print(f"  {row['feature'][:40]:<40} {row['importance']:.4f} {bar}")

    # Return metrics dictionary
    metrics = {
        'accuracy': accuracy,
        'precision': precision,
        'recall': recall,
        'f1_score': f1,
        'roc_auc': roc_auc,
        'confusion_matrix': cm.tolist(),
        'feature_importance': feature_importance.to_dict('records')
    }

    return metrics


# ============================================================================
# SAVE MODEL
# ============================================================================

def save_model(model, scaler, feature_names, label_encoders, config, metrics):
    """
    Save the trained model and related objects

    Args:
        model: Trained model
        scaler: Fitted StandardScaler
        feature_names: List of feature names
        label_encoders: Dictionary of LabelEncoders
        config: Config object
        metrics: Evaluation metrics
    """
    print("\n" + "=" * 60)
    print("SAVING MODEL")
    print("=" * 60)

    # Create saved_models directory if it doesn't exist
    os.makedirs(os.path.dirname(config.MODEL_PATH), exist_ok=True)

    # Save the model
    print(f"\n  Saving model to: {config.MODEL_PATH}")
    with open(config.MODEL_PATH, 'wb') as f:
        pickle.dump(model, f)

    # Save the scaler
    print(f"  Saving scaler to: {config.SCALER_PATH}")
    with open(config.SCALER_PATH, 'wb') as f:
        pickle.dump(scaler, f)

    # Save feature names
    print(f"  Saving feature names to: {config.FEATURE_NAMES_PATH}")
    with open(config.FEATURE_NAMES_PATH, 'wb') as f:
        pickle.dump(feature_names, f)

    # Save label encoders
    print(f"  Saving label encoders to: {config.LABEL_ENCODERS_PATH}")
    with open(config.LABEL_ENCODERS_PATH, 'wb') as f:
        pickle.dump(label_encoders, f)

    # Save training metadata
    metadata = {
        'training_date': datetime.now().isoformat(),
        'model_type': type(model).__name__,
        'n_features': len(feature_names),
        'feature_names': feature_names,
        'metrics': metrics,
        'config': {
            'test_size': config.TEST_SIZE,
            'random_state': config.RANDOM_STATE
        }
    }

    metadata_path = 'saved_models/training_metadata.pkl'
    print(f"  Saving metadata to: {metadata_path}")
    with open(metadata_path, 'wb') as f:
        pickle.dump(metadata, f)

    print("\n  ✅ All files saved successfully!")

    # Print file sizes
    print("\n  📁 Saved Files:")
    for path in [config.MODEL_PATH, config.SCALER_PATH, config.FEATURE_NAMES_PATH,
                 config.LABEL_ENCODERS_PATH, metadata_path]:
        if os.path.exists(path):
            size = os.path.getsize(path) / 1024  # KB
            print(f"      {path}: {size:.2f} KB")


# ============================================================================
# MAIN FUNCTION
# ============================================================================

def main():
    """Main training pipeline"""

    print("=" * 60)
    print("🎓 STUDENT DROPOUT PREDICTION - MODEL TRAINING")
    print("=" * 60)
    print(f"Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

    # Initialize config
    config = Config()

    # Step 1: Load data
    print("\n" + "-" * 60)
    print("STEP 1: LOADING DATA")
    print("-" * 60)
    df = load_data(config.DATA_PATH)

    # Print target distribution
    print(f"\nTarget Distribution:")
    print(f"  Not Dropout (0): {(df[config.TARGET] == 0).sum()}")
    print(f"  Dropout (1):     {(df[config.TARGET] == 1).sum()}")
    print(f"  Dropout Rate:    {df[config.TARGET].mean() * 100:.2f}%")

    # Step 2: Preprocess data
    print("\n" + "-" * 60)
    print("STEP 2: PREPROCESSING DATA")
    print("-" * 60)
    X, y, scaler, label_encoders, feature_names = preprocess_data(df, config)

    # Step 3: Split data
    print("\n" + "-" * 60)
    print("STEP 3: SPLITTING DATA")
    print("-" * 60)
    X_train, X_test, y_train, y_test = train_test_split(
        X, y,
        test_size=config.TEST_SIZE,
        random_state=config.RANDOM_STATE,
        stratify=y  # Maintain class distribution
    )
    print(f"  Training set: {len(X_train)} samples")
    print(f"  Test set:     {len(X_test)} samples")

    # Step 4: Train model
    print("\n" + "-" * 60)
    print("STEP 4: TRAINING MODEL")
    print("-" * 60)

    # Use simple training for faster results
    # Change to train_random_forest() for hyperparameter tuning
    model = train_simple_random_forest(X_train, y_train, config)

    # Step 5: Evaluate model
    print("\n" + "-" * 60)
    print("STEP 5: EVALUATING MODEL")
    print("-" * 60)
    metrics = evaluate_model(model, X_test, y_test, feature_names)

    # Step 6: Save model
    print("\n" + "-" * 60)
    print("STEP 6: SAVING MODEL")
    print("-" * 60)
    save_model(model, scaler, feature_names, label_encoders, config, metrics)

    # Final summary
    print("\n" + "=" * 60)
    print("🎉 TRAINING COMPLETE!")
    print("=" * 60)
    print(f"\nFinished at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"\nModel Performance Summary:")
    print(f"  ├── Accuracy:  {metrics['accuracy']*100:.2f}%")
    print(f"  ├── Precision: {metrics['precision']*100:.2f}%")
    print(f"  ├── Recall:    {metrics['recall']*100:.2f}%")
    print(f"  ├── F1 Score:  {metrics['f1_score']*100:.2f}%")
    print(f"  └── ROC-AUC:   {metrics['roc_auc']*100:.2f}%")

    print(f"\n📁 Files saved in 'saved_models/' directory:")
    print(f"  ├── dropout_model.pkl")
    print(f"  ├── scaler.pkl")
    print(f"  ├── feature_names.pkl")
    print(f"  ├── label_encoders.pkl")
    print(f"  └── training_metadata.pkl")

    print(f"\n✅ You can now use these files in predict.py!")

    return model, scaler, feature_names, metrics


# ============================================================================
# ENTRY POINT
# ============================================================================

if __name__ == "__main__":
    model, scaler, feature_names, metrics = main()