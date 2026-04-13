import json
import numpy as np

# Load history
with open('results/comprehensive_training_20260209_085905/model2_order2_snps100_dataset0_history.json', 'r') as f:
    history = json.load(f)

val_acc = history['val_accuracy']
rounds = history['rounds']

# Find peak
max_acc = max(val_acc)
peak_round = rounds[val_acc.index(max_acc)]

print(f"Dataset 0:")
print(f"  Peak validation accuracy: {max_acc:.4f} ({max_acc*100:.2f}%)")
print(f"  Occurred at round: {peak_round}")
print(f"  Final accuracy (round 500): {val_acc[-1]:.4f} ({val_acc[-1]*100:.2f}%)")
print(f"  Decline from peak: {(max_acc - val_acc[-1]):.4f} ({(max_acc - val_acc[-1])*100:.2f}%)")
print(f"  Rounds after peak: {500 - peak_round}")

# Load dataset 1
with open('results/comprehensive_training_20260209_085905/model2_order2_snps100_dataset1_history.json', 'r') as f:
    history1 = json.load(f)

val_acc1 = history1['val_accuracy']
rounds1 = history1['rounds']

max_acc1 = max(val_acc1)
peak_round1 = rounds1[val_acc1.index(max_acc1)]

print(f"\nDataset 1:")
print(f"  Peak validation accuracy: {max_acc1:.4f} ({max_acc1*100:.2f}%)")
print(f"  Occurred at round: {peak_round1}")
print(f"  Final accuracy (round 500): {val_acc1[-1]:.4f} ({val_acc1[-1]*100:.2f}%)")
print(f"  Decline from peak: {(max_acc1 - val_acc1[-1]):.4f} ({(max_acc1 - val_acc1[-1])*100:.2f}%)")
print(f"  Rounds after peak: {500 - peak_round1}")

# Recommended patience
avg_peak = (peak_round + peak_round1) / 2
print(f"\n{'='*60}")
print(f"ANALYSIS:")
print(f"  Average peak round: {avg_peak:.0f}")
print(f"  Recommended patience: {int(avg_peak * 0.3)} - {int(avg_peak * 0.5)}")
print(f"  (30-50% of peak round is standard)")
print(f"{'='*60}")
