# Data Engineering 06: Provenance and Versioning — Glossary

## Quick Reference Table

| Term | Definition | Example |
|------|-----------|---------|
| Provenance | Where data came from | book_id, page, version |
| Source version | Snapshot identity of the source | v1, v2 |
| Trace | Passage → origin lookup | one query |
| Audit trail | Full history of a passage's origin | version + hash |
| Stale passage | Source changed, passage not refreshed | version mismatch |
| Re-ingest | Re-processing a source under a new version | attributable |
| Integrity failure | A passage that cannot be traced | loud error |

---

## Alphabetical Glossary

### Audit trail

**Definition:** The provenance plus versioning record: for any passage, which
source version produced it, when, and whether it is current. Makes data
trustworthy for citation.

**Example:**
```python
# passage -> source_version v2 -> content hash -> current?
```

**Related concepts:** Provenance, Source version

---

### Integrity failure

**Definition:** A passage that cannot be traced to its origin. A data
integrity failure, not a minor gap — it must fail loudly.

**Example:**
```python
# missing book_id or source_version: trace raises
```

**Related concepts:** Trace, Provenance

---

### Provenance

**Definition:** The recorded origin of data: book_id, page, source_version,
path. Mandatory on every passage, never optional.

**Example:**
```python
{"book_id": "b1", "page": 7, "source_version": "v1"}
```

**Related concepts:** Source version, Trace

---

### Re-ingest

**Definition:** Re-processing a source under a new version. Versioning makes
the re-ingest attributable — the new passages carry the new version.

**Example:**
```python
# book re-ingested -> passages now carry source_version v2
```

**Related concepts:** Source version, Stale passage

---

### Source version

**Definition:** The identity of a specific source snapshot. Changes when the
source changes; links passages to the source's history.

**Example:**
```python
# v1 = original scan, v2 = corrected scan
```

**Related concepts:** Provenance, Re-ingest

---

### Stale passage

**Definition:** A passage whose source changed but which was not refreshed.
Detected by version comparison or content-hash mismatch.

**Example:**
```python
# passage says v1, source is now v2 -> stale, re-ingest
```

**Related concepts:** Source version, Re-ingest

---

### Trace

**Definition:** The lookup from passage to origin: book_id/page/source_version
→ source snapshot → original text. Fails loudly, never guesses.

**Example:**
```python
trace(passage, sources)  # raises if any link is missing
```

**Related concepts:** Provenance, Integrity failure

---

## Related Concepts

- **Deduplication**: dedup must keep the right source version (topic 05)
- **Schemas**: provenance fields are part of the contract (topic 02)
- **Citations**: RAG answers cite the exact source version (topic 09)

## Key Takeaways

1. Provenance is mandatory, not optional.
2. Versions make re-ingests attributable.
3. Tracing fails loudly.
4. Version comparison detects staleness.