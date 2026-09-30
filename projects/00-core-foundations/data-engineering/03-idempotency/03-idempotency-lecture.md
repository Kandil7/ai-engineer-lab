# Data Engineering 03: Idempotency

## Topic Overview

Idempotency is the property that makes re-runs safe: running an operation twice leaves the same
state as running it once. It is the foundation of the roadmap's exit test, that running twice does
not duplicate data, and it is the property that turns a fragile pipeline into a recoverable one.
Pipelines fail and get re-run; without idempotency, every re-run risks duplicating or corrupting the
data.

This lecture covers what makes an operation idempotent, the stable key that idempotency requires,
the upsert pattern as the idempotent write primitive, how to test idempotency by running twice, and
the distinction between idempotent and merely retry-safe.

The key design decision is the stable key. Idempotency depends on the same logical row mapping to
the same key every run, so the key must be chosen by what "the same row" means, not by convenience.

## Learning Objectives

By the end of this lecture, you will be able to:

1. Explain idempotency and why pipelines need it.
2. Implement the upsert pattern keyed by a stable identifier.
3. Make writes idempotent (insert-or-update, not blind insert).
4. Test idempotency by running twice and asserting identical state.
5. Distinguish idempotent from merely retry-safe.
6. Choose a stable key from the meaning of "the same row".

## Prerequisites

- Data Engineering 01 (ETL) for the load stage and 02 (schemas) for the row identity.

---

## 1. What Idempotency Means

### The definition

An operation is idempotent if applying it twice has the same effect as applying it once. A blind
`INSERT` is not idempotent: the second run duplicates. An `INSERT ... ON CONFLICT DO UPDATE` is:
the second run updates the same row.

```sql
-- NOT idempotent: second run duplicates
INSERT INTO passages (id, text) VALUES (?, ?);

-- Idempotent: second run updates the same row
INSERT INTO passages (id, text) VALUES (?, ?)
  ON CONFLICT (id) DO UPDATE SET text = EXCLUDED.text;
```

### Why pipelines need it

A pipeline that takes hours will fail: a network drop, a crash, a bad page. The load stage must be
idempotent so a crash-and-retry never corrupts the data. Without it, the safe recovery path does not
exist.

### The blast radius

A non-idempotent load's failure mode is data corruption that may not surface until a wrong answer
months later, which makes it one of the highest-value properties to get right and test.

## 2. The Stable Key

### What it is

Idempotency needs a stable identifier: the same logical row maps to the same key every run. For
Athar, `passage_id` (book_id:page:index) is that key.

### Choosing it by meaning

A key derived from content (a hash of the text) changes when the text changes, which is right for
detecting edits but wrong for idempotent upserts, because a re-run of the same logical row with new
content would insert a new row rather than update the existing one. Choose the key by what "the same
row" means:

```python
key = f"{book_id}:p{page}:{index}"  # stable identity
```

### The tradeoff

A stable identity key means an edited passage updates in place (with the edit detected by a content
hash, Data Engineering 05), while a content key would treat the edit as a new row. The two serve
different purposes, and the idempotent load wants the identity key.

## 3. The Upsert Pattern

### The primitive

The upsert is the idempotent write primitive: insert if absent, update if present.

```python
def upsert(self, key: str, values: dict) -> None:
    self._rows[key] = values  # insert if absent, replace if present
```

### Why upsert over delete-then-insert

Delete-then-insert is also idempotent in the end state, but it risks a window where the row is missing
if the insert fails. The upsert has no such window; the row is always present, in old or new form.

### The read-back

The read-back after an upsert is deterministic (ordered by key), so the idempotency test can compare
states exactly.

## 4. Testing Idempotency

### The test

Run the pipeline twice and assert identical state:

```python
store = UpsertStore()
run_pipeline(store, rows)  # first run
first = store.read_all()
run_pipeline(store, rows)  # second run
second = store.read_all()
assert first == second, "idempotent: identical state after re-run"
assert len(second) == 2, "no duplicates"
```

### The second half of the test

The test also checks that a changed row updates in place rather than inserting a new one:

```python
run_pipeline(store, changed)
assert len(store.read_all()) == 2, "update in place, no new row"
```

That assertion catches an upsert that inserts instead of updating.

### In CI

The idempotency test belongs in CI so a regression cannot silently return. It is the roadmap's exact
check, and it is cheap to run.

## 5. Idempotent Versus Retry-Safe

### The distinction

Retry-safe means a failed attempt can be retried without harm. Idempotent means the operation itself
is safe to repeat. They overlap but differ: a retry-safe operation can still duplicate if the first
attempt actually succeeded before the failure was reported.

### Why the distinction matters

The dangerous case is "succeeded but the success was not reported" (a timeout after the write
committed). The retry then repeats a successful operation. Idempotency closes that gap: the retry is
safe because the operation is idempotent, whether or not the first attempt committed.

### The production lesson

Do not rely on "the operation probably did not complete." The network makes that unknowable. Make
the operation idempotent and the question irrelevant.

## 6. Idempotency Plus Checkpointing

### The combination

Checkpointing (Data Engineering 04) records progress so a failed run resumes; idempotency ensures
that re-processing a unit near the checkpoint boundary is harmless. Together they make crash-and-resume
safe.

### Why both

A checkpoint alone can be slightly stale (the last commit may have happened after the checkpoint was
written). Idempotency absorbs the resulting small re-process. This is the production-grade version of
"run twice is safe": "crash and resume is safe."

## Real-World Application

- Upserting Athar passages by `passage_id` so a re-run of the ingest does not duplicate passages.
- Updating an edited passage in place rather than inserting a new row.
- Testing idempotency in CI so a load change cannot silently introduce duplication.
- Combining the idempotent load with checkpointing so an interrupted ingest resumes safely.

## Common Mistakes

1. **Blind inserts that duplicate on re-run.** The classic corruption.
2. **Keys derived from content that changes between runs.** Edits insert instead of update.
3. **Delete-then-insert without handling the mid-window failure.** A window of missing data.
4. **Testing idempotency only on happy paths.** The update-in-place case goes unchecked.
5. **Relying on "the operation probably did not complete."** The network makes it unknowable.

## Key Takeaways

1. Idempotency means twice equals once, and it is what makes re-runs safe.
2. The upsert keyed by a stable identity is the idempotent write primitive.
3. Test by running twice and asserting identical state, plus the update-in-place case.
4. Idempotency is stronger than retry-safety because it covers the "succeeded but not reported" case.
5. Idempotency plus checkpointing makes crash-and-resume safe.

## Self-Check Questions

1. Why is a blind insert not idempotent, and what replaces it?
2. Why is a stable identity key better than a content hash for idempotent upserts?
3. What does the second half of the idempotency test check, and what bug does it catch?
4. Why is idempotency stronger than retry-safety?
5. How do idempotency and checkpointing combine to make resume safe?

## Further Reading / Connections

- Data Engineering 01 (ETL) and 04 (checkpointing) — the pipeline and the resume property.
- Data Engineering 05 (deduplication) — the content hash that complements the identity key.
- RAG System 06 (caching) — the same deterministic-key discipline.
- `projects/04-ai-engineering/athar-lab/` — the deterministic CLI whose re-run is byte-identical.
