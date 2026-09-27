# Data Engineering 04: Checkpointing — Glossary

## Quick Reference Table

| Term | Definition | Example |
|------|-----------|---------|
| Checkpoint | Record of completed work for resume | last committed page |
| Atomic write | Whole-or-nothing write, no torn records | temp file + rename |
| Resume | Continue after the last committed unit | no restart from zero |
| Torn write | Half-written record corrupting state | crash mid-append |
| Stale checkpoint | Slightly behind the true position | safe with idempotency |
| Commit unit | The smallest unit of completed work | one page, one batch |
| Resumable pipeline | Fails and continues, not restarts | checkpointed ingest |

---

## Alphabetical Glossary

### Atomic write

**Definition:** A write that is all-or-nothing: either the whole checkpoint
is written or none of it is. Prevents torn records from corrupting the
resume position.

**Example:**
```python
# write tmp file, then os.replace(tmp, checkpoint) — atomic on most FS
```

**Related concepts:** Torn write, Checkpoint

---

### Checkpoint

**Definition:** A durable record of completed work: the last committed unit,
enough to answer "what is done?" unambiguously.

**Example:**
```python
{"book_id": "b1", "last_committed_page": 42, "source_version": "v1"}
```

**Related concepts:** Resume, Commit unit

---

### Commit unit

**Definition:** The smallest unit of completed work a checkpoint records —
one page, one batch, one file. The granularity of resume.

**Example:**
```python
# checkpoint advances one committed page at a time
```

**Related concepts:** Checkpoint, Resume

---

### Resumable pipeline

**Definition:** A pipeline that fails and continues from its checkpoint
instead of restarting from zero. The payoff of checkpointing.

**Example:**
```python
# hour-3 crash resumes at page 42, not page 1
```

**Related concepts:** Checkpoint, Resume

---

### Resume

**Definition:** Continuing after the last committed unit. Must not redo
completed work and must not skip uncommitted work.

**Example:**
```python
# read checkpoint, start at last_committed_page + 1
```

**Related concepts:** Checkpoint, Commit unit

---

### Stale checkpoint

**Definition:** A checkpoint slightly behind the true position. Safe to
resume from when loads are idempotent — re-processing a committed unit is
harmless.

**Example:**
```python
# checkpoint says page 42, page 43 was committed: idempotency absorbs it
```

**Related concepts:** Idempotency, Resume

---

### Torn write

**Definition:** A half-written record from a crash mid-write. Corrupts the
checkpoint and the resume position. Prevented by atomic writes.

**Example:**
```python
# appending to a checkpoint file: crash mid-append = torn record
```

**Related concepts:** Atomic write, Checkpoint

---

## Related Concepts

- **Idempotency**: makes stale-checkpoint resume safe (topic 03)
- **Deduplication**: cleans up any overlap after resume (topic 05)
- **Provenance**: checkpoint state is part of the audit trail (topic 06)

## Key Takeaways

1. Checkpoints make failures resume, not restart.
2. Write checkpoints atomically.
3. Idempotency backs up stale checkpoints.