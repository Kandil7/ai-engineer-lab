# Prompt Engineering 04: Prompt Evaluation

## Topic Overview

A prompt is a hypothesis until it is measured. The instinct to judge a prompt by how it reads is
wrong; a prompt that reads well can score poorly, and a prompt that reads awkwardly can score
higher. Prompt evaluation runs the prompt against fixed test cases, scores the output against
metrics, and compares variations, so the choice is evidence rather than taste.

This lecture covers building test cases from real inputs, scoring against metrics, comparing
variations on the same cases, selecting the best-performing prompt, and monitoring in production.
The discipline is identical to the rest of the evaluation stack: fixed set, fixed metrics,
measured comparison, regression gate.

The most important habit is comparing prompts on the same cases with the same metrics. A prompt
that looks better on the developer's favorite example may be worse on the distribution, and only
the fixed set reveals it.

## Learning Objectives

By the end of this lecture, you will be able to:

1. Build test cases from real inputs.
2. Score output against explicit metrics.
3. Compare prompt variations on the same cases.
4. Select the best-performing prompt by score, not by reading.
5. Monitor the prompt in production with a feedback loop.
6. Gate prompt changes like any other change.

## Prerequisites

- Prompt Engineering 01 to 03 for the techniques being evaluated.
- AI Evaluation 01 (golden set) and 04 (LLM-as-judge) for the scoring machinery.

---

## 1. The Test Cases

### From real inputs

Test cases come from real inputs: user queries, edge cases, and the inputs that broke previous
versions. Each case has an expected behavior:

```python
cases = [
    {"input": "ما هو العدد الأولي", "expected": "a number with two divisors"},
    {"input": "Explain ice.", "expected": "density + hydrogen bonding"},
]
```

### Why fixed

The cases are fixed, so variations are compared on the same inputs. A moving case set measures
the set, not the prompt. This is the golden-set discipline applied to prompt evaluation.

### Coverage

The cases cover the input distribution and its edge cases, including the hard cases and the
adversarial ones. A set of easy cases makes every prompt look good.

## 2. The Metrics

### Explicit metrics

The output is scored against explicit metrics, each with a target:

| Metric | Target |
| --- | --- |
| Accuracy | > 95% |
| Relevance | > 90% |
| Helpfulness | > 85% |
| Clarity | > 90% |

### How to score

Mechanical metrics (exact match, schema validity, citation presence) are scored in code. Subjective
metrics (helpfulness, clarity) use a judge model validated against humans (AI Evaluation 04). The
combination covers both the checkable and the judgmental parts of quality.

### The metric must match the task

A prompt for extraction is scored on accuracy and schema validity; a prompt for explanation is
scored on relevance and clarity. Scoring a task on the wrong metric mis-ranks the variations.

## 3. Comparing Variations

### The same cases

Variations are compared on the same test cases: the same input, different prompts, scored output:

```python
assert score(v1, cases) == 0.5
assert score(v2, cases) == 1.0
```

### One change at a time

Change one thing between variations (the examples, the format, the reasoning instruction) so the
delta is attributable. Changing several things at once confounds the comparison, exactly as in
experiment design.

### The noise problem

Model output is stochastic. Run each variation several times or at temperature 0, and compare
aggregates, not single samples. A one-sample difference between prompts is usually noise.

## 4. Selecting the Best

### By score, not by reading

The best prompt is the one that scores highest on the metrics, not the one that reads best:

```python
assert select([v1, v2], cases) == "v2"
```

### Why this is hard to accept

Developers have intuition about prompts, and intuition is often right about obvious failures. It
is often wrong about close calls, which is precisely where the measurement matters. The rule is to
let the score decide the close calls and use intuition to generate the variations.

### The baseline

The current prompt is the baseline; a variation must beat it to replace it. "Different" is not
"better".

## 5. Production Monitoring

### The feedback loop

The selected prompt is monitored in production with a feedback loop (AI Evaluation 07): user
feedback, failure cases, and the rolling quality metric. A prompt that degrades in production is
re-evaluated.

### Why production differs from the test set

The test set is a sample; production is the distribution. A prompt can pass the golden set and meet
inputs the set did not anticipate. Monitoring catches the gap, and those inputs become new test
cases.

### The regression gate

Prompt changes run the evaluation in CI (AI Evaluation 06), so a change that lowers the metrics
fails the build. A prompt is a versioned artifact like code.

## 6. The Versioning Discipline

### Versioned prompts

Prompts are versioned (Prompt Engineering 01): each version is recorded, and the version is part
of the cache key and the trace. A prompt change is a tracked event, not a silent edit.

### Why it matters

Without versioning, a quality change cannot be attributed to a prompt change, and a rollback is
impossible. Versioning is what makes the evaluation meaningful over time.

## Real-World Application

- Comparing three prompt variants for the Athar answer format on the same golden cases and
  selecting the highest-scoring one.
- Using a validated judge for the helpfulness metric and mechanical checks for citation presence.
- Running each variation multiple times to separate a real gain from sampling noise.
- Gating a prompt change on the evaluation in CI so a regression cannot merge.

## Common Mistakes

1. **No test cases.** Quality is assumed.
2. **Scoring without a rubric.** The metric is undefined.
3. **Comparing variations on different inputs.** The comparison is meaningless.
4. **Choosing the prompt that reads best.** Close calls go to intuition over evidence.
5. **One sample per variation.** The difference may be noise.
6. **No production monitoring.** The set-versus-distribution gap is invisible.
7. **Unversioned prompts.** Changes cannot be attributed or rolled back.

## Key Takeaways

1. Test cases come from real inputs and are fixed, so variations compare on the same set.
2. Output is scored against explicit metrics, mechanical where possible and judge-based where
   necessary.
3. Variations change one thing at a time and are compared on aggregates, not single samples.
4. The best prompt is the best-scoring one; intuition generates variations, measurement selects.
5. Prompts are versioned, monitored in production, and gated in CI like any other artifact.

## Self-Check Questions

1. Why must the test cases be fixed across variations?
2. How do you score a subjective metric like helpfulness without trusting the judge blindly?
3. Why change only one thing between variations?
4. Why is one sample per variation unreliable?
5. Why must a prompt be versioned for the evaluation to be meaningful?

## Further Reading / Connections

- Prompt Engineering 01 to 03 — the techniques being compared.
- AI Evaluation 04 (LLM-as-judge) — scoring the subjective metrics.
- AI Evaluation 06 (eval in CI) — the gate that runs the comparison.
- `evaluations/prompts/golden-cases/` — where prompt golden cases live.
