# Training Files Comparison

## Overview

You now have two training files with different configurations:

| File | Default Rounds | Purpose |
|------|----------------|---------|
| `train_all_models_comprehensive.py` | **200** | Faster training, good results |
| `train_all_models_comprehensive222.py` | **1000** | Paper-compliant, best results |

---

## File 1: train_all_models_comprehensive.py

### Default Configuration (200 rounds):
```bash
python train_all_models_comprehensive.py
```

**Settings:**
- Minimum rounds: 50
- Maximum rounds: **200**
- Early stopping: Yes (patience=25)
- Time per dataset: ~1.2 hours
- Total time (178 datasets): **~9 days**

### High Accuracy Configuration (500 rounds):
```bash
python train_all_models_comprehensive.py --high-accuracy
```

**Settings:**
- Minimum rounds: 100
- Maximum rounds: **500**
- Early stopping: Yes (patience=40)
- Time per dataset: ~2.8 hours
- Total time (178 datasets): **~21 days**

### Quick Test Configuration (30 rounds):
```bash
python train_all_models_comprehensive.py --quick
```

**Settings:**
- Minimum rounds: 10
- Maximum rounds: **30**
- Early stopping: Yes (patience=10)
- Time per dataset: ~0.2 hours
- Total time (178 datasets): **~1.5 days**

---

## File 2: train_all_models_comprehensive222.py

### Default Configuration (1000 rounds):
```bash
python train_all_models_comprehensive222.py
```

**Settings:**
- Minimum rounds: 1000
- Maximum rounds: **1000**
- Early stopping: **NO** (patience=None)
- Time per dataset: ~6 hours
- Total time (178 datasets): **~44.5 days**

### Paper 1000 Configuration (alternative):
```bash
python train_all_models_comprehensive222.py --paper-1000
```

**Settings:**
- Minimum rounds: 1000
- Maximum rounds: **1000**
- Early stopping: **NO**
- More conservative (2 local epochs, 15 clients)
- Time per dataset: ~6 hours
- Total time (178 datasets): **~44.5 days**

### High Accuracy Configuration (500 rounds):
```bash
python train_all_models_comprehensive222.py --high-accuracy
```

**Settings:**
- Same as train_all_models_comprehensive.py --high-accuracy
- Maximum rounds: **500**
- Total time: **~21 days**

---

## Quick Reference Table

| Command | Rounds | Early Stop | Time (178 datasets) | Use Case |
|---------|--------|------------|---------------------|----------|
| `python train_all_models_comprehensive.py` | **200** | ✅ Yes | **~9 days** | Fast, good results |
| `python train_all_models_comprehensive.py --high-accuracy` | **500** | ✅ Yes | **~21 days** | Better results |
| `python train_all_models_comprehensive.py --quick` | **30** | ✅ Yes | **~1.5 days** | Testing only |
| `python train_all_models_comprehensive222.py` | **1000** | ❌ No | **~44.5 days** | Paper-compliant |
| `python train_all_models_comprehensive222.py --paper-1000` | **1000** | ❌ No | **~44.5 days** | Paper (alternative) |
| `python train_all_models_comprehensive222.py --high-accuracy` | **500** | ✅ Yes | **~21 days** | Better results |

---

## Which File Should You Use?

### Use `train_all_models_comprehensive.py` if:
- ✅ You want **faster results** (~9 days)
- ✅ You're okay with **200 rounds** per dataset
- ✅ You want **early stopping** to save time
- ✅ You need results quickly for analysis

### Use `train_all_models_comprehensive222.py` if:
- ✅ You want **paper-compliant** results (1000 rounds)
- ✅ You want **maximum accuracy**
- ✅ You have **time** (~44.5 days)
- ✅ You need results for publication

### Use `--high-accuracy` flag if:
- ✅ You want a **balance** between speed and accuracy
- ✅ 500 rounds is enough for your needs
- ✅ ~21 days is acceptable

---

## Recommendations

### For Quick Experimentation:
```bash
python train_all_models_comprehensive.py --quick
```
- Test your setup in ~1.5 days
- Verify everything works
- Then run full training

### For Production/Research:
```bash
python train_all_models_comprehensive.py --high-accuracy
```
- Good balance: 500 rounds, ~21 days
- High accuracy without excessive time
- Recommended for most use cases

### For Paper Publication:
```bash
python train_all_models_comprehensive222.py
```
- Full 1000 rounds as per paper
- Maximum accuracy
- Takes ~44.5 days but worth it for publication

### For Fast Results:
```bash
python train_all_models_comprehensive.py
```
- 200 rounds, ~9 days
- Good accuracy
- Fast turnaround

---

## Configuration Details

### train_all_models_comprehensive.py - DEFAULT:
```python
{
    'min_rounds': 50,
    'max_rounds': 200,
    'patience': 25,
    'local_epochs': 3,
    'clients_per_round': 12,
    'initial_lr': 0.005,
    'warmup_rounds': 10,
}
```

### train_all_models_comprehensive.py - HIGH_ACCURACY:
```python
{
    'min_rounds': 100,
    'max_rounds': 500,
    'patience': 40,
    'local_epochs': 2,
    'clients_per_round': 15,
    'initial_lr': 0.003,
    'warmup_rounds': 15,
}
```

### train_all_models_comprehensive222.py - DEFAULT:
```python
{
    'min_rounds': 1000,
    'max_rounds': 1000,
    'patience': None,  # NO early stopping
    'local_epochs': 3,
    'clients_per_round': 12,
    'initial_lr': 0.005,
    'warmup_rounds': 50,
}
```

---

## Summary

**Two files, different purposes:**

1. **`train_all_models_comprehensive.py`** - Fast (200 rounds default)
   - Use for quick results
   - Use `--high-accuracy` for 500 rounds

2. **`train_all_models_comprehensive222.py`** - Paper-compliant (1000 rounds)
   - Use for publication
   - Use for maximum accuracy

**Choose based on your needs: speed vs. accuracy!**
