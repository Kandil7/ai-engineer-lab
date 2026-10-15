# 07-machine-learning — 40: Transformers From Scratch — Attention Is All You Need

Companion exercise: `40-transformers-from-scratch.py`

---

## Topic Overview

Every LLM you will ever serve — GPT, Claude, LLaMA — is a stack of transformer
blocks. The transformer replaced recurrence with **attention**: a mechanism
where every token exchanges information with every other token, weighted by
relevance. Implementing attention yourself demystifies the whole GenAI stack:
what a context window is, why long contexts cost so much, what "attention"
actually computes, and why KV caches and sliding windows exist.

This topic builds the transformer from first principles: scaled dot-product
attention, the sqrt(d_k) scaling, multi-head attention, positional encoding,
and the complete transformer block with residuals and layer norm. The quadratic
cost story — O(S^2) in sequence length — is not a footnote; it is the single
most important engineering fact about modern LLMs.

## Learning Objectives

By the end of this lecture, you will be able to:

1. Write scaled dot-product attention from the equation.
2. Explain why scores are scaled by sqrt(d_k).
3. Implement multi-head attention with projection matrices.
4. Explain why positional encoding is necessary.
5. Assemble a complete transformer block (attention + FFN + residuals + norm).
6. State why attention cost grows quadratically with sequence length.
7. Explain how this architecture powers modern LLMs.
8. Read the shape flow through every layer of the block.

## Prerequisites

| Need | Where |
|---|---|
| Tensors and autograd | `36-pytorch-tensors.py` |
| The training loop | `37-pytorch-training-loop.py` |
| Neural network basics | `38-neural-network-basics.py` |
| Linear algebra (matmul) | `03-libraries/numpy/lectures/33-linear-algebra-lecture.md` |

## 1. Scaled Dot-Product Attention — The Core Equation

```python
def scaled_dot_product_attention(Q, K, V, mask=None):
    d_k = Q.shape[-1]
    scores = torch.matmul(Q, K.transpose(-2, -1)) / math.sqrt(d_k)
    if mask is not None:
        scores = scores.masked_fill(mask == 0, float("-inf"))
    weights = torch.softmax(scores, dim=-1)
    return torch.matmul(weights, V)
```

Output:
```
output shape: (1, 1, 4, 8)   # (batch, heads, seq, d_k)
```

Attention(Q, K, V) = softmax(QK^T / sqrt(d_k)) V. Each query scores every key
(how relevant is token j to token i?), the scores become a distribution over
keys, and the output is the weighted sum of values. Every token attends to
every other token — this is why it is called "self"-attention when Q=K=V.

## 2. Why Scale by sqrt(d_k)?

```python
scores_small = torch.randn(4, 4)  # d_k = 2
scores_large = torch.randn(4, 4) * math.sqrt(128)  # d_k = 128
```

Output:
```
small d: softmax entropy 1.315
large d: softmax entropy 0.402   # saturated -> near one-hot -> dead gradients
```

Dot products grow with dimension (sum of d_k products), and large logits push
softmax into near-one-hot distributions with tiny gradients. Dividing by
sqrt(d_k) keeps the logits at unit variance, preserving gradient flow.

## 3. Multi-Head Attention — Parallel Subspaces

```python
class MultiHeadAttention(nn.Module):
    def __init__(self, d_model, n_heads):
        super().__init__()
        assert d_model % n_heads == 0
        self.d_model, self.n_heads = d_model, n_heads
        self.d_k = d_model // n_heads
        self.W_q, self.W_k, self.W_v, self.W_o = (nn.Linear(d_model, d_model) for _ in range(4))

    def _split(self, x):
        B, S, _ = x.shape
        return x.view(B, S, self.n_heads, self.d_k).transpose(1, 2)

    def forward(self, x):
        Q, K, V = self._split(self.W_q(x)), self._split(self.W_k(x)), self._split(self.W_v(x))
        attn = scaled_dot_product_attention(Q, K, V)
        B, H, S, _ = attn.shape
        return self.W_o(attn.transpose(1, 2).contiguous().view(B, S, self.d_model))
```

