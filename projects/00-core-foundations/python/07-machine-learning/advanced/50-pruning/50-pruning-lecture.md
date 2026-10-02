# 07-machine-learning — 50: Pruning — Remove the Weights You Don't Need

Companion exercise: `50-pruning.py`

---

## Topic Overview

A trained network is full of weights that barely matter — near-zero entries that
contribute nothing to the output. Pruning removes them, shrinking the model and
often speeding it up, with little loss. The two families are **unstructured**
pruning (zero individual weights, producing sparse matrices) and **structured**
pruning (remove entire channels or filters, producing smaller dense matrices).
The distinction decides whether you actually get a speedup.

The simplest criterion is magnitude: weights closest to zero are removed first,
on the assumption that small weights matter least. This is the workhorse, and it
is built into PyTorch via `torch.nn.utils.prune`. The deeper result is the
lottery-ticket hypothesis — inside a dense network sits a sparse subnetwork that
trains to the same accuracy — which motivates pruning as a way to find that
subnetwork.

For a 16 GB GPU, pruning is a size and speed lever that pairs naturally with
quantization (`49`) and distillation (`51`) — the three tools of the compression
toolbox. The exercise applies magnitude, global, and structured pruning so the
difference between sparsity and actual speedup is concrete.

## Learning Objectives

By the end of this lecture, you will be able to:

1. Distinguish structured from unstructured pruning.
2. Explain magnitude pruning as the default criterion.
3. Use `torch.nn.utils.prune` for local, global, and structured pruning.
4. Explain why sparsity does not automatically equal speedup.
5. Describe the lottery-ticket hypothesis and its implication.
6. Choose structured pruning when a real speedup is the goal.
7. Combine pruning with fine-tuning to recover accuracy.

## Prerequisites

| Need | Where |
|---|---|
| Neural network basics | `38-neural-network-basics.py` |
| Model size/speed | `49-quantization.py` |

## 1. Unstructured vs Structured Pruning

### Unstructured

Unstructured pruning zeroes individual weights — any entry, anywhere. It can
reach very high sparsity (say 90%) with little accuracy loss, but the result is
a sparse matrix, which is hard to accelerate on standard hardware without
special support.

### Structured

Structured pruning removes whole units — entire channels, filters, or rows — so
the result is a smaller *dense* model. It is easier to speed up because the
model just got smaller in a hardware-friendly way, but it is coarser and drops
more accuracy per unit of sparsity.

### The deciding question

Sparsity is a number; speedup is a goal. If you need the speedup, prefer
structured. If you need maximum compression, unstructured wins but the speedup
is not guaranteed.

## 2. Magnitude Pruning

### The criterion

Magnitude pruning removes weights with the smallest absolute value — they
contribute least to the output. It is simple, effective, and the default.

### The code

```python
import torch.nn.utils.prune as prune

prune.l1_unstructured(lin, name="weight", amount=0.5)  # zero the bottom 50%
```

The `amount` is the fraction removed. After pruning, `lin.weight_mask` records
what was kept, and the pruned weights read as zero.

## 3. Global vs Local Pruning

### Local

Local pruning applies a fixed fraction per layer — every layer loses, say, 50%.
Simple, but it over-prunes layers that matter and under-prunes layers that don't.

### Global

Global pruning applies one fraction across the whole network, letting the
criterion find the least-important weights *anywhere*. It reaches the same
sparsity with less accuracy loss, at the cost of more bookkeeping.

```python
prune.global_unstructured(
    [(l1, "weight"), (l2, "weight")], pruning_method=prune.L1Unstructured, amount=0.5
)
```

## 4. The Lottery-Ticket Hypothesis

### The claim

Inside a randomly-initialized dense network there is a sparse subnetwork that,
trained alone, matches the full network's accuracy. Pruning finds an
approximation of that "winning ticket." The implication is that over-parameterized
networks hide efficient subnetworks — and pruning is how you surface them.

### The practical takeaway

Pruning is not just compression; it is evidence that much of a network's capacity
is redundant. The practical result is the same — smaller, faster models — but the
reason is deeper than "drop the small weights."

## 5. Prune, Then Fine-Tune

### The two-step

