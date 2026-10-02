# Data Engineering 11: Data Quality Frameworks

## Topic Overview

A schema (Data Engineering 02) says what shape the data must have; data quality says whether the data
actually satisfies that shape, and whether it is fit for use. Quality is checked with expectations — 
declarative assertions like "this column is never null" or "this value is always positive" — and it is
enforced by frameworks that run those expectations on every batch and fail loudly when one is violated.
Pydantic validates at the record boundary; Great Expectations validates whole datasets with profiling
and human-readable docs; Databand watches the pipeline itself for anomalies.

The six dimensions — completeness, validity, uniqueness, consistency, timeliness, and accuracy — are the
shared vocabulary. A pipeline that never checks them is one where a null passage id or a mistranscribed
Arabic string propagates silently into the vector index and then into a cited answer. For a system that
cites its sources, that is a correctness bug, not a cosmetic one.

Anomaly detection is the temporal layer: the same check run yesterday and today, compared. A row count
that halves overnight, a column that suddenly has nulls, a distribution that drifts — these are the
signals that a pipeline broke, and they are caught not by re-stating the rule but by watching the trend.

## Learning Objectives

By the end of this lecture, you will be able to:

1. Name the six dimensions of data quality and map each to a check.
2. Write record-level validation with Pydantic and dataset-level expectations with Great Expectations.
3. Explain what a Great Expectations checkpoint runs and why the docs matter.
4. Place Databand as pipeline-level anomaly detection.
5. Build a statistical anomaly detector for volume and freshness.
6. Enforce the Athar passage contract as a quality gate that fails loudly.
7. Explain why quality is checked at the boundary, not after the fact.

## Prerequisites

- Data Engineering 02 (schemas) for the shape the checks enforce.
- Data Engineering 01 (ETL) for the per-stage counts these checks extend.

---

## 1. The Six Dimensions

### The vocabulary

- **Completeness** — no missing values where a value is required.
- **Validity** — values conform to their type and domain.
- **Uniqueness** — no duplicate keys or rows.
- **Consistency** — the same fact is the same everywhere.
- **Timeliness** — data is fresh enough for its consumer.
- **Accuracy** — values match reality (the hardest to check automatically).

### Why dimensions first

A check without a dimension is a fix without a diagnosis. Saying "the row count dropped" is completeness
and timeliness; saying "the title column is null" is completeness and validity. Naming the dimension
tells you which system to fix: a schema change, a broken extract, a stale source.

### The Athar mapping

Every Athar passage is a candidate for all six: `book_id` and `page` non-null (completeness), `page >= 1`
and `source_version` well-formed (validity), `passage_id` unique (uniqueness), `original` and
`searchable` agreeing under the normalization (consistency), the corpus current to the latest source
(timeliness), and the text faithful to the book (accuracy, verified by spot check).

## 2. Record-Level Validation: Pydantic

### The boundary check

Pydantic validates one record at the moment it enters the system. A model with typed fields and
constraints refuses to construct an invalid record:

```python
from pydantic import BaseModel, Field


class Passage(BaseModel):
    book_id: str
    page: int = Field(ge=1)
    source_version: str
    original: str = Field(min_length=1)
    searchable: str = Field(min_length=1)
```

`Passage(book_id="", page=0, ...)` raises, so an invalid passage cannot exist downstream. This is the
structural-invariant idea of Data Engineering 02, enforced by a library instead of by hand.

### Where it lives

Pydantic lives at the ingest boundary — the transform's output, the API's request body, the message the
pipeline reads. It is cheap, synchronous, and precise, but it sees one record at a time, so it cannot
say whether the whole dataset is unique or fresh.

## 3. Dataset-Level Validation: Great Expectations

### Expectations, not models

Great Expectations (GX) works on batches, not records. An expectation is a declarative assertion about a
column or a table:

```python
import great_expectations as gx

context = gx.get_context()
suite = context.add_expectation_suite("passage_suite")
suite.add_expectation("expect_column_to_exist", column="book_id")
suite.add_expectation("expect_column_values_to_not_be_null", column="book_id")
suite.add_expectation("expect_column_values_to_be_unique", column="passage_id")
suite.add_expectation("expect_column_values_to_be_between", column="page", min_value=1)
```

### The checkpoint and the docs

A **checkpoint** runs a suite against a batch and produces a validation result: a list of which
expectations passed and failed, with unexpected-value samples. The **data docs** render those results as
human-readable HTML, so a non-engineer can see what broke. The docs are the bridge from "the pipeline
failed" to "this specific page number is zero on these rows."

### Why it complements Pydantic

Pydantic checks a record; GX checks a column across the whole batch. Uniqueness, null rate, and value
distributions are dataset properties, invisible to a record-level validator. Production systems use
both: Pydantic at the boundary, GX as the batch gate.

## 4. Pipeline Observability: Databand

### A different layer

Databand (IBM) watches the pipeline rather than the data: run durations, task status, data volumes,
dependency health. Where GX asks "is the data right?", Databand asks "did the pipeline behave as it
should?" and "is this run's volume a normal variation?"

