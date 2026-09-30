# AI Evaluation 02: Faithfulness and Citation Precision

## Topic Overview

A RAG system can retrieve the right passages and still produce a wrong or
misleading answer. Retrieval metrics (recall@k, MRR) measure what comes
into the context. Faithfulness and citation precision measure what comes
out — the answer itself. These are the answer-side metrics, and they are
the ones the user experiences.

Faithfulness asks: **is every claim in the answer supported by the
context?** A claim that is true in the world but absent from the context
is still a hallucination from the system's perspective — the system has
no way to verify it. Citation precision asks: **do the cited evidence ids
actually support the claims they are attached to?** A citation that points
at an irrelevant passage is an error even if the claim happens to be true.

Together, these two metrics define answer quality. They are measured on
the golden set (where answers are verified) and enforced as CI gates.

## Learning Objectives

By the end of this lecture, you will be able to:

1. Define faithfulness and distinguish it from relevance
2. Compute claim-level support from the context
3. Compute citation precision (supported / cited)
4. Distinguish citation validity from citation support
5. Detect unsupported claims mechanically and with a judge
6. Design the faithfulness test for CI
7. Connect faithfulness to the user's trust in the system

## Prerequisites

- Retrieval evaluation (ai-evaluation 03)
- Context construction (rag-system 04)
- LLM-as-judge basics (ai-evaluation 04)

---

## 1. Faithfulness vs Relevance

### The distinction

| Dimension | Measures | Question | Side |
|-----------|----------|----------|------|
| **Relevance** | Retrieval quality | Did we find the right passages? | Input |
| **Faithfulness** | Answer quality | Is the answer supported by the context? | Output |

A system can be perfectly relevant and completely unfaithful:

```
Query: "ما حكم الصلاة في السفر؟"
Relevant context retrieved: [passage about travel prayer rules] ✓
Answer: "الصلاة في السفر تجب تماماً كما في الحضر" ✗ (contradicts the context)

→ Relevant but unfaithful
```

And the reverse: a system can retrieve poorly but the model happens to
give a correct answer from its parametric knowledge:

```
Query: "ما حكم الصلاة في السفر؟"
Irrelevant context retrieved: [passage about fasting] ✗
Answer: "القصر جائز للمسافر" ✓ (correct from pretraining)

→ Irrelevant but faithful? No — faithful to WHAT? The context says fasting.
```

This is why both metrics are needed. Relevance without faithfulness is a
correct pipeline producing wrong answers. Faithfulness without relevance
is luck.

### The formal definition

An answer is **faithful** if and only if every claim in the answer is
entailed by at least one passage in the context.

```
∀ claim ∈ Answer: ∃ passage ∈ Context such that passage ⊨ claim
```

A claim the context does not support is a **hallucination**, even if it
is factually true in the world.

---

## 2. Claim-Level Faithfulness

### Why claim-level

