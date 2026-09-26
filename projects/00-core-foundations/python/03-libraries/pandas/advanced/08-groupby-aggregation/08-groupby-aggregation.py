"""
Pandas GroupBy & Aggregation: split-apply-combine, agg, transform, filter
===========================================================================

Comprehensive guide to pandas groupby operations for data analysis.
"""

import pandas as pd
import numpy as np

np.random.seed(42)

# Create sample data
df = pd.DataFrame(
    {
        "employee_id": range(1, 51),
        "name": [f"Emp_{i}" for i in range(1, 51)],
        "department": np.random.choice(["Engineering", "Sales", "Marketing", "HR", "Finance"], 50),
        "role": np.random.choice(
            ["Junior", "Senior", "Lead", "Manager"], 50, p=[0.4, 0.3, 0.2, 0.1]
        ),
        "age": np.random.randint(22, 60, 50),
        "salary": np.random.randint(40000, 180000, 50),
        "years_experience": np.random.randint(1, 25, 50),
        "performance_score": np.random.uniform(2.0, 5.0, 50).round(2),
        "city": np.random.choice(["NYC", "SF", "LA", "Chicago", "Austin", "Seattle", "Boston"], 50),
        "is_remote": np.random.choice([True, False], 50, p=[0.3, 0.7]),
    }
)

print("Sample DataFrame:")
print(df.head(10))
print(f"Shape: {df.shape}")
print()

# =============================================================================
# 1. BASIC GROUPBY
# =============================================================================

print("=" * 60)
print("1. BASIC GROUPBY")
print("=" * 60)

# Group by single column
dept_groups = df.groupby("department")
print("GroupBy object:", type(dept_groups))
print("Groups:", list(dept_groups.groups.keys()))
print()

# Iterate groups
print("First 2 rows of each department:")
for name, group in dept_groups:
    print(f"\n{name} ({len(group)} employees):")
    print(group[["name", "role", "salary"]].head(2))

# Get group
eng_group = dept_groups.get_group("Engineering")
print(f"\nEngineering group shape: {eng_group.shape}")
print()

# =============================================================================
# 2. AGGREGATION
# =============================================================================

print("=" * 60)
print("2. AGGREGATION")
print("=" * 60)

# Single aggregation
print("Mean salary by department:")
print(df.groupby("department")["salary"].mean().round(0))
print()

# Multiple aggregations on single column
print("Salary stats by department:")
salary_stats = df.groupby("department")["salary"].agg(
    ["mean", "median", "std", "min", "max", "count"]
)
print(salary_stats.round(0))
print()

# Multiple columns, multiple aggregations
print("Multiple columns, multiple aggregations:")
multi_agg = (
    df.groupby("department")
    .agg(
        {
            "salary": ["mean", "median", "std"],
            "age": ["mean", "min", "max"],
            "performance_score": ["mean", "std"],
            "years_experience": "mean",
        }
    )
    .round(2)
)
print(multi_agg)
print()

# Custom aggregation functions
print("Custom aggregations:")


def salary_range(x):
    return x.max() - x.min()


def top_performer_pct(x):
    return (x > 4.0).mean() * 100


custom = (
    df.groupby("department")
    .agg(
        salary_mean=("salary", "mean"),
        salary_range=("salary", salary_range),
        top_performers_pct=("performance_score", top_performer_pct),
        avg_age=("age", "mean"),
        headcount=("employee_id", "count"),
    )
    .round(2)
)
print(custom)
print()

# =============================================================================
# 3. GROUPBY WITH MULTIPLE KEYS
# =============================================================================

print("=" * 60)
print("3. MULTIPLE GROUPING KEYS")
print("=" * 60)

# Group by department AND role
print("Salary by department and role:")
dept_role = df.groupby(["department", "role"])["salary"].mean().round(0)
print(dept_role)
print()

# As DataFrame (unstack)
dept_role_df = df.groupby(["department", "role"])["salary"].mean().unstack(fill_value=0).round(0)
print("Unstacked:")
print(dept_role_df)
print()

# Multiple aggregations with multi-key
multi_key = (
    df.groupby(["department", "role"])
    .agg({"salary": ["mean", "count"], "performance_score": "mean"})
    .round(2)
)
print("Multi-key with multiple aggs:")
print(multi_key)
print()

# =============================================================================
# 4. TRANSFORM - RETURN SAME SHAPE
# =============================================================================

print("=" * 60)
print("4. TRANSFORM (SAME SHAPE AS ORIGINAL)")
print("=" * 60)

# Add department average salary to each row
df["dept_avg_salary"] = df.groupby("department")["salary"].transform("mean")
print("With dept_avg_salary:")
print(df[["name", "department", "salary", "dept_avg_salary"]].head(10))
print()

# Z-score within group
df["salary_zscore"] = df.groupby("department")["salary"].transform(
    lambda x: (x - x.mean()) / x.std()
)
print("Salary z-score within department:")
print(df[["name", "department", "salary", "salary_zscore"]].head(10))
print()

# Rank within group
df["salary_rank_dept"] = df.groupby("department")["salary"].transform("rank", ascending=False)
print("Salary rank within department:")
print(df[["name", "department", "salary", "salary_rank_dept"]].head(10))
print()

