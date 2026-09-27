# Matplotlib 05: Histograms — Glossary

## Quick Reference Table

| Term | Definition | Example |
|------|-----------|---------|
| Histogram | Value distribution via binned counts (`hist`) | latency spread |
| Bins | Intervals partitioning the value range | 40 bins for 2000 samples |
| Density | Normalized view, area = 1, comparable across sizes | shape comparison |
| Cumulative | Running-fraction view reading quantiles directly | SLO verification |
| Step histogram | Outline-only overlay style for comparison | two chunkers overlaid |
| Skew | Asymmetric tail (latency skews right) | gamma-like shapes |
| Bimodality | Two peaks signaling mixed populations | cached vs uncached |

---

## Alphabetical Glossary

### Bimodality

**Definition:** Two distinct peaks indicating mixed subpopulations. The
diagnostic that splits one analysis into two (cache hits vs misses).

**Example:**
```python
# latency bimodal at 0.2s and 2.1s -> two serving paths, analyze separately
```

**Related concepts:** Histogram, Skew

---

### Bins

**Definition:** The intervals values are counted into. Count and edges set
the resolution: too few blur shape, too many show noise.

**Example:**
```python
ax.hist(x, bins=40)  # starting near sqrt(n), then varied deliberately
```

**Related concepts:** Histogram, Density

---

### Cumulative

**Definition:** Cumulative-fraction view (`cumulative=True`): the y-value at
x is the fraction below x. Reads quantiles and SLO compliance directly.

**Example:**
```python
ax.hist(lat, bins=100, cumulative=True, density=True)  # 0.95 line -> p95
```

**Related concepts:** Density, Histogram

---

### Density

**Definition:** Density-normalized view (area sums to 1). Compares shapes
across unequal sample sizes where counts would mislead.

**Example:**
```python
ax.hist(a, bins=40, density=True, histtype="step", label="before")
```

**Related concepts:** Cumulative, Step histogram

---

### Histogram

**Definition:** `ax.hist`: counts of values per bin. The distribution
workhorse for scores, latencies, lengths — anything with spread.

**Example:**
```python
ax.hist(scores, bins=30)  # golden-set difficulty at a glance
```

**Related concepts:** Bins, Density

---

### Skew

**Definition:** Asymmetric tail direction. Right-skew (latency, cost) means
means exceed medians — quote percentiles, not means.

**Example:**
```python
# mean 1.2s, p50 0.8s, p95 3.1s: the mean describes nobody
```

**Related concepts:** Bimodality, Cumulative

---

### Step histogram

**Definition:** Outline-only style (`histtype="step"`) for overlaying
multiple distributions without occlusion. The comparison default.

**Example:**
```python
ax.hist(old, histtype="step"); ax.hist(new, histtype="step")  # shared axes
```

**Related concepts:** Density, Histogram

---

## Related Concepts

- **Box plots**: quartile compression of the same distributions (topic 07)
- **Percentiles**: p50/p95 read off cumulative views
- **Golden-set difficulty**: spikes mean an all-easy set

## Key Takeaways

1. Vary bins; trust surviving shape.
2. Density compares, cumulative verifies SLOs, counts total.
3. Plot the distribution before quoting any number from it.
