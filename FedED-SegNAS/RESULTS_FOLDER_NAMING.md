# Results Folder Naming Convention

## Overview

The `train_all_models_comprehensive222.py` script now creates **descriptive result folders** that make it easy to identify different training runs.

## Folder Naming Structure

### Format
```
results/[CONFIG_NAME]_[TIMESTAMP]/
```

Where:
- `CONFIG_NAME`: Descriptive name based on the configuration used
- `TIMESTAMP`: Date and time in format `YYYYMMDD_HHMMSS`

## Folder Names by Configuration

### 1. Default Configuration (1000 Epochs)
```bash
python train_all_models_comprehensive222.py
```
**Folder Name**: `PAPER_1000EPOCHS_DEFAULT_20260202_150000/`

**Contains**:
- 1000 communication rounds
- No early stopping
- Standard settings

---

### 2. Paper 1000 Configuration
```bash
python train_all_models_comprehensive222.py --paper-1000
```
**Folder Name**: `PAPER_1000EPOCHS_20260202_150000/`

**Contains**:
- 1000 communication rounds
- No early stopping
- High accuracy settings (15 clients, 2 local epochs)

---

### 3. High Accuracy Configuration (500 Epochs)
```bash
python train_all_models_comprehensive222.py --high-accuracy
```
**Folder Name**: `HIGH_ACCURACY_100rounds_20260202_150000/`

**Contains**:
- 100-500 communication rounds
- Early stopping enabled (patience=40)
- High accuracy settings

---

### 4. Quick Test Configuration
```bash
python train_all_models_comprehensive222.py --quick
```
**Folder Name**: `QUICK_TEST_10rounds_20260202_150000/`

**Contains**:
- 10-30 communication rounds
- Early stopping enabled (patience=10)
- Fast testing settings

---

### 5. With NAS Configuration
```bash
python train_all_models_comprehensive222.py --with-nas
```
**Folder Name**: `WITH_NAS_80rounds_20260202_150000/`

**Contains**:
- 80-300 communication rounds
- Neural Architecture Search enabled
- NAS frequency: every 20 rounds

---

## Folder Contents

Each results folder contains:

```
results/[CONFIG_NAME]_[TIMESTAMP]/
├── final_summary.json              # Overall results in JSON format
├── final_summary.txt               # Human-readable summary
├── training_config.json            # Configuration used for this run
├── training_progress.json          # Per-dataset results and progress
├── plots/                          # Visualization plots
│   ├── accuracy_by_model.png
│   ├── training_time.png
│   └── ...
└── trained_models/                 # Saved model weights
    ├── model1_order2_snps100_dataset0.h5
    ├── model1_order2_snps100_dataset1.h5
    └── ...
```

## Examples

### Example 1: Running Default (1000 Epochs)
```bash
cd FedED-SegNAS
python train_all_models_comprehensive222.py
```

**Output**:
```
⚙️ Using DEFAULT configuration (1000 EPOCHS)
================================================================================
COMPREHENSIVE FEDERATED TRAINING - DEFAULT CONFIGURATION
================================================================================
Results directory: results/PAPER_1000EPOCHS_DEFAULT_20260202_150000
```

**Results saved to**: `results/PAPER_1000EPOCHS_DEFAULT_20260202_150000/`

---

### Example 2: Running High Accuracy
```bash
cd FedED-SegNAS
python train_all_models_comprehensive222.py --high-accuracy
```

**Output**:
```
🎯 Using HIGH ACCURACY configuration
================================================================================
COMPREHENSIVE FEDERATED TRAINING - HIGH ACCURACY CONFIGURATION
================================================================================
Results directory: results/HIGH_ACCURACY_100rounds_20260202_151500
```

**Results saved to**: `results/HIGH_ACCURACY_100rounds_20260202_151500/`

---

### Example 3: Running Quick Test
```bash
cd FedED-SegNAS
python train_all_models_comprehensive222.py --quick
```

**Output**:
```
🚀 Using QUICK TEST configuration
================================================================================
COMPREHENSIVE FEDERATED TRAINING - QUICK CONFIGURATION
================================================================================
Results directory: results/QUICK_TEST_10rounds_20260202_152000
```

**Results saved to**: `results/QUICK_TEST_10rounds_20260202_152000/`

---

## Comparison: Old vs New Naming

### Old Naming (train_all_models_comprehensive.py)
```
results/comprehensive_training_20260202_144642/
results/comprehensive_training_20260202_150000/
results/comprehensive_training_20260202_151500/
```
❌ **Problem**: Hard to distinguish which configuration was used

### New Naming (train_all_models_comprehensive222.py)
```
results/PAPER_1000EPOCHS_DEFAULT_20260202_150000/
results/HIGH_ACCURACY_100rounds_20260202_151500/
results/QUICK_TEST_10rounds_20260202_152000/
```
✅ **Benefit**: Immediately clear which configuration was used

---

## Benefits

1. **Easy Identification**: Know at a glance which configuration was used
2. **No Confusion**: Different runs are clearly distinguished
3. **Organized Results**: Easy to compare results from different configurations
4. **Timestamp Preserved**: Still includes timestamp for uniqueness
5. **Parallel Runs**: Can run multiple configurations simultaneously without confusion

---

## Finding Your Results

### List All Results
```powershell
# In PowerShell
Get-ChildItem results/ | Sort-Object LastWriteTime -Descending
```

### Find Specific Configuration
```powershell
# Find all 1000 epoch runs
Get-ChildItem results/ -Filter "*1000EPOCHS*"

# Find all high accuracy runs
Get-ChildItem results/ -Filter "*HIGH_ACCURACY*"

# Find all quick test runs
Get-ChildItem results/ -Filter "*QUICK_TEST*"
```

### Check Latest Results
```powershell
# Get the most recent results folder
Get-ChildItem results/ | Sort-Object LastWriteTime -Descending | Select-Object -First 1
```

---

## Tips

1. **Keep Old Results**: The old naming format from `train_all_models_comprehensive.py` will still exist in folders like `comprehensive_training_YYYYMMDD_HHMMSS/`

2. **Compare Configurations**: You can now easily compare results:
   ```
   results/HIGH_ACCURACY_100rounds_20260202_151500/final_summary.txt
   results/PAPER_1000EPOCHS_DEFAULT_20260202_150000/final_summary.txt
   ```

3. **Archive Old Results**: Move old results to an archive folder:
   ```powershell
   mkdir results/archive
   Move-Item results/comprehensive_training_* results/archive/
   ```

4. **Disk Space**: Each run can take several GB. Monitor disk space:
   ```powershell
   Get-ChildItem results/ -Recurse | Measure-Object -Property Length -Sum
   ```

---

## Summary

| Configuration | Folder Name Pattern | Rounds | Early Stop |
|--------------|---------------------|--------|------------|
| Default | `PAPER_1000EPOCHS_DEFAULT_*` | 1000 | No |
| Paper 1000 | `PAPER_1000EPOCHS_*` | 1000 | No |
| High Accuracy | `HIGH_ACCURACY_100rounds_*` | 100-500 | Yes (40) |
| Quick Test | `QUICK_TEST_10rounds_*` | 10-30 | Yes (10) |
| With NAS | `WITH_NAS_80rounds_*` | 80-300 | Yes (30) |

Now you can easily identify and compare results from different training runs! 🎉
