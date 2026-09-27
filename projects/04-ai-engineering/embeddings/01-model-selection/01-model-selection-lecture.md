# Embeddings 01: Model Selection

## 🎯 Topic Overview

The embedding model decides retrieval quality. The choice is a tradeoff
between dimensions, cost, speed, and language coverage. This lecture
covers the selection criteria and the multilingual requirement for Arabic.

## 📚 Learning Objectives

By the end of this lecture, you will be able to:

1. Compare embedding models on the key axes
2. Match the model to the corpus language
3. Choose for the deployment context
4. Keep the model consistent across the pipeline
5. Re-evaluate the choice when the corpus changes

---

## 1. The Axes

Embedding models differ on dimensions, cost, speed, and quality. Higher
dimensions capture more but cost more to store and search. The choice is a
tradeoff, not a preference. The roadmap's exit test: "the model is chosen
deliberately."

| Model | Dims | Cost | Quality |
|-------|------|------|---------|
| all-MiniLM-L6-v2 | 384 | Free | Fair |
| nomic-embed-text | 768 | Free | Good |
| text-embedding-3-small | 1536 | Low | Good |
| text-embedding-3-large | 3072 | High | Best |

## 2. Language Coverage

For Arabic retrieval, the model must handle Arabic. A monolingual English
model embeds Arabic poorly. The roadmap's exit test: "the model covers the
corpus language." Multilingual models are the default for Arabic corpora.

## 3. The Deployment Context

Prototyping uses a free local model; production balances cost and quality.
A cost-sensitive production uses a self-hosted model; a quality-first
production uses a paid API. The roadmap's exit test: "the model matches
the deployment context."

## 4. Consistency

The same model must embed the corpus and the queries. A model change
requires re-embedding the whole corpus — the old and new vectors are
incomparable. The roadmap's exit test: "the model is consistent across the
pipeline."

## 5. Re-Evaluation

The choice is re-evaluated when the corpus changes. A corpus that grows
Arabic content may need a better Arabic model. The re-evaluation is
measured on the golden set, not guessed.

## Common Mistakes

- A monolingual model for an Arabic corpus.
- Mixing models across the pipeline.
- Choosing dimensions without measuring quality.
- Never re-evaluating the choice.
- Cost ignored in the choice.

## Key Takeaways

1. The choice is a tradeoff across axes.
2. The model must cover the corpus language.
3. The deployment context decides the tier.
4. One model across the whole pipeline.
5. Re-evaluate when the corpus changes.