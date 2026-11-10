# Glossary: Decision Trees

## Quick Reference Table

| Term | Definition | Category |
|------|-----------|----------|
| Decision Tree | Flowchart model for classification/regression | Algorithm |
| DecisionTreeClassifier | Classification decision tree | Tool |
| DecisionTreeRegressor | Regression decision tree | Tool |
| Gini Impurity | Measure of node purity | Metric |
| Entropy | Measure of disorder in data | Metric |
| Information Gain | Reduction in entropy from splitting | Metric |
| max_depth | Maximum depth of tree | Parameter |
| min_samples_split | Min samples to split a node | Parameter |
| min_samples_leaf | Min samples in a leaf node | Parameter |
| Feature Importance | Contribution of features to predictions | Concept |
| Overfitting | Tree too complex, memorizes noise | Problem |
| Pruning | Reducing tree complexity | Technique |
| Leaf Node | Terminal node making prediction | Structure |
| Internal Node | Decision node with feature test | Structure |
| Branch | Path from node to child | Structure |
| Root Node | Top node of the tree | Structure |
| Split | Division of data at a node | Process |
| Criterion | Quality measure for splits | Parameter |
| Depth | Distance from root to deepest leaf | Metric |
| Node Count | Total number of nodes in tree | Metric |

---

## Detailed Definitions

### C

#### Classification Decision Tree
**Definition:** A decision tree that predicts discrete class labels. Each leaf node represents a class, and predictions are made by following the path from root to leaf.

**Example:**
```python
from sklearn.tree import DecisionTreeClassifier
from sklearn.datasets import make_classification
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

X, y = make_classification(n_samples=200, n_features=4, random_state=42)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

clf = DecisionTreeClassifier(max_depth=3, random_state=42)
clf.fit(X_train, y_train)

y_pred = clf.predict(X_test)
print(f"Accuracy: {accuracy_score(y_test, y_pred):.4f}")
```

**Related Terms:** DecisionTreeRegressor, Classification, Gini Impurity

#### Criterion
**Definition:** The quality measure used to evaluate splits. Options are 'gini' (Gini impurity) and 'entropy' (information gain).

**Example:**
```python
from sklearn.tree import DecisionTreeClassifier

# Gini (default)
clf_gini = DecisionTreeClassifier(criterion="gini", random_state=42)

# Entropy
clf_entropy = DecisionTreeClassifier(criterion="entropy", random_state=42)
```

**Related Terms:** Gini Impurity, Entropy, Information Gain

---

### E

#### Entropy
**Definition:** A measure of disorder or uncertainty in a dataset. Ranges from 0 (pure) to log₂(k) (maximum disorder for k classes).

**Formula:**
```
Entropy = -Σ(pᵢ × log₂(pᵢ))
```

**Example:**
```python
import numpy as np

# Pure node (all same class)
p = 1.0
entropy_pure = -(p * np.log2(p) if p > 0 else 0)
print(f"Pure node entropy: {entropy_pure:.4f}")  # 0.0

# Impure node (50/50 split)
p = 0.5
entropy_impure = -(p * np.log2(p) + (1 - p) * np.log2(1 - p))
print(f"Impure node entropy: {entropy_impure:.4f}")  # 1.0
```

**Related Terms:** Gini Impurity, Information Gain, Criterion

---

### F

#### Feature Importance
**Definition:** A measure of how much each feature contributes to the model's predictions. In decision trees, based on how much each feature reduces impurity across all splits.

**Example:**
```python
from sklearn.tree import DecisionTreeClassifier

clf = DecisionTreeClassifier(max_depth=5, random_state=42)
clf.fit(X_train, y_train)

importances = clf.feature_importances_
for i, imp in enumerate(importances):
    print(f"Feature {i}: {imp:.4f}")
```

**Related Terms:** Gini Importance, Permutation Importance, Feature Selection

---

### G

#### Gini Impurity
**Definition:** A measure of how often a randomly chosen element would be incorrectly classified. Ranges from 0 (pure) to 0.5 (maximum impurity for binary classification).

**Formula:**
```
Gini = 1 - Σ(pᵢ²)
```

**Example:**
```python
import numpy as np

# Pure node (all same class)
p = 1.0
gini_pure = 1 - p**2
print(f"Pure node Gini: {gini_pure:.4f}")  # 0.0

# Impure node (50/50 split)
p = 0.5
gini_impure = 1 - (p**2 + (1 - p) ** 2)
print(f"Impure node Gini: {gini_impure:.4f}")  # 0.5
```

**Interpretation:**
- Gini = 0: Pure node (all samples same class)
- Gini = 0.5: Maximum impurity (binary, 50/50 split)
- Lower Gini = better split

**Related Terms:** Entropy, Information Gain, Criterion

---

### I

#### Information Gain
**Definition:** The reduction in entropy achieved by splitting on a particular feature. The feature with highest information gain is chosen for splitting.

**Formula:**
```
Information Gain = Entropy(parent) - Σ(weighted entropy of children)
```

