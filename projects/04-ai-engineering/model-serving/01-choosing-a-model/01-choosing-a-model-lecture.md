# Model Serving 01: Choosing a Model

## Topic Overview

Choosing a model is a tradeoff across four axes (capability, cost, latency, and
license), and the tradeoff is decided by the task, not by benchmarks on a leaderboard.
The biggest model is rarely the right answer: it is slower, more expensive, and often
not better at the specific task you have. The right answer is the smallest model that
clears the quality bar you can measure.

This lecture covers the four axes, how the task narrows the candidates before any
evaluation, how to score the shortlist on the golden set, and why the choice belongs
in an ADR. It also covers the constraint that decides many real choices: the cost
budget. A model that is excellent but exceeds the per-request budget is not a
candidate, it is an aspiration.

Model choice is not permanent. Models change, tasks change, and budgets change, so the
decision records when it should be revisited. Once chosen, the model sits behind an
interface so that replacing it is a configuration change, not a rewrite.

## Learning Objectives

By the end of this lecture, you will be able to:

1. Compare models on capability, cost, latency, and license.
2. Use the task to narrow the candidate list before evaluating.
3. Evaluate the shortlist on the golden set and pick the winner.
4. Apply a cost budget as a hard constraint, not an afterthought.
5. Record the choice and the rationale as an ADR.
6. State the triggers that reopen the decision.

## Prerequisites

- AI Evaluation 01 (the golden set) and 03 (the metrics used to score candidates).
- Cost and latency awareness from Model Serving 02 and 03.

---

## 1. The Four Axes

| Axis | Question | Failure if ignored |
| --- | --- | --- |
| **Capability** | Does it solve the task? | Wrong answers, or a task it cannot do |
| **Cost** | What does it cost per token or per request? | The bill scales past the budget |
| **Latency** | How fast is the first token and the full response? | Users abandon slow answers |
| **License** | May we use it, how, and where? | A legal or terms-of-service problem |

The choice is a tradeoff across all four. Optimizing capability alone produces an
expensive, slow system; optimizing cost alone produces a cheap, wrong one.

### Capability is task-specific

Capability is not a single number. A model that tops a general benchmark may be weak on
Arabic, or on code, or on long-context reasoning. Evaluate capability on your task, not
on the leaderboard, which is why the golden set from AI Evaluation 01 comes first.

### License and location

A permissive open license allows self-hosting and modification; a proprietary API
license may forbid storing outputs or using them to train other models. The license
also interacts with where the data goes: sending private data to a third-party API is a
different decision from running a model on your own GPU.

## 2. Matching the Task to the Model

Before evaluating anything, use the task to cut the candidate list:

- A **coding** task needs a code-capable model.
- A **multi-step reasoning** task needs a model that chains steps reliably.
- An **Arabic** task needs a multilingual or Arabic-specific model that does not
  tokenize Arabic into fragments.
- A **high-volume, low-complexity** task (classification, extraction) needs a small,
  cheap model, not a frontier model.

### Why the narrowing matters

Evaluation is expensive in time and tokens. Narrowing on clearly disqualifying
properties (no Arabic support, no tool calling, wrong license) leaves a shortlist that
is worth scoring. Evaluating twenty candidates when three were viable wastes the
budget the evaluation itself spends.

### The small-model-first heuristic

Start with the smallest model that could plausibly work and move up only when the
golden set says it fails. Many teams pay for a frontier model for a task a 7B model
handles at a fraction of the cost and latency. Let the measurement, not the habit,
decide.

## 3. Evaluation on the Golden Set

### The procedure

Run each candidate on the same golden set, score the outputs with the same metrics, and
compare against the baseline. The exercise models the scoring directly:

```python
def evaluate(candidate: dict, golden: list[dict]) -> float:
    """Score a candidate on the golden set."""
    correct = 0
    for case in golden:
        if candidate["answer_fn"](case["query"]) == case["expected"]:
            correct += 1
    return correct / len(golden)
```

### What to score

Score both answer quality (does it answer correctly) and the operational metrics that
matter (latency, token cost). A candidate that is marginally more accurate but three
times slower and five times more expensive is usually not the winner.

### Same set, same metrics

Every candidate sees the same queries and is scored by the same metrics. A comparison
across different sets or metrics measures the setup, not the models (this is the
retrieval exit-test discipline applied to model choice).

