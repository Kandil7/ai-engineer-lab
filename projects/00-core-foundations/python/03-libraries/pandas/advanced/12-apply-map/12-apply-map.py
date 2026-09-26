"""
Pandas Apply & Map: apply, map, applymap, pipe
================================================

Custom transformations and function application in pandas.
"""

import pandas as pd
import numpy as np

np.random.seed(42)

# =============================================================================
# 1. CREATE SAMPLE DATA
# =============================================================================

df = pd.DataFrame(
    {
        "A": [1, 2, 3, 4, 5],
        "B": [10.5, 20.3, 30.1, 40.7, 50.9],
        "C": ["apple", "banana", "cherry", "date", "elderberry"],
        "D": pd.date_range("2023-01-01", periods=5),
        "E": [True, False, True, False, True],
    }
)

print("Sample DataFrame:")
print(df)
print(f"Dtypes:\n{df.dtypes}")
print()

# =============================================================================
# 2. MAP - SERIES ONLY
# =============================================================================

print("=" * 60)
print("2. MAP - SERIES TRANSFORMATION")
print("=" * 60)

# Map with dict (ASCII-safe labels: emoji are not printable on Windows cp1252)
fruit_map = {
    "apple": "APPLE",
    "banana": "BANANA",
    "cherry": "CHERRY",
    "date": "DATE",
    "elderberry": "BERRY",
}
df["C_emoji"] = df["C"].map(fruit_map)
print("Map with dict:")
print(df[["C", "C_emoji"]])
print()

# Map with function
df["A_squared"] = df["A"].map(lambda x: x**2)
print("Map with lambda:")
print(df[["A", "A_squared"]])
print()

# Map with Series (index alignment)
mapper = pd.Series(["X", "Y", "Z"], index=[1, 3, 5])
df["A_mapped"] = df["A"].map(mapper)
print("Map with Series (index alignment):")
print(df[["A", "A_mapped"]])
print()

# Map with NaN handling
df["A_mapped_filled"] = df["A"].map(mapper).fillna("default")
print("Map with fillna:")
print(df[["A", "A_mapped_filled"]])
print()

# =============================================================================
# 3. APPLY - SERIES & DATAFRAME
# =============================================================================

print("=" * 60)
print("3. APPLY - FLEXIBLE TRANSFORMATION")
print("=" * 60)

# Series apply
print("Series apply:")
print(df["A"].apply(lambda x: x * 2))
print()

print(df["C"].apply(len))
print()

# DataFrame apply - column-wise (axis=0 default)
print("DataFrame apply (axis=0 - columns):")
print(df.apply(lambda col: col.mean() if col.dtype in ["int64", "float64"] else "non-numeric"))
print()

# DataFrame apply - row-wise (axis=1)
print("DataFrame apply (axis=1 - rows):")
row_result = df.apply(lambda row: f"{row['C']}_{row['A']}", axis=1)
print(row_result)
print()


# Apply with multiple return values (returns DataFrame)
def describe_col(col):
    if col.dtype in ["int64", "float64"]:
        return pd.Series({"mean": col.mean(), "std": col.std(), "min": col.min(), "max": col.max()})
    return pd.Series({"type": str(col.dtype)})


print("Apply returning Series (expands to DataFrame):")
print(df.apply(describe_col))
print()


# Apply with args/kwargs
def multiply_add(x, mult, add):
    return x * mult + add


print("Apply with args:")
# NOTE: apply(func, args=..., **kwds) — there is no 'kwargs=' parameter;
# keyword arguments are passed directly (apply(..., add=10))
print(df["A"].apply(multiply_add, args=(2,), add=10))
print()

# =============================================================================
# 4. APPLYMAP - ELEMENTWISE (DATAFRAME ONLY)
# =============================================================================

print("=" * 60)
print("4. APPLYMAP - ELEMENTWISE")
print("=" * 60)

# Create numeric DataFrame for applymap
num_df = pd.DataFrame(
    {"X": [1.234, 2.345, 3.456], "Y": [4.567, 5.678, 6.789], "Z": [7.890, 8.901, 9.012]}
)
print("Numeric DataFrame:")
print(num_df)
print()

# Element-wise: DataFrame.map (applymap was removed in pandas 3)
rounded = num_df.map(lambda x: round(x, 1))
print("Map round to 1 decimal:")
print(rounded)
print()

# Format all numbers
formatted = num_df.map(lambda x: f"{x:.2f}")
print("Map format as string:")
print(formatted)
print()


# Conditional formatting
def highlight(x):
    if x > 5:
        return f"**{x:.2f}**"
    return f"{x:.2f}"


highlighted = num_df.map(highlight)
print("Map with conditional:")
print(highlighted)
print()

