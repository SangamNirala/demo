# FedED-SegNAS — Presentation Speaker Script
### Total Duration: ~17 minutes | Speaking pace: ~130 words/minute
### Each slide's word count = time × 130

---

## How to Use This Script
- Read naturally, don't rush
- Pause briefly at each `[PAUSE]` marker
- Bold words = slight emphasis when speaking
- Total words across all slides ≈ 2,210

---

---

## SLIDE 1 · Title
**⏱ Time: ~40 seconds | Words: ~85**

---

Good morning everyone. Today I'm presenting **FedED-SegNAS** — a framework I implemented for detecting complex genetic diseases using federated deep learning.

The full name is Federated Epistasis Detection with Segmented Neural Architecture Search. This work is based on a paper published in IEEE Transactions on Fuzzy Systems in January 2025.

What makes this project unique is that it combines three things at once — a Fuzzy CNN for handling biological uncertainty, Federated Learning so hospitals can collaborate without sharing patient data, and an automated architecture search that finds the best model structure on its own.

Let me walk you through how it all works.

---

---

## SLIDE 2 · The Problem
**⏱ Time: ~90 seconds | Words: ~195**

---

Let's start with the problem we're solving.

Most people assume genetic diseases are caused by a single faulty gene. But that's rarely true. The real cause is often **epistasis** — when two or more genes interact together to cause disease, even though each gene alone is completely harmless.

Think of it this way. Gene A alone — healthy. Gene B alone — healthy. But Gene A and Gene B together — disease. [PAUSE] Traditional genetic tests look at one gene at a time, so they miss this interaction entirely. Research suggests up to 70% of genetic risk factors go undetected this way.

Now, to detect these interactions reliably, you need large datasets — thousands of patients. But no single hospital has that many. So hospitals need to collaborate. [PAUSE] The problem is, privacy laws like HIPAA in the US and the Cyber Security Law in China prevent hospitals from sharing raw patient DNA data.

And there's a third challenge — biological uncertainty. Genotype values zero, one, and two are not perfectly discrete. A heterozygous gene doesn't always mean exactly 50% risk. Context matters.

This is why existing methods like BOOST and standard federated learning frameworks fall short. They weren't designed for this problem.

---

---

## SLIDE 3 · Our Solution
**⏱ Time: ~75 seconds | Words: ~160**

---

So here's what FedED-SegNAS does to solve all three problems.

**First**, the Fuzzy CNN. Instead of treating each gene value as a hard number, we convert it into three fuzzy membership scores — representing low, medium, and high risk. This captures the biological uncertainty that standard CNNs completely ignore.

**Second**, Federated Learning. We have 50 hospitals training a shared model together. But here's the key — no raw patient data ever leaves the hospital. Only model weights travel over the network. And we've mathematically proven that an attacker gains zero information from those transmitted weights.

**Third**, PSO-based Neural Architecture Search. Instead of manually choosing the CNN structure, the system automatically searches for the best architecture for each dataset. And it outperforms gradient-based NAS methods like DARTS and MnasNet in both accuracy and parameter efficiency.

[PAUSE] These three components work together as one unified framework — each solving a different piece of the problem.

---

---

## SLIDE 4 · Understanding the Data
**⏱ Time: ~70 seconds | Words: ~150**

---

Before we go into the model, let me explain what the data actually looks like.

Each row in our dataset represents one patient. Each column represents one SNP — a Single Nucleotide Polymorphism — which is a specific position in that person's DNA where people differ from each other.

The values in each cell are zero, one, or two. [PAUSE] Here's why. Every person inherits two copies of each gene — one from their mother, one from their father. If both copies are normal, we encode that as zero. If one copy is mutated, that's one — heterozygous. If both copies are mutated, that's two — homozygous mutant.

The last column is the disease label. Zero means healthy, one means diseased.

This encoding is not arbitrary. The ordering zero, one, two reflects increasing mutation dosage. And our Fuzzy CNN specifically uses this ordering — it initializes its fuzzy membership functions at exactly zero, one, and two to match the biology.

---

---

## SLIDE 5 · The Dataset
**⏱ Time: ~65 seconds | Words: ~140**

---

Now let's look at the scale of the dataset we built.

We generated **192 simulated genomic datasets** using a tool called GAMETES. The datasets are organized across three dimensions. First, eight disease models — covering everything from simple additive interactions to complex nested epistasis. Second, two epistasis orders — two-gene interactions and three-gene interactions. Third, six SNP sizes — from 50 SNPs all the way up to 5,000 SNPs.

