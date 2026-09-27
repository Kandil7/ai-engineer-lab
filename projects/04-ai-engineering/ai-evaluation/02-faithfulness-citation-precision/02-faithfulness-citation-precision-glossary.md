# AI Evaluation 02: Faithfulness and Citation Precision — Glossary

## Quick Reference Table

| Term | Definition | Example |
|------|-----------|---------|
| Faithfulness | Every claim in the answer is supported by the context | claim-level check |
| Relevance | Did we retrieve the right passages? | retrieval-side metric |
| Citation precision | Fraction of citations that support their claim | supported / cited |
| Citation validity | The cited id exists in the context | mechanical check |
| Citation support | The cited passage backs the claim | judge or human |
| Unsupported claim | A claim the context does not support | hallucination |
| Claim-level check | Splitting the answer into claims and checking each | partial errors caught |

---

## Alphabetical Glossary

### Citation precision

**Definition:** The fraction of the answer's citations that actually support
the claim they are attached to. A citation pointing at an irrelevant passage
is an error even if the claim is true.

**Example:**
```python
# 3 of 4 citations support their claims -> 0.75
```

**Related concepts:** Citation validity, Citation support

---

### Citation support

**Definition:** The cited passage actually backs the claim. Needs a judge or
a human; not a mechanical check.

**Example:**
```python
# the cited passage entails the claim
```

**Related concepts:** Citation precision, Citation validity

---

### Citation validity

**Definition:** The cited id exists in the context. A pure mechanical
validation, distinct from support.

**Example:**
```python
# cited id in context_ids -> valid
```

**Related concepts:** Citation support, Citation precision

---

### Claim-level check

**Definition:** Splitting the answer into claims and checking each against
the context. Whole-answer checks miss partial errors.

**Example:**
```python
# "القصر جائز، والجمع ممنوع" -> two claims, each checked
```

**Related concepts:** Faithfulness

---

### Faithfulness

**Definition:** Every claim in the answer is supported by the context. A
true claim the context does not support is still a hallucination.

**Example:**
```python
# claim supported by a context passage -> faithful
```

**Related concepts:** Relevance, Unsupported claim

---

### Relevance

**Definition:** Did we retrieve the right passages? The retrieval-side
metric. Faithfulness is the answer-side metric; both are needed.

**Example:**
```python
# recall@5 on the golden set
```

**Related concepts:** Faithfulness

---

### Unsupported claim

**Definition:** A claim the context does not support. A hallucination even
if true in the world.

**Example:**
```python
# answer claims X, no context passage supports X
```

**Related concepts:** Faithfulness

---

## Related Concepts

- **Gold dataset**: faithfulness is measured on verified answers (topic 01)
- **Retrieval evaluation**: relevance metrics (topic 03)
- **LLM-as-judge**: the judge that decides support (topic 04)

## Key Takeaways

1. Relevance is retrieval-side; faithfulness is answer-side.
2. A claim must be supported by the context, not merely true.
3. Citation precision is the fraction of citations that support their claim.
4. Validity (id exists) is not support (passage backs the claim).
5. Faithfulness and citation precision gate together in CI.