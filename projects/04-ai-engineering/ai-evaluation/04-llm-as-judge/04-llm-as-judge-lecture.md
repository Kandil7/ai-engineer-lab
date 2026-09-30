# AI Evaluation 04: LLM-as-Judge

## Topic Overview

Some evaluation questions cannot be answered mechanically. "Is this claim supported by
this passage?" and "is this answer helpful?" are not string comparisons; they require
reading and judgment. A judge model answers them at scale: LLM-as-judge is the pattern
of using a model, with a rubric and a fixed set, to grade model output.

The danger is treating the judge as an oracle. Judges have known biases, they drift,
and they disagree with humans in ways that are invisible unless you measure. A judge
that is never validated is a second unreliable model whose errors are now baked into
your evaluation, which is worse than having no judge at all because it looks like
rigor.

This lecture covers judge design, the biases to expect, how to validate a judge
against human labels, when a judge is appropriate, and how the golden set anchors
everything. The judge is a scaling tool for human judgment, not a replacement for it.

## Learning Objectives

By the end of this lecture, you will be able to:

1. Design a judge prompt with a rubric, a scale, and a structured output format.
2. Name the judge's known biases and apply the matching mitigation.
3. Validate a judge against human labels and report its accuracy.
4. Decide when a judge is appropriate and when a human must verify.
5. Keep the judge anchored to the golden set and detect judge drift.
6. Account for the judge's own cost in the evaluation budget.

## Prerequisites

- AI Evaluation 01 (the golden set with human labels the judge is validated against).
- AI Evaluation 02 (faithfulness and citation precision) for the criteria a judge
  commonly scores.

---

## 1. What a Judge Is

### Definition

A judge is a model that grades output against a rubric. The judge prompt states the
criteria, the scale, and the output format. The structure is deterministic: the same
input, the same rubric, and the same format produce the same grade, so a regression is
visible.

```python
judge_prompt = """
Grade the answer against the rubric.
Criteria: faithfulness (0-1), helpfulness (0-1).
Output JSON: {"faithfulness": 0.9, "helpfulness": 0.8}
"""
```

### The exercise's stub judge

The exercise's `judge_grade` is a stand-in for a real judge: it grades faithfulness by
whether the answer cites a context passage and helpfulness by whether it answers at
all. It is deterministic and mechanical, which is exactly what makes it testable. A
real judge replaces the mechanic with a model but keeps the same interface: an answer
plus a rubric in, a structured grade out.

### Determinism is the point

A judge that returns a different grade for the same input is useless as a regression
signal. Temperature 0, a fixed rubric, and a structured output schema are not optional
for a judge used in CI.

## 2. Judge Design

### The rubric

The rubric is the criteria and the scale. It must be specific: "faithfulness" means
"every claim is supported by a cited passage", not "the answer is good". A vague rubric
lets the judge improvise criteria, and then you are measuring the judge's mood, not the
answer.

### Structured output

The judge returns a schema, not prose: `{"faithfulness": 0.9, "helpfulness": 0.8}`.
Structured output makes grades comparable across runs and machine-checkable, so a
regression gate can read them.

### One criterion per judgment

Asking one judge call to score five things at once invites interference between the
criteria. When the criteria are independent, score them separately or at least in a
fixed order with a fixed format.

## 3. Judge Bias

Judges have documented biases, and each has a mitigation:

- **Position bias.** The judge prefers whichever answer or passage appears first.
  Mitigation: randomize the order (and average over orderings) when comparing.
- **Verbosity bias.** The judge prefers longer answers, equating length with quality.
  Mitigation: cap length, or explicitly instruct the judge to ignore length.
- **Self-preference.** The judge prefers answers from its own model family. Mitigation:
  judge with a different model family than the one that answered.
- **Rubric drift.** The judge's interpretation of the rubric shifts over time or across
  prompt versions. Mitigation: pin the judge prompt version and re-validate after any
  change.

### Why naming the bias matters

A bias you cannot name is a bias you cannot correct. Listing them is the first control:
each review of the judge asks "could this score be a position or verbosity artifact?"
before it is trusted.

## 4. Validating the Judge Against Humans

### The rule

A judge is only as good as its agreement with humans. Run the judge and a human over
the same sample and measure agreement. A judge that disagrees with humans on
faithfulness is not measuring faithfulness, whatever its output claims.

```python
def judge_accuracy(judge_grades: list[float], human_grades: list[float]) -> float:
    """Fraction of judge grades within 0.25 of the human grade."""
    assert len(judge_grades) == len(human_grades)
    close = sum(1 for j, h in zip(judge_grades, human_grades) if abs(j - h) <= 0.25)
    return close / len(judge_grades)
```

