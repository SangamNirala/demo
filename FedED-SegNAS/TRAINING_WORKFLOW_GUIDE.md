# Training Workflow Guide

## Overview

You have two training scripts available:
1. **`train_all_models_comprehensive.py`** - 500 epochs (HIGH_ACCURACY config)
2. **`train_all_models_comprehensive222.py`** - 1000 epochs (PAPER config)

This guide helps you decide how to run them.

---

## Quick Decision Tree

```
Do you want to run both configurations?
│
├─ YES → Do you have 8+ cores and 16+ GB RAM?
│        │
│        ├─ YES → Use PARALLEL training (Option 2 or 3)
│        │
│        └─ NO → Use SEQUENTIAL training (Option 1)
│
└─ NO → Just run one:
         - For faster results: train_all_models_comprehensive.py --high-accuracy
         - For paper compliance: train_all_models_comprehensive222.py
```

---

## Option 1: Sequential Training (RECOMMENDED)

**Best for**: Most users, guaranteed no conflicts

### How to Run:
```bash
# Method 1: Use the batch script
run_sequential_training.bat

# Method 2: Manual commands
python train_all_models_comprehensive.py --high-accuracy
# Wait for completion, then:
python train_all_models_comprehensive222.py
```

### Pros:
- ✅ No resource conflicts
- ✅ Faster individual completion
- ✅ Easier to monitor
- ✅ Works on any system

### Cons:
- ❌ Takes longer overall (53-62 days total)

### Timeline:
```
Day 0-21:   500-epoch training running
Day 21:     First training complete, analyze results
Day 21-62:  1000-epoch training running
Day 62:     All training complete
```

---

## Option 2: Parallel Training (Full Overlap)

**Best for**: Powerful systems, want both results ASAP

### How to Run:
```bash
# Method 1: Use the batch script
run_parallel_training.bat

# Method 2: Manual - Open two terminals
# Terminal 1:
python train_all_models_comprehensive.py --high-accuracy

# Terminal 2:
python train_all_models_comprehensive222.py
```

### Pros:
- ✅ Both complete together (~18-42 days)
- ✅ Get all results faster

### Cons:
- ❌ Requires powerful system (8+ cores, 16+ GB RAM)
- ❌ Each training runs slower (1.5-2x)
- ❌ High CPU/RAM usage

### System Requirements:
- **CPU**: 8+ cores (16+ logical processors)
- **RAM**: 16+ GB total, 12+ GB free
- **Disk**: Fast SSD recommended

### Timeline:
```
Day 0-42:   Both trainings running in parallel
Day 42:     Both complete simultaneously
```

---

## Option 3: Parallel by Model (SMART APPROACH)

**Best for**: Balanced performance, no duplicate work

### How to Run:
```bash
# Use the batch script
run_parallel_by_model.bat

# Or manually:
# Terminal 1: Train models 1-4 with 500 epochs
python train_all_models_comprehensive.py --high-accuracy --model model1
python train_all_models_comprehensive.py --high-accuracy --model model2
python train_all_models_comprehensive.py --high-accuracy --model model3
python train_all_models_comprehensive.py --high-accuracy --model model4

# Terminal 2: Train models 5-8 with 1000 epochs
python train_all_models_comprehensive222.py --model model5
python train_all_models_comprehensive222.py --model model6
python train_all_models_comprehensive222.py --model model7
python train_all_models_comprehensive222.py --model model8
```

### Pros:
- ✅ No duplicate work
- ✅ Better resource utilization
- ✅ Faster than sequential (~25-35 days)
- ✅ More manageable than full parallel

### Cons:
- ❌ Still requires good system (6+ cores, 12+ GB RAM)
- ❌ More complex to set up manually

### Timeline:
```
Day 0-35:   Both terminals training different models
Day 35:     All models complete
```

---

## Before You Start: Check Your System

Run this to check if your system can handle parallel training:
```bash
check_system_resources.bat
```

### Interpreting Results:

**You can run PARALLEL if**:
- NumberOfLogicalProcessors ≥ 16
- TotalPhysicalMemory ≥ 17,179,869,184 bytes (16 GB)
- FreePhysicalMemory ≥ 12,582,912 KB (12 GB)
- LoadPercentage < 40%

