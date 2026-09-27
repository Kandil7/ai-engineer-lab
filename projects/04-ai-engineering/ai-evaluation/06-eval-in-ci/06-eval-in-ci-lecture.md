# AI Evaluation 06: Eval in CI

## 🎯 Topic Overview

An evaluation that never runs is a document, not a gate. The golden set,
the adversarial set, and the judge all run in CI on every change, with
thresholds that fail the build. This lecture covers the eval harness, the
thresholds, and the discipline of treating evaluation as part of the
pipeline, not an afterthought.

## 📚 Learning Objectives

By the end of this lecture, you will be able to:

1. Build an eval harness that runs the golden and adversarial sets
2. Set thresholds from a baseline and enforce them
3. Compare a change against the baseline, not in isolation
4. Report metrics so a regression is visible at a glance
5. Treat evaluation as a CI discipline

---

## 1. The Eval Harness

The harness is a script that runs the golden set and the adversarial set,
computes the metrics, and compares them to the baseline. It is deterministic:
same code, same sets, same thresholds, same verdict. The harness is the
single entry point — one command runs the whole evaluation.

```python
# one command, one verdict
python eval/run_eval.py --golden eval/golden.jsonl --adversarial eval/adversarial.jsonl
```

## 2. Thresholds from a Baseline

Every metric has a floor set from a baseline run. The baseline is captured
once, reviewed, and then enforced. A change that drops recall@5 below the
floor fails CI. Thresholds without a baseline are guesses; a baseline
without enforcement is a document.

## 3. Change vs Baseline

A change is judged against the baseline, not in isolation. A new chunker
that scores 0.9 recall@5 is good only if the baseline was 0.8. The eval
report shows the delta: metric, baseline, current, verdict. The roadmap's
exit test: "every change is evaluated against the baseline."

## 4. The Report

The report is a table: metric, baseline, current, delta, verdict. A
regression is visible at a glance — recall@5 down, faithfulness down,
resistance down. The report is the artifact of the eval run, committed
alongside the change.

## 5. The Discipline

Evaluation is part of the pipeline, not an afterthought. Every change that
touches the prompt, the retriever, the chunker, or the guardrails runs the
harness. A change that improves one metric and degrades another is a
tradeoff to be made explicitly, with the report as evidence.

## Common Mistakes

- An eval harness that never runs in CI.
- Thresholds without a baseline.
- Judging a change in isolation.
- No report (regressions invisible).
- Evaluation as a one-off after the work is done.

## Key Takeaways

1. The harness is one deterministic command.
2. Thresholds come from a baseline and are enforced.
3. A change is judged against the baseline.
4. The report makes regressions visible at a glance.
5. Evaluation is part of the pipeline, not an afterthought.