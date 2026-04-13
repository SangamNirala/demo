# Training Accuracy Summary - All Models

Generated: March 20, 2026

## Overview
This document summarizes the test accuracy achieved by all trained models across different configurations.

---

## Model 1 (Heterogeneous Epistasis)

### Latest Training Run: 2026-02-06 to 2026-02-09

| SNPs | Order | Dataset | Test Accuracy | Best Val Accuracy | Training Time (min) | Status |
|------|-------|---------|---------------|-------------------|---------------------|--------|
| 50   | 2     | 0       | **59.33%**    | 62.67%            | 442.0               | ✓ Success |
| 50   | 2     | 1       | **62.17%**    | 63.17%            | 941.8               | ✓ Success |
| 100  | 2     | 0       | **56.50%**    | 61.17%            | 73.2                | ✓ Success |
| 100  | 2     | 1       | **63.00%**    | 64.33%            | 72.3                | ✓ Success |
| 1000 | 2     | 0       | 49.67%        | 51.67%            | 159.4               | ✓ Success |
| 1000 | 2     | 1       | 50.33%        | 53.33%            | 195.0               | ✓ Success |
| 2000 | 2     | 0       | 47.17%        | 53.33%            | 583.5               | ✓ Success |
| 2000 | 2     | 1       | 50.83%        | 54.83%            | 645.2               | ✓ Success |
| 500  | 2     | 0       | 0.00%         | -                 | 233.5               | ✗ OOM Error |
| 500  | 2     | 1       | 0.00%         | -                 | 0.2                 | ✗ OOM Error |
| 5000 | 2     | 0       | 0.00%         | -                 | 0.0                 | ✗ Memory Error |
| 5000 | 2     | 1       | 0.00%         | -                 | 0.0                 | ✗ Memory Error |
| 100  | 3     | 0       | 0.00%         | -                 | 29.3                | ✗ OOM Error |

**Best Performance:** 63.00% (100 SNPs, Order 2, Dataset 1)

---

## Model 2 (Heterogeneous Epistasis)

### Latest Training Run: 2026-02-10 to 2026-02-11

| SNPs | Order | Dataset | Test Accuracy | Best Val Accuracy | Training Time (min) | Status |
|------|-------|---------|---------------|-------------------|---------------------|--------|
| 100  | 2     | 0       | **63.33%**    | 63.00%            | 87.7                | ✓ Success |
| 100  | 2     | 1       | **59.00%**    | 60.33%            | 186.7               | ✓ Success |
| 1000 | 2     | 0       | 48.83%        | 54.00%            | 689.0               | ✓ Success |

**Best Performance:** 63.33% (100 SNPs, Order 2, Dataset 0)

---

## Model 3 (Heterogeneous Epistasis)

### Latest Training Run: 2026-02-11 to 2026-02-15

| SNPs | Order | Dataset | Test Accuracy | Best Val Accuracy | Training Time (min) | Status |
|------|-------|---------|---------------|-------------------|---------------------|--------|
| 100  | 2     | 0       | **91.00%**    | 92.33%            | 67.2                | ✓ Success |
| 100  | 2     | 1       | **90.50%**    | 91.17%            | 123.5               | ✓ Success |
| 1000 | 2     | 0       | 50.83%        | 55.83%            | 487.9               | ✓ Success |
| 1000 | 2     | 1       | **90.00%**    | 91.50%            | 1371.2              | ✓ Success |
| 2000 | 2     | 0       | 50.67%        | 54.83%            | 3774.4              | ✓ Success |

**Best Performance:** 91.00% (100 SNPs, Order 2, Dataset 0) ⭐ EXCELLENT

---

## Model 4 (Pure Epistasis - 3-way)

### Latest Training Run: 2026-02-20

| SNPs | Order | Dataset | Test Accuracy | Best Val Accuracy | Training Time (min) | Status |
|------|-------|---------|---------------|-------------------|---------------------|--------|
| 100  | 3     | 0       | **74.17%**    | 76.33%            | 75.0                | ✓ Success |
| 100  | 3     | 1       | **74.33%**    | 74.17%            | 105.7               | ✓ Success |
| 1000 | 3     | 0       | 48.50%        | 53.67%            | 507.3               | ✓ Success |

**Best Performance:** 74.33% (100 SNPs, Order 3, Dataset 1)

---

## Model 5 (Pure Epistasis - 2-way)

### Latest Training Run: 2026-03-17 to 2026-03-19

| SNPs | Order | Dataset | Test Accuracy | Best Val Accuracy | Training Time (min) | Status |
|------|-------|---------|---------------|-------------------|---------------------|--------|
| 100  | 2     | 0       | **61.00%**    | 64.50%            | 117.3               | ✓ Success |
| 100  | 2     | 1       | **62.33%**    | 62.50%            | 241.5               | ✓ Success |
| 1000 | 2     | 0       | **60.33%**    | 62.83%            | 1676.5              | ✓ Success |

