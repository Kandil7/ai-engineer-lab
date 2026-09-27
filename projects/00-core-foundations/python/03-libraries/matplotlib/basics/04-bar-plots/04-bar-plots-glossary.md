# Matplotlib 04: Bar Plots — Glossary

## Quick Reference Table

| Term | Definition | Example |
|------|-----------|---------|
| Bar plot | Category comparison via `bar`/`barh` | model scorecards |
| Grouped bars | Side-by-side variants within categories | 3 chunkers × 3 metrics |
| Stacked bars | Composition segments summing to totals | latency breakdown |
| Zero baseline | Axis starts at 0 so area encodes value | honest comparisons |
| bar_label | Exact value annotation on bars | self-sufficient charts |
| Dot plot | Position-encoded alternative for tiny deltas | 0.971 vs 0.978 |

---

## Alphabetical Glossary

### Bar plot

**Definition:** `ax.bar` / `ax.barh`: rectangles whose length/area encodes
category values. The discrete-comparison workhorse.

**Example:**
```python
ax.bar(models, recall)  # one bar per model, zero baseline
```

**Related concepts:** Grouped bars, Zero baseline

---

### bar_label

**Definition:** Value annotation method placing exact numbers on bars. Makes
charts readable without their source tables.

**Example:**
```python
ax.bar_label(bars, fmt="%.2f")
```

**Related concepts:** Bar plot

---

### Dot plot

**Definition:** Values as positions on a common scale, no area encoding.
The honest choice for tiny-but-real differences where bars would lie.

**Example:**
```python
ax.plot(scores, categories, "o")  # 0.971 vs 0.978, no exaggeration
```

**Related concepts:** Zero baseline

---

### Grouped bars

**Definition:** Clusters of side-by-side bars comparing variants within each
category. Offsets computed per group; legend identifies variants.

**Example:**
```python
# three chunkers grouped under each metric name
```

**Related concepts:** Stacked bars, Bar plot

---

### Stacked bars

**Definition:** Segments summing to per-category totals (composition). Only
totals compare across stacks; at most ~4 segments.

**Example:**
```python
# embed + retrieve + rerank + generate stacked per query class
```

**Related concepts:** Grouped bars

---

### Zero baseline

**Definition:** Bar axes start at zero so area means value. Truncation
exaggerates differences — the most common bar-chart lie.

**Example:**
```python
ax.set_ylim(0, 1)  # recall bars always
```

**Related concepts:** Dot plot

---

## Related Concepts

- **Subplots**: scorecard grids (topic 08)
- **ADR figures**: results tables promoted to charts
- **3D bars**: ink without information — never

## Key Takeaways

1. Zero baseline, sorted categories, annotated values.
2. Group to compare, stack to compose.
3. Tiny deltas get dots, not truncated bars.
