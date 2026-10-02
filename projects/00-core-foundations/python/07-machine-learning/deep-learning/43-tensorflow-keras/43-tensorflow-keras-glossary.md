# TensorFlow and Keras — Glossary 43

Companion lecture: `43-tensorflow-keras-lecture.md`

## Quick Reference Table

| Term | Category | One-Line Definition |
|---|---|---|
| Sequential API | Keras | Linear stack of layers applied in order |
| Functional API | Keras | Layers as callables, enabling branched/shared graphs |
| compile | Keras | Bind optimizer, loss, and metrics before training |
| fit | Keras | Run the training loop with callbacks |
| Callback | Keras | A hook into the training loop (EarlyStopping, checkpoint) |
| SavedModel | Artifact | Self-describing model bundle for serving |
| Declarative | Style | Describe the model; the framework runs the loop |
| Explicit | Style | Write the loop yourself (PyTorch) |
| TF Lite | Edge | Converted model format for mobile/edge inference |
| Layer | Keras | A building block with weights and a forward pass |

## Detailed Definitions

### Sequential API
**Definition**: The Keras API for linear stacks — a list of layers applied one
after another. Shapes are inferred from the first input.
**Example**:
```python
keras.Sequential([keras.layers.Dense(64, activation="relu"), keras.layers.Dense(1)])
```
**Related**: Functional API, Layer

### Functional API
**Definition**: The Keras API that treats layers as callables, letting you build
branched, merged, and shared graphs that Sequential cannot express.
**Example**:
```python
x = keras.layers.Dense(64)(inputs)
```
**Related**: Sequential API, Layer

### compile
**Definition**: The Keras call that binds an optimizer, loss, and metrics to a
model — configuring, not running, training.
**Example**:
```python
model.compile(optimizer="adam", loss="mse")
```
**Related**: fit, Callback

### fit
**Definition**: The Keras call that runs the training loop — batching, forward,
backward, optimizer step, and metric logging — hidden behind callbacks.
**Example**:
```python
model.fit(X_train, y_train, epochs=10)
```
**Related**: compile, Callback

### Callback
**Definition**: A hook invoked at points in the training loop — `EarlyStopping`,
`ModelCheckpoint`, learning-rate schedules — so you get loop control without
writing the loop.
**Related**: fit, compile

### SavedModel
**Definition**: The self-describing export format for a trained Keras/TF model —
graph plus weights in one directory that a serving stack can load without the
training code.
**Related**: TF Lite, fit

### Declarative
**Definition**: The programming style where you describe what you want and the
framework implements how — Keras's `fit` versus a hand-written loop.
**Related**: Explicit

### Explicit
**Definition**: The style where you write every step of the loop yourself —
PyTorch's optimizer.zero_grad / loss.backward / opt.step.
**Related**: Declarative

### TF Lite
**Definition**: The converted, reduced model format for mobile and embedded
deployment, trading accuracy for size and latency.
**Related**: SavedModel

## Key Concepts Summary

### The mapping that matters
- `Dense(n)` ↔ `nn.Linear`
- `compile` ↔ choosing optimizer + loss
- `fit` ↔ the hand-written training loop

### The decision
- Keras: standard tasks, TF serving, low ceremony.
- PyTorch: research, novel loops, LLM tooling.

## Practice Terms

Match each term to its definition (answers at the bottom).

1. Linear stack of layers — ___
2. Layers as callables for branched graphs — ___
3. Bind optimizer + loss + metrics — ___
4. Run the training loop — ___
5. A hook into the training loop — ___
6. Self-describing serving artifact — ___
7. Describe the model, framework runs the loop — ___
8. Write the loop yourself — ___

**Answers:** 1-Sequential API, 2-Functional API, 3-compile, 4-fit,
5-callback, 6-SavedModel, 7-declarative, 8-explicit
