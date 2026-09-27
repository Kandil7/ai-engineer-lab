# Fine-Tuning 06: RAG vs Fine-Tuning — Glossary

## Quick Reference Table

| Term | Definition | Example |
|------|-----------|---------|
| RAG | Knowledge supplied at query time | retrieval + citations |
| Fine-tuning | Behavior shaped at training time | format + style |
| Query-time cost | Retrieval latency, embedding, context budget | per query |
| Training-time cost | Data curation, GPU hours, overfitting risk | per run |
| Hybrid | RAG for facts, fine-tuning for behavior | standard production shape |
| ADR | The recorded decision with rationale | the choice as evidence |

---

## Alphabetical Glossary

### ADR

**Definition:** Architecture decision record: the problem, the options, the
chosen split, and the rationale. Evidence the choice was deliberate.

**Example:**
```python
# "RAG for knowledge, fine-tuning for behavior" as a recorded decision
```

**Related concepts:** Hybrid

---

### Fine-tuning

**Definition:** Behavior shaped at training time. Good for stable formats,
styles, and instruction patterns; costs data curation and GPU hours.

**Example:**
```python
# a model trained to follow the citation format
```

**Related concepts:** RAG, Hybrid

---

### Hybrid

**Definition:** RAG supplies the facts, fine-tuning shapes how the model
uses them. The standard production shape.

**Example:**
```python
# fine-tuned citation behavior + a retriever feeding the context
```

**Related concepts:** RAG, Fine-tuning

---

### Query-time cost

**Definition:** What RAG costs per query: retrieval latency, embedding
cost, and the context budget.

**Example:**
```python
# every query pays retrieval + embedding + context tokens
```

**Related concepts:** RAG

---

### RAG

**Definition:** Knowledge supplied at query time. Good when knowledge
changes, is too large to train in, or must be cited.

**Example:**
```python
# a retriever feeds the context; every answer cites its source
```

**Related concepts:** Fine-tuning, Query-time cost

---

### Training-time cost

**Definition:** What fine-tuning costs per run: data curation, GPU hours,
and the risk of overfitting.

**Example:**
```python
# a new run for every behavior change
```

**Related concepts:** Fine-tuning

---

## Related Concepts

- **SFT**: the behavior side of the split (topic 01)
- **RAG system**: the knowledge side of the split (rag-system section)
- **Model registry**: the fine-tuned model is registered (topic 05)

## Key Takeaways

1. RAG is the tool for knowledge.
2. Fine-tuning is the tool for behavior.
3. RAG costs at query time; fine-tuning costs at training time.
4. The hybrid is the standard production shape.
5. The decision is written as an ADR.