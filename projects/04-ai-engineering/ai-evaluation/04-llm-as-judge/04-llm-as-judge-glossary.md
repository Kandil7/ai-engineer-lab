# AI Evaluation 04: LLM-as-Judge — Glossary

## Quick Reference Table

| Term | Definition | Example |
|------|-----------|---------|
| Judge | A model that grades output against a rubric | faithfulness 0-1 |
| Rubric | The criteria and scale the judge applies | faithfulness, helpfulness |
| Position bias | The judge prefers the first answer | randomize order |
| Verbosity bias | The judge prefers longer answers | cap length |
| Self-preference | The judge prefers its own model family | judge with a different model |
| Judge validation | Measuring judge-human agreement | kappa on a sample |
| Golden-set anchor | The judge grades where human answers are known | judge accuracy measured |

---

## Alphabetical Glossary

### Golden-set anchor

**Definition:** The judge grades the golden set, where human answers are
known. The judge's grades are compared to human grades; judge accuracy is
itself a metric.

**Example:**
```python
# judge grade vs human grade on the same golden query
```

**Related concepts:** Judge validation

---

### Judge

**Definition:** A model that grades output against a rubric, deterministically
in structure. Same input, same rubric, same grade — regressions visible.

**Example:**
```python
# judge_prompt with criteria, scale, and JSON output format
```

**Related concepts:** Rubric, Judge validation

---

### Judge validation

**Definition:** Measuring the judge's agreement with human labels on a
sample. A judge that disagrees with humans is not measuring what it claims.

**Example:**
```python
# judge vs human on 50 queries -> agreement measured
```

**Related concepts:** Judge, Golden-set anchor

---

### Position bias

**Definition:** The judge prefers the first answer presented. Mitigated by
randomizing order.

**Example:**
```python
# answer A graded higher when listed first
```

**Related concepts:** Verbosity bias, Self-preference

---

### Rubric

**Definition:** The criteria and scale the judge applies. Without a rubric
the judge improvises criteria.

**Example:**
```python
# faithfulness (0-1), helpfulness (0-1)
```

**Related concepts:** Judge

---

### Self-preference

**Definition:** The judge prefers answers from its own model family.
Mitigated by judging with a different model family than the one answering.

**Example:**
```python
# model A's answers graded higher by model A
```

**Related concepts:** Position bias

---

### Verbosity bias

**Definition:** The judge prefers longer answers. Mitigated by capping
length.

**Example:**
```python
# a padded answer graded higher than a concise one
```

**Related concepts:** Position bias

---

## Related Concepts

- **Faithfulness**: the judge decides claim support (topic 02)
- **Gold dataset**: the judge grades where human answers are known (topic 01)
- **Adversarial evaluation**: the judge also grades attack resistance (topic 05)

## Key Takeaways

1. A judge grades output against a rubric, deterministically.
2. Judges have position, verbosity, and self-preference bias.
3. Validate the judge against human labels.
4. Judges scale human judgment; they do not replace it.
5. The judge grades the golden set, and its own accuracy is measured.