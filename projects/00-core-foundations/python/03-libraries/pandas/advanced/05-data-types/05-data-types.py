"""
Pandas Data Types: astype, to_datetime, to_numeric, categories
===============================================================

Covers type conversion, optimization, and categorical data handling.
"""

import pandas as pd
import numpy as np

np.random.seed(42)
df = pd.DataFrame(
    {
        "id": range(1, 21),
        "name": [f"User_{i}" for i in range(1, 21)],
        "age_str": [str(np.random.randint(18, 70)) for _ in range(20)],
        "salary_str": [f"{np.random.randint(30000, 200000):,}" for _ in range(20)],
        "join_date_str": pd.date_range("2020-01-01", periods=20, freq="W").astype(str),
        "is_active_str": np.random.choice(["True", "False", "true", "false", "1", "0"], 20),
        "department": np.random.choice(["Eng", "Sales", "HR", "Marketing"], 20),
        "rating_str": [str(np.random.uniform(1.0, 5.0))[:4] for _ in range(20)],
        "bonus_str": ["$" + str(np.random.randint(0, 50000)) for _ in range(20)],
    }
)

print("Original DataFrame:")
print(df)
print(f"\nDtypes:\n{df.dtypes}")
print()

# =============================================================================
# 1. ASTYPE - BASIC TYPE CONVERSION
# =============================================================================

print("=" * 60)
print("1. ASTYPE - BASIC TYPE CONVERSION")
print("=" * 60)

# Convert string to int
df["age"] = df["age_str"].astype(int)
print(f"age_str -> int: {df['age'].dtype}")
print(df[["age_str", "age"]].head())
print()

# Convert string to float
df["rating"] = df["rating_str"].astype(float)
print(f"rating_str -> float: {df['rating'].dtype}")
print()

# Convert to boolean (careful with strings!)
df["is_active"] = df["is_active_str"].map(
    {"True": True, "False": False, "true": True, "false": False, "1": True, "0": False}
)
print(f"is_active_str -> bool (via map): {df['is_active'].dtype}")
print()

# Convert multiple columns at once
df[["age", "rating"]] = df[["age", "rating"]].astype({"age": "int32", "rating": "float32"})
print(f"After astype dict: age={df['age'].dtype}, rating={df['rating'].dtype}")
print()

# Convert to nullable integer (supports NaN)
# NOTE: value list must match the DataFrame length (20 rows) — pandas raises
# "Length of values (4) does not match length of index (20)" otherwise
df["age_nullable"] = pd.array([1, 2, None, 4] + [None] * 16, dtype="Int64")  # Capital I
print(f"Nullable Int64: {df['age_nullable'].dtype}")
print(df["age_nullable"])
print()

# =============================================================================
# 2. TO_NUMERIC - ROBUST NUMERIC CONVERSION
# =============================================================================

print("=" * 60)
print("2. TO_NUMERIC - ROBUST NUMERIC CONVERSION")
print("=" * 60)

# salary_str has commas: "50,000"
df["salary_clean"] = df["salary_str"].str.replace(",", "").astype(int)
print("After str.replace + astype:")
print(df[["salary_str", "salary_clean"]].head())
print()

# to_numeric with errors handling
messy_numbers = pd.Series(["1", "2", "3.5", "four", "5", "$100", "1,000", None])
print("Messy series:", messy_numbers.tolist())

# errors='coerce' -> NaN for non-numeric
numeric_coerce = pd.to_numeric(messy_numbers, errors="coerce")
print("to_numeric(errors='coerce'):", numeric_coerce.tolist())

# errors='ignore' -> return original (removed in pandas 3; emulate it)
try:
    numeric_ignore = pd.to_numeric(messy_numbers)
except (ValueError, TypeError):
    numeric_ignore = messy_numbers
print("to_numeric(errors='ignore'):", numeric_ignore.tolist())

# downcast for memory efficiency
df["salary_downcast"] = pd.to_numeric(df["salary_clean"], downcast="integer")
print(f"Downcast to: {df['salary_downcast'].dtype}")
print()

# =============================================================================
# 3. TO_DATETIME - DATE/TIME CONVERSION
# =============================================================================

print("=" * 60)
print("3. TO_DATETIME - DATE/TIME CONVERSION")
print("=" * 60)

# Basic conversion
df["join_date"] = pd.to_datetime(df["join_date_str"])
print(f"join_date dtype: {df['join_date'].dtype}")
print(df[["join_date_str", "join_date"]].head())
print()

# With format specification (faster for large datasets)
df["join_date_fmt"] = pd.to_datetime(df["join_date_str"], format="%Y-%m-%d")
print(f"With format: {df['join_date_fmt'].dtype}")
print()

# Mixed formats - infer_datetime_format (pandas 2.x needs format='mixed' for
# heterogeneous strings, then repeat the 4 parsed dates to match 20 rows)
mixed_dates = pd.Series(["2020-01-01", "01/15/2020", "2020.02.01", "Jan 3 2020"])
df["mixed_dates"] = np.tile(pd.to_datetime(mixed_dates, format="mixed"), 5)
print("Mixed formats parsed:")
print(df["mixed_dates"])
print()

# Errors handling
bad_dates = pd.Series(["2020-01-01", "not-a-date", "2020-02-30", None])  # Feb 30 invalid
print("Bad dates:", bad_dates.tolist())
print("coerce:", pd.to_datetime(bad_dates, errors="coerce").tolist())
try:
    print("ignore:", pd.to_datetime(bad_dates).tolist())
