# 07-machine-learning — 44: JAX and Flax — Functional Transforms and Composability

Companion exercise: `44-jax-flax.py`

---

## Topic Overview

JAX is NumPy with three magic functions — `jit`, `grad`, and `vmap` —
built on a
single idea: your model is a *pure function* of its parameters, so the
framework
can transform it freely. `jit` compiles it, `grad` differentiates it,
`vmap`
vectorizes it, and the three compose. Flax is the neural-network layer
on top of
JAX that packages that function into reusable modules while staying
explicit.

The contrast with PyTorch is philosophical. PyTorch is object-oriented —
the
model is an object holding state. JAX is functional — the parameters are
a
plain value passed in, and the model is a pure function `params ->
predictions`.
That purity is what lets JAX's transforms compose cleanly and what makes
JAX the
emerging choice for large-scale, TPU-oriented research.

Because JAX is not installed in this environment, the exercise
demonstrates the
*functional-transform philosophy* using PyTorch's analogues (`torch.autograd.grad`,
`torch.vmap`, `torch.compile`) so the ideas are concrete, then maps them
to their
JAX counterparts. The philosophy — pure functions that transforms act on
— is
the durable lesson; the syntax is a detail.

## Learning Objectives

By the end of this lecture, you will be able to:

1. Explain the functional view: parameters as a value, model as a pure function.
2. Describe what `jit`, `grad`, and `vmap` each transform and why they compose.
3. Contrast JAX's functional style with PyTorch's object-oriented style.
4. Explain Flax's role and its `params` dict convention.
5. Use `grad` to take a derivative and `vmap` to vectorize without a loop.
6. State when JAX's TPU/large-scale strengths justify the learning curve.
7. Decide whether to adopt JAX for a given project.
8. Explain the `init`/`apply` split and why purity requires it.

## Prerequisites

| Need | Where |
|---|---|
| Tensors and autograd | `36-pytorch-tensors.py` |
| Neural network basics | `38-neural-network-basics.py` |

## 1. The Functional View

### Parameters as a value

In JAX, the model's parameters are an ordinary value — a dict or pytree
— and the
model is a function that takes parameters and input and returns output:

```python
def predict(params, x):
    return jnp.tanh(params["W"] @ x + params["b"])
```

There is no `self` holding weights. The function is *pure*: same input,
same
output, no hidden state, no side effects.

### The real-world analogy

Think of a function as a recipe card: it has no memory of previous
meals, only
instructions that turn ingredients (parameters + input) into a dish
(output).
Because the card is self-contained, you can photocopy it (vmap), hire a
faster
chef (jit), or calculate how the dish changes with the recipe (grad) —
none of
which works if the card scribbles on shared state.

### Why purity matters

Because the function is pure, JAX can transform it. `grad(predict)` is a
new
function that returns derivatives; `jit(predict)` compiles it;
`vmap(predict)`
batches it. Each transform is a function from functions to functions — a
composable algebra over your model.

### When it works, when it fails

Purity works beautifully for numerical models that are functions of
their
parameters. It grates when the model has dynamic, data-dependent control
flow
(loops whose trip count depends on the input), which JAX handles via
`lax`
primitives but which feels awkward compared to PyTorch's imperative
freedom.

## 2. The Three Transforms

### jit — just-in-time compile

`jit` traces the function once per input shape and compiles it to fast
device
code. Subsequent calls reuse the compiled kernel:

```python
fast = jax.jit(predict)
fast(params, x)  # first call compiles; later calls are fast
```

### grad — automatic differentiation

`grad` returns the gradient of a function with respect to its first
argument:

```python
loss = lambda params, x, y: jnp.mean((predict(params, x) - y) ** 2)
dloss = jax.grad(loss)
grads = dloss(params, x, y)
```

### vmap — automatic vectorization

`vmap` lifts a function over an extra batch dimension, replacing a
Python loop
with a vectorized kernel:

```python
batch_predict = jax.vmap(predict, in_axes=(None, 0))  # batch over x
outs = batch_predict(params, X_batch)
```

### They compose

`jax.jit(jax.vmap(jax.grad(loss)))` is a single, compilable training
step. That
composition is JAX's signature superpower — no other framework makes
transforms
stack so cleanly, because no other framework models the network as a
pure
function.

## 3. Flax — Modules on Top

### What Flax adds

Flax provides the neural-network conveniences JAX deliberately omits: a
`Module`
with an `apply` method, layer primitives (`nn.Dense`), and a `params`
dict
returned by `init`. It keeps the functional core — parameters stay an
external
value — while giving you familiar building blocks:

```python
import flax.linen as nn


class MLP(nn.Module):
    @nn.compact
    def __call__(self, x):
        x = nn.Dense(64)(x)
        return nn.Dense(1)(nn.relu(x))


params = MLP().init(rng, x)
out = MLP().apply(params, x)
```

### Why init/apply split

