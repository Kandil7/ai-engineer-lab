# AI Evaluation 04: LLM-as-Judge

## 🎯 Topic Overview

Some evaluation questions cannot be answered mechanically — is this claim
supported by this passage? Is this answer helpful? A judge model answers
them at scale. LLM-as-judge is the pattern of using a model to grade model
output, with a rubric, on a fixed set. This lecture covers judge design,
judge bias, and when the judge is trustworthy.

## 📚 Learning Objectives

By the end of this lecture, you will be able to:

1. Design a judge prompt with a rubric and structured output
2. Detect the judge's biases (position, verbosity, self-preference)
3. Validate the judge against human labels
4. Choose when a judge is appropriate and when it is not
5. Use the judge on the golden set, not on live traffic

---

## 1. What a Judge Is

A judge is a model that grades output against a rubric. The judge prompt
states the criteria, the scale, and the output format. The judge is
deterministic in structure — same input, same rubric, same grade — so
regressions are visible. The roadmap's exit test: "a judge model grades
the golden set."

```python
judge_prompt = """
Grade the answer against the rubric.
Criteria: faithfulness (0-1), helpfulness (0-1).
Output JSON: {"faithfulness": 0.9, "helpfulness": 0.8}
"""
```

## 2. Judge Bias

Judges have known biases. Position bias: the judge prefers the first
answer. Verbosity bias: the judge prefers longer answers. Self-preference:
the judge prefers answers from its own family of models. Mitigations:
randomize order, cap length, use a different model family for judging than
for answering.

## 3. Validating the Judge

A judge is only as good as its agreement with humans. Run the judge and a
human over the same sample; measure agreement. A judge that disagrees with
humans on faithfulness is not measuring faithfulness. The judge is a
scaling tool for human judgment, not a replacement for it.

## 4. When a Judge Is Appropriate

Judges are appropriate for rubric-based, comparative, and support-based
questions at scale. They are not appropriate for factual correctness on
high-stakes answers, where a human must verify. The golden set carries the
human-verified answers; the judge extends coverage beyond it.

## 5. The Golden Set Anchor

The judge grades the golden set, where the human answers are known. The
judge's grades are compared to the human grades — judge accuracy is itself
a metric. A judge that drifts (grades drift from human grades) is a
regression in the evaluation stack, caught like any other.

## Common Mistakes

- No rubric (the judge improvises criteria).
- Ignoring position and verbosity bias.
- Judging with the same model that answers (self-preference).
- Never validating the judge against humans.
- Running the judge on live traffic instead of the fixed set.

## Key Takeaways

1. A judge grades output against a rubric, deterministically.
2. Judges have position, verbosity, and self-preference bias.
3. Validate the judge against human labels.
4. Judges scale human judgment; they do not replace it.
5. The judge grades the golden set, and its own accuracy is measured.