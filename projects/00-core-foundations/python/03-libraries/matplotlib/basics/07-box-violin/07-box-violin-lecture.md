# Matplotlib Lecture 07: Box and Violin Plots

## Topic Overview

Box and violin plots compress whole distributions into comparable glyphs:
medians, quartiles, tails, and density shape across a dozen variants at
once. This lecture covers quartiles and whiskers, when violins beat boxes,
and grouped comparison layouts — the chart for per-model, per-chunker, and
per-endpoint distribution comparison.

## Learning Objectives

By the end of this lecture, you will be able to:

1. Read a box: median, quartiles, whiskers, fliers — and state each precisely
2. Choose violin over box when shape (bimodality) matters
3. Compare a dozen distributions in one grouped figure
4. Order groups by median, not alphabetically
5. Pair distribution plots with the sample sizes behind them

## 1. The Box, Precisely

```python
import matplotlib.pyplot as plt

fig, ax = plt.subplots()
ax.boxplot([m_a_scores, m_b_scores, m_c_scores], labels=["haiku", "sonnet", "local"])
ax.set_ylabel("faithfulness")
```

Box edges are Q1/Q3 (the middle 50%), the line is the median, whiskers
extend to 1.5×IQR by default, points beyond are fliers. Whiskers are NOT
min/max and NOT confidence intervals — the two most common misreadings,
stated plainly so you never make them.

## 2. Violins for Shape

```python
ax.violinplot([m_a_scores, m_b_scores], showmedians=True)
```

Violins mirror a density estimate around the axis: bimodality shows as
waists, skew as asymmetry. Use them when the question is about shape
("are slow queries a tail or a second population?"); keep boxes when the
question is about quartiles and outliers. Small samples (<~30) suit neither —
show the points.

## 3. Grouped Comparison Discipline

One axis per variant, shared scale, median-ordered, sample sizes annotated
(n=200 under each label — a tight box on n=12 is a lie of confidence).
Twelve chunker variants, three models, eight endpoints: this is the only
chart type that holds that many distributions legibly.

## Common Mistakes

- Reading whiskers as min/max or confidence intervals.
- Violin plots on tiny samples (density estimates of nothing).
- Alphabetical group order hiding the ranking.
- Missing sample sizes (precision without evidence).

## Eval and Portfolio Connection

Per-model faithfulness distributions, per-chunker recall spreads, per-endpoint
latency shapes — weeks 2–3 and week 7 comparisons live in these glyphs. The
chunking ADR's Figure 2 (recall distributions, not just means) comes from
this lecture.

## Key Takeaways

1. Boxes for quartiles, violins for shape, points for small samples.
2. Whiskers are 1.5×IQR fences — know what you're reading.
3. Median-ordered, shared scale, annotated n.