Flax separates `init` (produce the parameter dict) from `apply` (run the
forward
pass on parameters). That split keeps the module pure — the same
function can be
applied to different parameter values, which is what enables clean
`vmap` over
parameter ensembles and `grad` over parameters.

## 4. PyTorch vs JAX

### The philosophical split

PyTorch: the model is an object; `model.parameters()` returns tensors
that
autograd tracks in place. JAX: the model is a function; parameters are a
value
you pass; gradients are returned, not accumulated.

### The practical consequences

JAX's purity gives cleaner transforms and trivial parallelism across
TPUs, but it
demands a different mental model and is less ergonomic for stateful,
dynamic
Python control flow. PyTorch's object model is more intuitive and
dominates
research tooling. The choice is a trade of ergonomics for composability.

## 5. The PyTorch Analogues

### The mapping

| JAX | PyTorch analogue |
|---|---|
| `jax.jit(f)` | `torch.compile(f)` |
| `jax.grad(loss)` | `torch.autograd.grad(loss, params)` |
| `jax.vmap(f)` | `torch.vmap(f)` |
| Flax `Module.apply` | `nn.Module.forward` |
| `params` dict | `model.state_dict()` |

### Why the analogues matter

The exercise runs these PyTorch analogues so the *transform philosophy*
is
concrete even without JAX installed. The ideas — pure functions, grad,
vmap —
transfer one-to-one; only the syntax differs. Learn the ideas here, and
JAX's
syntax is a lookup away.

## 6. When JAX Wins

### The scale argument

JAX was built for TPUs and huge, parallel, XLA-compiled workloads. When
you need
to `vmap` over many seeds, `pmap`/`jit` over many devices, or express a
model as
a pure function for research, JAX's transforms pay for themselves.

### The research argument

Cutting-edge work — large model training, diffusion, reinforcement
learning with
massive parallelism — increasingly ships in JAX. If you are entering
that space,
JAX fluency is a differentiator, not a nicety.

### The honest default

For a full-stack AI engineer, PyTorch remains the workhorse; JAX is the
tool you
reach for when transforms and TPU scale are the bottleneck. Learn the
ideas, and
the syntax follows.

## 7. Pytrees and State

### Parameters as a tree

A pytree is any nested container of arrays — a dict of dicts of tensors. JAX
treats a pytree as one value, so `grad`, `jit`, and `vmap` traverse it
automatically. Your model's parameters are a pytree, which is why you can pass
"all the weights" as a single argument and get "all the gradients" back as a
matching tree.

```python
params = {"layer1": {"W": ..., "b": ...}, "layer2": {"W": ..., "b": ...}}
grads = jax.grad(loss)(params, x, y)   # grads has the same tree shape
```

### Why the tree shape matters

Because transforms preserve the pytree structure, the gradient of a nested
parameter dict is a nested gradient dict, and you update weights by walking both
trees together. This is the functional analogue of `optimizer.step()` — but
explicit, with no hidden state in an optimizer object.

### The state you cannot put in the tree

Pure functions have no hidden state, so anything stateful — the running mean in
BatchNorm, the optimizer's momentum — must be *passed in and returned out*
explicitly. Flax handles this with `Mutable` collections. This is the cost of
purity: state is visible, not hidden, which is a feature for debugging and a
burden for ergonomics.

## 8. pmap and Multi-Device

### Parallelism as a transform

Just as `vmap` vectorizes over a batch axis, `pmap` parallelizes over devices —
the same function is compiled and run on each accelerator, with the data sharded
across them. This is JAX's scale story: multi-GPU and multi-TPU training
expressed as one more function transform.

```python
# pseudocode: pmap over devices, sharding the batch dimension
parallel_step = jax.pmap(update_step, axis_name="devices")
```

### Why it composes with the others

`pmap` composes with `jit`, `grad`, and `vmap` the way they compose with each
other, because they are all transformations over pure functions. That uniformity
is the real reason JAX attracted large-scale research: going from one GPU to a
thousand TPUs is one more transform, not a rewrite.

### The honest caveat on this machine

On a single RTX 5000 there is no `pmap` across devices to exploit, so this
advantage is theoretical here. It matters when you scale to a cluster — which is
exactly the moment the JAX learning curve pays for itself.

## Real-World Application

- **Large-model research** — diffusion and RL pipelines that lean on `pmap` and
  XLA compilation.
- **Ensembles** — `vmap` over a batch of seeds to run many models in one kernel.
- **Custom autodiff** — expressing a loss and getting `grad` without a framework
  loop.
- **TPU-scale training** — where JAX's multi-device story is decisive.
- **The DevMate case** — the functional-transform mental model applies even when
  you stay on PyTorch for its ecosystem.

## Common Mistakes to Avoid

### Mistake 1: Hidden state in a "pure" function
```
# WRONG — a function that mutates a global or relies on iteration order
# CORRECT — parameters passed in, no side effects, same in -> same out
```

### Mistake 2: Confusing grad's argument convention
```
# WRONG — expecting grad to return the derivative wrt the second argument
# CORRECT — jax.grad differentiates wrt the FIRST argument; use argnums for others
```

