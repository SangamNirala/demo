#!/usr/bin/env python3
"""
Quick test to verify FedProx shape handling fix
"""

import sys
import os
import numpy as np

# Add parent directory to path
script_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, script_dir)

# Import federated learning
import importlib.util
phase3_dir = os.path.join(script_dir, 'Phase 3')
spec = importlib.util.spec_from_file_location(
    "federated_learning",
    os.path.join(phase3_dir, "federated_learning.py")
)
federated_learning = importlib.util.module_from_spec(spec)
spec.loader.exec_module(federated_learning)

print("=" * 70)
print("TESTING FEDPROX SHAPE HANDLING FIX")
print("=" * 70)

# Load a small dataset
data_path = "data/processed/model1/order2/snps100/dataset_0.npz"
print(f"\n1. Loading test dataset: {data_path}")

try:
    data = np.load(data_path)
    X_train = data['X_train']
    y_train = data['y_train']
    X_test = data['X_test']
    y_test = data['y_test']
    
    print(f"   ✓ Dataset loaded successfully")
    print(f"   - Training samples: {len(X_train)}")
    print(f"   - Test samples: {len(X_test)}")
    print(f"   - Input shape: {X_train.shape}")
    
except Exception as e:
    print(f"   ✗ Failed to load dataset: {e}")
    sys.exit(1)

# Create trainer with FedProx enabled
print(f"\n2. Creating SimpleFederatedTrainer with FedProx")
try:
    trainer = federated_learning.SimpleFederatedTrainer(
        num_clients=3,
        local_epochs=2,
        learning_rate=0.001,
        use_fedprox=True,
        fedprox_mu=0.01
    )
    print(f"   ✓ Trainer created successfully")
    print(f"   - FedProx enabled: {trainer.use_fedprox}")
    print(f"   - FedProx mu: {trainer.fedprox_mu}")
except Exception as e:
    print(f"   ✗ Failed to create trainer: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

# Try training for 1 round
print(f"\n3. Testing training with FedProx (1 round)")
try:
    results = trainer.train(
        X_train, y_train,
        X_test, y_test,
        num_rounds=1,
        verbose=True
    )
    
    print(f"\n   ✓ Training completed successfully!")
    print(f"   - Final test accuracy: {results['test_accuracy']:.4f}")
    print(f"   - Training time: {results['training_time']:.2f}s")
    
    if results['test_accuracy'] > 0.5:
        print(f"\n   🎉 SUCCESS! Accuracy > 50% (better than random)")
    else:
        print(f"\n   ⚠ Warning: Accuracy = 50% (random guessing)")
        print(f"      This is expected for 1 round of training")
    
except Exception as e:
    print(f"\n   ✗ Training failed: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

print("\n" + "=" * 70)
print("TEST PASSED! FedProx shape handling is working correctly")
print("=" * 70)
print("\nYou can now run the full training:")
print("  python train_all_models_comprehensive.py")
print()
