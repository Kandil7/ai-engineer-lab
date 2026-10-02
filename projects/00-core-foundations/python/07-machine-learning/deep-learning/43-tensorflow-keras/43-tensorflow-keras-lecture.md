# 07-machine-learning — 43: TensorFlow and Keras — The Declarative Framework

Companion exercise: `43-tensorflow-keras.py`

---

## Topic Overview

PyTorch asks you to write the loop; Keras asks you to describe the
model.
TensorFlow/Keras is the *declarative* side of deep learning — you stack
layers,
call `compile` with an optimizer and loss, then `fit`, and the framework
runs the
training loop for you. That ergonomics difference, not raw performance,
is why
Keras dominates applied ML and tutorials while PyTorch dominates
research.

This topic maps the two frameworks to each other so you can read either.
Keras
offers two APIs — the Sequential API for linear stacks and the
Functional API
for branching graphs — plus the same primitives (layers, optimizers,
losses)
under different names. Because TensorFlow is not installed in this
environment,
the exercise runs the Keras *mental model* in PyTorch so the comparison
is
concrete, not theoretical.

The payoff is fluency: a production ML system may embed a Keras model
for
serving, a PyTorch model for research, and you must move between the two
without
losing the plot. The mapping table in this topic is the durable skill —
the rest
is syntax that any reference will show you.

## Learning Objectives

By the end of this lecture, you will be able to:

1. Distinguish the declarative Keras style from the explicit PyTorch style.
2. Map Keras layers, optimizers, and losses onto their PyTorch equivalents.
3. Use the Sequential API and explain when the Functional API is required.
4. Explain what `compile` and `fit` abstract away.
5. Choose TensorFlow/Keras versus PyTorch by use case.
6. Serve a Keras model (SavedModel) and understand its artifact shape.
7. Translate a Keras model into PyTorch by hand.
8. Explain the channels-first vs channels-last difference and why it matters.

## Prerequisites

| Need | Where |
|---|---|
| Neural network basics | `38-neural-network-basics.py` |
| PyTorch training loop | `37-pytorch-training-loop.py` |

## 1. Declarative vs Explicit

### The Keras way

Keras describes the model and the training *configuration*, and the
framework
runs the loop:

```python
from tensorflow import keras

model = keras.Sequential(
    [
        keras.layers.Dense(64, activation="relu"),
        keras.layers.Dense(1),
    ]
)
model.compile(optimizer="adam", loss="mse")
model.fit(X_train, y_train, epochs=10)
```

### The PyTorch way

PyTorch expresses the same thing, but you own the loop:

```python
model = nn.Sequential(nn.Linear(8, 64), nn.ReLU(), nn.Linear(64, 1))
opt = torch.optim.Adam(model.parameters())
for _ in range(10):
    loss = nn.functional.mse_loss(model(X_train), y_train)
    opt.zero_grad()
    loss.backward()
    opt.step()
```

### The real difference

The difference is control versus convenience. Keras hides the loop;
PyTorch
exposes it. Research that needs a custom gradient or a novel loop
reaches for
PyTorch; a standard supervised task reaches for Keras. The analogy is a
fully-automatic camera versus manual controls: the automatic gets you a
good
picture fast; the manual lets you do things the automatic cannot.

### When each style wins

Declarative wins when the standard loop is all you need — the 90% case.
Explicit wins when you need to change *how* training happens, not just
what the
model is. The moment your loss or update rule is nonstandard, the hidden
loop
becomes a wall you must climb over.

## 2. The Sequential API

### Linear stacks

`Sequential` is a list of layers applied in order — the right choice
when data
flows straight through. Each layer's output feeds the next, and shapes
are
inferred from the input.

### What it cannot express

A Sequential model cannot branch, merge, or share layers. The moment a
model has
a residual connection or two inputs, Sequential is out and the
Functional API is
in. This limitation is not a flaw but a scope: Sequential is the 80%
convenience,
Functional is the 100% generality.

## 3. The Functional API

### Branching graphs

The Functional API treats layers as callable functions, so you can build
arbitrary graphs — shared layers, multiple inputs, skip connections:

```python
inputs = keras.Input(shape=(8,))
x = keras.layers.Dense(64, activation="relu")(inputs)
out = keras.layers.Dense(1)(x)
model = keras.Model(inputs=inputs, outputs=out)
```

