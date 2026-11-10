# Glossary: Cross-Validation (Lecture 22)

## Quick Reference Table

| Term | Definition | Example |
|------|-----------|---------|
| Cross-Validation | Evaluate model using multiple splits | `cross_val_score()` |
| K-Fold | Split data into K equal folds | `KFold(n_splits=5)` |
| Stratified K-Fold | Preserves class distribution | `StratifiedKFold()` |
| Holdout | Single train/test split | `train_test_split()` |
| cross_val_score | Easy CV implementation | `cross_val_score(model, X, y)` |
| Scoring Metric | Performance measure | 'accuracy', 'f1' |
| Data Leakage | Using test info in training | Fitting scaler on all data |
| Pipeline | Chain preprocessing + model | `Pipeline([...])` |
| Validation Set | Holdout for final evaluation | Separate from CV |
| Leave-One-Out | K = number of samples | `LeaveOneOut()` |
| Shuffle | Randomize fold assignments | `shuffle=True` |
| Random State | Seed for reproducibility | `random_state=42` |
| Mean Score | Average across folds | `scores.mean()` |
| Std Score | Variability across folds | `scores.std()` |

---

## Detailed Term Definitions

### Cross-Validation

**Definition:** A technique for assessing how well a model generalizes to an independent dataset by splitting data into multiple training/validation sets.

**Example:**
```python
from sklearn.model_selection import cross_val_score
from sklearn.linear_model import LogisticRegression
from sklearn.datasets import make_classification

X, y = make_classification(n_samples=200, n_features=10, random_state=42)

model = LogisticRegression(random_state=42)
scores = cross_val_score(model, X, y, cv=5, scoring="accuracy")

print(f"CV scores: {scores}")
print(f"Mean accuracy: {scores.mean():.4f}")
print(f"Std accuracy: {scores.std():.4f}")
```

**Related Terms:** K-Fold, Holdout, Model Evaluation

---

### K-Fold Cross-Validation

**Definition:** Splits data into K equal folds, trains on K-1 folds, and tests on the remaining fold. Repeats K times.

**Example:**
```python
from sklearn.model_selection import KFold
from sklearn.linear_model import LogisticRegression
from sklearn.datasets import make_classification
from sklearn.metrics import accuracy_score
import numpy as np

X, y = make_classification(n_samples=200, n_features=10, random_state=42)

kf = KFold(n_splits=5, shuffle=True, random_state=42)

scores = []
for train_idx, val_idx in kf.split(X):
    X_train, X_val = X[train_idx], X[val_idx]
    y_train, y_val = y[train_idx], y[val_idx]
    
    model = LogisticRegression(random_state=42)
    model.fit(X_train, y_train)
    score = accuracy_score(y_val, model.predict(X_val))
    scores.append(score)

print(f"Fold scores: {[f'{s:.4f}' for s in scores]}")
print(f"Mean: {np.mean(scores):.4f} +/- {np.std(scores):.4f}")
```

**Parameters:**
- `n_splits`: Number of folds (default 5)
- `shuffle`: Randomize before splitting
- `random_state`: Seed for reproducibility

**Related Terms:** Stratified K-Fold, Holdout, Leave-One-Out

---

### Stratified K-Fold

**Definition:** K-Fold that preserves the percentage of samples for each class in each fold. Essential for imbalanced datasets.

**Example:**
```python
from sklearn.model_selection import StratifiedKFold
from sklearn.linear_model import LogisticRegression
from sklearn.datasets import make_classification
import numpy as np

X, y = make_classification(n_samples=200, n_features=10, weights=[0.7, 0.3], random_state=42)

print(f"Original class distribution: {np.bincount(y)}")

skf = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)

for fold, (train_idx, val_idx) in enumerate(skf.split(X, y)):
    print(f"Fold {fold + 1}: Train {np.bincount(y[train_idx])}, Val {np.bincount(y[val_idx])}")
```

**Why stratified?**
- Ensures each fold has representative class distribution
- Prevents folds with only one class
- More reliable estimates for imbalanced data

**Related Terms:** K-Fold, Class Imbalance, Stratification

---

### Holdout Method

**Definition:** Splitting data into a single training set and test set. Simple but less reliable than cross-validation.

**Example:**
```python
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.datasets import make_classification
from sklearn.metrics import accuracy_score
import numpy as np

X, y = make_classification(n_samples=200, n_features=10, random_state=42)

# Different splits give different results
print("Multiple holdout splits:")
for i in range(5):
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)
    model = LogisticRegression(random_state=42)
    model.fit(X_train, y_train)
    acc = accuracy_score(y_test, model.predict(X_test))
    print(f"  Split {i + 1}: {acc:.4f}")
```

