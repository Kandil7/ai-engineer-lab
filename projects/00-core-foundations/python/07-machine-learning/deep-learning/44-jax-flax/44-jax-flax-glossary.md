# JAX and Flax — Glossary 44

Companion lecture: `44-jax-flax-lecture.md`

## Quick Reference Table

| Term | Category | One-Line Definition |
|---|---|---|
| jit | Transform | Compile a function to fast device code |
| grad | Transform | Differentiate a function automatically |
| vmap | Transform | Vectorize a function over a batch axis |
| Pure function | Style | Same input, same output, no side effects |
| Pytree | Data | A nested container of arrays (params) |
| Flax | Library | Neural-network modules on JAX's functional core |
| init | Flax | Produce the parameter dict from shapes |
| apply | Flax | Run the forward pass on parameters |
| pmap | Transform | Parallelize a function across devices |
| XLA | Compiler | The accelerator compiler behind jit |

## Detailed Definitions

### jit
**Definition**: The JAX transform that traces a function once per input shape and
compiles it to fast accelerator code, reusing the kernel on later calls.
**Example**:
```python
fast = jax.jit(predict)
fast(params, x)
```
**Related**: XLA, vmap

### grad
**Definition**: The JAX transform that returns the gradient of a function with
respect to its first argument (or `argnums`), enabling functional autodiff.
**Example**:
```python
jax.grad(loss)(params, x, y)
```
**Related**: jit, Pure function

### vmap
**Definition**: The JAX transform that lifts a function over a batch dimension,
replacing a Python loop with a single vectorized kernel.
**Example**:
```python
jax.vmap(predict, in_axes=(None, 0))(params, X_batch)
```
**Related**: jit, Pytree

### Pure function
**Definition**: A function with no side effects — same inputs always produce the
same outputs. The precondition for JAX's transforms.
**Related**: jit, grad

### Pytree
**Definition**: A nested container (dicts, lists, tuples) of arrays used to hold
parameters as a single value.
**Related**: Pure function, Flax

### Flax
**Definition**: The neural-network library for JAX providing `nn.Module`, layers,
and the `init`/`apply` split while keeping parameters an external value.
**Example**:
```python
params = MLP().init(rng, x)
out = MLP().apply(params, x)
```
**Related**: init, apply

### init / apply
**Definition**: Flax's split — `init` produces the parameter dict from the input
shape, `apply` runs the forward pass on those parameters, keeping the module pure.
**Related**: Flax, Pure function

### pmap
**Definition**: The JAX transform that parallelizes a function across multiple
accelerators, the scale story behind JAX's TPU adoption.
**Related**: jit, XLA

## Key Concepts Summary

### The three transforms
- `jit` compiles, `grad` differentiates, `vmap` vectorizes.
- They compose: `jit(vmap(grad(loss)))`.

### The philosophical split
- JAX: model = pure function; params = value.
- PyTorch: model = object; params = state.

## Practice Terms

Match each term to its definition (answers at the bottom).

1. Compile a function to fast code — ___
2. Differentiate a function automatically — ___
3. Vectorize a function over a batch — ___
4. Same input, same output, no side effects — ___
5. Nested container of arrays — ___
6. Neural modules on JAX's functional core — ___
7. Produce the parameter dict — ___
8. Parallelize across devices — ___

**Answers:** 1-jit, 2-grad, 3-vmap, 4-pure function, 5-pytree, 6-Flax,
7-init, 8-pmap
