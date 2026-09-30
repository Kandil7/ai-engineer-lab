# Prompt Engineering 04: Prompt Evaluation — Glossary

## Quick Reference Table

| Term | Definition | Example |
|------|-----------|---------|
| Test cases | Real inputs with expected behavior | student questions |
| Metrics | The output scores | accuracy, relevance |
| Variation | A prompt alternative | v1 vs v2 |
| Comparison | Variations on the same cases | evidence-based |
| Selection | The best-scoring prompt wins | not the best-reading |
| Production monitoring | The feedback loop | re-evaluate on drift |
| Rubric | The scoring criteria | per metric |

---

## Alphabetical Glossary

### Comparison

**Definition:** Running variations on the same test cases and scoring the
output. The evidence for the choice.

**Example:**
```python
# same input, prompt v1 vs v2, scored output
```

**Related concepts:** Variation, Selection

---

### Metrics

**Definition:** The output scores: accuracy, relevance, helpfulness,
clarity. Each has a target.

**Example:**
```python
# accuracy > 95%, relevance > 90%
```

**Related concepts:** Rubric

---

### Production monitoring

**Definition:** The feedback loop on the selected prompt. A prompt that
degrades in production is re-evaluated.

**Example:**
```python
# track output quality; re-evaluate on drift
```

**Related concepts:** Selection

---

### Rubric

**Definition:** The scoring criteria per metric. Without it, scoring is a
guess.

**Example:**
```python
# accuracy: 1.0 correct, 0.5 partial, 0.0 wrong
```

**Related concepts:** Metrics

---

### Selection

**Definition:** The best-scoring prompt wins, not the best-reading one.
Evidence-based.

**Example:**
```python
# v2 scores 0.92, v1 scores 0.85 -> v2
```

**Related concepts:** Comparison

---

### Test cases

**Definition:** Real inputs with expected behavior. Fixed, so variations
are compared on the same inputs.

**Example:**
```python
{"input": "Explain ice.", "expected": "density + hydrogen bonding"}
```

**Related concepts:** Comparison

---

### Variation

**Definition:** A prompt alternative being compared. Variations differ in
structure, examples, or wording.

**Example:**
```python
# v1: no examples; v2: two few-shot examples
```

**Related concepts:** Comparison

---

## Related Concepts

- **Prompt structure**: the structure is what varies (topic 01)
- **Few-shot**: examples are a variation axis (topic 02)
- **Chain-of-thought**: CoT is a variation axis (topic 03)

## Key Takeaways

1. Test cases come from real inputs.
2. Output is scored against the metrics.
3. Variations compare on the same cases.
4. The best prompt is the best-scoring one.
5. Production is monitored with feedback.