### The value

A pipeline that silently produces half the usual rows may pass every static expectation — the rows it
did produce are valid — yet be broken at the source. Databand's volume and duration tracking catches
that temporal failure, which is the same per-stage-count discipline of Data Engineering 01 turned into
a first-class monitoring surface with baselines and alerts.

## 5. Anomaly Detection in Pipelines

### The temporal layer

Anomaly detection compares this run to the history of runs. The simplest robust detectors:

- **Z-score** on row count — flag a run whose volume is more than a few standard deviations from the
  mean.
- **IQR** (interquartile range) — flag values outside `[Q1 - 1.5*IQR, Q3 + 1.5*IQR]`, robust to outliers.
- **Null-rate drift** — flag a column whose null fraction jumped.

### The code

```python
def is_anomalous(count: int, history: list[int]) -> bool:
    mean = sum(history) / len(history)
    sd = (sum((x - mean) ** 2 for x in history) / len(history)) ** 0.5
    return sd > 0 and abs(count - mean) > 3 * sd
```

### Why baselines matter

An anomaly detector without a baseline is guessing. The history of runs is the baseline, and it must be
retained (Data Engineering 06's audit trail gives it a home). A sudden drop in Athar passages after a
re-ingest is the signal that an extract stage silently lost pages, and the detector is what turns the
silence into an alert.

## 6. The Quality Gate

### Fail loudly at the boundary

The rule that binds these together is from the tracing discipline of Data Engineering 06: quality
failures fail loudly, at the boundary, not quietly downstream. A passage that fails a GX expectation
never reaches the vector index; a run that is anomalous stops and pages a human.

### The gate's position

The gate sits between transform and load — the same position the per-stage counts occupy. Transform
produces rows; the gate validates them; load writes only what passed. A row that cannot pass is not
loaded, and the failure is attributed to a stage, which is exactly the observability contract of Data
Engineering 01.

### The exit-test connection

The roadmap's bar is that bad data cannot silently propagate. Pydantic blocks invalid records, GX blocks
invalid batches, and anomaly detection blocks abnormal runs. Together they make "the data is wrong" a
loud event rather than a silent citation error.

## 7. Choosing the Tool

### The selection rule

- **Pydantic** for the record boundary — API bodies, message schemas, per-record constraints.
- **Great Expectations** for the dataset gate — column properties, uniqueness, distributions, and
  human-readable validation docs.
- **Databand** (or an equivalent) for pipeline health — durations, volumes, and anomalies over time.

### They are layers, not rivals

The three live at different layers and compose: Pydantic inside the transform, GX as the pre-load gate,
and Databand watching the whole pipeline. Choosing one is the wrong question; the right question is
which layer of the stack is unchecked.

### The pragmatic floor

If you adopt nothing else, adopt the smallest set that makes failures loud: a record-level schema
(Pydantic), one dataset expectation on the key column (uniqueness), and one volume anomaly check. That
floor catches the majority of real failures at trivial cost.

## Real-World Application

- Validating every Athar passage with Pydantic so an empty `book_id` cannot enter the corpus.
- Running a GX suite on the re-ingest batch, failing the gate if any `passage_id` duplicates or any
  `page` is less than one.
- Alerting on a z-score volume anomaly after a Shamela sync, catching a silently truncated extract.
- Rendering GX data docs so a non-engineer can see exactly which rows failed and why.

## Common Mistakes

1. **No checks at all.** Bad data propagates to the index and into cited answers.
2. **Validating after load.** The bad rows are already in the destination when the failure surfaces.
3. **Record-only or batch-only checks.** Uniqueness needs the batch; validity needs the record; use both.
4. **Static rules with no temporal baseline.** A valid-but-halved run passes every static check.
5. **Silent failures.** A failing check that does not stop the pipeline or page a human is noise.
6. **No validation docs.** The team cannot see what broke or why.

## Key Takeaways

1. Six dimensions — completeness, validity, uniqueness, consistency, timeliness, accuracy — name the
   failure.
2. Pydantic validates the record boundary; Great Expectations validates the whole batch.
3. A GX checkpoint runs a suite and the data docs render the failures readably.
4. Databand and anomaly detection watch the pipeline and its trends, not just the data.
5. The quality gate sits between transform and load and fails loudly, not downstream.

## Self-Check Questions

1. Why are the six dimensions useful before writing a single check?
2. What can a batch-level expectation catch that a record-level validator cannot?
3. Why is a volume anomaly detector needed even when static checks pass?
4. Where in the pipeline should the quality gate sit, and why?
5. What is the smallest useful quality floor, and why does it cover most failures?

## Further Reading / Connections

- Data Engineering 02 (schemas) — the shape these checks enforce.
- Data Engineering 01 (ETL) — the per-stage counts the anomaly layer extends.
- Data Engineering 06 (provenance) — the audit trail that holds the baseline history.
- Data Engineering 05 (deduplication) — the uniqueness dimension at scale.
- `projects/04-ai-engineering/devmate/src/devmate/ingest/` — where the gate would run.
