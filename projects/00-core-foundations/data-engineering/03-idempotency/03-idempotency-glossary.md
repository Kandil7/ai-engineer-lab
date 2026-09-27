# Data Engineering 03: Idempotency — Glossary

## Quick Reference Table

| Term | Definition | Example |
|------|-----------|---------|
| Idempotency | Twice equals once | re-run leaves same state |
| Stable key | Identifier mapping the same row every run | passage_id |
| Upsert | Insert-if-absent, update-if-present | ON CONFLICT DO UPDATE |
| Blind insert | Unconditional insert, duplicates on re-run | anti-pattern |
| Delete-then-insert | Idempotent but risky mid-window | missing-data window |
| Retry-safe | Failed attempt can be retried harmlessly | overlaps idempotency |
| Idempotency test | Run twice, assert identical state | CI gate |

---

## Alphabetical Glossary

### Blind insert

**Definition:** An unconditional insert that duplicates rows on re-run. The
anti-pattern idempotency exists to prevent.

**Example:**
```python
# INSERT INTO passages ...  # second run duplicates
```

**Related concepts:** Upsert, Idempotency

---

### Delete-then-insert

**Definition:** An idempotent write strategy that deletes a key's rows then
re-inserts them. Correct, but risks a window where data is missing if the
insert fails.

**Example:**
```python
# DELETE WHERE passage_id = ?; INSERT ...  # idempotent, risky window
```

**Related concepts:** Upsert, Idempotency

---

### Idempotency

**Definition:** The property that applying an operation twice has the same
effect as applying it once. The foundation of safe pipeline re-runs.

**Example:**
```python
# run twice -> identical state, no duplicates
```

**Related concepts:** Upsert, Stable key

---

### Idempotency test

**Definition:** The test that runs a pipeline twice and asserts identical
state. The roadmap's exit criterion, enforced in CI.

**Example:**
```python
run()
first = read_all()
run()
assert read_all() == first
```

**Related concepts:** Idempotency, Stable key

---

### Retry-safe

**Definition:** A failed attempt can be retried without harm. Overlaps
idempotency but differs: a retry-safe operation may still duplicate if the
first attempt succeeded before the failure was reported.

**Example:**
```python
# idempotency closes the retry gap: retry is safe because twice equals once
```

**Related concepts:** Idempotency

---

### Stable key

**Definition:** The identifier that maps the same logical row to the same
key every run. Content-derived keys change when text changes — wrong for
upserts.

**Example:**
```python
# passage_id = "b1:p7:0" — stable across runs
```

**Related concepts:** Upsert, Idempotency

---

### Upsert

**Definition:** Insert-if-absent, update-if-present, keyed by a stable
identifier. The idempotent write primitive.

**Example:**
```python
# INSERT ... ON CONFLICT (id) DO UPDATE SET text = EXCLUDED.text
```

**Related concepts:** Stable key, Idempotency

---

## Related Concepts

- **Checkpointing**: resuming without redoing completed work (topic 04)
- **Deduplication**: cleaning up past duplicates (topic 05)
- **Contracts**: the stable keys come from the schema (topic 02)

## Key Takeaways

1. Twice equals once.
2. Upsert by a stable key.
3. Test idempotency in CI.