# Data Engineering 16: DuckDB Profiling over Parquet

## Topic Overview

Quality gates cannot judge what nobody measured. Profiling is that measurement:
row counts, null rates, distinct counts, duplicate counts, and the shape of each
numeric column, computed over the stored Parquet before any gate runs. DuckDB
does it in place with SQL, without loading full frames into memory, which is why
ADR-0011 gives profiling to DuckDB while Polars keeps cleaning and transformation.

This lecture covers `read_parquet` in place, the one-query `SUMMARIZE` overview,
null-rate / distinct-count / duplicate queries, approximate quantiles for skew,
the predicate pushdown concept, and exporting the profile as a table that the
quality gates consume.

The subtle risk is profiling a sample and trusting it as the corpus. A profile
that runs in near-constant memory has no excuse for sampling, so profile the
whole file, every run.

## Learning Objectives

By the end of this lecture, you will be able to:

1. Query Parquet in place with `read_parquet`, without loading full frames.
2. Produce a one-query column overview with `SUMMARIZE`.
3. Write null-rate, distinct-count, and duplicate-count queries.
4. Read approximate quantiles to detect numeric skew.
5. Explain predicate pushdown and why it keeps profiling cheap.
6. Export the profile as a table the quality gates consume.

## Prerequisites

- Data Engineering 07 (Parquet and object storage) for the file layout.
- Data Engineering 11 (data quality) for the gates that consume the profile.
- ADR-0011 for the Polars / DuckDB division of labor.

---

## 1. `read_parquet` in Place

### The tool

`read_parquet` queries the file where it sits; no import step, no eager frame:

```python
con.execute("CREATE OR REPLACE VIEW docs AS SELECT * FROM read_parquet('gold.parquet')")
```

Every later query reads through the view. The Parquet file stays the source of
truth, and the profiler holds no copy of the corpus in memory.

### Why it matters

A profiler that loads the corpus first fails exactly when profiling matters
most: on data too large to hold comfortably. In-place reads keep the profile
step in near-constant memory regardless of corpus size.

### The discipline

Point every profile query at the stored file, never at a frame the pipeline
happens to hold. If the file and the frame disagree, the file wins, because the
file is what the gates and the next stage will read.

## 2. SUMMARIZE: the One-Query Overview

### The tool

`SUMMARIZE` returns one row per column with counts, nulls, min, max, and
approximate quantiles, which is the fastest way to meet a new file:

```sql
SELECT * FROM (SUMMARIZE docs);
```

Four columns in, four rows out. When the row count stops matching the schema,
something upstream changed shape without telling anyone.

### Why it is first

Run `SUMMARIZE` before any targeted query. It catches the cheap surprises, an
all-null column or a numeric stored as text, in one round trip, and it tells
you which columns deserve the focused queries of the next section.

### Its limit

`SUMMARIZE` describes columns one at a time. It never relates them: it cannot
say two rows share a `passage_id`, or that nulls cluster on one source. Cross
column and cross row questions need the queries below.

## 3. Null-Rate, Distinct-Count, Duplicate Queries

### Null rate

```sql
SELECT COUNT(*) FILTER (WHERE text IS NULL) * 1.0 / COUNT(*) FROM docs;
```

A null rate is a fraction with an exact expectation: this corpus has 2 nulls in
10 rows, so the query must return 0.2. Assert the math, not a vibe. A rate of
1.0 means an all-null column, which is either a dead extractor or a column the
pipeline fills later, and both deserve a name in the profile.

### Distinct count

```sql
SELECT COUNT(DISTINCT passage_id) FROM docs;
```

Distinct counts test identity: 10 rows with 8 distinct ids mean 2 duplicate
passages. Compare against the row count every run; the gap is the duplicate
count, and it must match the dedup topic's expectation (Data Engineering 05).

### Duplicate passages

```sql
SELECT COUNT(*) - COUNT(DISTINCT passage_id) FROM docs;
```

This is the headline number for retrieval health. It is exact, cheap, and
directly asserts the ingest contract: each passage stored once.

## 4. Approximate Quantiles and Skew

### The tool

