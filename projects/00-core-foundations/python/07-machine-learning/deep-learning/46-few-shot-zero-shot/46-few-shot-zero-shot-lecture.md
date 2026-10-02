# 07-machine-learning — 46: Few-Shot and Zero-Shot Learning — Generalizing From Almost Nothing

Companion exercise: `46-few-shot-zero-shot.py`

---

## Topic Overview

Classical supervised learning needs thousands of labeled examples per class.
Zero-shot learning needs *none*: it classifies by matching an input's embedding
against a textual description of each class. Few-shot learning needs only a
handful — it classifies by comparing to a small set of labeled examples. Both
are possible because a pretrained model already embeds meaning into a shared
space, so "similarity" can substitute for "training."

This is the mechanism behind CLIP-style image-text matching, prompt-based
classification with LLMs, and the ability to add a new category to a deployed
system without retraining. The core primitive is *similarity in embedding
space*: zero-shot compares to class descriptions, few-shot compares to a
prototype (the mean of a few support examples), and both are a distance
computation, not a training run.

The topic covers the shared-space premise, zero-shot classification by
description matching, few-shot classification by prototypical networks, the
in-context few-shot of LLMs, and the honest limits — when similarity is not
enough and you still need real fine-tuning.

## Learning Objectives

By the end of this lecture, you will be able to:

1. Explain the shared embedding space that makes few/zero-shot possible.
2. Classify zero-shot by matching against class descriptions.
3. Build a prototypical few-shot classifier (mean of support examples).
4. Distinguish in-context learning from embedding similarity.
5. State when few/zero-shot fails and fine-tuning is required.
6. Compute cosine similarity and nearest-prototype classification.
7. Explain why new classes need no retraining in these regimes.

## Prerequisites

| Need | Where |
|---|---|
| Embeddings | `06-embeddings` (embeddings module) |
| Transfer learning | `39-transfer-learning.py` |
| Cosine similarity | vector math from `36-pytorch-tensors.py` |

## 1. The Shared-Space Premise

### Why similarity works

Few/zero-shot works because a pretrained model maps inputs *and* class concepts
into one space where related things are close. An image of a cat and the text
"a cat" land near each other; so classification becomes nearest-neighbor search
rather than a trained decision boundary.

### The enabling model

This is what CLIP (contrastive image-text) and embedding models provide: a space
where *meaning* is geometry. Once that space exists, a new class is just a new
point (or prototype) in it — no gradient descent required.

## 2. Zero-Shot Classification

### Match to a description

Zero-shot embeds the query and each class name (or description), and predicts
the class whose embedding is closest:

```python
def zero_shot(query, class_embeds):
    sims = {c: cosine(query, e) for c, e in class_embeds.items()}
    return max(sims, key=sims.get)
```

### The "zero" in zero-shot

There are zero *labeled examples* of the target classes — only their names or
descriptions. The model relies entirely on the alignment between input space
and text space learned during pretraining.

## 3. Few-Shot Classification

### Prototypical networks

Few-shot uses a small *support set* — k labeled examples per class — and builds a
prototype as their mean embedding. A query is classified by its nearest
prototype:

```python
def prototype(support):
    return support.mean(dim=0)


def few_shot(query, prototypes):
    return min(prototypes, key=lambda c: -cosine(query, prototypes[c]))
```

### Why the mean

The mean of a few examples averages out their individual noise, giving a robust
class center from very few samples. This is the "prototype" idea from
Prototypical Networks, and it is the workhorse of few-shot learning.

## 4. In-Context Learning (LLM few-shot)

### A different mechanism

LLMs do few-shot *in context*: you put a few examples in the prompt, and the
model infers the pattern by attention, with no weight update at all. This is
few-shot as *conditioning*, distinct from the embedding-prototype view.

### Why it is powerful but different

In-context few-shot needs no gradient step and generalizes across tasks, but it
burns context length and is not always as precise as a fine-tuned model. It is
the LLM-era face of the same "generalize from a few examples" idea.

## 5. When Similarity Is Not Enough

### The honest limits

