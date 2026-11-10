# Glossary: R-squared (Coefficient of Determination)

## Quick Reference Table

| Term | Definition | Category |
|------|-----------|----------|
| R-squared | Proportion of variance explained by model | Metric |
| Adjusted R² | R² penalized for number of features | Metric |
| Coefficient of Determination | Another name for R² | Concept |
| TSS | Total Sum of Squares | Component |
| RSS | Residual Sum of Squares | Component |
| ESS | Explained Sum of Squares | Component |
| Residual | Difference between actual and predicted | Concept |
| Variance | Spread of data around mean | Concept |
| Overfitting | Model learns noise, not pattern | Problem |
| Explained Variance | Variance captured by model | Concept |
| Unexplained Variance | Variance not captured by model | Concept |
| .score() | Scikit-learn method returning R² | Method |
| Baseline | Simple model (e.g., predict mean) | Concept |
| Goodness of Fit | How well model matches data | Concept |
| Regression Metrics | Tools to evaluate regression models | Category |
| Mean Squared Error | Average squared prediction error | Metric |
| Root Mean Squared Error | Square root of MSE | Metric |
| Mean Absolute Error | Average absolute prediction error | Metric |
| Sum of Squares | Foundation of R² calculation | Concept |
| Normalized | Scaled to standard range | Technique |

---

## Detailed Definitions

### A

#### Adjusted R-squared
**Definition:** A modified version of R² that adjusts for the number of predictors in the model. Unlike regular R², it can decrease when irrelevant features are added, making it useful for comparing models with different numbers of features.

**Formula:**
```
Adjusted R² = 1 - (1 - R²) × (n - 1) / (n - p - 1)
```
where n = samples, p = features

**Example:**
```python
import numpy as np
from sklearn.linear_model import LinearRegression

np.random.seed(42)
n = 100

# Model with 1 feature
X1 = np.random.rand(n, 1)
y = 2 * X1.ravel() + np.random.randn(n)

model1 = LinearRegression().fit(X1, y)
r2_1 = model1.score(X1, y)
adj_r2_1 = 1 - (1 - r2_1) * (n - 1) / (n - 1 - 1)

# Model with 10 features (only 1 meaningful)
X10 = np.random.rand(n, 10)
X10[:, 0] = X1.ravel()
model10 = LinearRegression().fit(X10, y)
r2_10 = model10.score(X10, y)
adj_r2_10 = 1 - (1 - r2_10) * (n - 1) / (n - 10 - 1)

print(f"1 feature:  R²={r2_1:.4f}, Adj R²={adj_r2_1:.4f}")
print(f"10 features: R²={r2_10:.4f}, Adj R²={adj_r2_10:.4f}")
# R² increases with more features, but Adjusted R² may decrease
```

**Related Terms:** R-squared, Overfitting, Feature Selection

---

### B

#### Baseline Model
**Definition:** A simple reference model used for comparison. The simplest baseline is predicting the mean of the target variable for all predictions.

**Example:**
```python
import numpy as np
from sklearn.metrics import r2_score

y = np.array([1, 2, 3, 4, 5])
y_mean = np.full_like(y, y.mean())

baseline_r2 = r2_score(y, y_mean)
print(f"Baseline (mean) R²: {baseline_r2:.4f}")  # 0.0
# Any model with R² > 0 is better than the baseline
```

**Related Terms:** R-squared, Null Model, Intercept-only Model

---

### E

#### Explained Sum of Squares (ESS)
**Definition:** The portion of the total variance that is explained by the model. Measures how much better the model is compared to just predicting the mean.

**Formula:**
```
ESS = Σ(ŷᵢ - ȳ)²
```

**Example:**
```python
import numpy as np

y_actual = np.array([1, 2, 3, 4, 5])
y_pred = np.array([1.1, 1.9, 3.2, 3.8, 5.1])
y_mean = y_actual.mean()

ess = np.sum((y_pred - y_mean) ** 2)
tss = np.sum((y_actual - y_mean) ** 2)
rss = np.sum((y_actual - y_pred) ** 2)

print(f"ESS: {ess:.4f}")
print(f"TSS: {tss:.4f}")
print(f"RSS: {rss:.4f}")
print(f"ESS + RSS = TSS: {np.isclose(ess + rss, tss)}")
```

**Related Terms:** TSS, RSS, R-squared, Explained Variance

#### Explained Variance
**Definition:** The variance in the target variable that is predictable from the features. Closely related to R² but doesn't account for model bias.

**Example:**
```python
from sklearn.metrics import explained_variance_score

y_actual = np.array([1, 2, 3, 4, 5])
y_predicted = np.array([1.1, 1.9, 3.2, 3.8, 5.1])

evs = explained_variance_score(y_actual, y_predicted)
print(f"Explained Variance: {evs:.4f}")
```

**Related Terms:** R-squared, Variance, TSS

---

### R

#### R-squared (R²)
**Definition:** A statistical measure that represents the proportion of the variance in the dependent variable that is predictable from the independent variable(s). Also called the Coefficient of Determination.

**Formula:**
```
R² = 1 - (RSS / TSS)
```

