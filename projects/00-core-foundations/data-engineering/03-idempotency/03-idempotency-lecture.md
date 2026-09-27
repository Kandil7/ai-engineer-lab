# Data Engineering 03: Idempotency

## 🎯 Topic Overview

Idempotency is the property that makes re-runs safe: running an operation
twice leaves the same state as running it once. It is the foundation of the
roadmap's exit test — "running twice does not duplicate data." This lecture
covers what makes an operation idempotent, the upsert pattern, and how to
test for it.

## 📚 Learning Objectives

By the end of this lecture, you will be able to:

1. Explain idempotency and why pipelines need it
2. Implement the upsert pattern keyed by a stable identifier
3. Make writes idempotent (insert-or-update, not blind insert)
4. Test idempotency by running twice and asserting identical state
5. Distinguish idempotent from merely retry-safe

---

## 1. What Idempotency Means

An operation is idempotent if applying it twice has the same effect as
applying it once. A blind `INSERT` is not idempotent — the second run
duplicates. An `INSERT ... ON CONFLICT DO UPDATE` is — the second run
updates the same row. The pipeline's load stage must be idempotent so a
crash-and-retry never corrupts the data.

```python
# NOT idempotent: second run duplicates
# INSERT INTO passages (id, text) VALUES (?, ?)

# Idempotent: second run updates the same row
# INSERT INTO passages (id, text) VALUES (?, ?)
#   ON CONFLICT (id) DO UPDATE SET text = EXCLUDED.text
```

## 2. The Stable Key

Idempotency needs a stable identifier: the same logical row must map to the
same key every run. For Athar, `passage_id` (book_id:page:index) is that
key. A key derived from content (a hash of the text) changes when the text
changes — which is correct for detecting edits but wrong for idempotent
upserts. Choose the key by what "the same row" means.

## 3. The Upsert Pattern

```python
def upsert(rows, sink):
    for row in rows:
        sink.upsert(
            key=row["passage_id"],
            values=row,
        )  # insert if absent, update if present
```

The upsert is the idempotent write primitive. It handles both the first run
(insert) and re-runs (update). The alternative — delete-then-insert — is
also idempotent but risks a window where data is missing if the insert
fails.

## 4. Testing Idempotency

```python
def test_idempotent_load(tmp_path):
    run_pipeline(tmp_path)  # first run
    first = read_all(tmp_path)
    run_pipeline(tmp_path)  # second run
    second = read_all(tmp_path)
    assert first == second  # identical state, no duplicates
```

The test is the exit criterion: run twice, assert identical state. This is
the roadmap's exact check, and it belongs in CI so a regression cannot
silently return.

## 5. Idempotent vs Retry-Safe

Retry-safe means a failed attempt can be retried without harm. Idempotent
means the operation itself is safe to repeat. They overlap but differ: a
retry-safe operation may still duplicate if the first attempt actually
succeeded before the failure was reported. Idempotency closes that gap —
the retry is safe because the operation is idempotent.

## Common Mistakes

- Blind inserts that duplicate on re-run.
- Keys derived from content that changes between runs.
- Delete-then-insert without handling the mid-window failure.
- Testing idempotency only on happy paths.

## Key Takeaways

1. Idempotency: twice equals once.
2. Upsert keyed by a stable identifier.
3. Test by running twice and asserting identical state.
4. Idempotency makes retries genuinely safe.