# 07-machine-learning — 46: Few-Shot and Zero-Shot Learning — Generalizing From Almost Nothing

Companion exercise: `46-few-shot-zero-shot.py`

---

## Topic Overview

Classical supervised learning needs thousands of labeled examples per
class.
Zero-shot learning needs *none*: it classifies by matching an input's
embedding
against a textual description of each class. Few-shot learning needs
only a
handful — it classifies by comparing to a small set of labeled examples.
Both
are possible because a pretrained model already embeds meaning into a
shared
space, so "similarity" can substitute for "training."

This is the mechanism behind CLIP-style image-text matching,
prompt-based
classification with LLMs, and the ability to add a new category to a
deployed
system without retraining. The core primitive is *similarity in
embedding
space*: zero-shot compares to class descriptions, few-shot compares to a
prototype (the mean of a few support examples), and both are a distance
computation, not a training run.

The topic covers the shared-space premise, zero-shot classification by
description matching, few-shot classification by prototypical networks,
the
in-context few-shot of LLMs, and the honest limits — when similarity is
not
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
8. Describe the cost ladder: zero-shot -> few-shot -> fine-tune.

## Prerequisites

| Need | Where |
|---|---|
| Embeddings | `06-embeddings` (embeddings module) |
| Transfer learning | `39-transfer-learning.py` |
| Cosine similarity | vector math from `36-pytorch-tensors.py` |

## 1. The Shared-Space Premise

### Why similarity works

Few/zero-shot works because a pretrained model maps inputs *and* class
concepts
into one space where related things are close. An image of a cat and the
text
"a cat" land near each other; so classification becomes nearest-neighbor
search
rather than a trained decision boundary.

### The real-world analogy

Think of a dictionary plus a shared language. You know what "cat" means
in
language and you know what a cat looks like in the world; the shared
space is
the alignment that lets you match the word to the image. Once that
alignment
exists, a new word (a new class) is just another entry — no new training
needed.

### The enabling model

This is what CLIP (contrastive image-text) and embedding models provide:
a space
where *meaning* is geometry. Once that space exists, a new class is just
a new
point (or prototype) in it — no gradient descent required.

### When it works, when it fails

Similarity works when the pretrained space actually covers the task's
domain —
the classes are things the model's text/vision encoder has seen. It
fails when
the domain is niche or the vocabulary is out-of-distribution, because
then the
embeddings carry no signal about the distinction you need.

## 2. Zero-Shot Classification

### Match to a description

Zero-shot embeds the query and each class name (or description), and
predicts
the class whose embedding is closest:

```python
def zero_shot(query, class_embeds):
    sims = {c: cosine(query, e) for c, e in class_embeds.items()}
    return max(sims, key=lambda c: sims[c])
```

### The "zero" in zero-shot

There are zero *labeled examples* of the target classes — only their
names or
descriptions. The model relies entirely on the alignment between input
space
and text space learned during pretraining.

### Descriptions beat names

A class *name* can be ambiguous ("crane" — bird or machine); a short
description
("a crane, the bird") disambiguates. Good zero-shot performance depends
on good
prompts, which is why prompt design is a first-class skill in this
regime.

## 3. Few-Shot Classification

### Prototypical networks

Few-shot uses a small *support set* — k labeled examples per class — and
builds a
prototype as their mean embedding. A query is classified by its nearest
prototype:

```python
def prototype(support):
    return support.mean(dim=0)


def few_shot(query, prototypes):
    return min(prototypes, key=lambda c: -cosine(query, prototypes[c]))
```

### Why the mean

The mean of a few examples averages out their individual noise, giving a
robust
class center from very few samples. This is the "prototype" idea from
Prototypical Networks, and it is the workhorse of few-shot learning. A
single
noisy example is a bad prototype; several clean ones are a good one.

## 4. In-Context Learning (LLM few-shot)

### A different mechanism

LLMs do few-shot *in context*: you put a few examples in the prompt, and
the
model infers the pattern by attention, with no weight update at all.
This is
few-shot as *conditioning*, distinct from the embedding-prototype view.

### Why it is powerful but different

In-context few-shot needs no gradient step and generalizes across tasks,
but it
burns context length and is not always as precise as a fine-tuned model.
It is
the LLM-era face of the same "generalize from a few examples" idea, and
the
distinction (no weight change) is a common source of confusion.

## 5. When Similarity Is Not Enough

### The honest limits

Few/zero-shot fails when the pretrained space does not align with the
target
task — a niche domain, a vocabulary the model never saw, or a
fine-grained
distinction the embedding does not capture. Then a handful of examples
is not
enough, and you fall back to fine-tuning (`39-transfer-learning`).