### Why it matters

Almost every non-trivial architecture (ResNet, U-Net, multi-modal
models) needs
the Functional API. Sequential is a convenience; Functional is the
general tool.
The same "layers as callables" idea appears in PyTorch as calling
modules
directly in `forward`.

## 4. compile and fit

### What compile does

`compile` binds the optimizer, loss, and metrics to the model — it
*configures*
training but does not run it. It is the analogue of choosing an
optimizer and
loss function in PyTorch.

### What fit does

`fit` runs the training loop: batches, forward, backward, optimizer
step, and
metric logging — all hidden. Callbacks (`EarlyStopping`,
`ModelCheckpoint`)
hook into the loop, which is how Keras gets early stopping without you
writing
the condition. This is the single abstraction that defines the
framework; every
other difference is cosmetic.

## 5. Mapping the Two Frameworks

### The translation table

| Keras | PyTorch |
|---|---|
| `Dense(64, activation="relu")` | `nn.Linear(8, 64)` + `nn.ReLU()` |
| `Conv2D`, `MaxPooling2D` | `nn.Conv2d`, `nn.MaxPool2d` |
| `LSTM`, `GRU` | `nn.LSTM`, `nn.GRU` |
| `model.compile(optimizer="adam", loss="mse")` | `Adam(...)` + `nn.functional.mse_loss` |
| `model.fit(X, y, epochs=10)` | your explicit loop |
| `EarlyStopping` | `optuna` pruning / manual check |
| `model.save("m")` (SavedModel) | `torch.save(model.state_dict(), ...)` |

### The channels convention

Keras defaults to channels-last `(batch, H, W, C)` for images; PyTorch
defaults
to channels-first `(batch, C, H, W)`. This is the most common silent bug
when
porting a vision model between frameworks — the same tensor means
different
things. Pin `data_format` (Keras) or transpose the tensor explicitly.

### The single most important row

`fit` versus the loop. If you need to write the loop, use PyTorch; if
the
standard loop suffices, Keras saves you from rewriting it every time.

## 6. Serving a Keras Model

### The SavedModel artifact

A trained Keras model exports to a SavedModel directory — a
self-contained
bundle of graph and weights that TensorFlow Serving or `tf.keras` can
load
without the training code. That artifact shape matters for deployment
(`model-serving` in this curriculum).

### The comparison

PyTorch ships weights plus your model class; Keras ships a
self-describing
artifact. Each has an edge: Keras's artifact is more portable to its
serving
stack; PyTorch's class keeps the logic inspectable. Neither is wrong;
they are
different deployment contracts.

## 7. Choosing a Framework

### When to choose TensorFlow/Keras

Choose Keras for standard supervised models, for deployment into the
TensorFlow
serving ecosystem (TF Serving, TF Lite for edge), and for teams that
want
low-ceremony training.

### When to choose PyTorch

Choose PyTorch for research, novel architectures, and tight control of
the
training loop. Most modern LLM and research code is PyTorch, so it is
the
default in this curriculum.

### The honest rule

Both compute the same math. The choice is ecosystem and ergonomics, not
capability — and the ability to read both is worth more than loyalty to
one. A
full-stack AI engineer is bilingual by necessity, not by preference.

## 8. Eager vs Graph Execution

### Two execution modes

TensorFlow has two ways to run a model. **Graph mode** builds a static
computation graph first, then executes it — the original design,
optimized for
production and portability. **Eager mode** executes operations
immediately, like
PyTorch — the modern default, friendlier for debugging. The trade is
productivity versus optimization.

### Why it matters to you

Eager is what you write in; graph is what you ship. `tf.function`
decorates a
Python function and traces it into a graph, giving you eager-style
development
with graph-style speed. Understanding the two modes explains why TF code
sometimes behaves differently under `tf.function` — a classic source of
"works in debugging, differs in production" confusion.

### The PyTorch parallel

PyTorch is eager by default and compiles opt-in via `torch.compile` (the
JAX
`jit` analogue from `44`). The direction of travel in every framework is
the
same: write eagerly, compile for speed. TF just made the split explicit
first.

## 9. TF Lite and TF Serving

