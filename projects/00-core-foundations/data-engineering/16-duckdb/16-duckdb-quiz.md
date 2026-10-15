# Data Engineering 16: DuckDB Profiling — Quiz

> **Topic Overview**: Profiling Parquet in place with DuckDB: read_parquet,
> SUMMARIZE, null and duplicate queries, quantiles, pushdown, profile tables.

---

## Score Tracker

| Metric | Value |
|--------|-------|
| Questions Answered | 0 / 10 |
| Correct Answers | 0 |
| Score | 0% |

---

## Questions

### Question 1 — Easy

**What does `read_parquet` let DuckDB do?**

- A) Import Parquet into memory frames
- B) Query the Parquet file in place without loading it
- C) Rewrite Parquet files faster
- D) Delete duplicate rows

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: read_parquet queries the file where it sits, keeping profiling in near-constant memory.

</details>

---

### Question 2 — Easy

**What does `SUMMARIZE` return?**

- A) One row per duplicate passage
- B) One row per column with counts, nulls, min, max, quantiles
- C) The query execution plan
- D) A list of file names

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: SUMMARIZE is the one-query column overview; four columns in means four rows out.

</details>

---

### Question 3 — Easy

**A corpus has 10 rows with 8 distinct passage ids. How many duplicates?**

- A) 0
- B) 2
- C) 8
- D) 10

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: Duplicate count is rows minus distinct keys: 10 minus 8 is 2.

</details>

---

### Question 4 — Medium

**What does a null rate of 1.0 on a column mean?**

- A) The column is healthy
- B) Every value is missing: a dead extractor or an unfilled column
- C) The column has no duplicates
- D) The file failed to load

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: A 1.0 rate is an all-null column, which is a finding that needs a name, not just a number.

</details>

---

### Question 5 — Medium

**Why are quantiles approximate in profiling?**

- A) Exact values are impossible to compute
- B) Approximation shows the shape in one pass without sorting, at no decision cost
- C) DuckDB cannot sort numbers
- D) Tests require randomness

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: The profile needs skew shape, not the sixth decimal, so one-pass estimates buy speed.

</details>

---

### Question 6 — Medium

**What is predicate pushdown?**

- A) Deleting rows that match a filter
- B) Pushing query filters into the file read so non-matching row groups are skipped
- C) Sorting the output by predicate
- D) Compressing the Parquet file

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: Row-group min/max metadata lets the engine skip groups that cannot match the filter.

</details>

---

### Question 7 — Medium

**Why export the profile as a table instead of printing it?**

- A) Tables print more nicely
- B) Quality gates consume tables: they query measurements instead of recomputing them
- C) Logs cannot hold numbers
- D) DuckDB cannot print output

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: Measure once in DuckDB into column_profile, then judge many times in the gates.

</details>

---

### Question 8 — Hard

**What is the Polars / DuckDB division per ADR-0011?**

- A) Polars profiles, DuckDB cleans
- B) Polars owns cleaning and transformation; DuckDB owns profiling and measurement
- C) Both tools do everything interchangeably
- D) DuckDB replaces Polars entirely

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: One sentence each, with the Parquet file as the boundary: Polars writes it, DuckDB reads it.

</details>

---

### Question 9 — Hard

**Why must tests assert quantile ranges, never exact quantile values?**

- A) Quantiles are always wrong
- B) Approximate quantiles estimate shape, so exact values are unstable across runs and versions
- C) Ranges run faster than values
- D) Scores are never numeric

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: Assert the valid range and let the printed numbers inform the human; exact asserts would be flaky.

</details>

---

### Question 10 — Hard

**A SUMMARIZE returns 5 rows for a 4-column schema. What happened?**

- A) Nothing, extra rows are normal
- B) Schema drift: something upstream changed shape without notice
- C) The file has duplicates
- D) Pushdown failed

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: One row per column is the contract, so a mismatched count means the stored shape changed.

</details>

---

## Answer Key

| Q# | Answer | Difficulty |
|----|--------|------------|
| 1 | B | Easy |
| 2 | B | Easy |
| 3 | B | Medium |
| 4 | B | Medium |
| 5 | B | Medium |
| 6 | B | Medium |
| 7 | B | Medium |
| 8 | B | Hard |
| 9 | B | Hard |
| 10 | B | Hard |

---

## Scoring Guide

| Score | Rating | Recommendation |
|-------|--------|----------------|
| 9-10 | Expert | Ready for data quality gates |
| 7-8 | Proficient | Review pushdown and quantiles |
| 5-6 | Developing | Re-study the profile table |
| 0-4 | Novice | Restart the lecture |

---

**Previous**: [15 - Storage and Databases](../15-storage-and-databases/15-storage-and-databases-quiz.md) | **Next**: [18 - DVC](../18-dvc/18-dvc-quiz.md)
