# Matplotlib Lecture 11: Animation

## Topic Overview

Animation turns static charts into process stories: training dynamics,
retrieval behavior over thresholds, agent trajectories. This lecture covers
`FuncAnimation` (init + update functions, blitting), writers for GIF/MP4,
and the performance discipline that keeps animations smooth — the machinery
behind the week-8 demo GIF.

## Learning Objectives

By the end of this lecture, you will be able to:

1. Build a `FuncAnimation` with init and update functions over frames
2. Use blitting correctly and explain what it skips (and what breaks with it)
3. Save GIFs (Pillow) and MP4s (ffmpeg) with controlled frame rate and DPI
4. Animate artists in place instead of re-plotting per frame
5. Scope animations to demos: what earns motion vs what should stay static

## 1. The Frame Contract

```python
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np

fig, ax = plt.subplots()
(line,) = ax.plot([], [], "b-", linewidth=2)
ax.set_xlim(0, 10); ax.set_ylim(-1.2, 1.2)   # fixed limits: no autoscale jitter

def init():
    line.set_data([], [])
    return (line,)

def update(frame):
    x = np.linspace(0, frame / 10, 200)
    line.set_data(x, np.sin(x))
    return (line,)

ani = animation.FuncAnimation(fig, update, frames=100, init_func=init, blit=True)
ani.save("sine.gif", writer="pillow", fps=20)
```

Fixed limits (no rescaling jitter), artists updated in place (no re-plot
cost), blit redraws only changed artists. Violate any of the three and the
animation stutters or lies.

## 2. Writers and Formats

Pillow writes GIFs anywhere (large files, 256 colors — fine for line demos);
ffmpeg writes MP4 (small, smooth, needs the binary installed). Control fps
(20–30 for demos) and DPI (72–100 for web; retina doubles file size for
zero demo value). Check the writer exists before a long render — discovering
missing ffmpeg after 10 minutes is a rite of passage worth skipping.

## 3. What Earns Motion

Motion is justified when time or iteration is the variable: loss descending,
recall climbing with k, an agent's tool sequence unfolding. Static
comparisons, distributions, and scorecards never need it. The week-8 demo
GIF shows one process (ask → retrieve → rerank → answer, timings attached);
everything else in the README stays still.

## Common Mistakes

- Autoscaling axes per frame (the chart dances instead of progressing).
- Re-plotting inside update (O(n²) artists, slideshow frame rates).
- Blitting with legends/titles changing per frame (stale artifacts).
- 60 fps retina GIFs (megabytes that teach nothing extra).

## Eval and Portfolio Connection

The demo GIF is a week-8 deliverable; threshold sweeps animate naturally
(recall@k vs k as k grows); training dynamics in week 11. One GIF per story,
each under ~2 MB, each reproducible from a script in the repo.

## Key Takeaways

1. Fixed limits, in-place artists, blit — the smooth-animation triple.
2. Pillow for GIFs, ffmpeg for MP4; check writers first.
3. Motion shows process; static shows state. Never confuse them.
