"""
Pandas Missing Data Handling: isna, fillna, dropna, interpolation
==================================================================

This module covers comprehensive techniques for handling missing data in pandas.
"""

import pandas as pd
import numpy as np

# Create sample data with various missing value patterns
np.random.seed(42)
df = pd.DataFrame(
    {
        "id": range(1, 21),
        "name": [f"User_{i}" for i in range(1, 21)],
        "age": [
            25,
            30,
            np.nan,
            35,
            40,
            28,
            np.nan,
            32,
            29,
            31,
            27,
            33,
            36,
            np.nan,
            38,
            26,
            34,
            37,
            24,
            39,
        ],
        "salary": [
            50000,
            np.nan,
            60000,
            65000,
            np.nan,
            55000,
            58000,
            np.nan,
            62000,
            59000,
            53000,
            64000,
            np.nan,
            67000,
            56000,
            54000,
            np.nan,
            68000,
            57000,
            61000,
        ],
        "department": [
            "Eng",
            "Sales",
            "Eng",
            np.nan,
            "HR",
            "Eng",
            "Sales",
            "Eng",
            "HR",
            "Sales",
            "Eng",
            np.nan,
            "HR",
            "Sales",
            "Eng",
            "HR",
            "Sales",
            "Eng",
            "HR",
            "Sales",
        ],
        "join_date": pd.date_range("2020-01-01", periods=20, freq="ME"),
        "performance": [
            4.2,
            3.8,
            np.nan,
            4.5,
            3.9,
            4.1,
            3.7,
            np.nan,
            4.3,
            4.0,
            3.6,
            4.4,
            3.5,
            np.nan,
            4.6,
            3.9,
            4.2,
            3.8,
            4.1,
            4.0,
        ],
        "bonus": [
            1000,
            2000,
            np.nan,
            1500,
            3000,
            np.nan,
            2500,
            1800,
            np.nan,
            2200,
            1200,
            np.nan,
            2800,
            1600,
            np.nan,
            2400,
            1900,
            np.nan,
            2100,
            1700,
        ],
    }
)

print("=" * 60)
print("1. DETECTING MISSING VALUES")
print("=" * 60)

print("df.isna() - Boolean mask:")
print(df.isna().head(10))
print()

print("df.isna().sum() - Count per column:")
print(df.isna().sum())
print()

print("df.isna().mean() - Percentage missing:")
print((df.isna().mean() * 100).round(2))
print()

print("df.notna().sum() - Non-null count:")
print(df.notna().sum())
print()

print("=" * 60)
print("2. DROPPING MISSING VALUES")
print("=" * 60)

print("df.dropna() - Drop rows with ANY missing:")
dropped_any = df.dropna()
print(f"Original: {len(df)} rows, After dropna(): {len(dropped_any)} rows")
print(dropped_any)
print()

print("df.dropna(how='all') - Drop rows where ALL are missing:")
# Add a row with all NaN
df_all_nan = df.copy()
df_all_nan.loc[20] = [np.nan] * len(df.columns)
print(f"With all-NaN row: {len(df_all_nan)} rows")
print(f"After dropna(how='all'): {len(df_all_nan.dropna(how='all'))} rows")
print()

print("df.dropna(axis=1) - Drop COLUMNS with any missing:")
dropped_cols = df.dropna(axis=1)
print(f"Original columns: {len(df.columns)}, After: {len(dropped_cols.columns)}")
print(f"Remaining columns: {dropped_cols.columns.tolist()}")
print()

print("df.dropna(subset=['salary', 'age']) - Drop only if missing in specific cols:")
dropped_subset = df.dropna(subset=["salary", "age"])
print(f"Original: {len(df)} rows, After: {len(dropped_subset)} rows")
print()

print("df.dropna(thresh=5) - Keep rows with at least 5 non-null values:")
dropped_thresh = df.dropna(thresh=5)
print(f"Original: {len(df)} rows, After: {len(dropped_thresh)} rows")
print()

print("=" * 60)
print("3. FILLING MISSING VALUES")
print("=" * 60)

print("df.fillna(value) - Fill with scalar:")
filled_scalar = df.fillna(0)
print(
    f"Salary missing before: {df['salary'].isna().sum()}, after: {filled_scalar['salary'].isna().sum()}"
)
print()

print("df.fillna(dict) - Fill per column:")
filled_dict = df.fillna(
    {"salary": df["salary"].median(), "age": df["age"].mean(), "department": "Unknown"}
)
print(filled_dict[["age", "salary", "department"]].head(10))
print()

print("df.fillna(method='ffill') - Forward fill:")
# Create time series with gaps
ts = pd.Series(
    [1, np.nan, np.nan, 4, 5, np.nan, 7], index=pd.date_range("2020-01-01", periods=7, freq="D")
)
print("Original:")
print(ts)
print("Forward fill:")
print(ts.ffill())
print("Backward fill:")
print(ts.bfill())
print()