# Fill missing with group mean
df_with_nan = df.copy()
df_with_nan.loc[0:3, "performance_score"] = np.nan
df_with_nan["perf_filled"] = df_with_nan.groupby("department")["performance_score"].transform(
    lambda x: x.fillna(x.mean())
)
print("Fill NaN with group mean:")
print(df_with_nan[["name", "department", "performance_score", "perf_filled"]].head(10))
print()

# =============================================================================
# 5. FILTER - SUBSET GROUPS
# =============================================================================

print("=" * 60)
print("5. FILTER GROUPS")
print("=" * 60)

# Keep only departments with >5 employees
large_depts = df.groupby("department").filter(lambda x: len(x) > 5)
print(
    f"Departments with >5 employees: {large_depts['department'].nunique()} depts, {len(large_depts)} employees"
)
print(large_depts["department"].value_counts())
print()

# Keep groups where avg salary > 80000
high_pay_depts = df.groupby("department").filter(lambda x: x["salary"].mean() > 80000)
print(f"Departments with avg salary > 80k: {high_pay_depts['department'].nunique()} depts")
print(high_pay_depts["department"].value_counts())
print()

# Keep groups with at least one senior/lead
senior_depts = df.groupby("department").filter(
    lambda x: x["role"].isin(["Senior", "Lead", "Manager"]).any()
)
print(f"Departments with senior+ roles: {senior_depts['department'].nunique()} depts")
print()

# =============================================================================
# 6. APPLY - FLEXIBLE GROUP OPERATIONS
# =============================================================================

print("=" * 60)
print("6. APPLY - CUSTOM GROUP OPERATIONS")
print("=" * 60)


# Apply custom function to each group
def describe_group(group):
    return pd.Series(
        {
            "count": len(group),
            "avg_salary": group["salary"].mean(),
            "top_performer": group.loc[group["performance_score"].idxmax(), "name"],
            "salary_spread": group["salary"].max() - group["salary"].min(),
        }
    )


dept_describe = df.groupby("department").apply(describe_group)
print("Custom describe per department:")
print(dept_describe.round(2))
print()


# Top N per group
def top_n_salary(group, n=2):
    return group.nlargest(n, "salary")


# pandas 2.2+ excludes the grouping key from each applied group; it stays in the index
top_2_per_dept = df.groupby("department").apply(top_n_salary, n=2)
print("Top 2 salaries per department:")
print(
    top_2_per_dept.reset_index(level="department")[["name", "department", "salary"]].reset_index(
        drop=True
    )
)
print()

# =============================================================================
# 7. ADVANCED PATTERNS
# =============================================================================

print("=" * 60)
print("7. ADVANCED PATTERNS")
print("=" * 60)

# Named aggregation (pandas 0.25+)
named_agg = (
    df.groupby("department")
    .agg(
        avg_salary=("salary", "mean"),
        median_salary=("salary", "median"),
        total_employees=("employee_id", "count"),
        avg_performance=("performance_score", "mean"),
        max_exp=("years_experience", "max"),
    )
    .round(2)
)
print("Named aggregation:")
print(named_agg)
print()

# Groupby with as_index=False
print("Groupby with as_index=False:")
flat = df.groupby("department", as_index=False).agg(
    avg_salary=("salary", "mean"), count=("employee_id", "count")
)
print(flat)
print()

# Groupby on computed column
df["salary_band"] = pd.cut(
    df["salary"],
    bins=[0, 60000, 100000, 150000, 200000],
    labels=["Low", "Medium", "High", "Very High"],
)
band_stats = (
    df.groupby("salary_band", observed=True)
    .agg(
        count=("employee_id", "count"),
        avg_age=("age", "mean"),
        avg_perf=("performance_score", "mean"),
    )
    .round(2)
)
print("Salary band stats:")
print(band_stats)
print()

# Groupby with datetime
df["hire_date"] = pd.date_range("2020-01-01", periods=50, freq="W")
df["hire_year"] = df["hire_date"].dt.year
yearly = df.groupby("hire_year").agg(hires=("employee_id", "count"), avg_salary=("salary", "mean"))
print("Yearly hiring:")
print(yearly)
print()

# =============================================================================
# 8. PERFORMANCE TIPS
# =============================================================================

print("=" * 60)
print("8. PERFORMANCE TIPS")
print("=" * 60)

# 1. Use categorical for groupby columns
df_cat = df.copy()
df_cat["department"] = df_cat["department"].astype("category")
df_cat["role"] = df_cat["role"].astype("category")

import time

# Time groupby
start = time.time()
for _ in range(100):
    df.groupby("department")["salary"].mean()
time_regular = time.time() - start

start = time.time()
for _ in range(100):
    df_cat.groupby("department")["salary"].mean()
time_categorical = time.time() - start

print(f"Regular groupby: {time_regular:.4f}s")
print(f"Categorical groupby: {time_categorical:.4f}s")
print(f"Speedup: {time_regular / time_categorical:.2f}x")
print()

# 2. Use observed=True for categorical (excludes unobserved categories)
print("With observed=True:")
print(df.groupby("department", observed=True)["salary"].mean())
print()

# 3. Avoid apply when possible - use vectorized operations
# SLOW:
# df.groupby('dept').apply(lambda x: x['salary'].sum() / x['age'].sum())
# FAST:
# df.groupby('dept')['salary'].sum() / df.groupby('dept')['age'].sum()

print("=" * 60)
print("END OF GROUPBY & AGGREGATION")
print("=" * 60)