Output:
```
input  (2, 10, 64) -> output (2, 10, 64)
```

Instead of one attention function, the model runs h parallel ones in different
subspaces (each head with d_model/h dimensions), then concatenates and projects
back. Different heads learn different relationships — syntax, co-reference,
position — which is why the plural "heads" matters.

## 4. Positional Encoding — Inject Order

```python
def positional_encoding(seq_len, d_model):
    pe = torch.zeros(seq_len, d_model)
    pos = torch.arange(seq_len).unsqueeze(1).float()
    div = torch.exp(torch.arange(0, d_model, 2).float() * (-math.log(10000.0) / d_model))
    pe[:, 0::2] = torch.sin(pos * div)
    pe[:, 1::2] = torch.cos(pos * div)
    return pe.unsqueeze(0)
```

Output:
```
shape (1, 20, 64); sin/cos pattern distinguishes token positions
row 0 vs row 1 distance: 1.105
```

Attention is permutation-invariant — it would treat a sentence and its word
scramble identically. Positional encoding adds a deterministic sin/cos signal
per position so the model knows token order. (Modern LLMs use learned
rotary/ALiBi variants, but the purpose is identical.)

## 5. The Transformer Block — Attention + FFN + Residuals

```python
class TransformerBlock(nn.Module):
    def __init__(self, d_model, n_heads, ff_dim):
        super().__init__()
        self.attn = MultiHeadAttention(d_model, n_heads)
        self.norm1 = nn.LayerNorm(d_model)
        self.ff = nn.Sequential(nn.Linear(d_model, ff_dim), nn.ReLU(), nn.Linear(ff_dim, d_model))
        self.norm2 = nn.LayerNorm(d_model)

    def forward(self, x):
        x = x + self.attn(self.norm1(x))  # pre-norm attention + residual
        x = x + self.ff(self.norm2(x))  # pre-norm FFN + residual
        return x
```

Output:
```
(2, 10, 64) -> (2, 10, 64)
```

Each block: layer-norm, attention, residual add; layer-norm, feed-forward
(expand -> ReLU -> contract), residual add. Residuals let gradients flow around
the attention/FFN sublayers — the fix for the vanishing-gradient problem from
topic 38. Pre-norm (norm before the sublayer) is the modern default.

## 6. Quadratic Scaling — The Cost Story

```python
for s in [100, 1_000, 10_000, 100_000]:
    print(s, s * s)
```

Output:
```
seq    100:     10,000 token pairs
seq  1,000:  1,000,000 token pairs
seq 10,000: 100,000,000 token pairs
seq 100,000: 10,000,000,000 token pairs
```

The attention matrix is S x S: memory and compute grow quadratically with
sequence length. This single fact explains context-window limits, KV-cache
memory pressure, chunking in RAG, sliding-window attention, and why long
contexts are priced so high. It is the most important engineering constraint
in LLM systems.

## 7. From Block to LLM

A modern LLM stacks dozens of these blocks, adds an embedding layer and an
output head, and trains on next-token prediction. The "context window" is the
S in the quadratic story; the "KV cache" stores K and V across generation steps
so each new token attends to history without recomputing; and the many
engineering tricks in GenAI production — chunking, caching, reranking — exist
to respect the O(S^2) budget.

## 8. Common Mistakes to Avoid

### Mistake 1: Forgetting the sqrt(d_k) scaling
```
# WRONG — unnormalized dot products saturate softmax in large dims
scores = torch.matmul(Q, K.transpose(-2, -1))
# CORRECT
scores = torch.matmul(Q, K.transpose(-2, -1)) / math.sqrt(Q.shape[-1])
```

### Mistake 2: Wrong shapes in the matmul
```
# WRONG — Q @ K with K un-transposed: (S, d) @ (S, d) fails
# CORRECT — scores[i, j] = Q[i] . K[j] via Q @ K^T
```

### Mistake 3: Reshaping heads without .transpose(1, 2)
```
# WRONG — view(B, S, H, d) keeps heads inside the sequence dim
# CORRECT — view then transpose so heads are the 2nd dim
```