# =============================================================================
# 5. PIPE - METHOD CHAINING
# =============================================================================

print("=" * 60)
print("5. PIPE - METHOD CHAINING")
print("=" * 60)


# Functions for piping
def clean_data(df):
    """Remove rows with any NaN."""
    return df.dropna()


def add_features(df):
    """Add computed columns."""
    df = df.copy()
    if "A" in df.columns and "B" in df.columns:
        df["A_plus_B"] = df["A"] + df["B"]
        df["A_times_B"] = df["A"] * df["B"]
    return df


def filter_data(df, threshold=100):
    """Filter rows where A_plus_B > threshold."""
    if "A_plus_B" in df.columns:
        return df[df["A_plus_B"] > threshold]
    return df


def summarize(df):
    """Return summary stats."""
    return df.describe()


# Method chaining with pipe
result = df.pipe(clean_data).pipe(add_features).pipe(filter_data, threshold=50).pipe(summarize)

print("Pipe chain result:")
print(result)
print()


# Pipe with function that returns different type
def to_csv_string(df):
    return df.to_csv(index=False)


csv_str = df.pipe(clean_data).pipe(add_features).pipe(to_csv_string)
print("Pipe to CSV string:")
print(csv_str[:200] + "...")
print()

# =============================================================================
# 6. AGG & TRANSFORM WITH CUSTOM FUNCTIONS
# =============================================================================

print("=" * 60)
print("6. AGG & TRANSFORM")
print("=" * 60)

# Create grouped data
group_df = pd.DataFrame(
    {
        "group": ["A", "A", "A", "B", "B", "B", "C", "C"],
        "value": [1, 2, 3, 4, 5, 6, 7, 8],
        "value2": [10, 20, 30, 40, 50, 60, 70, 80],
    }
)

print("Group DataFrame:")
print(group_df)
print()

# agg - aggregation (reduces)
print("GroupBy agg with custom:")
custom_agg = group_df.groupby("group").agg(
    mean_val=("value", "mean"),
    sum_val2=("value2", "sum"),
    range_val=("value", lambda x: x.max() - x.min()),
)
print(custom_agg)
print()

# transform - same shape as input
print("GroupBy transform (same shape):")
group_df["group_mean"] = group_df.groupby("group")["value"].transform("mean")
group_df["value_centered"] = group_df.groupby("group")["value"].transform(lambda x: x - x.mean())
print(group_df)
print()

# filter - subset groups
print("GroupBy filter (keep groups with mean > 3):")
filtered = group_df.groupby("group").filter(lambda x: x["value"].mean() > 3)
print(filtered)
print()

# =============================================================================
# 7. VECTORIZED ALTERNATIVES (FASTER)
# =============================================================================

print("=" * 60)
print("7. VECTORIZED ALTERNATIVES")
print("=" * 60)

# Create larger DataFrame for timing
large_df = pd.DataFrame(
    {"A": np.random.randn(100000), "B": np.random.randn(100000), "C": np.random.randn(100000)}
)

import time

# apply (slow)
start = time.time()
result_apply = large_df.apply(lambda row: row["A"] + row["B"] * row["C"], axis=1)
time_apply = time.time() - start

# vectorized (fast)
start = time.time()
result_vec = large_df["A"] + large_df["B"] * large_df["C"]
time_vec = time.time() - start

# apply on Series (moderate)
start = time.time()
result_series = large_df["A"].apply(lambda x: x * 2)
time_series = time.time() - start

# vectorized Series
start = time.time()
result_series_vec = large_df["A"] * 2
time_series_vec = time.time() - start

print(f"DataFrame apply(axis=1): {time_apply:.4f}s")
print(f"Vectorized: {time_vec:.4f}s")
print(f"Speedup: {time_apply / max(time_vec, 1e-6):.1f}x")
print()
print(f"Series apply: {time_series:.4f}s")
print(f"Series vectorized: {time_series_vec:.4f}s")
print(f"Speedup: {time_series / max(time_series_vec, 1e-6):.1f}x")
print()

# When to use apply:
print("USE APPLY WHEN:")
print("  - Complex logic not expressible with vectorized ops")
print("  - Multiple columns need to interact row-wise")
print("  - Calling external libraries (e.g., scipy, custom functions)")
print("  - Prototyping before optimizing")
print()
print("USE VECTORIZED WHEN:")
print("  - Simple arithmetic, comparisons, boolean ops")
print("  - String operations (use .str accessor)")
print("  - DateTime operations (use .dt accessor)")
print("  - GroupBy aggregations (use built-in agg funcs)")

print("\n" + "=" * 60)
print("END OF APPLY & MAP")
print("=" * 60)
