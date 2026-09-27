# Matplotlib Lecture 04: Bar Plots

## Topic Overview

Bar plots compare discrete categories: per-model scores, per-repo chunk
counts, cost by provider. This lecture covers vertical and horizontal bars,
grouped and stacked layouts, value annotation, and the zero-baseline rule —
the chart behind every eval comparison table that deserves to be a picture.

## Learning Objectives

By the end of this lecture, you will be able to:

1. Choose vertical vs horizontal bars by label length and category count
2. Build grouped bars for side-by-side variants and stacked bars for composition
3. Annotate exact values so the chart survives without its data table
4. Defend the zero baseline — and state the one exception
5. Sort categories by value, not alphabetically, unless order carries meaning

## 1. Bars for Categories

```python
import matplotlib.pyplot as plt

models = ["haiku", "sonnet", "local-8b"]
recall = [0.81, 0.93, 0.78]

fig, ax = plt.subplots()
bars = ax.bar(models, recall)
ax.set_ylim(0, 1)                      # zero baseline: bar AREA means value
ax.bar_label(bars, fmt="%.2f")         # exact values on the chart itself
ax.set_ylabel("recall@10")
```

Horizontal bars (`barh`) win when labels are long or categories exceed ~8 —
readability beats convention.

## 2. Grouped vs Stacked

Grouped bars compare variants within each category (three chunkers × three
metrics: nine bars, three groups). Stacked bars show composition (latency =
embed + retrieve + rerank + generate per query). Never stack more than ~4
segments, and never stack values the reader must compare across stacks —
only totals compare reliably in stacked form.

## 3. The Zero Baseline (and Its Exception)

Bar area encodes value, so truncating the axis exaggerates differences —
0.81 vs 0.93 looks like 3× at a 0.75 baseline. Keep zero. The single
exception: tiny relative differences that matter (0.971 vs 0.978 recall),
where you annotate prominently AND state the axis break in the caption —
or better, switch to a dot plot, which carries no area encoding to lie with.

## Common Mistakes

- Truncated y-axis exaggerating a 2pp gap into a canyon.
- Alphabetical category order hiding the ranking the chart exists to show.
- 3D bars (ink without information; perspective distorts the encoding).
- Stacked bars for cross-stack comparison (only totals are comparable).

## Eval and Portfolio Connection

Chunking-strategy comparisons, model scorecards, cost-by-provider breakdowns —
the weeks 2–3 ADR results table becomes Figures 1–3 here, and the week-8
README leads with the scorecard chart. Every bar in those figures starts at
zero and carries its values.

## Key Takeaways

1. Categories get bars; bars start at zero.
2. Grouped compares, stacked composes (totals only).
3. Sort by value, annotate values, skip the 3D.
