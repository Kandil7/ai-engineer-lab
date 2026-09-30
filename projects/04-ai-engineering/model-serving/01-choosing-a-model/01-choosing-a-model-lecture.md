# Model Serving 01: Choosing a Model

## 🎯 Topic Overview

Choosing a model is a tradeoff across capability, cost, latency, and
license. This lecture covers the decision axes and the evaluation
discipline.

## 📚 Learning Objectives

By the end of this lecture, you will be able to:

1. Compare models on capability, cost, latency, and license
2. Match the model to the task
3. Evaluate candidates on the golden set
4. Document the choice as an ADR
5. Re-evaluate when the task changes

---

## 1. The Axes

Models differ on capability (how well they solve the task), cost (per
token), latency (time to first token), and license (open vs proprietary).
The choice is a tradeoff, not a preference. The roadmap's exit test: "the
model is chosen deliberately."

| Axis | Question |
|------|----------|
| Capability | Does it solve the task? |
| Cost | What does it cost per token? |
| Latency | How fast does it respond? |
| License | Can we use it? |

## 2. Matching the Task

A coding task needs a code-capable model. A reasoning task needs a model
that chains steps. An Arabic task needs a multilingual model. The task
narrows the candidates. The roadmap's exit test: "the model matches the
task."

## 3. Evaluation on the Golden Set

Candidates are evaluated on the golden set: the same queries, scored
output, compared metrics. The best-scoring candidate wins. The roadmap's
exit test: "candidates are evaluated on the golden set."

## 4. The ADR

The choice is recorded as an ADR: the problem, the candidates, the chosen
model, the rationale, and the re-evaluation trigger. The ADR is the
evidence the choice was deliberate. The roadmap's exit test: "the choice
is documented as an ADR."

## 5. Re-Evaluation

The choice is re-evaluated when the task changes, the corpus grows, or a
better model is released. The re-evaluation runs the same golden set.

## Common Mistakes

- Choosing the largest model (cost ignored).
- No golden-set evaluation.
- No ADR (the choice is invisible).
- Never re-evaluating.
- Choosing without matching the task.

## Key Takeaways

1. Four axes: capability, cost, latency, license.
2. The task narrows the candidates.
3. The golden set evaluates the candidates.
4. The ADR records the choice.
5. Re-evaluate on change.