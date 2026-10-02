# 07-machine-learning — 45: Data Augmentation — More Signal From the Same Data

Companion exercise: `45-data-augmentation.py`

---

## Topic Overview

Data augmentation synthesizes new training examples by transforming existing
ones — flipping an image, adding noise, cropping, rotating — without changing
their label. The goal is to teach the model the *invariances* it should have:
a horizontal flip of a cat is still a cat, so the model should not learn a
spurious dependence on left-versus-right. Augmentation is regularization in the
data domain: it constrains the model to generalize, rather than memorize.

This topic covers the mechanics — the transform, the label-invariance rule, and
the augmentation pipeline — plus the two disciplines that make it safe. First,
an augmentation must never change the label; a rotation that flips a "6" into a
"9" is wrong. Second, augmentation must be applied *only* to the training set,
never the validation or test set, or your eval numbers become dishonest.

Augmentation is not just for images: text (synonym replacement, back-translation),
audio (pitch shift, time stretch), and tabular data (SMOTE, noise injection) all
use the same principle. The exercise demonstrates the image case in pure PyTorch
so the mechanism is visible.

## Learning Objectives

By the end of this lecture, you will be able to:

1. Explain augmentation as label-preserving data regularization.
2. Distinguish label-preserving from label-breaking transforms.
3. Build a composition of transforms applied on the fly.
4. Explain why augmentation applies only to training, never eval.
5. Recognize augmentation across text, audio, and tabular data.
6. State when augmentation helps most (small data) and least (huge data).
7. Implement a basic augmentation pipeline in PyTorch.

## Prerequisites

| Need | Where |
|---|---|
| Tensors | `36-pytorch-tensors.py` |
| Training loop | `37-pytorch-training-loop.py` |
| Overfitting | `22-cross-validation.py` |

## 1. The Idea — Regularization in the Data Domain

### What augmentation does

Instead of adding a penalty to the loss, augmentation injects the invariance into
the data itself. A model trained on both the original and flipped versions learns
that "flipped" is not a signal — which is exactly the prior a vision model needs.

### Why it beats hand-engineering

Hand-coding "the model should be flip-invariant" is hard; showing it flipped
examples is automatic. Augmentation encodes domain knowledge (what a valid
perturbation is) as *data*, and the optimizer does the rest.

## 2. The Label-Invariance Rule

### The one hard rule

A valid augmentation leaves the label unchanged. Flipping an image of a cat
keeps it a cat; rotating a handwritten "6" by 180 degrees turns it into a "9",
which breaks the label. The rule is: would a human still give the same label?

### Per-domain invariants

- Images: flips, small rotations, crops, color jitter, noise — usually safe.
- Text: synonym swap, back-translation, deletion — safe; negation or sentiment
  flip — unsafe.
- Audio: pitch shift, time stretch, noise — safe; reversing speech — unsafe.
- Tabular: SMOTE, noise injection — needs care because feature semantics vary.

## 3. The Transform Pipeline

### Composition

Augmentations compose into a pipeline applied on the fly each epoch, so the model
sees a slightly different dataset every pass:

```python
def augment(x):
    x = random_hflip(x)
    x = x + 0.05 * torch.randn_like(x)  # gaussian noise
    return x
```

### On-the-fly vs offline

On-the-fly augmentation (applied in the dataloader) costs compute but stores
nothing extra; offline augmentation (materialized to disk) stores an inflated
dataset but is a one-time cost. On-the-fly is the default for images.

## 4. Training Only, Never Eval

### The leakage risk

Augmentation is a training-only transformation. If you augment the validation or
test set, the eval distribution no longer matches production, and your metrics
lie. The discipline is structural: the eval pipeline is the *clean* pipeline, the
training pipeline is the *augmented* one.

### The code shape

```python
train_loader = DataLoader(train_set, ...)  # augmented transforms
eval_loader = DataLoader(val_set, ...)  # only normalization, no augmentation
```

## 5. Augmentation as a Regularizer

### The effect on overfitting

Augmentation is most valuable when data is scarce and the model is large — the
overfitting regime. It reduces the effective capacity to memorize by forcing the
model to share features across transformed versions of the same example.

### The diminishing returns

