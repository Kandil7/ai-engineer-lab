# Knowledge Distillation — Glossary 51

Companion lecture: `51-distillation-lecture.md`

## Quick Reference Table

| Term | Category | One-Line Definition |
|---|---|---|
| Distillation | Technique | Train a small student to imitate a big teacher's soft outputs |
| Teacher | Model | The large, accurate model that provides the knowledge |
| Student | Model | The small model trained to match the teacher |
| Soft label | Target | The full per-class probability distribution |
| Hard label | Target | The one-hot ground-truth label |
| Temperature | Parameter | Softens logits to expose secondary structure |
| Dark knowledge | Concept | Information in the non-argmax probabilities |
| KL divergence | Loss | Measures the gap between two distributions |

## Detailed Definitions

### Distillation
**Definition**: Compressing a large, accurate teacher into a small student by
training the student on the teacher's softened output distributions rather than
hard labels alone.
**Example**:
```python
loss = F.kl_div(log_softmax(s / T), softmax(t / T), reduction="batchmean") * T * T
```
**Related**: Teacher, Student, Temperature

### Teacher / student
**Definition**: The teacher is the large model whose knowledge is transferred; the
student is the small model that inherits it and is deployed.
**Related**: Distillation, Soft label

### Soft label
**Definition**: The full probability vector over classes — the teacher's confidence
structure — carrying more signal per example than a one-hot hard label.
**Related**: Hard label, Dark knowledge

### Hard label
**Definition**: The one-hot ground truth — a single correct class, discarding the
confusability structure a soft label preserves.
**Related**: Soft label

### Temperature
**Definition**: The divisor applied to logits before softmax. `T > 1` softens the
distribution, exposing dark knowledge; `T = 1` is the ordinary softmax.
**Example**:
```python
torch.softmax(logits / T, dim=-1)
```
**Related**: Dark knowledge, Soft label

### Dark knowledge
**Definition**: The information in a teacher's non-argmax probabilities — which
classes are confusable — invisible to hard labels, and the substance of what
distillation transfers.
**Related**: Soft label, Temperature

### KL divergence
**Definition**: The divergence measuring how one distribution differs from
another, the loss used to match the student's softened output to the teacher's.
**Related**: Distillation, Temperature

## Key Concepts Summary

### The mechanism
- soft labels + temperature + KL divergence = distillation.

### The toolbox
- distill (knowledge) -> prune (redundancy) -> quantize (representation).

## Practice Terms

Match each term to its definition (answers at the bottom).

1. Train a small student to imitate a big teacher — ___
2. The large model providing knowledge — ___
3. The full per-class distribution — ___
4. The one-hot ground truth — ___
5. Softens logits to expose structure — ___
6. Information in non-argmax probabilities — ___
7. Divergence between two distributions — ___
8. The small model that is deployed — ___

**Answers:** 1-distillation, 2-teacher, 3-soft label, 4-hard label,
5-temperature, 6-dark knowledge, 7-KL divergence, 8-student
