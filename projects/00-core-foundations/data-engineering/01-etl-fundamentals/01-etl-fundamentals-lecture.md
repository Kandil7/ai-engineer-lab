# Data Engineering 01: ETL Fundamentals

## Topic Overview

Every data pipeline is ETL: extract, transform, load. The names are old, but the discipline is
what makes a pipeline trustworthy rather than merely functional. Extract reads the source; transform
turns raw material into structured data; load writes it to a destination. For Athar, this is raw
book pages becoming structured passages with provenance.

This lecture covers the three stages, the batch-versus-stream decision, and the two correctness
properties that separate a production pipeline from a script: determinism (same input, same output)
and idempotency (running twice leaves the same state). Together they make re-runs safe, which is
what a pipeline needs, because pipelines fail and get re-run.

The through-line is that a pipeline is a function, not a process with side effects. When it behaves
like a function, a re-run is harmless and a failure is recoverable; when it does not, every re-run
risks duplicating or corrupting the data.

## Learning Objectives

By the end of this lecture, you will be able to:

1. Decompose a data job into extract, transform, and load stages.
2. Choose batch versus streaming from the source and the consumer's latency need.
3. Make each stage deterministic and idempotent.
4. Log per-stage counts so failures are attributable.
5. Build the raw-book-to-passages pipeline as a clean ETL.
6. Explain why re-runs must be safe.

## Prerequisites

- Basic file handling and JSON in Python.
- A grasp of the Athar passage contracts (book_id, page, original, searchable).

---

## 1. The Three Stages

### Extract

Extract reads from a source: files, a database, an API, a crawl. It must be read-only and
resumable, never destructive:

```python
def extract(pages_dir: Path) -> list[tuple[int, str]]:
    """Read-only extract: page number + raw text, sorted by page."""
    ...
```

A destructive extract (deleting the source after reading) makes a failed run unrecoverable. Extract
never mutates its input.

### Transform

Transform applies the business logic: cleaning, normalization, chunking, enrichment. It should be
pure where possible, meaning the same input always yields the same output. Purity is what makes the
stage testable and the pipeline deterministic.

### Load

Load writes to the destination: a database, a vector store, a file. It must be idempotent, so a
re-run never duplicates. The load stage is where most idempotency bugs live (Data Engineering 03).

### The contracts

Each stage is a function with a clear contract: `extract(source) -> raw`, `transform(raw) ->
rows`, `load(rows, sink) -> count`. The count is the observability hook.

## 2. Batch Versus Stream

### Batch

Batch processes bounded chunks on a schedule: nightly, hourly, on demand. It is simple, cheap, and
easy to reason about.

### Streaming

Streaming processes events as they arrive. It gives freshness but adds latency, ordering, and
exactly-once complexity.

### Deciding

The decision follows from the source and the consumer. Is the source a finite corpus or a live
feed? How fresh must the data be? Athar's corpus is batch: books are finite, and a new book can
trigger a batch job. Streaming would add complexity without benefit for a corpus that changes
rarely.

### The default

Start with batch. Move to streaming only when a real freshness requirement demands it, because
streaming's complexity is paid continuously while its benefit applies only when freshness matters.

## 3. Determinism

### The property

A deterministic pipeline produces identical output for identical input. No timestamps in the output,
no unseeded randomness, no dependence on iteration order:

```python
assert first == second, "deterministic + idempotent: identical output"
```

### Why it matters

Determinism is what makes the re-run comparison meaningful (Data Engineering 03). If the output
changes between runs, a re-run cannot be compared to the first, and a real difference is hidden
among the noise of nondeterminism.

### The usual culprits

Timestamps written into records, iteration over an unordered set, dictionary ordering assumptions,
and unseeded random sampling. Each is a one-line fix and a large reliability gain.

## 4. Idempotency

### The property

An idempotent load can run twice and leave the same state as running once:

```python
def load(rows, out_path) -> int:
    """Idempotent load: deterministic JSONL output."""
    ...
```

### Why pipelines need it

Pipelines fail and get re-run: a network drop, a crash, a bad page. Without idempotency, every
re-run risks duplicates or corruption. With it, a re-run is safe, which is what lets a pipeline
recover.

### The combination

Determinism plus idempotency equals safe re-runs. Together they make the pipeline behave like a
function of its input, and that is the property the roadmap's exit test checks: running twice does
not duplicate data.

## 5. Observability

### Per-stage counts

Every stage logs rows in, rows out, duration, and any rows skipped or failed. A pipeline without
per-stage counts is a black box: when a passage goes missing, no one can say which stage lost it.

### Why the counts are first

The stage counts are the first thing an incident review asks for. They localize the failure to a
stage in seconds, which turns a mystery into a fix. Instrument the stages before the incident, not
after.

### The link to the log

The per-stage counts are part of the pipeline's log (RAG System 07), so the trend is visible over
time and a regression is attributable.

## 6. The Athar Pipeline

### The shape

```text
extract:   read book pages (UTF-8, page numbers from filenames)
transform: clean, normalize (two-text discipline), chunk into passages
load:      write passages with book_id/page/source_version
```

### Each stage a function

The athar-lab scaffold implements exactly this shape. The lecture is the theory behind the scaffold:
a read-only extract, a pure transform that applies the two-text discipline (Arabic NLP 01), and an
idempotent load that carries provenance.

### The exit test

Running the pipeline twice produces identical output and no duplicates. That is the property that
makes the rest of the pipeline (checkpointing, dedup, versioning) possible.

## Real-World Application

- Ingesting an Athar book: extract pages, transform to normalized passages, load with provenance.
- Choosing batch for the corpus so the scheduling is simple and the re-runs are safe.
- Writing per-stage counts so a missing passage is traced to the stage that lost it.
- Making the load idempotent so an interrupted ingest resumes without duplicating passages.

## Common Mistakes

1. **Destructive extract.** The source is gone if the run fails.
2. **Nondeterministic output.** Timestamps or unseeded randomness break re-run comparison.
3. **Non-idempotent load.** Re-runs duplicate.
4. **No per-stage counts.** Failures are unlocatable.
5. **Streaming when batch suffices.** Complexity paid for no benefit.
6. **Impure transform.** The stage is untestable and the pipeline nondeterministic.

## Key Takeaways

1. Extract read-only, transform pure, load idempotent.
2. Batch for finite corpora; stream only when freshness demands the complexity.
3. Determinism plus idempotency equals safe re-runs.
4. Per-stage counts make failures attributable in seconds.
5. The Athar pipeline is these three stages applied to book pages.

## Self-Check Questions

1. Why must extract be read-only, and what goes wrong if it deletes the source?
2. When is batch preferred over streaming, and why?
3. Give three common sources of nondeterminism in a pipeline.
4. Why must the load stage be idempotent, and how is that tested?
5. What does each per-stage count let you diagnose?

## Further Reading / Connections

- Data Engineering 02 (schemas and contracts) and 03 (idempotency) — the properties this stage needs.
- Arabic NLP 01 (Arabic text fundamentals) — the two-text discipline the transform applies.
- `projects/04-ai-engineering/athar-lab/` — the working ETL scaffold.
- RAG System 07 (context failure modes) — where pipeline failures surface.
