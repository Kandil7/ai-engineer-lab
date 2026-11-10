# Matplotlib Lecture 01: Introduction to Matplotlib

## 🎯 Topic Overview

Matplotlib is the foundational data visualization library for Python, created by John D. Hunter in 2003. It provides a MATLAB-like interface for creating static, animated, and interactive visualizations in Python. From simple line plots to complex 3D visualizations, Matplotlib is the backbone of Python's visualization ecosystem.

## 📚 Learning Objectives

By the end of this lecture, you will be able to:

1. Understand what Matplotlib is and its role in the data science stack
2. Install and import Matplotlib correctly
3. Recognize the two main interfaces: pyplot (functional) and OOP (explicit)
4. Create your first basic plots
5. Understand figure vs axes architecture
6. Save plots to files in various formats

---

## 1. What is Matplotlib?

Matplotlib is a comprehensive library for creating static, animated, and interactive visualizations in Python. It was inspired by MATLAB's plotting interface but has evolved into a much more powerful and flexible tool.

### Core Philosophy

- **Matplotlib** is the entire library, providing the object-oriented API
- **pyplot** is a convenience module that mimics MATLAB's plotting interface
- **Figures** are the top-level container for all plot elements
- **Axes** are the actual plotting areas (what most people think of as "a plot")

### The Visualization Ecosystem

```
┌──────────────────────────────────────────────────────┐
│                  Visualization                        │
├──────────────────────────────────────────────────────┤
│   Matplotlib (foundation, static plots)              │
│   ├── pyplot (MATLAB-like, quick)                    │
│   └── OOP API (explicit, powerful)                   │
│                                                      │
│   Extensions & Wrappers                              │
│   ├── Seaborn (statistical, pretty defaults)         │
│   ├── Pandas.plot() (convenient, DataFrame plots)    │
│   ├── Plotly (interactive, web-based)                │
│   ├── Bokeh (interactive, streaming)                 │
│   └── Altair (declarative, Vega-Lite)                │
└──────────────────────────────────────────────────────┘
```

---

## 2. Installation and Import

### Installation

```bash
# Using pip
pip install matplotlib

# Using conda
conda install matplotlib

# With optional backends
pip install matplotlib[qt]  # Qt backend for interactive plots
```

### Standard Import Conventions

```python
# THE universal convention — pyplot as plt
import matplotlib.pyplot as plt

# For the full library
import matplotlib as mpl

# Verify installation
print(mpl.__version__)  # e.g., 3.8.4
```

---

## 3. Two Interfaces: pyplot vs OOP

Matplotlib provides two ways to create plots. Understanding both is essential.

### The pyplot (Functional) Interface

```python
import matplotlib.pyplot as plt

# MATLAB-like, state-machine based
plt.figure(figsize=(8, 4))
plt.plot([1, 2, 3, 4], [1, 4, 2, 3])
plt.title("Simple Plot (pyplot)")
plt.xlabel("X axis")
plt.ylabel("Y axis")
plt.grid(True)
plt.show()
```

**Pros**: Quick and concise, MATLAB users feel at home
**Cons**: State-machine can be confusing for complex plots, less explicit

### The OOP (Object-Oriented) Interface

```python
import matplotlib.pyplot as plt

# Explicit figure and axes creation
fig, ax = plt.subplots(figsize=(8, 4))
ax.plot([1, 2, 3, 4], [1, 4, 2, 3])
ax.set_title("Simple Plot (OOP)")
ax.set_xlabel("X axis")
ax.set_ylabel("Y axis")
ax.grid(True)
plt.show()
```

**Pros**: Explicit, better for complex plots, works well with subplots
**Cons**: Slightly more verbose

### When to Use Each

| Scenario | Recommended Interface |
|----------|---------------------|
| Quick exploratory plots | pyplot |
| Jupyter notebooks | pyplot |
| Complex multi-subplot layouts | OOP |
| Publication-quality figures | OOP |
| Embedded in applications | OOP |
| Teaching beginners | pyplot first, then OOP |