print("df.fillna(method='ffill', limit=1) - Limit consecutive fills:")
print(ts.ffill(limit=1))
print()

print("=" * 60)
print("4. INTERPOLATION")
print("=" * 60)

print("df.interpolate() - Linear interpolation (default):")
interp_linear = df[["age", "salary", "performance"]].interpolate()
print(interp_linear.head(10))
print()

print("df.interpolate(method='time') - Time-aware interpolation:")
df_time = df.set_index("join_date")[["salary", "performance"]].interpolate(method="time")
print(df_time.head(10))
print()

print("df.interpolate(method='polynomial', order=2) - Polynomial:")
interp_poly = df[["age", "salary"]].interpolate(method="polynomial", order=2)
print(interp_poly.head(10))
print()

print("df.interpolate(method='spline', order=3) - Spline:")
interp_spline = df[["age", "salary"]].interpolate(method="spline", order=3)
print(interp_spline.head(10))
print()

print("df.interpolate(method='pad') / 'nearest' / 'cubic' / 'akima':")
for method in ["pad", "nearest", "cubic", "akima"]:
    try:
        result = df[["age"]].interpolate(method=method)
        print(f"{method}: {result['age'].iloc[2]:.2f} (index 2)")
    except Exception as e:
        print(f"{method}: {e}")
print()

print("=" * 60)
print("5. ADVANCED FILLING STRATEGIES")
print("=" * 60)

print("Fill with group statistics:")
df["salary_filled_group"] = df.groupby("department")["salary"].transform(
    lambda x: x.fillna(x.median())
)
print(df[["department", "salary", "salary_filled_group"]].head(10))
print()

print("Fill with rolling statistics (time series):")
ts_data = pd.Series(
    [10, np.nan, np.nan, 13, 14, np.nan, 17, 18, np.nan, 20],
    index=pd.date_range("2020-01-01", periods=10, freq="D"),
)
print("Original:", ts_data.values)
print("Rolling mean fill:", ts_data.fillna(ts_data.rolling(3, min_periods=1).mean()).values)
print("Expanding mean fill:", ts_data.fillna(ts_data.expanding().mean()).values)
print()

print("Fill with KNN imputation (using sklearn):")
from sklearn.impute import KNNImputer

knn_imputer = KNNImputer(n_neighbors=3)
numeric_cols = ["age", "salary", "performance", "bonus"]
df_knn = df[numeric_cols].copy()
df_knn_imputed = pd.DataFrame(
    knn_imputer.fit_transform(df_knn), columns=numeric_cols, index=df.index
)
print("Before KNN:")
print(df[numeric_cols].head(10))
print("After KNN:")
print(df_knn_imputed.head(10))
print()

print("=" * 60)
print("6. REPLACING VALUES")
print("=" * 60)

print("df.replace() - Replace specific values:")
df_replaced = df.replace({"department": {"Eng": "Engineering", "HR": "Human Resources"}})
print(df_replaced[["department"]].head(10))
print()

print("df.replace() with regex:")
df_text = pd.DataFrame({"text": ["hello world", "foo bar", "hello foo", np.nan]})
print(df_text.replace(r"hello", "hi", regex=True))
print()

print("df.replace() with list of values:")
df_num = pd.DataFrame({"values": [1, 2, -999, 3, -999, 4]})
print(df_num.replace([-999], np.nan))
print()

print("=" * 60)
print("7. HANDLING MISSING IN SPECIFIC CONTEXTS")
print("=" * 60)

print("For categorical data - use mode:")
df["department_filled"] = df["department"].fillna(df["department"].mode()[0])
print(df[["department", "department_filled"]].head(10))
print()

print("For time series - use forward/backward fill:")
ts_df = df.set_index("join_date")[["salary"]].asfreq("D")
print("Resampled to daily:", len(ts_df), "rows")
ts_filled = ts_df.ffill()
print("After ffill:", ts_filled["salary"].isna().sum(), "missing")
print()

print("Mark missing as category (for ML):")
df["salary_missing"] = df["salary"].isna().astype(int)
df["salary_for_ml"] = df["salary"].fillna(-1)  # or use median
print(df[["salary", "salary_missing", "salary_for_ml"]].head(10))
print()

print("=" * 60)
print("8. BEST PRACTICES SUMMARY")
print("=" * 60)

best_practices = """
BEST PRACTICES FOR MISSING DATA:

1. ALWAYS investigate WHY data is missing (MCAR, MAR, MNAR)
2. Don't blindly drop - you lose information
3. For numeric: median (robust) or mean; for categorical: mode
4. Time series: forward/backward fill or interpolation
5. Consider adding missingness indicator columns: 'is_missing' for ML models
6. Use domain knowledge for imputation values
7. For ML: KNN, MICE, or model-based imputation
8. Document your imputation strategy
9. Test sensitivity: does imputation method affect results?
10. Consider multiple imputation for statistical inference
"""
print(best_practices)

print("=" * 60)
print("END OF MISSING DATA HANDLING")
print("=" * 60)