Eight times two times six times two replicates gives us 192 datasets. Each dataset has 4,000 patients — perfectly balanced, 2,000 cases and 2,000 controls.

The eight disease models are split into two groups. Models one through four have marginal effects — meaning each gene has some individual impact on disease. Models five through eight are pure epistasis — the genes are completely harmless alone, and only dangerous in combination. [PAUSE] This second group is significantly harder to detect, and that's intentional — it tests the limits of the model.

---

---

## SLIDE 6 · Data Pipeline
**⏱ Time: ~75 seconds | Words: ~160**

---

Let me walk through how raw simulation data becomes federated training data.

**Step one is generation.** We use `generate_simple_datasets.py` which implements Hardy-Weinberg equilibrium genotype sampling and a sigmoid-based disease risk model. It generates dataset zero and dataset one for each configuration — two independent replicates with different random seeds, same settings.

**Step two is preprocessing.** The `DataPreprocessor` class takes each raw text file of 4,000 patients and does three things. It splits the data — 70% for training, 15% for validation, 15% for test — using stratified splitting to preserve class balance. Then it distributes the training data equally across 50 clients in an IID fashion. Finally it saves everything as a compressed `.npz` file, which is ten times smaller than the original text file.

**Step three is validation.** The `DataValidator` checks class balance, missing values, genotype encoding, and MAF per SNP. It generates a full validation report.

Each `.npz` file contains 50 client data splits, a shared validation set, a held-out test set, and metadata. This is the exact format the federated trainer expects.

---

---

## SLIDE 7 · Fuzzy CNN — The Core Idea
**⏱ Time: ~80 seconds | Words: ~170**

---

Now let's get into the model itself. The most important innovation is the Fuzzy CNN.

Here's the core problem with standard CNNs on genomic data. A standard CNN sees genotype one as exactly 1.0 — a fixed, hard number. But in biology, a heterozygous gene doesn't always mean 50% risk. The actual effect depends on which other genes are active. Context matters enormously.

The fuzzy solution is to replace that single hard number with **three soft membership scores**. For SNP value zero, the scores might be 0.95 low, 0.10 medium, 0.00 high. For SNP value one, it's 0.10 low, 0.95 medium, 0.10 high. For SNP value two, it's 0.00 low, 0.10 medium, 0.95 high.

The network learns what "low", "medium", and "high" actually mean for each gene — it's not hardcoded.

The formula is a Gaussian membership function — exponential of negative squared distance from the mean, divided by twice the variance. [PAUSE] The means are initialized at zero, one, and two to match the genotypes, and they're trainable. The standard deviations are also trainable, but constrained to always be positive using a softplus transformation. That's just six trainable parameters encoding all the biological uncertainty.

---

---

## SLIDE 8 · Fuzzy CNN — Full Architecture
**⏱ Time: ~80 seconds | Words: ~170**

---

Let me now walk through the complete model architecture layer by layer.

The input is a batch of SNP vectors — raw values zero, one, or two. The first thing we do is normalize them to zero mean and unit variance using pre-computed statistics for the SNP distribution.

Then comes the fuzzification layer — this is where each SNP value becomes three membership scores, expanding the shape from batch by num-SNPs to batch by num-SNPs by three.

After batch normalization, we pass through N fuzzy convolutional blocks. Each block does Conv1D, batch normalization, Swish activation — which replaced sigmoid to eliminate vanishing gradients — dropout, and a residual connection. The residual connection uses a 1x1 convolution projection when channel dimensions change.

Then the SNP attention layer learns which SNP positions are most predictive for disease. This is a simple attention mechanism — dense layer, softmax, multiply.

The learnable defuzzification layer converts the fuzzy feature maps back to crisp values using a small neural network.

Then global average pooling and global max pooling are concatenated — capturing both average and peak signals. Two dense layers with batch norm and dropout follow, and finally a softmax output layer.

The architecture automatically adapts to the SNP count — three blocks for small datasets, up to five blocks for genome-scale data. The same single function call handles everything.

---

---

## SLIDE 9 · Federated Learning
**⏱ Time: ~80 seconds | Words: ~170**

---

Now let's talk about how federated learning works in this system.

The central server holds the global Fuzzy CNN. At the start of each round, it broadcasts the current model weights to a randomly selected subset of clients — between 12 and 15 out of 50.

Each selected client then trains locally on its own data for two to three epochs. During this local training, we use FedProx loss — which I'll explain in the next slide — along with adaptive batch sizing based on how much data each client has, and gradient clipping to prevent exploding gradients.

