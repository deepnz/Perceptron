# Modernize Perceptron Classifier — Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Modernize a Python 2 perceptron digit classifier to Python 3, fix deprecated pandas APIs, add type hints, use f-strings, and add a `requirements.txt`.

**Architecture:** Three standalone scripts (`generate_features.py`, `perceptron_train.py`, `evaluate.py`) that run in sequence. No structural changes — same filenames, same data folder layout. Only syntax, API calls, and style are updated.

**Tech Stack:** Python 3.10+, pandas 2.x, numpy 1.x

---

### Task 1: Add `requirements.txt`

**Files:**
- Create: `git/perceptron/requirements.txt`

**Step 1: Create the file**

```
numpy>=1.24
pandas>=2.0
```

**Step 2: Verify pip can read it**

```bash
pip install -r git/perceptron/requirements.txt --dry-run
```
Expected: lists numpy and pandas without errors.

**Step 3: Commit**

```bash
git add git/perceptron/requirements.txt
git commit -m "chore: add requirements.txt with numpy and pandas"
```

---

### Task 2: Fix `generate_features.py`

**Files:**
- Modify: `git/perceptron/generate_features.py`

**Issues to fix:**
- `DataFrame.append()` removed in pandas 2.0 → replace with `pd.concat()`
- No f-strings (minor style)

**Step 1: Replace the file contents**

```python
# -*- coding: utf-8 -*-

import numpy as np
import pandas as pd

NUM_POS = 87
NUM_NEG = 130
pos_labels = [1] * NUM_POS
neg_labels = [-1] * NUM_NEG
pos_labels.extend(neg_labels)

def load_image(path: str) -> np.ndarray:
    temp = [[0 for _ in range(30)] for _ in range(20)]
    with open(path) as infile:
        rf = infile.readlines()
    for i in range(min(len(rf), 20)):
        for j in range(min(len(rf[i]), 30)):
            if rf[i][j] == '#':
                temp[i][j] = 1
    return np.array(temp).reshape(600)

pos_features = [load_image(f"data/train8/{k}.txt") for k in range(1, NUM_POS + 1)]
neg_features = [load_image(f"data/trainOthers/{k}.txt") for k in range(1, NUM_NEG + 1)]

features = pd.concat([
    pd.DataFrame(pos_features),
    pd.DataFrame(neg_features),
], ignore_index=True)

features["LABEL"] = pos_labels
features = features.iloc[np.random.permutation(len(features))]
features.to_csv("features.csv", index=False)
print("features.csv written.")
```

**Step 2: Run the script from the perceptron directory**

```bash
cd git/perceptron && python3 generate_features.py
```
Expected: prints `features.csv written.` and creates/updates `features.csv`.

**Step 3: Commit**

```bash
git add git/perceptron/generate_features.py
git commit -m "fix: port generate_features.py to Python 3, replace deprecated DataFrame.append"
```

---

### Task 3: Fix `perceptron_train.py`

**Files:**
- Modify: `git/perceptron/perceptron_train.py`

**Issues to fix:**
- `print "string"` (Python 2 syntax) → `print()` calls
- No f-strings

**Step 1: Replace the file contents**

```python
# -*- coding: utf-8 -*-

import pandas as pd

num_features = 600
WEIGHTS: list[float] = [0.0] * 602
LEARNING_RATE = 0.10
MAX_ITERATIONS = 15
BIAS = 0.10


def find_sum(x_vec, weights: list[float]) -> float:
    ans = weights[0]
    for i in range(len(x_vec)):
        ans += x_vec[i] * weights[i + 1]
    return ans


def update_weight(x_vec, weights: list[float], error: float, learning_rate: float) -> list[float]:
    for i in range(len(weights) - 1):
        weights[i + 1] = weights[i + 1] + learning_rate * x_vec[i] * error
    return weights


WEIGHTS[0] = BIAS
training_features = pd.read_csv("features.csv")
labels = training_features.LABEL.tolist()
del training_features["LABEL"]

epoch = 0
while epoch < MAX_ITERATIONS:
    print(f"epoch: {epoch}")
    num_mis = 0
    for i in range(len(training_features)):
        x_vec = training_features.iloc[i]
        label = labels[i]
        output = 1 if find_sum(x_vec, WEIGHTS) > 0 else -1
        error = label - output
        if error != 0:
            num_mis += 1
        WEIGHTS = update_weight(x_vec, WEIGHTS, error, LEARNING_RATE)
    print(f"misclassifications: {num_mis}")
    epoch += 1

pd.DataFrame(WEIGHTS).to_csv("weights.csv", index=False)
print("weights.csv written.")
```

**Step 2: Run the script from the perceptron directory**

```bash
cd git/perceptron && python3 perceptron_train.py
```
Expected: prints epoch lines and `weights.csv written.`, misclassifications trending toward 0.

**Step 3: Commit**

```bash
git add git/perceptron/perceptron_train.py
git commit -m "fix: port perceptron_train.py to Python 3 with type hints and f-strings"
```

---

### Task 4: Fix `evaluate.py`

**Files:**
- Modify: `git/perceptron/evaluate.py`

**Issues to fix:**
- Minor: use f-strings, add type hint to `find_sum`

**Step 1: Replace the file contents**

```python
# -*- coding: utf-8 -*-

import pandas as pd
import numpy as np


def find_sum(x_vec: np.ndarray, weights: list[float]) -> float:
    ans = weights[0]
    for i in range(len(x_vec)):
        ans += x_vec[i] * weights[i + 1]
    return ans


weights_df = pd.read_csv("weights.csv", names=["weights"])
w = weights_df.weights.tolist()[1:]

y_vec = [[0 for _ in range(30)] for _ in range(20)]
with open("data/test/img.txt") as infile:
    rf = infile.readlines()
for i in range(min(len(rf), 20)):
    for j in range(min(len(rf[i]), 30)):
        if rf[i][j] == '#':
            y_vec[i][j] = 1

y_vec = np.array(y_vec).reshape(600)
output = 1 if find_sum(y_vec, w) > 0 else -1

print("It is a 8") if output == 1 else print("It is NOT a 8")
```

**Step 2: Run the script from the perceptron directory**

```bash
cd git/perceptron && python3 evaluate.py
```
Expected: prints `It is a 8` or `It is NOT a 8`.

**Step 3: Commit**

```bash
git add git/perceptron/evaluate.py
git commit -m "fix: port evaluate.py to Python 3 with type hints and f-strings"
```

---

### Task 5: Update README

**Files:**
- Modify: `git/README.md`

**Step 1: Fix the typo (`perceptron_trains.py` → `perceptron_train.py`) and note Python 3**

Update the header paragraph to say:

```
Requires Python 3.10+ with numpy and pandas. Install dependencies with:

    pip install -r requirements.txt

Then run in order:

    python3 generate_features.py
    python3 perceptron_train.py
    python3 evaluate.py
```

**Step 2: Commit**

```bash
git add git/README.md
git commit -m "docs: update README for Python 3 and fix script name typo"
```
