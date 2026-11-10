# Lecture 21: Support Vector Machines (SVM)

## Topic Overview

Support Vector Machines (SVM) are powerful classification algorithms that find the optimal hyperplane to separate classes with maximum margin. SVM excels in high-dimensional spaces and uses the kernel trick to handle non-linear data. This lecture covers the fundamentals of SVM, different kernels, and practical implementation.

---

## Learning Objectives

By the end of this lecture, you will be able to:

1. Understand the concept of maximum margin classifier
2. Explain what support vectors are and their role
3. Use different kernels (linear, RBF, polynomial)
4. Tune C and gamma parameters
5. Implement SVM for classification and regression
6. Know when to use SVM vs other algorithms

---

## Key Concepts

### 1. Maximum Margin Classifier

SVM finds the hyperplane that maximizes the distance (margin) between the closest points of different classes.

**Margin**: Distance between hyperplane and nearest support vectors

### 2. Support Vectors

The data points closest to the decision boundary. Only these points determine the hyperplane position.

### 3. The Kernel Trick

Transforms data to higher dimensions where it becomes linearly separable, without actually computing the transformation.

### 4. Key Parameters


| Parameter | Description | Effect |
|-----------|-------------|--------|
| `C` | Regularization | Small C = more regularization |
| `gamma` | Kernel coefficient | Large gamma = more complex boundary |
| `kernel` | Kernel type | linear, rbf, poly, sigmoid |

---

## Code Examples

### Example 1: Linear SVM

```python
import numpy as np
from sklearn.svm import SVC
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from sklearn.datasets import make_classification
from sklearn.preprocessing import StandardScaler

# Generate linear data
np.random.seed(42)
X, y = make_classification(
    n_samples=200,
    n_features=2,
    n_redundant=0,
    n_informative=2,
    random_state=42,
    n_clusters_per_class=1,
)

# Split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Scale (IMPORTANT for SVM!)
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# Linear SVM
svm_linear = SVC(kernel="linear", random_state=42)
svm_linear.fit(X_train_scaled, y_train)

y_pred = svm_linear.predict(X_test_scaled)
accuracy = accuracy_score(y_test, y_pred)

print(f"Linear SVM Accuracy: {accuracy:.4f}")
print(f"Number of support vectors: {svm_linear.n_support_}")
```

### Example 2: Different Kernels

```python
from sklearn.svm import SVC
from sklearn.datasets import make_circles
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from sklearn.preprocessing import StandardScaler
import numpy as np

# Non-linear data
np.random.seed(42)
X_circles, y_circles = make_circles(n_samples=200, noise=0.1, factor=0.5, random_state=42)

X_train, X_test, y_train, y_test = train_test_split(
    X_circles, y_circles, test_size=0.2, random_state=42
)

scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# Test different kernels
kernels = ["linear", "rbf", "poly", "sigmoid"]
print("Kernel Comparison (non-linear data):")
print("-" * 35)

for kernel in kernels:
    svm = SVC(kernel=kernel, random_state=42)
    svm.fit(X_train_scaled, y_train)
    acc = accuracy_score(y_test, svm.predict(X_test_scaled))
    print(f"{kernel:>10}: Accuracy = {acc:.4f}")
```

### Example 3: Support Vectors

```python
from sklearn.svm import SVC
from sklearn.datasets import make_classification
from sklearn.preprocessing import StandardScaler
import numpy as np

X, y = make_classification(n_samples=200, n_features=2, n_redundant=0, random_state=42)

scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

svm = SVC(kernel="rbf", random_state=42)
svm.fit(X_scaled, y)

print(f"Number of support vectors per class: {svm.n_support_}")
print(f"Total support vectors: {sum(svm.n_support_)}")
print(f"Support vectors shape: {svm.support_vectors_.shape}")
print(f"\nSupport vectors (first 5):")
print(svm.support_vectors_[:5])
```

### Example 4: Parameter Tuning

