# Lecture 20: Random Forest

## Topic Overview

Random Forest is an ensemble learning method that combines multiple decision trees to create a more robust and accurate model. It uses bagging (bootstrap aggregation) and feature randomness to reduce overfitting. This lecture covers how Random Forest works, feature importance, parameter tuning, and practical applications.

---

## Learning Objectives

By the end of this lecture, you will be able to:

1. Understand how Random Forest combines decision trees
2. Explain bagging and feature randomness
3. Implement RandomForestClassifier and RandomForestRegressor
4. Interpret feature importance scores
5. Tune key hyperparameters
6. Use Out-of-Bag (OOB) score for validation
7. Compare Random Forest with single decision trees

---

## Key Concepts

### 1. Ensemble Learning

Combining multiple models to create a better predictor than any single model.

**Types:**
- **Bagging**: Train models on random subsets, combine predictions
- **Boosting**: Train models sequentially, each correcting previous errors
- **Stacking**: Combine different model types

### 2. Random Forest Algorithm

1. Create B bootstrap samples from training data
2. Train a decision tree on each sample
3. At each split, consider only m randomly selected features
4. Final prediction: majority vote (classification) or average (regression)

### 3. Why It Works

- **Bagging**: Reduces variance by averaging multiple trees
- **Feature Randomness**: Decorrelates trees (different trees use different features)
- **Combined**: More robust than any single tree

### 4. Key Parameters


| Parameter | Description | Default |
|-----------|-------------|---------|
| `n_estimators` | Number of trees | 100 |
| `max_depth` | Maximum tree depth | None |
| `min_samples_split` | Min samples to split node | 2 |
| `min_samples_leaf` | Min samples in leaf | 1 |
| `max_features` | Features to consider at split | sqrt(n) |

---

## Code Examples

### Example 1: Basic Random Forest

```python
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from sklearn.datasets import make_classification

# Generate data
np.random.seed(42)
X, y = make_classification(
    n_samples=500, n_features=10, n_informative=5, n_redundant=2, random_state=42
)

print(f"Samples: {X.shape[0]}")
print(f"Features: {X.shape[1]}")

# Train/test split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train Random Forest
rf = RandomForestClassifier(n_estimators=100, random_state=42)
rf.fit(X_train, y_train)

# Evaluate
y_pred = rf.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)

print(f"\nNumber of trees: {rf.n_estimators}")
print(f"Accuracy: {accuracy:.4f}")
```

### Example 2: Random Forest vs Single Tree

```python
from sklearn.ensemble import RandomForestClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score
from sklearn.datasets import make_classification
from sklearn.model_selection import train_test_split
import numpy as np

np.random.seed(42)
X, y = make_classification(n_samples=500, n_features=10, n_informative=5, random_state=42)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Single Decision Tree
dt = DecisionTreeClassifier(random_state=42)
dt.fit(X_train, y_train)
acc_dt = accuracy_score(y_test, dt.predict(X_test))

# Random Forest
rf = RandomForestClassifier(n_estimators=100, random_state=42)
rf.fit(X_train, y_train)
acc_rf = accuracy_score(y_test, rf.predict(X_test))

print(f"Single Decision Tree: {acc_dt:.4f}")
print(f"Random Forest: {acc_rf:.4f}")
print(f"Improvement: {(acc_rf - acc_dt) * 100:.2f}%")
```

### Example 3: Feature Importance

```python
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.datasets import make_classification

np.random.seed(42)
X, y = make_classification(n_samples=500, n_features=10, n_informative=5, random_state=42)

feature_names = [f"Feature {i}" for i in range(X.shape[1])]

rf = RandomForestClassifier(n_estimators=100, random_state=42)
rf.fit(X, y)

# Feature importance
importances = rf.feature_importances_
feature_importance = pd.DataFrame(
    {"feature": feature_names, "importance": importances}
).sort_values("importance", ascending=False)

print("Feature Importances:")
for _, row in feature_importance.iterrows():
    print(f"  {row['feature']}: {row['importance']:.4f}")

# Visualize
import matplotlib.pyplot as plt

plt.figure(figsize=(8, 4))
plt.barh(feature_importance["feature"], feature_importance["importance"])
plt.xlabel("Importance")
plt.title("Feature Importance (Random Forest)")
plt.gca().invert_yaxis()
plt.tight_layout()
plt.savefig("feature_importance.png", dpi=100)
plt.show()
```

