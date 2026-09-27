# RAG System 05: Abstention and Citations — Glossary

## Quick Reference Table

| Term | Definition | Example |
|------|-----------|---------|
| Abstention | Refusing to answer when evidence is absent | "cannot answer" |
| Citation | An evidence id attached to a claim | b1:p7:0 |
| Fabricated citation | A cited id not in the context | rejected by backend |
| Citation validation | Cited ids must be a subset of context ids | mechanical check |
| Evidence id | The chunk identifier a claim traces to | b1:p7:0 |
| Source link | The original text + provenance a citation resolves to | book/page/version |
| Hallucination | A claim without a citation | by construction |

---

## Alphabetical Glossary

### Abstention

**Definition:** The model refusing to answer when the context cannot support
an answer. A correctness feature, not a failure.

**Example:**
```python
# "لا أستطيع الإجابة من النص المقدم" on thin context
```

**Related concepts:** Thin context, Hallucination

---

### Citation

**Definition:** An evidence id attached to a claim, tracing it to the
context. A claim without a citation is a hallucination by construction.

**Example:**
```python
{"answer": "الكتاب على المكتب", "citations": ["b1:p7:0"]}
```

**Related concepts:** Evidence id, Citation validation

---

### Citation validation

**Definition:** The mechanical check that every cited id is in the context.
Rejects fabricated citations the model invented.

**Example:**
```python
all(c in context_ids for c in cited)
```

**Related concepts:** Fabricated citation, Evidence id

---

### Evidence id

**Definition:** The chunk identifier a claim traces to. The unit of
citation.

**Example:**
```python
# "b1:p7:0" = book b1, page 7, chunk 0
```

**Related concepts:** Citation, Source link

---

### Fabricated citation

**Definition:** A cited id the model invented, not present in the context.
The roadmap's exit test: the backend must reject it.

**Example:**
```python
# model cites "b9:p99" which is not in the context -> rejected
```

**Related concepts:** Citation validation

---

### Hallucination

**Definition:** A claim without a supporting citation. Made impossible by
construction when every claim must cite.

**Example:**
```python
# a claim with no evidence id is rejected at output
```

**Related concepts:** Abstention, Citation

---

### Source link

**Definition:** The original text and provenance a citation resolves to —
book_id, page, source_version. The user's path to the evidence.

**Example:**
```python
# citation -> original text -> book b1, page 7, version v1
```

**Related concepts:** Evidence id, Provenance

---

## Related Concepts

- **Context construction**: the evidence ids come from the context (topic 04)
- **Provenance**: citations resolve to provenance (data-engineering 06)
- **Faithfulness**: the eval metric for claim-evidence alignment (stage 10)

## Key Takeaways

1. Abstain when evidence is absent.
2. Every claim cites an evidence id.
3. Validate cited ids against the context.
4. Citations resolve to the original source.