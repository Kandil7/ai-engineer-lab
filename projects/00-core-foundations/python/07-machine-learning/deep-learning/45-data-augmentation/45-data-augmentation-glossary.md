# Data Augmentation — Glossary 45

Companion lecture: `45-data-augmentation-lecture.md`

## Quick Reference Table

| Term | Category | One-Line Definition |
|---|---|---|
| Augmentation | Technique | Label-preserving transforms that synthesize new training examples |
| Label invariance | Rule | A valid transform never changes the ground truth |
| On-the-fly | Strategy | Apply transforms in the dataloader, store nothing extra |
| Offline | Strategy | Materialize the augmented dataset to disk |
| Mixup | Technique | Blend two examples and their labels in proportion |
| Cutmix | Technique | Cut-and-paste regions across examples |
| SMOTE | Technique | Synthetic minority oversampling for tabular imbalance |
| Regularizer | Effect | Augmentation fights overfitting in the data domain |
| Train-only | Discipline | Augment training, never eval |

## Detailed Definitions

### Augmentation
**Definition**: Generating additional training examples by applying label-preserving
transformations to existing ones, teaching the model the invariances it should have.
**Example**:
```python
aug_x = x.flip(-1) + 0.05 * torch.randn_like(x)
```
**Related**: Label invariance, Regularizer

### Label invariance
**Definition**: The rule that an augmentation must leave the label unchanged — a
human would still assign the same answer. The guardrail that makes augmentation
safe.
**Example**:
```python
# safe: horizontal flip of a cat; unsafe: 180-degree rotate of a digit "6"
```
**Related**: Augmentation

### On-the-fly
**Definition**: Applying augmentation in the dataloader each epoch, so the model
sees a different dataset every pass without extra disk.
**Related**: Offline, Augmentation

### Offline
**Definition**: Materializing the augmented dataset to disk once, trading storage
for faster epochs.
**Related**: On-the-fly, Augmentation

### Mixup
**Definition**: A strong augmentation that blends two examples and their labels in
proportion, encouraging smoother decision boundaries.
**Related**: Cutmix, Augmentation

### Cutmix
**Definition**: A strong augmentation that cuts a region from one image and pastes
it into another, with the label mixed proportionally to the area.
**Related**: Mixup, Augmentation

### SMOTE
**Definition**: Synthetic Minority Over-sampling Technique — generating synthetic
minority-class examples for imbalanced tabular data.
**Related**: Augmentation

### Regularizer
**Definition**: The effect of augmentation — constraining the model to share
features across transformed versions, reducing memorization.
**Related**: Augmentation, Train-only

### Train-only
**Definition**: The discipline that augmentation applies to the training set only,
so eval reflects the true production distribution.
**Related**: Augmentation, Label invariance

## Key Concepts Summary

### The two disciplines
- Label invariance: the transform must not change the answer.
- Train-only: never augment eval data.

### The payoff
- Augmentation is the cheapest accuracy win on small data.

## Practice Terms

Match each term to its definition (answers at the bottom).

1. Label-preserving transforms that synthesize examples — ___
2. The rule that the transform must not change the answer — ___
3. Apply transforms in the dataloader — ___
4. Materialize the augmented set to disk — ___
5. Blend two examples and labels — ___
6. Synthetic minority oversampling — ___
7. Fights overfitting in the data domain — ___
8. Augment training, never eval — ___

**Answers:** 1-augmentation, 2-label invariance, 3-on-the-fly, 4-offline,
5-mixup, 6-SMOTE, 7-regularizer, 8-train-only
