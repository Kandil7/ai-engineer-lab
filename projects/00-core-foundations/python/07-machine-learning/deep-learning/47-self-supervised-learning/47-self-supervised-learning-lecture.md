# 07-machine-learning — 47: Self-Supervised Learning — Labels From the Data Itself

Companion exercise: `47-self-supervised-learning.py`

---

## Topic Overview

Supervised learning is bottlenecked by labels; self-supervised learning
(SSL)
removes that bottleneck by *inventing* the labels from the data itself.
The
model learns a pretext task — predict the next token, mask and
reconstruct a
word, or match two views of the same image — and in doing so learns
representations that transfer to real tasks. This is how BERT, GPT, and
CLIP
learned to embed language and vision without a single human label.

The two families are contrastive and generative. **Contrastive**
learning pulls
different views of the same example together and pushes different
examples
apart, learning invariances. **Generative** (masked) learning hides part
of the
input and asks the model to reconstruct it, learning structure. Both
produce a
pretrained encoder whose features are then reused with little labeled
data —
the engine behind `39-transfer-learning`.

The topic covers the pretext-task premise, contrastive (SimCLR/InfoNCE)
and
masked (BERT-style) objectives, and why SSL-pretrained encoders are the
default
starting point for downstream fine-tuning. The economics are the
through-line:
unlabeled data is abundant and free, so SSL moves the learning cost onto
data
that costs nothing.

## Learning Objectives

By the end of this lecture, you will be able to:

1. Explain how SSL invents labels from the data itself.
2. Distinguish contrastive from generative (masked) self-supervision.
3. Describe the InfoNCE loss and what positive/negative pairs mean.
4. Explain the masked-language-modeling objective.
5. State why SSL pretraining beats training from scratch on small labeled data.
6. Connect SSL to transfer learning and fine-tuning.
7. Identify when SSL is the right first step.
8. Explain representation collapse and how to avoid it.

## Prerequisites

| Need | Where |
|---|---|
| Transfer learning | `39-transfer-learning.py` |
| Data augmentation | `45-data-augmentation.py` |
| Neural network basics | `38-neural-network-basics.py` |

## 1. The Pretext-Task Premise

### Labels without a labeler

SSL defines a *pretext task* whose answer is already in the data. "What
is the
masked word?" or "Are these two views the same example?" require no
annotation —
the data supplies the answer. Training on that task forces the model to
learn
structure that a supervised task can later reuse.

### The real-world analogy

A child learns language by hearing it and predicting what comes next —
no one
labels each sentence. The task (predict the next word) is
self-generated, and
the byproduct is a working understanding of the language. SSL does the
same for
models: the pretext task is the engine, the learned representation is
the fuel.

### Why it transfers

A model that can reconstruct a masked word knows syntax and semantics; a
model
that can match two views of an image knows visual invariance. Those
learned
features — not the pretext task itself — are the product. The pretext
task is
discarded; the encoder is kept.

## 2. Contrastive Learning

### Positive and negative pairs

Contrastive learning treats two augmented views of the *same* example as
a
positive pair (must be close), and views of *different* examples as
negative
pairs (must be far). The InfoNCE loss implements this as a softmax over
similarities:

```text
loss = -log( exp(sim(z_i, z_j)/tau) / sum_k exp(sim(z_i, z_k)/tau) )
```

### What it learns

By pulling positives together and pushing negatives apart, the encoder
learns the
invariances that define "the same thing" — the same object under
different
lighting, the same sentence paraphrased. SimCLR and CLIP are the
canonical
examples; CLIP adds text as the second view, which is the shared space
behind
`46-few-shot-zero-shot`.

## 3. Masked (Generative) Learning

### Hide and reconstruct

Masked modeling hides part of the input and asks the model to predict it
from
context. BERT masks 15% of tokens; the model predicts the masked words.
The task
is generative — reconstruct the hidden part — but the product is the
encoder.

### What it learns

To predict a masked word, the model must learn bidirectional context and
deep
semantics. BERT's success on downstream tasks proved that this single
pretext
task yields transferable representations. GPT's next-token prediction is
the
autoregressive cousin — predict the future, not the middle.

## 4. SSL Pretraining, Then Fine-Tuning

### The production flow

The real workflow is two-stage: SSL-pretrain on a large unlabeled corpus
(cheap,
no labels), then fine-tune on a small labeled task
(`39-transfer-learning`).
The SSL step buys a general encoder; the fine-tune step specializes it
cheaply.

### The economic logic

Unlabeled data is abundant and free; labels are scarce and expensive.
SSL moves
most of the learning cost onto the free data, leaving a small labeled
budget for
the actual task. That is the economic argument behind BERT, GPT, and
every
foundation model.

## 5. Representation Collapse

### The failure mode

Contrastive learning has a degenerate solution: map everything to the
same
point. Then every similarity is 1, the loss is trivially zero, and the
representation is useless. This is *collapse*, and it is the central
challenge of
contrastive methods.

### How to avoid it

The standard guards are enough negative pairs (so the model cannot
satisfy the
objective by collapsing), a temperature that keeps the distribution
sharp, and
normalization that keeps vectors on the hypersphere. Architectures like
SimCLR's momentum encoder and BYOL avoid collapse by design.

## 6. Why Not Always SSL

### The cost and the ceiling

SSL pretraining is itself expensive — pretraining a large model on a big
corpus
is a data-center-scale job. For a small task, you rarely pretrain from
scratch;
you download a pretrained encoder. SSL is the *idea* you inherit from,
not a step
you rerun every project.

### The honest role