### Mistake 4: Skipping the residual connections
```
# WRONG — deep stacks re-accumulate vanishing gradients
# CORRECT — x = x + attn(norm(x))
```

### Mistake 5: Ignoring O(S^2) in system design
```
# WRONG — throw the whole corpus into one context
# CORRECT — chunk, retrieve, cache; design around the quadratic budget
```

## 9. Best Practices

1. Verify shapes at every layer with a tiny dummy input (2, 5, 8).
2. Scale scores by sqrt(d_k); test with and without on a small case.
3. Use pre-norm + residual as the default block layout.
4. Keep heads as a separate dimension: view -> transpose -> attend -> merge.
5. Implement in float32 first; optimize later.
6. Test attention weights sum to 1 along the key dimension.
7. Add a causal mask for decoder (autoregressive) use.
8. Measure memory growth vs sequence length to see the quadratic curve.
9. Reuse the block in a stack; residuals + norms make depth safe.
10. Read real implementations (PyTorch's `nn.MultiheadAttention`, FlashAttention) after building yours.

## 10. Complexity and Cost

| Operation | Time | Space | Notes |
|---|---|---|---|
| Attention scores QK^T | O(S^2 x d) | O(S^2) | The quadratic term |
| Softmax over keys | O(S^2) | O(S^2) | Same shape |
| Weighted sum AV | O(S^2 x d) | O(S^2) | — |
| FFN per token | O(S x d x ff) | O(S x d) | Linear in S |
| Total block | O(S^2 x d) | O(S^2 + S x d) | Dominated by attention |

FlashAttention reduces the *memory* to O(S) by not materializing the S x S
matrix; the compute stays O(S^2). Sequence length is the variable to manage.

## 11. AI Engineering Relevance

**Where this shows up:** this architecture is the entire LLM ecosystem — the
models you call, the embeddings you index, the agents you orchestrate.
Understanding it directly explains GenAI production facts: why context windows
are limited, why KV caches consume VRAM, why RAG chunks documents, and why
rerankers are cross-attention machines.

| Concept here | Used for |
|---|---|
| O(S^2) attention | Choosing chunk sizes and context budgets in RAG |
| Q/K/V | Understanding KV-cache memory in inference engines |
| Multi-head | Why embeddings capture multiple semantic aspects |
| Positional encoding | Understanding rotary embeddings in modern LLMs |
| Residuals + norms | Why deep LLMs train stably; LoRA lives on top |

**Scale note:** the O(S^2) term is why serving a 100k-token context costs more
than 1000x a 100-token one. Cost models, caching layers, and chunking
strategies in `09-genai/18-caching-and-cost` all exist to fight this curve.

## 12. Summary

| Concept | Description |
|---|---|
| Attention | softmax(QK^T/sqrt(d_k)) V — tokens exchange information |
| Scaling | sqrt(d_k) prevents softmax saturation |
| Multi-head | Parallel attention subspaces, richer patterns |
| Positional encoding | Adds order; attention is permutation-invariant |
| Block | Attention + FFN + residual + layer norm (pre-norm) |
| O(S^2) | The cost fact behind every LLM engineering decision |

## Quick Reference

| Task | Idiom |
|---|---|
| Attention | `softmax(Q @ K^T / sqrt(d_k)) @ V` |
| Scale | `math.sqrt(Q.shape[-1])` |
| Split heads | `x.view(B, S, H, d_k).transpose(1, 2)` |
| Merge heads | `attn.transpose(1, 2).contiguous().view(B, S, d_model)` |
| Positions | sin/cos table added to embeddings |
| Block | `x = x + attn(norm(x)); x = x + ff(norm(x))` |
| Cost check | `s * s` token pairs for sequence length s |

## Next Steps

Next: **[09-genai — 01 LLM Fundamentals](../../09-genai/lectures/01-llm-fundamentals-lecture.md)** — tokenization, context windows, generation.

Continues in: **[09-genai — 06 Embeddings](../../09-genai/lectures/06-embeddings-lecture.md)** — encoders built on this stack.

Official docs: <https://arxiv.org/abs/1706.03762> · <https://pytorch.org/docs/stable/generated/torch.nn.MultiheadAttention.html>
