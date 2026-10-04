# Pandas Advanced Quiz

## Topic Overview
This quiz covers advanced Pandas concepts including multi-level indexing, time series operations, performance optimization, advanced groupby operations, and window functions. These topics are essential for professional data analysis and engineering.

**Difficulty:** Intermediate to Advanced
**Questions:** 20
**Time:** ~30 minutes
**Passing Score:** 70% (14/20)

---

## Questions

### Question 1 [Medium]
**What is a MultiIndex in Pandas?**

A) A DataFrame with multiple indexes
B) A hierarchical indexing system with multiple levels
C) A way to merge multiple DataFrames
D) An index with duplicate values

**Correct Answer:** B
**Explanation:** MultiIndex allows hierarchical (multi-level) indexing, enabling you to work with higher-dimensional data in a 2D DataFrame. It's like having multiple index columns.

```python
arrays = [["bar", "bar", "baz"], ["one", "two", "one"]]
index = pd.MultiIndex.from_arrays(arrays, names=["first", "second"])
```

---

### Question 2 [Hard]
**What does `df.unstack()` do?**

A) Removes stacked elements
B) Converts a level in the index to columns
C) Flattens the DataFrame
D) Removes MultiIndex

**Correct Answer:** B
**Explanation:** `unstack()` pivots a level of the index into columns. The inverse operation is `stack()`, which pivots columns into the index. This is useful for reshaping data.

---

### Question 3 [Medium]
**How do you handle time series data in Pandas?**

A) Using `pd.to_datetime()`
B) Setting a datetime column as the index
C) Using `resample()` for frequency conversion
D) All of the above

**Correct Answer:** D
**Explanation:** Pandas provides comprehensive time series support: `to_datetime()` for parsing, DatetimeIndex for indexing, and `resample()` for changing frequency (e.g., daily to monthly).

---

### Question 4 [Hard]
**What is the difference between `resample()` and `rolling()`?**

A) No difference
B) `resample()` groups by time periods, `rolling()` creates sliding windows
C) `resample()` is faster
D) `rolling()` groups by time periods

**Correct Answer:** B
**Explanation:** `resample()` aggregates data over fixed time periods (e.g., monthly averages). `rolling()` creates sliding window calculations (e.g., 7-day moving average).

```python
df.resample("M").mean()  # Monthly averages
df["price"].rolling(7).mean()  # 7-day moving average
```

---

### Question 5 [Medium]
**What does `df.pipe()` do?**

A) Pipes data to another process
B) Applies a function that takes a DataFrame and returns a DataFrame
C) Connects two DataFrames
D) Creates a data pipeline

**Correct Answer:** B
**Explanation:** `pipe()` applies a function to the DataFrame, enabling method chaining. It's useful for creating reusable, composable data transformations.

```python
def add_mean(df, col):
    df[f"{col}_mean"] = df[col].mean()
    return df


df.pipe(add_mean, "price").pipe(add_mean, "quantity")
```

---

### Question 6 [Hard]
**What are the performance implications of `df.iterrows()`?**

A) It's the fastest way to iterate
B) It's very slow for large DataFrames, creating a Series per row
C) It has no performance impact
D) It's optimized for large datasets

**Correct Answer:** B
**Explanation:** `iterrows()` is extremely slow because it creates a Series for each row. Use vectorized operations, `apply()`, or `itertuples()` (which is much faster) instead.

---

### Question 7 [Medium]
**What does `pd.cut()` do?**

A) Removes outliers
B) Bins continuous data into discrete categories
C) Cuts the DataFrame
D) Removes rows

**Correct Answer:** B
**Explanation:** `pd.cut()` bins continuous values into discrete intervals (like a histogram). Useful for creating categorical variables from numeric data.

```python
pd.cut(df["age"], bins=[0, 18, 35, 60, 100], labels=["child", "young", "middle", "senior"])
```

---

### Question 8 [Hard]
**What is the difference between `merge()` and `join()`?**

A) No difference
B) `merge` joins on columns, `join` joins on indexes by default
C) `join` is faster
D) `merge` only supports inner joins

**Correct Answer:** B
**Explanation:** `merge()` is more flexible and joins on specified columns. `join()` joins on indexes by default and is more concise for index-based joins.

---

### Question 9 [Medium]
**What does `df.agg()` allow you to do?**

A) Aggregate with a single function
B) Apply multiple aggregation functions to columns
C) Only count values
D) Only sum values

**Correct Answer:** B
**Explanation:** `agg()` (or `aggregate()`) allows you to apply different functions to different columns in one call, making it more flexible than `apply()` for mixed aggregations.

```python
df.groupby("department").agg({"salary": ["mean", "max"], "name": "count"})
```

---

### Question 10 [Hard]
**What is `pd.eval()` used for?**

A) Evaluating Python expressions
B) Efficient expression evaluation on DataFrames
C) Parsing data
D) Evaluating model performance

**Correct Answer:** B
**Explanation:** `pd.eval()` evaluates string expressions efficiently using NumPy under the hood. It's faster than equivalent Python operations for large DataFrames and uses less memory.

