# Lecture 11: Decision Trees

## Topic Overview

Decision Trees are intuitive, easy-to-interpret models that split data based on feature values to make predictions. They work for both classification and regression tasks. This lecture covers the DecisionTreeClassifier, tree parameters, Gini impurity vs entropy, feature importance, overfitting, and pruning.

---

## Learning Objectives

By the end of this lecture, you will be able to:

1. Understand how decision trees make predictions
2. Use `DecisionTreeClassifier` for classification
3. Use `DecisionTreeRegressor` for regression
4. Understand Gini impurity and entropy
5. Control tree size with hyperparameters
6. Interpret feature importances
7. Recognize and prevent overfitting
8. Generate classification reports

---

## Key Concepts

### 1. How Decision Trees Work

A decision tree creates a flowchart of if-else rules:
```
Is feature X₁ > threshold?
├── Yes → Is feature X₂ > threshold?
│         ├── Yes → Class A
│         └── No → Class B
└── No → Class C
```

### 2. Splitting Criteria

**Gini Impurity:**
```
Gini = 1 - Σ(pᵢ²)
```
Measures how often a randomly chosen element would be misclassified.

**Entropy:**
```
Entropy = -Σ(pᵢ × log₂(pᵢ))
```
Measures the disorder or uncertainty in the data.

### 3. Tree Parameters


| Parameter | Description | Default |
|-----------|-------------|---------|
| `max_depth` | Maximum tree depth | None |
| `min_samples_split` | Min samples to split a node | 2 |
| `min_samples_leaf` | Min samples in a leaf | 1 |
| `criterion` | Split quality measure | 'gini' |

### 4. Overfitting in Decision Trees

Unconstrained trees can grow very deep and memorize training data. Regularization parameters help control this.

### 5. Feature Importance

Shows which features contribute most to the tree's decisions. Based on how much each feature reduces impurity.

---

## Code Examples

### Example 1: Generate Classification Data

```python
from sklearn.datasets import make_classification
from sklearn.model_selection import train_test_split

np.random.seed(42)
X, y = make_classification(
    n_samples=200, n_features=4, n_informative=3, n_redundant=1, n_classes=2, random_state=42
)

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

print(f"Features: {X.shape[1]}")
print(f"Samples: {X.shape[0]}")
print(f"Classes: {np.unique(y)}")
```

### Example 2: Basic Decision Tree

```python
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score

clf = DecisionTreeClassifier(random_state=42)
clf.fit(X_train, y_train)

y_pred = clf.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)

print(f"Accuracy: {accuracy:.4f}")
print(f"Number of nodes: {clf.tree_.node_count}")
print(f"Number of leaves: {clf.get_n_leaves()}")
print(f"Tree depth: {clf.get_depth()}")
```

### Example 3: Gini vs Entropy

```python
# Gini impurity (default)
clf_gini = DecisionTreeClassifier(criterion="gini", random_state=42)
clf_gini.fit(X_train, y_train)
acc_gini = accuracy_score(y_test, clf_gini.predict(X_test))

# Entropy
clf_entropy = DecisionTreeClassifier(criterion="entropy", random_state=42)
clf_entropy.fit(X_train, y_train)
acc_entropy = accuracy_score(y_test, clf_entropy.predict(X_test))

print(f"Gini accuracy: {acc_gini:.4f}")
print(f"Entropy accuracy: {acc_entropy:.4f}")
```

### Example 4: Controlling Tree Size

```python
# Max depth
clf_depth3 = DecisionTreeClassifier(max_depth=3, random_state=42)
clf_depth3.fit(X_train, y_train)
acc_depth3 = accuracy_score(y_test, clf_depth3.predict(X_test))

# Min samples split
clf_split10 = DecisionTreeClassifier(min_samples_split=10, random_state=42)
clf_split10.fit(X_train, y_train)
acc_split10 = accuracy_score(y_test, clf_split10.predict(X_test))

# Min samples leaf
clf_leaf5 = DecisionTreeClassifier(min_samples_leaf=5, random_state=42)
clf_leaf5.fit(X_train, y_train)
acc_leaf5 = accuracy_score(y_test, clf_leaf5.predict(X_test))

print(f"max_depth=3: Accuracy={acc_depth3:.4f}, Depth={clf_depth3.get_depth()}")
print(f"min_samples_split=10: Accuracy={acc_split10:.4f}")
print(f"min_samples_leaf=5: Accuracy={acc_leaf5:.4f}")
```

