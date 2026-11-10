# Glossary: Train/Test Split

## Quick Reference Table

| Term | Definition | Category |
|------|-----------|----------|
| Train/Test Split | Dividing data into training and test sets | Process |
| Training Set | Data used to train the model | Data Split |
| Test Set | Data used to evaluate the model | Data Split |
| Validation Set | Data used for hyperparameter tuning | Data Split |
| train_test_split | Scikit-learn splitting function | Tool |
| test_size | Proportion of data for testing | Parameter |
| train_size | Proportion of data for training | Parameter |
| random_state | Seed for reproducibility | Parameter |
| stratify | Maintain class proportions | Parameter |
| Data Leakage | Test info leaking into training | Problem |
| Cross-Validation | Multiple train/test splits | Technique |
| K-Fold | Splitting data into k parts | Technique |
| Overfitting | Model learns noise, not pattern | Problem |
| Generalization | Performance on unseen data | Concept |
| Holdout Set | Data kept aside for final evaluation | Concept |
| Baseline | Simple model for comparison | Concept |
| Stratified Split | Maintains class distribution | Technique |
| Shuffle | Randomize data before splitting | Parameter |
| Shuffle | Randomize data before splitting | Parameter |
| Reproducibility | Getting same results each time | Goal |
| Evaluation | Measuring model performance | Process |

---

## Detailed Definitions

### B

#### Baseline Model
**Definition:** A simple reference model used for comparison. The simplest baseline predicts the mean (regression) or the majority class (classification).

**Example:**
```python
import numpy as np
from sklearn.metrics import r2_score, accuracy_score

# Regression baseline: predict mean
y = np.array([1, 2, 3, 4, 5])
y_baseline = np.full_like(y, y.mean())
r2_baseline = r2_score(y, y_baseline)
print(f"Baseline R²: {r2_baseline:.4f}")  # 0.0

# Classification baseline: predict majority class
y_clf = np.array([0, 0, 0, 0, 1])
y_baseline_clf = np.full_like(y_clf, 0)
acc_baseline = accuracy_score(y_clf, y_baseline_clf)
print(f"Baseline accuracy: {acc_baseline:.4f}")  # 0.8
```

**Related Terms:** Null Model, Intercept-only Model, R-squared

---

### C

#### Cross-Validation
**Definition:** A technique that splits the data into multiple folds, training on some folds and testing on others, rotating through all combinations. Provides a more reliable performance estimate than a single split.

**Example:**
```python
from sklearn.model_selection import cross_val_score
from sklearn.linear_model import LinearRegression

model = LinearRegression()
scores = cross_val_score(model, X, y, cv=5, scoring="r2")

print(f"Fold scores: {scores}")
print(f"Mean: {scores.mean():.4f} ± {scores.std():.4f}")
```

**Types:**
- K-Fold: Standard k folds
- Stratified K-Fold: Maintains class proportions
- Leave-One-Out: Each sample is a test set
- Time Series Split: Respects temporal order

**Related Terms:** K-Fold, Validation Set, Generalization

---

### D

#### Data Leakage
**Definition:** When information from outside the training dataset is used to create the model, leading to overly optimistic performance estimates.

**Example:**
```python
# WRONG: Leakage
from sklearn.preprocessing import StandardScaler

scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)  # Uses ALL data
X_train, X_test = train_test_split(X_scaled, test_size=0.2)

# CORRECT: No leakage
X_train, X_test = train_test_split(X, test_size=0.2)
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)
```

**Common causes:**
- Scaling before splitting
- Feature selection before splitting
- Using future data in time series
- Target leakage (features derived from target)

**Related Terms:** Train/Test Split, Preprocessing, Data Quality

---

### G

#### Generalization
**Definition:** A model's ability to perform well on new, unseen data. The ultimate goal of machine learning — not just memorizing training data, but learning patterns that apply broadly.

**Example:**
```python
model = LinearRegression()
model.fit(X_train, y_train)

train_r2 = model.score(X_train, y_train)
test_r2 = model.score(X_test, y_test)

print(f"Training R²: {train_r2:.4f}")
print(f"Test R²: {test_r2:.4f}")

if train_r2 - test_r2 > 0.1:
    print("Poor generalization — possible overfitting!")
```

**Related Terms:** Overfitting, Underfitting, Train/Test Split

---

### H

#### Holdout Set
**Definition:** A portion of data kept aside and not used during model development. Used only for the final evaluation of the model.

**Example:**
```python
# Split into train+val and holdout
X_temp, X_holdout, y_temp, y_holdout = train_test_split(X, y, test_size=0.1, random_state=42)

# Split temp into train and validation
X_train, X_val, y_train, y_val = train_test_split(X_temp, y_temp, test_size=0.2, random_state=42)

print(f"Train: {len(X_train)}")
print(f"Validation: {len(X_val)}")
print(f"Holdout: {len(X_holdout)}")
```

**Related Terms:** Validation Set, Test Set, Train/Test Split

---

### K

#### K-Fold Cross-Validation
**Definition:** A cross-validation technique that splits the data into k equal folds, using each fold as the test set once while training on the remaining k-1 folds.