```python
pd.eval("df.a + df.b * df.c")
```

---

### Question 11 [Medium]
**What does `df.transform()` do?**

A) Transforms the DataFrame shape
B) Applies a function element-wise or column-wise
C) Converts data types
D) Transposes the DataFrame

**Correct Answer:** B
**Explanation:** `transform()` applies a function to each group or column, returning a result with the same shape as the input. It's useful within `groupby()` for element-wise transformations.

---

### Question 12 [Hard]
**What is the purpose of `pd.Categorical`?**

A) Creates categories from data
B) Optimizes memory for columns with few unique values
C) Both A and B
D) Only sorts data

**Correct Answer:** C
**Explanation:** `pd.Categorical` stores data as categories instead of repeated values. This saves memory for columns with many repeated values (like country names) and enables categorical operations.

---

### Question 13 [Medium]
**How do you handle duplicate values in a DataFrame?**

A) `df.drop_duplicates()`
B) `df.duplicated()`
C) `df[~df.duplicated()]`
D) All of the above

**Correct Answer:** D
**Explanation:** `duplicated()` returns a boolean mask of duplicate rows. `drop_duplicates()` removes them. Boolean indexing with `~duplicated()` achieves the same result.

---

### Question 14 [Hard]
**What does `df.clip()` do?**

A) Clips the DataFrame to a file
B) Limits values to specified thresholds
C) Removes outliers
D) Copies the DataFrame

**Correct Answer:** B
**Explanation:** `df.clip(lower, upper)` caps values at the specified thresholds. Values below `lower` become `lower`, values above `upper` become `upper`. Useful for handling outliers.

---

### Question 15 [Medium]
**What is `df.pivot()` used for?**

A) Rotates rows to columns
B) Reshapes data from long to wide format
C) Creates pivot tables
D) Both B and C

**Correct Answer:** D
**Explanation:** `pivot()` reshapes data from long to wide format. It's simpler than `pivot_table()` as it doesn't support aggregation - it requires unique index/column combinations.

---

### Question 16 [Hard]
**How do you optimize Pandas operations for large datasets?**

A) Use `chunksize` when reading files
B) Use appropriate dtypes (e.g., `category`, `int32`)
C) Use `eval()` for complex expressions
D) All of the above

**Correct Answer:** D
**Explanation:** For large datasets: read in chunks, downcast dtypes, use `eval()` for complex expressions, avoid `iterrows()`, and consider using `dask` for out-of-core processing.

---

### Question 17 [Medium]
**What does `df.applymap()` (now `df.map()` in newer versions) do?**

A) Maps index values
B) Applies a function to each element
C) Creates a map of the DataFrame
D) Maps column names

**Correct Answer:** B
**Explanation:** `map()` (formerly `applymap()`) applies a function element-wise across the entire DataFrame. For column-wise operations, use `apply()` instead.

---

### Question 18 [Hard]
**What is `pd.MultiIndex.from_product()` used for?**

A) Creates a MultiIndex from the Cartesian product of iterables
B) Multiplies index values
C) Creates a product index
D) Multiplies DataFrames

**Correct Answer:** A
**Explanation:** `from_product()` creates a MultiIndex from the Cartesian product of all input iterables. This is useful for creating all combinations of index levels.

```python
pd.MultiIndex.from_product([["A", "B"], [1, 2, 3]], names=["letter", "number"])
# Creates: (A,1), (A,2), (A,3), (B,1), (B,2), (B,3)
```

---

### Question 19 [Medium]
**What does `df.style` provide?**

A) DataFrame styling for Jupyter notebooks
B) CSS styling
C) Formatting for exports
D) All of the above

**Correct Answer:** D
**Explanation:** `df.style` provides styling for Jupyter notebooks, including conditional formatting, color scales, and custom CSS. It's useful for data exploration and presentations.

---

### Question 20 [Hard]
**What is `pd.read_parquet()` used for?**

A) Reading Excel files
B) Reading Parquet columnar storage format
C) Reading JSON files
D) Reading CSV files

**Correct Answer:** B
**Explanation:** Parquet is a columnar storage format optimized for analytics. `pd.read_parquet()` reads Parquet files, which offer better compression and faster queries than CSV for large datasets.

---

## Answer Key

| Question | Answer |
|----------|--------|
| 1 | B |
| 2 | B |
| 3 | D |
| 4 | B |
| 5 | B |
| 6 | B |
| 7 | B |
| 8 | B |
| 9 | B |
| 10 | B |
| 11 | B |
| 12 | C |
| 13 | D |
| 14 | B |
| 15 | D |
| 16 | D |
| 17 | B |
| 18 | A |
| 19 | D |
| 20 | B |

---

## Score Tracking

| Score Range | Level |
|-------------|-------|
| 18-20 | Expert - You've mastered advanced Pandas! |
| 14-17 | Proficient - Strong understanding, ready for professional use |
| 10-13 | Developing - Good foundation, practice advanced patterns |
| 6-9 | Beginner - Review Pandas basics first |
| 0-5 | Novice - Start with Pandas basics quiz |

---

*Quiz created for AI Engineer Lab - Python Foundations*
