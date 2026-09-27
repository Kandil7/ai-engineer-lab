# Matplotlib 07: Box and Violin Plots — Glossary

## Quick Reference Table

| Term | Definition | Example |
|------|-----------|---------|
| Box plot | Quartile glyph: box, median line, whiskers, fliers | per-model scores |
| Quartiles | Q1/median/Q3 splitting data into quarters | middle-50% box |
| IQR | Interquartile range (Q3−Q1); whisker fence basis | spread measure |
| Whiskers | 1.5×IQR fences, not min/max or CIs | outlier boundary |
| Fliers | Points beyond whiskers, plotted individually | slow-query dots |
| Violin plot | Mirrored density glyph showing shape | bimodality check |
| Median ordering | Sorting groups by median, not alphabet | ranking-visible charts |

---

## Alphabetical Glossary

### Box plot

**Definition:** `ax.boxplot`: box (Q1–Q3), median line, 1.5×IQR whiskers,
fliers as points. Distribution comparison across many groups.

**Example:**
```python
ax.boxplot([a_scores, b_scores, c_scores], labels=[...])
```

**Related concepts:** Quartiles, Whiskers

---

### Fliers

**Definition:** Observations outside the whisker fences, drawn as individual
points. Candidates for investigation, not automatic deletions.

**Example:**
```python
# three dots at 12s latency: the incident, or the misconfiguration?
```

**Related concepts:** Whiskers, IQR

---

### IQR

**Definition:** Interquartile range, Q3 minus Q1: the middle-50% spread.
Robust to outliers where standard deviation is not.

**Example:**
```python
# IQR 0.06 on faithfulness: tight consensus, whatever the mean says
```

**Related concepts:** Quartiles, Whiskers

---

### Median ordering

**Definition:** Sorting comparison groups by median value. The ranking the
chart exists to show, instead of alphabetical camouflage.

**Example:**
```python
order = np.argsort([np.median(g) for g in groups])
```

**Related concepts:** Box plot

---

### Quartiles

**Definition:** Q1 (25th), median (50th), Q3 (75th) percentiles. The box is
Q1–Q3; the line is the median — resistant to skew, unlike the mean.

**Example:**
```python
np.percentile(x, [25, 50, 75])
```

**Related concepts:** IQR, Box plot

---

### Violin plot

**Definition:** `ax.violinplot`: mirrored density estimate around an axis,
waists showing bimodality. Shape questions, not quartile questions.

**Example:**
```python
ax.violinplot([before, after], showmedians=True)
```

**Related concepts:** Box plot, Bimodality

---

### Whiskers

**Definition:** Fences at 1.5×IQR beyond the quartiles (matplotlib default).
Neither min/max nor confidence intervals — the most misread chart element.

**Example:**
```python
# points beyond: fliers worth investigating, not deleting
```

**Related concepts:** Fliers, IQR

---

## Related Concepts

- **Histograms**: the full distribution behind the glyph (topic 05)
- **Sample size**: annotate n; tight boxes on n=12 mislead
- **Cumulative views**: quantile reading alternative

## Key Takeaways

1. Know what every glyph element means before reading one.
2. Shape questions get violins, quartile questions get boxes.
3. Order by median, annotate n, share the scale.