**Example:**
```python
import numpy as np


def entropy(labels):
    probs = np.bincount(labels) / len(labels)
    return -np.sum([p * np.log2(p) for p in probs if p > 0])


# Parent entropy
parent = np.array([0, 0, 0, 1, 1])
parent_entropy = entropy(parent)

# Split on feature
left = np.array([0, 0, 0])  # All class 0
right = np.array([1, 1])  # All class 1

# Weighted child entropy
child_entropy = (len(left) / len(parent)) * entropy(left) + (len(right) / len(parent)) * entropy(
    right
)

info_gain = parent_entropy - child_entropy
print(f"Information Gain: {info_gain:.4f}")
```

**Related Terms:** Entropy, Gini Impurity, Split

---

### L

#### Leaf Node
**Definition:** A terminal node in a decision tree that makes the final prediction. For classification, it predicts the majority class; for regression, it predicts the mean of training samples.

**Example:**
```python
clf = DecisionTreeClassifier(max_depth=3, random_state=42)
clf.fit(X_train, y_train)

print(f"Number of leaves: {clf.get_n_leaves()}")
# Each leaf contains predictions for samples that reach it
```

**Related Terms:** Internal Node, Root Node, Node Count

---

### M

#### min_samples_leaf
**Definition:** The minimum number of samples required to be in a leaf node. Prevents leaves from being too specific and helps prevent overfitting.

**Example:**
```python
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score

# Default (min_samples_leaf=1)
clf_default = DecisionTreeClassifier(random_state=42)
clf_default.fit(X_train, y_train)

# With min_samples_leaf=5
clf_leaf5 = DecisionTreeClassifier(min_samples_leaf=5, random_state=42)
clf_leaf5.fit(X_train, y_train)

print(f"Default: {clf_default.get_n_leaves()} leaves")
print(f"min_samples_leaf=5: {clf_leaf5.get_n_leaves()} leaves")
print(f"Default accuracy: {accuracy_score(y_test, clf_default.predict(X_test)):.4f}")
print(f"Leaf5 accuracy: {accuracy_score(y_test, clf_leaf5.predict(X_test)):.4f}")
```

**Related Terms:** max_depth, min_samples_split, Pruning

#### min_samples_split
**Definition:** The minimum number of samples required to split an internal node. Higher values prevent splitting nodes with few samples.

**Example:**
```python
clf = DecisionTreeClassifier(min_samples_split=10, random_state=42)
clf.fit(X_train, y_train)
print(f"Accuracy: {accuracy_score(y_test, clf.predict(X_test)):.4f}")
```

**Related Terms:** max_depth, min_samples_leaf, Pruning

---

### P

#### Pruning
**Definition:** The process of reducing the size of a decision tree by removing nodes that provide little predictive power. Helps prevent overfitting.

**Types:**
- **Pre-pruning:** Stop growing tree early (max_depth, min_samples_split)
- **Post-pruning:** Grow full tree, then remove branches

**Example:**
```python
# Pre-pruning with max_depth
clf_pruned = DecisionTreeClassifier(
    max_depth=5, min_samples_split=10, min_samples_leaf=5, random_state=42
)
clf_pruned.fit(X_train, y_train)
```

**Related Terms:** Overfitting, max_depth, min_samples_split

---

### R

#### Regression Decision Tree
**Definition:** A decision tree that predicts continuous numerical values. Each leaf node predicts the mean of training samples that reach it.

**Example:**
```python
from sklearn.tree import DecisionTreeRegressor

reg = DecisionTreeRegressor(max_depth=3, random_state=42)
reg.fit(X_train_reg, y_train_reg)

r2 = reg.score(X_test_reg, y_test_reg)
print(f"Regression tree R²: {r2:.4f}")
```

**Related Terms:** DecisionTreeClassifier, Regression, R-squared

#### Root Node
**Definition:** The topmost node of a decision tree where the first split is made. Contains the entire dataset before any splitting.

**Example:**
```python
clf = DecisionTreeClassifier(random_state=42)
clf.fit(X_train, y_train)

# Root node contains all training samples
print(f"Root node samples: {clf.tree_.n_node_samples[0]}")
```

**Related Terms:** Internal Node, Leaf Node, Tree Structure

---

## Key Parameters


| Parameter | Description | Default | Effect |
|-----------|-------------|---------|--------|
| `criterion` | Split quality measure | 'gini' | gini or entropy |
| `max_depth` | Maximum tree depth | None | Controls complexity |
| `min_samples_split` | Min samples to split | 2 | Prevents small splits |
| `min_samples_leaf` | Min samples in leaf | 1 | Prevents small leaves |
| `max_features` | Features to consider | None | Feature subsampling |
| `max_leaf_nodes` | Max number of leaves | None | Limits tree size |

---

## Python Import Cheat Sheet

```python
# Classification
from sklearn.tree import DecisionTreeClassifier

# Regression
from sklearn.tree import DecisionTreeRegressor

# Visualization (optional)
from sklearn.tree import plot_tree, export_text

# Metrics
from sklearn.metrics import accuracy_score, classification_report

# Workflow
clf = DecisionTreeClassifier(
    max_depth=5, min_samples_split=10, min_samples_leaf=5, criterion="gini", random_state=42
)
clf.fit(X_train, y_train)
y_pred = clf.predict(X_test)

# Feature importance
importances = clf.feature_importances_

# Tree info
print(f"Depth: {clf.get_depth()}")
print(f"Leaves: {clf.get_n_leaves()}")
print(f"Nodes: {clf.tree_.node_count}")
```
