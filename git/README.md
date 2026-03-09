# Perceptron — Handwritten Digit Classifier

**Deepak Nalla · Intro to AI**

A perceptron trained from scratch in Python to recognize the digit **8** in ASCII art images — with zero external ML libraries.

---

## Overview

| | |
|---|---|
| **Features** | 600 (30 columns × 20 rows per image) |
| **Training samples** | 86 positive (digit 8) · 129 negative (others) |
| **Epochs** | 15 |
| **Learning rate** | 0.10 |
| **Bias** | 0.10 |
| **Convergence** | 0 misclassifications by epoch 11 |

---

## How It Works

A perceptron is the simplest possible neural network — one neuron that computes a weighted sum of its inputs and fires if the result crosses a threshold.

```
output = +1  if  Σ(w · x) + bias > 0   →  "It is a 8"
output = −1  otherwise                  →  "It is NOT a 8"
```

**The learning rule** updates weights after every misclassification:

```
w  ←  w + η × x × error
```

where `η = 0.10` (learning rate), `x` is the pixel value (0 or 1), and `error = label − prediction`.

**Training loop (per epoch):**
1. Forward pass — compute weighted sum for each image
2. Compute error — `label − output` (0 if correct, ±2 if wrong)
3. Update weights — nudge each weight by `η × x × error`
4. Repeat for all 215 training images

---

## Architecture — Three-Script Pipeline

```
data/               →   generate_features.py   →   features.csv
(215 ASCII images)      (30×20 grid → 600-dim       (215 rows × 601 cols
                         binary vector)               + LABEL column)

features.csv        →   perceptron_train.py    →   weights.csv
                        (15 epochs, lr=0.10)        (601 learned weights)

weights.csv         →   evaluate.py            →   "It is a 8"
+ test image                                        or "It is NOT a 8"
```

**Feature extraction:** Each ASCII image is read as a 20×30 grid. A `#` character becomes `1`, everything else becomes `0`. The grid is flattened into a 600-element binary vector — one vector per image.

---

## File Structure

```
perceptron/
├── generate_features.py   # feature extraction from ASCII images
├── perceptron_train.py    # perceptron training loop
├── evaluate.py            # classify a new image
├── features.csv           # generated feature matrix
├── weights.csv            # learned weights (output of training)
├── requirements.txt
└── data/
    ├── train8/            # 86 positive training samples (digit 8)
    ├── trainOthers/       # 129 negative training samples
    └── test/              # evaluation images
```

---

## Training Results

Misclassifications per epoch on the full training set (215 images):

| Epoch | Misclassifications |
|------:|-------------------:|
| 0 | 89 |
| 1 | 44 |
| 2 | 29 |
| 3 | 25 |
| 4 | 17 |
| 5 | 15 |
| 6 | 18 |
| 7 | 11 |
| 8 | 7 |
| 9 | 6 |
| 10 | 2 |
| **11** | **0** ✓ |
| 12–14 | 0 |

---

## Run It Yourself

**Requirements:** Python 3.10+

```bash
# Install dependencies
pip install -r requirements.txt

# 1. Generate feature matrix from training images
python3 generate_features.py

# 2. Train the perceptron (saves weights.csv)
python3 perceptron_train.py

# 3. Classify a test image
cp data/test/8.txt data/test/img.txt
python3 evaluate.py
# → It is a 8
```

---

## Parameters

| Parameter | Value | Notes |
|---|---|---|
| `num_features` | 600 | 30 cols × 20 rows |
| `LEARNING_RATE` | 0.10 | step size per weight update |
| `MAX_ITERATIONS` | 15 | epochs |
| `BIAS` | 0.10 | constant offset to weighted sum |