### Reading the number

The exercise asserts that the judge agrees with the humans on at least 0.8 of the
sample, and that a judge which returns 1.0 for everything falls below that bar. The
second assertion is the important one: a judge that always agrees with itself but not
with humans fails the validation, no matter how confident it sounds.

### Judge accuracy is itself a metric

Track the judge's agreement with humans over time. A drop in agreement is a regression
in the evaluation stack, caught and fixed like any other, usually by tightening the
rubric or re-validating after a judge prompt change.

## 5. When a Judge Is Appropriate

### Appropriate

Judges fit rubric-based, comparative, and support-based questions at scale:

- **Rubric-based:** "does this answer cite the passage it relies on?"
- **Comparative:** "which of these two answers is better?" (with order randomized).
- **Support-based:** "is this claim supported by this passage?"

### Not appropriate

Judges are not appropriate for factual correctness on high-stakes answers, where a
human must verify. A judge can be wrong in the same way the answering model is wrong,
and a wrong judge on a high-stakes question launders an error into a passing score.

### The division of labor

The golden set carries the human-verified answers. The judge extends coverage beyond
that small set by grading many more answers against the same rubric. Human judgment
sets the standard; the judge scales the measurement of it.

## 6. The Golden Set Anchor and Judge Drift

### Anchored on the golden set

The judge grades the golden set, where the human answers are known. The judge's grades
are compared to the human grades, so judge accuracy is measured on the same fixed
yardstick as everything else. This is what keeps the judge honest.

### Detecting drift

If the judge's grades over the golden set start moving away from the human grades while
the system is unchanged, the judge has drifted. Drift is almost always caused by a judge
prompt change, a model version change, or a rubric re-reading. Pin the judge prompt and
model version so drift is attributable.

## 7. Cost and Calibration

### Cost

A judge call is a model call. Judging a large golden set is inexpensive; judging every
production answer is not. Budget the judge like any other inference cost, and track
cost per judged item the same way the answering model's cost is tracked.

### Calibration on a sample

Do not judge everything. Judge a sample, validate agreement with humans on a smaller
sample, and rely on the golden set plus the retrieval and faithfulness metrics for the
rest. The judge fills the gap where mechanical metrics cannot reach, not the whole
evaluation.

## Real-World Application

- Grading Athar answers for faithfulness when the mechanical citation check is
  ambiguous (partial support).
- Comparing two prompt variants by having the judge pick the better answer with the
  position randomized.
- Tracking the judge's agreement with human labels on the DevMate golden set as a
  first-class metric.
- Refusing to use a judge for a high-stakes factual claim that must be human-verified.

## Common Mistakes

1. **No rubric.** The judge improvises criteria and the score means nothing stable.
2. **Ignoring position and verbosity bias.** The judge rewards the first or the longest
   answer, not the best.
3. **Judging with the same model that answers.** Self-preference inflates its own
   family's scores.
4. **Never validating against humans.** Judge accuracy is unknown and untrusted.
5. **Running the judge on live traffic instead of the fixed set.** Results are not
   comparable across runs.
6. **Letting the judge prompt drift unversioned.** A score change cannot be attributed.
7. **Treating judge grades as ground truth for high-stakes answers.** A human must
   verify those.

## Key Takeaways

1. A judge grades output against a rubric, deterministically, with structured output.
2. Judges have position, verbosity, and self-preference bias; name each and mitigate it.
3. Validate the judge against human labels; judge accuracy is itself a metric.
4. Judges scale human judgment; they do not replace it, and never for high-stakes
   facts.
5. The judge grades the fixed golden set so drift is attributable, and its cost is
   budgeted like any other inference.

## Self-Check Questions

1. Why must a judge return structured output rather than prose?
2. Name three judge biases and one mitigation for each.
3. A judge returns 1.0 for every faithfulness grade. Why does it fail validation
   against humans even though it is consistent?
4. Give one evaluation question a judge should answer and one a human must.
5. How would you detect that the judge has drifted?

## Further Reading / Connections

- AI Evaluation 01 (gold datasets and annotation) — the human labels that validate the
  judge.
- AI Evaluation 02 (faithfulness and citation precision) — the criteria a judge most
  often scores.
- AI Evaluation 06 (eval in CI) — where the judge gate runs on every change.
- `docs/reference/llm-production-architecture.md` — the evaluation and guardrails
  sections.
