# Data Engineering 16: DuckDB Profiling — Glossary

## Quick Reference Table

| Term | Definition | Example |
|------|-----------|---------|
| read_parquet | Querying Parquet in place | FROM read_parquet('gold.parquet') |
| SUMMARIZE | One row per column overview | SELECT * FROM (SUMMARIZE docs) |
| Null rate | Fraction of nulls in a column | 0.2 = 2 nulls in 10 rows |
| Distinct count | Number of distinct values | COUNT(DISTINCT passage_id) |
| Duplicate count | Rows minus distinct keys | 10 rows, 8 ids = 2 dupes |
| Approximate quantile | Estimated distribution point | approx_quantile(score, 0.5) |
| Predicate pushdown | Filters skip unread row groups | WHERE source = 'b1' |
| Zero-copy read | Querying without loading frames | view over read_parquet |
| Columnar storage | Values stored column by column | Parquet layout |
| Row group | Independently readable row chunk | min/max metadata per group |
| Profile table | Stored measurements gates query | column_profile |
| Quality gate | Threshold check over the profile | null rate < 0.05 |
| Data skew | Asymmetric value distribution | scores clustered near 0.9 |
| All-null column | Column with null rate 1.0 | dead extractor signal |
| COUNT DISTINCT | Exact distinct-value aggregate | COUNT(DISTINCT text) |
| FILTER clause | Conditional aggregate | COUNT(*) FILTER (WHERE ...) |
| In-place query | Querying the stored file directly | no import step |
| Division of labor | Polars cleans, DuckDB measures | ADR-0011 boundary |
| Descriptive statistics | Counts, min, max, quantiles | SUMMARIZE output |
| Schema drift | Stored shape differs from expected | 4 rows expected, 5 found |
| Median | 50th percentile center | robust to outliers |
| Gold Parquet | Cleaned corpus artifact | gates read this file |

---

## Alphabetical Glossary

### All-null column

**Definition:** A column whose null rate is 1.0: every value missing. Either a
dead extractor or a legitimately unfilled column. **See also:** Null rate.

### Approximate quantile

**Definition:** An estimated distribution point computed in one pass without
sorting. Shows shape, never asserted exactly. **See also:** Median, Data skew.

### Columnar storage

**Definition:** Storing each column's values together, so a query reading two
columns skips the rest. **See also:** Row group.

### COUNT DISTINCT

**Definition:** The exact distinct-value aggregate; nulls are ignored.
**See also:** Distinct count.

### Data skew

**Definition:** Asymmetric distribution, for example scores clustered high with
a low tail. Quantiles reveal it; averages hide it. **See also:** Median.

### Descriptive statistics

**Definition:** Counts, nulls, min, max, and quantiles per column: the
SUMMARIZE output. **See also:** Profile table.

### Distinct count

**Definition:** The number of distinct values in a column. Compared against row
count, the gap is the duplicate count. **See also:** Duplicate count.

### Division of labor

**Definition:** Polars owns cleaning and transformation; DuckDB owns profiling
and measurement, per ADR-0011, with the Parquet file as the boundary.

### Duplicate count

**Definition:** Rows minus distinct keys: the headline retrieval-health number.
**See also:** Distinct count.

### FILTER clause

**Definition:** A conditional aggregate: `COUNT(*) FILTER (WHERE ...)` counts
only matching rows. **See also:** Null rate.

### Gold Parquet

**Definition:** The cleaned corpus artifact Polars writes and DuckDB profiles.
**See also:** In-place query.

### In-place query

**Definition:** Querying the stored file directly through `read_parquet`, with
no import step and no eager frame. **See also:** Zero-copy read.

### Median

**Definition:** The 50th percentile: the robust center, unlike the mean under
skew. **See also:** Approximate quantile.

### Null rate

**Definition:** The fraction of nulls in a column, with an exact expectation
to assert. **See also:** All-null column.

### Predicate pushdown

**Definition:** Pushing query filters into the file read so non-matching row
groups are skipped undecided. **See also:** Row group.

### Profile table

**Definition:** Stored per-column measurements the quality gates query instead
of recomputing. **See also:** Quality gate.

### Quality gate

**Definition:** A threshold check over the profile table, for example null rate
under limit or duplicate count at zero. **See also:** Profile table.

### read_parquet

**Definition:** The DuckDB function querying Parquet where it sits, keeping the
profile step in near-constant memory. **See also:** In-place query.

### Row group

**Definition:** An independently readable chunk of Parquet rows carrying min/max
metadata that pushdown uses to skip. **See also:** Predicate pushdown.

### Schema drift

**Definition:** The stored shape differing from expectation, caught when the
SUMMARIZE row count stops matching the column count. **See also:** SUMMARIZE.

### SUMMARIZE

**Definition:** The one-query column overview: one row per column with counts,
nulls, min, max, and approximate quantiles. **See also:** Descriptive statistics.

### Zero-copy read

**Definition:** Querying through a view over `read_parquet` without loading the
corpus into memory. **See also:** In-place query.

---

## Related Concepts

- **Parquet layout**: row groups and min/max metadata make pushdown possible (topic 07)
- **Quality gates**: threshold judges over the profile table (topic 11)
- **Dedup contract**: what the duplicate count guards (topic 05)

## Key Takeaways

1. Profile the stored file in place with read_parquet.
2. SUMMARIZE first, targeted queries second, profile table for the gates.
3. Assert exact rates and counts; read approximate shapes, never assert them.
