"""
Simple diagnostic test
"""
import sys
import os

print("=" * 60)
print("DIAGNOSTIC TEST")
print("=" * 60)
print()

# Test 1: Check Python version
print("1. Python version:", sys.version)
print()

# Test 2: Check current directory
print("2. Current directory:", os.getcwd())
print()

# Test 3: Check if model files exist
print("3. Checking for model files...")
base_path = os.path.dirname(os.path.abspath(__file__))
saved_models = os.path.join(base_path, 'saved_models')
print(f"   Base path: {base_path}")
print(f"   Saved models path: {saved_models}")
print()

files_to_check = [
    'dropout_model.pkl',
    'scaler.pkl',
    'feature_names.pkl',
    'label_encoders.pkl',
    'training_metadata.pkl'
]

for filename in files_to_check:
    filepath = os.path.join(saved_models, filename)
    exists = os.path.exists(filepath)
    status = "✓ EXISTS" if exists else "✗ MISSING"
    print(f"   {status}: {filename}")
print()

# Test 4: Try to import predict module
print("4. Trying to import predict module...")
try:
    from predict import DropoutPredictor
    print("   ✓ Import successful!")
except Exception as e:
    print(f"   ✗ Import failed: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

print()

# Test 5: Try to create predictor
print("5. Creating predictor instance...")
try:
    predictor = DropoutPredictor()
    print(f"   Predictor created")
    print(f"   Model loaded: {predictor.is_loaded}")
except Exception as e:
    print(f"   ✗ Failed: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

print()
print("=" * 60)
print("DIAGNOSTIC COMPLETE")
print("=" * 60)