**Pros/Cons:**
- ✓ Simple, fast
- ✗ Less reliable, wastes data

**Related Terms:** Cross-Validation, Train/Test Split

---

### cross_val_score

**Definition:** A convenient function that performs cross-validation and returns scores for each fold.

**Example:**
```python
from sklearn.model_selection import cross_val_score
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC
from sklearn.ensemble import RandomForestClassifier
from sklearn.datasets import make_classification

X, y = make_classification(n_samples=200, n_features=10, random_state=42)

# Compare models
models = {
    "Logistic Regression": LogisticRegression(random_state=42),
    "SVM": SVC(random_state=42),
    "Random Forest": RandomForestClassifier(n_estimators=100, random_state=42),
}

for name, model in models.items():
    scores = cross_val_score(model, X, y, cv=5, scoring="accuracy")
    print(f"{name:25s}: {scores.mean():.4f} +/- {scores.std():.4f}")
```

**Parameters:**
- `estimator`: Model to evaluate
- `X, y`: Data
- `cv`: Number of folds or CV object
- `scoring`: Metric to use

**Related Terms:** K-Fold, Scoring Metric

---

### Scoring Metric

**Definition:** The performance measure used to evaluate model predictions during cross-validation.

**Common Metrics:**

| Metric | Use Case | Higher is Better |
|--------|----------|------------------|
| accuracy | Balanced classification | ✓ |
| f1 | Imbalanced classification | ✓ |
| precision | Minimize false positives | ✓ |
| recall | Minimize false negatives | ✓ |
| roc_auc | Probability-based | ✓ |
| r2 | Regression | ✓ |
| neg_mse | Regression (negative) | ✓ |

**Example:**
```python
from sklearn.model_selection import cross_val_score
from sklearn.linear_model import LogisticRegression
from sklearn.datasets import make_classification

X, y = make_classification(n_samples=200, n_features=10, random_state=42)

model = LogisticRegression(random_state=42)

# Try different metrics
for metric in ["accuracy", "f1", "precision", "recall", "roc_auc"]:
    scores = cross_val_score(model, X, y, cv=5, scoring=metric)
    print(f"{metric:12s}: {scores.mean():.4f}")
```

**Related Terms:** Accuracy, F1 Score, Precision, Recall

---

### Data Leakage

**Definition:** When information from the test set leaks into the training process, leading to overly optimistic performance estimates.

**Example:**
```python
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import cross_val_score, KFold
from sklearn.pipeline import Pipeline
from sklearn.datasets import make_classification
import numpy as np

X, y = make_classification(n_samples=200, n_features=10, random_state=42)

# WRONG: Scaler fitted on all data (leakage!)
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)  # Uses test data info!

model = LogisticRegression(random_state=42)
# This gives inflated scores

# CORRECT: Use pipeline
pipeline = Pipeline([("scaler", StandardScaler()), ("model", LogisticRegression(random_state=42))])

scores = cross_val_score(pipeline, X, y, cv=5, scoring="accuracy")
print(f"Correct CV accuracy: {scores.mean():.4f}")
```

**Common Causes:**
- Fitting scaler on all data
- Feature selection using test data
- Hyperparameter tuning on test set

**Related Terms:** Pipeline, Preprocessing, Train/Test Contamination

---

### Pipeline

**Definition:** A sequence of processing steps chained together, ensuring consistent preprocessing and preventing data leakage.

**Example:**
```python
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import cross_val_score
from sklearn.datasets import make_classification

X, y = make_classification(n_samples=200, n_features=10, random_state=42)

pipeline = Pipeline(
    [
        ("scaler", StandardScaler()),
        ("pca", PCA(n_components=5)),
        ("model", LogisticRegression(random_state=42)),
    ]
)

scores = cross_val_score(pipeline, X, y, cv=5, scoring="accuracy")
print(f"Pipeline CV accuracy: {scores.mean():.4f}")
```

**Benefits:**
- Prevents data leakage
- Clean, reproducible code
- Easy to save/load

**Related Terms:** Data Leakage, Preprocessing, Transformer

---

### Leave-One-Out (LOO)

**Definition:** Special case of K-Fold where K equals the number of samples. Each iteration uses one sample for validation.

**Example:**
```python
from sklearn.model_selection import LeaveOneOut, cross_val_score
from sklearn.linear_model import LogisticRegression
from sklearn.datasets import make_classification
import time

X, y = make_classification(n_samples=100, n_features=10, random_state=42)

model = LogisticRegression(random_state=42)

start = time.time()
loo = LeaveOneOut()
scores = cross_val_score(model, X, y, cv=loo, scoring="accuracy")
time_taken = time.time() - start

print(f"LOO CV accuracy: {scores.mean():.4f}")
print(f"Time: {time_taken:.2f}s")
print(f"Number of fits: {len(X)}")
# Very expensive for large datasets!
```