### Example 5: Feature Importance

```python
clf = DecisionTreeClassifier(max_depth=5, random_state=42)
clf.fit(X_train, y_train)

importances = clf.feature_importances_
feature_names = [f"Feature {i}" for i in range(X.shape[1])]

print("Feature importances:")
for name, importance in sorted(zip(feature_names, importances), key=lambda x: x[1], reverse=True):
    print(f"  {name}: {importance:.4f}")
```

### Example 6: Overfitting Demonstration

```python
# Unconstrained (overfits)
clf_unlimited = DecisionTreeClassifier(random_state=42)
clf_unlimited.fit(X_train, y_train)

acc_train = accuracy_score(y_train, clf_unlimited.predict(X_train))
acc_test = accuracy_score(y_test, clf_unlimited.predict(X_test))

print("Unconstrained tree:")
print(f"  Train accuracy: {acc_train:.4f}")
print(f"  Test accuracy: {acc_test:.4f}")
print(f"  Gap: {acc_train - acc_test:.4f}")

# Pruned
clf_pruned = DecisionTreeClassifier(max_depth=5, random_state=42)
clf_pruned.fit(X_train, y_train)

acc_train_p = accuracy_score(y_train, clf_pruned.predict(X_train))
acc_test_p = accuracy_score(y_test, clf_pruned.predict(X_test))

print("\nPruned tree (max_depth=5):")
print(f"  Train accuracy: {acc_train_p:.4f}")
print(f"  Test accuracy: {acc_test_p:.4f}")
print(f"  Gap: {acc_train_p - acc_test_p:.4f}")
```

### Example 7: Classification Report

```python
from sklearn.metrics import classification_report

y_pred = clf_pruned.predict(X_test)
print(classification_report(y_test, y_pred))
```

### Example 8: Decision Tree for Regression

```python
from sklearn.tree import DecisionTreeRegressor

np.random.seed(42)
X_reg = np.random.rand(100, 1) * 10
y_reg = np.sin(X_reg.squeeze()) + np.random.randn(100) * 0.2

X_train_reg, X_test_reg, y_train_reg, y_test_reg = train_test_split(
    X_reg, y_reg, test_size=0.2, random_state=42
)

reg = DecisionTreeRegressor(max_depth=3, random_state=42)
reg.fit(X_train_reg, y_train_reg)

r2_train = reg.score(X_train_reg, y_train_reg)
r2_test = reg.score(X_test_reg, y_test_reg)

print(f"Regression tree R² (train): {r2_train:.4f}")
print(f"Regression tree R² (test): {r2_test:.4f}")
```

---

## Common Mistakes to Avoid

1. **Not pruning** — Unconstrained trees overfit
2. **Ignoring feature importance** — Helps understand the model
3. **Using default parameters** — Always tune max_depth
4. **Not evaluating on test set** — Training accuracy is misleading
5. **Expecting linear boundaries** — Trees create axis-parallel splits

---

## Best Practices

1. **Start with max_depth=3-5** — Prevents overfitting
2. **Use min_samples_leaf** — Ensures leaves have enough samples
3. **Check feature importance** — For interpretability
4. **Use ensemble methods** — Random Forest, Gradient Boosting for better performance
5. **Visualize the tree** — If possible, for understanding

---

## Summary

| Concept | Description |
|---------|-------------|
| **Decision Tree** | Flowchart of if-else rules |
| **Gini Impurity** | Measure of node purity |
| **Entropy** | Measure of disorder |
| **max_depth** | Controls tree complexity |
| **Feature Importance** | Which features matter most |
| **Overfitting** | Tree too deep, memorizes noise |
| **Pruning** | Reducing tree complexity |

**Key Takeaway:** Decision trees are intuitive and interpretable models that split data based on feature values. Control tree size with max_depth and min_samples_leaf to prevent overfitting. Use feature importance to understand which features drive predictions.

---

## Next Lecture

In [Lecture 12: Confusion Matrix](12-confusion-matrix-lecture.md), we'll learn about classification evaluation metrics — accuracy, precision, recall, and F1 score.
