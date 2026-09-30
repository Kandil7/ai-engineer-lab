# Data Engineering 05: Deduplication

## Topic Overview

Duplicates corrupt retrieval. The same passage indexed twice splits its relevance across two entries
and pollutes citations, because the answer may cite one copy while the other sits unused. Dedup
removes them: at ingest by design, and as a cleanup when they slip through. It is a small discipline
with an outsized effect on retrieval quality and citation fidelity.

This lecture covers exact dedup by key, content-based dedup and edit detection, near-duplicate
detection, the choice between ingest-time and cleanup dedup, and the two-half test that guards
against over-aggressive dedup.

The subtle risk is the opposite of the obvious one. Everyone worries about missing duplicates; the
test that catches real bugs is the one that asserts distinct passages are never removed.

## Learning Objectives

By the end of this lecture, you will be able to:

1. Deduplicate exactly by a stable key (`passage_id`).
2. Detect exact duplicates and edited pages with content hashing.
3. Explain near-duplicate detection and why it is a review queue.
4. Choose ingest-time versus cleanup dedup.
5. Test both halves: duplicates removed and distinct passages kept.
6. Explain why dedup is a retrieval-quality concern.

## Prerequisites

- Data Engineering 03 (idempotency) for the stable key.
- Data Engineering 06 (provenance) for the identity fields.

---

## 1. Exact Dedup by Key

### The tool

The stable key from idempotency is the exact-dedup tool: two rows with the same `passage_id` are the
same passage. Dedup at ingest means the upsert never creates a duplicate in the first place:

```python
def dedup_by_key(rows):
    """Exact dedup by passage_id: keep the last occurrence."""
    seen = {}
    for row in rows:
        seen[row["passage_id"]] = row
    return list(seen.values())
```

### Why it is the baseline

Exact dedup by key is cheap and correct, so it is the baseline every other approach is measured
against. If the key is right, exact dedup catches the common duplicate.

### Keeping the last occurrence

Keeping the last occurrence means a re-ingest of a corrected page wins over the old copy. The choice
is a policy, and it is deterministic, which matters for reproducibility (Data Engineering 01).

## 2. Content-Based Dedup and Edit Detection

### The gap in key-based dedup

The same content can arrive under different keys, for example re-ingested from a different source or
duplicated across books. Key-based dedup misses it because the keys differ.

### Content hashing

Hash the normalized text; identical content maps to the same hash:

```python
def content_hash(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()
```

Content hashing catches exact duplicates regardless of key, and it is half of the edit-detection tool.

### Edit detection

A page is edited when the same key has a different content hash than the stored one:

```python
def detect_edits(rows, index):
    return [
        r["passage_id"] for r in rows
        if r["passage_id"] in index
        and index[r["passage_id"]] != content_hash(r["text"])
    ]
```

This is the roadmap's "a single edited page is detected" check: the hash changes exactly when the
content changes, so a one-character edit is caught.

### Why not treat an edit as a new passage

The key is the identity; the hash is the content. An edit is the same passage with new content, so it
updates in place (Data Engineering 03), and the hash difference is the signal that it changed.

## 3. Near-Duplicate Detection

### The problem

Near-duplicates (a page with a typo, a reflowed paragraph, a title repeated in the body) share content
but not hashes. Hash-based dedup misses them.

### The methods

Near-duplicate detection uses similarity: token overlap, shingling, or embedding distance. The methods
find candidates that are close but not identical.

### Why it is a review queue

Automatic near-dedup risks deleting distinct content: two similar passages can be genuinely different
(for example, two similar hadith with different chains). For a corpus like Athar, near-dedup should
produce a review queue for a human to decide, not an automatic delete. The cost of deleting a distinct
passage is a wrong answer; the cost of keeping a near-duplicate is minor.

## 4. Ingest-Time Versus Cleanup

### Ingest-time

Ingest-time dedup (upsert by key, hash check on write) prevents duplicates from existing. It is
cheaper and should be the default, because a duplicate that never exists never has to be found.

### Cleanup

Cleanup dedup (a periodic job scanning for duplicates) repairs past mistakes and pipeline bugs. It is
the safety net for legacy data.

### The division

Ingest-time is prevention; cleanup is repair. A system needs both, because pipelines have bugs and
history has data that predates the current discipline. The roadmap's exit test ("a single edited page
is detected") is a cleanup-style check that belongs in CI so it runs continuously.

## 5. Testing Dedup

### The two halves

```python
def test_dedup_never_removes_distinct():
    rows = [passage_a, passage_b, passage_a_duplicate]
    result = dedup_by_key(rows)
    assert len(result) == 2            # duplicate removed
    assert any(r["passage_id"] == "b1:p1:0" for r in result)  # original kept
    assert any(r["passage_id"] == "b1:p2:0" for r in result)  # distinct kept
```

### Why the second half matters

The first half (duplicates removed) is easy to pass with an over-aggressive dedup. The second half
(distinct kept) is what catches a dedup that removes too much. Both halves are required for the test
to mean anything.

### The edit test

The edit test asserts that a changed page is flagged and an unchanged one is not:

```python
assert detect_edits([a_edited], index) == ["b1:p1:0"]
assert detect_edits([a], index) == []
```

Both directions matter: a detector that flags everything is as useless as one that flags nothing.

## Real-World Application

- Upserting Athar passages by `passage_id` so a re-ingest does not duplicate passages.
- Detecting a single edited page by its content hash changing so the ingest refreshes it.
- Building a near-duplicate review queue for similar hadith so a human decides redundancy.
- Running the dedup and edit-detection tests in CI so a regression cannot return.

## Common Mistakes

1. **Key-based dedup missing content duplicated under different keys.** Content hashing fills the gap.
2. **Treating an edited page as a new passage.** The key is the identity; the edit updates in place.
3. **Automatic near-dedup deleting distinct content.** Use a review queue.
4. **Testing only that duplicates are removed.** The distinct-kept half is the important one.
5. **No cleanup job.** Historical duplicates and pipeline bugs persist.

## Key Takeaways

1. Exact dedup by stable key at ingest is the baseline.
2. Content hashing detects exact duplicates regardless of key and detects edited pages.
3. Near-dedup is a review queue, not an automatic delete.
4. Ingest-time is prevention, cleanup is repair; a system needs both.
5. Test both halves: duplicates removed and distinct passages kept.

## Self-Check Questions

1. Why does key-based dedup miss content duplicated under different keys?
2. How does content hashing detect a single edited page?
3. Why should near-dedup be a review queue rather than an automatic delete?
4. What is the division of labor between ingest-time and cleanup dedup?
5. Why is "distinct passages kept" the more important half of the dedup test?

## Further Reading / Connections

- Data Engineering 03 (idempotency) and 06 (provenance) — the key and hashes this builds on.
- Data Engineering 01 (ETL) — where ingest-time dedup runs.
- Arabic NLP 02 (normalization) — the normalization before hashing.
- RAG System 01 (chunking) — where passage ids are assigned.