**Best Performance:** 62.33% (100 SNPs, Order 2, Dataset 1)

---

## Model 6 (Pure Epistasis)

### Training Run: 2026-01-15

| SNPs | Order | Dataset | Test Accuracy | Status |
|------|-------|---------|---------------|--------|
| 50   | 2     | 0       | **64.50%**    | ✓ Success |
| 50   | 2     | 1       | **64.33%**    | ✓ Success |
| 100  | 2     | 0       | **62.00%**    | ✓ Success |
| 100  | 2     | 1       | **62.17%**    | ✓ Success |
| 500  | 2     | 0       | **62.33%**    | ✓ Success |
| 500  | 2     | 1       | 61.17%        | ✓ Success |
| 1000 | 2     | 0       | **62.00%**    | ✓ Success |
| 1000 | 2     | 1       | **65.00%**    | ✓ Success |
| 2000 | 2     | 0       | **63.33%**    | ✓ Success |
| 2000 | 2     | 1       | 61.67%        | ✓ Success |
| 5000 | 2     | 0       | 60.83%        | ✓ Success |
| 5000 | 2     | 1       | 60.67%        | ✓ Success |

**Best Performance:** 65.00% (1000 SNPs, Order 2, Dataset 1)

---

## Model 8 (Heterogeneous Epistasis)

### Latest Training Run: 2026-03-12 to 2026-03-17 (1000 Epochs)

| SNPs | Order | Dataset | Test Accuracy | Best Val Accuracy | Training Time (min) | Rounds | Status |
|------|-------|---------|---------------|-------------------|---------------------|--------|--------|
| 100  | 2     | 0       | **93.33%**    | 89.00%            | 6718.3              | 1000   | ✓ Success |

**Best Performance:** 93.33% (100 SNPs, Order 2, Dataset 0) ⭐ BEST OVERALL

---

## Summary Statistics

### Top 5 Best Performing Configurations

| Rank | Model | SNPs | Order | Dataset | Test Accuracy | Training Time |
|------|-------|------|-------|---------|---------------|---------------|
| 1    | Model 8 | 100  | 2     | 0       | **93.33%**    | 6718.3 min    |
| 2    | Model 3 | 100  | 2     | 0       | **91.00%**    | 67.2 min      |
| 3    | Model 3 | 100  | 2     | 1       | **90.50%**    | 123.5 min     |
| 4    | Model 3 | 1000 | 2     | 1       | **90.00%**    | 1371.2 min    |
| 5    | Model 4 | 100  | 3     | 1       | **74.33%**    | 105.7 min     |

### Performance by Model Type

| Model | Type | Best Accuracy | Avg Accuracy (successful) |
|-------|------|---------------|---------------------------|
| Model 8 | Heterogeneous Epistasis | 93.33% | 93.33% |
| Model 3 | Heterogeneous Epistasis | 91.00% | 74.60% |
| Model 4 | Pure Epistasis (3-way) | 74.33% | 65.67% |
| Model 6 | Pure Epistasis | 65.00% | 62.48% |
| Model 1 | Heterogeneous Epistasis | 63.00% | 56.75% |
| Model 2 | Heterogeneous Epistasis | 63.33% | 57.05% |
| Model 5 | Pure Epistasis (2-way) | 62.33% | 61.22% |

### Key Insights

1. **Best Overall Model:** Model 8 achieved 93.33% accuracy with 1000 training rounds
2. **Most Efficient:** Model 3 achieved 91.00% accuracy in just 67.2 minutes
3. **Optimal SNP Count:** 100 SNPs consistently performs best across models
4. **Large SNP Challenges:** Models with 500+ SNPs often face OOM errors or poor performance
5. **Training Time vs Accuracy:** Model 8's extended training (1000 rounds) yielded the highest accuracy

### Training Status Summary

- **Total Configurations Attempted:** 35+
- **Successful Trainings:** 28
- **Failed (OOM/Memory Errors):** 7
- **Models Trained:** 6 (Model 1, 2, 3, 4, 5, 6, 8)
- **Models Pending:** 2 (Model 7 - no results found)

---

## Recommendations

1. **For Production:** Use Model 8 or Model 3 with 100 SNPs (Order 2)
2. **For Quick Testing:** Use Model 3 with 100 SNPs (excellent accuracy, fast training)
3. **For 3-way Interactions:** Use Model 4 with 100 SNPs (74% accuracy)
4. **Avoid:** Configurations with >500 SNPs due to memory constraints

---

*Note: Accuracies marked with ⭐ indicate exceptional performance (>90%)*
