# 07-machine-learning — 50: Pruning — Remove the Weights You Don't Need

Companion exercise: `50-pruning.py`

---

## Topic Overview

A trained network is full of weights that barely matter — near-zero
entries that
contribute nothing to the output. Pruning removes them, shrinking the
model and
often speeding it up, with little loss. The two families are
**unstructured**
pruning (zero individual weights, producing sparse matrices) and
**structured**
pruning (remove entire channels or filters, producing smaller dense
matrices).
The distinction decides whether you actually get a speedup.

The simplest criterion is magnitude: weights closest to zero are removed
first,
on the assumption that small weights matter least. This is the
workhorse, and it
is built into PyTorch via `torch.nn.utils.prune`. The deeper result is
the
lottery-ticket hypothesis — inside a dense network sits a sparse
subnetwork that
trains to the same accuracy — which motivates pruning as a way to find
that
subnetwork.

For a 16 GB GPU, pruning is a size and speed lever that pairs naturally
with
quantization (`49`) and distillation (`51`) — the three tools of the
compression
toolbox. The exercise applies magnitude, global, and structured pruning
so the
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
8. Reason about iterative versus one-shot pruning.

## Prerequisites

| Need | Where |
|---|---|
| Neural network basics | `38-neural-network-basics.py` |
| Model size/speed | `49-quantization.py` |

## 1. Unstructured vs Structured Pruning

### Unstructured

Unstructured pruning zeroes individual weights — any entry, anywhere. It
can
reach very high sparsity (say 90%) with little accuracy loss, but the
result is
a sparse matrix, which is hard to accelerate on standard hardware
without
special support.

### Structured

Structured pruning removes whole units — entire channels, filters, or
rows — so
the result is a smaller *dense* model. It is easier to speed up because
the
model just got smaller in a hardware-friendly way, but it is coarser and
drops
more accuracy per unit of sparsity.

### The real-world analogy

Unstructured pruning is removing scattered words from a book — you save
paper but
the book is harder to read quickly. Structured pruning is removing whole
chapters
— the book is genuinely shorter and faster to read, but you might lose
something
important. Sparsity is the words removed; speedup is the chapters
removed.

### The deciding question

Sparsity is a number; speedup is a goal. If you need the speedup, prefer
structured. If you need maximum compression, unstructured wins but the
speedup
is not guaranteed.

## 2. Magnitude Pruning

### The criterion

Magnitude pruning removes weights with the smallest absolute value —
they
contribute least to the output. It is simple, effective, and the
default.

### The code

```python
import torch.nn.utils.prune as prune

prune.l1_unstructured(lin, name="weight", amount=0.5)  # zero the bottom 50%
```

The `amount` is the fraction removed. After pruning, `lin.weight_mask`
records
what was kept, and the pruned weights read as zero.

### Why it works

The assumption is that the output is most sensitive to the largest
weights, so
removing the smallest changes the output least. This is exactly true for
a
linear layer, and approximately true for the nonlinear case — which is
why
magnitude pruning is both simple and surprisingly effective.

## 3. Global vs Local Pruning

### Local

Local pruning applies a fixed fraction per layer — every layer loses,
say, 50%.
Simple, but it over-prunes layers that matter and under-prunes layers
that don't.

### Global

Global pruning applies one fraction across the whole network, letting
the
criterion find the least-important weights *anywhere*. It reaches the
same
sparsity with less accuracy loss, at the cost of more bookkeeping.

```python
prune.global_unstructured(
    [(l1, "weight"), (l2, "weight")], pruning_method=prune.L1Unstructured, amount=0.5
)
```

### Why global wins on accuracy

Some layers are more sensitive than others. Global pruning lets the
criterion
spend sparsity where it hurts least, rather than imposing a uniform cut
that
hits a critical bottleneck layer as hard as a redundant one.

## 4. The Lottery-Ticket Hypothesis

### The claim

Inside a randomly-initialized dense network there is a sparse subnetwork
that,
trained alone, matches the full network's accuracy. Pruning finds an
approximation of that "winning ticket." The implication is that
over-parameterized
networks hide efficient subnetworks — and pruning is how you surface
them.

### The practical takeaway

Pruning is not just compression; it is evidence that much of a network's
capacity
is redundant. The practical result is the same — smaller, faster models
— but the
reason is deeper than "drop the small weights."

## 5. Prune, Then Fine-Tune

### The two-step