After local training, each client sends its updated weights back to the server. The server then aggregates them using a weighted FedAvg — where clients with more data contribute proportionally more. We also apply quality weighting — if a client's local accuracy is more than one standard deviation below average, its contribution is halved.

The server then evaluates the new global model on the shared validation set. We use exponential moving average smoothing over the last ten rounds to get a stable accuracy signal for early stopping.

This entire loop repeats for 200 to 1,000 rounds depending on the configuration. [PAUSE] And throughout all of this, raw patient data never leaves any hospital.

---

---

## SLIDE 10 · FedProx
**⏱ Time: ~75 seconds | Words: ~160**

---

The biggest challenge in federated learning is client drift — and FedProx is how we solve it.

Here's the problem. Each hospital has different patients with different demographics and disease patterns. When clients train independently, their models drift in different directions. When you aggregate drifted models, the global model actually gets worse, not better.

FedProx fixes this by adding a proximal term to each client's loss function. The standard cross-entropy loss is augmented with mu over two times the squared L2 distance between the local weights and the global weights. This term penalizes the client for moving too far from the global model — it acts like a leash.

We use mu equals 0.01 by default, and 0.005 in high-accuracy mode. Lower mu gives clients more freedom to adapt locally. Higher mu keeps them tighter to the global solution.

We implement this as a custom TensorFlow GradientTape training loop — not standard Keras fit — because we need full control over the loss computation. Shape mismatches between local and global weights are handled gracefully — those layers simply skip the proximal term rather than crashing.

We also use a two-phase learning rate schedule. Linear warmup for the first 15 rounds prevents unstable gradients at the start. Then cosine annealing smoothly decays the learning rate to enable fine-tuning without overshooting.

---

---

## SLIDE 11 · Neural Architecture Search
**⏱ Time: ~75 seconds | Words: ~160**

---

Now let's talk about Neural Architecture Search — the component that makes the model self-optimizing.

The problem NAS solves is this: the optimal CNN architecture is different for snps50 versus snps5000, and different for pure epistasis versus additive models. Manually tuning this for 192 datasets would take weeks. PSO-NAS does it automatically.

Every candidate architecture is encoded as a 16-element vector. The first element is the number of blocks. Then for each of four possible blocks, we have three values — filters, kernel size, and pool type. Finally, dense layer sizes and dropout rate. This encoding covers the entire search space.

We optimize four objectives simultaneously. F1 is the misclassification rate — the primary accuracy objective. F2 is the number of blocks — simpler models generalize better. F3 is total parameters — fewer parameters means less communication overhead in federated learning. F4 is GFLOPs — faster models allow more training rounds.

The key innovation is the three-stage fitness function. In the first third of training, all four objectives are weighted equally — broad exploration. In the middle third, we focus on accuracy and FLOPs — speed matters. In the final third, we focus on accuracy and parameters — communication efficiency matters. [PAUSE] The fitness function literally changes as federated learning progresses.

---

---

## SLIDE 12 · PSO in Action
**⏱ Time: ~75 seconds | Words: ~160**

---

Let me explain how the Particle Swarm Optimization actually works.

We run 15 particles, each representing a different candidate CNN architecture as a 16-dimensional vector. Each particle has a position — its current architecture — and a velocity — the direction it's moving in architecture space.

Each particle remembers its personal best — the best architecture it has personally found — and the swarm tracks the global best — the best architecture any particle has found.

The velocity update equation pulls each particle toward both its personal best and the global best. The inertia weight omega decays from 0.9 to 0.4 over iterations — high inertia early means more exploration, low inertia late means more exploitation.

We have five smart features that prevent the search from failing. Boundary reflection means particles bounce off the limits of the search space rather than getting clipped — this preserves diversity. An architecture cache using MD5 hashing means we never evaluate the same architecture twice — saving significant computation. The Pareto front keeps all non-dominated solutions, not just the single best. Stagnation detection perturbs particles that haven't improved in five rounds. And diversity maintenance reinitializes the worst 20% of particles if the swarm converges too early.

When a better architecture is found, we transfer compatible weights from the old model and continue training — no restart needed.

---

---

## SLIDE 13 · Training System
**⏱ Time: ~65 seconds | Words: ~140**

---

Let me show you how easy it is to actually run this system.

We have four ready-to-use training presets. Default gives 200 rounds with patience of 25 — good for quick results. High-accuracy gives 500 rounds with patience of 80 and 15 clients per round — this is what you use for publication-quality results. Quick gives just 30 rounds — useful for debugging. And with-NAS enables the architecture search.