### The decision rule

Start zero-shot (free). If insufficient, try few-shot (cheap). If still
insufficient, fine-tune (the real cost). The ladder matches cost to
difficulty,
and each rung is tried only after the cheaper one demonstrably fails.

## 6. Evaluation Discipline

### The description-tuning trap

It is tempting to tune the class descriptions until the eval score
rises. That
is leakage — the descriptions are a hyperparameter, and tuning them
against the
test set inflates the metric. The discipline is the same as `33`: fix
the
prompts/prototypes on a dev split, measure once on test.

### The metric

For zero/few-shot, the metric is standard classification accuracy (or a
ranking
metric like top-k) on a held-out set — but the *held-out* guarantee only
holds
if you did not tune against it.

## 7. CLIP and Multimodal Alignment

### The model that made zero-shot real

CLIP trains a contrastive objective over (image, text) pairs: the image
encoder
and the text encoder are pulled together for matching pairs and pushed
apart for
mismatched ones. The result is a *joint* space where an image and its
caption
are neighbors. This is `47-self-supervised-learning`'s contrastive idea
applied
across modalities — and it is what makes zero-shot image classification
by text
description work at all.

### Why it generalizes

Because CLIP learned from arbitrary captions, not a fixed class list, it
can be
prompted with any text at test time. "A photo of a cat" is a point in
the space,
and the nearest image wins. New classes are new prompts, which is the
whole
zero-shot story compressed into one model.

### The engineering lesson

The valuable artifact is the *alignment*, not the classifier. Once you
have an
aligned multimodal space, every downstream task — retrieval,
classification,
search — becomes a similarity query. That is why CLIP-style models are
foundational, not task-specific.

## 8. Prompt Design for Zero-Shot

### Prompts are the tuning knob

Zero-shot accuracy swings wildly with the prompt. "A photo of a {class}"
beats
the bare class name for CLIP; a well-crafted instruction beats a vague
one for
LLMs. Prompt design is the zero-shot analogue of hyperparameter tuning —
the
model is fixed, but the input that conditions it is a search space.

### The evaluation discipline

Because prompts are a search space, tuning them against the test set is
leakage
(`6`). The correct loop is: design prompts on a dev split, freeze them,
measure
once on test. This is the same discipline as `33`'s "tune inside CV,"
applied to
text instead of hyperparameters.

### The practical default

Start with a simple template, evaluate, and iterate only if the task
warrants
it. The marginal gain from prompt engineering is real but bounded, and
it is
often cheaper to move one rung up the cost ladder (few-shot or
fine-tune) than
to squeeze the last point out of a zero-shot prompt.

## 9. Evaluation Metrics for Few/Zero-Shot

### Accuracy is not enough

Top-1 accuracy hides the structure of the errors. In few/zero-shot, two
extra
metrics matter: **top-k accuracy** (is the right class in the top k
nearest
prototypes?) and the **margin** (how much closer is the chosen class
than the
runner-up?). A high-accuracy model with tiny margins is fragile; a
slightly
lower-accuracy model with large margins is robust.

### Why margins matter

Similarity-based classifiers have no calibrated probability — the cosine
score
is a ranking, not a confidence. A large margin between the top two
classes says
"the decision was easy"; a small margin says "this example is
ambiguous," which
is exactly the case a human should review. Reporting margins turns a
classifier
into a triage tool.

### The class-balance check

Few-shot support sets are tiny, so a single mislabeled example can
dominate a
class's prototype. Always inspect per-class accuracy, not just the
average — an
80% overall score can hide a class at 20% because its one support example was
wrong.

### The held-out discipline

Every metric here is only honest if measured on a set you did not tune
the
prompts or prototypes against. The metrics are easy; the discipline is
what makes
them mean something.

## 10. Failure Analysis for Similarity Classifiers

### The three failure modes

When a similarity classifier fails, it is almost always one of three
things: the
embedding space does not separate the classes (a domain gap), the
prototype is
bad (too few or mislabeled support examples), or the class descriptions
are
ambiguous (poor prompts). The fix differs for each, so the first job is
diagnosis.

### Diagnosing the domain gap

If the failure is uniform across classes and the confusions are
semantically
unrelated, the space likely does not cover the domain — a candidate for
fine-tuning. If the failures cluster around specific class pairs, the
space
*does* separate most things and the problem is local, which suggests better
prototypes or descriptions.

### The confusions matrix

For few-shot, plot the confusion matrix over classes. A block of
confusions
between two classes says their prototypes are too close; a scattered
matrix says
the space is weak. The matrix is the fastest way to tell "one bad class"
from
"the whole space is wrong."