Pruning usually drops some accuracy. The standard remedy is a short
fine-tuning
pass after pruning, so the surviving weights adapt to the new, smaller
structure.
Prune → fine-tune → repeat (iterative pruning) recovers most of the
loss.

### Iterative vs one-shot

One-shot pruning (remove a big fraction at once) is fast but fragile.
Iterative
pruning removes a little, fine-tunes, and repeats, which reaches the
same
sparsity with much less accuracy loss. The trade is wall-clock time
versus
accuracy.

### Why it matters

Pruning without fine-tuning leaves accuracy on the floor; fine-tuning
without
pruning buys nothing. The two are a pair, and the recipe is what makes
pruning
viable in practice.

## 6. When Pruning Helps and Hurts

### When it helps

Pruning helps when the model is over-parameterized for the task — the
common
case — and the goal is smaller size or lower latency. It compounds with
quantization: a pruned INT8 model is small on both the redundancy and
precision
axes.

### When it hurts

Pruning hurts when the model is already small and well-fit, because
there is no
redundancy to remove without real accuracy loss. Pruning a tiny,
efficient model
is cutting into muscle, not fat.

## 7. Iterative Pruning in Detail

### The one-shot problem

Removing 90% of weights in a single step destroys too much structure at
once,
and the accuracy collapse is hard to recover from. One-shot pruning is
fast but
fragile, and it is the mistake most first attempts make.

### The iterative loop

Iterative pruning removes a small fraction (say 10%), fine-tunes to
recover,
and repeats until the target sparsity is reached. Each step cuts a
little and
lets the surviving weights adapt before the next cut. The same total
sparsity is
reached with far less accuracy loss, at the cost of several training
passes.

```python
for _ in range(n_rounds):
    prune.l1_unstructured(model, name="weight", amount=0.1)
    fine_tune(model)  # recover after this round's cut
```

### The cost-accuracy trade

Iterative pruning trades wall-clock time for accuracy — the same ladder
that
appears throughout this curriculum (zero-shot to fine-tune, PTQ to QAT).
When
the model is expensive to deploy, the extra fine-tuning passes are a
small price
for a smaller, still-accurate model.

## 8. Per-Layer Sensitivity

### Layers are not equal

Some layers tolerate heavy pruning; others — often the first and last,
or
bottleneck layers — collapse under it. A uniform cut ignores this and
hurts the
sensitive layers as much as the redundant ones. Global pruning (`3`)
addresses
this implicitly by finding least-important weights anywhere.

### The sensitivity-analysis approach

A more explicit method prunes each layer independently and measures the
accuracy
drop, producing a per-layer sensitivity curve. Layers that tolerate
pruning get
cut hard; sensitive layers are spared. This is the principled version of
"not
all layers are equal," and it is how you push sparsity further than a
uniform
cut allows.

### The practical default

Start with global magnitude pruning — it captures most of the per-layer
sensitivity benefit for free. Reach for explicit sensitivity analysis
only when
you need to push sparsity to the edge and the uniform/global cut is
hurting a
specific layer.

## 9. Combining Pruning with Quantization and Distillation

### The three levers

Compression has three orthogonal levers. **Pruning** removes redundant
weights.
**Quantization** shrinks the representation of the remaining weights.
**Distillation** transfers a big model's knowledge into a small one. They attack
different axes: redundancy, precision, and capacity. Because they are
orthogonal,
they compose — and the composition multiplies the size reduction.

### The pipeline order

The common order is distill → prune → quantize → fine-tune. Distill
first to get
a small, capable model (knowledge). Prune it to remove redundancy
(structure).
Quantize the result to shrink the representation (precision). Fine-tune
once at
the end to recover any accuracy lost along the way. Each step starts
from the
previous step's output.

### Why order matters

Quantizing before pruning means pruning a coarser representation, where
the
magnitude signal is noisier — so prune first. Distilling before pruning
means the
student inherits the teacher's redundancy, which pruning then removes —
so
distill first. The order is not arbitrary; each step assumes the prior
step's
output.

### The measurement at each step

Measure accuracy and size after *every* step, not just at the end. If a
step
costs more accuracy than it saves in size, drop it. The pipeline is a
sequence of
trades, and each trade must be justified on its own — the same
discipline as
every ablation in this curriculum.

## 10. When Pruning Fails and What to Do

### Failure 1: Accuracy collapse from over-pruning

