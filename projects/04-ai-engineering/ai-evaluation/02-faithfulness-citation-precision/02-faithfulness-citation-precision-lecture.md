# AI Evaluation 02: Faithfulness and Citation Precision

## 🎯 Topic Overview

Retrieval quality is not answer quality. A RAG system can retrieve the
right passages and still generate a wrong or unsupported answer. Faithfulness
measures whether the answer is supported by the context; citation precision
measures whether the cited evidence actually supports the claim. Together
they are the roadmap's exit test for answer quality.

## 📚 Learning Objectives

By the end of this lecture, you will be able to:

1. Define faithfulness and why retrieval metrics do not cover it
2. Compute citation precision from the answer's citations
3. Detect unsupported claims (hallucination) mechanically
4. Distinguish faithfulness from relevance
5. Use both metrics as CI gates

---

## 1. Faithfulness vs Relevance

Relevance asks "did we retrieve the right passages?" Faithfulness asks "is
the answer supported by what we retrieved?" A system can be perfectly
relevant and completely unfaithful: the right passages retrieved, the
answer invented. Faithfulness is the answer-side metric; relevance is the
retrieval-side metric. Both are needed.

## 2. Faithfulness

An answer is faithful when every claim in it is supported by the context.
The check is claim-level: split the answer into claims, and for each claim
ask whether the context supports it. The roadmap's exit test: "the answer
is faithful to the context." A claim the context does not support is a
hallucination, even if it is true in the world.

```python
def is_supported(claim, context):
    # does any context passage entail the claim?
    ...
```

## 3. Citation Precision

Citation precision is the fraction of the answer's citations that actually
support the claim they are attached to. A citation that points at an
irrelevant passage is a citation error even if the claim is true. The
roadmap's exit test: "citation precision is high."

```python
def citation_precision(cited, supported):
    return sum(supported) / len(cited)
```

## 4. The Mechanical Checks

Both metrics have mechanical components. Citation validity — the cited id
exists in the context — is pure validation. Citation support — the cited
passage actually backs the claim — needs a judge or a human. The mechanical
checks run in CI; the judge-based checks run on the golden set.

## 5. The Golden Set Anchor

Faithfulness and citation precision are measured on the golden set, where
the answers are verified. A change that improves retrieval but degrades
faithfulness is a regression, not an improvement. The two metrics gate
together: high recall with low faithfulness is a failed change.

## Common Mistakes

- Reporting retrieval metrics as answer quality.
- Confusing a true claim with a supported claim.
- Counting citation validity as citation support.
- Tuning for recall while faithfulness drops.
- No claim-level decomposition (whole-answer checks miss partial errors).

## Key Takeaways

1. Relevance is retrieval-side; faithfulness is answer-side.
2. A claim must be supported by the context, not merely true.
3. Citation precision is the fraction of citations that support their claim.
4. Validity (id exists) is not support (passage backs the claim).
5. Faithfulness and citation precision gate together in CI.