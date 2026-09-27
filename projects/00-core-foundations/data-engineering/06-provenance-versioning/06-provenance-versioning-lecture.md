# Data Engineering 06: Provenance and Versioning

## 🎯 Topic Overview

Provenance answers "where did this come from?" and versioning answers "which
version of the source produced this?" Together they make every passage
traceable to its origin — the roadmap's exit test — and every re-ingest
auditable. This lecture covers the provenance fields, source versioning,
and the audit trail.

## 📚 Learning Objectives

By the end of this lecture, you will be able to:

1. Record provenance on every passage: book_id, page, source_version, path
2. Version sources so re-ingests are attributable
3. Trace any passage to its origin in one query
4. Detect source changes via version comparison
5. Build the audit trail that makes data trustworthy

---

## 1. The Provenance Fields

Every passage carries its origin: `book_id` (which book), `page` (where),
`source_version` (which version of the source), and optionally `path` (the
original file). These four fields make the passage traceable. The roadmap's
exit test — "every passage can be traced to its origin" — is satisfied when
these fields are mandatory, not optional.

```python
# Provenance on every passage
{"book_id": "b1", "page": 7, "source_version": "v1", "path": "book_p7.txt"}
```

## 2. Source Versioning

A source version identifies a specific snapshot of the source material. When
a book is re-ingested, the version changes; when the content is unchanged,
the version stays. Versioning makes re-ingests attributable: a passage with
`source_version: v2` came from the v2 snapshot, and its content hash tells
you whether it changed. The version is the link between the passage and the
source's history.

## 3. Tracing to Origin

```python
def trace(passage, sources):
    source = sources[passage["book_id"]][passage["source_version"]]
    return source.locate(passage["page"])
```

Tracing is a lookup: passage → book_id/page/source_version → the source
snapshot → the original text. If any link is missing, the trace fails loudly
rather than returning a guess. A passage that cannot be traced is a data
integrity failure, not a minor gap.

## 4. Detecting Source Changes

Compare the current source snapshot against the version recorded on the
passage: if the source changed (new version, different content hash), the
passage is stale and must be re-ingested. This is the roadmap's "a single
edited page is detected" at the source level — the version comparison flags
what needs refresh.

## 5. The Audit Trail

Provenance plus versioning is the audit trail: for any passage, you can
state which source version produced it, when, and whether it is current.
This is what makes the data trustworthy for citation — a RAG answer citing
a passage can point to the exact source version the passage came from.

## Common Mistakes

- Provenance fields optional (passages that cannot be traced).
- No source versioning (re-ingests un-attributable).
- Tracing that returns a guess instead of failing loudly.
- Ignoring source changes (stale passages served as current).

## Key Takeaways

1. Provenance fields are mandatory, not optional.
2. Source versions make re-ingests attributable.
3. Tracing fails loudly, never guesses.
4. Version comparison detects stale passages.