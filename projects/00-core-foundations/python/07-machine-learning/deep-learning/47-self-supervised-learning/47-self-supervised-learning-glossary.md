# Self-Supervised Learning — Glossary 47

Companion lecture: `47-self-supervised-learning-lecture.md`

## Quick Reference Table

| Term | Category | One-Line Definition |
|---|---|---|
| Self-supervised learning | Paradigm | Learning from labels invented out of the data itself |
| Pretext task | SSL | An artificial task whose answer is already in the data |
| Contrastive | SSL family | Pull views of the same example together, push others apart |
| Masked modeling | SSL family | Hide part of the input and reconstruct it |
| InfoNCE | Loss | The contrastive loss over positive and negative pairs |
| Positive pair | Contrastive | Two views of the same example |
| Negative pair | Contrastive | Views of different examples |
| Representation collapse | Failure | All embeddings drift to one point |
| Pretrain-then-fine-tune | Workflow | SSL pretrain on unlabeled data, fine-tune on labeled |

## Detailed Definitions

### Self-supervised learning
**Definition**: Training a model on a task constructed from the data itself — no
human labels — so the model learns representations that transfer to real tasks.
**Example**:
```text
mask 15% of tokens and predict them; the answer is in the data
```
**Related**: Pretext task, Contrastive

### Pretext task
**Definition**: The artificial training task whose label is derivable from the
data — next-token prediction, masked reconstruction, view matching. Discarded
after training; the encoder is kept.
**Related**: Self-supervised learning

### Contrastive
**Definition**: The SSL family that pulls augmented views of the same example
together and pushes different examples apart, learning invariances.
**Example**:
```python
loss = -log(exp(sim(z_i, z_j)/tau) / sum_k exp(sim(z_i, z_k)/tau))
```
**Related**: InfoNCE, Positive pair

### Masked modeling
**Definition**: The SSL family that hides part of the input and asks the model to
reconstruct it, learning bidirectional context and structure.
**Example**:
```text
BERT: predict the masked token from surrounding tokens
```
**Related**: Pretext task

### InfoNCE
**Definition**: The contrastive loss — a softmax over similarities — that
maximizes positive-pair similarity while minimizing negative-pair similarity.
**Related**: Contrastive, Positive pair

### Positive / negative pair
**Definition**: A positive pair is two views of the same example (must be close);
a negative pair is views of different examples (must be far).
**Related**: Contrastive, InfoNCE

### Representation collapse
**Definition**: The failure where contrastive learning maps everything to one
point, making similarities meaningless. Avoided with enough negatives, a
temperature, and normalization.
**Related**: Contrastive

### Pretrain-then-fine-tune
**Definition**: The production workflow — SSL-pretrain on abundant unlabeled data,
then fine-tune on a small labeled task.
**Related**: Self-supervised learning, Transfer learning

## Key Concepts Summary

### The two families
- Contrastive: invariance (SimCLR, CLIP).
- Masked: structure (BERT, GPT).

### The economics
- Unlabeled data is free; SSL moves most learning cost onto it.

## Practice Terms

Match each term to its definition (answers at the bottom).

1. Labels invented from the data itself — ___
2. The artificial task whose answer is in the data — ___
3. Pull views together, push others apart — ___
4. Hide part of the input and reconstruct — ___
5. The contrastive softmax loss — ___
6. Two views of the same example — ___
7. All embeddings drift to one point — ___
8. SSL pretrain then fine-tune — ___

**Answers:** 1-self-supervised learning, 2-pretext task, 3-contrastive,
4-masked modeling, 5-InfoNCE, 6-positive pair, 7-representation collapse,
8-pretrain-then-fine-tune
