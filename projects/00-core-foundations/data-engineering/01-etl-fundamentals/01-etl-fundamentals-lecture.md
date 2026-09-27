# Data Engineering 01: ETL Fundamentals

## 🎯 Topic Overview

ETL — extract, transform, load — is the pipeline that turns raw source
material into queryable data. For Athar, that means raw book pages becoming
structured passages with provenance. This lecture covers the three stages,
the batch-versus-stream decision, and the correctness discipline that makes
a pipeline trustworthy: every stage is deterministic, observable, and
re-runnable.

## 📚 Learning Objectives

By the end of this lecture, you will be able to:

1. Decompose any data job into extract, transform, and load stages
2. Choose batch vs streaming from the source's nature and the consumer's latency need
3. Make each stage deterministic and idempotent
4. Log and observe every stage so failures are attributable
5. Build the Athar raw-book-to-passages pipeline as a clean ETL

---

## 1. The Three Stages

**Extract** reads from a source: files, a database, an API, a crawl. It
should be read-only and resumable — never destructive. **Transform** applies
the business logic: cleaning, normalization, chunking, enrichment. It should
be pure where possible: same input, same output. **Load** writes to the
destination: a database, a vector store, Parquet files. It must be
idempotent so re-running never duplicates.

```python
# The shape every pipeline stage follows
def extract(source) -> list[RawPage]: ...
def transform(pages) -> list[Passage]: ...
def load(passages, sink) -> int: ...  # returns rows written
```

## 2. Batch vs Stream

Batch processes bounded chunks on a schedule — nightly, hourly, on-demand.
Stream processes events as they arrive. The decision is driven by the
source (is it a finite corpus or a live feed?) and the consumer (how fresh
must the data be?). Athar's corpus is batch: books are finite, and a new
book can trigger a batch job. Streaming adds latency complexity without
benefit for a corpus that changes rarely.

## 3. Determinism and Idempotency

A deterministic pipeline produces identical output for identical input —
no timestamps in output, no unseeded randomness, no dependence on
iteration order. An idempotent load can run twice and leave the same
state. Together they make re-runs safe: the pipeline is a function, not a
process with side effects. This is the property the roadmap's exit test
checks ("running twice does not duplicate data").

## 4. Observability

Every stage logs: rows in, rows out, duration, and any rows skipped or
failed. A pipeline without per-stage counts is a black box — when a passage
goes missing, you cannot tell which stage lost it. The stage counts are the
first thing an incident review asks for.

## 5. The Athar Pipeline

```text
extract:  read book pages (UTF-8, page numbers from filenames)
transform: clean, normalize (two-text discipline), chunk into passages
load:     write passages with book_id/page/source_version to JSONL or DB
```

Each stage is a function with a clear contract. The athar-lab scaffold
already implements this shape; this lecture is the theory behind it.

## Common Mistakes

- Destructive extract (deleting source after reading).
- Non-deterministic output (timestamps, unseeded randomness) breaking re-runs.
- No per-stage counts, so failures are unlocatable.
- Choosing stream when batch suffices (complexity without benefit).

## Key Takeaways

1. Extract read-only, transform pure, load idempotent.
2. Batch for finite corpora; stream only when freshness demands it.
3. Determinism + idempotency = safe re-runs.
4. Per-stage counts make failures attributable.