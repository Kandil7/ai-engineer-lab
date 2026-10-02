# 07-machine-learning — 45: Data Augmentation — More Signal From the Same Data

Companion exercise: `45-data-augmentation.py`

---

## Topic Overview

Data augmentation synthesizes new training examples by transforming
existing
ones — flipping an image, adding noise, cropping, rotating — without
changing
their label. The goal is to teach the model the *invariances* it should
have:
a horizontal flip of a cat is still a cat, so the model should not learn
a
spurious dependence on left-versus-right. Augmentation is regularization
in the
data domain: it constrains the model to generalize, rather than
memorize.

This topic covers the mechanics — the transform, the label-invariance
rule, and
the augmentation pipeline — plus the two disciplines that make it safe.
First,
an augmentation must never change the label; a rotation that flips a "6"
into a
"9" is wrong. Second, augmentation must be applied *only* to the
training set,
never the validation or test set, or your eval numbers become dishonest.

Augmentation is not just for images: text (synonym replacement,
back-translation),
audio (pitch shift, time stretch), and tabular data (SMOTE, noise
injection) all
use the same principle. The exercise demonstrates the image case in pure
PyTorch
so the mechanism is visible, but the rule — choose a label-preserving
transform
per domain — is universal.

## Learning Objectives

By the end of this lecture, you will be able to:

1. Explain augmentation as label-preserving data regularization.
2. Distinguish label-preserving from label-breaking transforms.
3. Build a composition of transforms applied on the fly.
4. Explain why augmentation applies only to training, never eval.
5. Recognize augmentation across text, audio, and tabular data.
6. State when augmentation helps most (small data) and least (huge data).
7. Implement a basic augmentation pipeline in PyTorch.
8. Explain mixup and cutmix as stronger, label-mixing augmentations.

## Prerequisites

| Need | Where |
|---|---|
| Tensors | `36-pytorch-tensors.py` |
| Training loop | `37-pytorch-training-loop.py` |
| Overfitting | `22-cross-validation.py` |

## 1. The Idea — Regularization in the Data Domain

### What augmentation does

Instead of adding a penalty to the loss, augmentation injects the
invariance into
the data itself. A model trained on both the original and flipped
versions learns
that "flipped" is not a signal — which is exactly the prior a vision
model needs.

### The real-world analogy

A child learns to recognize a cat not from one photograph but from many
angles,
lighting conditions, and crops. Augmentation is showing the model the
same
object under many valid variations, so it latches onto the object's
essence
rather than the photograph's accidents.

### Why it beats hand-engineering

Hand-coding "the model should be flip-invariant" is hard; showing it
flipped
examples is automatic. Augmentation encodes domain knowledge (what a
valid
perturbation is) as *data*, and the optimizer does the rest. It is the
cheapest
way to inject a prior without touching the architecture or the loss.

## 2. The Label-Invariance Rule

### The one hard rule

A valid augmentation leaves the label unchanged. Flipping an image of a
cat
keeps it a cat; rotating a handwritten "6" by 180 degrees turns it into
a "9",
which breaks the label. The rule is: would a human still give the same
label?

### Per-domain invariants

- Images: flips, small rotations, crops, color jitter, noise — usually safe.
- Text: synonym swap, back-translation, deletion — safe; negation or sentiment
  flip — unsafe.
- Audio: pitch shift, time stretch, noise — safe; reversing speech — unsafe.
- Tabular: SMOTE, noise injection — needs care because feature semantics vary.

### When it breaks

Augmentation breaks when the transform crosses a class boundary — the
"6" to "9"
rotation, the "not good" to "good" negation. Every domain has such
boundaries,
and the human-in-the-loop check is the only reliable guard.

## 3. The Transform Pipeline

### Composition

Augmentations compose into a pipeline applied on the fly each epoch, so
the model
sees a slightly different dataset every pass:

