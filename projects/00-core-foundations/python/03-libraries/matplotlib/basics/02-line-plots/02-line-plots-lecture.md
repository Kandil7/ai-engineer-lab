# Matplotlib Lecture 02: Line Plots

## Topic Overview

Line plots are the default visualization for anything ordered: loss curves,
latency over time, metric trends across eval runs. This lecture covers the
plot call, line styles and markers, multi-line comparison, and the figure
habits that keep trend charts honest — the exact skills behind every
training curve and week-8 portfolio chart.

## Learning Objectives

By the end of this lecture, you will be able to:

1. Plot single and multiple series with labels, legend, and axis titles
2. Control style (`-`, `--`, `-.`, `:`), color, width, and markers deliberately
3. Compare runs on shared axes without misleading scales
4. Save publication-ready PNGs with tight bounding boxes
5. Choose line plots over bars for ordered data (and explain why)

## 1. The plot Call

```python
import matplotlib.pyplot as plt

epochs = [1, 2, 3, 4, 5]
train = [0.9, 0.6, 0.45, 0.38, 0.34]
valid = [0.95, 0.7, 0.6, 0.58, 0.59]

fig, ax = plt.subplots()
ax.plot(epochs, train, "b-", label="train")
ax.plot(epochs, valid, "r--", label="valid")
ax.set_xlabel("epoch"); ax.set_ylabel("loss"); ax.legend()
fig.savefig("loss.png", bbox_inches="tight")
```

Every element earns its place: labeled axes (units included), a legend when
lines exceed one, and `bbox_inches="tight"` so labels survive saving.

## 2. Style as Encoding, Not Decoration

Linestyle, color, and marker each encode one variable: solid vs dashed for
train vs valid, color for model variant, markers for sparse measured points.
Two rules prevent chartjunk: one encoding per variable, and no dual axes
with different scales on the same plot (they manufacture correlations).

## 3. Multi-Run Comparison

Overlay runs on shared axes with a fixed y-range so improvements read
honestly — autoscaling per subplot hides regressions. Twin curves that
diverge (train falling, valid rising) diagnose overfitting at a glance;
that single picture decides early stopping more reliably than any table.

## Common Mistakes

- Missing axis labels or units (a curve without units is decoration).
- Dual y-axes implying false correlation.
- Autoscaled subplots hiding a regression between runs.
- Saving without `bbox_inches="tight"` (clipped labels in the README).

## Eval and Portfolio Connection

Loss curves during the week-11 ML sprint, recall@k across chunking variants
in the weeks 2–3 ADR, latency percentiles in week 7 — all line plots, all
judged by the habits in section 2. The week-8 demo README earns its charts
here.

## Key Takeaways

1. Ordered data gets lines; labels, legend, tight save, always.
2. Style encodes variables — one encoding each, no dual axes.
3. Shared fixed scales make comparisons honest.
