# Arabic NLP 04: Arabic Embeddings

## Topic Overview

Embeddings map Arabic text to vectors where meaning becomes distance. They are what let a
query with no words in common with a passage still find it, by matching on meaning rather
than on exact terms. That is the dense arm of retrieval, and it is the complement of BM25.

Arabic embeddings carry a specific trap. Multilingual models are trained mostly on English
and often tokenize Arabic poorly, splitting words into awkward subword fragments, so Arabic
semantic similarity is weaker than English for the same model. The fix is not "use any
embedding model"; it is choosing a model with verified Arabic performance and measuring it on
your own golden set before trusting it.

This lecture covers why model choice matters more for Arabic, the evaluation protocol that
makes the dense arm comparable to the lexical arm, normalization before embedding, and the
diagnosis of a dense miss.

## Learning Objectives

By the end of this lecture, you will be able to:

1. Explain why model choice matters more for Arabic than for English.
2. Evaluate an embedding model on Arabic retrieval with recall@k.
3. Embed normalized Arabic passages and queries consistently.
4. Build a dense retrieval arm over a vector store.
5. Diagnose a dense miss (tokenization, normalization, model).
6. Explain why dense and lexical arms fail in opposite directions.

## Prerequisites

- Arabic NLP 02 (normalization) and 03 (lexical retrieval and recall@k).
- Applied ML 01 (vectors and similarity) for cosine and normalization.

---

## 1. The Arabic Embedding Problem

### Tokenization quality

Embedding models tokenize text into subword units before encoding. A model with poor Arabic
coverage splits words into many small fragments, so a short Arabic sentence becomes a long,
noisy token sequence and the resulting vector captures less meaning. This is a property of
the model's tokenizer and training data, not of your pipeline.

### Training-data skew

Most multilingual models see far more English than Arabic in training. Their Arabic
representations are therefore less well separated, so Arabic paraphrases score lower
similarity than equivalent English paraphrases would. The effect is measurable: run the same
protocol on both languages and compare.

### The consequence

You cannot assume a well-known multilingual model handles Arabic well. The candidate set is
Arabic-specialized models and strong multilingual models with verified Arabic benchmarks, and
the golden set decides among them.

## 2. Evaluating on Arabic Retrieval

### The same protocol as the lexical arm

The dense arm is measured exactly as the lexical arm was: the same labeled set of
(query, relevant passages), the same recall@k. That is the point: the two arms must be
comparable before fusion, so the same yardstick is applied.

```python
# Embed each passage once; embed each query; rank by cosine; measure recall@k.
```

### What the numbers mean

A dense model that scores below the lexical arm on exact-term queries is not a failure; it
is the expected division of labor. The dense arm's value shows on paraphrase and synonym
queries, where the lexical arm scores near zero. Compare the arms per query type, not only
on the aggregate.

### The golden set must cover both

If the golden set is all exact-term lookups, the dense arm looks useless. If it is all
paraphrases, the lexical arm looks useless. Coverage (AI Evaluation 01) is what makes the
comparison honest.

## 3. Normalization Before Embedding

### Embed the searchable text

Embed the normalized searchable text, not the raw display text. Diacritics, hamza variants,
and tatweel would split the embedding space for no semantic benefit, so the same
normalization that feeds the lexical index feeds the embedder.

### Consistency, not perfection

Whatever normalization the embeddings use, the query must use the same. The failure is not
choosing a "wrong" normalization; it is choosing two different ones, so the query and the
passage land in different regions of the space.

### The two-text link

The embedding is computed from `searchable`; the citation still comes from `original`. The
two-text discipline from Topic 01 carries forward unchanged.

## 4. The Dense Arm

### The pipeline

```python
# passage -> embedding -> vector store (Qdrant, FAISS)
# query  -> embedding -> cosine (or dot on normalized vectors) -> top-k
```

### What it retrieves

The dense arm retrieves by meaning. A query that shares no tokens with the passage still
matches if the meaning aligns. This catches paraphrase, synonym, and cross-vocabulary
queries that the lexical arm misses.

### Its failure mode

The dense arm blurs exact terms. A query for a specific name or an error code may return
semantically similar but wrong passages, because embeddings compress rare strings into
meaning-space. This is the opposite of the lexical arm's failure, which is exactly why the
two are fused (Topic 05).

## 5. Diagnosing Dense Misses

### Three suspects

A dense miss has three suspects, plus the model:

- **Normalization:** the query and the passage were normalized differently before embedding.
- **Tokenization:** the model splinters Arabic so badly that meaning is lost.
- **Model choice:** the model's Arabic representations are weak overall.
- **Index:** the passage was not indexed, or the ANN parameters pruned it (Topic 06).

### The method

Take the missed query and its known relevant passage. Embed both. If their cosine is low,
the problem is upstream (normalization or tokenization/model). If their cosine is high but
the passage did not rank, the problem is in the index or the ranking, not the embedding.

### The expected misses

Dense misses on exact-term queries are expected and are the lexical arm's job. Do not
"fix" the dense arm for a failure the lexical arm is designed to cover.

## 6. Choosing the Model

### The candidates

Arabic-specialized sentence-transformer models, and strong multilingual models with
published Arabic retrieval benchmarks, form the shortlist. Prefer models whose training data
and evaluation explicitly cover Arabic.

### The decision

Run the shortlist on the golden set, compare recall@k per query type, and record the choice
as an ADR (the same discipline as Model Serving 01). The model is a long-lived decision, and
a future swap should be a measured change.

### The cost axis

Embedding cost matters at corpus scale: embedding a large Athar corpus once is a one-time
cost, but re-embedding after a model change is repeated. Record the model version with the
index so a change is deliberate.

## Real-World Application

- Choosing an Arabic-capable embedding model for the Athar index after measuring it against
  a lexical baseline.
- Embedding normalized passage text so a diacritized query matches an undiacritized passage.
- Diagnosing a dense miss by comparing the query-passage cosine before blaming the index.
- Recording the embedding model version with the index so re-embedding is a tracked change.

## Common Mistakes

1. **Assuming a multilingual model handles Arabic well.** Measure it.
2. **Embedding raw display text.** Diacritics split the space for no benefit.
3. **Comparing arms on different labeled sets.** The comparison becomes meaningless.
4. **Judging the dense arm by exact-term queries.** That is the lexical arm's job.
5. **Normalizing the query differently from the passages.** Silent, systematic misses.
6. **Changing the embedding model without re-embedding the corpus.** Query and index live in
   different spaces.

## Key Takeaways

1. Arabic embedding quality is a measured choice; tokenization and training-data skew make
   generic models weaker on Arabic.
2. Evaluate the dense arm with the same labeled set and recall@k as the lexical arm.
3. Embed the normalized searchable text, with the same normalization for query and passages.
4. The dense arm catches paraphrase and fails on exact terms; the lexical arm does the
   reverse.
5. Diagnose a dense miss by checking the query-passage cosine before blaming the index.

## Self-Check Questions

1. Why does Arabic embedding quality depend on the model more than English does?
2. Why must the dense arm use the same labeled set as the lexical arm?
3. What should you embed: the display text or the searchable text, and why?
4. A dense miss occurs on a query that shares no tokens with the passage. Is that a bug?
5. How do you diagnose whether a dense miss is an embedding problem or an index problem?

## Further Reading / Connections

- Arabic NLP 02 (normalization) — the text the embedder consumes.
- Arabic NLP 05 (hybrid search) — fusing the dense and lexical arms.
- Arabic NLP 06 (ANN search) — the index that serves the dense arm at scale.
- Applied ML 01 (vectors and similarity) — cosine and normalization.
