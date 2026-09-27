# AI Evaluation 01: Gold Datasets and Annotation — Glossary

## Quick Reference Table

| Term | Definition | Example |
|------|-----------|---------|
| Gold dataset | Fixed, curated query set with verified answers | 50 queries |
| Golden query | One query + relevant passages + answer | b3:p12:0 |
| Annotation guidelines | Rules that make labels reproducible | relevance definition |
| Inter-annotator agreement | Measured consistency between annotators | Cohen's kappa |
| Cohen's kappa | Agreement corrected for chance | 0.7 = trustworthy |
| Coverage | The query space the golden set spans | verse, hadith, fiqh |
| Regression gate | Golden set runs in CI on every change | recall@5 drop caught |

---

## Alphabetical Glossary

### Annotation guidelines

**Definition:** The written rules that make labels reproducible: what counts
as relevant, how to pick the answer, how to mark unanswerable queries.
Without them the golden set measures the annotators, not the system.

**Example:**
```python
# "a passage is relevant if it answers the query's core question"
```

**Related concepts:** Inter-annotator agreement, Gold dataset

---

### Cohen's kappa

**Definition:** Inter-annotator agreement corrected for chance. Two
annotators agreeing 80% on a 90%-majority label is far less than 80% real
agreement. Kappa below 0.7 means the guidelines are ambiguous.

**Example:**
```python
# kappa = (observed - chance) / (1 - chance)
```

**Related concepts:** Inter-annotator agreement, Annotation guidelines

---

### Coverage

**Definition:** The query space the golden set spans. Fifty well-chosen
queries beat five hundred random ones. Coverage includes the hard cases and
the abstention cases.

**Example:**
```python
# verse questions, hadith questions, fiqh questions, unanswerable queries
```

**Related concepts:** Gold dataset

---

### Gold dataset

**Definition:** A small, fixed, curated set of queries with verified answers
and relevant passages. Not training data, not a traffic sample — a yardstick
that runs against every change.

**Example:**
```python
# 50 queries, each with relevant passages and a verified answer
```

**Related concepts:** Golden query, Regression gate

---

### Golden query

**Definition:** One entry in the golden set: the query, the relevant passage
ids, the verified answer, and notes on why.

**Example:**
```python
{"query": "ما حكم الصلاة في السفر؟", "relevant": ["b3:p12:0"], "answer": "القصر جائز"}
```

**Related concepts:** Gold dataset

---

### Inter-annotator agreement

**Definition:** The measured consistency between annotators labeling the
same queries. Measured, never assumed.

**Example:**
```python
# two annotators label the same 50 queries; agreement is computed
```

**Related concepts:** Cohen's kappa, Annotation guidelines

---

### Regression gate

**Definition:** The golden set running in CI on every change. A retrieval
change that drops recall@5 on the golden set is caught before it ships.

**Example:**
```python
# CI fails when golden-set recall@5 falls below the threshold
```

**Related concepts:** Gold dataset

---

## Related Concepts

- **Faithfulness**: the golden set anchors the faithfulness metric (topic 02)
- **Retrieval evaluation**: recall@5 measured against the golden set (topic 03)
- **Eval in CI**: the golden set as the regression gate (topic 06)

## Key Takeaways

1. The golden set is a fixed, curated yardstick.
2. Coverage beats size.
3. Guidelines make labels reproducible.
4. Measure agreement; kappa below 0.7 is a warning.
5. The golden set gates every change in CI.