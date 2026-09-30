# Data Engineering 06: Provenance and Versioning

## Topic Overview

Provenance answers "where did this come from?" and versioning answers "which version of the source
produced this?" Together they make every passage traceable to its origin and every re-ingest
auditable. For a knowledge system that cites its sources, provenance is not optional metadata; it is
the mechanism that makes a citation verifiable.

This lecture covers the provenance fields, source versioning, tracing a passage to its origin, stale
detection by version comparison, and the audit trail that makes the data trustworthy for citation.

The strongest rule here is that tracing fails loudly rather than guessing. A passage that cannot be
traced is a data-integrity failure; returning a best-guess origin would silently corrupt the citation
chain that the whole RAG system depends on.

## Learning Objectives

By the end of this lecture, you will be able to:

1. Record provenance on every passage (`book_id`, `page`, `source_version`, `path`).
2. Version sources so re-ingests are attributable.
3. Trace any passage to its origin in one lookup.
4. Detect source changes by version comparison.
5. Build the audit trail that makes data trustworthy.
6. Explain why tracing must fail loudly.

## Prerequisites

- Data Engineering 02 (schemas) for the provenance fields and 01 (ETL) for the load.

---

## 1. The Provenance Fields

### The four fields

Every passage carries its origin: `book_id` (which book), `page` (where), `source_version` (which
version of the source), and optionally `path` (the original file):

```python
{"book_id": "b1", "page": 7, "source_version": "v1", "path": "book_p7.txt"}
```

### Why mandatory

The roadmap's exit test is that every passage can be traced to its origin, and that is satisfied only
when these fields are mandatory, not optional. An optional provenance field is one that is missing
exactly when it is needed.

### The schema link

The provenance fields are part of the schema (Data Engineering 02), so they are enforced structurally
at construction. A passage without provenance cannot exist, which is what removes the class of
untraceable data.

## 2. Source Versioning

### What a version is

A source version identifies a specific snapshot of the source material. When a book is re-ingested,
the version changes; when the content is unchanged, the version stays.

### What it buys

Versioning makes re-ingests attributable: a passage with `source_version: v2` came from the v2
snapshot, and its content hash (Data Engineering 05) says whether the content changed. Without
versioning, a re-ingest silently replaces data and the change is lost.

### The link to the cache and the index

The source version is the same version that appears in the embedding cache key (Embeddings 03) and the
answer cache key (RAG System 06), so a source change invalidates the downstream artifacts
consistently.

## 3. Tracing to Origin

### The lookup

```python
def trace(passage, sources):
    source = sources[passage["book_id"]][passage["source_version"]]
    return source.locate(passage["page"])
```

Tracing is a lookup: passage, then book and version, then the source snapshot, then the original
text. It is a chain, and the whole chain must resolve.

### Failing loudly

If any link is missing, the trace fails loudly rather than returning a guess:

```python
broken = {"book_id": "b1", "page": 1, "source_version": "v9"}
# raises KeyError("unknown version v9")
```

A passage that cannot be traced is a data-integrity failure. Returning a best-guess origin would
silently corrupt the citation chain, which is worse than a visible failure.

### Why it matters for RAG

A RAG answer cites a passage; the citation resolves to the passage's origin. If the trace can fail
silently, the citation can point at the wrong source, and the user's verification of the answer is
misled. Loud failure is the honest behavior.

## 4. Detecting Source Changes

### The comparison

Compare the current source snapshot against the version recorded on the passage:

```python
def is_stale(passage, current):
    """True if the passage's source version is not the current one."""
    return current.get(passage["book_id"]) != passage["source_version"]
```

If the source changed (a new version), the passage is stale and must be re-ingested.

### Why staleness matters

A stale passage is grounded in a superseded source, so a faithful answer can still be wrong
(RAG System 07). Detecting it at the source level is how the pipeline knows which passages to refresh.

### The link to the edit test

This is the source-level version of the "single edited page is detected" check: the version comparison
flags what needs refresh, and the content hash flags what changed within a version.

## 5. The Audit Trail

### What it is

Provenance plus versioning is the audit trail: for any passage, you can state which source version
produced it and whether it is current. For any answer, you can trace each claim to the passage, and
each passage to its source version.

### Why it matters

The audit trail is what makes the data trustworthy for citation. It is also what makes an incident
review possible: when a wrong answer is traced to a stale source, the audit trail says which passage
and which version, and the fix is targeted.

### The retention question

The source snapshots themselves must be retained (or archived) for the trace to resolve over time.
Object storage with versioning (Data Engineering 07) is where the snapshots live, and immutability
keeps an old version available for the trace.

## Real-World Application

- Recording `book_id`, `page`, and `source_version` on every Athar passage so an answer's citation can
  be traced to the exact source snapshot.
- Re-ingesting a corrected book as `v2` so old passages are flagged stale and refreshed.
- Failing loudly when a passage references a version that is no longer available, rather than guessing.
- Keeping source snapshots in versioned object storage so old citations still resolve.

## Common Mistakes

1. **Provenance fields optional.** Passages that cannot be traced.
2. **No source versioning.** Re-ingests un-attributable and silent.
3. **Tracing that returns a guess.** The citation chain is silently corrupted.
4. **Ignoring source changes.** Stale passages served as current.
5. **Not retaining source snapshots.** Old citations cannot resolve.

## Key Takeaways

1. Provenance fields are mandatory, not optional, and are enforced by the schema.
2. Source versions make re-ingests attributable and drive downstream invalidation.
3. Tracing fails loudly, never guesses; an untraceable passage is a data-integrity failure.
4. Version comparison detects stale passages, the source-level version of edit detection.
5. Provenance plus versioning is the audit trail that makes citations verifiable.

## Self-Check Questions

1. Why must provenance fields be mandatory rather than optional?
2. What does source versioning make possible, and where else does the version appear?
3. Why must tracing fail loudly instead of returning a best guess?
4. How does version comparison detect a stale passage?
5. What does the audit trail let you do that un-versioned data cannot?

## Further Reading / Connections

- Data Engineering 02 (schemas) and 05 (deduplication) — the schema fields and the content hash.
- Data Engineering 07 (Parquet and object storage) — where snapshots are retained.
- RAG System 07 (context failure modes) — stale material as a failure mode.
- Arabic NLP 01 (Arabic text fundamentals) — the original text the trace resolves to.
