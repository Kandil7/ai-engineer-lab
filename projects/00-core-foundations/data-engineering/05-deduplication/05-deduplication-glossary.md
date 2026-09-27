# Data Engineering 05: Deduplication — Glossary

## Quick Reference Table

| Term | Definition | Example |
|------|-----------|---------|
| Deduplication | Removing duplicate rows | same passage twice |
| Stable key | Exact-dedup identifier | passage_id |
| Content hash | Hash of normalized text | sha256 |
| Near-duplicate | Similar but not identical content | one typo apart |
| Ingest-time dedup | Preventing duplicates at write | upsert + hash check |
| Cleanup dedup | Periodic job repairing past duplicates | legacy data |
| Edit detection | Same key, different content | hash comparison |

---

## Alphabetical Glossary

### Cleanup dedup

**Definition:** A periodic job scanning for and removing duplicates that
already exist. The safety net for legacy data and pipeline bugs.

**Example:**
```python
# nightly job: find same content_hash, keep one
```

**Related concepts:** Ingest-time dedup, Content hash

---

### Content hash

**Definition:** A hash of the normalized text identifying exact content.
Changes when content changes — the edit-detection tool.

**Example:**
```python
hashlib.sha256(text.encode("utf-8")).hexdigest()
```

**Related concepts:** Near-duplicate, Edit detection

---

### Deduplication

**Definition:** Removing duplicate rows so each passage exists once.
Prevents split relevance and polluted citations.

**Example:**
```python
# two rows, same passage_id -> keep one
```

**Related concepts:** Stable key, Content hash

---

### Edit detection

**Definition:** Detecting that a passage changed: same key, different
content hash. The roadmap's "a single edited page is detected" check.

**Example:**
```python
# passage_id same, content_hash different -> edited, re-index
```

**Related concepts:** Content hash, Stable key

---

### Ingest-time dedup

**Definition:** Preventing duplicates at write time via upsert by key and a
hash check. Cheaper than cleanup; the default.

**Example:**
```python
# upsert by passage_id: a duplicate never exists
```

**Related concepts:** Cleanup dedup, Upsert

---

### Near-duplicate

**Definition:** Content that is similar but not identical — one typo, a
reflowed paragraph. Detected by similarity, decided by a human.

**Example:**
```python
# same passage with one typo: review queue, not auto-delete
```

**Related concepts:** Content hash, Deduplication

---

### Stable key

**Definition:** The identifier identifying the same logical row. The exact
dedup tool: same key means same passage.

**Example:**
```python
# passage_id = "b1:p7:0"
```

**Related concepts:** Deduplication, Edit detection

---

## Related Concepts

- **Idempotency**: upserts prevent duplicates at write (topic 03)
- **Provenance**: dedup must keep the right source (topic 06)
- **Content hashing**: the edit-detection primitive

## Key Takeaways

1. Dedup by stable key at ingest.
2. Content hashing detects edits.
3. Near-dedup is a human review queue.
4. Test both halves of dedup.