## 4. The Cost Budget Constraint

### The budget is a hard filter

The budget is not a tiebreaker; it is a constraint. The exercise filters candidates by
cost first, then picks the best among those within budget:

```python
def choose(candidates: list[dict], golden: list[dict], budget: float) -> str:
    """Pick the best-scoring candidate within the cost budget."""
    within = [c for c in candidates if c["cost"] <= budget]
    return max(within, key=lambda c: evaluate(c, golden))["name"]
```

When the budget is 0.10, the good candidate (0.05) wins over the expensive one (0.50).
When the budget drops to 0.02, only the cheap candidate qualifies, and it wins by
default even though it scores lower. Budget decides the candidate set; quality decides
the winner within it.

### Cost per useful answer

A better cost metric than cost per token is cost per useful answer, which folds in
retries, failures, and the tokens spent by a wrong answer that has to be redone. A
model that is cheap per token but often wrong can be expensive per answer.

## 5. The ADR

### What it records

The choice is recorded as an ADR: the problem, the candidates considered, the metrics
measured, the chosen model, the rationale, and the re-evaluation trigger. The ADR is
the evidence that the choice was deliberate and measured, not a default.

### Why it matters later

Six months on, a new engineer asks "why this model?". The ADR answers with numbers:
"candidate A scored recall 0.81 on the golden set at cost 0.04, candidate B scored 0.83
at cost 0.30, so A was chosen." Without the ADR the answer is a shrug, and the model
gets changed on vibes.

### It is a decision, not a preference

A weak ADR ("we used model X because it is popular") fails review. The ADR must tie the
choice to the measured drivers.

## 6. Re-Evaluation Triggers

The choice is re-evaluated when:

- **The task changes** (new query types, new languages, new output requirements).
- **The corpus changes** (the golden set is regenerated for a larger or different
  corpus).
- **A better model is released** that changes the capability/cost frontier.
- **The budget changes** upward or downward.
- **The measured quality drifts** in production (AI Evaluation 07).

Re-evaluation runs the same golden set so the comparison is fair across time. A new
model's headline improvement is not a reason to switch until it wins on your set.

## Real-World Application

- Choosing a small multilingual model for Athar answer generation after the golden set
  shows a frontier model's quality edge is within the error bars.
- Selecting the cheapest model that clears the faithfulness bar for DevMate's
  extraction tasks.
- Recording the choice in `docs/decisions/` so a future model swap is a deliberate,
  measured change.
- Re-running the golden set when a new model version is released.

## Common Mistakes

1. **Choosing the largest model.** Cost and latency are ignored; the quality gain may
   be within noise.
2. **No golden-set evaluation.** The choice is a guess dressed as a decision.
3. **No ADR.** The choice is invisible and gets reversed on vibes.
4. **Ignoring the budget.** The model is excellent and unaffordable.
5. **Choosing without matching the task.** A general model on an Arabic or code task
   underperforms.
6. **Never re-evaluating.** The system is stuck on a model the frontier has passed.
7. **Comparing on different sets or metrics.** The comparison is meaningless.

## Key Takeaways

1. Four axes: capability, cost, latency, license; the tradeoff is task-driven.
2. The task narrows the candidates before evaluation; start small and move up only if
   the golden set says to.
3. Score the shortlist on the same golden set with the same metrics.
4. The budget is a hard constraint that defines the candidate set; quality picks the
   winner within it.
5. Record the choice and its triggers as an ADR, and re-evaluate on change.

## Self-Check Questions

1. Why is a leaderboard score a poor proxy for capability on your task?
2. The budget drops so only the cheap candidate qualifies, and it scores lower. Which
   model do you ship, and why?
3. What does the ADR for a model choice need to contain to be useful in six months?
4. Name two triggers that should reopen the model decision.
5. Why is cost per useful answer a better cost metric than cost per token?

## Further Reading / Connections

- AI Evaluation 01 (gold datasets) and 03 (retrieval evaluation) — the set and metrics
  used to score candidates.
- Model Serving 02 (self-hosted models) and 04 (HF Inference SDK) — the deployment
  options a chosen model runs on.
- `docs/decisions/` — where the model-choice ADR lives.
- `docs/reference/llm-production-architecture.md` — the model-selection and cost
  sections.
