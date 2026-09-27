# Matplotlib 09: 3D Plots — Glossary

## Quick Reference Table

| Term | Definition | Example |
|------|-----------|---------|
| mplot3d | 3D toolkit (`projection="3d"`) | surfaces, wireframes |
| Surface plot | Filled two-input function rendering | loss landscapes |
| Wireframe | Grid-line rendering for sparse surfaces | coarse sweeps |
| 3D scatter | Point cloud in three axes | embedding projections |
| Viewpoint | Elevation/azimuth angles choosing the projection | elev=25, azim=-60 |
| Occlusion | Near geometry hiding far features in 3D | rotated peaks |
| Contour plot | 2D level-line alternative for decisions | threshold reading |

---

## Alphabetical Glossary

### Contour plot

**Definition:** 2D level lines of a two-input function with labeled values.
The decision-grade replacement for 3D surfaces.

**Example:**
```python
ax.contour(X, Y, Z, levels=12)  # read thresholds, no rotation needed
```

**Related concepts:** Surface plot, Occlusion

---

### mplot3d

**Definition:** matplotlib's 3D toolkit, enabled per-axes with
`projection="3d"`. Surfaces, wireframes, 3D scatter and bars.

**Example:**
```python
ax = fig.add_subplot(111, projection="3d")
```

**Related concepts:** Surface plot, Viewpoint

---

### Occlusion

**Definition:** Near 3D geometry hiding farther features from the current
viewpoint. Why 3D shows shape but never measures.

**Example:**
```python
# the valley exists; this rotation hides it: set view_init deliberately
```

**Related concepts:** Viewpoint, Contour plot

---

### Surface plot

**Definition:** `plot_surface`: filled rendering of Z over an X–Y grid.
Landscape intuition; colormap encodes height redundantly with geometry.

**Example:**
```python
ax.plot_surface(X, Y, Z, cmap="viridis")
```

**Related concepts:** Wireframe, Contour plot

---

### Viewpoint

**Definition:** The (`elev`, `azim`) projection angles. An editorial choice
that decides which features are visible — set explicitly, never defaulted.

**Example:**
```python
ax.view_init(elev=25, azim=-60)
```

**Related concepts:** Occlusion

---

### Wireframe

**Definition:** `plot_wireframe`: grid-line-only surface rendering. Suits
sparse grids where filled surfaces would imply false smoothness.

**Example:**
```python
ax.plot_wireframe(X[::4, ::4], Y[::4, ::4], Z[::4, ::4])
```

**Related concepts:** Surface plot

---

### 3D scatter

**Definition:** Points positioned in three axes. Embedding-cloud orientation
and cluster separation at a glance; precise membership needs 2D projections.

**Example:**
```python
ax.scatter(xs, ys, zs, c=labels)
```

**Related concepts:** Surface plot, Occlusion

---

## Related Concepts

- **Heatmaps**: the 2D decision alternative (advanced module)
- **Embedding projections**: UMAP/t-SNE clouds as 3D scatter input
- **Colormaps**: viridis default; perceptual uniformity matters

## Key Takeaways

1. 3D shows shape; 2D decides.
2. Label all three axes; set the viewpoint.
3. One landscape figure per talk, maximum.