### Example 4: Parameter Tuning

```python
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import cross_val_score
import numpy as np

np.random.seed(42)
from sklearn.datasets import make_classification

X, y = make_classification(n_samples=500, n_features=10, n_informative=5, random_state=42)

# Test different n_estimators
print("Effect of n_estimators:")
for n_trees in [10, 50, 100, 200, 500]:
    rf = RandomForestClassifier(n_estimators=n_trees, random_state=42)
    scores = cross_val_score(rf, X, y, cv=5, scoring="accuracy")
    print(f"  {n_trees:3d} trees: {scores.mean():.4f} +/- {scores.std():.4f}")

# Test different max_depth
print("\nEffect of max_depth:")
for depth in [3, 5, 10, 20, None]:
    rf = RandomForestClassifier(n_estimators=100, max_depth=depth, random_state=42)
    scores = cross_val_score(rf, X, y, cv=5, scoring="accuracy")
    print(f"  depth={str(depth):5s}: {scores.mean():.4f} +/- {scores.std():.4f}")
```

### Example 5: Out-of-Bag Score

```python
from sklearn.ensemble import RandomForestClassifier
from sklearn.datasets import make_classification
import numpy as np

np.random.seed(42)
X, y = make_classification(n_samples=500, n_features=10, n_informative=5, random_state=42)

# OOB score uses unused samples for validation
rf_oob = RandomForestClassifier(n_estimators=100, oob_score=True, random_state=42)
rf_oob.fit(X, y)

print(f"OOB Score: {rf_oob.oob_score_:.4f}")
print("OOB score is a free validation estimate!")
print(f"Each tree uses ~63% of samples, leaving ~37% for OOB evaluation")
```

### Example 6: Random Forest for Regression

```python
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import r2_score, mean_squared_error
import numpy as np

np.random.seed(42)
X = np.random.rand(200, 5)
y = 3 * X[:, 0] + 2 * X[:, 1] + np.random.randn(200) * 0.5

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

rf_reg = RandomForestRegressor(n_estimators=100, random_state=42)
rf_reg.fit(X_train, y_train)

y_pred = rf_reg.predict(X_test)

print(f"R² (train): {r2_score(y_train, rf_reg.predict(X_train)):.4f}")
print(f"R² (test): {r2_score(y_test, y_pred):.4f}")
print(f"RMSE: {np.sqrt(mean_squared_error(y_test, y_pred)):.4f}")
```

---

## Common Mistakes to Avoid

### Mistake 1: Using Too Few Trees

```python
# WRONG: Using very few trees
rf_few = RandomForestClassifier(n_estimators=5, random_state=42)
# May have high variance

# CORRECT: Use enough trees (100-500)
rf_enough = RandomForestClassifier(n_estimators=100, random_state=42)
```

### Mistake 2: Not Checking Overfitting

```python
# Check if training score >> test score
from sklearn.metrics import accuracy_score

rf = RandomForestClassifier(n_estimators=100, random_state=42)
rf.fit(X_train, y_train)

train_acc = accuracy_score(y_train, rf.predict(X_train))
test_acc = accuracy_score(y_test, rf.predict(X_test))

print(f"Train accuracy: {train_acc:.4f}")
print(f"Test accuracy: {test_acc:.4f}")

if train_acc - test_acc > 0.1:
    print("WARNING: Possible overfitting!")
```

### Mistake 3: Ignoring Feature Importance

```python
# Always check feature importance
importances = rf.feature_importances_
low_importance = np.where(importances < 0.01)[0]

if len(low_importance) > 0:
    print(f"Features with low importance: {low_importance}")
    # Consider removing them
```

---

## Best Practices

### 1. Use OOB Score for Quick Validation

```python
rf = RandomForestClassifier(n_estimators=100, oob_score=True, random_state=42)
rf.fit(X, y)
print(f"OOB Score: {rf.oob_score_:.4f}")
```

### 2. Tune n_estimators First

```python
from sklearn.model_selection import cross_val_score

# Find good n_estimators
for n in [50, 100, 200, 500]:
    rf = RandomForestClassifier(n_estimators=n, random_state=42)
    scores = cross_val_score(rf, X, y, cv=5)
    print(f"n={n}: {scores.mean():.4f}")
```

### 3. Use Feature Importance for Selection

```python
# Remove low-importance features
importances = rf.feature_importances_
threshold = 0.05
important_features = np.where(importances > threshold)[0]
print(f"Selected {len(important_features)} features")
```