Removing too much at once collapses accuracy beyond recovery. The fix is
iterative pruning (`7`) — smaller cuts with fine-tuning between — rather
than one
big cut.

### Failure 2: No speedup from unstructured sparsity

A sparse matrix without sparse-kernel support runs no faster. If speedup
is the
goal, switch to structured pruning (`1`) even at the cost of some
accuracy.

### Failure 3: Fine-tuning cannot recover

Sometimes the fine-tune does not bring accuracy back, which means the
pruned
structure was genuinely needed. The fix is to prune less, or to use
per-layer
sensitivity (`8`) to spare the critical layers.

### Failure 4: Pruning a model with no redundancy

A small, well-fit model has no fat to cut, and pruning it only removes
muscle.
The diagnostic is the baseline: if a same-sized model trained from
scratch
matches the pruned one, there was nothing to gain. Prune only where
over-parameterization is real.

## Real-World Application

- **Shrinking a model for a latency budget** — structured pruning to meet a
  serving SLO on a tight edge device.
- **Compounding with quantization** — prune the redundancy, then quantize the
  representation.
- **Finding winning tickets** — sparse subnetworks for deployment.
- **The DevMate case** — pruning a small classifier or embedding projection that
  is over-parameterized for its retrieval task.

## Common Mistakes to Avoid

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

### Mistake 6: Pruning an already-small, well-fit model
```
# WRONG — cutting into a compact model with no redundancy to spare
# CORRECT — prune only when over-parameterization is real
```

## Best Practices

1. Use magnitude (L1) pruning as the default criterion.
2. Prefer structured pruning when speedup is the goal.
3. Follow every prune with a short fine-tune pass.
4. Prune iteratively in small steps, not one big cut.
5. Use global pruning to respect per-layer sensitivity.
6. Report latency and memory, not just sparsity.
7. Keep the unpruned model for comparison and rollback.
8. Combine pruning with quantization for compounding wins.

## Complexity and Cost

| Operation | Time | Space | Notes |
|---|---|---|---|
| Unstructured prune | seconds | sparse | Max compression, uncertain speed |
| Structured prune | seconds | smaller dense | Real speedup, coarser |
| Fine-tune after prune | minutes | — | Recovers accuracy |
| Iterative pruning | N x prune+fine-tune | — | Best accuracy per sparsity |

## AI Engineering Relevance

**Where this shows up:** shrinking a model for a tight VRAM or latency budget.
On the RTX 5000, pruning is the lever you pull alongside quantization
when a
model is too big or too slow — and the structured/unstructured
distinction is
what decides whether the shrink actually makes it faster.

| Concept here | Used for |
|---|---|
| Structured pruning | Real, hardware-friendly speedup |
| Magnitude criterion | The default "what to remove" rule |
| Prune-then-fine-tune | Recovering accuracy after pruning |
| Lottery ticket | Why over-parameterized nets compress well |

**Scale note:** pruning pairs with quantization — a pruned INT8 model is smaller
and faster on both axes. The compression toolbox (quantize, prune,
distill) is
applied together, not in isolation.

## Key Takeaways

1. Unstructured pruning gives sparsity; structured pruning gives real speedup.
2. Magnitude (smallest |w| first) is the default criterion.
3. Global pruning respects per-layer sensitivity better than a uniform cut.
4. The lottery ticket says sparse subnetworks match dense nets.
5. Prune-then-fine-tune (iteratively) recovers accuracy.
6. Report latency and memory, not sparsity alone.

## Self-Check Questions

1. Why does unstructured sparsity not guarantee a speedup?
2. Why is magnitude a good default criterion for what to remove?
3. How does global pruning improve on a uniform per-layer cut?
4. What is the lottery-ticket hypothesis, and what does it imply?
5. Why is iterative pruning better than one-shot over-pruning?
6. Why should you report latency and memory rather than sparsity?

## Summary

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

## Further Reading / Connections

- `49-quantization-lecture.md` — the representation lever this pairs with.
- `51-distillation-lecture.md` — the knowledge lever of the compression toolbox.
- Frankle & Carbin, "The Lottery Ticket Hypothesis".
- Official docs: <https://pytorch.org/docs/stable/generated/torch.nn.utils.prune.l1_unstructured.html>

## Next Steps

Next: **[51 — Knowledge
Distillation](../advanced/51-distillation-lecture.md)** — compress a big
teacher into a small student.