From the command line, you just run one command. For high accuracy, add the flag. To train a specific model, add the model name. For the paper configuration of 1,000 rounds with no early stopping, use the 222 variant.

You can also override any individual parameter — minimum rounds, maximum rounds, patience, clients per round, learning rate — all from the command line.

After each dataset completes, four files are saved automatically. A JSON result file with accuracy, F1, precision, and recall. The trained Keras model as an H5 file. A history JSON with per-round metrics including validation accuracy, learning rate, and client drift. And a four-panel training plot.

Progress is saved after every single dataset — so if the run is interrupted, you don't lose anything.

---

---

## SLIDE 14 · Results
**⏱ Time: ~80 seconds | Words: ~170**

---

Let's look at what the model actually achieves.

For the centralized Fuzzy CNN — where all client data is merged — we trained on order-2 datasets with 50 SNPs, 100 epochs maximum. Models three, four, seven, and eight all achieved Excellent accuracy — above 89%, with models seven and eight reaching 93%. These are the models with higher heritability of 0.15 and MAF of 0.4, which gives stronger signal. Models one, two, five, and six achieved Good accuracy in the 60 to 64% range. Average training time was just 1.2 minutes per dataset with early stopping kicking in between 30 and 55 epochs.

For federated training, the best result was 74.33% on model four, order three, snps100. The gap between centralized 93% and federated 74% is the cost of privacy — data fragmented across 50 clients means each client sees less. [PAUSE] That gap is expected and acceptable — we're trading accuracy for the ability to collaborate without sharing patient records.

On the NAS benchmark using CIFAR-10, FedED-SegNAS achieved 96.22% accuracy with only 2.1 million parameters. DARTS got 95.19% with 3.3 million parameters. MnasNet got 94.52% with 3.1 million. SGAS got 92.05% with 4.7 million. Our PSO-based approach beats all gradient-based methods in accuracy while using the fewest parameters.

---

---

## SLIDE 15 · Summary
**⏱ Time: ~65 seconds | Words: ~140**

---

Let me close with a summary of what was built and why it matters.

The complete system flows from raw genomic data through a validated data pipeline, through the Fuzzy CNN with six custom Keras layers, through federated training with FedProx and quality weighting, through PSO-NAS with three-stage multi-objective optimization, and finally to saved results including accuracy metrics, trained models, and training plots.

Six design decisions made this work. Swish instead of sigmoid eliminated vanishing gradients. FedProx instead of standard FedAvg reduced client drift. Softplus for fuzzy standard deviations guaranteed positive values. EMA smoothing prevented premature early stopping. Adaptive architecture means the same code handles 50 to 5,000 SNPs. And three-stage NAS fitness balanced accuracy against efficiency as training matured.

The numbers: 192 datasets, 50 clients, 259,000 parameters, 74% federated accuracy, 96% NAS accuracy, and 27 years to brute-force crack the privacy protection.

[PAUSE] FedED-SegNAS shows that hospitals can collaborate on genomic research at scale — without ever sharing a single patient record. Thank you.

---

---

## Word Count Summary

| Slide | Topic | Words | Time |
|-------|-------|-------|------|
| 1 | Title | 85 | ~40s |
| 2 | The Problem | 195 | ~90s |
| 3 | Our Solution | 160 | ~75s |
| 4 | Understanding Data | 150 | ~70s |
| 5 | The Dataset | 140 | ~65s |
| 6 | Data Pipeline | 160 | ~75s |
| 7 | Fuzzy CNN Idea | 170 | ~80s |
| 8 | Fuzzy CNN Architecture | 170 | ~80s |
| 9 | Federated Learning | 170 | ~80s |
| 10 | FedProx | 160 | ~75s |
| 11 | NAS | 160 | ~75s |
| 12 | PSO in Action | 160 | ~75s |
| 13 | Training System | 140 | ~65s |
| 14 | Results | 170 | ~80s |
| 15 | Summary | 140 | ~65s |
| **Total** | | **2,130** | **~17 min** |

---

## Speaking Tips

- **Slides 2 and 3** are the most important — spend full time here, don't rush
- **Slides 7 and 8** are technical — slow down slightly, let the audience absorb
- **Slide 14** — pause after each table row if audience seems engaged
- **[PAUSE]** markers = 1–2 second natural pause, not a full stop
- If running long, trim Slide 12 (PSO details) — it's the most skippable
- If running short, expand on Slide 14 results with more commentary
