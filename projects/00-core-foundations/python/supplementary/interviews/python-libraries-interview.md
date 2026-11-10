# Python Libraries Interview Guide

> Comprehensive interview preparation for NumPy, Pandas, Matplotlib, and SciPy.  
> Covers core operations, data manipulation, visualization, and scientific computing.

---

## Table of Contents

1. [Topic Overview](#topic-overview)
2. [Interview Questions](#interview-questions)
3. [Coding Challenges](#coding-challenges)
4. [Follow-Up Questions](#follow-up-questions)
5. [Tips for Answering](#tips-for-answering)

---

## Topic Overview

Python's data science ecosystem consists of powerful libraries that work together to handle numerical computation, data manipulation, visualization, and scientific computing.

### Library Comparison

| Library | Primary Use | Key Data Structure | Typical Operations |
|---------|------------|-------------------|-------------------|
| NumPy | Numerical computation | ndarray | Array math, linear algebra, FFT |
| Pandas | Data manipulation | DataFrame | Data wrangling, cleaning, aggregation |
| Matplotlib | Visualization | Figure/Axes | Charts, plots, graphs |
| SciPy | Scientific computing | Sparse matrices | Statistics, optimization, signal processing |
| Scikit-learn | Machine learning | Estimator | Classification, regression, clustering |

### When to Use What

| Task | Library | Example |
|------|---------|---------|
| Matrix multiplication | NumPy | `np.dot(A, B)` |
| Reading CSV files | Pandas | `pd.read_csv('data.csv')` |
| Creating bar charts | Matplotlib | `plt.bar(x, y)` |
| Statistical tests | SciPy | `scipy.stats.ttest_ind(a, b)` |
| Building ML models | Scikit-learn | `model.fit(X, y)` |

---

## Interview Questions

### NumPy Operations

**Q1: What is a NumPy ndarray and why is it faster than Python lists?** 🟢

**Answer:**
NumPy arrays (ndarray) are homogeneous, fixed-size arrays that provide faster operations due to:

```python
import numpy as np
import time

# Python list operations
python_list = list(range(1000000))
start = time.time()
result_list = [x * 2 for x in python_list]
print(f"Python list: {time.time() - start:.4f}s")

# NumPy array operations
np_array = np.arange(1000000)
start = time.time()
result_array = np_array * 2
print(f"NumPy array: {time.time() - start:.4f}s")
# NumPy is typically 10-100x faster
```

**Why NumPy is faster:**
1. **Homogeneous data**: All elements same type (vs Python lists can mix types)
2. **Contiguous memory**: Elements stored in continuous memory block
3. **Vectorized operations**: Operations applied to entire array at once (C implementation)
4. **No type checking**: No runtime type checking overhead

**Key differences:**

| Aspect | Python List | NumPy Array |
|--------|-------------|-------------|
| Data type | Mixed types | Single type |
| Memory | Pointer array + objects | Contiguous block |
| Operations | Element-by-element | Vectorized (C loops) |
| Size | Dynamic | Fixed at creation |

---

**Q2: Explain array broadcasting in NumPy.** 🟡

**Answer:**
Broadcasting allows operations between arrays of different shapes:

```python
import numpy as np

# Scalar operations (broadcasting scalar to array)
arr = np.array([1, 2, 3, 4, 5])
result = arr * 3  # [3, 6, 9, 12, 15]

# Array + scalar
matrix = np.array([[1, 2, 3], [4, 5, 6]])
result = matrix + 10  # Each element + 10

# 2D + 1D broadcasting
matrix = np.array([[1, 2, 3], [4, 5, 6]])  # Shape: (2, 3)
vector = np.array([10, 20, 30])  # Shape: (3,)
result = matrix + vector
# Result:
# [[11, 22, 33],
#  [14, 25, 36]]

# Broadcasting rules:
# 1. Arrays with different ndim: prepend 1s to smaller shape
# 2. Size 1 dimensions stretch to match other array
# 3. Incompatible shapes (neither 1 nor same) → error
```

**Visual example:**
```python
# Matrix (2, 3) + Vector (3,) → (2, 3)
#   [[1, 2, 3],       [10, 20, 30]
#    [4, 5, 6]]   +   [10, 20, 30]  # vector broadcasts across rows
#
# Result:
#   [[11, 22, 33],
#    [14, 25, 36]]
```

---

**Q3: How do you index and slice NumPy arrays?** 🟢

**Answer:**
```python
import numpy as np

arr = np.array([[1, 2, 3, 4], [5, 6, 7, 8], [9, 10, 11, 12]])

# Single element
arr[0, 0]  # 1

# Row slicing
arr[0]  # First row: [1, 2, 3, 4]
arr[0, :]  # Same as above

# Column slicing
arr[:, 0]  # First column: [1, 5, 9]

# Submatrix
arr[0:2, 1:3]  # First 2 rows, columns 1-2
# [[2, 3],
#  [6, 7]]

# Boolean indexing
mask = arr > 5
arr[mask]  # [6, 7, 8, 9, 10, 11, 12]

# Fancy indexing
arr[[0, 2], [1, 3]]  # Elements at (0,1) and (2,3): [2, 12]

# Conditional selection
arr[arr % 2 == 0]  # All even numbers
```

---

**Q4: What are common NumPy array operations?** 🟢

**Answer:**
```python
import numpy as np

arr = np.array([1, 2, 3, 4, 5])

# Basic operations
arr + 10  # Add scalar
arr * 2  # Multiply scalar
arr**2  # Square each element
np.sqrt(arr)  # Square root
np.log(arr)  # Natural log

# Aggregation
np.sum(arr)  # Sum
np.mean(arr)  # Mean
np.std(arr)  # Standard deviation
np.min(arr)  # Minimum
np.max(arr)  # Maximum
np.argmin(arr)  # Index of minimum
np.argmax(arr)  # Index of maximum

# Matrix operations
A = np.array([[1, 2], [3, 4]])
B = np.array([[5, 6], [7, 8]])

np.dot(A, B)  # Matrix multiplication
A @ B  # Same as dot
A.T  # Transpose
np.linalg.inv(A)  # Inverse
np.linalg.det(A)  # Determinant

# Array manipulation
arr.reshape(5, 1)  # Reshape
arr.flatten()  # Flatten to 1D
np.concatenate([A, B])  # Concatenate
np.split(arr, 3)  # Split array
np.unique(arr)  # Unique values
np.sort(arr)  # Sort
```

---

**Q5: How do you create NumPy arrays from different sources?** 🟢

**Answer:**
```python
import numpy as np

# From Python list
arr1 = np.array([1, 2, 3, 4, 5])
arr2d = np.array([[1, 2, 3], [4, 5, 6]])

# From file
arr = np.loadtxt("data.txt", delimiter=",")
arr = np.genfromtxt("data.csv", delimiter=",", skip_header=1)

# Special arrays
np.zeros((3, 4))  # 3x4 array of zeros
np.ones((3, 4))  # 3x4 array of ones
np.full((3, 4), 7)  # 3x4 array filled with 7
np.eye(3)  # 3x3 identity matrix

# Sequence arrays
np.arange(0, 10, 2)  # [0, 2, 4, 6, 8]
np.linspace(0, 1, 5)  # [0, 0.25, 0.5, 0.75, 1.0]

# Random arrays
np.random.rand(3, 4)  # Uniform [0, 1)
np.random.randn(3, 4)  # Standard normal
np.random.randint(0, 10, (3, 4))  # Random integers
np.random.choice(arr, size=3)  # Random sample
np.random.seed(42)  # For reproducibility

# From existing data
arr = np.fromiter((x**2 for x in range(10)), dtype=int)
```

---

**Q6: How do you handle missing values in NumPy?** 🟡

**Answer:**
```python
import numpy as np

# NumPy uses NaN for missing values (not None)
arr = np.array([1, 2, np.nan, 4, 5])

# Check for NaN
np.isnan(arr)  # [False, False, True, False, False]
np.any(np.isnan(arr))  # True

# Replace NaN
np.nan_to_num(arr, nan=0)  # Replace NaN with 0

# Aggregations with NaN
np.nanmean(arr)  # Mean ignoring NaN
np.nansum(arr)  # Sum ignoring NaN
np.nanstd(arr)  # Std ignoring NaN
np.nanmin(arr)  # Min ignoring NaN

# Mask NaN values
valid_mask = ~np.isnan(arr)
valid_values = arr[valid_mask]

# For 2D arrays
matrix = np.array([[1, np.nan], [3, 4]])
np.nanmean(matrix, axis=0)  # Column means (ignore NaN)
np.nanmean(matrix, axis=1)  # Row means (ignore NaN)
```

---

### Pandas Data Manipulation

**Q7: Explain the difference between Series and DataFrame.** 🟢

**Answer:**
```python
import pandas as pd

# Series: 1D labeled array
s = pd.Series([1, 2, 3, 4], index=["a", "b", "c", "d"])
# a    1
# b    2
# c    3
# d    4

# DataFrame: 2D labeled table (dict of Series)
df = pd.DataFrame(
    {"name": ["Alice", "Bob", "Charlie"], "age": [25, 30, 35], "city": ["NYC", "LA", "Chicago"]}
)
#       name  age     city
# 0    Alice   25      NYC
# 1      Bob   30       LA
# 2  Charlie   35  Chicago

# Accessing Series elements
s["a"]  # By label
s[0]  # By position
s["a":"c"]  # Slice by label

# Accessing DataFrame elements
df["name"]  # Column as Series
df[["name", "age"]]  # Multiple columns
df.iloc[0]  # Row by position
df.loc[0]  # Row by label
```

---

**Q8: How do you filter and select data in Pandas?** 🟡

**Answer:**
```python
import pandas as pd

df = pd.DataFrame(
    {
        "name": ["Alice", "Bob", "Charlie", "David"],
        "age": [25, 30, 35, 28],
        "salary": [50000, 60000, 75000, 55000],
    }
)

# Boolean filtering
df[df["age"] > 30]  # Age > 30
df[(df["age"] > 25) & (df["salary"] > 55000)]  # Multiple conditions

# Query method
df.query("age > 30 and salary > 50000")

# loc (label-based)
df.loc[df["age"] > 30, ["name", "salary"]]

# iloc (position-based)
df.iloc[0:2, 1:3]  # First 2 rows, columns 1-2

# isin for categorical filtering
df[df["name"].isin(["Alice", "Bob"])]

# String methods
df[df["name"].str.startswith("A")]

# Between for range
df[df["age"].between(25, 30)]

# Where (keeps shape, fills with NaN)
df.where(df["age"] > 30, other=0)
```

---

**Q9: How do you handle missing data in Pandas?** 🟡

**Answer:**
```python
import pandas as pd
import numpy as np

df = pd.DataFrame({"A": [1, 2, np.nan, 4], "B": [5, np.nan, np.nan, 8], "C": [10, 11, 12, 13]})

# Check for missing values
df.isnull()  # Boolean DataFrame
df.isnull().sum()  # Count per column
df.isnull().sum().sum()  # Total missing

# Drop missing values
df.dropna()  # Drop rows with any NaN
df.dropna(axis=1)  # Drop columns with any NaN
df.dropna(thresh=2)  # Keep rows with at least 2 non-NaN

# Fill missing values
df.fillna(0)  # Fill with 0
df.fillna(df.mean())  # Fill with column mean
df.fillna(df.median())  # Fill with column median
df.fillna(method="ffill")  # Forward fill
df.fillna(method="bfill")  # Backward fill

# Interpolation
df.interpolate(method="linear")  # Linear interpolation

# Replace specific values
df.replace({np.nan: 0, -1: np.nan})

# Imputation with scikit-learn
from sklearn.impute import SimpleImputer

imputer = SimpleImputer(strategy="mean")
df_imputed = pd.DataFrame(imputer.fit_transform(df), columns=df.columns)
```

---

**Q10: How do you group and aggregate data in Pandas?** 🟡

**Answer:**
```python
import pandas as pd

sales = pd.DataFrame(
    {
        "region": ["North", "South", "North", "South", "North"],
        "product": ["A", "A", "B", "B", "A"],
        "revenue": [100, 150, 200, 120, 180],
        "units": [10, 15, 20, 12, 18],
    }
)

# Basic groupby
grouped = sales.groupby("region")
grouped["revenue"].sum()
# region
# North    480
# South    270

# Multiple aggregations
sales.groupby("region").agg({"revenue": ["sum", "mean", "max"], "units": ["sum", "count"]})

# Multiple groupby columns
sales.groupby(["region", "product"]).agg({"revenue": "sum", "units": "mean"})


# Custom aggregation functions
def revenue_range(x):
    return x.max() - x.min()


sales.groupby("region")["revenue"].agg(["sum", revenue_range])

# Transform (returns same size as input)
sales["revenue_pct"] = sales.groupby("region")["revenue"].transform(lambda x: x / x.sum() * 100)

# Filter groups
sales.groupby("region").filter(lambda x: x["revenue"].sum() > 300)


# Apply
def top_n(group, n=2):
    return group.nlargest(n, "revenue")


sales.groupby("region").apply(top_n, n=2)
```

---

**Q11: How do you merge and join DataFrames in Pandas?** 🟡

**Answer:**
```python
import pandas as pd

customers = pd.DataFrame({"customer_id": [1, 2, 3], "name": ["Alice", "Bob", "Charlie"]})

orders = pd.DataFrame(
    {"order_id": [101, 102, 103], "customer_id": [1, 2, 2], "amount": [100, 200, 150]}
)

# Inner join (only matching rows)
pd.merge(customers, orders, on="customer_id", how="inner")

# Left join (all from left, matching from right)
pd.merge(customers, orders, on="customer_id", how="left")

# Right join (all from right, matching from left)
pd.merge(customers, orders, on="customer_id", how="right")

# Outer join (all rows from both)
pd.merge(customers, orders, on="customer_id", how="outer")

# Different column names
pd.merge(customers, orders, left_on="customer_id", right_on="cust_id")

# Concatenation
df1 = pd.DataFrame({"A": [1, 2]})
df2 = pd.DataFrame({"A": [3, 4]})

pd.concat([df1, df2])  # Stack vertically
pd.concat([df1, df2], axis=1)  # Stack horizontally
pd.concat([df1, df2], ignore_index=True)  # Reset index

# Join (index-based)
df1.set_index("customer_id").join(df2.set_index("customer_id"), how="inner")
```

---

**Q12: How do you handle time series data in Pandas?** 🟡

**Answer:**
```python
import pandas as pd
import numpy as np

# Create time series
dates = pd.date_range("2024-01-01", periods=365, freq="D")
ts = pd.Series(np.random.randn(365), index=dates)

# Resampling
ts.resample("M").mean()  # Monthly mean
ts.resample("W").sum()  # Weekly sum

# Rolling windows
ts.rolling(window=7).mean()  # 7-day moving average
ts.rolling(window=30).std()  # 30-day rolling std

# Shifting (lag/lead)
ts.shift(1)  # Lag by 1 period
ts.shift(-1)  # Lead by 1 period

# Percentage change
ts.pct_change()

# Time zone handling
ts_utc = ts.tz_localize("UTC")
ts_local = ts_utc.tz_convert("US/Eastern")

# Date components
df = pd.DataFrame({"date": pd.date_range("2024-01-01", periods=10)})
df["year"] = df["date"].dt.year
df["month"] = df["date"].dt.month
df["day_name"] = df["date"].dt.day_name()
df["quarter"] = df["date"].dt.quarter

# Business day operations
pd.bdate_range("2024-01-01", periods=10)  # Business days only
```

---

### Matplotlib Visualization

**Q13: Explain the Matplotlib object hierarchy.** 🟢

**Answer:**
```python
import matplotlib.pyplot as plt

# Figure: The entire canvas
fig = plt.figure(figsize=(10, 6))

# Axes: Individual plot areas
ax1 = fig.add_subplot(2, 2, 1)  # 2x2 grid, position 1
ax2 = fig.add_subplot(2, 2, 2)  # 2x2 grid, position 2

# Artists: Lines, labels, titles, etc.
ax1.plot([1, 2, 3], [1, 4, 9], label="Line 1")
ax1.set_title("Plot 1")
ax1.set_xlabel("X-axis")
ax1.set_ylabel("Y-axis")
ax1.legend()

# Pyplot interface (simpler, state-based)
plt.figure(figsize=(10, 6))
plt.plot([1, 2, 3], [1, 4, 9])
plt.title("Simple Plot")
plt.show()

# Object-oriented approach (recommended)
fig, axes = plt.subplots(2, 2, figsize=(10, 8))

axes[0, 0].plot([1, 2, 3], [1, 4, 9])
axes[0, 0].set_title("Line Plot")

axes[0, 1].bar(["A", "B", "C"], [3, 7, 5])
axes[0, 1].set_title("Bar Plot")

axes[1, 0].scatter([1, 2, 3, 4], [1, 4, 2, 3])
axes[1, 0].set_title("Scatter Plot")

axes[1, 1].hist([1, 2, 2, 3, 3, 3, 4, 4, 4, 4])
axes[1, 1].set_title("Histogram")

plt.tight_layout()
plt.show()
```

---

**Q14: How do you create different types of plots?** 🟡

**Answer:**
```python
import matplotlib.pyplot as plt
import numpy as np

# Line plot
x = np.linspace(0, 10, 100)
plt.figure(figsize=(10, 6))
plt.plot(x, np.sin(x), label="sin(x)")
plt.plot(x, np.cos(x), label="cos(x)")
plt.title("Trigonometric Functions")
plt.xlabel("x")
plt.ylabel("y")
plt.legend()
plt.grid(True)
plt.show()

# Bar chart
categories = ["A", "B", "C", "D"]
values = [23, 45, 56, 78]
plt.bar(categories, values, color=["red", "blue", "green", "orange"])
plt.title("Bar Chart")
plt.show()

# Histogram
data = np.random.randn(1000)
plt.hist(data, bins=30, edgecolor="black", alpha=0.7)
plt.title("Histogram")
plt.xlabel("Value")
plt.ylabel("Frequency")
plt.show()

# Scatter plot
x = np.random.randn(100)
y = x * 2 + np.random.randn(100) * 0.5
colors = np.random.rand(100)
sizes = np.random.rand(100) * 100
plt.scatter(x, y, c=colors, s=sizes, alpha=0.6)
plt.title("Scatter Plot")
plt.show()

# Pie chart
sizes = [30, 25, 25, 20]
labels = ["A", "B", "C", "D"]
plt.pie(sizes, labels=labels, autopct="%1.1f%%")
plt.title("Pie Chart")
plt.show()

# Box plot
data = [np.random.randn(100) + i for i in range(5)]
plt.boxplot(data)
plt.title("Box Plot")
plt.show()
```

---

**Q15: How do you customize plot appearance?** 🟡

**Answer:**
```python
import matplotlib.pyplot as plt
import numpy as np

# Set style
plt.style.use("seaborn-v0_8")  # or 'ggplot', 'darkgrid', etc.

# Figure size and DPI
fig, ax = plt.subplots(figsize=(10, 6), dpi=100)

# Colors
ax.plot([1, 2, 3], [1, 4, 9], color="#FF5733", linewidth=2, linestyle="--")

# Markers
ax.scatter([1, 2, 3], [1, 4, 9], marker="o", s=100, c="green", alpha=0.7)

# Labels and titles
ax.set_title("Custom Plot", fontsize=16, fontweight="bold", pad=20)
ax.set_xlabel("X Axis", fontsize=12)
ax.set_ylabel("Y Axis", fontsize=12)

# Ticks
ax.set_xticks([0, 1, 2, 3])
ax.set_xticklabels(["Zero", "One", "Two", "Three"], rotation=45)
ax.tick_params(axis="both", which="major", labelsize=10)

# Grid
ax.grid(True, linestyle="--", alpha=0.7)

# Legend
ax.legend(["Line 1"], loc="upper left", fontsize=10)

# Annotations
ax.annotate("Peak", xy=(2, 4), xytext=(2.5, 3), arrowprops=dict(arrowstyle="->", color="red"))

# Limits
ax.set_xlim(0, 3)
ax.set_ylim(0, 10)

# Spines
ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)

plt.tight_layout()
plt.savefig("custom_plot.png", dpi=300, bbox_inches="tight")
plt.show()
```

---

### SciPy Scientific Computing

**Q16: What is SciPy and when would you use it?** 🟡

**Answer:**
SciPy builds on NumPy to provide scientific computing tools:

```python
import scipy.stats as stats
import scipy.optimize as optimize
import scipy.interpolate as interpolate
import scipy.signal as signal
from scipy.sparse import csr_matrix

# 1. Statistics
data = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

# Descriptive statistics
stats.describe(data)

# Hypothesis testing
group1 = [1, 2, 3, 4, 5]
group2 = [6, 7, 8, 9, 10]
t_stat, p_value = stats.ttest_ind(group1, group2)

# Probability distributions
normal = stats.norm(loc=0, scale=1)
normal.pdf(0)  # Probability density
normal.cdf(0)  # Cumulative distribution
normal.rvs(size=5)  # Random samples

# Confidence interval
ci = stats.norm.interval(0.95, loc=50, scale=10)


# 2. Optimization
def objective(x):
    return (x - 3) ** 2


result = optimize.minimize(objective, x0=0)
print(f"Minimum at x = {result.x[0]:.4f}")

# 3. Interpolation
x = np.array([0, 1, 2, 3, 4])
y = np.array([0, 1, 4, 9, 16])
f = interpolate.interp1d(x, y, kind="cubic")
x_new = np.linspace(0, 4, 100)
y_new = f(x_new)

# 4. Signal processing
from scipy import signal

# Design a low-pass filter
b, a = signal.butter(4, 0.1)  # 4th order, cutoff 0.1
filtered = signal.filtfilt(b, a, noisy_signal)
```

**When to use SciPy:**

| Task | SciPy Module | Example |
|------|--------------|---------|
| Statistical tests | `scipy.stats` | t-test, chi-square |
| Optimization | `scipy.optimize` | Minimize functions |
| Integration | `scipy.integrate` | Numerical integration |
| Interpolation | `scipy.interpolate` | Fit curves to data |
| Signal processing | `scipy.signal` | Filter signals |
| Linear algebra | `scipy.linalg` | Advanced matrix operations |
| Sparse matrices | `scipy.sparse` | Large sparse data |

---

**Q17: How do you perform statistical tests with SciPy?** 🟡

**Answer:**
```python
import scipy.stats as stats
import numpy as np

# 1. T-test (compare two groups)
group1 = np.random.normal(100, 15, 50)
group2 = np.random.normal(110, 15, 50)

# Independent samples t-test
t_stat, p_value = stats.ttest_ind(group1, group2)
print(f"t-statistic: {t_stat:.4f}")
print(f"p-value: {p_value:.4f}")
print(f"Significant: {p_value < 0.05}")

# Paired t-test (before/after)
before = np.random.normal(100, 15, 50)
after = before + np.random.normal(5, 5, 50)
t_stat, p_value = stats.ttest_rel(before, after)

# 2. Chi-square test (categorical data)
observed = np.array([[10, 20], [30, 40]])
chi2, p_value, dof, expected = stats.chi2_contingency(observed)

# 3. ANOVA (compare multiple groups)
group1 = np.random.normal(100, 15, 50)
group2 = np.random.normal(110, 15, 50)
group3 = np.random.normal(120, 15, 50)
f_stat, p_value = stats.f_oneway(group1, group2, group3)

# 4. Correlation
x = np.random.randn(100)
y = x * 2 + np.random.randn(100) * 0.5
corr, p_value = stats.pearsonr(x, y)  # Pearson correlation
spearman_corr, p_value = stats.spearmanr(x, y)  # Spearman

# 5. Normality test
stat, p_value = stats.shapiro(data)  # Shapiro-Wilk
stat, p_value = stats.normaltest(data)  # D'Angostino-Pearson

# 6. Mann-Whitney U test (non-parametric)
stat, p_value = stats.mannwhitneyu(group1, group2)

# Decision framework
if p_value < 0.05:
    print("Reject null hypothesis")
else:
    print("Fail to reject null hypothesis")
```

---

**Q18: Explain sparse matrices and when to use them.** 🟡

**Answer:**
Sparse matrices store only non-zero values, saving memory for sparse data:

```python
import numpy as np
from scipy.sparse import csr_matrix, lil_matrix, save_npz, load_npz

# Dense matrix (stores all values)
dense = np.array([[0, 0, 3, 0], [0, 0, 0, 0], [0, 0, 0, 4], [0, 5, 0, 0]])

# Sparse matrix (stores only non-zero)
sparse = csr_matrix(dense)
print(sparse)
# (0, 2) 3
# (2, 3) 4
# (3, 1) 5

# Memory comparison
print(f"Dense: {dense.nbytes} bytes")
print(f"Sparse: {data.nbytes + indices.nbytes + indptr.nbytes} bytes")

# Convert back to dense
dense_back = sparse.toarray()

# Create sparse matrices
# From COO format (coordinate)
from scipy.sparse import coo_matrix

row = [0, 0, 2, 3]
col = [2, 3, 3, 1]
data = [3, 4, 4, 5]
sparse = coo_matrix((data, (row, col)), shape=(4, 4))

# From diagonal
from scipy.sparse import diags

diagonal = [1, 2, 3, 4]
sparse = diags(diagonal)

# Operations
sparse + sparse  # Addition
sparse.dot(vector)  # Matrix-vector multiplication

# Save and load
save_npz("sparse_matrix.npz", sparse)
loaded = load_npz("sparse_matrix.npz")
```

**When to use:**

| Use Case | Example |
|----------|---------|
| Text data (TF-IDF) | Document-term matrices |
| Recommendation systems | User-item interaction matrices |
| Graph adjacency matrices | Social networks |
| Image processing | Masks, kernels |
| ML with many features | One-hot encoded categorical data |

---

## Coding Challenges

### Challenge 1: Data Cleaning Pipeline 🟡

**Problem:** Build a comprehensive data cleaning function.

```python
"""
Build a data cleaning function that:
1. Handles missing values
2. Removes duplicates
3. Fixes data types
4. Handles outliers
5. Validates data quality
"""

import pandas as pd
import numpy as np


def clean_dataset(df, target_column=None):
    """Comprehensive data cleaning"""
    df_clean = df.copy()

    # 1. Remove duplicates
    initial_rows = len(df_clean)
    df_clean = df_clean.drop_duplicates()
    print(f"Removed {initial_rows - len(df_clean)} duplicates")

    # 2. Handle missing values
    for col in df_clean.columns:
        missing_pct = df_clean[col].isnull().mean()

        if missing_pct > 0.5:
            # Drop column if >50% missing
            df_clean = df_clean.drop(columns=[col])
            print(f"Dropped {col}: {missing_pct:.1%} missing")
        elif missing_pct > 0:
            if df_clean[col].dtype in ["int64", "float64"]:
                # Fill numerical with median
                df_clean[col] = df_clean[col].fillna(df_clean[col].median())
            else:
                # Fill categorical with mode
                df_clean[col] = df_clean[col].fillna(df_clean[col].mode()[0])
            print(f"Imputed {col}: {missing_pct:.1%} missing")

    # 3. Fix data types
    for col in df_clean.columns:
        # Try to convert to numeric
        if df_clean[col].dtype == "object":
            try:
                df_clean[col] = pd.to_numeric(df_clean[col])
                print(f"Converted {col} to numeric")
            except (ValueError, TypeError):
                pass

    # 4. Handle outliers (IQR method)
    numerical_cols = df_clean.select_dtypes(include=[np.number]).columns
    for col in numerical_cols:
        if col == target_column:
            continue

        Q1 = df_clean[col].quantile(0.25)
        Q3 = df_clean[col].quantile(0.75)
        IQR = Q3 - Q1
        lower = Q1 - 1.5 * IQR
        upper = Q3 + 1.5 * IQR

        outliers = ((df_clean[col] < lower) | (df_clean[col] > upper)).sum()
        if outliers > 0:
            df_clean[col] = df_clean[col].clip(lower, upper)
            print(f"Clipped {outliers} outliers in {col}")

    # 5. Data quality report
    print("\n=== Data Quality Report ===")
    print(f"Shape: {df_clean.shape}")
    print(f"Missing values: {df_clean.isnull().sum().sum()}")
    print(f"Duplicates: {df_clean.duplicated().sum()}")

    return df_clean


# Usage
df = pd.read_csv("data.csv")
df_clean = clean_dataset(df, target_column="price")
```

---

### Challenge 2: Exploratory Data Analysis 🟡

**Problem:** Create a comprehensive EDA function.

```python
"""
Build an EDA function that:
1. Shows data overview
2. Analyzes distributions
3. Detects correlations
4. Identifies patterns
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns


def comprehensive_eda(df, target_column=None):
    """Complete Exploratory Data Analysis"""

    print("=" * 60)
    print("DATASET OVERVIEW")
    print("=" * 60)
    print(f"Shape: {df.shape}")
    print(f"\nData Types:\n{df.dtypes.value_counts()}")
    print(f"\nMemory Usage: {df.memory_usage(deep=True).sum() / 1024**2:.2f} MB")

    print("\n" + "=" * 60)
    print("MISSING VALUES")
    print("=" * 60)
    missing = df.isnull().sum()
    missing_pct = missing / len(df) * 100
    missing_df = pd.DataFrame({"Missing": missing, "Percentage": missing_pct}).sort_values(
        "Missing", ascending=False
    )
    print(missing_df[missing_df["Missing"] > 0])

    print("\n" + "=" * 60)
    print("NUMERICAL FEATURES")
    print("=" * 60)
    numerical = df.select_dtypes(include=[np.number])
    print(numerical.describe().T)

    # Distribution plots
    fig, axes = plt.subplots(len(numerical.columns), 2, figsize=(12, 4 * len(numerical.columns)))
    for i, col in enumerate(numerical.columns):
        # Histogram
        axes[i, 0].hist(df[col].dropna(), bins=30, edgecolor="black")
        axes[i, 0].set_title(f"{col} Distribution")

        # Box plot
        axes[i, 1].boxplot(df[col].dropna())
        axes[i, 1].set_title(f"{col} Box Plot")
    plt.tight_layout()
    plt.savefig("numerical_distributions.png")
    plt.show()

    print("\n" + "=" * 60)
    print("CATEGORICAL FEATURES")
    print("=" * 60)
    categorical = df.select_dtypes(include=["object", "category"])
    for col in categorical.columns:
        print(f"\n{col}:")
        print(f"  Unique values: {df[col].nunique()}")
        print(f"  Top values:\n{df[col].value_counts().head()}")

    print("\n" + "=" * 60)
    print("CORRELATIONS")
    print("=" * 60)
    if len(numerical.columns) > 1:
        corr = numerical.corr()
        plt.figure(figsize=(10, 8))
        sns.heatmap(corr, annot=True, cmap="coolwarm", center=0)
        plt.title("Correlation Matrix")
        plt.savefig("correlation_matrix.png")
        plt.show()

        # Top correlations with target
        if target_column and target_column in corr.columns:
            target_corr = corr[target_column].drop(target_column).abs().sort_values(ascending=False)
            print(f"\nTop correlations with {target_column}:")
            print(target_corr.head(10))

    return df


# Usage
df = pd.read_csv("data.csv")
comprehensive_eda(df, target_column="price")
```

---

### Challenge 3: Advanced Data Transformation 🟡

**Problem:** Build complex data transformations for feature engineering.

```python
"""
Build feature engineering functions that:
1. Creates time-based features
2. Bins continuous variables
3. Encodes categorical variables
4. Creates interaction features
"""

import pandas as pd
import numpy as np
from sklearn.preprocessing import LabelEncoder, StandardScaler


def create_time_features(df, date_column):
    """Extract time-based features"""
    df = df.copy()
    df[date_column] = pd.to_datetime(df[date_column])

    df["year"] = df[date_column].dt.year
    df["month"] = df[date_column].dt.month
    df["day"] = df[date_column].dt.day
    df["day_of_week"] = df[date_column].dt.dayofweek
    df["day_of_year"] = df[date_column].dt.dayofyear
    df["week_of_year"] = df[date_column].dt.isocalendar().week.astype(int)
    df["quarter"] = df[date_column].dt.quarter
    df["is_month_end"] = df[date_column].dt.is_month_end.astype(int)
    df["is_month_start"] = df[date_column].dt.is_month_start.astype(int)
    df["is_weekend"] = df["day_of_week"].isin([5, 6]).astype(int)

    return df


def create_binned_features(df, columns, bins=5, method="equal"):
    """Create binned versions of continuous features"""
    df = df.copy()
    for col in columns:
        if method == "equal":
            df[f"{col}_binned"] = pd.cut(df[col], bins=bins, labels=False)
        elif method == "quantile":
            df[f"{col}_binned"] = pd.qcut(df[col], q=bins, labels=False, duplicates="drop")
    return df


def create_encoded_features(df, columns, method="onehot"):
    """Encode categorical features"""
    df = df.copy()
    if method == "onehot":
        df = pd.get_dummies(df, columns=columns, drop_first=True)
    elif method == "label":
        le = LabelEncoder()
        for col in columns:
            df[f"{col}_encoded"] = le.fit_transform(df[col].astype(str))
    return df


def create_interaction_features(df, columns, operation="multiply"):
    """Create interaction features between columns"""
    df = df.copy()
    for i, col1 in enumerate(columns):
        for col2 in columns[i + 1 :]:
            if operation == "multiply":
                df[f"{col1}_x_{col2}"] = df[col1] * df[col2]
            elif operation == "divide":
                df[f"{col1}_div_{col2}"] = df[col1] / (df[col2] + 1e-8)
            elif operation == "add":
                df[f"{col1}_plus_{col2}"] = df[col1] + df[col2]
    return df


# Usage
df = pd.read_csv("data.csv")

# Apply transformations
df = create_time_features(df, "date")
df = create_binned_features(df, ["price", "quantity"], bins=5)
df = create_encoded_features(df, ["category", "region"], method="onehot")
df = create_interaction_features(df, ["price", "quantity"], operation="multiply")
```

---

### Challenge 4: Performance Optimization 🟡

**Problem:** Optimize slow Pandas operations.

```python
"""
Optimize Pandas operations by:
1. Using vectorization instead of loops
2. Choosing appropriate data types
3. Using eval() for large DataFrames
4. Chunking large file reads
"""

import pandas as pd
import numpy as np
import time


# 1. Vectorization vs Loops
def slow_approach(df):
    """Slow: row-by-row iteration"""
    results = []
    for idx, row in df.iterrows():
        if row["price"] > 100:
            results.append(row["price"] * 1.1)
        else:
            results.append(row["price"] * 1.2)
    return results


def fast_approach(df):
    """Fast: vectorized operation"""
    return np.where(df["price"] > 100, df["price"] * 1.1, df["price"] * 1.2)


# Benchmark
df = pd.DataFrame({"price": np.random.uniform(10, 200, 100000)})

start = time.time()
_ = slow_approach(df)
print(f"Loop: {time.time() - start:.4f}s")

start = time.time()
_ = fast_approach(df)
print(f"Vectorized: {time.time() - start:.4f}s")


# 2. Optimize dtypes
def optimize_dtypes(df):
    """Convert to optimal dtypes"""
    for col in df.columns:
        col_type = df[col].dtype

        if col_type == "int64":
            if df[col].min() >= 0:
                if df[col].max() < 255:
                    df[col] = df[col].astype(np.uint8)
                elif df[col].max() < 65535:
                    df[col] = df[col].astype(np.uint16)
            else:
                if df[col].min() > -128 and df[col].max() < 127:
                    df[col] = df[col].astype(np.int8)
                elif df[col].min() > -32768 and df[col].max() < 32767:
                    df[col] = df[col].astype(np.int16)

        elif col_type == "float64":
            df[col] = df[col].astype(np.float32)

        elif col_type == "object":
            num_unique = df[col].nunique()
            num_total = len(df[col])
            if num_unique / num_total < 0.5:
                df[col] = df[col].astype("category")

    return df


# 3. Use eval() for large DataFrames
def compute_with_eval(df):
    """Use eval for complex expressions"""
    return df.eval("result = (price * quantity * (1 - discount)) / (1 + tax)")


# 4. Chunked reading
def read_large_csv(filepath, chunksize=10000):
    """Read large CSV in chunks"""
    chunks = []
    for chunk in pd.read_csv(filepath, chunksize=chunksize):
        # Process each chunk
        chunk = optimize_dtypes(chunk)
        chunks.append(chunk)
    return pd.concat(chunks, ignore_index=True)
```

---

### Challenge 5: Data Validation 🟡

**Problem:** Build a data validation framework.

```python
"""
Build a data validation function that:
1. Checks data types
2. Validates value ranges
3. Checks for required columns
4. Validates constraints
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Any


class DataValidator:
    def __init__(self):
        self.errors = []
        self.warnings = []

    def validate(self, df: pd.DataFrame, schema: Dict[str, Any]) -> bool:
        """Validate DataFrame against schema"""
        self.errors = []
        self.warnings = []

        # Check required columns
        required_cols = schema.get("required_columns", [])
        for col in required_cols:
            if col not in df.columns:
                self.errors.append(f"Missing required column: {col}")

        # Check column types
        type_checks = schema.get("column_types", {})
        for col, expected_type in type_checks.items():
            if col in df.columns:
                actual_type = str(df[col].dtype)
                if expected_type not in actual_type:
                    self.warnings.append(
                        f"Column {col}: expected {expected_type}, got {actual_type}"
                    )

        # Check value ranges
        range_checks = schema.get("value_ranges", {})
        for col, (min_val, max_val) in range_checks.items():
            if col in df.columns:
                if df[col].min() < min_val:
                    self.errors.append(f"Column {col}: min value {df[col].min()} < {min_val}")
                if df[col].max() > max_val:
                    self.errors.append(f"Column {col}: max value {df[col].max()} > {max_val}")

        # Check for nulls
        null_checks = schema.get("null_allowed", {})
        for col, allowed in null_checks.items():
            if col in df.columns and not allowed:
                null_count = df[col].isnull().sum()
                if null_count > 0:
                    self.errors.append(f"Column {col}: {null_count} null values not allowed")

        # Check unique constraints
        unique_checks = schema.get("unique_columns", [])
        for col in unique_checks:
            if col in df.columns:
                if df[col].duplicated().any():
                    self.errors.append(f"Column {col}: contains duplicates")

        # Check custom constraints
        custom_checks = schema.get("custom_constraints", [])
        for check in custom_checks:
            if not check(df):
                self.errors.append(f"Custom constraint failed: {check.__name__}")

        return len(self.errors) == 0

    def report(self):
        """Print validation report"""
        print("\n=== Validation Report ===")
        if self.errors:
            print(f"\nErrors ({len(self.errors)}):")
            for error in self.errors:
                print(f"  ❌ {error}")
        else:
            print("\n✅ No errors")

        if self.warnings:
            print(f"\nWarnings ({len(self.warnings)}):")
            for warning in self.warnings:
                print(f"  ⚠️ {warning}")

        return len(self.errors) == 0


# Usage
schema = {
    "required_columns": ["id", "name", "price"],
    "column_types": {"price": "float", "quantity": "int"},
    "value_ranges": {"price": (0, 10000), "quantity": (0, 1000)},
    "null_allowed": {"id": False, "name": False},
    "unique_columns": ["id"],
    "custom_constraints": [lambda df: (df["price"] > 0).all()],
}

validator = DataValidator()
is_valid = validator.validate(df, schema)
validator.report()
```

---

### Challenge 6: Matrix Operations with NumPy 🟡

**Problem:** Implement common matrix operations.

```python
"""
Implement matrix operations:
1. Matrix multiplication
2. Eigenvalue decomposition
3. Singular Value Decomposition
4. Matrix inverse and solving linear systems
"""

import numpy as np


def matrix_operations_demo():
    """Demonstrate common matrix operations"""

    # Create matrices
    A = np.array([[1, 2], [3, 4]])
    B = np.array([[5, 6], [7, 8]])

    # 1. Matrix multiplication
    print("=== Matrix Multiplication ===")
    print(f"A @ B =\n{A @ B}")
    print(f"np.dot(A, B) =\n{np.dot(A, B)}")

    # 2. Transpose
    print(f"\nA.T =\n{A.T}")

    # 3. Determinant and Inverse
    print(f"\ndet(A) = {np.linalg.det(A):.4f}")
    print(f"inv(A) =\n{np.linalg.inv(A):.4f}")

    # 4. Solving linear systems: Ax = b
    print("\n=== Solving Linear System ===")
    b = np.array([5, 6])
    x = np.linalg.solve(A, b)
    print(f"Solution x = {x}")
    print(f"Verification Ax = {A @ x}")

    # 5. Eigenvalue decomposition
    print("\n=== Eigenvalue Decomposition ===")
    eigenvalues, eigenvectors = np.linalg.eig(A)
    print(f"Eigenvalues: {eigenvalues}")
    print(f"Eigenvectors:\n{eigenvectors}")

    # 6. Singular Value Decomposition
    print("\n=== Singular Value Decomposition ===")
    U, S, Vt = np.linalg.svd(A)
    print(f"U:\n{U}")
    print(f"Singular values: {S}")
    print(f"Vt:\n{Vt}")

    # Reconstruct matrix
    A_reconstructed = U @ np.diag(S) @ Vt
    print(f"\nReconstructed A:\n{A_reconstructed}")

    # 7. Norms
    print(f"\nFrobenius norm: {np.linalg.norm(A, 'fro'):.4f}")
    print(f"L2 norm: {np.linalg.norm(A, 2):.4f}")

    return A, B


A, B = matrix_operations_demo()
```

---

### Challenge 7: Advanced Pandas Aggregation 🟡

**Problem:** Build complex aggregation pipelines.

```python
"""
Build advanced aggregation pipeline that:
1. Groups by multiple columns
2. Applies multiple aggregation functions
3. Creates pivot tables
4. Handles hierarchical indices
"""

import pandas as pd
import numpy as np


def advanced_aggregation(df):
    """Advanced Pandas aggregation techniques"""

    # 1. Multi-column grouping with multiple aggregations
    result1 = df.groupby(["region", "product"]).agg(
        {
            "revenue": ["sum", "mean", "std", "count"],
            "units": ["sum", "mean"],
            "price": ["min", "max"],
        }
    )

    # Flatten column names
    result1.columns = ["_".join(col) for col in result1.columns]
    result1 = result1.reset_index()

    # 2. Custom aggregation with named aggregation
    result2 = (
        df.groupby("region")
        .agg(
            total_revenue=("revenue", "sum"),
            avg_order_value=("revenue", "mean"),
            order_count=("revenue", "count"),
            unique_products=("product", "nunique"),
        )
        .reset_index()
    )

    # 3. Pivot table
    pivot = pd.pivot_table(
        df,
        values="revenue",
        index="region",
        columns="product",
        aggfunc="sum",
        fill_value=0,
        margins=True,  # Add row/column totals
        margins_name="Total",
    )

    # 4. Cross-tabulation
    cross_tab = pd.crosstab(
        df["region"],
        df["product"],
        values=df["revenue"],
        aggfunc="sum",
        normalize="index",  # Row percentages
    )

    # 5. Rolling aggregations
    df_sorted = df.sort_values("date")
    df_sorted["rolling_revenue"] = df_sorted.groupby("region")["revenue"].transform(
        lambda x: x.rolling(window=7, min_periods=1).mean()
    )

    # 6. Expanding aggregations
    df_sorted["cumulative_revenue"] = df_sorted.groupby("region")["revenue"].transform(
        lambda x: x.expanding().sum()
    )

    # 7. Window functions
    df_sorted["revenue_rank"] = df_sorted.groupby("region")["revenue"].rank(
        ascending=False, method="dense"
    )

    return result1, result2, pivot, cross_tab


# Usage
df = pd.read_csv("sales_data.csv")
result1, result2, pivot, cross_tab = advanced_aggregation(df)
```

---

### Challenge 8: Matplotlib Dashboard 🟡

**Problem:** Create a multi-panel visualization dashboard.

```python
"""
Build a dashboard that:
1. Shows multiple chart types
2. Has consistent styling
3. Includes annotations
4. Saves as high-quality image
"""

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


def create_dashboard(data_dict, output_file="dashboard.png"):
    """Create a comprehensive visualization dashboard"""

    # Set style
    plt.style.use("seaborn-v0_8")
    fig = plt.figure(figsize=(16, 12))
    fig.suptitle("Sales Dashboard", fontsize=20, fontweight="bold", y=1.02)

    # Create grid
    gs = fig.add_gridspec(3, 3, hspace=0.3, wspace=0.3)

    # 1. Line chart (top left, spans 2 columns)
    ax1 = fig.add_subplot(gs[0, :2])
    months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun"]
    ax1.plot(months, data_dict["sales"], marker="o", linewidth=2, label="Sales")
    ax1.plot(months, data_dict["target"], linestyle="--", linewidth=2, label="Target")
    ax1.fill_between(months, data_dict["sales"], alpha=0.3)
    ax1.set_title("Sales vs Target")
    ax1.legend()
    ax1.grid(True, alpha=0.3)

    # 2. KPI card (top right)
    ax2 = fig.add_subplot(gs[0, 2])
    ax2.axis("off")
    total_sales = sum(data_dict["sales"])
    growth = (data_dict["sales"][-1] - data_dict["sales"][0]) / data_dict["sales"][0] * 100
    ax2.text(0.5, 0.7, f"${total_sales:,.0f}", fontsize=24, ha="center", fontweight="bold")
    ax2.text(0.5, 0.5, "Total Sales", fontsize=12, ha="center", color="gray")
    ax2.text(
        0.5,
        0.3,
        f"+{growth:.1f}%",
        fontsize=16,
        ha="center",
        color="green" if growth > 0 else "red",
    )

    # 3. Bar chart (middle left)
    ax3 = fig.add_subplot(gs[1, 0])
    categories = ["Product A", "Product B", "Product C", "Product D"]
    values = [45, 30, 15, 10]
    colors = ["#2ecc71", "#3498db", "#e74c3c", "#f39c12"]
    ax3.bar(categories, values, color=colors)
    ax3.set_title("Sales by Product")
    ax3.set_ylabel("Percentage")

    # 4. Pie chart (middle center)
    ax4 = fig.add_subplot(gs[1, 1])
    ax4.pie(values, labels=categories, autopct="%1.1f%%", colors=colors)
    ax4.set_title("Market Share")

    # 5. Box plot (middle right)
    ax5 = fig.add_subplot(gs[1, 2])
    data = [np.random.normal(100 + i * 10, 15, 50) for i in range(4)]
    ax5.boxplot(data, labels=["Q1", "Q2", "Q3", "Q4"])
    ax5.set_title("Revenue Distribution")

    # 6. Scatter plot (bottom left)
    ax6 = fig.add_subplot(gs[2, 0])
    x = np.random.randn(100)
    y = x * 2 + np.random.randn(100) * 0.5
    ax6.scatter(x, y, alpha=0.6, c=colors[0])
    ax6.set_title("Price vs Units")
    ax6.set_xlabel("Price")
    ax6.set_ylabel("Units Sold")

    # 7. Heatmap (bottom center)
    ax7 = fig.add_subplot(gs[2, 1])
    heatmap_data = np.random.rand(5, 5)
    im = ax7.imshow(heatmap_data, cmap="YlOrRd")
    ax7.set_title("Regional Performance")
    plt.colorbar(im, ax=ax7)

    # 8. Histogram (bottom right)
    ax8 = fig.add_subplot(gs[2, 2])
    ax8.hist(np.random.normal(50, 10, 1000), bins=30, edgecolor="black", alpha=0.7)
    ax8.set_title("Order Value Distribution")

    # Add footer
    fig.text(
        0.5,
        0.01,
        "Generated on 2024-01-15 | Data Source: Sales DB",
        ha="center",
        fontsize=8,
        color="gray",
    )

    plt.savefig(output_file, dpi=300, bbox_inches="tight", facecolor="white")
    plt.show()

    return fig


# Usage
data_dict = {
    "sales": [45000, 52000, 48000, 61000, 55000, 67000],
    "target": [50000, 50000, 55000, 55000, 60000, 60000],
}
create_dashboard(data_dict)
```

---

## Follow-Up Questions

### NumPy Follow-ups
1. "When would you use NumPy over pure Python?"
2. "How do you handle very large arrays that don't fit in memory?"
3. "Explain the difference between `view` and `copy` in NumPy."

### Pandas Follow-ups
1. "When would you use `apply` vs vectorized operations?"
2. "How do you handle very large CSV files?"
3. "Explain the difference between `merge`, `join`, and `concat`."

### Matplotlib Follow-ups
1. "How do you create interactive visualizations?"
2. "When would you use Seaborn over Matplotlib?"
3. "How do you customize plot fonts and colors?"

### SciPy Follow-ups
1. "When would you use SciPy instead of NumPy?"
2. "Explain the difference between `optimize.minimize` methods."
3. "How do you handle sparse matrices efficiently?"

---

## Tips for Answering

### Before the Interview

1. **Know the Basics**
   - Array vs list operations
   - DataFrame operations
   - Common visualization types
   - Basic statistical concepts

2. **Practice Common Operations**
   - Filtering and grouping
   - Merging datasets
   - Creating plots
   - Handling missing values

3. **Understand Performance**
   - Vectorization vs loops
   - Memory-efficient operations
   - When to use chunking

### During the Interview

1. **Start with the Simplest Solution**
   - Show you understand fundamentals
   - Then optimize if needed

2. **Explain Your Approach**
   - Why you chose this library
   - Why this specific function
   - What the tradeoffs are

3. **Handle Edge Cases**
   - Empty data
   - Missing values
   - Large datasets

4. **Know the Alternatives**
   - Pandas vs SQL
   - Matplotlib vs Seaborn vs Plotly
   - NumPy vs SciPy

### Common Mistakes to Avoid

1. **Using loops instead of vectorization**
   ```python
   # Wrong
   result = []
   for x in arr:
       result.append(x**2)

   # Correct
   result = arr**2
   ```

2. **Modifying original DataFrame**
   ```python
   # Wrong
   df["new_col"] = df["old_col"] * 2  # Modifies original

   # Correct
   df = df.copy()
   df["new_col"] = df["old_col"] * 2
   ```

3. **Forgetting to handle NaN**
   ```python
   # Wrong
   mean = df["col"].mean()  # May give wrong result with NaN

   # Correct
   mean = df["col"].mean()  # Pandas ignores NaN by default
   # Or explicitly: df['col'].dropna().mean()
   ```

---

## Quick Reference Card

### NumPy Essentials

```python
import numpy as np

# Array creation
arr = np.array([1, 2, 3])
zeros = np.zeros((3, 4))
ones = np.ones((3, 4))
eye = np.eye(3)
arange = np.arange(0, 10, 2)
linspace = np.linspace(0, 1, 5)

# Operations
arr + 10  # Element-wise add
arr * 2  # Element-wise multiply
np.dot(A, B)  # Matrix multiplication
arr.sum()  # Sum
arr.mean()  # Mean
arr.std()  # Standard deviation
```

### Pandas Essentials

```python
import pandas as pd

# Reading data
df = pd.read_csv("data.csv")
df = pd.read_excel("data.xlsx")
df = pd.read_json("data.json")

# Selection
df["column"]  # Column
df[["col1", "col2"]]  # Multiple columns
df.iloc[0]  # Row by position
df.loc[0]  # Row by label

# Filtering
df[df["col"] > 5]
df.query("col > 5")

# Grouping
df.groupby("col").agg({"col2": "sum"})

# Merging
pd.merge(df1, df2, on="key")
pd.concat([df1, df2])
```

### Matplotlib Essentials

```python
import matplotlib.pyplot as plt

# Basic plot
plt.plot(x, y)
plt.show()

# Object-oriented
fig, ax = plt.subplots()
ax.plot(x, y)
plt.show()

# Subplots
fig, axes = plt.subplots(2, 2)
axes[0, 0].plot(x, y)

# Saving
plt.savefig("plot.png", dpi=300, bbox_inches="tight")
```

### SciPy Essentials

```python
import scipy.stats as stats
import scipy.optimize as optimize

# Statistics
stats.ttest_ind(group1, group2)
stats.pearsonr(x, y)

# Optimization
optimize.minimize(objective, x0)

# Interpolation
from scipy.interpolate import interp1d

f = interp1d(x, y, kind="cubic")
```

---

## Additional Resources

- [NumPy Documentation](https://numpy.org/doc/)
- [Pandas Documentation](https://pandas.pydata.org/docs/)
- [Matplotlib Documentation](https://matplotlib.org/)
- [SciPy Documentation](https://docs.scipy.org/)
- [Python Data Science Handbook](https://jakevdp.github.io/PythonDataScienceHandbook/)
