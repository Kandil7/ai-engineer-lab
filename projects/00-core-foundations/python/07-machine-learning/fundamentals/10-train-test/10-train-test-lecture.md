# Lecture 10: Train/Test Split

## Topic Overview

Splitting data into training and test sets is one of the most fundamental practices in machine learning. It prevents overfitting by ensuring we evaluate models on data they haven't seen during training. This lecture covers why splitting is necessary, how to use `train_test_split`, the effects of different test sizes, reproducibility with random_state, stratified splits, and cross-validation.

---

## Learning Objectives

By the end of this lecture, you will be able to:

1. Explain why train/test splitting is essential
2. Use `train_test_split` with proper parameters
3. Choose appropriate test sizes
4. Use `random_state` for reproducibility
5. Apply stratified splits for classification
6. Understand data leakage and how to prevent it
7. Use cross-validation for more reliable evaluation
8. Avoid common train/test split mistakes

---

## Key Concepts

### 1. Why Split Data?

If we train and test on the same data, we get misleadingly high accuracy. The model may memorize the training data instead of learning generalizable patterns.

```
Without split:
Train data → Model → Test on same data → High accuracy (misleading!)

With split:
Train data → Model → Test on different data → Honest accuracy
```

### 2. Data Leakage

Data leakage occurs when information from the test set leaks into the training process. Common causes:
- Scaling before splitting
- Feature selection before splitting
- Looking at test data during training

### 3. Split Ratios

| Dataset Size | Train % | Test % | Typical Split |
|-------------|---------|--------|---------------|
| < 1,000 | 80% | 20% | Standard |
| 1,000 - 10,000 | 70% | 30% | Common |
| > 10,000 | 90% | 10% | Can use smaller test |

### 4. Stratified Split

For classification with imbalanced classes, `stratify=y` ensures both sets have the same class proportions.

### 5. Cross-Validation

A single train/test split can be unstable. Cross-validation splits the data multiple times and averages the results.

---

## Code Examples

### Example 1: The Overfitting Problem

```python
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score

np.random.seed(42)
X = np.random.rand(50, 1) * 10
y = 2 * X.squeeze() + 3 + np.random.randn(50) * 0.5

# Train and test on SAME data
model = LinearRegression()
model.fit(X, y)
r2_all = r2_score(y, model.predict(X))

print(f"R² on same data: {r2_all:.4f}")
print("(This is misleadingly high!)")
```

### Example 2: Basic Train/Test Split

```python
from sklearn.model_selection import train_test_split

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

print(f"Original size: {len(X)}")
print(f"Training set: {len(X_train)}")
print(f"Test set: {len(X_test)}")
```

### Example 3: Proper Evaluation

```python
model = LinearRegression()
model.fit(X_train, y_train)

r2_train = r2_score(y_train, model.predict(X_train))
r2_test = r2_score(y_test, model.predict(X_test))

print(f"Training R²: {r2_train:.4f}")
print(f"Test R²: {r2_test:.4f}")
print("(Test R² is more realistic)")
```

### Example 4: Test Size Effects

```python
test_sizes = [0.1, 0.2, 0.3, 0.4]

for test_size in test_sizes:
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=test_size, random_state=42)

    model = LinearRegression()
    model.fit(X_train, y_train)
    r2 = r2_score(y_test, model.predict(X_test))

    print(f"Test size {test_size:.0%}: Train={len(X_train)}, Test={len(X_test)}, R²={r2:.4f}")
```

### Example 5: Reproducibility with random_state

```python
print("Without random_state (different each time):")
for i in range(3):
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)
    print(f"  Split {i + 1}: Test indices = {X_test[:3].flatten()}")

print("\nWith random_state=42 (same every time):")
for i in range(3):
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    print(f"  Split {i + 1}: Test indices = {X_test[:3].flatten()}")
```

### Example 6: Stratified Split

```python
from sklearn.datasets import make_classification

X_clf, y_clf = make_classification(
    n_samples=200, n_features=10, n_informative=5, n_redundant=2, random_state=42
)

print(f"Original class distribution: {np.bincount(y_clf)}")

# Without stratify
X_train, X_test, y_train, y_test = train_test_split(X_clf, y_clf, test_size=0.2, random_state=42)
print(f"Without stratify: Train {np.bincount(y_train)}, Test {np.bincount(y_test)}")

# With stratify
X_train, X_test, y_train, y_test = train_test_split(
    X_clf, y_clf, test_size=0.2, stratify=y_clf, random_state=42
)
print(f"With stratify: Train {np.bincount(y_train)}, Test {np.bincount(y_test)}")
```

### Example 7: Cross-Validation

```python
from sklearn.model_selection import cross_val_score

model = LinearRegression()
scores = cross_val_score(model, X, y, cv=5, scoring="r2")

print(f"5-fold CV R² scores: {scores}")
print(f"Mean R²: {scores.mean():.4f} ± {scores.std():.4f}")
```

---

## Common Mistakes to Avoid

1. **Scaling before split** — Causes data leakage
2. **Too small test set** — Unreliable estimates
3. **Not using random_state** — Non-reproducible results
4. **Not stratifying** — Class imbalance in splits
5. **Tuning on test set** — Use validation set instead
6. **Looking at test data** — Should be completely unseen

---

## Best Practices

1. **Use 20-30% for test** — Enough for reliable evaluation
2. **Always set random_state** — For reproducibility
3. **Use stratify for classification** — Especially with imbalanced classes
4. **Never preprocess before split** — Use pipelines instead
5. **Use cross-validation** — For model selection
6. **Keep test set locked away** — Only touch at the very end

---

## Summary


| Parameter | Description | Recommended |
|-----------|-------------|-------------|
| `test_size` | Proportion for testing | 0.2-0.3 |
| `random_state` | Seed for reproducibility | Any integer |
| `stratify` | Maintain class proportions | y (for classification) |
| `cv` (cross_val) | Number of folds | 5-10 |

**Key Takeaway:** Always split your data before training. Use `train_test_split` with `random_state` for reproducibility and `stratify` for classification. Never touch the test set until your model is final.

---

## Next Lecture

In [Lecture 11: Decision Trees](11-decision-tree-lecture.md), we'll explore a different type of model that can handle non-linear relationships and is easy to interpret.
