# 07-machine-learning — 51: Knowledge Distillation — A Big Teacher Teaches a Small Student

Companion exercise: `51-distillation.py`

---

## Topic Overview

A large model is accurate but expensive to serve; a small model is cheap but
weak. Knowledge distillation bridges the gap: you train a large **teacher**, then
train a small **student** to imitate the teacher's *soft predictions*, not just
the hard labels. The student inherits the teacher's confidence structure — that a
"3" is also a bit like an "8", or that one answer is "mostly right but close to
another" — which carries far more signal per example than a one-hot label.

The mechanism is a temperature-softened distribution. The teacher's logits are
divided by a temperature `T` and passed through softmax; the student is trained
to match that softened distribution with a KL-divergence loss. The temperature
controls how much of the teacher's *dark knowledge* — the information in the
non-max probabilities — is exposed to the student.

Distillation is the third tool of the compression toolbox, alongside
quantization (`49`) and pruning (`50`). It is also how large language models are
compressed into smaller ones — GPT teacher, small student — and how a heavy model
becomes deployable on a phone or a 16 GB GPU. The exercise trains a tiny teacher
and student so the temperature, soft labels, and KL loss are concrete.

## Learning Objectives

By the end of this lecture, you will be able to:

1. Explain why soft labels carry more information than hard labels.
2. Define the temperature parameter and what softening does.
3. Write the distillation loss (KL divergence on temperature-scaled logits).
4. Explain "dark knowledge" and why it transfers.
5. Compare distillation to training a student on hard labels alone.
6. Choose teacher and student architectures for a distillation job.
7. Reason about distillation's role alongside quantization and pruning.
8. State when distillation is worth the extra engineering.

## Prerequisites

| Need | Where |
|---|---|
| Neural network basics | `38-neural-network-basics.py` |
| Training loop | `37-pytorch-training-loop.py` |
| Softmax / cross-entropy | `38-neural-network-basics.py` |

## 1. Soft Labels vs Hard Labels

### The information difference

A hard label says "this is a 3, and nothing else." A soft label says "this is a 3,
but somewhat like an 8, and slightly like a 5." That secondary structure — which
classes are confusable — is what a student needs to generalize, and it is exactly
what a hard label throws away.

### The analogy

A student learning from an expert learns not just the expert's final answer but
the expert's *reasoning and confidence* — "I'm sure it's A, but B is plausible."
Distillation is the same: the teacher's per-class probabilities are its reasoning,
and the student learns them, not just the argmax.

### Why it matters per example

A hard label gives one bit of signal per example (the correct class). A soft
label gives a full distribution — hundreds of numbers describing the class
relationships. That is why a student trained on soft labels can match a teacher
with far less data and capacity than it would need otherwise.

## 2. Temperature Softening

### What the temperature does

The teacher's raw logits are often sharp — the correct class is near 1.0 and the
rest near 0.0, which hides the subtle "3 is like 8" signal. Dividing by a
temperature `T > 1` softens the distribution, exposing that structure:

```python
def soften(logits, T):
    return torch.softmax(logits / T, dim=-1)
```

At `T = 1` the distribution is the ordinary softmax; at high `T` it flattens
toward uniform; at `T < 1` it sharpens. Distillation uses a high `T` on both
teacher and student during training, then serves the student at `T = 1`.

### Why soften both

The student and teacher distributions are compared at the same temperature so
their shapes align. The temperature is a *signal amplifier* for the dark
knowledge — high enough to expose it, not so high as to wash it out into noise.

## 3. Dark Knowledge

### What the term means

"Dark knowledge" (Hinton et al.) is the information in the teacher's non-argmax
probabilities — the parts of the distribution a hard label never shows. A teacher
that outputs `[0.9, 0.08, 0.02]` for a "3" is saying "8 is more likely than 5"
even though both are wrong, and that ordering is the dark knowledge.

### Why it transfers

That ordering reflects the true geometry of the problem — which mistakes are
plausible — and it generalizes better than a one-hot. The student learns the
teacher's full confusion structure, not just the decision boundary.

## 4. The Distillation Loss

### KL divergence on soft targets

The student is trained to minimize the KL divergence between its softened
distribution and the teacher's:

```python
soft_teacher = soften(teacher(x), T)
soft_student = F.log_softmax(student(x) / T, dim=-1)
loss = F.kl_div(soft_student, soft_teacher, reduction="batchmean") * T * T
```

The `T * T` factor rescales the gradient to match the temperature-scaled
magnitude. Optionally, a hard-label term is added — a weighted sum of the
distillation loss and the standard cross-entropy — to keep the student anchored
to the ground truth.

### The code shape

The two terms are often combined:

```text
loss = alpha * (T^2 * KL) + (1 - alpha) * CE(hard_labels)
```

`alpha` balances imitating the teacher versus fitting the data.

## 5. Distillation vs Training From Scratch

### The gap it closes

A small student trained on hard labels alone underfits the subtle structure. The
same student trained on the teacher's soft labels matches the teacher's behavior
much more closely, because the soft labels compress the teacher's knowledge into
a form a small model can absorb.

### The measurement

The comparison is: student-from-scratch accuracy versus student-from-distillation
accuracy, on the same held-out set. Distillation should close most of the gap
between the student's naive accuracy and the teacher's accuracy.

## 6. Choosing Teacher and Student

### The architectures

The teacher is typically a large, accurate model — an ensemble or a big network.
The student is a small model chosen to fit the deployment budget. The gap in
capacity is the whole point: the student inherits what the teacher knows without
the teacher's size.