### 4. Parallel Training

```python
# Use multiple CPU cores
rf = RandomForestClassifier(n_estimators=100, n_jobs=-1, random_state=42)
# n_jobs=-1 uses all available cores
```

---

## Practice Exercises

### Exercise 1: Compare Ensemble Methods

```python
"""
Compare Random Forest with other ensemble methods.
1. Train Decision Tree
2. Train Random Forest
3. Train Gradient Boosting
4. Compare accuracy and training time
"""

from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.datasets import make_classification
from sklearn.model_selection import cross_val_score
import time

X, y = make_classification(n_samples=500, n_features=10, n_informative=5, random_state=42)

models = {
    "Decision Tree": DecisionTreeClassifier(random_state=42),
    "Random Forest": RandomForestClassifier(n_estimators=100, random_state=42),
    "Gradient Boosting": GradientBoostingClassifier(n_estimators=100, random_state=42),
}

for name, model in models.items():
    start = time.time()
    scores = cross_val_score(model, X, y, cv=5, scoring="accuracy")
    time_taken = time.time() - start
    print(f"{name:20s}: {scores.mean():.4f} +/- {scores.std():.4f} ({time_taken:.2f}s)")
```

### Exercise 2: Feature Selection with Random Forest

```python
"""
Use Random Forest feature importance for feature selection.
1. Train Random Forest
2. Get feature importances
3. Select top 5 features
4. Compare performance
"""

from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import cross_val_score
from sklearn.datasets import make_classification
import numpy as np

np.random.seed(42)
X, y = make_classification(n_samples=500, n_features=20, n_informative=10, random_state=42)

# Your code here
rf = RandomForestClassifier(n_estimators=100, random_state=42)
rf.fit(X, y)

importances = rf.feature_importances_
top_5 = np.argsort(importances)[-5:][::-1]
print(f"Top 5 features: {top_5}")
print(f"Importances: {importances[top_5]}")

# Compare performance
scores_all = cross_val_score(rf, X, y, cv=5, scoring="accuracy")
scores_top5 = cross_val_score(rf, X[:, top_5], y, cv=5, scoring="accuracy")

print(f"\nAll features: {scores_all.mean():.4f}")
print(f"Top 5 features: {scores_top5.mean():.4f}")
```

### Exercise 3: Hyperparameter Tuning

```python
"""
Tune Random Forest hyperparameters.
1. Tune n_estimators
2. Tune max_depth
3. Tune min_samples_split
4. Find best combination
"""

from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import GridSearchCV
from sklearn.datasets import make_classification

X, y = make_classification(n_samples=500, n_features=10, n_informative=5, random_state=42)

# Your code here
param_grid = {
    "n_estimators": [50, 100, 200],
    "max_depth": [5, 10, 20, None],
    "min_samples_split": [2, 5, 10],
}

grid_search = GridSearchCV(
    RandomForestClassifier(random_state=42), param_grid, cv=5, scoring="accuracy", n_jobs=-1
)
grid_search.fit(X, y)

print(f"Best parameters: {grid_search.best_params_}")
print(f"Best CV accuracy: {grid_search.best_score_:.4f}")
```

---

## Summary

| Concept | Description |
|---------|-------------|
| **Random Forest** | Ensemble of decision trees with bagging |
| **Bagging** | Training on random subsets |
| **Feature Randomness** | Random feature selection at each split |
| **Feature Importance** | Measures feature contribution |
| **OOB Score** | Free validation using unused samples |
| **n_estimators** | Number of trees (more = better, slower) |

### Key Takeaways

1. Random Forest is **robust to overfitting**
2. Use **OOB score** for quick validation
3. **Feature importance** helps with interpretation
4. **More trees** = better performance (with diminishing returns)
5. Works for both **classification and regression**

---

## Next Steps

- **Lecture 21**: SVM — Another powerful algorithm
- **Lecture 22**: Cross-Validation — Proper evaluation
- **Lecture 23**: KNN — Instance-based learning

---

## References

- [W3Schools - Random Forest](https://www.w3schools.com/python/ml_random_forest.asp)
- [Scikit-learn Documentation - RandomForestClassifier](https://scikit-learn.org/stable/modules/generated/sklearn.ensemble.RandomForestClassifier.html)
- [Wikipedia - Random Forest](https://en.wikipedia.org/wiki/Random_forest)