**Example:**
```python
from sklearn.model_selection import KFold, cross_val_score
from sklearn.linear_model import LinearRegression

model = LinearRegression()
kf = KFold(n_splits=5, shuffle=True, random_state=42)

scores = cross_val_score(model, X, y, cv=kf, scoring="r2")
print(f"5-Fold CV scores: {scores}")
print(f"Mean R²: {scores.mean():.4f} ± {scores.std():.4f}")
```

**Related Terms:** Cross-Validation, Folds, Validation

---

### O

#### Overfitting
**Definition:** When a model learns the training data too well, including noise and outliers, resulting in poor performance on unseen data.

**Example:**
```python
from sklearn.tree import DecisionTreeClassifier

# Overfitting: no depth limit
overfit = DecisionTreeClassifier(max_depth=None)
overfit.fit(X_train, y_train)

train_acc = overfit.score(X_train, y_train)
test_acc = overfit.score(X_test, y_test)

print(f"Train accuracy: {train_acc:.4f}")  # 100%
print(f"Test accuracy: {test_acc:.4f}")  # Lower
print(f"Gap: {train_acc - test_acc:.4f}")  # Large gap = overfitting
```

**Signs:**
- Large gap between train and test performance
- Model is very complex
- Training accuracy is perfect

**Related Terms:** Underfitting, Generalization, Regularization

---

### S

#### Stratified Split
**Definition:** A train/test split that maintains the same class proportions in both training and test sets. Essential for imbalanced classification problems.

**Example:**
```python
from sklearn.model_selection import train_test_split
import numpy as np

# Imbalanced classes
y = np.array([0, 0, 0, 0, 0, 0, 0, 1, 1, 1])  # 70% class 0, 30% class 1

# Without stratify
_, y_test_no = train_test_split(y, test_size=0.3, random_state=42)
print(f"Without stratify: {np.bincount(y_test_no)}")

# With stratify
_, y_test_strat = train_test_split(y, test_size=0.3, stratify=y, random_state=42)
print(f"With stratify: {np.bincount(y_test_strat)}")
# Maintains 70/30 split in both
```

**Related Terms:** Class Imbalance, Train/Test Split, Classification

---

### T

#### Test Set
**Definition:** A subset of data reserved for evaluating the final model. Never used during training or model selection. Provides an unbiased estimate of real-world performance.

**Example:**
```python
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train on training set
model = LinearRegression()
model.fit(X_train, y_train)

# Evaluate ONLY on test set (once, at the end)
final_r2 = model.score(X_test, y_test)
print(f"Final test R²: {final_r2:.4f}")
```

**Related Terms:** Training Set, Validation Set, Holdout Set

#### Training Set
**Definition:** The subset of data used to train the machine learning model. The model learns patterns from this data.

**Example:**
```python
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

model = LinearRegression()
model.fit(X_train, y_train)  # Train on training set only
```

**Related Terms:** Test Set, Validation Set, Model Training

#### Train/Test Split
**Definition:** The process of dividing a dataset into training and test sets to evaluate model performance on unseen data.

**Example:**
```python
from sklearn.model_selection import train_test_split

# Basic split
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,  # 20% for testing
    random_state=42,  # Reproducible
    stratify=y,  # Maintain class proportions (classification)
)

print(f"Training: {X_train.shape}, {y_train.shape}")
print(f"Test: {X_test.shape}, {y_test.shape}")
```

**Related Terms:** test_size, random_state, stratify, Data Leakage

---

### U

#### Underfitting
**Definition:** When a model is too simple to capture the underlying patterns in the data, resulting in poor performance on both training and test data.

**Example:**
```python
# Linear model on non-linear data
from sklearn.linear_model import LinearRegression

model = LinearRegression()
model.fit(X_train, y_train)

train_r2 = model.score(X_train, y_train)
test_r2 = model.score(X_test, y_test)

print(f"Train R²: {train_r2:.4f}")  # Low
print(f"Test R²: {test_r2:.4f}")  # Also low
```

**Signs:**
- Low performance on both train and test
- Model can't capture obvious patterns
- High bias

**Related Terms:** Overfitting, Bias, Model Complexity

---

## Key Parameters


| Parameter | Description | Default | Recommended |
|-----------|-------------|---------|-------------|
| `test_size` | Proportion for test set | 0.25 | 0.2-0.3 |
| `train_size` | Proportion for train set | None (1-test_size) | 0.7-0.8 |
| `random_state` | Seed for reproducibility | None | Any integer |
| `stratify` | Class proportions | None | y (for classification) |
| `shuffle` | Shuffle before splitting | True | True (usually) |
| `cv` (cross_val) | Number of folds | 5 | 5-10 |

---

## Python Import Cheat Sheet

```python
# Train/test split
from sklearn.model_selection import train_test_split

# Cross-validation
from sklearn.model_selection import cross_val_score, KFold, StratifiedKFold

# Basic workflow
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

# Cross-validation workflow
from sklearn.linear_model import LinearRegression

model = LinearRegression()
scores = cross_val_score(model, X, y, cv=5, scoring="r2")
print(f"Mean R²: {scores.mean():.4f} ± {scores.std():.4f}")
```