```python
def augment(x):
    x = random_hflip(x)
    x = x + 0.05 * torch.randn_like(x)  # gaussian noise
    return x
```

### On-the-fly vs offline

On-the-fly augmentation (applied in the dataloader) costs compute but
stores
nothing extra; offline augmentation (materialized to disk) stores an
inflated
dataset but is a one-time cost. On-the-fly is the default for images,
because
the transform is cheap and the disk is better spent on the raw data.

## 4. Training Only, Never Eval

### The leakage risk

Augmentation is a training-only transformation. If you augment the
validation or
test set, the eval distribution no longer matches production, and your
metrics
lie. The discipline is structural: the eval pipeline is the *clean*
pipeline, the
training pipeline is the *augmented* one.

### The code shape

```python
train_loader = DataLoader(train_set, ...)  # augmented transforms
eval_loader = DataLoader(val_set, ...)  # only normalization, no augmentation
```

### Why it is subtle

The leak is invisible — the augmented eval examples still have correct
labels,
so nothing crashes; the metric just looks a bit too good. That is
exactly the
kind of bug that survives a smoke test and only shows up in production
degradation, which is why the train/eval transform split must be
structural.

## 5. Augmentation as a Regularizer

### The effect on overfitting

Augmentation is most valuable when data is scarce and the model is large
— the
overfitting regime. It reduces the effective capacity to memorize by
forcing the
model to share features across transformed versions of the same example.

### The diminishing returns

With a huge, diverse dataset, augmentation adds less, because the real
data
already covers the variance. The classic win is the small-data case — a
few
thousand images — where augmentation can be the difference between a
memorized
model and a generalizing one.

## 6. Beyond Images

### Text augmentation

Synonym replacement, random deletion, back-translation, and paraphrase
all expand
a text corpus while preserving meaning. The guardrail is the same: the
label
(sentiment, intent) must survive the transform.

### Audio and tabular

Audio: pitch shift, time stretch, background noise. Tabular: SMOTE for
class
imbalance, noise injection, and mixup. Each domain needs a human to
decide what
perturbation is label-preserving — the mechanism is generic, the
invariant is not.

## 7. Mixup and Cutmix

### Label-mixing augmentations

Mixup blends two examples *and their labels* in proportion; cutmix cuts
a region
from one image and pastes it into another, mixing labels by area. Both
go beyond
label-preserving transforms to *label-interpolating* ones, which
encourages
smoother decision boundaries and strong regularization.

### When to use them

Mixup/cutmix are the "strong" end of augmentation, most useful when the
base
transforms are not enough and the model is large. They cost a little
more compute
and complicate the loss, but they are a standard ingredient in modern
image
training.

## 8. Text Augmentation in Depth

### The techniques

Text augmentation is subtler than image augmentation because every word carries
meaning. The safe transforms are lexical, not semantic: synonym replacement
(swap a word for a near-synonym), random deletion (drop a word), random
insertion, and back-translation (translate to another language and back to get a
paraphrase). These preserve the label most of the time.

### The unsafe transforms

Anything that flips the meaning is unsafe: negating a verb, swapping sentiment
words, or replacing an entity with a different one. "The film was great" must not
become "the film was terrible." The label-invariance rule (`2`) is harder to
guarantee for text, which is why text augmentation is validated more carefully.

### Why it matters for low-resource languages

For languages with little labeled data — Arabic dialects, for instance —
augmentation is disproportionately valuable. Back-translation and paraphrase are
how a small Arabic corpus is stretched into a viable training set, and the same
discipline (split first, augment only training, verify the label survives)
applies exactly as it does for images.

## 9. Audio and Tabular Augmentation

### Audio: warping the signal, not the meaning

Audio augmentation warps the signal without changing the content: pitch shift,
time stretch, background noise, and SpecAugment (masking frequency/time bands
of a spectrogram). These make a speech or sound model robust to recording
variation. The guardrail is the same — a pitch shift must not change *what was
said*.

