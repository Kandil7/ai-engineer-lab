# Data Engineering 11: Data Quality Frameworks — Glossary

## Quick Reference Table

| Term | Definition | Example |
|------|-----------|---------|
| Data quality | Whether data is fit for use | no null passage ids |
| Expectation | A declarative assertion about a column or table | `expect_column_values_to_not_be_null` |
| Pydantic | Record-boundary validation with typed constraints | `page: int = Field(ge=1)` |
| Great Expectations | Dataset-level expectations, checkpoints, data docs | batch validation suite |
| Checkpoint | A run of a suite against a batch, producing a result | pass/fail per expectation |
| Data docs | Human-readable rendering of validation results | HTML of failed rows |
| Databand | Pipeline-level observability and anomaly detection | duration and volume baselines |
| Anomaly detection | Comparing a run to history to flag drift | z-score on row count |
| Six dimensions | Completeness, validity, uniqueness, consistency, timeliness, accuracy | a shared vocabulary |
| Quality gate | The pre-load checkpoint that fails loudly | block bad rows from loading |

---

## Alphabetical Glossary

### Anomaly detection

**Definition:** The temporal quality layer that compares this run to the history of runs, flagging
volume drops, null-rate drift, and distribution change. Needs a retained baseline to be meaningful.

**Example:**
```python
is_anomalous(count, history)  # abs(count - mean) > 3 * sd
```

**Related concepts:** Databand, Timeliness

---

### Checkpoint

**Definition:** In Great Expectations, the execution of an expectation suite against a batch, producing
a validation result that lists which expectations passed and failed, with samples.

**Example:**
```python
context.run_checkpoint(checkpoint_name="passage_check")
```

**Related concepts:** Expectation, Data docs

---

### Data docs

**Definition:** The human-readable rendering of Great Expectations validation results, showing what
failed and which values were unexpected. The bridge from "pipeline failed" to "this row is wrong".

**Example:**
```html
<!-- rendered HTML: expect_column_values_to_be_between, 3 unexpected values -->
```

**Related concepts:** Checkpoint, Great Expectations

---

### Expectation

**Definition:** A declarative assertion about a column or table, expressed as a named check. The unit of
Great Expectations validation.

**Example:**
```python
suite.add_expectation("expect_column_values_to_be_unique", column="passage_id")
```

**Related concepts:** Great Expectations, Checkpoint

---

### Great Expectations

**Definition:** The open-source data-quality framework for dataset-level validation. Expectation suites,
checkpoints, and data docs validate whole batches, catching uniqueness and distribution failures that
record-level checks cannot.

**Example:**
```python
# a suite over the passage batch: non-null, unique, page >= 1
```

**Related concepts:** Expectation, Pydantic

---

### Pydantic

**Definition:** A Python validation library that checks a single record at the boundary, using typed
fields and constraints, refusing to construct an invalid record.

**Example:**
```python
class Passage(BaseModel):
    page: int = Field(ge=1)
```

**Related concepts:** Validity, Quality gate

---

### Quality gate

**Definition:** The pre-load checkpoint where validated data is allowed through and failures stop the
pipeline. Sits between transform and load, so bad data never reaches the destination.

**Example:**
```python
# transform -> validate -> load (only rows that passed)
```

**Related concepts:** Great Expectations, Validity

---

### Six dimensions

**Definition:** Completeness, validity, uniqueness, consistency, timeliness, and accuracy — the shared
vocabulary for naming what went wrong, which points at which system to fix.

**Example:**
```python
# "page is null" = completeness + validity; "row count halved" = timeliness
```

**Related concepts:** Data quality, Anomaly detection

---

## Related Concepts

- **Schemas**: the shape the checks enforce (topic 02)
- **Deduplication**: the uniqueness dimension at scale (topic 05)
- **Provenance**: the audit trail holding the baseline history (topic 06)

## Key Takeaways

1. Six dimensions name the failure before the fix.
2. Pydantic validates records; Great Expectations validates batches.
3. Checkpoints run suites; data docs render failures readably.
4. Databand and anomaly detection watch the pipeline over time.
5. The gate fails loudly between transform and load.
