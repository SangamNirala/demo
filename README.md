# FedED-SegNAS — Presentation
### 15 Slides · Every Line Earns Its Place

---

---

# SLIDE 1 · Title

---

## FedED-SegNAS

### Federated Epistasis Detection
### with Segmented Neural Architecture Search

---

> **A Privacy-Preserving Deep Learning Framework for Genomic Disease Detection**

---

| Published | IEEE Transactions on Fuzzy Systems · Vol. 33, No. 1 · January 2025 |
|-----------|----------------------------------------------------------------------|
| Framework | Fuzzy CNN + Federated Learning + PSO-NAS |
| Scale | 50 hospitals · 192 datasets · 8 disease models · 6 SNP sizes |
| Key result | 96.22% NAS accuracy — beats DARTS, MnasNet, SGAS |

---

---

# SLIDE 2 · The Problem

---

## Genetic Diseases Are Caused by Gene Combinations — Not Single Genes

---

### Epistasis: The Hidden Interaction

```
Gene A alone   →   Healthy ✓
Gene B alone   →   Healthy ✓
Gene A + Gene B together   →   Disease ✗
```

> Traditional genetic tests look at **one gene at a time** — they miss this entirely.
> Up to **70% of genetic risk factors** go undetected this way.

---

### Three Barriers That Block Progress

| Barrier | Real Impact |
|---------|-------------|
| 🏥 **Data is scattered** | One hospital has 400 patients — not enough to find rare combinations |
| 🔒 **Privacy laws** | HIPAA (USA), Cyber Security Law (China) — raw DNA cannot be shared |
| 🧩 **Biological uncertainty** | Genotype `1` doesn't always mean exactly 50% risk — context matters |

---

### Why Existing Methods Fall Short

- **BOOST, AntEpiSeeker** — statistical methods, struggle with high-order interactions
- **Standard FL frameworks** — not designed for epistasis, ignore genomic security
- **Plain CNNs** — treat SNP values as hard numbers, miss biological ambiguity

---

---

# SLIDE 3 · Our Solution

---

## Three Innovations That Work Together

---

### 1 · Fuzzy CNN — Handles Biological Uncertainty
- Converts each SNP value into **3 fuzzy membership scores** (low / medium / high)
- Learns what those boundaries mean from data — not hardcoded
- Captures gene interaction patterns that standard CNNs miss

---

### 2 · Federated Learning — Privacy by Design
- **50 hospitals** train a shared model without sharing any patient data
- Only model weights travel over the network — raw DNA stays local
- Mathematically proven: **zero information leakage** from transmitted parameters

---

### 3 · PSO-NAS — Self-Optimizing Architecture
- Automatically searches for the best CNN structure for each dataset
- Balances accuracy, speed, and parameter count simultaneously
- Outperforms gradient-based NAS methods (DARTS, MnasNet) in accuracy

---

```
Hospital 1 ──┐
Hospital 2 ──┤──► Global Fuzzy CNN ──► Epistasis Detected
    ...       │        ↑
Hospital 50 ─┘    PSO-NAS optimizes
              (no raw data shared)
```

---

---

# SLIDE 4 · Understanding the Data

---

## Every Patient Is a Row. Every Gene Is a Column.

---

### The Raw Data Format

```
SNP1  SNP2  SNP3  ...  SNP50  Disease
  0     1     2   ...    0       1      ← Patient 1: diseased
  1     0     1   ...    2       0      ← Patient 2: healthy
  2     2     0   ...    1       1      ← Patient 3: diseased
```

---

### What 0, 1, 2 Mean — The Genotype Encoding

Every person inherits **two copies** of each gene (one from each parent).

| Value | Genotype | Biological Meaning | Risk Level |
|-------|----------|--------------------|------------|
| **0** | AA | Both copies normal | Baseline |
| **1** | AG | One copy mutated (heterozygous) | Partial |
| **2** | GG | Both copies mutated (homozygous) | Full |

---

### Why This Encoding Matters for the Model

- The ordering `0 < 1 < 2` reflects **increasing mutation dosage**
- The Fuzzy CNN uses this ordering to initialize membership functions at [0, 1, 2]
- Standard CNNs treat these as arbitrary numbers — Fuzzy CNN treats them as biology

---