**You should run SEQUENTIAL if**:
- NumberOfLogicalProcessors < 16
- TotalPhysicalMemory < 17,179,869,184 bytes
- FreePhysicalMemory < 12,582,912 KB
- LoadPercentage > 40%

---

## Current Training Status

### Check if Training is Already Running:
```bash
# PowerShell
Get-Process python | Select-Object Id, CPU, WorkingSet, StartTime

# Command Prompt
tasklist /FI "IMAGENAME eq python.exe" /V
```

### Monitor Progress:
```bash
# Check latest results folder
dir results\comprehensive_training_* /O-D

# View progress file
type results\comprehensive_training_YYYYMMDD_HHMMSS\training_progress.json
```

---

## Handling Conflicts

### If Both Scripts Try to Run Simultaneously:

**Will it cause errors?** 
- ❌ No errors - they use separate result directories
- ⚠️ But both will run slower due to resource contention

**What happens?**
1. Each creates a timestamped results folder
2. Both read from `data/processed/` (safe - read-only)
3. Both write to separate folders (no conflicts)
4. CPU/RAM usage doubles
5. Each takes 1.5-2x longer

### If You Need to Stop Training:

**Stop one training:**
- Press `Ctrl+C` in that terminal
- Or close the terminal window

**Stop all training:**
```bash
# PowerShell
Get-Process python | Stop-Process

# Command Prompt
taskkill /IM python.exe /F
```

---

## Results Organization

### Results Folder Structure:
```
results/
├── comprehensive_training_20260202_144642/  # 500-epoch run
│   ├── final_summary.json
│   ├── final_summary.txt
│   ├── training_config.json
│   ├── training_progress.json
│   ├── plots/
│   └── trained_models/
│
└── comprehensive_training_20260202_150000/  # 1000-epoch run
    ├── final_summary.json
    ├── final_summary.txt
    ├── training_config.json
    ├── training_progress.json
    ├── plots/
    └── trained_models/
```

### Identifying Which is Which:
Check `training_config.json`:
```json
{
  "max_rounds": 500,  // This is the 500-epoch run
  ...
}
```
or
```json
{
  "max_rounds": 1000,  // This is the 1000-epoch run
  ...
}
```

---

## Troubleshooting

### Problem: System is too slow
**Solution**: 
- Stop one training process
- Run sequentially instead
- Close other applications

### Problem: Out of memory
**Solution**:
- Stop one training process
- Reduce `clients_per_round` in config
- Run sequentially

### Problem: Can't tell which training is which
**Solution**:
- Check the terminal window title
- Check `training_config.json` in results folder
- Look at the timestamp in folder name

### Problem: Training stopped unexpectedly
**Solution**:
- Check the error in terminal
- Review logs in results folder
- Restart from the same command

---

## Recommendations by System Type

### Laptop (4-8 cores, 8-16 GB RAM):
- ✅ Use **Sequential Training** (Option 1)
- ⚠️ Avoid parallel training
- 💡 Train one model at a time if needed

### Desktop (8-16 cores, 16-32 GB RAM):
- ✅ Use **Parallel by Model** (Option 3)
- ✅ Or **Sequential Training** (Option 1)
- ⚠️ Full parallel might work but will be slow

### Workstation/Server (16+ cores, 32+ GB RAM):
- ✅ Use **Parallel Training** (Option 2)
- ✅ Or **Parallel by Model** (Option 3)
- 💡 Can even run more models in parallel

---

## Summary Table

| Option | Time | System Req | Complexity | Recommended For |
|--------|------|------------|------------|-----------------|
| Sequential | 53-62 days | Low | Easy | Most users |
| Parallel Full | 18-42 days | High | Easy | Powerful systems |
| Parallel by Model | 25-35 days | Medium | Medium | Balanced approach |

---

## Next Steps

1. **Check your system**: Run `check_system_resources.bat`
2. **Choose your approach**: Sequential, Parallel, or by Model
3. **Run the training**: Use the appropriate batch script
4. **Monitor progress**: Check results folders periodically
5. **Analyze results**: Compare 500 vs 1000 epoch performance

Good luck with your training! 🚀
