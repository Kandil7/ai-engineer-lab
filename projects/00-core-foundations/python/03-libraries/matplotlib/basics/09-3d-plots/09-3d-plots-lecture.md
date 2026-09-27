# Matplotlib Lecture 09: 3D Plots

## Topic Overview

3D surface and wireframe plots show two-input functions: loss landscapes,
hyperparameter grids, embedding projections. This lecture covers
`mpl_toolkits.mplot3d` surfaces, wireframes, and 3D scatter — plus the
honest warning that 3D rarely beats a 2D heatmap for actual decisions.

## Learning Objectives

By the end of this lecture, you will be able to:

1. Build surface, wireframe, and 3D-scatter plots from grid data
2. Set viewpoint angles deliberately (elevation, azimuth)
3. State when 3D helps (landscape intuition) vs harms (occlusion, perspective)
4. Prefer contour/heatmap when the decision needs precise values
5. Label all three axes — unlabelled 3D is pure decoration

## 1. Surfaces and Wireframes

```python
import matplotlib.pyplot as plt
import numpy as np

x = np.linspace(-3, 3, 60); y = np.linspace(-3, 3, 60)
X, Y = np.meshgrid(x, y)
Z = np.sin(np.sqrt(X**2 + Y**2))   # any two-input function

fig = plt.figure()
ax = fig.add_subplot(111, projection="3d")
ax.plot_surface(X, Y, Z, cmap="viridis")
ax.set_xlabel("x"); ax.set_ylabel("y"); ax.set_zlabel("f(x, y)")
ax.view_init(elev=25, azim=-60)    # viewpoint is a decision, set it
```

Wireframes (`plot_wireframe`) suit sparse grids; surfaces suit dense ones;
3D scatter suits point clouds (embedding projections). All three share the
same axes discipline as 2D: labels with units, every axis, no exceptions.

## 2. The Viewpoint Problem

A 3D plot is a 2D projection chosen by angles — rotate 30 degrees and peaks
hide behind ridges. Occlusion and perspective make value-reading unreliable,
which is why 3D serves intuition (landscape shape, cluster separation) and
never measurement. Any decision needing numbers gets a contour plot or
heatmap instead.

## 3. When to Use (Rarely) and What Instead

Use 3D for: loss-landscape intuition talks, embedding-cloud orientation,
hyperparameter-surface shape. Replace with 2D when: comparing values
(heatmap), reading thresholds (contour with labeled levels), publishing
numbers (tables). The week-8 demo may carry one landscape figure; it will
not carry the argument.

## Common Mistakes

- Unlabelled z-axis (the most common 3D sin).
- Default viewpoint hiding the feature the plot exists to show.
- 3D bars (perspective-distorted area encoding — never).
- Using 3D where a heatmap would decide faster.

## Eval and Portfolio Connection

Hyperparameter sweeps (week 11) and embedding-space orientation figures.
One landscape intuition chart per talk maximum; decisions cite contour plots
and tables, which is where the advanced module's contour topic earns its keep.

## Key Takeaways

1. Surfaces for shape intuition, never for measurement.
2. Viewpoint angles are editorial decisions — set them deliberately.
3. When numbers matter, drop a dimension: contour or heatmap.