---

# SLIDE 5 · The Dataset

---

## 192 Carefully Designed Genomic Datasets

---

### Dataset Organization

```
data/simulated/
└── model{1–8}/           ← 8 disease interaction types
    └── order{2, 3}/      ← 2-gene or 3-gene interactions
        └── snps{50 → 5000}/    ← 6 complexity levels
            ├── dataset_0.txt   ← replicate 1 (different random seed)
            └── dataset_1.txt   ← replicate 2 (same settings, different noise)
```

**8 × 2 × 6 × 2 = 192 datasets · 4,000 patients each · perfectly balanced 50/50**

---

### 8 Disease Models — Covering the Full Spectrum

| Models 1–4 (With Marginal Effects) | Models 5–8 (Pure Epistasis) |
|------------------------------------|------------------------------|
| Each gene has some individual effect | Genes are harmless alone |
| Additive · Multiplicative · Heterogeneous · Threshold | Pure Epistasis · XOR-like · Complex · Nested |
| Moderate difficulty | Hard → Very Hard |
| Baseline for comparison | The real challenge |

---

### Why 6 SNP Sizes?

`50 → 100 → 500 → 1000 → 2000 → 5000` — logarithmic progression.
Tests how the model scales from **quick debugging** to **genome-scale** data.

---

---

# SLIDE 6 · Data Pipeline

---

## From Raw Simulation to 50-Client Federated Splits

---

### Step 1 · Generate Datasets

```
experiments/generate_simple_datasets.py

→ Hardy-Weinberg equilibrium genotype sampling
→ Sigmoid-based disease risk model
→ Controlled heritability (H² = 0.10 or 0.15) and MAF (0.2 or 0.4)
→ Output: dataset_0.txt, dataset_1.txt per configuration
```

---

### Step 2 · Preprocess into Federated Format

```
experiments/data_preprocessing.py  →  DataPreprocessor

4000 patients × N SNPs
      ↓  stratified split (preserves class balance)
  70% train  |  15% validation  |  15% test
      ↓  IID distribution
  Split training data equally across 50 clients
      ↓  compress
  Save as .npz  (10× smaller · loads 5× faster)
```

---

### Step 3 · Validate

```
experiments/validate_data.py  →  DataValidator

Checks: class balance · missing values · genotype encoding {0,1,2}
Calculates: MAF per SNP · federated split integrity
Output: results/validation_report.txt
```

---

### What Each .npz Contains

```
client_0_X/y  ...  client_49_X/y   ← 50 hospital data splits
validation_X/y                      ← shared validation (server-side)
test_X/y                            ← held-out test set
metadata                            ← shapes, class distribution, num_clients
```

---

---

# SLIDE 7 · Fuzzy CNN — The Core Idea

---

## Why Standard CNNs Fail on Genomic Data

---

### The Hard-Number Problem

A standard CNN sees genotype `1` as exactly `1.0` — a fixed point.

But in biology, **heterozygous (AG) doesn't always mean 50% risk**.
The actual effect depends on which other genes are active — context matters.

---

### The Fuzzy Solution: Degrees of Membership

Each SNP value becomes **three soft scores** instead of one hard number:

```
SNP = 0  →  { low: 0.95,  medium: 0.10,  high: 0.00 }
SNP = 1  →  { low: 0.10,  medium: 0.95,  high: 0.10 }
SNP = 2  →  { low: 0.00,  medium: 0.10,  high: 0.95 }
```

The network **learns** what "low", "medium", "high" mean for each gene.

---

### The Gaussian Membership Formula (from the paper)

```
membership = exp( −((x − mean)²) / (2 × std²) )

means → initialized at [0, 1, 2], then trained
stds  → initialized at 0.4, constrained positive via softplus
```

- **Trainable means**: the model shifts fuzzy boundaries to fit the data
- **Softplus constraint**: `std = softplus(log_std) + 1e-6` — never goes negative
- **Result**: 6 trainable parameters that encode all biological uncertainty

---

---

# SLIDE 8 · Fuzzy CNN — Full Architecture

---

## Every Layer Has a Specific Job

---

