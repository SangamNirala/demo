"""
Backend Setup Verification Script
==================================

This script verifies that all backend components are properly set up.
"""

import os
import sys
import json
from pathlib import Path

def check_file_exists(file_path, description):
    """Check if a file exists"""
    if os.path.exists(file_path):
        print(f"  ✓ {description}")
        return True
    else:
        print(f"  ✗ {description} - NOT FOUND")
        return False

def check_directory_exists(dir_path, description):
    """Check if a directory exists"""
    if os.path.isdir(dir_path):
        print(f"  ✓ {description}")
        return True
    else:
        print(f"  ✗ {description} - NOT FOUND")
        return False

def check_json_valid(file_path, description):
    """Check if JSON file is valid"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            json.load(f)
        print(f"  ✓ {description} - Valid JSON")
        return True
    except json.JSONDecodeError:
        print(f"  ✗ {description} - INVALID JSON")
        return False
    except FileNotFoundError:
        print(f"  ✗ {description} - NOT FOUND")
        return False

def check_python_imports():
    """Check if required Python packages can be imported"""
    packages = {
        'flask': 'Flask',
        'flask_cors': 'Flask-CORS',
        'pandas': 'Pandas',
        'numpy': 'NumPy',
        'sklearn': 'scikit-learn',
        'pickle': 'Pickle (built-in)'
    }
    
    all_ok = True
    for package, name in packages.items():
        try:
            __import__(package)
            print(f"  ✓ {name}")
        except ImportError:
            print(f"  ✗ {name} - NOT INSTALLED")
            all_ok = False
    
    return all_ok

def main():
    """Run all verification checks"""
    print("\n" + "="*60)
    print("BACKEND SETUP VERIFICATION")
    print("="*60)
    
    base_dir = Path(__file__).parent
    all_checks_passed = True
    
    # Check 1: Core files
    print("\n1. Checking Core Files...")
    checks = [
        (base_dir / 'server.py', 'server.py'),
        (base_dir / 'config.py', 'config.py'),
        (base_dir / 'requirements.txt', 'requirements.txt'),
        (base_dir / '.env.example', '.env.example'),
    ]
    
    for file_path, desc in checks:
        if not check_file_exists(file_path, desc):
            all_checks_passed = False
    
    # Check 2: Database
    print("\n2. Checking Database...")
    db_path = base_dir / 'database' / 'students_data.json'
    if not check_json_valid(db_path, 'students_data.json'):
        all_checks_passed = False
    
    # Check 3: ML Model Files
    print("\n3. Checking ML Model Files...")
    model_dir = base_dir / 'ml' / 'saved_models'
    model_files = [
        'dropout_model.pkl',
        'scaler.pkl',
        'feature_names.pkl',
        'label_encoders.pkl'
    ]
    
    for model_file in model_files:
        if not check_file_exists(model_dir / model_file, model_file):
            all_checks_passed = False
    
    # Check 4: Directory Structure
    print("\n4. Checking Directory Structure...")
    directories = [
        (base_dir / 'routes', 'routes/'),
        (base_dir / 'services', 'services/'),
        (base_dir / 'schemas', 'schemas/'),
        (base_dir / 'ml', 'ml/'),
        (base_dir / 'utils', 'utils/'),
        (base_dir / 'database', 'database/'),
    ]
    
    for dir_path, desc in directories:
        if not check_directory_exists(dir_path, desc):
            all_checks_passed = False
    
    # Check 5: Route Files
    print("\n5. Checking Route Files...")
    route_files = [
        (base_dir / 'routes' / 'student_routes' / 'student_routes.py', 'student_routes.py'),
        (base_dir / 'routes' / 'prediction_routes' / 'prediction_routes.py', 'prediction_routes.py'),
    ]
    
    for file_path, desc in route_files:
        if not check_file_exists(file_path, desc):
            all_checks_passed = False
    
    # Check 6: Service Files
    print("\n6. Checking Service Files...")
    service_files = [
        (base_dir / 'services' / 'student_service' / 'student_service.py', 'student_service.py'),
        (base_dir / 'services' / 'prediction_service' / 'prediction_service.py', 'prediction_service.py'),
    ]
    
    for file_path, desc in service_files:
        if not check_file_exists(file_path, desc):
            all_checks_passed = False
    
    # Check 7: Schema Files
    print("\n7. Checking Schema Files...")
    schema_files = [
        (base_dir / 'schemas' / 'student_schema' / 'student_schema.py', 'student_schema.py'),
        (base_dir / 'schemas' / 'prediction_schema' / 'prediction_schema.py', 'prediction_schema.py'),
    ]
    
    for file_path, desc in schema_files:
        if not check_file_exists(file_path, desc):
            all_checks_passed = False
    
    # Check 8: ML Files
    print("\n8. Checking ML Files...")
    ml_files = [
        (base_dir / 'ml' / 'predict.py', 'predict.py'),
        (base_dir / 'ml' / 'train.py', 'train.py'),
    ]
    
    for file_path, desc in ml_files:
        if not check_file_exists(file_path, desc):
            all_checks_passed = False
    
    # Check 9: Python Packages
    print("\n9. Checking Python Packages...")
    if not check_python_imports():
        all_checks_passed = False
    
    # Check 10: Test if modules can be imported
    print("\n10. Checking Module Imports...")
    try:
        sys.path.insert(0, str(base_dir))
        from ml.predict import DropoutPredictor
        print("  ✓ Can import DropoutPredictor")
    except Exception as e:
        print(f"  ✗ Cannot import DropoutPredictor: {e}")
        all_checks_passed = False
    
    # Final Result
    print("\n" + "="*60)
    if all_checks_passed:
        print("✅ ALL CHECKS PASSED!")
        print("\nYour backend is properly set up and ready to run.")
        print("\nTo start the server, run:")
        print("  python server.py")
    else:
        print("⚠️  SOME CHECKS FAILED")
        print("\nPlease fix the issues above before running the server.")
        print("\nCommon fixes:")
        print("  - Install dependencies: pip install -r requirements.txt")
        print("  - Ensure model files are in ml/saved_models/")
        print("  - Check that all files are properly created")
    print("="*60 + "\n")
    
    return 0 if all_checks_passed else 1

if __name__ == "__main__":
    sys.exit(main())
