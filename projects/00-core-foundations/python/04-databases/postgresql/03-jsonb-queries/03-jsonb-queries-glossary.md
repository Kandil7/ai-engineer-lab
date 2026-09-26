# Postgres 03: JSONB Queries — Glossary

## Quick Reference Table

| Term | Definition | Example |
|------|-----------|---------|
| JSONB | Parsed binary JSON: normalized, indexed, queryable | metadata columns |
| `->` | Extraction returning jsonb (chainable) | meta -> 'repo' |
| `->>` | Extraction returning text (terminal) | meta ->> 'language' |
| `#>` | Path extraction over nested structure | meta #> '{span,lines}' |
| `@>` | Containment: document includes this structure | GIN fast path |
| `?` / `?|` / `?&` | Key existence: one / any / all | meta ? 'repo' |
| GIN index | Generalized inverted index over JSONB paths | path query accelerator |

---

## Alphabetical Glossary

### `#>` operator

**Definition:** JSONB path extraction taking a text array path into nested
structure. Powerful, and the slow path in WHERE clauses without index support.

**Example:**
```sql
meta #> '{span,lines}'  -- nested value, still jsonb
```

**Related concepts:** `->`, `@>`

---

### `->` operator

**Definition:** JSONB field extraction returning jsonb. Chainable for
navigation; must terminate in `->>` before text comparison.

**Example:**
```python
# meta -> 'repo' = '"devmate"' (jsonb!) — comparing to 'devmate' fails
```

**Related concepts:** `->>`, `@>`

---

### `->>` operator

**Definition:** JSONB field extraction returning text. The terminal step
before comparison, display, or joining to text columns.

**Example:**
```sql
WHERE meta ->> 'language' = 'python'  -- text to text: correct
```

**Related concepts:** `->`, `@>`

---

### `@>` operator

**Definition:** Containment test: left document includes the right structure.
The GIN-indexable fast path for JSONB filtering.

**Example:**
```sql
WHERE meta @> '{"language": "python"}'  -- Bitmap Index Scan with GIN
```

**Related concepts:** GIN index, Metadata filter

---

### `?` / `?|` / `?&` operators

**Definition:** Key-existence tests: single key, any-of list, all-of list.
Schema-shape checks without value comparison.

**Example:**
```sql
WHERE meta ?& array['repo', 'chunk_type']  -- both keys present
```

**Related concepts:** `@>`, GIN index

---

### GIN index

**Definition:** Generalized Inverted Index: maps keys/elements to containing
rows. Makes `@>` and existence operators fast on JSONB (and arrays, trigrams).

**Example:**
```sql
CREATE INDEX ON chunks USING GIN (meta);
```

**Related concepts:** `@>`, EXPLAIN

---

### JSONB

**Definition:** Postgres binary JSON: parsed on write, normalized, indexable.
The only sane JSON column type unless byte-exact round-trips are required.

**Example:**
```python
mapped_column(JSONB, name="metadata")  # DevMate chunk payloads
```

**Related concepts:** `json`, GIN index

---

## Related Concepts

- **EXPLAIN**: proves the index is used (Bitmap Index Scan, not Seq Scan)
- **Metadata filter**: the retrieval use case for these operators (vector-stores 06)
- **json**: text JSON, parse-on-read, uninterested in indexes

## Key Takeaways

1. Chain with `->`, terminate with `->>`, filter with `@>`.
2. `jsonb` + GIN is the production combination.
3. The EXPLAIN output is the receipt.