```
Input  (batch × num_snps)        ← raw SNP values {0, 1, 2}
    ↓
InputNormalizationLayer          ← (x − 1.0) / 0.8165  →  zero mean, unit variance
    ↓
ImprovedFuzzificationLayer       ← (batch × num_snps × 3)  →  3 membership scores per SNP
    ↓
BatchNormalization                ← stabilizes fuzzy output distribution
    ↓
ImprovedFuzzyConvBlock × N       ← detects gene-gene interaction patterns
  Conv1D + BatchNorm + Swish + Residual + Dropout
    ↓
SNPAttentionLayer                 ← learns which SNPs are most predictive
    ↓
LearnableDefuzzificationLayer    ← converts fuzzy maps back to crisp features
    ↓
GlobalAvgPool + GlobalMaxPool → Concatenate   ← captures both average and peak signals
    ↓
Dense + BatchNorm + Swish + Dropout  (×2)
    ↓
Dense(2) + Softmax               ← {0 = healthy, 1 = diseased}
```

---

### Adaptive Architecture — One Model for All SNP Sizes

| SNP Count | Blocks | Filters | Kernels | Dense |
|-----------|--------|---------|---------|-------|
| ≤ 50 | 3 | [32, 64, 128] | [3, 3, 3] | [128, 64] |
| ≤ 200 | 3 | [64, 128, 256] | [5, 3, 3] | [256, 128] |
| ≤ 1000 | 4 | [64, 128, 256, 512] | [7, 5, 3, 3] | [512, 256] |
| > 1000 | 5 | [64, 128, 256, 512, 512] | [9, 7, 5, 3, 3] | [512, 256, 128] |

> Same `build_fuzzy_cnn(num_snps)` call — architecture chosen automatically.

---

---

# SLIDE 9 · Federated Learning

---

## 50 Hospitals. One Model. Zero Data Sharing.

---

### The Training Loop (Repeated 200–1000 Rounds)

```
Central Server holds Global Fuzzy CNN
        │
        ▼  broadcast weights
Select 12–15 random clients this round
        │
        ▼  local training
Each client trains on its own data (2–3 epochs)
  → FedProx loss prevents drifting from global model
  → Adaptive batch size (16–64) based on local data size
  → Gradient clipping (clipnorm=1.0) for stability
        │
        ▼  upload weights only
Server aggregates:
  → Sample-weighted FedAvg (larger datasets contribute more)
  → Quality weighting (underperforming clients get 0.5× weight)
        │
        ▼  evaluate
Validate on shared validation set
  → EMA smoothing over last 10 rounds (stable early stopping)
  → Save best model weights automatically
```

---

### Why This Works for Genomic Data

- **IID splits** across clients → fair contribution from each hospital
- **Class weights** computed per client → handles imbalanced disease data
- **Every 10 rounds**: Keras session cleared → prevents out-of-memory crashes on long runs

---

---

# SLIDE 10 · FedProx — Preventing Client Drift

---

## The Biggest Problem in Federated Learning — Solved

---

### What Is Client Drift?

Each hospital has different patients → different data distributions.
Without control, each client's model drifts in a different direction.
Aggregating drifted models → the global model gets **worse**, not better.

---

### FedProx: Add a Proximal Term to the Loss

```
Standard FedAvg:   Loss = CrossEntropy(predictions, labels)

FedProx:           Loss = CrossEntropy(predictions, labels)
                        + (μ/2) × ‖ w_local − w_global ‖²
                                    ↑
                          penalizes moving too far from global model
```

- **μ = 0.01** (default) · **μ = 0.005** (high-accuracy mode)
- Lower μ → more freedom to adapt locally
- Higher μ → tighter alignment with global model

---

### Learning Rate Schedule — Two Phases

```
Phase 1 — Warmup (rounds 1 → 15):
  LR rises linearly:  0.00001 → 0.003
  Prevents unstable gradients at the start

Phase 2 — Cosine Annealing (rounds 15 → 500):
  LR decays smoothly:  0.003 → 0.00001
  Enables fine-tuning without overshooting
```

---

### Result: Stable Convergence Across All 8 Disease Models

- Client drift tracked per round → logged in `*_history.json`
- Average drift decreases over training → confirms FedProx is working
- Best model weights saved automatically → restored before final evaluation

---

---

# SLIDE 11 · Neural Architecture Search

---

## The Model Designs Itself

---

### The Problem NAS Solves