### Mistake 3: Forgetting vmap's in_axes
```
# WRONG — vmap over a function whose batch axis is assumed
# CORRECT — specify in_axes=(None, 0) to batch over the data, not the params
```

### Mistake 4: Rewriting the loop instead of vmapping
```
# WRONG — a Python for-loop over the batch where vmap gives a vectorized kernel
# CORRECT — lift the function with vmap
```

### Mistake 5: Overlooking the compile warm-up
```
# WRONG — judging jit speed on the first, uncompiled call
# CORRECT — measure steady-state after the first trace/compile
```

### Mistake 6: Forgetting JAX's functional no-in-place rule
```
# WRONG — in-place updates (x[i] = ...) which break JAX's purity contract
# CORRECT — use .at[i].set(...) or build new arrays
```

## Best Practices

1. Write models as pure functions of `(params, x)`.
2. Compose transforms — `jit(vmap(grad(loss)))` — rather than calling separately.
3. Use Flax's `init`/`apply` split to keep modules pure.
4. Specify `in_axes`/`out_axes` explicitly in `vmap`.
5. Use `argnums` in `grad` when differentiating a non-first argument.
6. Benchmark after the compile warm-up, not before.
7. Keep parameters in a pytree/dict for clean serialization.
8. Reach for JAX when TPU scale or transform composition is the bottleneck.
9. Stay with PyTorch for dynamic control flow and ecosystem tooling.
10. Learn the ideas first; syntax is a detail.

## Complexity and Cost

| Operation | Time | Space | Notes |
|---|---|---|---|
| jit first call | high (trace + compile) | — | One-time; amortize over calls |
| jit steady-state | low | — | Compiled kernel reuse |
| grad | one backward pass | graph | Functional, no in-place state |
| vmap | one vectorized pass | batched | Replaces a Python loop |
| pmap across TPUs | parallel | per-device | JAX's scale story |

## AI Engineering Relevance

**Where this shows up:** large-scale model training and TPU research. On this
workstation (a single RTX 5000, no TPU) the practical value of JAX is
narrower,
but the *functional-transform mental model* — model as pure function,
grad and
vmap as composable transforms — sharpens how you reason about any
framework.

| Concept here | Used for |
|---|---|
| Model as pure function | Clean `vmap` over seeds/ensembles |
| grad transform | Custom loss differentiation |
| vmap | Replacing Python loops with kernels |
| init/apply split | Pure, reusable modules |

**Scale note:** JAX's advantage is XLA compilation and multi-device `pmap`, which
matters at TPU-pod scale. For a 16 GB single GPU, the transforms still
apply but
the ecosystem overhead may not justify the switch — a decision, not a
default.

## Key Takeaways

1. In JAX, the model is a pure function and parameters are a value you pass in.
2. `jit` compiles, `grad` differentiates, `vmap` vectorizes — and they compose.
3. Purity is what makes `jit(vmap(grad(loss)))` a valid, compilable expression.
4. Flax adds modules with an `init`/`apply` split while staying functional.
5. JAX wins at TPU scale; PyTorch remains the ergonomic default.
6. The functional-transform mental model sharpens reasoning in any framework.

## Self-Check Questions

1. Why does making the model a pure function enable transform composition?
2. What is the difference between `jit`, `grad`, and `vmap`, and what does each return?
3. Why does Flax separate `init` from `apply`?
4. How does JAX's "no in-place mutation" rule change how you write code?
5. When does JAX's overhead not justify the switch from PyTorch?
6. What is the PyTorch analogue of each JAX transform?

## Summary

| Concept | Description |
|---|---|
| Functional view | Parameters are a value; model is a pure function |
| jit | Compile a function to fast device code |
| grad | Differentiate a function automatically |
| vmap | Vectorize a function over a batch |
| Flax | Modules (init/apply) on JAX's functional core |
| Composition | Transforms stack: jit(vmap(grad(...))) |

## Quick Reference

| Task | JAX idiom | PyTorch analogue |
|---|---|---|
| Compile | `jax.jit(f)` | `torch.compile(f)` |
| Gradient | `jax.grad(loss)(p, x)` | `torch.autograd.grad(loss, p)` |
| Vectorize | `jax.vmap(f, in_axes=(None,0))` | `torch.vmap(f)` |
| Module | `MLP().apply(params, x)` | `model(x)` |

## Further Reading / Connections

- `36-pytorch-tensors-lecture.md` — the autograd JAX's `grad` generalizes.
- `38-neural-network-basics-lecture.md` — the layers Flax provides.
- Official docs: <https://jax.readthedocs.io/> and <https://flax.readthedocs.io/>

## Next Steps

Next: **[45 — Data Augmentation](45-data-augmentation-lecture.md)** —
synthesizing more training signal.

Continues in: **[09-genai — 21
Fine-Tuning](../../09-genai/lectures/21-fine-tuning-lecture.md)** —
where framework choice recurs.

