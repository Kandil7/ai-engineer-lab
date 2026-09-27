# Arabic NLP 04: Arabic Embeddings

## 🎯 Topic Overview

Embeddings map Arabic text to vectors where meaning is distance. But Arabic
embeddings carry a specific trap: multilingual models often tokenize Arabic
poorly, and generic models trained mostly on English underperform on Arabic
semantics. This lecture covers how to choose an Arabic-capable embedding
model, how to evaluate it on Arabic retrieval, and how to build the dense
arm that hybrid search fuses with BM25.

## 📚 Learning Objectives

By the end of this lecture, you will be able to:

1. Explain why model choice matters more for Arabic than for English
2. Evaluate embedding models on Arabic retrieval with recall@k
3. Embed Arabic passages and queries with proper normalization
4. Build a dense retrieval arm over a vector store
5. Diagnose dense-arm misses (tokenization, normalization, model)

---

## 1. The Arabic Embedding Problem

Multilingual embedding models tokenize Arabic into subword units that often
split words awkwardly, and their training data skews heavily toward English.
The result: Arabic semantic similarity is weaker than English similarity for
the same model. The fix is not "use any embedding model" — it is choosing
and measuring. Arabic-specialized or strong multilingual models (e.g.,
Arabic-specific Sentence Transformers, or multilingual models with verified
Arabic benchmarks) are the candidates; the golden set decides.

## 2. Evaluating on Arabic Retrieval

```python
# The protocol: same labeled set as the lexical arm, same recall@k.
# Embed each passage once; embed each query; rank by cosine; measure.
```

The evaluation is identical to topic 03's — which is the point. The same
labeled query-to-passage set that measured BM25 measures the dense arm, so
the two arms are comparable before fusion. A model that scores below the
lexical arm on exact-term queries is not a failure; it is the expected
division of labor.

## 3. Normalization Before Embedding

Embed the normalized searchable text, not the raw display text — the same
discipline as the lexical index. Diacritics and hamza variants would split
the embedding space for no retrieval benefit. Consistency matters more than
perfection: whatever normalization the index uses, the embeddings use the
same.

## 4. The Dense Arm

```python
# passage -> embedding -> vector store (Qdrant, FAISS)
# query -> embedding -> cosine search -> top-k
```

The dense arm retrieves by meaning: a query with no shared tokens with the
passage still matches if the meaning aligns. This is the arm that catches
paraphrase and synonym queries the lexical arm misses. Its failure mode is
the opposite: exact terms and names get blurred.

## 5. Diagnosing Dense Misses

A dense miss has three suspects: tokenization (the model splits Arabic
poorly), normalization (query and passage embedded differently), and model
choice (the model's Arabic is weak). The diagnosis loop from topic 03
applies with the model added as a stage. When the dense arm misses an
exact-term query, that is expected — the lexical arm covers it.

## Common Mistakes

- Assuming a multilingual model handles Arabic well without measuring.
- Embedding raw display text instead of normalized searchable text.
- Comparing arms on different labeled sets.
- Judging the dense arm by exact-term queries alone.

## Key Takeaways

1. Arabic embedding quality is a measured choice, not an assumption.
2. Same labeled set, same recall@k, both arms comparable.
3. Embed the normalized searchable text.
4. Dense and lexical fail in opposite directions — that is the point.