---

## 4. Your First Plot

```python
import matplotlib.pyplot as plt
import numpy as np

# Data
x = np.linspace(0, 10, 100)
y = np.sin(x)

# Create figure and axes
fig, ax = plt.subplots(figsize=(8, 5))

# Plot
ax.plot(x, y, label="sin(x)", color="blue", linewidth=2)

# Customize
ax.set_title("First Plot: Sine Wave", fontsize=14, fontweight="bold")
ax.set_xlabel("x (radians)", fontsize=12)
ax.set_ylabel("sin(x)", fontsize=12)
ax.legend()
ax.grid(True, alpha=0.3)

# Display
plt.show()
```

---

## 5. Figure vs Axes Architecture

Understanding the hierarchy is crucial:

```
Figure (the entire window/page)
├── Title (fig.suptitle)
├── Subplot / Axes (the actual plot area)
│   ├── Title (ax.set_title)
│   ├── X-axis
│   │   ├── Label
│   │   ├── Ticks
│   │   └── Tick labels
│   ├── Y-axis
│   │   ├── Label
│   │   ├── Ticks
│   │   └── Tick labels
│   ├── Data lines / Markers / Bars
│   ├── Grid
│   └── Legend
├── Colorbar (if applicable)
└── Multiple subplots (if applicable)
```

### Key Objects

```python
fig = plt.figure(figsize=(8, 6))  # The canvas
ax = fig.add_subplot(111)  # One subplot (1 row, 1 col, index 1)
# OR
fig, ax = plt.subplots(2, 2, figsize=(10, 8))  # 2×2 grid of subplots

print(type(fig))  # <class 'matplotlib.figure.Figure'>
print(type(ax))  # <class 'matplotlib.axes._subplots.AxesSubplot'>
```

---

## 6. Saving Plots

```python
import matplotlib.pyplot as plt
import numpy as np

x = np.linspace(0, 10, 100)
y = np.sin(x)

fig, ax = plt.subplots()
ax.plot(x, y)
ax.set_title("Sine Wave")

# Save before show() - save clears the figure
fig.savefig("sine_wave.png", dpi=300, bbox_inches="tight")
fig.savefig("sine_wave.pdf", dpi=300, bbox_inches="tight")
fig.savefig("sine_wave.svg", dpi=300, bbox_inches="tight")

plt.show()
```

### savefig() Parameters


| Parameter | Description | Example |
|-----------|-------------|---------|
| `fname` | File path/name | `'plot.png'` |
| `dpi` | Resolution | `300` (print quality) |
| `bbox_inches` | Tight bounding box | `'tight'` |
| `transparent` | Transparent background | `True` |
| `format` | Override format | `'png'`, `'pdf'`, `'svg'` |
| `facecolor` | Background color | `'white'` |

### Supported Formats

| Format | Use Case | Pros | Cons |
|--------|----------|------|------|
| PNG | Web, presentations | Universal, raster | Pixelation at scale |
| PDF | Publications | Vector, scalable | Large file size |
| SVG | Web, editing | Vector, editable | Browser support varies |
| EPS | LaTeX | Vector, LaTeX native | Obsolete format |
| JPG | Photos | Small file size | Lossy compression |

---

## 7. Matplotlib Styles and Themes

Matplotlib comes with built-in styles:

```python
import matplotlib.pyplot as plt

# List available styles
print(plt.style.available)

# Use a style
plt.style.use("ggplot")

# OR with context manager
with plt.style.context("seaborn-v0_8-darkgrid"):
    fig, ax = plt.subplots()
    ax.plot([1, 2, 3], [1, 4, 2])
    ax.set_title("Seaborn Dark Grid Style")
```

### Popular Styles

- `'default'` — Matplotlib's classic look
- `'ggplot'` — Inspired by R's ggplot2
- `'seaborn-v0_8'` — Clean statistical plots
- `'fivethirtyeight'` — Data journalism style
- `'dark_background'` — Dark mode plots
- `'bmh'` — Bayesian Methods for Hackers
- `'tableau-colorblind10'` — Accessible color palette