### The serving ecosystem

Keras's real advantage is the deployment ecosystem. **TF Serving** hosts
a
SavedModel behind a gRPC/REST endpoint; **TF Lite** converts a model to
a small
format for mobile and embedded devices. These are mature, managed paths
that
have no PyTorch equivalent of the same age.

### The conversion trade

TF Lite trades accuracy for size by quantizing (`49`) and pruning the
graph. The
conversion is one call, but the result must be re-validated — a model
that
passes in full precision can fail the quantized edge form, which is why
the
quantization ladder (`49`) matters even when the framework hands you the
button.

### The honest comparison

PyTorch serving is increasingly strong (TorchServe, ONNX,
torch.compile), but
TF's edge story — TF Lite on phones — remains the most battle-tested
path for
mobile deployment. If the target is a phone, Keras/TF is often the
pragmatic
choice regardless of your training preference.

## 10. A Decision Procedure — Keras or PyTorch?

### The questions, in order

A short procedure removes the guesswork:

1. **Is the training loop standard?** If yes, Keras is a candidate. If you need a
   custom loop, custom gradient, or unusual loss, PyTorch.
2. **What is the serving target?** A phone or a TF Serving endpoint favors Keras;
   a PyTorch/ONNX stack favors PyTorch.
3. **What does the team already use?** Inherited codebases decide more framework
   choices than benchmarks do.
4. **Is the architecture novel or well-trodden?** Novel architectures and research
   code are PyTorch; standard supervised models are either.

### The default

When the answers are genuinely balanced, default to PyTorch — it is the
curriculum's workhorse and the dominant ecosystem for LLM tooling.
Choose Keras
when the serving target or the team's existing stack points there.

### The meta-lesson

The decision procedure matters more than the answer, because frameworks
change
and the questions do not. A team that reasons this way can adopt
whatever
framework tomorrow brings; a team that picked by fashion will
re-litigate the
choice every year.

### The porting safety net

Whichever you choose, the mapping table (`5`) is the safety net: any
model in one
framework can be expressed in the other, and the ability to translate is
the
durable skill. Framework loyalty is a liability; framework fluency is an
asset.

## Real-World Application

- **Legacy production models** — many are Keras/TF SavedModels; you inherit them
  and must serve or retrain them.
- **Edge deployment** — TF Lite converts a Keras model to a phone-sized artifact.
- **Research / LLM tooling** — PyTorch, where the loop is the product.
- **Porting a model** — moving a vision model between frameworks requires the
  channels-first/last translation above.
- **The DevMate case** — the serving target, not the GPU, decides the framework.

## Common Mistakes to Avoid

### Mistake 1: Sequential for a branching model
```
# WRONG — a residual/skip connection in a Sequential list
# CORRECT — the Functional API for any graph that is not a straight line
```

### Mistake 2: Forgetting compile before fit
```
# WRONG — model.fit(...) with no optimizer/loss configured
# CORRECT — model.compile(optimizer=..., loss=...) first
```

### Mistake 3: Expecting Keras fit to be reproducible without seeds
```
# WRONG — rerunning fit and expecting identical weights
# CORRECT — set random seeds (and note GPU nondeterminism)
```

### Mistake 4: Shape mismatch from the wrong input convention
```
# WRONG — passing (batch, channels, H, W) to a Keras Conv2D expecting channels_last
# CORRECT — Keras defaults to channels_last; set data_format or transpose
```

### Mistake 5: Confusing model.save formats
```
# WRONG — mixing H5 and SavedModel expectations
# CORRECT — know which artifact your serving stack loads
```

### Mistake 6: Assuming one framework is "faster"
```
# WRONG — choosing a framework on a benchmark that does not transfer to your task
# CORRECT — the math is the same; profile your actual workload
```

## Best Practices

1. Use Sequential for linear stacks, Functional for anything branched.
2. Always `compile` before `fit`, and name your metrics.
3. Use callbacks (EarlyStopping, ModelCheckpoint) instead of hand-rolled logic.
4. Set seeds and record them for reproducibility.
5. Pin the `data_format` (channels_first/last) explicitly.
6. Export a SavedModel for serving; keep the training script separate.
7. Match the framework to the ecosystem you deploy into.
8. Be fluent in both — read PyTorch and Keras equally well.
9. Prefer PyTorch for research and novel loops; Keras for standard pipelines.
10. Profile before assuming one framework is "faster".

