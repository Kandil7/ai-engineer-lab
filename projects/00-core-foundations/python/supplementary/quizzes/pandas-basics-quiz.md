# Pandas Basics Quiz

## Topic Overview
Pandas is the most popular Python library for data manipulation and analysis. It provides DataFrames and Series data structures for working with structured data. This quiz covers core concepts including DataFrame creation, data selection, filtering, and basic operations.

**Difficulty:** Beginner to Intermediate
**Questions:** 20
**Time:** ~25 minutes
**Passing Score:** 70% (14/20)

---

## Questions

### Question 1 [Easy]
**What are the two primary data structures in Pandas?**

A) Lists and Dictionaries
B) Series and DataFrame
C) Arrays and Matrices
D) Tables and Charts

**Correct Answer:** B
**Explanation:** `Series` is a one-dimensional labeled array, and `DataFrame` is a two-dimensional labeled table. Together, they form the foundation of all Pandas operations.

---

### Question 2 [Easy]
**How do you create a DataFrame from a dictionary?**

A) `pd.DataFrame(dict)`
B) `pd.from_dict(dict)`
C) `pd.create_frame(dict)`
D) Both A and B

**Correct Answer:** D
**Explanation:** Both `pd.DataFrame(dict)` and `pd.DataFrame.from_dict(dict)` create DataFrames. `pd.DataFrame(dict)` is the most common and concise approach.

```python
import pandas as pd

data = {"Name": ["Alice", "Bob"], "Age": [25, 30]}
df = pd.DataFrame(data)
```

---

### Question 3 [Easy]
**What does `df.head(5)` do?**

A) Returns the first 5 rows
B) Returns the last 5 rows
C) Returns 5 random rows
D) Returns column headers

**Correct Answer:** A
**Explanation:** `df.head(n)` returns the first n rows of the DataFrame. Default is 5. Similarly, `df.tail(n)` returns the last n rows.

---

### Question 4 [Easy]
**How do you check the dimensions of a DataFrame?**

A) `df.shape`
B) `df.dimensions()`
C) `df.size()`
D) `df.count()`

**Correct Answer:** A
**Explanation:** `df.shape` returns a tuple `(rows, columns)`. `df.size` returns the total number of elements. `df.count()` returns non-null values per column.

---

### Question 5 [Medium]
**What does `df.info()` display?**

A) Only column names
B) Data types, non-null counts, and memory usage
C) Statistical summary
D) First 5 rows

**Correct Answer:** B
**Explanation:** `df.info()` provides a concise summary including column names, data types, non-null counts, memory usage, and the DataFrame's total memory consumption.

---

### Question 6 [Medium]
**How do you select a single column from a DataFrame?**

A) `df['column_name']`
B) `df.column_name`
C) Both A and B
D) `df.get_column('column_name')`

**Correct Answer:** C
**Explanation:** Both bracket notation `df['column']` and dot notation `df.column` work. Bracket notation is preferred when column names have spaces or special characters.

---

### Question 7 [Medium]
**What is the difference between `df.loc[]` and `df.iloc[]`?**

A) No difference
B) `loc` uses labels, `iloc` uses integer positions
C) `loc` is faster
D) `iloc` supports boolean indexing

**Correct Answer:** B
**Explanation:** `df.loc[]` selects by label (row/column names). `df.iloc[]` selects by integer position (0-based index). Both support slicing, but the endpoints differ (loc is inclusive, iloc is exclusive).

---

### Question 8 [Easy]
**How do you get column names of a DataFrame?**

A) `df.columns`
B) `df.keys()`
C) `df.column_names()`
D) Both A and B

**Correct Answer:** D
**Explanation:** Both `df.columns` and `df.keys()` return the column labels. `df.columns` returns an Index object that supports various operations.

---

### Question 9 [Medium]
**What does `df.describe()` provide?**

A) DataFrame info
B) Summary statistics (count, mean, std, min, max, quartiles)
C) Data types
D) Missing values count

**Correct Answer:** B
**Explanation:** `df.describe()` returns descriptive statistics including count, mean, standard deviation, min, max, and quartile values for numeric columns.

---

### Question 10 [Easy]
**How do you rename columns in a DataFrame?**

A) `df.rename(columns={'old': 'new'})`
B) `df.columns = ['new1', 'new2']`
C) `df.rename_column('old', 'new')`
D) Both A and B

**Correct Answer:** D
**Explanation:** `df.rename(columns={...})` renames specific columns. Assigning to `df.columns` replaces all column names at once. `rename()` is safer for partial renames.

---

### Question 11 [Medium]
**What does `df.groupby('col')` do?**

A) Sorts the DataFrame by column
B) Groups rows by unique values in the column
C) Filters the DataFrame
D) Drops the column