Few/zero-shot fails when the pretrained space does not align with the target
task — a niche domain, a vocabulary the model never saw, or a fine-grained
distinction the embedding does not capture. Then a handful of examples is not
enough, and you fall back to fine-tuning (`39-transfer-learning`).

### The decision rule

Start zero-shot (free). If insufficient, try few-shot (cheap). If still
insufficient, fine-tune (the real cost). The ladder matches cost to difficulty.

## 6. Common Mistakes to Avoid

### Mistake 1: Expecting zero-shot on an unseen domain
```
# WRONG — zero-shot medical coding with a model never trained on medical text
# CORRECT — check the space aligns with the task before trusting similarity
```

### Mistake 2: Prototype built from one noisy example
```
# WRONG — a single mislabeled support example defines the class center
# CORRECT — more support examples (k >= 5) and clean labels
```

### Mistake 3: Forgetting normalization before cosine
```
# WRONG — cosine on unnormalized embeddings is just scaled dot product noise
# CORRECT — L2-normalize embeddings before computing cosine similarity
```

### Mistake 4: Confusing in-context few-shot with fine-tuning
```
# WRONG — claiming the model "learned" the task when weights were untouched
# CORRECT — in-context is conditioning; fine-tuning changes weights
```

### Mistake 5: No held-out evaluation
```
# WRONG — picking the best class description by testing on the eval set
# CORRECT — fix descriptions/prototypes on a dev split, measure once on test
```

## 7. Best Practices

1. L2-normalize embeddings before any cosine comparison.
2. Start zero-shot; escalate to few-shot, then fine-tune, as the task demands.
3. Build prototypes from several clean support examples, not one.
4. Choose class *descriptions*, not just names, for better zero-shot alignment.
5. Measure on a held-out set; don't tune descriptions against the test set.
6. Treat in-context few-shot as conditioning, and say so in your docs.
7. Watch the domain gap — similarity only works inside the pretrained space.
8. Record the embedding model and version for reproducibility.

## 8. Complexity and Cost

| Operation | Time | Space | Notes |
|---|---|---|---|
| Zero-shot classify | one forward pass + k cosines | embeddings | Free of training |
| Few-shot prototype | k forward passes + mean | support set | Seconds |
| In-context few-shot | one forward pass, long prompt | context window | Context-length cost |
| Fine-tuning | minutes-hours GPU | model | The fallback |

## 9. AI Engineering Relevance

**Where this shows up:** adding a category to a live system without retraining,
CLIP-style multimodal retrieval, and prompt-based classification. On this
workstation, embedding models run cheaply on the RTX 5000, so zero/few-shot is
the first thing to try before spending GPU hours on fine-tuning.

| Concept here | Used for |
|---|---|
| Cosine in embedding space | Zero-shot classification and retrieval |
| Prototype | Few-shot with k examples |
| In-context learning | LLM few-shot without weight updates |
| Cost ladder | zero-shot -> few-shot -> fine-tune |

**Scale note:** the economics are the point — similarity is a forward pass and a
few dot products, orders of magnitude cheaper than training. Use it as the first
rung; reserve fine-tuning for where it demonstrably fails.

## 10. Summary

| Concept | Description |
|---|---|
| Shared space | Meaning as geometry from a pretrained model |
| Zero-shot | Classify by matching class descriptions |
| Few-shot | Classify by nearest prototype (mean of support) |
| In-context | LLM few-shot via the prompt, no weight change |
| Cost ladder | zero-shot -> few-shot -> fine-tune |

## Quick Reference

| Task | Idiom |
|---|---|
| Normalize | `emb = F.normalize(emb, dim=-1)` |
| Cosine | `sim = (a * b).sum(-1)` (normalized) |
| Prototype | `support.mean(dim=0)` |
| Zero-shot | `argmax over cosine(query, class_embed)` |

## Next Steps

Next: **[47 — Self-Supervised Learning](47-self-supervised-learning-lecture.md)** — learning without labels at all.

Continues in: **[39 — Transfer Learning](39-transfer-learning-lecture.md)** — the fine-tuning rung of the ladder.

Official docs: <https://pytorch.org/docs/stable/nn.functional.html#cosine-similarity>