Manually picking CNN architecture means:
- Guessing filter sizes, kernel sizes, depth, dropout
- Different optimal architecture for snps50 vs snps5000
- Hours of trial and error per dataset

**PSO-NAS eliminates all of this.**

---

### Each Architecture = A 16-Number Vector

```
[ num_blocks,
  block0_filters,  block0_kernel,  block0_pool,
  block1_filters,  block1_kernel,  block1_pool,
  block2_filters,  block2_kernel,  block2_pool,
  block3_filters,  block3_kernel,  block3_pool,
  dense_1,  dense_2,  dropout ]

Valid options:
  num_blocks: 1–4
  filters:    [32, 48, 64, 96, 128, 192, 256]
  kernels:    [3, 5, 7]
  pool:       MaxPool / AvgPool / None
  dense:      [64, 128, 192, 256, 384, 512]
  dropout:    0.1 – 0.5
```

---

### 4 Objectives — Optimized Simultaneously

| Objective | Formula | Why It Matters |
|-----------|---------|----------------|
| **f1** | Nfalse / Nall | Accuracy — the primary goal |
| **f2** | num_blocks | Simpler models generalize better |
| **f3** | num_parameters | Fewer params → less communication overhead |
| **f4** | GFLOPs | Faster training → more FL rounds possible |

---

### 3-Stage Fitness — Adapts to FL Progress

| Stage | When | Fitness | Strategy |
|-------|------|---------|----------|
| 1 | 0 → R/3 | f1 + f2 + f3 + f4 | Explore broadly — find good candidates |
| 2 | R/3 → 2R/3 | f1 + f4 | Prioritize speed — reduce computation |
| 3 | 2R/3 → R | f1 + f3 | Prioritize parameters — reduce comm cost |

---

---

# SLIDE 12 · PSO in Action

---

## How 15 Particles Find the Best Architecture

---

### The Swarm Concept

```
15 particles, each = one candidate CNN architecture (16-dim vector)

Each particle remembers:
  pbest  →  best architecture it personally found
  gbest  →  best architecture any particle has found

Particles move through architecture space, pulled toward both.
```

---

### Velocity Update — How Particles Move

```
v_new = ω × v_old
      + C1 × r1 × (pbest − position)   ← personal experience
      + C2 × r2 × (gbest − position)   ← swarm knowledge

ω decays 0.9 → 0.4  (explore early, exploit late)
C1 = C2 = 2.0  (balanced personal vs social pull)
```

---

### Five Smart Features That Prevent Failure

| Feature | Problem It Solves |
|---------|-------------------|
| **Boundary reflection** | Particles bounce off limits — no invalid architectures |
| **Architecture cache** | MD5 hash — never evaluates the same architecture twice |
| **Pareto front** | Keeps all non-dominated solutions — not just the single best |
| **Stagnation detection** | Perturbs stuck particles after 5 rounds without improvement |
| **Diversity maintenance** | Reinitializes worst 20% if swarm converges too early |

---

### What Happens When NAS Finds a Better Architecture

```
1. Build new model from discovered architecture
2. Transfer compatible weights from old model (same-shape layers)
3. If no weights transferred → fine-tune new model for 5 epochs
4. Replace global model → continue federated training
```

---

---

# SLIDE 13 · Training System

---

## One Script. Four Modes. Full Automation.

---

### 4 Training Presets — Pick One and Run

| Preset | Rounds | Patience | Clients/Round | Best For |
|--------|--------|----------|---------------|----------|
| `default` | 200 | 25 | 12 | Quick results, balanced accuracy |
| `high-accuracy` | 500 | 80 | 15 | Best accuracy, publication quality |
| `quick` | 30 | 10 | 8 | Debugging, sanity checks |
| `with-nas` | 300 | 30 | 12 | Architecture search enabled |

---

### Run Any Configuration from CLI

```bash
# High accuracy — recommended for final results
python train_all_models_comprehensive.py --high-accuracy

# Train one specific model
python train_all_models_comprehensive.py --model model4

# Paper configuration — 1000 rounds, no early stopping
python train_all_models_comprehensive222.py

# Custom override — full control
python train_all_models_comprehensive.py \
    --min-rounds 100 --max-rounds 400 --patience 50 \
    --clients-per-round 15 --initial-lr 0.003
```