Pruning usually drops some accuracy. The standard remedy is a short fine-tuning
pass after pruning, so the surviving weights adapt to the new, smaller structure.
Prune → fine-tune → repeat (iterative pruning) recovers most of the loss.

### Why it matters

Pruning without fine-tuning leaves accuracy on the floor; fine-tuning without
pruning buys nothing. The two are a pair, and the recipe is what makes pruning
viable in practice.

## 6. Common Mistakes to Avoid

### Mistake 1: Expecting speedup from unstructured sparsity
```
# WRONG — a 90% sparse matrix with no sparse-kernel support runs no faster
# CORRECT — use structured pruning when a real speedup is the goal
```

### Mistake 2: Pruning without a fine-tune pass
```
# WRONG — drop 50% of weights and ship the accuracy loss
# CORRECT — prune, then fine-tune, then measure
```

### Mistake 3: One-shot over-pruning
```
# WRONG — remove 90% in one step and watch accuracy collapse
# CORRECT — prune iteratively in small steps with fine-tuning between
```

### Mistake 4: Local pruning ignoring layer sensitivity
```
# WRONG — a uniform 50% on a bottleneck layer that cannot spare it
# CORRECT — global pruning, or per-layer sensitivity analysis
```

### Mistake 5: Measuring sparsity instead of the real goal
```
# WRONG — reporting "95% sparse" when the model is neither smaller nor faster
# CORRECT — report latency, memory, and accuracy, not sparsity alone
```

## 7. Best Practices

1. Use magnitude (L1) pruning as the default criterion.
2. Prefer structured pruning when speedup is the goal.
3. Follow every prune with a short fine-tune pass.
4. Prune iteratively in small steps, not one big cut.
5. Use global pruning to respect per-layer sensitivity.
6. Report latency and memory, not just sparsity.
7. Keep the unpruned model for comparison and rollback.
8. Combine pruning with quantization for compounding wins.

## 8. Complexity and Cost

| Operation | Time | Space | Notes |
|---|---|---|---|
| Unstructured prune | seconds | sparse | Max compression, uncertain speed |
| Structured prune | seconds | smaller dense | Real speedup, coarser |
| Fine-tune after prune | minutes | — | Recovers accuracy |
| Iterative pruning | N x prune+fine-tune | — | Best accuracy per sparsity |

## 9. AI Engineering Relevance

**Where this shows up:** shrinking a model for a tight VRAM or latency budget.
On the RTX 5000, pruning is the lever you pull alongside quantization when a
model is too big or too slow — and the structured/unstructured distinction is
what decides whether the shrink actually makes it faster.

| Concept here | Used for |
|---|---|
| Structured pruning | Real, hardware-friendly speedup |
| Magnitude criterion | The default "what to remove" rule |
| Prune-then-fine-tune | Recovering accuracy after pruning |
| Lottery ticket | Why over-parameterized nets compress well |

**Scale note:** pruning pairs with quantization — a pruned INT8 model is smaller
and faster on both axes. The compression toolbox (quantize, prune, distill) is
applied together, not in isolation.

## 10. Summary

| Concept | Description |
|---|---|
| Unstructured | Zero individual weights -> sparse |
| Structured | Remove whole channels -> smaller dense |
| Magnitude | Remove smallest-|w| weights |
| Lottery ticket | Sparse subnetworks match dense nets |
| Prune-then-fine-tune | The accuracy-recovery recipe |

## Quick Reference

| Task | Idiom |
|---|---|
| Unstructured | `prune.l1_unstructured(lin, name="weight", amount=0.5)` |
| Global | `prune.global_unstructured([(l1,"weight"),...], prune.L1Unstructured, amount=0.5)` |
| Structured | `prune.ln_structured(lin, name="weight", amount=0.5, n=1, dim=0)` |
| Make permanent | `prune.remove(lin, "weight")` |

## Next Steps

Next: **[51 — Knowledge Distillation](../advanced/51-distillation-lecture.md)** — compress a big teacher into a small student.

Continues in: **[49 — Quantization](49-quantization-lecture.md)** — the size lever this pairs with.

Official docs: <https://pytorch.org/docs/stable/generated/torch.nn.utils.prune.l1_unstructured.html>