### The escalation trigger

The diagnosis decides the ladder rung: local failures → better prompts
or more
support examples; global failures → fine-tune (`39`). Failure analysis
is what
turns "it does not work" into a specific, cheap next step.

## Real-World Application

- **Adding a category without retraining** — a live classifier gains a new class
  as a new embedding.
- **CLIP-style multimodal retrieval** — match images to free-text queries.
- **Prompt-based classification** — LLMs classifying by a few examples in the prompt.
- **Low-resource languages** — few-shot where labeled data is expensive (e.g.
  Arabic dialects).
- **The Athar/DevMate case** — zero-shot topic labeling of passages via their
  embeddings against topic descriptions.

## Common Mistakes to Avoid

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

### Mistake 6: Using class names instead of descriptions
```
# WRONG — a bare ambiguous name ("crane") when a description disambiguates
# CORRECT — write descriptions that pin down the intended meaning
```

## Best Practices

1. L2-normalize embeddings before any cosine comparison.
2. Start zero-shot; escalate to few-shot, then fine-tune, as the task demands.
3. Build prototypes from several clean support examples, not one.
4. Choose class *descriptions*, not just names, for better zero-shot alignment.
5. Measure on a held-out set; don't tune descriptions against the test set.
6. Treat in-context few-shot as conditioning, and say so in your docs.
7. Watch the domain gap — similarity only works inside the pretrained space.
8. Record the embedding model and version for reproducibility.

## Complexity and Cost

| Operation | Time | Space | Notes |
|---|---|---|---|
| Zero-shot classify | one forward pass + k cosines | embeddings | Free of training |
| Few-shot prototype | k forward passes + mean | support set | Seconds |
| In-context few-shot | one forward pass, long prompt | context window | Context-length cost |
| Fine-tuning | minutes-hours GPU | model | The fallback |

## AI Engineering Relevance

**Where this shows up:** adding a category to a live system without retraining,
CLIP-style multimodal retrieval, and prompt-based classification. On
this
workstation, embedding models run cheaply on the RTX 5000, so
zero/few-shot is
the first thing to try before spending GPU hours on fine-tuning.

| Concept here | Used for |
|---|---|
| Cosine in embedding space | Zero-shot classification and retrieval |
| Prototype | Few-shot with k examples |
| In-context learning | LLM few-shot without weight updates |
| Cost ladder | zero-shot -> few-shot -> fine-tune |

**Scale note:** the economics are the point — similarity is a forward pass and a
few dot products, orders of magnitude cheaper than training. Use it as
the first
rung; reserve fine-tuning for where it demonstrably fails.

## Key Takeaways

1. A shared embedding space turns classification into nearest-neighbor search.
2. Zero-shot matches class descriptions; few-shot matches support prototypes.
3. In-context few-shot conditions an LLM without changing its weights.
4. The ladder is zero-shot -> few-shot -> fine-tune, each tried in order.
5. Similarity only works inside the pretrained space; watch the domain gap.
6. Tune descriptions on a dev split, never against the test set.

## Self-Check Questions

1. What property of a pretrained model makes zero-shot classification possible?
2. How does a prototype differ from a single support example, and why is the mean used?
3. What is the difference between in-context few-shot and fine-tuning?
4. Why is tuning class descriptions against the test set a form of leakage?
5. What is the cost ladder, and why try each rung in order?
6. Why does zero-shot fail on an out-of-distribution domain?

## Summary

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

## Further Reading / Connections

- `39-transfer-learning-lecture.md` — the fine-tuning rung of the ladder.
- `47-self-supervised-learning-lecture.md` — how the shared space is learned (CLIP).
- `06-embeddings` module — the embedding models this relies on.
- Official docs: <https://pytorch.org/docs/stable/nn.functional.html#cosine-similarity>

## History and Motivation

Zero-shot learning began with attribute-based methods: describe a class by
attributes ("has stripes, is a mammal") and classify by matching attributes,
with no examples of the class. It was a niche idea until CLIP (2021) showed that
a contrastive image-text model could do zero-shot classification at scale, simply
by comparing embeddings. CLIP turned a research curiosity into a product
primitive.

Few-shot learning followed a parallel path — prototypical networks and matching
networks (2016-2017) formalized "classify by comparing to a few examples." Then
GPT-3 (2020) introduced in-context learning: few-shot via the prompt, no gradient
step, which reframed few-shot as conditioning rather than metric learning. The
two lineages — embedding similarity and in-context conditioning — are both live
today, and this topic covers both.

## Next Steps

Next: **[47 — Self-Supervised
Learning](47-self-supervised-learning-lecture.md)** — learning without
labels at all.