### Tabular: the hardest case

Tabular data has no obvious spatial or temporal structure, so augmentation is
harder and riskier. SMOTE synthesizes minority-class examples by interpolating
between neighbors; noise injection perturbs features slightly. But feature
semantics vary — perturbing a "has_disease" binary is not like perturbing a
pixel — so every tabular transform needs a human to confirm it is label-
preserving.

### The common thread

Across every domain the principle is identical: choose a perturbation that a
human would still label the same way, apply it only to training, and verify it
empirically. The mechanism is generic; the invariant is domain-specific, and
getting the invariant wrong is the failure mode that survives every framework.

## Real-World Application

- **Image classification on small datasets** — augmentation is the difference
  between a memorized and a generalizing model.
- **Text/NLP** — back-translation and paraphrase for low-resource languages.
- **Speech/audio** — pitch and time warping for robust recognition.
- **Imbalanced tabular data** — SMOTE to synthesize minority examples.
- **The Athar/DevMate case** — Arabic text augmentation (paraphrase, dialect
  variants) where labeled data is scarce.

## Common Mistakes to Avoid

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

### Mistake 6: Over-augmenting past the point of realism
```
# WRONG — transforms so extreme the "augmented" examples no longer resemble reality
# CORRECT — stay within the distribution of plausible real variations
```

## Best Practices

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

## Complexity and Cost

| Operation | Time | Space | Notes |
|---|---|---|---|
| On-the-fly transform | per-batch CPU | none | The default; overlaps with training |
| Offline augmentation | one-time | dataset x N | More disk, faster epochs |
| Mixup/cutmix | per-batch | none | Stronger, slightly more compute |
| Augmentation benefit | — | — | Largest on small data |

## AI Engineering Relevance

**Where this shows up:** any model trained on a modest dataset — which on a
single RTX 5000 is most of what you will train locally. Augmentation is
the
cheapest accuracy win before you buy more data or a bigger model.

| Concept here | Used for |
|---|---|
| Label-preserving transforms | Encoding domain invariants as data |
| Train-only augmentation | Honest eval numbers |
| Small-data regularization | Making a few-thousand-sample task viable |
| Per-domain invariants | Text/audio/tabular pipelines |

**Scale note:** augmentation is a *data* lever, not a *compute* lever. When GPU
hours are the constraint, augmentation buys generalization without more
compute —
the right trade on a 16 GB single-GPU budget.

## Key Takeaways

1. Augmentation is regularization in the data domain — it teaches invariances.
2. The one hard rule: the transform must not change the label.
3. The one discipline: augment training only, never eval.
4. Split first, then augment, so no example leaks across folds.
5. It helps most on small data and least on huge diverse data.
6. Mixup/cutmix are the strong, label-interpolating end of augmentation.

## Self-Check Questions

1. Why is augmentation considered regularization, and where does it differ from weight decay?
2. What is the one hard rule for a valid transform, and what is an example of breaking it?
3. Why must augmentation be applied only to the training set, and what makes the leak subtle?
4. Why must you split before augmenting, not after?
5. When does augmentation add the least value, and why?
6. How do mixup and cutmix differ from ordinary label-preserving augmentation?

## Summary

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

## Further Reading / Connections

- `39-transfer-learning-lecture.md` — the pretrained-model sibling of augmentation.
- `22-cross-validation-lecture.md` — the overfitting regime augmentation fights.
- `47-self-supervised-learning-lecture.md` — augmentation as the "view" in contrastive learning.
- Official docs: <https://pytorch.org/vision/stable/transforms.html>

## Next Steps

Next: **[46 — Few-Shot and Zero-Shot
Learning](46-few-shot-zero-shot-lecture.md)** — generalizing from a
handful of examples.

Continues in: **[39 — Transfer
Learning](39-transfer-learning-lecture.md)** — the pretrained-model
sibling of augmentation.