The answer is not a single statement — it is a sequence of claims. Each
claim must be checked independently. A whole-answer check ("is this
answer supported?") hides partial errors.

```
Answer: "القصر جائز للمسافر، والجمع بين الصلاتين جائز، وصوم رمضان واجب"

Claim 1: "القصر جائز للمسافر"           → supported by context ✓
Claim 2: "الجمع بين الصلاتين جائز"       → supported by context ✓
Claim 3: "صوم رمضان واجب"               → NOT in context ✗ (hallucination)

Whole-answer check: "mostly supported" → hides claim 3
Claim-level check: 2/3 faithful, 1 hallucination
```

### Decomposing the answer into claims

For English, claim decomposition is straightforward (split by sentence or
clause). For Arabic, the same principle applies:

```python
def decompose_claims(answer: str) -> list[str]:
    """Split an answer into individual claims."""
    # Arabic sentence separators: . ؛ ؟ !
    import re

    claims = re.split(r"[.؛؟!]\s*", answer)
    return [c.strip() for c in claims if c.strip()]
```

### Checking support

A claim is supported if at least one context passage entails it. In
practice, "entails" is checked by:
1. **Keyword overlap** (cheap, approximate)
2. **Semantic similarity** (embedding-based)
3. **Judge model** (expensive, accurate)

```python
def is_supported(claim: str, context: list[str]) -> bool:
    """Check if any context passage supports the claim."""
    claim_terms = set(claim.split())
    for passage in context:
        passage_terms = set(passage.split())
        overlap = claim_terms & passage_terms
        if len(overlap) >= len(claim_terms) * 0.5:
            return True
    return False
```

The keyword approach is a baseline. A judge model (topic 04) is more
accurate for nuanced support.

---

## 3. Citation Precision

### What it measures

Citation precision is the fraction of citations that actually support
their claims.

```
Citation Precision = (citations that support their claim) / (total citations)
```

### The two levels

| Level | Check | Cost | Example |
|-------|-------|------|---------|
| **Validity** | The cited id exists in the context | Free (mechanical) | "b3:p12:0" is in context_ids |
| **Support** | The cited passage backs the claim | Judge or human | The passage entails the claim |

### Validity (mechanical)

```python
def citation_validity(cited: list[str], context_ids: set[str]) -> bool:
    """Every cited id must be in the context. Free to check."""
    return all(c in context_ids for c in cited)
```

A fabricated citation id — one the model invented — is rejected by
validity checking. This is the roadmap's exit test: "the model does not
accept a fabricated backend citation id."

### Support (judge or human)

```python
def citation_support(claim: str, passage: str, judge) -> bool:
    """Does the passage support the claim? Needs a judge."""
    return judge.entails(passage, claim)
```

Support is not mechanical. It requires understanding whether the passage
logically entails the claim. A judge model (LLM-as-judge) is the scalable
approach.

### Computing precision

```python
def citation_precision(citations: list[dict]) -> float:
    """Fraction of citations that support their claims."""
    supported = sum(1 for c in citations if c["supports_claim"])
    return supported / len(citations) if citations else 0.0


# Example:
# citations = [
#     {"id": "b3:p12:0", "supports_claim": True},
#     {"id": "b3:p12:1", "supports_claim": True},
#     {"id": "b3:p12:2", "supports_claim": True},
#     {"id": "b9:p1:0", "supports_claim": False},  # cited but doesn't support
# ]
# precision = 3/4 = 0.75
```

---

## 4. Unsupported Claims and Hallucination

### What is an unsupported claim?

A claim is unsupported when the context does not provide evidence for it.
This includes:
- Claims that contradict the context
- Claims that go beyond what the context says
- Claims that are true in the world but absent from the context

### Why "true in the world" is not enough

```
Context: "القصر هو رفع بعض الصلاة للمسافر"
Claim: "القصر جائز للمسافر"

The claim is true in the world AND supported by the context. ✓ Faithful.
```

```
Context: "القصر هو رفع بعض الصلاة للمسافر"
Claim: "الصلاة في السفر مبطلة"

The claim is false AND contradicts the context. ✗ Unfaithful.
```

```
Context: [passage about fasting]
Claim: "القصر جائز للمسافر"

The claim is true in the world BUT not supported by the context. ✗ Unfaithful.
The system has no basis for this claim from the retrieved material.
```

The third case is the subtle one. The system must abstain or cite a
source — it cannot rely on parametric knowledge when the task is
grounded generation.

### The faithfulness score

```
Faithfulness = (supported claims) / (total claims)
```

A faithful answer scores 1.0. An answer with one hallucination in five
claims scores 0.8. The threshold for CI is typically 0.9 or higher.

---

## 5. Measuring on the Golden Set

### Why the golden set

The golden set has verified answers and known relevant passages. This
means we know which claims should be supported and which citations should
be valid. We can compute faithfulness and citation precision as ground
truth, not estimates.

### The test procedure

```python
def test_faithfulness(golden_set, system):
    for case in golden_set:
        answer = system.answer(case["query"], case["context"])
        claims = decompose_claims(answer["text"])

        for claim in claims:
            supported = is_supported(claim, case["context"])
            if not supported:
                report(f"Unsupported claim: {claim}")

        precision = citation_precision(answer["citations"])
        assert precision >= 0.9, f"Citation precision {precision} below threshold"
```

### The CI gate

| Metric | Threshold | Failure action |
|--------|-----------|----------------|
| Faithfulness | ≥ 0.9 | Block merge |
| Citation precision | ≥ 0.9 | Block merge |
| Citation validity | = 1.0 | Block merge (fabricated ids) |
| Abstention rate | Per golden set | Report only |

The gates run on every change. A change that improves recall@5 but drops
faithfulness is a regression, not an improvement.

---

## 6. The Judge Model Approach

### When to use a judge

For nuanced support checking ("does this passage entail this claim?"),
keyword overlap is insufficient. A judge model evaluates the semantic
relationship.

### The judge prompt

```text
Given a claim and a passage, determine if the passage supports the claim.

Claim: {claim}
Passage: {passage}

Answer: SUPPORTED or NOT_SUPPORTED
Reason: {one sentence}
```

### Judge validation

The judge must be validated against human labels. If the judge disagrees
with humans on support judgments, it is measuring something else.

```
Judge-human agreement target: ≥ 85%
If below: re-calibrate the judge prompt or use human labels
```

### Judge cost

A judge call costs one LLM inference per claim. For 50 golden queries ×
3 claims × 2 checks = 300 judge calls. At $0.001 per call, this is $0.30
per evaluation run — negligible compared to the cost of shipping
hallucinations.

---

## 7. The User's Perspective

### What the user experiences

| Metric | User symptom when low |
|--------|----------------------|
| Faithfulness | "The answer is wrong / made up" |
| Citation precision | "The citations don't match the claims" |
| Validity | "The citation link is broken" |

### Trust erosion

A single hallucination destroys trust more than a wrong retrieval. If the
retrieval is wrong, the user sees "the system didn't find the right
passage." If the answer hallucinates, the user sees "the system lied to
me." Faithfulness is the trust metric.

---

## Real-World Application

In the Athar project:

1. The golden set has 50 Arabic queries with verified answers.
2. Each answer is decomposed into claims.
3. Each claim is checked against the context (keyword + judge).
4. Citations are validated (ids exist) and judged (passages support).
5. The CI gate blocks changes that drop faithfulness below 0.9.
6. Production monitoring tracks the faithfulness rolling average.

The pipeline ensures that every answer is grounded in the retrieved
Islamic text and every citation traces to a real source location.

---

## Common Mistakes

1. **Confusing relevance with faithfulness** — high recall@5 does not
   mean the answer is supported.

2. **Whole-answer checks** — missing individual hallucinated claims.

3. **Treating "true in the world" as faithful** — the claim must be
   supported by the context, not just true.

4. **Counting validity as support** — a real citation id that points at
   an irrelevant passage is still wrong.

5. **No judge for nuanced support** — keyword overlap misses paraphrases
   and partial support.

6. **No CI gate** — faithfulness degrades silently with each change.

7. **Ignoring citation precision** — a correct claim with a wrong citation
   is still a citation error.

---

## Key Takeaways

1. Relevance is input-side; faithfulness is output-side. Both are needed.
2. Faithfulness = every claim is supported by the context.
3. Citation precision = citations that support their claims / total citations.
4. Validity (id exists) is mechanical; support (passage backs claim) needs a judge.
5. A claim true in the world but absent from the context is still a hallucination.

---

## Self-Check Questions

1. What is the difference between relevance and faithfulness?
2. Why is a claim that is true in the world but absent from the context
   still a hallucination?
3. What is the difference between citation validity and citation support?
4. How do you compute citation precision?
5. Why must the faithfulness metric run as a CI gate?

---

## Further Reading / Connections

- **ai-evaluation 01** — Gold datasets (where the answers are verified)
- **ai-evaluation 03** — Retrieval evaluation (the input-side metrics)
- **ai-evaluation 04** — LLM-as-judge (for support checking)
- **rag-system 05** — Abstention and citations (the system behavior)
- **rag-system 07** — Context failure modes (where bad context comes from)