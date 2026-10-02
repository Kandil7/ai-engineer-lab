# Data Engineering 14: Data Versioning and Lineage

## Topic Overview

Code is versioned; data is not — that asymmetry is the root of most reproducibility failures. Data
versioning makes a dataset addressable by a content hash, so "which version of the corpus produced this
answer" has a precise, checkable answer. Lineage makes the flow of data visible, from source column to
derived table to feature, so "if this changes, what breaks" is a query rather than a guess. Together
they are the traceability layer that turns a pipeline into an auditable system.

The tools split by concern. DVC versions data files on top of Git, storing content hashes and pointers
while the heavy files live in remote storage. Data catalogs (Amundsen, DataHub) index the metadata and
make datasets discoverable, with lineage graphs. Column-level lineage tracks provenance at the finest
granularity, and impact analysis answers the "what breaks" question. Audit trails make every change
attributable to a person and a time.

This lecture is the natural extension of Data Engineering 06. Provenance said where a passage came
from; this lecture gives provenance the machinery to be checked (a hash), queried (a lineage graph), and
reconstructed (a versioned dataset). For a system that cites its sources, that is the difference between
"we think this is where it came from" and "here is the exact snapshot, verified by hash."

## Learning Objectives

By the end of this lecture, you will be able to:

1. Explain why data must be versioned separately from code.
2. Describe how DVC uses content hashes and pointers over Git.
3. Distinguish Amundsen and DataHub and what a catalog adds.
4. Model table-level and column-level lineage.
5. Run an impact analysis: which downstream artifacts break on an upstream change.
6. Build an audit trail that makes every change attributable.
7. Connect content hashing to the deduplication discipline of earlier lectures.

## Prerequisites

- Data Engineering 06 (provenance) for the traceability this lecture mechanizes.
- Data Engineering 05 (deduplication) for the content hash both reuse.

---

## 1. Why Data Must Be Versioned

### The asymmetry

Git versions code exactly: a commit identifies a tree of files by hash. Data usually lives outside Git —
too large, too mutable — so it is versioned by convention, not by mechanism. "The corpus as of last
month" becomes a folder that may or may not still be what it was.

### The failure it causes

An unreproducible result is a trace that cannot be verified. A cited answer is only as trustworthy as
the corpus snapshot behind it; if that snapshot changed silently, the citation is a claim, not a
verification. This is the same "tracing fails loudly" principle from Data Engineering 06, at the dataset
level.

### What versioning provides

Versioning gives a dataset an immutable, addressable identity: a content hash that changes exactly when
the data changes. Two copies with the same hash are the same data; two with different hashes differ.
That single property makes reproducibility checkable rather than assumed.

## 2. DVC

### The model

DVC (Data Version Control) layers data versioning on top of Git without storing the data in Git. A
`.dvc` file records the data file's path and its MD5 hash; the data itself lives in remote storage (S3,
GCS, a local cache).

```yaml
# corpus.dvc — the pointer; the real bytes live in remote storage
outs:
  - md5: 3f9c2...e1a
    path: passages.parquet
```

### The workflow

`dvc add` hashes the file and writes the pointer; `dvc push` uploads the bytes to the remote; `dvc pull`
retrieves them by hash; `dvc checkout` restores the exact snapshot a pointer describes. The Git commit
records only the pointer, so a data change is a one-line diff that points at a new hash.

### The repro pipeline

DVC also models the pipeline as stages with dependencies and outputs, and `dvc repro` re-runs only the
stages whose inputs changed. That is the re-run safety of Data Engineering 01, generalized: change an
input, and DVC knows exactly which stages must recompute. The hash is the signal, and the dependency
graph is the map.

## 3. Data Catalogs

### What a catalog adds

A catalog is the searchable index over your data assets: what datasets exist, who owns them, their
schema, their lineage, and their freshness. It answers "where do I find the passage count" without
reading code, and "who owns this table" when it breaks.

### Amundsen

Amundsen (Lyft) is discovery-first: search for tables and dashboards by name and metadata, see owners,
descriptions, and popularity, and navigate lineage. It is the answer to "I need data about X — where is
it?"

### DataHub

DataHub (LinkedIn) is a metadata platform built on a streaming metadata graph: metadata changes flow
through Kafka into a graph, and lineage is a first-class, queryable edge type. It spans tables, jobs,
models, and dashboards in one graph, which makes it the stronger choice when lineage and cross-asset
impact matter more than discovery alone.

### A note on the roadmap's "Marimo"

The roadmap lists Amundsen, DataHub, and Marimo together as catalog tools, but that is a miscategorization.
Marimo is a reactive Python notebook (cells re-run on dependency change), not a data catalog. The
correction matters: a notebook is where you compute, a catalog is where you discover and trace. Keep the
two roles separate.

## 4. Column-Level Lineage

### Table-level versus column-level

Table-level lineage says table B derives from table A. Column-level lineage says which columns: B's
`searchable` derives from A's `original` through a normalization transform, while B's `page` passes
through unchanged. The finer grain is what makes impact analysis precise.

### The graph model

Lineage is a directed graph of nodes (columns, tables, features) and edges ("derived from"). It can be
captured by hand (dbt models, which declare `original -> searchable`), inferred by SQL parsing
(SQLGlot, OpenLineage), or recorded by the pipeline as it runs.

