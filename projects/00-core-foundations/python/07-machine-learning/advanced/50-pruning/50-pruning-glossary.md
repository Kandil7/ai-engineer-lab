# Pruning — Glossary 50

Companion lecture: `50-pruning-lecture.md`

## Quick Reference Table

| Term | Category | One-Line Definition |
|---|---|---|
| Pruning | Technique | Removing weights that barely matter |
| Unstructured | Family | Zero individual weights -> sparse matrix |
| Structured | Family | Remove whole channels -> smaller dense |
| Magnitude pruning | Criterion | Remove smallest-|w| weights |
| Global pruning | Strategy | One fraction across the whole network |
| Lottery ticket | Theory | A sparse subnetwork matches the dense net |
| Fine-tune after prune | Recipe | Recover accuracy post-pruning |
| Sparsity | Metric | Fraction of weights that are zero |

## Detailed Definitions

### Pruning
**Definition**: Reducing a model's size by removing weights that contribute
little, then optionally fine-tuning to recover accuracy.
**Example**:
```python
prune.l1_unstructured(lin, name="weight", amount=0.5)
```
**Related**: Unstructured, Structured

### Unstructured pruning
**Definition**: Zeroing individual weights anywhere in the network, producing a
sparse matrix that compresses well but may not speed up on standard hardware.
**Related**: Structured pruning, Sparsity

### Structured pruning
**Definition**: Removing entire channels, filters, or rows, producing a smaller
dense model that is hardware-friendly and actually faster.
**Related**: Unstructured pruning

### Magnitude pruning
**Definition**: The default criterion — remove the weights with the smallest
absolute value, on the assumption they contribute least.
**Related**: Pruning, Global pruning

### Global pruning
**Definition**: Applying one sparsity fraction across the whole network so the
least-important weights are found anywhere, respecting per-layer sensitivity.
**Related**: Magnitude pruning

### Lottery ticket
**Definition**: The hypothesis that a dense network contains a sparse subnetwork
that trains to the same accuracy — motivation for pruning as subnetwork search.
**Related**: Pruning

### Fine-tune after prune
**Definition**: A short training pass after pruning so surviving weights adapt to
the smaller structure and accuracy is recovered.
**Related**: Pruning, Iterative pruning

### Sparsity
**Definition**: The fraction of weights that are zero — a compression number, not
a guarantee of speedup.
**Related**: Unstructured pruning, Pruning

## Key Concepts Summary

### The two families
- Unstructured: max sparsity, sparse matrix, uncertain speed.
- Structured: smaller dense, real speedup, coarser.

### The recipe
- prune -> fine-tune -> repeat.

## Practice Terms

Match each term to its definition (answers at the bottom).

1. Removing weights that barely matter — ___
2. Zero individual weights -> sparse — ___
3. Remove whole channels -> dense — ___
4. Remove smallest-|w| weights — ___
5. One fraction across the network — ___
6. Sparse subnetwork matches dense — ___
7. Recover accuracy post-pruning — ___
8. Fraction of zero weights — ___

**Answers:** 1-pruning, 2-unstructured, 3-structured, 4-magnitude pruning,
5-global pruning, 6-lottery ticket, 7-fine-tune after prune, 8-sparsity