**Correct Answer:** B
**Explanation:** `groupby()` splits the DataFrame into groups based on column values. You typically chain it with an aggregation method like `.mean()`, `.sum()`, or `.count()`.

```python
df.groupby("Department")["Salary"].mean()
```

---

### Question 12 [Easy]
**How do you check for missing values?**

A) `df.isnull()`
B) `df.isna()`
C) Both A and B
D) `df.missing()`

**Correct Answer:** C
**Explanation:** Both `df.isnull()` and `df.isna()` are aliases that return a boolean DataFrame indicating missing values (True where null). Use `.sum()` to count them.

---

### Question 13 [Medium]
**What does `df.merge()` do?**

A) Combines two DataFrames based on common columns
B) Appends rows
C) Concatenates along axis
D) Joins indexes only

**Correct Answer:** A
**Explanation:** `pd.merge()` combines DataFrames based on common columns (like SQL JOIN). It supports inner, outer, left, and right joins. `pd.concat()` is for appending along an axis.

---

### Question 14 [Medium]
**What is the difference between `df.apply()` and `df.applymap()`?**

A) No difference
B) `apply()` works row/column-wise, `applymap()` works element-wise
C) `applymap()` is deprecated
D) Both are element-wise

**Correct Answer:** B
**Explanation:** `apply()` applies a function along an axis (rows or columns). `applymap()` applies a function to each element. Note: `applymap()` is deprecated in favor of `map()` in newer versions.

---

### Question 15 [Easy]
**How do you filter rows based on a condition?**

A) `df[df['col'] > value]`
B) `df.query('col > value')`
C) Both A and B
D) `df.filter(rows)`

**Correct Answer:** C
**Explanation:** Boolean indexing `df[df['col'] > value]` is the most common approach. `df.query()` provides a string-based query syntax which can be more readable for complex conditions.

---

### Question 16 [Medium]
**What does `df.sort_values('col')` do?**

A) Sorts by index
B) Sorts rows by values in the specified column
C) Removes duplicates
D) Filters rows

**Correct Answer:** B
**Explanation:** `sort_values()` sorts the DataFrame by specified column(s). Use `ascending=False` for descending order. `sort_index()` sorts by the index instead.

---

### Question 17 [Easy]
**How do you add a new column to a DataFrame?**

A) `df['new_col'] = values`
B) `df.insert()`
C) `df.assign()`
D) All of the above

**Correct Answer:** D
**Explanation:** All three methods add columns. Bracket assignment is simplest. `insert()` lets you specify position. `assign()` returns a new DataFrame (non-mutating).

---

### Question 18 [Medium]
**What does `df.pivot_table()` do?**

A) Creates a pivot table for data summarization
B) Rotates the DataFrame
C) Transposes the DataFrame
D) Pivots the index

**Correct Answer:** A
**Explanation:** `pivot_table()` creates a spreadsheet-style pivot table. It groups data by specified index/columns and applies an aggregation function (default is mean).

---

### Question 19 [Hard]
**What is the difference between `inplace=True` and returning a new DataFrame?**

A) No difference
B) `inplace=True` modifies the original, returning creates a copy
C) `inplace=True` is always better
D) Returning is always better

**Correct Answer:** B
**Explanation:** `inplace=True` modifies the original DataFrame and returns None. Without it, a new DataFrame is returned. Inplace is memory-efficient but harder to debug. Modern Pandas recommends avoiding inplace.

---

### Question 20 [Medium]
**How do you read a CSV file with Pandas?**

A) `pd.read_csv('file.csv')`
B) `pd.load_csv('file.csv')`
C) `pd.csv_read('file.csv')`
D) `pd.open_csv('file.csv')`

**Correct Answer:** A
**Explanation:** `pd.read_csv()` is the standard function for reading CSV files. It supports many parameters: `sep`, `header`, `index_col`, `usecols`, `dtype`, `na_values`, etc.

---

## Answer Key

| Question | Answer |
|----------|--------|
| 1 | B |
| 2 | D |
| 3 | A |
| 4 | A |
| 5 | B |
| 6 | C |
| 7 | B |
| 8 | D |
| 9 | B |
| 10 | D |
| 11 | B |
| 12 | C |
| 13 | A |
| 14 | B |
| 15 | C |
| 16 | B |
| 17 | D |
| 18 | A |
| 19 | B |
| 20 | A |

---

## Score Tracking

| Score Range | Level |
|-------------|-------|
| 18-20 | Expert - You've mastered Pandas basics! |
| 14-17 | Proficient - Strong foundation, ready for advanced topics |
| 10-13 | Developing - Good start, practice more |
| 6-9 | Beginner - Review DataFrame fundamentals |
| 0-5 | Novice - Start with Pandas documentation |

---

*Quiz created for AI Engineer Lab - Python Foundations*
