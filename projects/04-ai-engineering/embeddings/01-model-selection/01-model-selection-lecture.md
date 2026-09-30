# Embeddings 01: Model Selection

## Topic Overview

The embedding model decides retrieval quality more than any other single component. It is what
turns text into the vectors the dense arm searches, and its choices (dimensions, language
coverage, cost) propagate through storage, search speed, and accuracy. Choosing it badly, or
defaulting to whatever is popular, is a silent quality ceiling on everything downstream.

This lecture covers the selection axes (dimensions, cost, speed, language coverage, quality),
why language coverage is a hard filter for Arabic, how the deployment context (prototype versus
production) shifts the choice, and the consistency rule that the same model must embed both the
corpus and the queries.

The consistency rule is the one that causes the most damage when violated: if the corpus and
the queries are embedded with different models, they live in different vector spaces and the
similarity scores are meaningless. That is why the model version is recorded with the index
(RAG System 06, Arabic NLP 04).

## Learning Objectives

By the end of this lecture, you will be able to:

1. Compare embedding models on dimensions, cost, speed, and quality.
2. Treat language coverage as a hard filter for the corpus language.
3. Choose for the deployment context (prototype versus production).
4. Keep one model consistent across the corpus and the queries.
5. Re-evaluate the choice when the corpus changes.

## Prerequisites

- Arabic NLP 04 (Arabic embeddings) for the language-coverage problem.
- Applied ML 01 (vectors and similarity) for the geometric background.

---

## 1. The Axes

### Dimensions

More dimensions can capture more nuance but cost more to store and slower to search, because
each vector is larger and each distance computation is longer. The gain from more dimensions is
real but diminishing and task-dependent.

### Cost and speed

Some models are free to self-host, others are billed per token by an API. A larger model is
usually slower as well as more expensive. The cost axis is measured per useful answer, not per
token (Model Serving 01).

### Quality

Quality is not a single number; it is task- and language-specific. A model that tops a general
benchmark may be weak on Arabic or on code. Evaluate quality on your own golden set.

| Model | Dims | Cost | Multilingual |
| --- | --- | --- | --- |
| all-MiniLM-L6-v2 | 384 | Free | No |
| nomic-embed-text | 768 | Free | Yes |
| text-embedding-3-small | 1536 | Low | Yes |
| text-embedding-3-large | 3072 | High | Yes |

## 2. Language Coverage Is a Hard Filter

### The rule

For an Arabic corpus, the model must handle Arabic. A monolingual English model embeds Arabic
poorly, so it is not a candidate regardless of its quality score. Language coverage filters the
candidate list before any evaluation.

```python
candidates = [
    m for m, p in MODELS.items() if p["multilingual"] or corpus_language == "en"
]
```

### Why it is a filter, not a preference

A model without Arabic coverage does not produce a slightly worse vector; it produces a vector
in which Arabic structure is noise. The failure is silent: the model runs, the search returns
results, and the results are subtly wrong. This is why coverage is a gate, not a tiebreaker.

### The cost of getting it wrong

Discovering a coverage failure after ingesting a large corpus means re-embedding the whole
corpus, which is expensive and slow. Filtering on coverage first avoids the re-index.

## 3. The Deployment Context

### Prototype

A prototype wants speed of iteration and zero cost. The smallest multilingual model that covers
the language is the right choice, because it is fast and free and the quality bar is provisional.

```python
assert choose("ar", "prototype") == "nomic-embed-text"  # smallest multilingual
```

### Production

Production balances quality against cost at corpus scale. A cost-sensitive deployment prefers a
free self-hosted model; a quality-first deployment pays for a stronger API model. The choice is
recorded in an ADR with the measured numbers.

### The staging trap

A model chosen for the prototype and never revisited is a common way to ship a mediocre
production system. The prototype choice is a starting point to be re-evaluated, not a default
to be kept.

## 4. Consistency Across the Pipeline

### One model for corpus and queries

The corpus vectors and the query vectors must come from the same model:

```python
corpus_model = choose("ar", "production")
query_model = choose("ar", "production")
assert corpus_model == query_model, "one model across the pipeline"
```

### Why a mismatch is fatal

Different models define different spaces, so a cosine between a query from model A and a passage
from model B is meaningless. The retrieval would return essentially arbitrary results while
looking superficially functional.

### The versioning consequence

Because changing the model changes the space, the model version is part of the index's
configuration (RAG System 06). A model change is a re-embed of the whole corpus, scheduled
deliberately, never a silent swap.

## 5. Re-Evaluation

### When

The choice is re-evaluated when the corpus changes (a growth in Arabic content may need a
stronger Arabic model), when a better model is released, or when the cost or latency budget
changes.

### How

Re-evaluation runs the golden set (Embeddings 04) with the same protocol as the original choice,
so the comparison is fair across time. A new model's headline claim is not a reason to switch
until it wins on the golden set.

### The ADR

The choice and its re-evaluation triggers are recorded, so a later swap is a deliberate,
measured decision.

## Common Mistakes

1. **A monolingual model for an Arabic corpus.** Silent, systematic quality loss.
2. **Mixing models across the pipeline.** Query and corpus in different spaces.
3. **Choosing dimensions without measuring quality.** More is not automatically better.
4. **Never re-evaluating.** The system is stuck on a prototype-era model.
5. **Ignoring cost.** A high-quality model can be unaffordable at scale.
6. **Swapping the model without re-embedding.** The index and the queries diverge.

## Key Takeaways

1. The model choice trades dimensions, cost, speed, language coverage, and quality.
2. Language coverage is a hard filter; a model without Arabic coverage is not a candidate.
3. Prototype picks the smallest covering model; production balances quality and cost.
4. One model must embed both the corpus and the queries; a mismatch is fatal and silent.
5. Re-evaluate on corpus, model, or budget change, and record the choice as an ADR.

## Self-Check Questions

1. Why is language coverage a filter rather than a tiebreaker?
2. What happens to retrieval if the corpus and queries use different models?
3. Why is the embedding-model version part of the index configuration?
4. When should the model choice be re-evaluated, and how is a new model compared?
5. Why is a prototype model choice not automatically the production choice?

## Further Reading / Connections

- Arabic NLP 04 (Arabic embeddings) — the Arabic-specific quality problem.
- Embeddings 04 (quality evaluation) — the golden pairs that measure the choice.
- RAG System 06 (caching) — the model version in the cache key.
- Model Serving 01 (choosing a model) — the same axes applied to generative models.
