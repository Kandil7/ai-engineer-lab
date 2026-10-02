# Few-Shot and Zero-Shot Learning — Glossary 46

Companion lecture: `46-few-shot-zero-shot-lecture.md`

## Quick Reference Table

| Term | Category | One-Line Definition |
|---|---|---|
| Zero-shot | Regime | Classify by matching class descriptions, no examples |
| Few-shot | Regime | Classify from k labeled examples per class |
| Shared space | Premise | Embedding space where related things are close |
| Prototype | Few-shot | The mean embedding of a support set |
| Support set | Few-shot | The k labeled examples per class |
| In-context learning | LLM | Few-shot via the prompt, no weight update |
| Cosine similarity | Metric | Normalized dot product measuring alignment |
| CLIP | Model | Contrastive image-text model enabling zero-shot |

## Detailed Definitions

### Zero-shot
**Definition**: Classifying with no labeled examples of the target classes, by
matching an input's embedding against class names or descriptions in a shared
space.
**Example**:
```python
argmax over cosine(query_embed, class_embed)
```
**Related**: Shared space, Few-shot

### Few-shot
**Definition**: Classifying from a handful (k) of labeled examples per class,
typically by nearest-prototype over a support set.
**Example**:
```python
prototype = support.mean(dim=0)
```
**Related**: Zero-shot, Prototype

### Shared space
**Definition**: The embedding space a pretrained model produces, where meaning is
geometry — related inputs and concepts are close, enabling similarity-based
classification.
**Related**: Zero-shot, CLIP

### Prototype
**Definition**: The class center computed as the mean of its support examples,
averaging out per-example noise.
**Related**: Few-shot, Support set

### Support set
**Definition**: The small set of labeled examples used to define classes in
few-shot learning.
**Related**: Prototype, Few-shot

### In-context learning
**Definition**: LLM few-shot performed by placing examples in the prompt, letting
the model infer the pattern by attention with no weight update.
**Related**: Few-shot

### Cosine similarity
**Definition**: The normalized dot product measuring alignment between two
vectors, the standard similarity for embedding comparison.
**Example**:
```python
sim = (F.normalize(a, dim=-1) * F.normalize(b, dim=-1)).sum(-1)
```
**Related**: Shared space, Zero-shot

### CLIP
**Definition**: A contrastive image-text model whose joint embedding space
enables zero-shot image classification by text description.
**Related**: Shared space, Zero-shot

## Key Concepts Summary

### The cost ladder
- zero-shot (free) -> few-shot (cheap) -> fine-tune (costly)

### The two mechanisms
- Embedding similarity: zero-shot and prototypical few-shot.
- In-context conditioning: LLM few-shot, no weight change.

## Practice Terms

Match each term to its definition (answers at the bottom).

1. Classify by matching class descriptions — ___
2. Classify from k examples per class — ___
3. Space where related things are close — ___
4. Mean embedding of a support set — ___
5. The k labeled examples per class — ___
6. LLM few-shot via the prompt — ___
7. Normalized dot product — ___
8. Contrastive image-text model — ___

**Answers:** 1-zero-shot, 2-few-shot, 3-shared space, 4-prototype,
5-support set, 6-in-context learning, 7-cosine similarity, 8-CLIP
