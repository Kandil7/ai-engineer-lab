# AI Evaluation 06: Eval in CI

## Topic Overview

An evaluation that never runs is a document, not a gate. The golden set, the
adversarial set, and the judge are only useful if they run on every change and can
fail the build. This lecture is about turning evaluation from an occasional report
into a permanent part of the pipeline.

The center of it is a harness: one deterministic command that runs the sets, computes
the metrics, compares them to a baseline, and returns a verdict. The thresholds come
from a captured baseline, not from guesswork. A change is judged against that baseline,
and the report shows the delta so a regression is visible at a glance.

The discipline matters more than the tooling. If the harness runs only when someone
remembers, the regressions it would catch ship anyway. Evaluation in CI is what keeps
the system from silently getting worse one reasonable-looking change at a time.

## Learning Objectives

By the end of this lecture, you will be able to:

1. Build an eval harness that runs the golden and adversarial sets and returns a
   verdict.
2. Capture a baseline and derive thresholds from it.
3. Judge a change against the baseline, not in isolation.
4. Produce a report that makes regressions and tradeoffs explicit.
5. Wire the harness into CI so a regression fails the build.
6. Explain how this maps to the roadmap exit test.

## Prerequisites

- AI Evaluation 01 (the golden set) and 05 (the adversarial set).
- Basic familiarity with running a script and reading its exit code.

---

## 1. The Eval Harness

### One command, one verdict

The harness is a single entry point that runs the golden set and the adversarial set,
computes the metrics, and compares them to the baseline. It is deterministic: same
code, same sets, same thresholds, same verdict. Determinism is what makes the result a
gate rather than an opinion.

```python
# One command, one verdict.
python eval/run_eval.py --golden eval/golden.jsonl --adversarial eval/adversarial.jsonl
```

### Why a single entry point

If the evaluation is five scripts and a notebook, it will be run inconsistently and
compared across inconsistent runs. One command means the same evaluation every time,
which is the only basis for a threshold.

### Deterministic inputs

The sets are files, pinned in the repo. The model and prompt versions are pinned. With
the inputs fixed, a change in the result is a change in the system, which is exactly
what the harness is meant to detect.

## 2. Thresholds from a Baseline

### Capture the baseline

Run the current system against the fixed sets and record the numbers. That is the
baseline. Review it once, then enforce it.

### Derive the floors

Each metric gets a floor derived from the baseline. The exercise's `run_harness` takes
a baseline dictionary of floors and compares the current metrics against them:

```python
def run_harness(
    metrics: dict[str, float], baseline: dict[str, float]
) -> dict[str, str]:
    """Compare current metrics against the baseline floors. A metric below its floor fails."""
    verdicts = {}
    for name, floor in baseline.items():
        current = metrics[name]
        verdicts[name] = "PASS" if current >= floor else "FAIL"
    return verdicts
```

### A threshold is not a guess

A threshold invented without a baseline has no relationship to what the system can do,
so it either never fires (too low) or always fires (too high). Derive it from the
baseline and adjust with a tolerance that reflects measurement noise.

## 3. Change vs Baseline

### The delta is the unit of review

A change is judged against the baseline, not in isolation. A new chunker that scores
0.85 recall@5 is good only if the baseline was 0.80, and a regression if the baseline
was 0.90. The number alone is meaningless; the delta is the signal.

### The exercise's two cases

```python
baseline = {"recall@5": 0.80, "faithfulness": 0.90, "resistance": 0.90}

# A good change: at or above every floor.
good = {"recall@5": 0.85, "faithfulness": 0.92, "resistance": 0.95}
assert all(v == "PASS" for v in run_harness(good, baseline).values())

# A regression: recall improves, faithfulness drops below the floor.
regression = {"recall@5": 0.88, "faithfulness": 0.80, "resistance": 0.95}
verdicts = run_harness(regression, baseline)
assert verdicts["recall@5"] == "PASS"
assert verdicts["faithfulness"] == "FAIL"  # below the floor
```

The regression case is the important one: a change can improve one metric and degrade
another, and the harness must surface both.

### The exit test

The roadmap's exit test: "every change is evaluated against the baseline." That is
this section, and it is what separates a measured system from a hopeful one.

