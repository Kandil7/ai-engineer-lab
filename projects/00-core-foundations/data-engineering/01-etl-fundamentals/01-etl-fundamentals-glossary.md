# Data Engineering 01: ETL Fundamentals — Glossary

## Quick Reference Table

| Term | Definition | Example |
|------|-----------|---------|
| ETL | Extract, transform, load pipeline | raw books → passages |
| Extract | Read-only, resumable source reading | page files, DB, API |
| Transform | Pure business logic: clean, normalize, chunk | two-text discipline |
| Load | Idempotent write to destination | JSONL, DB, vector store |
| Batch | Bounded chunks on a schedule | nightly corpus job |
| Stream | Events processed as they arrive | live feed |
| Determinism | Same input → same output, always | no timestamps in output |
| Idempotency | Re-running leaves identical state | no duplicates |

---

## Alphabetical Glossary

### Batch

**Definition:** Processing bounded chunks of data on a schedule or trigger.
Right for finite corpora that change rarely, like Athar's books.

**Example:**
```python
# a new book triggers a batch job, not a stream
```

**Related concepts:** Stream, ETL

---

### Determinism

**Definition:** Identical input produces identical output. No timestamps in
output, no unseeded randomness, no iteration-order dependence.

**Example:**
```python
# re-running the same pages yields byte-identical JSONL
```

**Related concepts:** Idempotency

---

### ETL

**Definition:** Extract, transform, load — the pipeline turning raw source
material into queryable data. The backbone of every data system.

**Example:**
```python
extract(source) -> transform(pages) -> load(passages, sink)
```

**Related concepts:** Extract, Transform, Load

---

### Extract

**Definition:** The read-only stage pulling data from a source. Resumable
and never destructive — the source is never modified or deleted.

**Example:**
```python
def extract(source) -> list[RawPage]: ...
```

**Related concepts:** ETL, Transform

---

### Idempotency

**Definition:** The property that running an operation twice leaves the same
state as running it once. The load stage must be idempotent so re-runs
never duplicate.

**Example:**
```python
# upsert by passage_id: second run updates, never duplicates
```

**Related concepts:** Determinism, Load

---

### Load

**Definition:** The write stage sending transformed data to its destination.
Must be idempotent and report rows written.

**Example:**
```python
def load(passages, sink) -> int: ...  # returns rows written
```

**Related concepts:** ETL, Idempotency

---

### Stream

**Definition:** Processing events as they arrive, continuously. Adds latency
complexity; choose only when freshness demands it.

**Example:**
```python
# live chat logs stream; a book corpus does not
```

**Related concepts:** Batch, ETL

---

### Transform

**Definition:** The business-logic stage: cleaning, normalization, chunking,
enrichment. Pure where possible — same input, same output.

**Example:**
```python
# clean -> normalize (two-text) -> chunk into passages
```

**Related concepts:** ETL, Determinism

---

## Related Concepts

- **Provenance**: tracing every row to its source (topic 06)
- **Checkpointing**: resuming interrupted pipelines (topic 04)
- **Deduplication**: removing accidental duplicates (topic 05)

## Key Takeaways

1. Extract read-only, transform pure, load idempotent.
2. Batch for finite corpora; stream only for freshness.
3. Determinism plus idempotency makes re-runs safe.