**Properties:**
- No randomness in splits
- Maximum training data per iteration
- Very expensive for large datasets
- Almost unbiased estimate

**Related Terms:** K-Fold, Computational Cost

---

### Shuffle

**Definition:** Randomly reorders data before splitting into folds. Important for ordered datasets.

**Example:**
```python
from sklearn.model_selection import KFold
from sklearn.datasets import make_classification
import numpy as np

X, y = make_classification(n_samples=200, n_features=10, random_state=42)

# Without shuffle (bad for ordered data)
kf_no_shuffle = KFold(n_splits=5, shuffle=False, random_state=42)
for train_idx, val_idx in kf_no_shuffle.split(X):
    print(f"Val indices: {val_idx[:5]}...")  # Sequential

print()

# With shuffle (recommended)
kf_shuffle = KFold(n_splits=5, shuffle=True, random_state=42)
for train_idx, val_idx in kf_shuffle.split(X):
    print(f"Val indices: {val_idx[:5]}...")  # Random
```

**When to shuffle:**
- Ordered datasets (time series need special handling)
- Always recommended for K-Fold

**Related Terms:** K-Fold, Random State, Data Ordering

---

### Random State

**Definition:** Seed for random number generator, ensuring reproducibility of cross-validation splits.

**Example:**
```python
from sklearn.model_selection import cross_val_score, KFold
from sklearn.linear_model import LogisticRegression
from sklearn.datasets import make_classification

X, y = make_classification(n_samples=200, n_features=10, random_state=42)

# Same random_state = same splits
kf1 = KFold(n_splits=5, shuffle=True, random_state=42)
kf2 = KFold(n_splits=5, shuffle=True, random_state=42)

model = LogisticRegression(random_state=42)

scores1 = cross_val_score(model, X, y, cv=kf1, scoring="accuracy")
scores2 = cross_val_score(model, X, y, cv=kf2, scoring="accuracy")

print(f"Scores 1: {scores1}")
print(f"Scores 2: {scores2}")
print(f"Same results: {np.allclose(scores1, scores2)}")
```

**Related Terms:** Reproducibility, Shuffle, Split

---

## Formulas Summary

| Formula | Description |
|---------|-------------|
| K-Fold MSE | (1/K) Σ MSEₖ |
| Bias (K-Fold) | Approximately unbiased when K is large |
| Variance (K-Fold) | Increases with K |
| LOO Bias | Approximately zero |
| LOO Variance | Can be high |

---

## Code Snippets Quick Reference

```python
# Basic Cross-Validation
from sklearn.model_selection import cross_val_score

scores = cross_val_score(model, X, y, cv=5, scoring="accuracy")

# K-Fold
from sklearn.model_selection import KFold

kf = KFold(n_splits=5, shuffle=True, random_state=42)
for train_idx, val_idx in kf.split(X):
    X_train, X_val = X[train_idx], X[val_idx]

# Stratified K-Fold
from sklearn.model_selection import StratifiedKFold

skf = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)
scores = cross_val_score(model, X, y, cv=skf, scoring="accuracy")

# Leave-One-Out
from sklearn.model_selection import LeaveOneOut

loo = LeaveOneOut()
scores = cross_val_score(model, X, y, cv=loo)

# GridSearchCV with CV
from sklearn.model_selection import GridSearchCV

grid = GridSearchCV(model, param_grid, cv=5, scoring="accuracy")
grid.fit(X, y)

# Pipeline (prevents leakage)
from sklearn.pipeline import Pipeline

pipe = Pipeline([("scaler", StandardScaler()), ("model", model)])
scores = cross_val_score(pipe, X, y, cv=5)
```

---

## Common Pitfalls

1. **Data leakage** — Use pipelines for preprocessing
2. **Wrong CV for imbalance** — Use StratifiedKFold
3. **Too few folds** — High variance estimates
4. **Too many folds** — Computationally expensive
5. **Using CV for final eval** — Use test set once

---

## Further Reading

- [Scikit-learn - Cross Validation](https://scikit-learn.org/stable/modules/cross_validation.html)
- [Wikipedia - Cross-validation](https://en.wikipedia.org/wiki/Cross-validation_(statistics))
- [Machine Learning Mastery - Cross Validation](https://machinelearningmastery.com/k-fold-cross-validation/)