For an application engineer, SSL matters as the origin story of every
pretrained
model you fine-tune, and as the technique to reach for when you have
unlabeled
domain data and no labels — a real case for specialized corpora, where
continued
pretraining on in-domain text can beat a generic encoder.

## Real-World Application

- **Foundation models** — GPT (next-token), BERT (masked), CLIP (contrastive).
- **Continued pretraining** — adapting a general encoder to a niche domain (e.g.
  a specialized Arabic or Islamic corpus) on unlabeled text.
- **Vision pretraining** — SimCLR/MoCo-style contrastive learning for image
  encoders before downstream fine-tuning.
- **The Athar case** — SSL pretraining on unlabeled Arabic text to build an
  encoder that transfers to passage classification.

## Common Mistakes to Avoid

### Mistake 1: Pretraining from scratch for a small task
```
# WRONG — SSL-pretrain a BERT on your 1 GB corpus when a pretrained one exists
# CORRECT — download a pretrained encoder and fine-tune (39-transfer-learning)
```

### Mistake 2: Collapsing contrastive representations
```
# WRONG — all embeddings drift to the same point (a degenerate InfoNCE solution)
# CORRECT — enough negatives, a temperature, and normalization to avoid collapse
```

### Mistake 3: Leaking the answer into the mask
```
# WRONG — the masked token still present via a bug, so the task is trivial
# CORRECT — actually remove the masked content before predicting
```

### Mistake 4: Evaluating the pretext task instead of the downstream task
```
# WRONG — reporting mask accuracy when what matters is the fine-tuned metric
# CORRECT — the product is the encoder; measure the real task
```

### Mistake 5: Ignoring the domain gap
```
# WRONG — a general SSL encoder for a highly specialized corpus, no adaptation
# CORRECT — consider continued pretraining on in-domain unlabeled data
```

### Mistake 6: Too few negative pairs
```
# WRONG — a batch of 2 makes the contrastive objective nearly vacuous
# CORRECT — a large batch (or a memory bank) for meaningful negatives
```

## Best Practices

1. Inherit a pretrained encoder rather than pretraining from scratch.
2. Use contrastive learning for invariance; masked modeling for structure.
3. Keep a healthy number of negative pairs to avoid collapse.
4. Normalize embeddings and use a temperature in InfoNCE.
5. Fine-tune the SSL encoder on the downstream task with a small LR.
6. Consider continued pretraining on in-domain unlabeled data.
7. Record the pretext task, corpus, and checkpoint for reproducibility.
8. Measure the downstream task, never the pretext task, as success.

## Complexity and Cost

| Operation | Time | Space | Notes |
|---|---|---|---|
| Contrastive step | batch of two views | 2x batch | More negatives help |
| Masked prediction | batch forward | masked batch | Pretraining-scale |
| SSL pretraining | days-weeks | data-center | Inherited, not rerun |
| Fine-tuning | minutes-hours | small labeled set | Your actual cost |

## AI Engineering Relevance

**Where this shows up:** every foundation model you serve is an SSL product —
GPT (next-token), BERT (masked), CLIP (contrastive). On this workstation
you
fine-tune these, not pretrain them; but understanding the pretext task
is what
tells you *why* a pretrained encoder generalizes and when to continue
pretraining
on in-domain data.

| Concept here | Used for |
|---|---|
| Contrastive | Invariance-focused encoders (CLIP, SimCLR) |
| Masked | Structure-focused encoders (BERT, GPT) |
| Pretrain-then-fine-tune | The production default |
| In-domain continued pretraining | Adapting to a niche corpus |

**Scale note:** SSL is where the "pretrain big, fine-tune small" economics come
from. You inherit the big pretraining; your budget is the fine-tune,
which is
why the RTX 5000's 16 GB is usually enough.

## Key Takeaways

1. SSL invents labels from the data itself via a pretext task.
2. Contrastive pulls views together and pushes others apart; masked reconstructs the hidden part.
3. InfoNCE is a softmax over similarities with positive/negative pairs.
4. Representation collapse is the central contrastive failure, avoided with negatives + temperature + normalization.
5. The production flow is pretrain-then-fine-tune, and you inherit the pretraining.
6. The product is the encoder, so measure the downstream task, not the pretext task.

## Self-Check Questions

1. What is a pretext task, and why does its answer require no labeler?
2. How do contrastive and masked (generative) SSL differ in what they learn?
3. What are positive and negative pairs, and what does InfoNCE do with them?
4. What is representation collapse, and what three guards prevent it?
5. Why do you inherit an SSL encoder rather than pretraining it yourself?
6. Why should you measure the downstream task, not the pretext task?

## Summary

| Concept | Description |
|---|---|
| Pretext task | Labels invented from the data itself |
| Contrastive | Pull views of the same example together |
| Masked | Hide and reconstruct part of the input |
| InfoNCE | The contrastive loss over positive/negative pairs |
| Pretrain-then-fine-tune | The production default |

## Quick Reference

| Task | Idiom |
|---|---|
| InfoNCE | `-log(exp(sim/τ)/sum exp(sim/τ))` |
| Positive pair | two views of the same example |
| Negative pair | views of different examples |
| Masked objective | predict the hidden token from context |

## Further Reading / Connections

- `39-transfer-learning-lecture.md` — the fine-tune half of the pair.
- `45-data-augmentation-lecture.md` — the "views" used in contrastive learning.
- `46-few-shot-zero-shot-lecture.md` — the shared space contrastive learning builds.
- Chen et al., "A Simple Framework for Contrastive Learning" (SimCLR).

## Next Steps

Next: **[48 — Hyperband and
BOHB](../advanced/48-hyperband-bohb-lecture.md)** — multi-fidelity
tuning.

