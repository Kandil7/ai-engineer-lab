# RAG System 05: Abstention and Citations

## Topic Overview

A RAG answer is only as trustworthy as its evidence. Two behaviors make the answer
trustworthy: abstention, where the model refuses to answer when the evidence is absent, and
citations, where the answer points at the exact evidence it used. Together they are the
roadmap's exit test for this module, and they are the difference between a system that can be
trusted with a knowledge task and one that only looks like it can.

Abstention is a correctness feature, not a failure. A confident wrong answer is worse than an
honest refusal, because the user cannot tell the wrong answer from a right one. Citations are
the other half: they let the user verify the answer against the source, which is the whole
point of retrieval.

This lecture covers abstention on thin context, citation-required answers, backend validation
that rejects fabricated citation ids, and the tests that keep both behaviors working.

## Learning Objectives

By the end of this lecture, you will be able to:

1. Make the model abstain when the context cannot support an answer.
2. Require every claim to cite an evidence id from the context.
3. Validate cited ids against the context in the backend and reject fabrications.
4. Return citations that resolve to the original text and source.
5. Test abstention and citation integrity as permanent gates.
6. Explain why abstention is a feature rather than a failure.

## Prerequisites

- RAG System 04 (context construction) for the context and evidence ids.
- AI Evaluation 02 (faithfulness and citation precision) for measuring the result.

---

## 1. Abstention

### The rule in the prompt

The model must refuse to answer when the evidence is absent or contradictory. The prompt states
the rule plainly:

```text
Answer only from the context. If the context does not contain the answer,
state that you cannot answer. Never guess.
```

### Why it is a feature

A system that always answers will answer questions outside its corpus, and it will sound
confident while doing it. That is the hallucination failure mode of RAG, and abstention is the
guard. An honest "I cannot answer that from the sources" is more useful than a plausible
fabrication, because the user can act on the refusal.

### The trigger

Abstention triggers on thin context (RAG System 04) and on contradiction detection (RAG System
07). Both are detectable signals, not model judgment calls, which is what makes abstention
reliable rather than occasional.

## 2. Citation-Required Answers

### Every claim cites an id

Every claim in the answer cites an evidence id from the context. The structured output enforces
this mechanically: the answer is a list of claims, each with an evidence id.

```python
{"answer": "الصلاة على المؤمن", "citations": ["b1:p7:0"]}
```

### A claim without a citation is a hallucination by construction

If the structured output requires a citation per claim, then a claim with no citation cannot be
emitted; the model must either find an evidence id or drop the claim. This shifts the
hallucination guard from "does the answer look right" to "does every claim have a handle",
which is checkable.

### Why structured output

Free-text answers cannot be validated for grounding. Structured output with per-claim
citations makes the answer a data structure the backend can check, which is what makes the
guard real rather than aspirational.

## 3. Rejecting Fabricated Citations

### The validation

The backend validates every cited id against the context ids. A citation the model invented,
not present in the context, is rejected:

```python
def validate_citations(cited, context_ids):
    """Every cited id must be in the context. Rejects fabricated ids."""
    return all(c in context_ids for c in cited)
```

### Why the model cannot be trusted here

A model can produce a plausible-looking id that was never in the context, especially under
pressure to answer. The backend check is mechanical and cannot be fooled: the cited ids must be
a subset of the context ids. This is the roadmap's exit test that the model does not accept a
fabricated citation id.

### What happens on rejection

A rejected citation is a failure to retry or abstain, not a failure to hide. The pipeline
should re-prompt, drop the unsupported claim, or abstain, and log the event, because a
fabricated citation is a symptom of a context or prompt problem.

## 4. Citations with Links

### Resolving to the source

Each citation resolves to the original text and its source link, using the passage's
provenance (book_id, page, source_version). The user can click through to verify the answer
against the book.

### Why links matter

A citation without a resolvable source is a claim of grounding, not grounding. The link is what
lets the user check the answer, and it is the visible form of the pipeline's honesty.

### The two-text link

The linked text is the `original` form (Arabic NLP 01). The citation shows what the book
actually says, not a normalized paraphrase of it.

## 5. Testing

### The two tests

```python
def test_abstention():
    answer = generate("ما حكم الصوم", thin_context)
    assert answer["abstained"]  # refused, did not guess


def test_citation_integrity():
    answer = generate("الصلاة", context)
    assert validate_citations(answer["citations"], context_ids)
```

### Why both are gates

Both failure modes are named explicitly in the roadmap, and both belong in CI. Abstention
without evidence and fabricated citations are the two ways a RAG answer lies, and neither
should be able to ship undetected.

### The adversarial set

The adversarial evaluation (AI Evaluation 05) extends these tests with attacks that try to
provoke a fabrication or a non-abstention, so the guards are tested against hostile input, not
only cooperative input.

## Real-World Application

- Athar abstaining on a question whose answer is not in the corpus rather than inventing a
  ruling.
- Requiring per-claim citations so a fiqh answer's every statement traces to a passage.
- Rejecting a fabricated evidence id in the backend and re-prompting the generator.
- Displaying citations that link to the diacritized original passage for verification.

## Common Mistakes

1. **No abstention rule.** The model guesses on thin context.
2. **Claims without citations.** Hallucination by construction.
3. **Trusting the model's cited ids.** Fabrications pass through.
4. **Citations that do not resolve.** Grounding is claimed, not provided.
5. **No CI gate.** The two failure modes ship undetected.
6. **Treating abstention as a failure.** It is the correct behavior on absent evidence.

## Key Takeaways

1. Abstention on absent evidence is a correctness feature; a confident wrong answer is worse
   than an honest refusal.
2. Every claim cites an evidence id; structured output makes a citation-free claim
   unrepresentable.
3. The backend validates cited ids against the context and rejects fabrications; the model
   cannot be trusted to.
4. Citations resolve to the original text and source, so the user can verify.
5. Abstention and citation integrity are permanent CI gates, extended by the adversarial set.

## Self-Check Questions

1. Why is abstention a feature rather than a failure, and what triggers it?
2. How does structured output make a citation-free claim impossible?
3. Why is backend validation necessary when the model already cites ids?
4. What should happen when a fabricated citation is detected?
5. Why must the citation link resolve to the original text rather than the normalized form?

## Further Reading / Connections

- RAG System 04 (context construction) — the context and evidence ids this relies on.
- RAG System 07 (context failure modes) — missing and contradictory material.
- AI Evaluation 02 (faithfulness and citation precision) — measuring grounding.
- AI Evaluation 05 (adversarial evaluation) — attacks that probe abstention and citations.
