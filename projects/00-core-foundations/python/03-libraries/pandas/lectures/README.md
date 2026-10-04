# Pandas Data Analysis: Complete Lecture Series

## Welcome

This directory contains **25 comprehensive learning materials** covering Pandas data manipulation, analysis, and visualization. Each topic includes a **Lecture** (theory + code) and a **Glossary** (quick reference + definitions).

---

## All Topics (Lectures 13–24)

| # | Topic | Lecture | Glossary | Core Skill |
|---|-------|---------|----------|------------|
| 13 | Clearing Data | `13-clearing-data-lecture.md` | `13-clearing-data-glossary.md` | Data cleaning & preprocessing |
| 14 | Adding New Columns | `14-data-new-column-lecture.md` | `14-data-new-column-glossary.md` | Column creation & derivation |
| 15 | Statistics | `15-statistics-lecture.md` | `15-statistics-glossary.md` | Descriptive statistics |
| 16 | Scatter Plot | `16-scatter-plot-lecture.md` | `16-scatter-plot-glossary.md` | Correlation visualization |
| 17 | Histogram | `17-histogram-lecture.md` | `17-histogram-glossary.md` | Distribution analysis |
| 18 | Pie Chart | `18-pie-chart-lecture.md` | `18-pie-chart-glossary.md` | Proportion visualization |
| 19 | Bar Chart | `19-bar-chart-lecture.md` | `19-bar-chart-glossary.md` | Categorical comparison |
| 20 | Merge | `20-merge-lecture.md` | `20-merge-glossary.md` | SQL-style joins |
| 21 | Concat | `21-concat-lecture.md` | `21-concat-glossary.md` | DataFrame stacking |
| 22 | GroupBy | `22-groupby-lecture.md` | `22-groupby-glossary.md` | Split-apply-combine |
| 23 | Correlation | `23-corr-lecture.md` | `23-corr-glossary.md` | Statistical relationships |
| 24 | Plotting | `24-plotting-lecture.md` | `24-plotting-glossary.md` | Advanced visualization |

---

## Recommended Learning Order

### Phase 1: Data Preparation (Topics 13–14)

> **Goal**: Master data cleaning and transformation before analysis.

```
13. Clearing Data     → Learn to handle missing values, duplicates, type errors
14. Adding Columns    → Create derived features and computed columns
```

### Phase 2: Descriptive Statistics (Topics 15, 23)

> **Goal**: Understand your data numerically before visualizing it.

```
15. Statistics        → Mean, median, mode, std, quartiles
23. Correlation       → Pearson/Spearman correlations between variables
```

### Phase 3: Visualization Fundamentals (Topics 16–19)

> **Goal**: Create the four most common chart types.

```
16. Scatter Plot      → Relationship between two continuous variables
17. Histogram         → Distribution of a single variable
18. Pie Chart         → Parts of a whole (use sparingly!)
19. Bar Chart         → Comparison across categories
```

### Phase 4: Data Combining (Topics 20–21)

> **Goal**: Merge datasets and work with multiple DataFrames.

```
20. Merge             → SQL-style joins (inner, outer, left, right)
21. Concat            → Vertical/horizontal stacking
```

### Phase 5: Advanced Analysis (Topics 22, 24)

> **Goal**: Group-level analysis and publication-quality plots.

```
22. GroupBy           → Split-apply-combine pattern
24. Plotting          → Subplots, themes, formatting, export
```

---

## Study Schedule

### Option A: Intensive (2 Weeks)

| Day | Topics | Hours |
|-----|--------|-------|
| Day 1 | 13 – Clearing Data | 2h |
| Day 2 | 14 – New Columns + 15 – Statistics | 3h |
| Day 3 | 23 – Correlation | 2h |
| Day 4 | 16 – Scatter Plot | 2h |
| Day 5 | 17 – Histogram + 18 – Pie Chart | 3h |
| Day 6 | 19 – Bar Chart | 2h |
| Day 7 | *Review Phase 1–3* | 2h |
| Day 8 | 20 – Merge | 3h |
| Day 9 | 21 – Concat | 2h |
| Day 10 | 22 – GroupBy | 3h |
| Day 11 | 24 – Plotting | 3h |
| Day 12 | *Capstone project* | 4h |
| Day 13–14 | *Review + Exercises* | 4h |

### Option B: Steady (5 Weeks)

| Week | Topics | Focus |
|------|--------|-------|
| Week 1 | 13, 14 | Data prep |
| Week 2 | 15, 23 | Statistics |
| Week 3 | 16, 17, 18, 19 | Visualization |
| Week 4 | 20, 21, 22 | Combining & grouping |
| Week 5 | 24 + review | Advanced plotting + consolidation |

---

## Prerequisites

- Python basics (variables, loops, functions)
- Basic NumPy knowledge (arrays, indexing)
- matplotlib fundamentals (recommended)

## How to Use These Materials

1. **Read the lecture** sequentially — each builds on prior topics
2. **Run every code example** in a Jupyter notebook
3. **Complete the exercises** before moving to the next topic
4. **Use the glossary** as a quick-reference card while coding
5. **Review the mistakes section** — these are the most common pitfalls

---

## Dataset References

Most examples use these sample datasets:

```python
import pandas as pd

# Sales data
df = pd.read_csv("sales.csv")

# Titanic dataset (built-in via seaborn)
import seaborn as sns

df = sns.load_dataset("titanic")

# Iris dataset
df = sns.load_dataset("iris")
```

---

*Part of the AI Engineer Lab – Core Foundations track.*
