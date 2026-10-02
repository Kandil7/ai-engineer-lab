# Recurrent Neural Networks — Glossary 42

Companion lecture: `42-rnns-lecture.md`

## Quick Reference Table

| Term | Category | One-Line Definition |
|---|---|---|
| Backprop through time | Training | Unrolling the recurrence and propagating gradients across steps |
| Cell state | LSTM | The long-term memory channel of an LSTM |
| GRU | Architecture | A two-gate recurrent cell, lighter than LSTM |
| Hidden state | RNN | The running summary carried forward between steps |
| LSTM | Architecture | Gated recurrent cell with cell state and three gates |
| Recurrence | Mechanism | Reusing the same weights across sequence steps |
| Sequence | Data | Ordered input whose arrangement carries meaning |
| Vanishing gradient | Problem | Gradients shrinking geometrically across long sequences |
| Forget gate | LSTM | Decides how much of the old cell state to keep |
| batch_first | Convention | (batch, seq_len, features) tensor layout |

## Detailed Definitions

### Backprop through time
**Definition**: Training a recurrent network by unrolling it across the sequence
steps and backpropagating the loss through every step, multiplying gradients at
each recurrence.
**Example**:
```python
loss.backward()  # gradients flow back across all sequence steps
```
**Related**: Vanishing gradient, Recurrence

### Cell state
**Definition**: The LSTM's separate long-term memory channel, updated by addition
through the forget and input gates so its gradient does not vanish across steps.
**Related**: LSTM, Hidden state

### GRU
**Definition**: Gated Recurrent Unit — a recurrent cell with reset and update
gates that merges cell and hidden state, learning long-range dependencies with
fewer parameters than an LSTM.
**Example**:
```python
nn.GRU(input_size, hidden_size, batch_first=True)
```
**Related**: LSTM, Hidden state

### Hidden state
**Definition**: The vector carried forward between sequence steps, encoding the
network's running summary of the sequence so far.
**Related**: Recurrence, Cell state

### LSTM
**Definition**: Long Short-Term Memory — a recurrent cell that adds a cell state
controlled by forget, input, and output gates, fixing the vanishing gradient for
long-range dependencies.
**Example**:
```python
out, (h_n, c_n) = nn.LSTM(in, hid, batch_first=True)(x)
```
**Related**: GRU, Cell state

### Recurrence
**Definition**: Applying the same weights at every sequence step, feeding the
previous hidden state back in — the temporal analogue of a convolution's shared
weights.
**Related**: Hidden state, Backprop through time

### Sequence
**Definition**: Ordered data whose arrangement carries meaning — text, audio,
sensor readings. The reason order-sensitivity is needed.
**Related**: Recurrence, Hidden state

### Vanishing gradient
**Definition**: The failure mode where gradients shrink geometrically as they are
multiplied across many steps, so the network stops learning long-range
dependencies. Fixed by LSTM/GRU gating.
**Related**: Backprop through time, LSTM

### batch_first
**Definition**: The tensor-layout convention (batch, seq_len, features) chosen
with `batch_first=True` so tensors read naturally.
**Example**:
```python
x = torch.randn(4, 10, 8)  # batch 4, seq 10, features 8
```
**Related**: Sequence

## Key Concepts Summary

### The core loop
- `h_t = tanh(W_ih @ x_t + b_ih + W_hh @ h_{t-1} + b_hh)`

### LSTM vs GRU
- LSTM: cell state + 3 gates — maximum capacity.
- GRU: 2 gates, no separate cell state — lighter, comparable quality.

### Why RNNs still matter
- O(seq) time, O(1) state — streaming and on-device friendly.

## Practice Terms

Match each term to its definition (answers at the bottom).

1. The running summary carried between steps — ___
2. Unrolling recurrence to train across steps — ___
3. LSTM's long-term memory channel — ___
4. The two-gate lighter recurrent cell — ___
5. Gradients shrinking over long sequences — ___
6. The (batch, seq, features) layout — ___
7. Reusing weights across sequence steps — ___
8. Ordered data whose arrangement matters — ___

**Answers:** 1-hidden state, 2-backprop through time, 3-cell state, 4-GRU,
5-vanishing gradient, 6-batch_first, 7-recurrence, 8-sequence
