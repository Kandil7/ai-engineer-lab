# Matplotlib 02: Line Plots — Glossary

## Quick Reference Table

| Term | Definition | Example |
|------|-----------|---------|
| Line plot | Ordered-series visualization via `plot` | loss curves |
| Linestyle | `-` solid, `--` dashed, `-.` dashdot, `:` dotted | train vs valid |
| Marker | Symbol per data point (`o`, `s`, `^`) | sparse measurements |
| Legend | Label key for multi-series plots | model variants |
| bbox_inches | Save option preventing clipped labels | portfolio PNGs |
| Dual axes | Two y-scales, one plot — avoid | false correlations |
| Shared axes | Fixed ranges across subplots for honest comparison | run-over-run evals |

---

## Alphabetical Glossary

### bbox_inches

**Definition:** `savefig` option (`"tight"`) expanding the saved area to
include labels and legends. The difference between a chart and a clipped one.

**Example:**
```python
fig.savefig("loss.png", bbox_inches="tight")
```

**Related concepts:** Legend

---

### Dual axes

**Definition:** Two y-scales on one plot via `twinx`. Manufactures apparent
correlations through arbitrary scaling — avoid in honest reporting.

**Example:**
```python
# cost and accuracy on different scales crossing "meaningfully": a lie
```

**Related concepts:** Shared axes

---

### Legend

**Definition:** The key mapping line styles to series names. Mandatory beyond
one series; placed to avoid covering data.

**Example:**
```python
ax.legend(loc="best")
```

**Related concepts:** Line plot

---

### Line plot

**Definition:** `ax.plot(x, y)`: the visualization for ordered data. Trends,
curves, and comparisons over sequence — the eval workhorse.

**Example:**
```python
ax.plot(epochs, train_loss, "b-", label="train")
```

**Related concepts:** Marker, Shared axes

---

### Linestyle

**Definition:** The `-`/`--`/`-.`/`:` stroke patterns encoding one variable
(typically train vs valid, or baseline vs candidate).

**Example:**
```python
ax.plot(x, a, "-", x, b, "--")  # solid baseline, dashed candidate
```

**Related concepts:** Marker

---

### Marker

**Definition:** Per-point symbols marking measured values on a line. For
sparse observations where the line interpolates between real points.

**Example:**
```python
ax.plot(xs, ys, "o-")  # circles joined by solid line
```

**Related concepts:** Linestyle

---

### Shared axes

**Definition:** Fixed identical ranges across compared subplots
(`sharex`/`sharey` or explicit limits). Makes improvements and regressions
visible instead of autoscaled away.

**Example:**
```python
fig, axes = plt.subplots(1, 2, sharey=True)
```

**Related concepts:** Dual axes

---

## Related Concepts

- **Subplots**: multi-panel figures (topic 08)
- **Eval deltas**: run-over-run charts in ADRs
- **Loss curves**: the week-11 application

## Key Takeaways

1. Lines for ordered data, labels always.
2. Style encodes; dual axes deceive.
3. Compare on shared scales.