### The practical rules

The teacher must be well-trained first; the student must be large enough to
express the teacher's soft structure but small enough to serve. Distillation
works best when the teacher is much better than a same-sized student trained from
scratch — the bigger the teacher advantage, the more there is to transfer.

## 7. Distillation in the Compression Toolbox

### The three tools

Quantization shrinks the *representation* of one model; pruning removes
*redundant* parts of one model; distillation transfers a *big model's* knowledge
into a *small model*. They are orthogonal and combine: distill to a small
student, then quantize and prune the student.

### The production pipeline

The common order is: distill (get a small, capable model) → prune (drop the
redundancy) → quantize (shrink the representation) → fine-tune (recover any lost
accuracy). Each step builds on the last, and the final artifact is a fraction of
the teacher's size.

## 8. Common Mistakes to Avoid

### Mistake 1: Training the student on hard labels and calling it distillation
```
# WRONG — a small student on one-hot labels; no teacher, no soft targets
# CORRECT — KL divergence against the teacher's softened logits
```

### Mistake 2: Too high a temperature
```
# WRONG — T = 100 washes the distribution into uniform noise
# CORRECT — a moderate T (2-10) exposes dark knowledge without destroying it
```

### Mistake 3: Forgetting the T^2 gradient factor
```
# WRONG — dropping the T*T rescale makes the distillation loss the wrong magnitude
# CORRECT — scale the KL term by T^2 (or use the combined alpha loss correctly)
```

### Mistake 4: Serving the student at training temperature
```
# WRONG — serving with T > 1, which flattens confidence and hurts calibration
# CORRECT — train at T > 1, serve at T = 1
```

### Mistake 5: A weak teacher
```
# WRONG — distilling from a teacher that is barely better than the student
# CORRECT — the teacher must be meaningfully better, or there is nothing to learn
```

### Mistake 6: Ignoring the hard-label anchor entirely
```
# WRONG — pure soft-label distillation drifting from the ground truth
# CORRECT — a small hard-label term (alpha < 1) keeps the student honest
```

## 9. Best Practices

1. Train the teacher first, and keep its weights frozen during distillation.
2. Use a moderate temperature (2-10) and tune it.
3. Match the student and teacher at the same temperature during training.
4. Combine the KL loss with a small hard-label cross-entropy term.
5. Serve the student at T = 1.
6. Use log-softmax on the student side and softmax on the teacher side in KL.
7. Pick a student just large enough to express the teacher's soft structure.
8. Measure student-from-scratch as the baseline, not just the teacher.
9. Distill to a small model, then quantize and prune it.
10. Record the temperature, alpha, and teacher architecture for reproducibility.

## 10. Complexity and Cost

| Operation | Time | Space | Notes |
|---|---|---|---|
| Train teacher | long | large | One-time; often a pretrained model |
| Distillation | one student-training pass | small | Soft labels per example |
| Serve student | fast | small | The point of the exercise |
| Combined toolbox | distill + prune + quantize | smallest | Compounding wins |

## 11. AI Engineering Relevance

**Where this shows up:** compressing a large model for deployment — the classic
case is taking a big ensemble or LLM and producing a small, fast student. On the
RTX 5000's 16 GB, distillation is how you run a "big model's" behavior through a
student that actually fits, and it is the standard route for on-device models.

| Concept here | Used for |
|---|---|
| Soft labels | Compressing the teacher's knowledge |
| Temperature | Exposing dark knowledge |
| KL loss | Matching distributions, not just argmax |
| Toolbox | Distill -> prune -> quantize |

**Scale note:** distillation is the *knowledge* half of compression — it reduces
the model's capacity need, where quantization and pruning reduce its footprint.
Together they are how a 7B teacher becomes a 1B student that still behaves well.

## 12. Summary

| Concept | Description |
|---|---|
| Soft labels | Full per-class distribution, not one-hot |
| Temperature | Softens logits to expose dark knowledge |
| Dark knowledge | Information in the non-argmax probabilities |
| Distillation loss | KL divergence on temperature-scaled logits |
| Toolbox | Distill -> prune -> quantize -> fine-tune |

## Quick Reference

| Task | Idiom |
|---|---|
| Soften | `softmax(logits / T, dim=-1)` |
| Distillation loss | `F.kl_div(log_softmax(s/T), softmax(t/T), reduction="batchmean") * T*T` |
| Combined loss | `alpha * KL + (1 - alpha) * CE` |
| Serve | student at `T = 1` |

## Self-Check Questions

1. Why does a soft label carry more signal per example than a hard label?
2. What does the temperature do, and why soften both teacher and student?
3. What is dark knowledge, and why does it transfer?
4. Why is the KL loss scaled by T²?
5. Why serve the student at T = 1 when it was trained at T > 1?
6. How do distillation, pruning, and quantization compose into one pipeline?

## Further Reading / Connections

- `49-quantization-lecture.md` — shrink the representation after distilling.
- `50-pruning-lecture.md` — drop the redundancy after distilling.
- `39-transfer-learning-lecture.md` — the pretrained-teacher sibling pattern.
- Hinton, Vinyals, Dean — "Distilling the Knowledge in a Neural Network."

## Next Steps

This completes the model-optimization trio (49-51). Continue to
**[36 — PyTorch Tensors](../deep-learning/36-pytorch-tensors-lecture.md)** to revisit the foundations, or
**[model-serving](../../../04-ai-engineering/model-serving/)** to deploy the compressed model.

Official docs: <https://pytorch.org/docs/stable/generated/torch.nn.functional.kl_div.html>