---

## 8. Common Mistakes to Avoid

### Mistake 1: Mixing pyplot and OOP Inconsistently
```python
# CONFUSING - mixing styles
plt.plot(x, y)  # pyplot
ax.set_title("Title")  # OOP - but which ax?

# CLEAR - choose one
fig, ax = plt.subplots()
ax.plot(x, y)
ax.set_title("Title")
```

### Mistake 2: Creating Multiple Figures Unintentionally
```python
# BAD - creates new figure each time
plt.plot(x, y)
plt.title("Plot")
# Later...
plt.plot(x2, y2)  # New figure created!

# GOOD - explicit figure management
plt.figure(1)  # Switch to figure 1
plt.plot(x, y)

plt.figure(2)  # Switch to figure 2
plt.plot(x2, y2)
```

### Mistake 3: Not Using `fig.tight_layout()`
```python
# BAD - overlapping labels
fig, ax = plt.subplots()
ax.set_xlabel("Very long label that overlaps")
ax.set_title("Title that also overlaps")

# GOOD - auto-adjust spacing
fig, ax = plt.subplots()
ax.set_xlabel("Very long label")
ax.set_title("Title")
fig.tight_layout()
```

### Mistake 4: Forgetting to Call `plt.show()` in Scripts
```python
# BUG - plot won't display in script
fig, ax = plt.subplots()
ax.plot(x, y)
# No plt.show() - nothing appears!

# FIX
fig, ax = plt.subplots()
ax.plot(x, y)
plt.show()
```

---

## 9. Best Practices

1. **Always use the OOP interface** for complex or publication plots
2. **Set figure size** explicitly: `fig, ax = plt.subplots(figsize=(8, 5))`
3. **Use vector formats** (PDF, SVG) for publications, PNG for web
4. **Set DPI to 300+** for print-quality figures
5. **Always add labels and titles** — never leave a plot bare
6. **Use `bbox_inches='tight'`** when saving to avoid clipping
7. **Pick appropriate color palettes** — consider colorblind accessibility
8. **Use `plt.style.context()`** for temporary style changes
9. **Close figures you don't need** with `plt.close(fig)` to save memory
10. **Export to PDF** for LaTeX papers — vector quality, editable text

---

## 10. Practice Exercises

### Exercise 1: Basic Plot
Create a line plot of `y = x²` for x from -10 to 10. Add title, labels, and grid.

### Exercise 2: Style Exploration
Plot the same data using 3 different Matplotlib styles. Save each as a separate PNG.

### Exercise 3: Figure vs Axes
Create a figure with 2 subplots (1 row, 2 columns) using the OOP interface. Plot `sin(x)` on the left and `cos(x)` on the right.

### Exercise 4: Save Formats
Create a plot and save it as PNG, PDF, SVG. Compare file sizes and quality.

### Exercise 5: Custom Style
Create a custom style by modifying the defaults (colors, font sizes, grid style). Apply it to a plot.

---

## 11. Summary

| Concept | Key Takeaway |
|---------|-------------|
| **What** | Foundational Python visualization library |
| **Import** | `import matplotlib.pyplot as plt` |
| **Two APIs** | pyplot (quick) vs OOP (explicit) |
| **Architecture** | Figure (canvas) → Axes (plot area) → Elements |
| **Formats** | PNG (web), PDF/SVG (publications) |
| **Styles** | Built-in themes for different aesthetics |
| **Best Practice** | Use OOP for complex plots, pyplot for quick exploration |

### Key Takeaways

1. Matplotlib is the foundation of Python visualization
2. Use the OOP interface for production-quality plots
3. Always specify figure size and DPI for consistent output
4. Save in vector formats for publications
5. Master the Figure → Axes → Element hierarchy

---

## 🔗 Next Lecture

→ [02-pyplot-lecture.md](./02-pyplot-lecture.md) — The Pyplot Interface
