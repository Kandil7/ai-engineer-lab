# 07-machine-learning — 42: Recurrent Neural Networks — Sequences That Remember

Companion exercise: `42-rnns.py`

---

## Topic Overview

A feed-forward network maps one fixed-size input to one output; it has no memory
between calls. A recurrent neural network (RNN) processes a *sequence* by
carrying a hidden state forward at each step, so the network's output at step `t`
depends on everything before it. That recurrence is what makes RNNs the natural
fit for text, audio, and time series — data whose order matters.

The plain RNN has a fatal flaw: gradients vanish or explode over long sequences,
so it cannot learn long-range dependencies. LSTM and GRU are the two fixes that
became industry standard — gated architectures that learn what to remember and
what to forget. This topic covers the recurrence mechanics, the vanishing
gradient, the LSTM/GRU gates, and how to shape sequence data for `torch.nn`.

Modern transformers (`40-transformers-from-scratch`) have largely replaced RNNs
for language, but RNNs remain the right tool for compact streaming models — real-time
audio, sensor telemetry, and on-device sequence models where attention's
quadratic cost does not fit.

## Learning Objectives

By the end of this lecture, you will be able to:

1. Explain how recurrence carries state across sequence steps.
2. Shape sequence tensors as (batch, seq_len, features) for `torch.nn`.
3. Distinguish the plain RNN's vanishing-gradient failure from LSTM/GRU gating.
4. Describe the forget, input, and output gates of an LSTM.
5. Build an LSTM or GRU classifier in `torch.nn`.
6. Explain when an RNN beats a transformer and vice versa.
7. State why RNNs are the compact streaming choice.

## Prerequisites

| Need | Where |
|---|---|
| Tensors and autograd | `36-pytorch-tensors.py` |
| Neural network basics | `38-neural-network-basics.py` |
| Training loop | `37-pytorch-training-loop.py` |

## 1. Recurrence — State Carried Forward

### The recurrent step

At each step, an RNN cell takes the current input and the previous hidden state,
and produces a new hidden state:

```python
h_t = tanh(W_ih @ x_t + b_ih + W_hh @ h_{t-1} + b_hh)
```

The same weights `W_ih` and `W_hh` are reused at every step — recurrence is the
temporal analogue of a convolution's shared weights. The hidden state is the
network's *memory*: a running summary of the sequence so far.

### Why order matters

A feed-forward net would see tokens independently; the RNN sees them in order,
so "not good" and "good not" produce different hidden states. That order
sensitivity is exactly what sequence tasks need.

## 2. Shaping Sequence Data

### The tensor layout

PyTorch RNNs expect a 3D tensor `(batch, seq_len, features)`:

```python
import torch
import torch.nn as nn

batch, seq_len, feat = 4, 10, 8
x = torch.randn(batch, seq_len, feat)  # 4 sequences of 10 steps, 8 features
```

### The output contract

An RNN returns the output at every step plus the final hidden state:

```python
rnn = nn.RNN(input_size=8, hidden_size=16, batch_first=True)
out, h_n = rnn(x)
# out: (batch, seq_len, 16) — outputs per step
# h_n: (num_layers, batch, 16) — final hidden state
```

`batch_first=True` is the conventional choice; the default is seq-first.

## 3. The Vanishing Gradient

### The problem

Backpropagation through time multiplies gradients across every step. With
`tanh` squashing into `(-1, 1)`, the product shrinks geometrically — after 50
steps the gradient is near zero, and the network stops learning long-range
dependencies.

### Why it matters in practice

A plain RNN can learn "the last few tokens" but not "a word that appeared three
sentences ago." That is the gap LSTM and GRU close, and the reason the plain
RNN is rarely used in production.

## 4. LSTM — Gated Memory

### The three gates

An LSTM adds a *cell state* `c_t` (the long-term memory) and three gates that
control it:

- **Forget gate** — how much of the old cell state to keep.
- **Input gate** — how much new information to write in.
- **Output gate** — how much of the cell state to expose as the hidden state.

### Why gates fix vanishing gradients

The cell state is updated by *addition* through the forget and input gates,
giving the gradient a highway that does not vanish across many steps. The LSTM
learns to keep the cell state steady when a long-range dependency is at play.

## 5. GRU — The Lighter Alternative

### Two gates instead of three

The GRU (Gated Recurrent Unit) merges the cell state and hidden state and uses
two gates: a reset gate and an update gate. It learns to remember long-range
dependencies with fewer parameters than an LSTM.

### When to prefer it

GRU is the default when the dataset is small or the model must be compact — its
smaller parameter count trains slightly faster and generalizes comparably. LSTM
is the choice when maximum capacity per cell matters.

## 6. An RNN Classifier

### The stack

A sequence classifier feeds the final hidden state (or the mean over steps) into
a dense head:

```python
class SeqClassifier(nn.Module):
    def __init__(self, in_size, hid, n_classes):
        super().__init__()
        self.lstm = nn.LSTM(in_size, hid, batch_first=True)
        self.head = nn.Linear(hid, n_classes)

    def forward(self, x):
        out, (h_n, c_n) = self.lstm(x)  # h_n: (1, batch, hid)
        return self.head(h_n.squeeze(0))
```

