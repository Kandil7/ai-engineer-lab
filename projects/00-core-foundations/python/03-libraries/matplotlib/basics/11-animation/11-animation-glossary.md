# Matplotlib 11: Animation — Glossary

## Quick Reference Table

| Term | Definition | Example |
|------|-----------|---------|
| FuncAnimation | Frame-driven animation (init + update) | sine wave demo |
| Blitting | Redraw-only-changed-artists optimization | smooth 20 fps |
| Writer | Backend serializing frames (Pillow/ffmpeg) | GIF vs MP4 |
| fps | Frames per second of saved output | 20 for demos |
| In-place update | Mutating artists via set_data, not re-plotting | O(1) per frame |
| Fixed limits | Preset axes preventing rescale jitter | set_xlim upfront |
| Demo GIF | Week-8 process story under ~2 MB | ask→answer flow |

---

## Alphabetical Glossary

### Blitting

**Definition:** `blit=True`: only changed artists redraw per frame. Fast,
with the constraint that static artists (titles, legends) must not change
mid-animation.

**Example:**
```python
FuncAnimation(fig, update, frames=100, init_func=init, blit=True)
```

**Related concepts:** In-place update, FuncAnimation

---

### Demo GIF

**Definition:** A short process animation for the portfolio README: one
story, timings attached, reproducible from a repo script, under ~2 MB.

**Example:**
```python
# week-8: ask -> retrieve -> rerank -> answer with per-stage timings
```

**Related concepts:** Writer, fps

---

### Fixed limits

**Definition:** Preset axis ranges preventing per-frame autoscaling. Without
them the chart dances and trends unread.

**Example:**
```python
ax.set_xlim(0, 10); ax.set_ylim(-1.2, 1.2)
```

**Related concepts:** FuncAnimation

---

### fps

**Definition:** Saved frames per second. 20–30 suits demos; higher values
cost file size without teaching more.

**Example:**
```python
ani.save("demo.gif", writer="pillow", fps=20)
```

**Related concepts:** Writer, Demo GIF

---

### FuncAnimation

**Definition:** matplotlib's frame animation: `init_func` sets the stage,
`update(frame)` mutates artists, `frames` counts steps.

**Example:**
```python
ani = animation.FuncAnimation(fig, update, frames=100, init_func=init)
```

**Related concepts:** Blitting, Writer

---

### In-place update

**Definition:** Mutating existing artists (`set_data`) instead of creating
new plot objects per frame. O(1) per frame vs O(n²) debris.

**Example:**
```python
line.set_data(x, y); return (line,)  # never ax.plot inside update
```

**Related concepts:** Blitting

---

### Writer

**Definition:** Serialization backend: Pillow (GIF, ubiquitous, bulky),
ffmpeg (MP4, compact, external binary). Verify availability before renders.

**Example:**
```python
# missing ffmpeg after a 10-minute render: check first
```

**Related concepts:** fps, Demo GIF

---

## Related Concepts

- **Subplots**: animated panels share the same discipline
- **Threshold sweeps**: recall@k vs k as natural animation subjects
- **Retina DPI**: doubles bytes, adds nothing to demos

## Key Takeaways

1. Limits fixed, artists mutated, blit on.
2. Check the writer before the render.
3. One process per GIF, two megabytes max.