---

### Everything Saved Automatically Per Dataset

```
results/comprehensive_training_YYYYMMDD_HHMMSS/
  ├── *_result.json    ← accuracy, F1, precision, recall, rounds used
  ├── *_model.h5       ← trained Keras model (loadable anytime)
  ├── *_history.json   ← per-round: val_accuracy, LR, client drift
  └── *_training.png   ← 4-panel plot: accuracy · loss · LR · drift
```

> Progress saved after every dataset — safe to interrupt and resume.

---

---

# SLIDE 14 · Results

---

## Numbers That Validate the Approach

---

### Centralized Fuzzy CNN — Accuracy by Disease Model

| Model | Interaction Type | Accuracy | Verdict |
|-------|-----------------|----------|---------|
| model1 | Additive (marginal) | ~62% | Good |
| model2 | Multiplicative (marginal) | ~63% | Good |
| model3 | Heterogeneous (marginal) | ~90% | ✅ Excellent |
| model4 | Threshold (marginal) | ~91% | ✅ Excellent |
| model5 | Pure Epistasis | ~62% | Good |
| model6 | XOR-like | ~64% | Good |
| model7 | Complex | ~93% | ✅ Excellent |
| model8 | Nested | ~92% | ✅ Excellent |

> **50% Excellent · 50% Good · Avg ~1.2 min/dataset · Early stopping in 30–55 epochs**

---

### Federated vs Centralized — The Privacy Trade-off

| Mode | Best Accuracy | What It Means |
|------|---------------|---------------|
| Centralized | ~93% | All data merged — upper bound |
| Federated | **74.33%** | Data split across 50 clients — privacy preserved |

> The 19% gap is the **cost of privacy** — and it's worth it.

---

### NAS Beats Gradient-Based Methods (CIFAR-10 Benchmark)

| Method | Accuracy | Params | Search Type |
|--------|----------|--------|-------------|
| DARTS | 95.19% | 3.3M | Gradient |
| MnasNet | 94.52% | 3.1M | Gradient |
| SGAS | 92.05% | 4.7M | Gradient |
| **FedED-SegNAS** | **96.22%** | **2.1M** | **PSO** |

> Highest accuracy · Fewest parameters · ~30% better GFLOPs than gradient-based methods

---

---

# SLIDE 15 · Summary

---

## What Was Built — And Why It Matters

---

### The Complete System in One View

```
Raw Genomic Data (GAMETES simulation)
        ↓
Data Pipeline → 192 datasets · 50-client federated splits · validated
        ↓
Fuzzy CNN → 6 custom Keras layers · adaptive architecture · ~259K params
        ↓
Federated Training → FedProx · quality weighting · EMA early stopping
        ↓
PSO-NAS → 3-stage multi-objective · Pareto front · architecture caching
        ↓
Results → accuracy · F1 · plots · saved models · per-round history
```

---

### Six Decisions That Made It Work

| Decision | Impact |
|----------|--------|
| **Swish over Sigmoid** | Eliminated vanishing gradients in fuzzy conv blocks |
| **FedProx over FedAvg** | Reduced client drift — stable convergence across all models |
| **Softplus for fuzzy stds** | Guaranteed positive fuzzy set widths — no training instability |
| **EMA smoothing** | Prevented premature early stopping from noisy validation curves |
| **Adaptive architecture** | Same codebase handles 50 → 5000 SNPs without modification |
| **3-stage NAS fitness** | Balanced accuracy vs efficiency as FL training matured |

---

### The Numbers That Tell the Story

| Metric | Value |
|--------|-------|
| Datasets generated & trained | **192** |
| Federated clients per dataset | **50** |
| Fuzzy CNN parameters | **~259K** (well under 5M limit) |
| Best federated test accuracy | **74.33%** (model4, order3, snps100) |
| Best centralized accuracy | **93%** (models 3, 4, 7, 8) |
| NAS accuracy on CIFAR-10 | **96.22%** — beats DARTS, MnasNet, SGAS |
| Privacy brute-force resistance | **27 years** to crack N=12 parameters |

---

> *"FedED-SegNAS proves that hospitals can collaborate on genomic research
> at scale — without ever sharing a single patient record."*

---