```python
from sklearn.svm import SVC
from sklearn.datasets import make_classification
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from sklearn.preprocessing import StandardScaler
import numpy as np

np.random.seed(42)
X, y = make_classification(n_samples=200, n_features=10, n_informative=5, random_state=42)

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# Grid search for C and gamma
results = []
for C in [0.1, 1, 10, 100]:
    for gamma in [0.1, 1, 10]:
        svm = SVC(kernel="rbf", C=C, gamma=gamma, random_state=42)
        svm.fit(X_train_scaled, y_train)
        acc = accuracy_score(y_test, svm.predict(X_test_scaled))
        results.append({"C": C, "gamma": gamma, "accuracy": acc})

# Find best
best = max(results, key=lambda x: x["accuracy"])
print(f"Best parameters: C={best['C']}, gamma={best['gamma']}")
print(f"Best accuracy: {best['accuracy']:.4f}")
```

### Example 5: SVM for Regression

```python
from sklearn.svm import SVR
from sklearn.model_selection import train_test_split
from sklearn.metrics import r2_score
from sklearn.preprocessing import StandardScaler
import numpy as np

np.random.seed(42)
X = np.random.rand(200, 1) * 10
y = 2 * X.squeeze() + 3 + np.random.randn(200) * 0.5

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

svr = SVR(kernel="rbf")
svr.fit(X_train_scaled, y_train)

y_pred = svr.predict(X_test_scaled)
r2 = r2_score(y_test, y_pred)

print(f"SVR R² Score: {r2:.4f}")
```

### Example 6: When to Use SVM

```python
print("SVM Advantages:")
print("  ✓ Effective in high-dimensional spaces")
print("  ✓ Memory efficient (uses support vectors only)")
print("  ✓ Versatile (different kernels)")
print("  ✓ Effective when number of features > samples")

print("\nSVM Disadvantages:")
print("  ✗ Slow on large datasets (O(n²) to O(n³))")
print("  ✗ Sensitive to feature scaling")
print("  ✗ Not good with noisy data")
print("  ✗ No probability estimates by default")

print("\nWhen to use SVM:")
print("  - Small to medium dataset (< 10,000 samples)")
print("  - High-dimensional data")
print("  - Clear margin of separation")
print("  - Text classification")
```

---

## Common Mistakes to Avoid

### Mistake 1: Not Scaling Features

```python
# WRONG: SVM is very sensitive to feature scales
svm_unscaled = SVC()
svm_unscaled.fit(X_train, y_train)  # Bad results

# CORRECT: Always scale for SVM
from sklearn.preprocessing import StandardScaler

scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)
svm_scaled = SVC()
svm_scaled.fit(X_train_scaled, y_train)  # Good results
```

### Mistake 2: Using SVM on Large Datasets

```python
# SVM is O(n²) to O(n³) - slow on large datasets
if len(X) > 10000:
    print("Consider using other algorithms:")
    print("  - Random Forest")
    print("  - Logistic Regression")
    print("  - Neural Networks")
```

### Mistake 3: Not Tuning Parameters

```python
# Default parameters may not be optimal
from sklearn.model_selection import GridSearchCV

param_grid = {"C": [0.1, 1, 10, 100], "gamma": [0.1, 1, 10], "kernel": ["rbf", "linear"]}

grid = GridSearchCV(SVC(), param_grid, cv=5, scoring="accuracy")
grid.fit(X_train_scaled, y_train)

print(f"Best parameters: {grid.best_params_}")
print(f"Best accuracy: {grid.best_score_:.4f}")
```

---

## Best Practices

### 1. Always Scale Features

```python
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.svm import SVC

# Use pipeline for reproducibility
pipeline = Pipeline(
    [("scaler", StandardScaler()), ("svm", SVC(kernel="rbf", C=1.0, gamma="scale"))]
)

pipeline.fit(X_train, y_train)
score = pipeline.score(X_test, y_test)
```

### 2. Use RBF Kernel by Default

```python
# RBF is usually the best choice
svm = SVC(kernel="rbf", C=1.0, gamma="scale")
# gamma='scale' uses 1/(n_features * X.var())
```

### 3. Tune C and Gamma

```python
from sklearn.model_selection import GridSearchCV

param_grid = {"C": [0.1, 1, 10], "gamma": [0.1, 1, 10]}
grid = GridSearchCV(SVC(), param_grid, cv=5)
grid.fit(X_train_scaled, y_train)
```

### 4. Use for Small/Medium Datasets

```python
if len(X) < 10000:
    # SVM is a good choice
    model = SVC(kernel="rbf")
else:
    # Consider faster alternatives
    from sklearn.ensemble import RandomForestClassifier

    model = RandomForestClassifier(n_estimators=100)
```

