# Matplotlib Lecture 05: Histograms

## Topic Overview

Histograms show distributions: score spreads, latency tails, chunk-length
profiles. This lecture covers bin selection (the decision that makes or
breaks the chart), density vs count, cumulative views, and overlaying
distributions for comparison — the tool behind every "what does the data
look like" question in evals.

## Learning Objectives

By the end of this lecture, you will be able to:

1. Choose bin counts deliberately (too few hides shape, too many shows noise)
2. Compare distributions with overlaid step histograms, not side-by-side bars
3. Switch between counts, density, and cumulative views by question asked
4. Read skew, bimodality, and outliers off a histogram
5. Plot latency as a histogram before quoting any percentile

## 1. Bins Are the Chart

```python
import matplotlib.pyplot as plt
import numpy as np

lat = np.random.gamma(2.0, 0.4, size=2000)  # right-skewed, like latency
fig, ax = plt.subplots()
ax.hist(lat, bins=40, density=False)
ax.set_xlabel("latency (s)")
ax.set_ylabel("queries")
ax.axvline(np.percentile(lat, 95), color="r", linestyle="--", label="p95")
```

Ten bins hides bimodality; two hundred shows sampling noise. Start near the
square-root rule (√n), then vary: shape that survives bin changes is signal,
shape that doesn't is artifact.

## 2. Compare by Overlay, Not Proximity

Two distributions side by side invite scale errors. Overlay step histograms
(`histtype="step"`, transparent fills) on shared axes: chunk-length profiles
of two chunkers, latency before/after an index change. The overlap region —
not the peaks — is usually the story.

## 3. Counts, Density, Cumulative

Counts answer "how many"; density answers "what shape" (area = 1, comparable
across sample sizes); cumulative answers "what fraction is below X" (SLO
reads directly: the 0.95 line crossing gives p95 visually). Latency analysis
wants cumulative; debugging shape wants density; stakeholder totals want
counts. Same data, three questions, three views.

## Common Mistakes

- Default bins accepted without thought (the #1 histogram failure).
- Bar-style overlapping histograms hiding one distribution behind another.
- Quoting mean latency without plotting the distribution (tails hide in means).
- Comparing counts across unequal sample sizes (use density).

## Eval and Portfolio Connection

Latency histograms precede every p50/p95 claim in week 7; score distributions
validate golden-set difficulty in weeks 2–3 (all-easy sets show as spikes);
chunk-length profiles justify the chunking ADR's size choices. Plot first,
quote second — always.

## Key Takeaways

1. Bins are a decision: vary them, trust surviving shape.
2. Overlay step histograms on shared axes for comparison.
3. Counts for totals, density for shape, cumulative for SLOs.
