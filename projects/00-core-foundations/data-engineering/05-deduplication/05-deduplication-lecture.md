# Data Engineering 05: Deduplication

## 🎯 Topic Overview

Duplicates corrupt retrieval: the same passage indexed twice splits its
relevance and pollutes citations. Deduplication removes them — at ingest
time by design, and as a cleanup when they slip through. This lecture covers
exact and fuzzy deduplication, the stable-key approach, and the roadmap's
"a single edited page is detected" requirement.

## 📚 Learning Objectives

By the end of this lecture, you will be able to:

1. Deduplicate exactly by stable key (passage_id)
2. Detect near-duplicates with content hashing and similarity
3. Detect a single edited page (same key, different content)
4. Choose dedup at ingest vs cleanup by cost
5. Test that dedup never removes distinct passages

---

## 1. Exact Dedup by Key

The stable key from topic 03 is the exact-dedup tool: two rows with the same
`passage_id` are the same passage. Dedup at ingest means the upsert never
creates a duplicate in the first place. Exact dedup by key is cheap and
correct — it is the baseline every other approach is measured against.

## 2. Content-Based Dedup

When the same content arrives under different keys (re-ingested from a
different source, or a page duplicated across books), key-based dedup
misses it. Content hashing catches exact duplicates: hash the normalized
text, and identical content maps to the same hash. This is the "detect a
single edited page" tool — the hash changes when the content changes.

```python
import hashlib


def content_hash(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()
```

## 3. Near-Duplicate Detection

Near-duplicates (a page with one typo, a reflowed paragraph) share content
but not hashes. Detecting them needs similarity: token overlap, shingling,
or embedding distance. For a corpus like Athar, near-dedup is usually a
review queue, not an automatic delete — a human decides whether two similar
passages are truly redundant. Automatic near-dedup risks deleting distinct
content.

## 4. Ingest-Time vs Cleanup

Ingest-time dedup (upsert by key, hash check on write) prevents duplicates
from existing. Cleanup dedup (a periodic job scanning for duplicates)
repairs past mistakes. Ingest-time is cheaper and should be the default;
cleanup is the safety net for legacy data and pipeline bugs. The roadmap's
exit test — "a single edited page is detected" — is a cleanup-style check
that belongs in CI.

## 5. Testing Dedup

```python
def test_dedup_never_removes_distinct(tmp_path):
    rows = [passage_a, passage_b, passage_a_duplicate]
    result = dedup(rows)
    assert len(result) == 2  # duplicate removed
    assert passage_a in result  # original kept
    assert passage_b in result  # distinct kept
```

The test has two halves: duplicates are removed, and distinct passages are
never removed. The second half is the one that catches over-aggressive
dedup.

## Common Mistakes

- Key-based dedup missing content duplicated under different keys.
- Content hashing treating an edited page as a new passage (no edit detection).
- Automatic near-dedup deleting distinct content.
- Testing only that duplicates are removed, not that distinct content survives.

## Key Takeaways

1. Exact dedup by stable key at ingest.
2. Content hashing detects exact duplicates and edited pages.
3. Near-dedup is a review queue, not an automatic delete.
4. Test both halves: duplicates removed, distinct kept.