---

## Practice Exercises

### Exercise 1: Linear vs Non-Linear

```python
"""
Compare linear and non-linear SVM on different datasets.
1. Generate linear data
2. Generate non-linear data (moons, circles)
3. Test linear and RBF kernels
4. Compare results
"""

from sklearn.svm import SVC
from sklearn.datasets import make_moons, make_circles
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score
import numpy as np

# Your code here
datasets = {
    "Linear": make_classification(n_samples=200, n_features=2, n_redundant=0, random_state=42),
    "Moons": make_moons(n_samples=200, noise=0.1, random_state=42),
    "Circles": make_circles(n_samples=200, noise=0.1, factor=0.5, random_state=42),
}

for name, (X, y) in datasets.items():
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)

    linear = SVC(kernel="linear").fit(X_train_scaled, y_train)
    rbf = SVC(kernel="rbf").fit(X_train_scaled, y_train)

    acc_linear = accuracy_score(y_test, linear.predict(X_test_scaled))
    acc_rbf = accuracy_score(y_test, rbf.predict(X_test_scaled))

    print(f"{name:10s}: Linear={acc_linear:.4f}, RBF={acc_rbf:.4f}")
```

### Exercise 2: Parameter Sensitivity

```python
"""
Analyze how C and gamma affect decision boundary.
1. Create 2D data
2. Train SVM with different C values
3. Train SVM with different gamma values
4. Visualize decision boundaries
"""

from sklearn.svm import SVC
from sklearn.datasets import make_moons
from sklearn.preprocessing import StandardScaler
import numpy as np

X, y = make_moons(n_samples=200, noise=0.1, random_state=42)
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# Your code here
C_values = [0.01, 0.1, 1, 10, 100]
for C in C_values:
    svm = SVC(kernel="rbf", C=C, gamma="scale")
    svm.fit(X_scaled, y)
    n_sv = sum(svm.n_support_)
    print(f"C={C:6.2f}: Support vectors={n_sv}")

print()
gamma_values = [0.01, 0.1, 1, 10, 100]
for gamma in gamma_values:
    svm = SVC(kernel="rbf", C=1, gamma=gamma)
    svm.fit(X_scaled, y)
    n_sv = sum(svm.n_support_)
    print(f"gamma={gamma:6.2f}: Support vectors={n_sv}")
```

### Exercise 3: SVM Pipeline

```python
"""
Build a complete SVM pipeline.
1. Load dataset
2. Scale features
3. Train SVM
4. Evaluate with cross-validation
"""

from sklearn.svm import SVC
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import cross_val_score
from sklearn.datasets import load_breast_cancer

# Your code here
data = load_breast_cancer()
X, y = data.data, data.target

pipeline = Pipeline(
    [
        ("scaler", StandardScaler()),
        ("svm", SVC(kernel="rbf", C=1.0, gamma="scale", random_state=42)),
    ]
)

scores = cross_val_score(pipeline, X, y, cv=5, scoring="accuracy")
print(f"Cross-validation accuracy: {scores.mean():.4f} +/- {scores.std():.4f}")
```

---

## Summary

| Concept | Description |
|---------|-------------|
| **SVM** | Finds maximum margin hyperplane |
| **Support Vectors** | Points closest to decision boundary |
| **Kernel Trick** | Handles non-linear data |
| **RBF Kernel** | Most common, handles non-linearity |
| **C Parameter** | Regularization (smaller = more) |
| **gamma** | Kernel coefficient (larger = complex) |

### Key Takeaways

1. **Always scale features** for SVM
2. **RBF kernel** is usually the best choice
3. **Tune C and gamma** for best performance
4. **Not suitable for large datasets** (>10k samples)
5. **Great for high-dimensional data**

---

## Next Steps

- **Lecture 22**: Cross-Validation — Proper model evaluation
- **Lecture 23**: KNN — Instance-based learning
- **Lecture 20**: Random Forest — Faster alternative for large data

---

## References

- [W3Schools - SVM](https://www.w3schools.com/python/ml_svm.asp)
- [Scikit-learn Documentation - SVM](https://scikit-learn.org/stable/modules/svm.html)
- [Wikipedia - SVM](https://en.wikipedia.org/wiki/Support_vector_machine)
