# SQL 05: Advanced Filtering — Glossary

## Quick Reference Table

| Term | Definition | Example |
|------|-----------|---------|
| IN | Membership test against a value list/subquery | repo in (...) |
| BETWEEN | Inclusive range test (endpoints included) | date windows |
| LIKE / ILIKE | Pattern match, case-sensitive / insensitive | prefix search |
| IS NULL | The only correct null test | missing summaries |
| Three-valued logic | TRUE/FALSE/UNKNOWN: NULL poisons AND/OR/NOT | WHERE traps |
| Boolean precedence | NOT > AND > OR; parentheses decide the rest | explicit grouping |
| Sargable | Filter form allowing index use | bare column comparisons |

---

## Alphabetical Glossary

### BETWEEN

**Definition:** Inclusive range predicate — both endpoints match. Date
windows and numeric bands without off-by-one fence-posting.

**Example:**
```sql
WHERE created_at BETWEEN '2026-01-01' AND '2026-02-01'  -- inclusive both ends
```

**Related concepts:** Sargable, IN

---

### Boolean precedence

**Definition:** NOT binds tightest, then AND, then OR. Unparenthesized mixed
conditions read differently than intended — parentheses are documentation.

**Example:**
```sql
WHERE a AND b OR c   -- means (a AND b) OR c; write the parens anyway
```

**Related concepts:** Three-valued logic

---

### ILIKE / LIKE

**Definition:** Pattern matching (`%` any run, `_` one char); ILIKE folds
case. Leading `%` defeats B-trees — trigram indexes (GIN) rescue suffix
search.

**Example:**
```sql
WHERE filename ILIKE '%.py'  -- extension filter, case-blind
```

**Related concepts:** GIN index, Sargable

---

### IN

**Definition:** Membership test against a list or subquery. The set-membership
predicate; long literal lists belong in a temp table or join instead.

**Example:**
```sql
WHERE repo IN ('devmate', 'lab')  -- small sets inline, big sets joined
```

**Related concepts:** BETWEEN, EXISTS

---

### IS NULL

**Definition:** Null test — the only one, since `= NULL` is never true.
Every nullable filter needs its explicit IS NULL branch or silently drops rows.

**Example:**
```sql
WHERE summary IS NULL  -- unprocessed chunks, not empty ones
```

**Related concepts:** NULL, Three-valued logic

---

### Sargable

**Definition:** Search-ARGument-ABLE: filter forms the planner can satisfy
with an index (bare column vs constant). Functions on columns kill it.

**Example:**
```sql
WHERE created_at >= '2026-01-01'       -- sargable: index seek
WHERE date_trunc('day', created_at) = ...  -- not: full scan computes per row
```

**Related concepts:** Indexes, EXPLAIN

---

### Three-valued logic

**Definition:** SQL's TRUE/FALSE/UNKNOWN: any comparison with NULL yields
UNKNOWN, and WHERE keeps only TRUE. Rows vanish silently — the classic
filtering trap.

**Example:**
```sql
WHERE NOT (lang = 'py')  -- NULL langs excluded too: UNKNOWN is not TRUE
```

**Related concepts:** IS NULL, Boolean precedence

---

## Related Concepts

- **EXISTS**: the correlated semi-join alternative to big IN lists
- **Metadata filters**: these predicates over chunk payloads (vector-stores 06)
- **GIN trigrams**: pg_trgm rescuing LIKE '%...%' queries

## Key Takeaways

1. NULL poisons logic — test with IS, reason in three values.
2. Parenthesize mixed boolean conditions, always.
3. Keep filters sargable or pay per row.