## Complexity and Cost

| Operation | Time | Space | Notes |
|---|---|---|---|
| Keras fit loop | same as PyTorch | same | Ergonomics differ, math does not |
| Sequential build | negligible | graph | Declarative, shapes inferred |
| SavedModel export | seconds | artifact | Self-describing bundle |
| TF Lite conversion | seconds-minutes | smaller | Edge deployment path |

## AI Engineering Relevance

**Where this shows up:** legacy production models are often Keras/TF (SavedModels
and TF Lite edge deployments), while new research and LLM tooling is
PyTorch. A
full-stack AI engineer must read both. On this workstation both run on
the RTX
5000; the deciding factor is the serving target, not the GPU.

| Concept here | Used for |
|---|---|
| Sequential vs Functional | Choosing the right API for the graph |
| compile + fit | Understanding what the framework abstracts |
| SavedModel | Deploying to TF Serving / TF Lite |
| Framework fluency | Reading and porting either codebase |

**Scale note:** framework choice is often inherited from the team or the serving
stack, not picked fresh. The skill is translation — moving a model
between the
two without changing its behavior, which this topic's mapping table
makes
explicit.

## Key Takeaways

1. Keras is declarative (describe, then `fit`); PyTorch is explicit (write the loop).
2. `compile` configures training; `fit` runs it with callbacks.
3. Sequential is for linear stacks; Functional is for any graph.
4. The one mapping that matters is `fit` versus the hand-written loop.
5. Channels-first (PyTorch) vs channels-last (Keras) is the classic porting bug.
6. The choice is ecosystem and ergonomics, never raw capability.

## Self-Check Questions

1. What is the single abstraction that defines Keras, and what does it hide?
2. When is the Functional API required, and what can Sequential not express?
3. Why is channels-first vs channels-last the classic porting bug?
4. What is a SavedModel, and how does it differ from a PyTorch state_dict?
5. How do `compile` and `fit` map onto PyTorch's optimizer, loss, and loop?
6. When would a team inherit Keras rather than choose it, and why?

## Summary

| Concept | Description |
|---|---|
| Declarative | Describe the model; Keras runs the loop |
| Sequential API | Linear layer stacks |
| Functional API | Branching/shared layer graphs |
| compile | Bind optimizer + loss + metrics |
| fit | Run the training loop with callbacks |
| SavedModel | Self-describing serving artifact |

## Quick Reference

| Task | Idiom |
|---|---|
| Sequential model | `keras.Sequential([...])` |
| Functional model | `keras.Model(inputs=..., outputs=...)` |
| Compile | `model.compile(optimizer="adam", loss="mse")` |
| Train | `model.fit(X, y, epochs=10)` |
| Save | `model.save("path/")` (SavedModel) |

## Further Reading / Connections

- `38-neural-network-basics-lecture.md` — the layers both frameworks wrap.
- `37-pytorch-training-loop-lecture.md` — the loop Keras hides.
- `model-serving` (in `04-ai-engineering`) — deploying either artifact.
- Official docs: <https://keras.io/guides/>

## History and Motivation

The framework landscape has consolidated in waves. Theano and Caffe were
the
first deep-learning frameworks; TensorFlow 1 (2015) introduced the
static graph
and won industry adoption; Keras (2015) wrapped it with a friendly API;
TensorFlow
2 (2019) made eager execution the default and folded Keras in as
`tf.keras`.
Meanwhile PyTorch (2016) made eager execution and dynamic graphs its
identity
and won research.

The current picture is a duopoly with a division of labor: PyTorch for
research
and LLM tooling, TensorFlow/Keras for the serving and edge ecosystem it
built
first. JAX (`44`) is the emerging third option for large-scale,
functional
research. The history explains the present: framework choice is often a
consequence of which ecosystem a team joined years ago, not a fresh
technical
evaluation.

## Next Steps

Next: **[44 — JAX and Flax](44-jax-flax-lecture.md)** — functional
transforms and composable modules.

Continues in:
**[model-serving](../../../04-ai-engineering/model-serving/)** — serving
Keras and PyTorch artifacts.