### Choosing the pooled representation

For sequence classification you can use the last hidden state, the mean of all
outputs, or the max over time. The last hidden state is the classic choice; the
mean is more robust when the whole sequence matters.

## 7. RNN vs Transformer

### Where each wins

RNNs process a sequence in one pass with constant memory in the sequence length
— O(seq) time, O(1) state — which makes them ideal for streaming and on-device
models. Transformers attend over all pairs — O(seq²) — so they capture long-range
dependencies better but do not stream cheaply.

### The production rule

Use a transformer when the sequence is long and you have compute; use an
RNN/GRU when the model must be compact, low-latency, or process an unbounded
stream. The two are not rivals but tools matched to constraints.

## 8. Common Mistakes to Avoid

### Mistake 1: Forgetting batch_first
```
# WRONG — passing (batch, seq, feat) to an RNN with batch_first=False (default)
# CORRECT — nn.LSTM(..., batch_first=True) and keep (batch, seq, feat)
```

### Mistake 2: Using the wrong hidden-state index
```
# WRONG — out[:, -1, :] with a packed/layered RNN where h_n is the right source
# CORRECT — h_n[-1] or h_n.squeeze(0) for the top layer's final state
```

### Mistake 3: A plain RNN for long sequences
```
# WRONG — nn.RNN for sequences of hundreds of steps; gradients vanish
# CORRECT — nn.LSTM or nn.GRU for anything beyond short windows
```

### Mistake 4: Ignoring padding in variable-length batches
```
# WRONG — treating padded tokens as real signal
# CORRECT — pack_padded_sequence, or mask padded steps
```

### Mistake 5: Forgetting to reset hidden state per batch
```
# WRONG — carrying h across unrelated batches (a stale-memory bug)
# CORRECT — default None hidden state per forward, or explicit reset
```

## 9. Best Practices

1. Use `batch_first=True` and document the (batch, seq, feat) convention.
2. Reach for LSTM/GRU, not the plain RNN.
3. Prefer GRU for compact or small-data models.
4. Feed the final hidden state (or a pooled one) into the classifier head.
5. Mask or pack variable-length sequences; never train on padding as signal.
6. Clip gradients (`clip_grad_norm_`) to tame the residual explosion risk.
7. Start with one or two layers; depth is not the first lever to pull.
8. Normalize inputs; RNNs are sensitive to scale.
9. Record sequence length and vocabulary in the experiment tracker.
10. Consider a transformer only when long-range dependencies actually matter.

## 10. Complexity and Cost

| Operation | Time | Space | Notes |
|---|---|---|---|
| RNN forward | O(seq · hidden²) | hidden state | Sequential — hard to parallelize across time |
| LSTM forward | ~4x RNN | cell + hidden | More gates, more capacity |
| GRU forward | ~3x RNN | single state | Cheaper than LSTM |
| Backprop through time | O(seq · hidden²) | activations | Vanishing gradient in plain RNN |
| Transformer (baseline) | O(seq²) | attention matrix | Parallel, but quadratic |

## 11. AI Engineering Relevance

**Where this shows up:** real-time audio/keyword spotting, sensor telemetry,
streaming speech, and compact on-device sequence models. On the RTX 5000 the
constraint is not training an RNN — it is that a *transformer* may not fit a
long-sequence batch in 16 GB, where an RNN's constant memory still runs.

| Concept here | Used for |
|---|---|
| Hidden state carried forward | Streaming models with constant memory |
| LSTM/GRU gating | Long-range dependencies in compact form |
| Sequence shaping | Any text, audio, or telemetry pipeline |
| O(seq) vs O(seq²) | Choosing RNN over transformer on budget |

**Scale note:** RNNs are the streaming default precisely because memory is
O(1) in sequence length — an unbounded audio stream never outgrows the state.
That is the argument transformers lost until streaming-attention tricks arrived.

## 12. Summary

| Concept | Description |
|---|---|
| Recurrence | Hidden state carried forward at each step |
| Vanishing gradient | Gradients shrink geometrically across steps |
| LSTM | Cell state + forget/input/output gates |
| GRU | Reset + update gates, fewer parameters |
| Sequence tensor | (batch, seq_len, features) |
| O(seq) cost | Why RNNs stream and transformers don't |

## Quick Reference

| Task | Idiom |
|---|---|
| LSTM layer | `nn.LSTM(in, hid, batch_first=True)` |
| GRU layer | `nn.GRU(in, hid, batch_first=True)` |
| Final hidden | `h_n.squeeze(0)` (top layer) |
| Gradient clip | `torch.nn.utils.clip_grad_norm_(params, 1.0)` |
| Input tensor | `torch.randn(batch, seq, feat)` |

## Next Steps

Next: **[43 — TensorFlow and Keras](43-tensorflow-keras-lecture.md)** — the other framework, and when to choose it.

Continues in: **[09-genai — 21 Fine-Tuning](../../09-genai/lectures/21-fine-tuning-lecture.md)** — sequence models in production.

Official docs: <https://pytorch.org/docs/stable/generated/torch.nn.LSTM.html>