```text
corpus.original ──normalize──> passage.searchable ──embed──> vector_store.embedding
corpus.page ───────────────────> passage.page
```

### Why the finer grain matters

If `original` changes, only `searchable`, its embedding, and the vector index are affected; `page` is
not. Table-level lineage would flag the whole passage table and force a full recompute. Column-level
lineage scopes the blast radius to what actually depends on the changed column.

## 5. Impact Analysis

### The question

Impact analysis is the query against the lineage graph: given a change at this node, which downstream
nodes are affected, transitively? It is the reverse of tracing — instead of "where did this come from",
"what does this change break."

### The traversal

A breadth-first walk from the changed node along "derived from" edges yields the affected set. A source
version bump on `book_id=b1` affects that book's passages, their embeddings, and the vector index rows
that carry them — and nothing else.

```python
def affected(nodes: dict[str, list[str]], changed: str) -> set[str]:
    seen, frontier = set(), {changed}
    while frontier:
        n = frontier.pop()
        if n in seen:
            continue
        seen.add(n)
        frontier.update(nodes.get(n, []))
    return seen
```

### Why it matters for operations

A precise impact set turns "we must re-ingest everything" into "we re-ingest this one book and
recompute its embeddings." For a corpus that changes rarely but is large, that is the difference between
minutes and days of work. The lineage graph is what makes the precise answer possible.

## 6. Audit Trails

### What an audit trail is

An audit trail is the immutable, attributable record of changes: who changed what, when, and why. For
data, it means every re-ingest, schema change, and version bump is logged with an actor, a timestamp,
and a reason, and the log is append-only.

### Why compliance needs it

Compliance frameworks (GDPR, SOC2) require the ability to say, for any record, what happened to it and
who did it. A citation system's trust rests on the same property: a passage must be traceable not only
to its source but to the process that changed it. The append-only log of Data Engineering 08 is the
mechanism; the audit trail is the policy on top.

### The link to provenance

Provenance (Data Engineering 06), content hashing (this lecture), and the audit trail are three views of
one property: traceability. Provenance names the origin, the hash makes it checkable, and the audit
trail makes every change attributable. Together they satisfy the roadmap's "every passage traceable"
bar, and go beyond it to "and every change auditable."

## 7. Building It for Our Systems

### The Athar corpus manifest

A DVC-style manifest for the Athar corpus is a pointer file per source version: a hash of the raw book
files, a hash of the normalized passages, and a hash of the embedding snapshot. Each stage's output hash
is the input hash of the next, so the whole chain is content-addressed and verifiable.

### The DevMate lineage graph

DevMate's lineage is short but real: repo files derive into chunks, chunks derive into embeddings,
embeddings derive into the vector index. A file change triggers chunk re-derivation for that file only,
then its embeddings, then its index rows — the column-level precision that avoids a full re-ingest.

### The exit-test connection

The roadmap's data-engineering bar is reproducibility and traceability. Versioning gives the verifiable
snapshot, lineage gives the precise impact, and the audit trail gives the attributable history. A cited
answer can be checked against the exact corpus snapshot by hash, which is the strongest form of the
"traceable to origin" requirement.

## Real-World Application

- Adding a `.dvc` pointer per Athar source version so the exact corpus snapshot behind any answer is
  retrievable by hash.
- Querying a DataHub lineage graph to answer "which vectors does a corrected book invalidate."
- Scoping a re-ingest to one book's passages and embeddings via column-level lineage, instead of a full
  recompute.
- Logging every re-ingest as an audit record — actor, timestamp, version, reason — for compliance.

## Common Mistakes

1. **Data outside version control.** A corpus that changes silently, unverifiable citations.
2. **Storing data in Git.** The repo balloons; versioning data and code are different jobs.
3. **Table-level lineage only.** A full recompute where a column-level change would suffice.
4. **A catalog that is never maintained.** Stale metadata is worse than none.
5. **No audit log.** Changes are unattributable, and compliance cannot be satisfied.
6. **Hashing without retaining the source snapshot.** The hash is checkable but the data is gone.

## Key Takeaways

1. Data needs its own versioning; content hashes make reproducibility checkable.
2. DVC stores hashes and pointers in Git, bytes in remote storage, and re-runs only changed stages.
3. Amundsen is discovery-first; DataHub is a metadata graph; Marimo is a notebook, not a catalog.
4. Column-level lineage scopes impact precisely; table-level forces over-recompute.
5. Audit trails make every change attributable; with provenance and hashing, they complete traceability.

## Self-Check Questions

1. Why does Git not version data, and what does DVC do about it?
2. What single property does content hashing give reproducibility?
3. Why is column-level lineage more useful than table-level for impact analysis?
4. What does an impact traversal answer, and how is it the reverse of tracing?
5. How do provenance, hashing, and audit trails compose into traceability?

## Further Reading / Connections

- Data Engineering 06 (provenance) — the traceability this lecture mechanizes.
- Data Engineering 05 (deduplication) — the content hash both reuse.
- Data Engineering 10 (lakehouse) — snapshots and time travel at the table level.
- Data Engineering 08 (batch vs streaming) — the append-only log the audit trail uses.
- `projects/04-ai-engineering/devmate/src/devmate/ingest/` — where the manifest and lineage would live.