```sql
SELECT approx_quantile(score, 0.5), approx_quantile(score, 0.9) FROM docs;
```

Medians and ninetieth percentiles describe skew that averages hide. A corpus
whose scores cluster near 0.9 with a tail near 0.1 is healthy; one clustered
near 0.5 with wide tails is undecided. The gate thresholds differ, so the
profile must show the shape.

### Why approximate

Exact quantiles sort; approximate quantiles sample the structure in one pass.
The profile needs the shape, not the sixth decimal, so approximation buys speed
at no decision cost. Never assert exact quantile values in a test; assert they
stay inside the valid range and let the printed numbers inform the human.

## 5. Predicate Pushdown

### The concept

A filter in the query is pushed into the file read, so Parquet row groups that
cannot match are skipped without being decoded. The query still sees the whole
file logically; physically it touches only the groups that matter:

```sql
SELECT COUNT(*) FROM docs WHERE source = 'b1';
```

Only the row groups containing `b1` are decoded. The rest are skipped by their
min/max metadata, which Parquet stores per group (Data Engineering 07).

### Why it belongs in this lecture

Pushdown is the reason in-place profiling stays cheap as corpora grow. A
profiler that cannot push filters down re-reads everything per question; one
that can answers ten questions for near the price of one scan. When a profile
query is slow, the first suspect is a filter the engine could not push.

## 6. Exporting the Profile and the Division of Labor

### The profile as a table

A printed summary informs a human; a table feeds a gate. Export per-column
measurements so the quality gates query them instead of recomputing them:

```sql
CREATE OR REPLACE TABLE column_profile AS
SELECT 'text' AS column_name,
       COUNT(*) FILTER (WHERE text IS NULL) * 1.0 / COUNT(*) AS null_rate,
       COUNT(DISTINCT text) AS distinct_count
FROM docs;
```

The gate then asserts on `column_profile`: null rate under threshold, duplicate
count at zero, no all-null column unless declared. Measure once in DuckDB, judge
many times in the gates.

### The division

Polars owns cleaning and transformation: it reshapes rows into the gold frame.
DuckDB owns profiling and measurement: it reads the stored Parquet and reports
what is there. One sentence each, per ADR-0011, and the boundary is the file:
Polars writes it, DuckDB reads it.

## Real-World Application

- Profiling the Athar gold Parquet each ingest so the gates judge fresh numbers.
- Catching an all-null column from a dead extractor before it reaches retrieval.
- Reading score skew to set gate thresholds instead of guessing them.
- Asserting duplicate count zero so a re-ingest never silently doubles passages.
- Skipping cold row groups with pushed-down source filters on large corpora.

## Common Mistakes

1. **Profiling a sample and trusting it as the corpus.** Profile the whole file.
2. **Loading the frame to profile the file.** Query in place with `read_parquet`.
3. **Asserting exact quantile values.** They are approximate; assert range only.
4. **Printing the profile instead of storing it.** Gates consume tables, not logs.
5. **Letting Polars and DuckDB overlap.** Polars cleans, DuckDB measures.

## Key Takeaways

1. `read_parquet` profiles the stored file in place, in near-constant memory.
2. `SUMMARIZE` gives one row per column; mismatched row counts mean schema drift.
3. Null-rate, distinct-count, and duplicate queries assert exact expectations.
4. Approximate quantiles show skew; pushdown keeps the questions cheap.
5. Export the profile as a table, and keep the Polars / DuckDB boundary at the file.

## Self-Check Questions

1. Why must the profiler read the stored file rather than a pipeline frame?
2. What does a `SUMMARIZE` row count different from the column count tell you?
3. Why is a null rate of 1.0 a finding, not just a number?
4. When is an approximate quantile preferable to an exact one?
5. What breaks if the quality gates read logs instead of a profile table?

## Further Reading / Connections

- ADR-0011 (DuckDB over Polars for profiling) and ADR-0010 (dependency adoption).
- Data Engineering 07 (Parquet) — the layout pushdown exploits.
- Data Engineering 11 (data quality) — the gates consuming the profile.
- Data Engineering 05 (deduplication) — what the duplicate count guards.