## 4. The Report

### The table

The report is a table: metric, baseline, current, delta, verdict. A regression is
visible at a glance, and the delta makes the tradeoff explicit rather than hidden.

| Metric | Baseline | Current | Delta | Verdict |
| --- | --- | --- | --- | --- |
| recall@5 | 0.80 | 0.88 | +0.08 | PASS |
| faithfulness | 0.90 | 0.80 | -0.10 | FAIL |
| resistance | 0.90 | 0.95 | +0.05 | PASS |

### The report is the artifact

The report is committed alongside the change, so the reasoning is preserved. A future
reader can see what the change did to every metric, not just the one it targeted.

## 5. The Gate

### Fail the build

The harness exits non-zero when any metric is below its floor, and CI treats that as a
failed build. The change does not merge. This is the mechanism that gives the
thresholds teeth.

### The gate is fast and offline

Unit-level eval runs use recorded fixtures or a mocked model so the gate is fast and
does not need a live API key. The full, model-backed evaluation runs are a separate,
heavier job. The gate catches regressions cheaply; the heavy run confirms quality.

## 6. Handling Tradeoffs

### Some trades are legitimate

A change that improves recall@5 while dropping precision@5 may be a deliberate,
documented tradeoff. The harness does not decide; it surfaces the delta so a human
decides with the numbers in front of them.

### The rule

A tradeoff is allowed only when it is explicit. Lowering a floor requires a recorded
reason, usually an ADR or a review note, so the change is a decision rather than a
silent drift. Raising a metric while quietly lowering a threshold is the anti-pattern
the gate exists to prevent.

## 7. The Discipline

### Run on every relevant change

Every change that touches the prompt, the retriever, the chunker, the guardrails, or
the model runs the harness. A change to a prompt is a change to the system, and it
gets the same scrutiny as a code change.

### Evaluation is not an afterthought

Running evaluation after the work is done, once, is how regressions accumulate.
Evaluation in CI is continuous, and it is the difference between a system that is known
to work and a system that worked on the day someone last checked.

## Real-World Application

- Wiring `make eval` into the DevMate CI job so a chunking change that lowers recall@5
  fails the build.
- Committing an eval report with each change so the delta is reviewable.
- Running the harness offline with a mocked model in the fast gate, and the full
  model-backed run in a heavier job.
- Raising a floor deliberately, with an ADR, when the system genuinely improves.

## Common Mistakes

1. **An eval harness that never runs in CI.** It cannot catch anything.
2. **Thresholds without a baseline.** They are guesses.
3. **Judging a change in isolation.** The absolute number is meaningless without the
   delta.
4. **No report.** Regressions become invisible and unarguable.
5. **Evaluation as a one-off after the work.** Regressions accumulate between checks.
6. **Lowering a floor silently to make the build pass.** This defeats the gate.
7. **A slow, online-only gate.** It gets skipped, and a skipped gate is no gate.

## Key Takeaways

1. The harness is one deterministic command that runs the fixed sets and returns a
   verdict.
2. Thresholds come from a captured baseline; a baseline without enforcement is a
   document.
3. A change is judged by its delta against the baseline, not by an absolute number.
4. The report makes regressions and tradeoffs explicit and is committed with the
   change.
5. Evaluation is part of the pipeline; a tradeoff is allowed only when it is explicit.

## Self-Check Questions

1. Why must the harness be deterministic, and what does that require of the inputs?
2. Why is a threshold without a baseline meaningless?
3. A change lifts recall@5 to 0.88 and drops faithfulness to 0.80 against a 0.90 floor.
   What is the verdict, and what should happen next?
4. Why is a fast offline gate separate from the full model-backed evaluation?
5. When is lowering a threshold acceptable, and what makes it acceptable?

## Further Reading / Connections

- AI Evaluation 01 (gold datasets) and 05 (adversarial evaluation) — the sets the
  harness runs.
- AI Evaluation 07 (production monitoring) — the same signals observed in production.
- `.ai/workflows/evaluation/` — the evaluation workflow that produces the report.
- `docs/reference/llm-production-architecture.md` — the evaluation-gating section.
