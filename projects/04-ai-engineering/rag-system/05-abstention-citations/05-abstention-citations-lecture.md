# RAG System 05: Abstention and Citations

## 🎯 Topic Overview

A RAG answer is only as trustworthy as its evidence. Abstention is the
model refusing to answer when the evidence is absent; citations are the
answer pointing at the exact evidence it used. Together they are the
roadmap's exit test: the model abstains without evidence, and it never
accepts a fabricated citation id.

## 📚 Learning Objectives

By the end of this lecture, you will be able to:

1. Make the model abstain when the context cannot support an answer
2. Require every claim to cite an evidence id from the context
3. Reject fabricated citation ids (backend validation)
4. Return citations with links to the original text
5. Test abstention and citation integrity

---

## 1. Abstention

The model must refuse to answer when the evidence is absent or
contradictory. The prompt states the rule: "If the context does not contain
the answer, say you cannot answer." Abstention is a correctness feature,
not a failure — a confident wrong answer is worse than an honest refusal.
The roadmap exit test: "the model abstains when evidence is absent."

```python
# The abstention contract in the prompt
"Answer only from the context. If the context does not contain the answer,
 state that you cannot answer. Never guess."
```

## 2. Citation-Required Answers

Every claim in the answer cites an evidence id from the context. The
structured output enforces this: the answer is a list of claims, each with
an evidence id. A claim without a citation is a hallucination by
construction.

```python
{"answer": "الكتاب على المكتب", "citations": ["b1:p7:0"]}
```

## 3. Rejecting Fabricated Citations

The backend validates every cited id against the context. A citation id the
model invented — not in the context — is rejected. This is the roadmap's
exit test: "the model does not accept a fabricated backend citation id."
The validation is mechanical: the cited ids must be a subset of the context
ids.

```python
def validate_citations(cited, context_ids):
    return all(c in context_ids for c in cited)
```

## 4. Citations with Links

Each citation resolves to the original text and its source link — the
passage's provenance (book_id, page, source_version). The user can click
through to the source. The citation is the bridge from the answer to the
evidence.

## 5. Testing

```python
def test_abstention():
    answer = generate("سؤال بلا دليل", thin_context)
    assert answer["abstained"]  # refused, did not guess


def test_citation_integrity():
    answer = generate("سؤال", context)
    assert validate_citations(answer["citations"], context_ids)
```

Both tests belong in CI. Abstention without evidence and fabricated
citations are the two failure modes the roadmap names explicitly.

## Common Mistakes

- The model guessing on thin context (no abstention rule).
- Claims without citations (hallucination by construction).
- Trusting the model's cited ids without backend validation.
- Citations that do not resolve to the original text.

## Key Takeaways

1. Abstain when evidence is absent.
2. Every claim cites an evidence id.
3. Validate cited ids against the context.
4. Citations resolve to the original source.