except (ValueError, TypeError):
    print("ignore:", bad_dates.tolist())  # pandas 3 removed errors='ignore'
print()

# UTC handling
df["join_date_utc"] = pd.to_datetime(df["join_date_str"], utc=True)
print(f"UTC datetime: {df['join_date_utc'].dtype}")
print()

# =============================================================================
# 4. CATEGORICAL DATA - MEMORY EFFICIENCY
# =============================================================================

print("=" * 60)
print("4. CATEGORICAL DATA")
print("=" * 60)

# Convert to category
df["department_cat"] = df["department"].astype("category")
print(f"Original: {df['department'].dtype}, Category: {df['department_cat'].dtype}")
print(f"Memory original: {df['department'].memory_usage(deep=True)} bytes")
print(f"Memory category: {df['department_cat'].memory_usage(deep=True)} bytes")
print()

# Ordered categories
rating_order = pd.CategoricalDtype(categories=[1, 2, 3, 4, 5], ordered=True)
df["rating_cat"] = df["rating"].astype(int).astype(rating_order)
print("Ordered categorical:")
print(df[["rating", "rating_cat"]].head())
print(f"Can compare: {(df['rating_cat'] > 3).sum()} ratings > 3")
print()

# Category methods
print("Categories:", df["department_cat"].cat.categories.tolist())
print("Codes:", df["department_cat"].cat.codes.tolist()[:5])
print()

# Rename categories
df["dept_renamed"] = df["department_cat"].cat.rename_categories(
    {"Eng": "Engineering", "HR": "Human Resources"}
)
print("Renamed categories:", df["dept_renamed"].cat.categories.tolist())
print()

# Add/remove categories
df["dept_new"] = df["department_cat"].cat.add_categories(["Finance", "Legal"])
print("After adding categories:", df["dept_new"].cat.categories.tolist())

df["dept_removed"] = df["dept_new"].cat.remove_categories(["Finance", "Legal"])
print("After removing:", df["dept_removed"].cat.categories.tolist())
print()

# Set categories (reorder, subset)
df["dept_ordered"] = df["department_cat"].cat.set_categories(["Eng", "Sales", "Marketing", "HR"])
print("Reordered categories:", df["dept_ordered"].cat.categories.tolist())
print()

# =============================================================================
# 5. DATETIME ACCESSORS (.dt)
# =============================================================================

print("=" * 60)
print("5. DATETIME ACCESSORS (.dt)")
print("=" * 60)

dt = df["join_date"]
print("Year:", dt.dt.year.tolist()[:5])
print("Month:", dt.dt.month.tolist()[:5])
print("Day:", dt.dt.day.tolist()[:5])
print("Day of week:", dt.dt.dayofweek.tolist()[:5])  # Monday=0
print("Day name:", dt.dt.day_name().tolist()[:5])
print("Quarter:", dt.dt.quarter.tolist()[:5])
print("Is weekend:", dt.dt.dayofweek.isin([5, 6]).tolist()[:5])
print("Days in month:", dt.dt.days_in_month.tolist()[:5])
print()

# Period conversion
df["join_period"] = dt.dt.to_period("M")
print("To period (month):", df["join_period"].head())
print()

# String formatting
print("Formatted:", dt.dt.strftime("%Y-%m-%d").head())
print()

# =============================================================================
# 6. OPTIMIZING MEMORY USAGE
# =============================================================================

print("=" * 60)
print("6. MEMORY OPTIMIZATION")
print("=" * 60)


def optimize_dtypes(df):
    """Optimize DataFrame dtypes for memory efficiency."""
    df_opt = df.copy()

    for col in df_opt.columns:
        col_type = df_opt[col].dtype

        if col_type == "object":
            # Try category for low cardinality
            if df_opt[col].nunique() / len(df_opt[col]) < 0.5:
                df_opt[col] = df_opt[col].astype("category")
        elif col_type == "int64":
            # Downcast integers
            df_opt[col] = pd.to_numeric(df_opt[col], downcast="integer")
        elif col_type == "float64":
            # Downcast floats
            df_opt[col] = pd.to_numeric(df_opt[col], downcast="float")
        elif col_type == "bool":
            pass  # Already optimal

    return df_opt


df_optimized = optimize_dtypes(df)
print("Original memory:", df.memory_usage(deep=True).sum() / 1024, "KB")
print("Optimized memory:", df_optimized.memory_usage(deep=True).sum() / 1024, "KB")
print()

# Check dtypes
print("Original dtypes:")
print(df.dtypes)
print("\nOptimized dtypes:")
print(df_optimized.dtypes)
print()

# =============================================================================
# 7. CONVERT_DTYPES - AUTOMATIC BEST PRACTICE
# =============================================================================

print("=" * 60)
print("7. CONVERT_DTYPES - AUTOMATIC CONVERSION")
print("=" * 60)

# Creates nullable types, string dtype, etc.
df_converted = df.convert_dtypes()
print("After convert_dtypes():")
print(df_converted.dtypes)
print()

# StringDtype (nullable string)
print("StringDtype example:")
s = pd.Series(["a", "b", None, "c"], dtype="string")
print(s)
print(f"Dtype: {s.dtype}")
print()

# BooleanDtype (nullable boolean)
b = pd.Series([True, False, None], dtype="boolean")
print("BooleanDtype example:")
print(b)
print(f"Dtype: {b.dtype}")
print()

print("=" * 60)
print("END OF DATA TYPES")
print("=" * 60)