With a huge, diverse dataset, augmentation adds less, because the real data
already covers the variance. The classic win is the small-data case — a few
thousand images — where augmentation can be the difference between a memorized
model and a generalizing one.

## 6. Beyond Images

### Text augmentation

Synonym replacement, random deletion, back-translation, and paraphrase all expand
a text corpus while preserving meaning. The guardrail is the same: the label
(sentiment, intent) must survive the transform.

### Audio and tabular

Audio: pitch shift, time stretch, background noise. Tabular: SMOTE for class
imbalance, noise injection, and mixup. Each domain needs a human to decide what
perturbation is label-preserving — the mechanism is generic, the invariant is not.

## 7. Common Mistakes to Avoid

### Mistake 1: Augmenting the test set
```
# WRONG — the eval pipeline applies flips/rotations
# CORRECT — eval uses only normalization; augmentation is train-only
```

### Mistake 2: Label-breaking transforms
```
# WRONG — a 180-degree rotation on handwritten digits (6 <-> 9)
# CORRECT — restrict transforms to the domain's valid invariants
```

### Mistake 3: Augmenting before the train/test split
```
# WRONG — augment first, then split; an original and its flip leak across folds
# CORRECT — split first, then augment only the training fold
```

### Mistake 4: Assuming one size fits all domains
```
# WRONG — flipping text or rotating tabular rows blindly
# CORRECT — choose the invariant per domain with a human in the loop
```

### Mistake 5: Forgetting normalization after augmentation
```
# WRONG — augmented images with a different scale than training-time normalization
# CORRECT — keep the normalization transform last and identical for train/eval
```

## 8. Best Practices

1. Split first, then augment only the training fold.
2. Verify each transform is label-preserving for the specific domain.
3. Compose transforms and apply on the fly in the dataloader.
4. Keep normalization identical between train and eval.
5. Start mild (flip + small crop) and add intensity only if it helps.
6. Use augmentation most aggressively when data is scarce.
7. Measure the effect on a held-out set — augmentation is not always free.
8. Record the exact augmentation recipe for reproducibility.
9. Consider mixup/cutmix for stronger image regularization.
10. For text/audio, sanity-check the label survives the transform.

## 9. Complexity and Cost

| Operation | Time | Space | Notes |
|---|---|---|---|
| On-the-fly transform | per-batch CPU | none | The default; overlaps with training |
| Offline augmentation | one-time | dataset x N | More disk, faster epochs |
| Mixup/cutmix | per-batch | none | Stronger, slightly more compute |
| Augmentation benefit | — | — | Largest on small data |

## 10. AI Engineering Relevance

**Where this shows up:** any model trained on a modest dataset — which on a
single RTX 5000 is most of what you will train locally. Augmentation is the
cheapest accuracy win before you buy more data or a bigger model.

| Concept here | Used for |
|---|---|
| Label-preserving transforms | Encoding domain invariants as data |
| Train-only augmentation | Honest eval numbers |
| Small-data regularization | Making a few-thousand-sample task viable |
| Per-domain invariants | Text/audio/tabular pipelines |

**Scale note:** augmentation is a *data* lever, not a *compute* lever. When GPU
hours are the constraint, augmentation buys generalization without more compute —
the right trade on a 16 GB single-GPU budget.

## 11. Summary

| Concept | Description |
|---|---|
| Augmentation | Label-preserving transforms applied to training data |
| Label invariance | The transform must not change the ground truth |
| On-the-fly | Apply in the dataloader, store nothing |
| Train-only | Never augment eval data |
| Regularizer | Fights overfitting in the data domain |

## Quick Reference

| Task | Idiom |
|---|---|
| Flip | `x.flip(-1)` (horizontal) |
| Noise | `x + sigma * torch.randn_like(x)` |
| Compose | a list of transforms applied in order |
| Eval pipeline | normalization only |

## Next Steps

Next: **[46 — Few-Shot and Zero-Shot Learning](46-few-shot-zero-shot-lecture.md)** — generalizing from a handful of examples.

Continues in: **[39 — Transfer Learning](39-transfer-learning-lecture.md)** — the pretrained-model sibling of augmentation.

Official docs: <https://pytorch.org/vision/stable/transforms.html>
