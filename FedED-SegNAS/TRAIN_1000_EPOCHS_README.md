# Training with 1000 Epochs - Configuration Guide

## Overview

Both training files have been configured to run **1000 communication rounds (epochs)** as specified in the paper:
- **`train_all_models_comprehensive.py`** - 1000 epochs (DEFAULT)
- **`train_all_models_comprehensive222.py`** - 1000 epochs (DEFAULT)

## Changes Made to BOTH Files

### 1. Default Configuration (1000 Epochs)
- **Minimum rounds**: 1000 (enforced)
- **Maximum rounds**: 1000
- **Early stopping**: DISABLED (patience=None)
- **Warmup rounds**: 50 (longer warmup for 1000 rounds)
- **Local epochs**: 3
- **Clients per round**: 12
- **Learning rate**: 0.005 → 0.00005 (with cosine annealing)

### 2. Alternative PAPER_1000 Configuration
- **Minimum rounds**: 1000
- **Maximum rounds**: 1000
- **Early stopping**: DISABLED
- **Warmup rounds**: 50
- **Local epochs**: 2 (reduced for less drift)
- **Clients per round**: 15 (more clients)
- **Learning rate**: 0.003 → 0.00001 (more conservative)

### 3. HIGH_ACCURACY Configuration (500 epochs)
- Still available for faster training
- Use `--high-accuracy` flag

## Usage

### Option 1: Run with Default (1000 epochs)
```bash
python train_all_models_comprehensive.py
# OR
python train_all_models_comprehensive222.py
```

### Option 2: Run with Alternative Paper Config
```bash
python train_all_models_comprehensive.py --paper-1000
# OR
python train_all_models_comprehensive222.py --paper-1000
```

### Option 3: Run with High Accuracy (500 epochs)
```bash
python train_all_models_comprehensive.py --high-accuracy
# OR
python train_all_models_comprehensive222.py --high-accuracy
```

### Option 4: Quick Test (30 epochs)
```bash
python train_all_models_comprehensive.py --quick
# OR
python train_all_models_comprehensive222.py --quick
```

### Option 5: Train Specific Model
```bash
python train_all_models_comprehensive.py --model model1
# OR
python train_all_models_comprehensive222.py --model model1
```

## Time Estimates

### For 1000 Epochs:
- **Per dataset**: ~5.5 hours (1000 rounds × 20 seconds/round)
- **All 178 datasets**: ~980 hours (41 days)

### Breakdown by Configuration:
| Configuration | Rounds | Time per Dataset | Total Time (178 datasets) |
|--------------|--------|------------------|---------------------------|
| DEFAULT (1000) | 1000 | ~5.5 hours | ~980 hours (41 days) |
| PAPER_1000 | 1000 | ~5.5 hours | ~980 hours (41 days) |
| HIGH_ACCURACY | 100-500 | ~1.7-2.8 hours | ~300-500 hours (12-21 days) |
| QUICK_TEST | 10-30 | ~0.2-0.5 hours | ~35-90 hours (1.5-4 days) |

## Key Features

### 1. No Early Stopping
- Training will run for the full 1000 rounds
- Ensures complete convergence as per paper specification

### 2. Extended Warmup
- 50 rounds of learning rate warmup
- Gradual increase from 0 to initial LR
- Prevents instability in early training

### 3. Cosine Annealing
- Learning rate decays smoothly over 1000 rounds
- From 0.005 to 0.00005 (or 0.003 to 0.00001)
- Enables fine-tuning in later rounds

### 4. FedProx Enabled
- Reduces client drift over long training
- Proximal term coefficient: 0.01 (or 0.005)
- Critical for 1000-round training

## Monitoring Progress

The script will display:
- Current round number (e.g., "Round 1/1000")
- Validation accuracy after each round
- Best validation accuracy achieved
- Estimated time remaining

Example output:
```
================================================================================
Round 1/1000
================================================================================
>> Learning rate: 0.000100
>> Selected 12 clients
...
>> Round 1 Results:
   Global Val Accuracy:   0.5217 (52.17%)
   Best Val Accuracy:     0.5217
   Round Time:            19.03s
```

## Results Location

Results will be saved to:
```
FedED-SegNAS/results/comprehensive_training_YYYYMMDD_HHMMSS/
├── final_summary.json          # Overall results
├── final_summary.txt           # Human-readable summary
├── training_config.json        # Configuration used
├── training_progress.json      # Per-dataset results
├── plots/                      # Visualization plots
└── trained_models/             # Saved model weights
```

## Recommendations

1. **For Paper Replication**: Use default configuration
   ```bash
   python train_all_models_comprehensive.py
   ```

2. **For Faster Testing**: Use quick configuration first
   ```bash
   python train_all_models_comprehensive.py --quick
   ```

3. **For Specific Models**: Train one model at a time
   ```bash
   python train_all_models_comprehensive.py --model model1
   ```

4. **Monitor Progress**: Check the results directory periodically
   - `training_progress.json` updates after each dataset
   - `final_summary.txt` shows overall progress

## Comparison Between Files

Both files are now identical in functionality:

| Aspect | train_all_models_comprehensive.py | train_all_models_comprehensive222.py |
|--------|-----------------------------------|--------------------------------------|
| Default Rounds | 1000 | 1000 |
| Early Stopping | Disabled | Disabled |
| Warmup Rounds | 50 | 50 |
| Paper Compliance | Full (1000 epochs) | Full (1000 epochs) |

**You can use either file - they work the same way!**

## Notes

- Both files now default to 1000 epochs as per paper
- Use `--high-accuracy` flag for faster 500-epoch training
- Consider running on a powerful machine or cluster due to long training time
- Results will be more accurate but take significantly longer

## Support

If you encounter issues:
1. Check the log files in the results directory
2. Verify all dependencies are installed
3. Ensure sufficient disk space for model checkpoints
4. Monitor system resources (CPU/RAM usage)