**Example:**
```python
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score
import numpy as np

# Create data
np.random.seed(42)
X = np.random.rand(100, 1) * 10
y = 2.5 * X.ravel() + 5 + np.random.randn(100) * 2

# Fit model
model = LinearRegression()
model.fit(X, y)

# Method 1: Using model.score()
r2_method1 = model.score(X, y)

# Method 2: Using r2_score()
y_pred = model.predict(X)
r2_method2 = r2_score(y, y_pred)

# Method 3: Manual calculation
y_mean = np.full_like(y, y.mean())
tss = np.sum((y - y_mean) ** 2)
rss = np.sum((y - y_pred) ** 2)
r2_method3 = 1 - (rss / tss)

print(f"R² (model.score): {r2_method1:.4f}")
print(f"R² (r2_score):    {r2_method2:.4f}")
print(f"R² (manual):      {r2_method3:.4f}")
```

**Interpretation:**

| R² | Meaning |
|----|---------|
| 1.0 | Perfect fit |
| 0.9 | 90% of variance explained |
| 0.5 | 50% of variance explained |
| 0.0 | No better than mean |
| < 0 | Worse than mean |

**Related Terms:** Adjusted R², TSS, RSS, Goodness of Fit

#### Residual
**Definition:** The difference between the actual and predicted values. Represents the error or unexplained portion of the data.

**Formula:**
```
Residual = Actual - Predicted = y - ŷ
```

**Example:**
```python
import numpy as np

y_actual = np.array([1, 2, 3, 4, 5])
y_predicted = np.array([1.1, 1.9, 3.2, 3.8, 5.1])

residuals = y_actual - y_predicted
print(f"Residuals: {residuals}")  # [-0.1, 0.1, -0.2, 0.2, -0.1]
print(f"Mean residual: {residuals.mean():.4f}")  # ≈ 0
```

**Properties of good residuals:**
- Mean ≈ 0
- No obvious patterns
- Approximately normally distributed
- Constant variance (homoscedasticity)

**Related Terms:** Error, RSS, R-squared, Homoscedasticity

#### Residual Sum of Squares (RSS)
**Definition:** The sum of squared differences between actual and predicted values. Represents the unexplained variance — the error that the model couldn't capture.

**Formula:**
```
RSS = Σ(yᵢ - ŷᵢ)²
```

**Example:**
```python
import numpy as np

y_actual = np.array([1, 2, 3, 4, 5])
y_predicted = np.array([1.1, 1.9, 3.2, 3.8, 5.1])

rss = np.sum((y_actual - y_predicted) ** 2)
print(f"RSS: {rss:.4f}")  # 0.10
```

**Related Terms:** TSS, ESS, R-squared, MSE

---

### T

#### Total Sum of Squares (TSS)
**Definition:** The total variance in the target variable — the sum of squared differences between actual values and the mean. Represents the baseline variance that any model should try to explain.

**Formula:**
```
TSS = Σ(yᵢ - ȳ)²
```

**Example:**
```python
import numpy as np

y = np.array([1, 2, 3, 4, 5])
y_mean = y.mean()

tss = np.sum((y - y_mean) ** 2)
print(f"Mean: {y_mean:.2f}")
print(f"TSS: {tss:.4f}")  # 10.0
```

**Related Terms:** RSS, ESS, R-squared, Variance

#### Training R-squared
**Definition:** R² calculated on the training data. Can be misleadingly high if the model overfits.

**Example:**
```python
model = LinearRegression()
model.fit(X_train, y_train)

train_r2 = model.score(X_train, y_train)
test_r2 = model.score(X_test, y_test)

print(f"Training R²: {train_r2:.4f}")  # Often higher
print(f"Testing R²:  {test_r2:.4f}")  # More realistic
if train_r2 - test_r2 > 0.1:
    print("Warning: Possible overfitting!")
```

**Related Terms:** Testing R-squared, Overfitting, Generalization

---

### V

#### Variance
**Definition:** A measure of how spread out data values are from their mean. In the context of R², it refers to the spread of the target variable.

**Formula:**
```
Variance = (1/n) × Σ(yᵢ - ȳ)²
```

**Example:**
```python
import numpy as np

y = np.array([1, 2, 3, 4, 5])
variance = np.var(y)
std = np.std(y)

print(f"Variance: {variance:.4f}")  # 2.0
print(f"Std Dev: {std:.4f}")  # 1.4142
```

**Related Terms:** Standard Deviation, TSS, R-squared

---

## Key Formulas

| Formula | Expression | Description |
|---------|-----------|-------------|
| R² | `1 - RSS/TSS` | Proportion of variance explained |
| Adjusted R² | `1 - (1-R²)(n-1)/(n-p-1)` | Penalizes for features |
| TSS | `Σ(y - ȳ)²` | Total variance |
| RSS | `Σ(y - ŷ)²` | Unexplained variance |
| ESS | `Σ(ŷ - ȳ)²` | Explained variance |
| Residual | `y - ŷ` | Prediction error |
| MSE | `(1/n) × RSS` | Average squared error |
| RMSE | `√MSE` | Error in original units |

---

## Python Import Cheat Sheet

```python
# R-squared and metrics
from sklearn.metrics import r2_score, mean_squared_error, mean_absolute_error
from sklearn.metrics import explained_variance_score

# Linear Regression (has .score() method)
from sklearn.linear_model import LinearRegression

# Train/test split
from sklearn.model_selection import train_test_split

# Model workflow
model = LinearRegression()
model.fit(X_train, y_train)

# Method 1: model.score()
r2 = model.score(X_test, y_test)

# Method 2: r2_score()
y_pred = model.predict(X_test)
r2 = r2_score(y_test, y_pred)

# Adjusted R²
n = len(X_test)
p = X_test.shape[1]
adj_r2 = 1 - (1 - r2) * (n - 1) / (n - p - 1)
```
