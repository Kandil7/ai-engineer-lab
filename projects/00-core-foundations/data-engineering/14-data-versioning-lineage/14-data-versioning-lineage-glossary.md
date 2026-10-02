# Data Engineering 14: Data Versioning and Lineage — Glossary

## Quick Reference Table

| Term | Definition | Example |
|------|-----------|---------|
| Data versioning | Make a dataset addressable by content hash | a corpus snapshot |
| DVC | Data versioning on Git: hashes and pointers, bytes in remote | `corpus.dvc` + S3 |
| Content hash | A digest that changes exactly when the data changes | MD5 of a file |
| `.dvc` pointer | A small file recording a data file's path and hash | `md5: 3f9c...` |
| Data catalog | Searchable index of datasets, owners, schema, lineage | Amundsen, DataHub |
| Lineage | Directed graph of "derived from" across data assets | table/column edges |
| Column-level lineage | Lineage at the column grain | `original -> searchable` |
| Impact analysis | Traversal: which downstream nodes a change affects | what breaks on a version bump |
| Audit trail | Immutable, attributable record of changes | actor, timestamp, reason |
| Repro | Re-run only the stages whose inputs changed | `dvc repro` |

---

## Alphabetical Glossary

### Audit trail

**Definition:** The append-only, attributable record of every change — actor, timestamp, and reason —
that makes a data system compliance-ready and every change traceable to a person.

**Example:**
```python
{"actor": "ingest-bot", "ts": "2026-10-02T09:00", "version": "v2", "reason": "typo fix"}
```

**Related concepts:** Lineage, Provenance

---

### Column-level lineage

**Definition:** Lineage tracked at the column grain, recording which input column produced which output
column. More precise than table-level lineage, it scopes impact to what actually changed.

**Example:**
```text
corpus.original -> passage.searchable -> vector_store.embedding
```

**Related concepts:** Lineage, Impact analysis

---

### Content hash

**Definition:** A digest of a file's bytes that changes exactly when the content changes. Two files with
the same hash are the same data; this property is the root of checkable reproducibility.

**Example:**
```python
hashlib.md5(data).hexdigest()
```

**Related concepts:** DVC, Data versioning

---

### Data catalog

**Definition:** A searchable index over data assets — names, owners, schemas, freshness, and lineage —
that makes data discoverable and governable without reading code.

**Example:**
```text
Amundsen (discovery-first), DataHub (metadata graph)
```

**Related concepts:** Lineage, DVC

---

### DVC

**Definition:** Data Version Control, which layers data versioning onto Git by storing hashes and pointer
files in the repo while the data bytes live in remote storage. `dvc repro` re-runs only changed stages.

**Example:**
```yaml
outs:
  - md5: 3f9c2...e1a
    path: passages.parquet
```

**Related concepts:** Content hash, Repro

---

### Impact analysis

**Definition:** The traversal over the lineage graph that answers "which downstream nodes does this
change affect," the reverse of tracing. Scopes a re-ingest to what actually breaks.

**Example:**
```python
affected(nodes, changed="corpus.original")
```

**Related concepts:** Lineage, Column-level lineage

---

### Lineage

**Definition:** The directed graph of "derived from" edges across data assets — tables, columns,
features, models — that makes data flow visible and queryable.

**Example:**
```text
repo files -> chunks -> embeddings -> vector index
```

**Related concepts:** Column-level lineage, Impact analysis

---

## Related Concepts

- **Provenance**: the origin-traceability this lecture mechanizes (topic 06)
- **Deduplication**: the content hash both reuse (topic 05)
- **Lakehouse**: snapshots and time travel at the table level (topic 10)

## Key Takeaways

1. Data needs versioning separate from code.
2. DVC stores hashes and pointers in Git, bytes in remote storage.
3. Amundsen is discovery-first; DataHub is a metadata graph.
4. Column-level lineage scopes impact; table-level over-recomputes.
5. Audit trails complete traceability alongside provenance and hashing.
