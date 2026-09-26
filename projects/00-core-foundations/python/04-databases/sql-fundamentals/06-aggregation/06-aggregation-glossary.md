# SQL 06: Aggregation — Glossary

## Quick Reference Table

| Term | Definition | Example |
|------|-----------|---------|
| COUNT / SUM / AVG / MIN / MAX | Set functions collapsing groups to scalars | eval metrics |
| GROUP BY | Partitions rows; one output row per group | per-repo counts |
| HAVING | Filters groups after aggregation (WHERE can't) | repos with >100 chunks |
| WHERE vs HAVING | Row filter before grouping vs group filter after | staged pipeline |
| COUNT(*) vs COUNT(col) | All rows vs non-null values in col | total vs answered |
| Scalar aggregate | No GROUP BY: whole set collapses to one row | grand totals |
| Eval metrics SQL | Aggregation as measurement: means, rates, percentiles | cost/query dashboards |

---

## Alphabetical Glossary

### COUNT / SUM / AVG / MIN / MAX

**Definition:** Aggregate functions reducing a group to one value. NULLs are
skipped (except COUNT(*)) — averages silently exclude missing data.

**Example:**
```sql
AVG(score)  -- mean over non-null scores only; know your denominator
```

**Related concepts:** GROUP BY, COUNT(*) vs COUNT(col)

---

### COUNT(*) vs COUNT(col)

**Definition:** COUNT(*) counts rows; COUNT(col) counts non-null values.
Mixing them up misstates coverage — the "answered rate" bug.

**Example:**
```sql
COUNT(*) AS total, COUNT(answer) AS answered  -- coverage = answered/total
```

**Related concepts:** NULL, Eval metrics SQL

---

### Eval metrics SQL

**Definition:** Aggregation as measurement harness: means, rates, p50 via
percentile_cont, cost sums — the SQL behind every dashboard in weeks 2–7.

**Example:**
```sql
SELECT AVG(latency_ms), SUM(cost_usd)/1e6 FROM eval_runs;  -- the $/query view
```

**Related concepts:** GROUP BY, Scalar aggregate

---

### GROUP BY

**Definition:** Row partitioner: one output row per distinct group key, with
aggregates computed within each. Every non-aggregated SELECT column must be
grouped (or functionally dependent).

**Example:**
```sql
SELECT repo, COUNT(*) FROM chunks GROUP BY repo;  -- per-repo inventory
```

**Related concepts:** HAVING, WHERE vs HAVING

---

### HAVING

**Definition:** Post-aggregation group filter. WHERE can't see aggregates
(they don't exist yet at row-filter time) — HAVING exists for that stage.

**Example:**
```sql
GROUP BY repo HAVING COUNT(*) > 100  -- busy repos only
```

**Related concepts:** WHERE vs HAVING, GROUP BY

---

### Scalar aggregate

**Definition:** Aggregation with no GROUP BY: the whole input collapses to a
single row. Grand totals, global means, dashboard headline numbers.

**Example:**
```sql
SELECT COUNT(*), AVG(score) FROM eval_scores;  -- one row, whole table
```

**Related concepts:** GROUP BY, Eval metrics SQL

---

### WHERE vs HAVING

**Definition:** The staged pipeline: WHERE filters rows before grouping
(cheap, indexed), HAVING filters groups after aggregation. Swapping them is
either wrong or slow.

**Example:**
```sql
WHERE date >= '...' GROUP BY repo HAVING COUNT(*) > 10  -- filter, group, filter
```

**Related concepts:** GROUP BY, HAVING

---

## Related Concepts

- **percentile_cont**: ordered-set aggregates for p50/p95 in SQL
- **Window functions**: per-row aggregates without collapsing (advanced/)
- **Cost-per-query view**: the week-4 SQL sprint deliverable built from these

## Key Takeaways

1. WHERE rows, HAVING groups — order matters.
2. Know every denominator: COUNT(*) vs COUNT(col).
3. Aggregation is the measurement language of evals and billing.
