# Model Serving 05: Inference Optimization — Quiz

> **Topic Overview**: The objective, batching, KV cache, quantization, routing, measurement.

---

## Score Tracker

| Metric | Value |
|--------|-------|
| Questions Answered | 0 / 15 |
| Correct Answers | 0 |
| Score | 0% |

---

## Questions

### Question 1

**The objective for an inference system is:**

- A) Peak tokens per second only
- B) A p95 latency SLO plus a cost ceiling plus a quality floor
- C) The largest model available
- D) Batch size 1

**Difficulty:** Easy

<details>
<summary>View Answer</summary>

**Correct Answer: B**

**Explanation:** All three numbers are declared before measuring. Speed without a cost
ceiling buys latency with money, and both without a quality floor buy it with answers.

</details>

---

### Question 2

**TTFT is composed of:**

- A) Model download time
- B) Embedding time
- C) Queueing plus prefill
- D) Decode time only

**Difficulty:** Easy

<details>
<summary>View Answer</summary>

**Correct Answer: C**

**Explanation:** The request waits in queue, then the prompt is processed in one
compute-bound prefill pass; decode starts only after the first token exists.

</details>

---

### Question 3

**The KV cache stores, for every past token:**

- A) Per-layer key and value vectors
- B) The final logits
- C) Only the query vectors
- D) The gradient state

**Difficulty:** Easy

<details>
<summary>View Answer</summary>

**Correct Answer: A**

**Explanation:** Attention for the next token needs the keys and values of everything
before it. Queries are recomputed each step, so they are never cached.

</details>

---

### Question 4

**To fit a 7B model on a 16 GB card, the biggest single lever is:**

- A) Raising the batch size
- B) Narrowing the weights with INT4 or a GGUF quant
- C) Enabling prefix caching
- D) Raising max_model_len

**Difficulty:** Easy

<details>
<summary>View Answer</summary>

**Correct Answer: B**

**Explanation:** Weights dominate resident memory at short context: about 15 GB at
16-bit against about 4 GB at 4 bits. Batching and caching add memory, they free none.

</details>

---

### Question 5

**PagedAttention, the core idea of vLLM, allocates the KV cache as:**

- A) Fixed blocks drawn from a shared pool
- B) One contiguous tensor per request
- C) Per-layer files on disk
- D) Float16-only pages

**Difficulty:** Easy

<details>
<summary>View Answer</summary>

**Correct Answer: A**

**Explanation:** Like an operating system paging virtual memory: a per-sequence block
table points into a shared pool, so fragmentation and over-reservation nearly vanish.

</details>

---

### Question 6

**Continuous batching re-forms the batch:**

- A) Once at startup
- B) At every decoding iteration
- C) Only when a request fails
- D) Once per minute

**Difficulty:** Medium

<details>
<summary>View Answer</summary>

**Correct Answer: B**

**Explanation:** After each token the scheduler admits requests whose prefill finished
and retires those that emitted their end token; no batch waits to fill or to complete.

</details>

---

### Question 7

**During the decode phase, each step is bound mainly by:**

- A) Grammar compilation
- B) Disk I/O
- C) Memory bandwidth reading weights
- D) Prompt length

**Difficulty:** Medium

<details>
<summary>View Answer</summary>

**Correct Answer: C**

**Explanation:** Every step reads every weight to emit one token per sequence, which is
why decode is memory-bound and batching amortizes that single read across requests.

</details>

---

### Question 8

**A request whose system prompt is byte-identical to a cached one gains from prefix
caching during:**

- A) Decode
- B) Postfill
- C) Prefill, so TTFT drops
- D) Quantization

**Difficulty:** Medium

<details>
<summary>View Answer</summary>

**Correct Answer: C**

**Explanation:** Prefix caching reuses KV for the shared prefix and skips that part of
the compute-bound prefill; decode cost is unchanged, the tokens must still be generated.

</details>

---

### Question 9

**FP8 reaches full speed only on hardware with:**

- A) FP8 tensor cores, Ada or Hopper
- B) GDDR6 memory
- C) More than 32 GB of VRAM
- D) A 64-bit CPU

**Difficulty:** Medium

<details>
<summary>View Answer</summary>

**Correct Answer: A**

**Explanation:** FP8 is a hardware feature lever. On Turing (sm_75, RTX 5000) there are
no FP8 tensor cores, so the levers here are INT8, INT4, and GGUF quants.

</details>

---

### Question 10

**The defining property of speculative decoding is that it:**

- A) Shrinks the KV cache
- B) Changes the output distribution
- C) Needs no target model
- D) Preserves the target model's output distribution while drafting k tokens

**Difficulty:** Medium

<details>
<summary>View Answer</summary>

**Correct Answer: D**

**Explanation:** The drafter proposes k tokens and the target verifies them in one pass
with rejection sampling, so the sampled distribution is provably the target's.

</details>

---

### Question 11

**A 7B-class model with 28 layers, 8 KV heads, head_dim 128 and fp16 KV uses, per
token:**

- A) 57,344 bytes
- B) 114,688 bytes
- C) 229,376 bytes
- D) 4,096 bytes

**Difficulty:** Hard

<details>
<summary>View Answer</summary>

**Correct Answer: B**

**Explanation:** 28 x 2 x 8 x 128 x 2 = 114,688 bytes per token per sequence: about
0.94 GB at 8192 context, about 3.76 GB at batch 4, against a 16 GB budget.

</details>

---

### Question 12

**Ollama's default Q4_K_M quant of a 7.6B model weighs about:**

- A) 1.9 GB
- B) 3.0 GB
- C) 4.6 GB
- D) 15.2 GB

**Difficulty:** Hard

<details>
<summary>View Answer</summary>

**Correct Answer: C**

**Explanation:** The 4-bit floor is 0.5 bytes per parameter, but k-quants carry scales
and super-blocks, so practice lands near 0.6: 7.6B x 0.6 is about 4.6 GB.

</details>

---

### Question 13

**A fallback ladder that omits per-hop timeouts fails how:**

- A) It can hang forever and never reach the next hop
- B) It doubles the cost of every request
- C) It disables batching
- D) It invalidates the prefix cache

**Difficulty:** Hard

<details>
<summary>View Answer</summary>

**Correct Answer: A**

**Explanation:** A hanging primary never returns, so control never reaches the cloud
hop, the cache, or the degraded terminal state. That hop also needs a budget cap.

</details>

---

### Question 14

**max_model_len rises from 4096 to 32768 at the same concurrency; the KV reservation:**

- A) Grows 8x
- B) Stays unchanged
- C) Shrinks
- D) Grows 2x

**Difficulty:** Hard

<details>
<summary>View Answer</summary>

**Correct Answer: A**

**Explanation:** Engines size the reservation as KV bytes per token times max_model_len
times concurrency, so cost scales linearly with the bound even for short prompts.

</details>

---

### Question 15

**Which failure can only the quality floor catch?**

- A) A 429 response from the API
- B) An out-of-memory error during prefill
- C) A p95 latency regression
- D) A routed downgrade that answers wrongly, but faster and cheaper

**Difficulty:** Hard

<details>
<summary>View Answer</summary>

**Correct Answer: D**

**Explanation:** Latency and cost improve exactly as routing shifts traffic to a smaller
model; only the golden-set score reveals that the answers got worse.

</details>

---

## Answer Key

| Q# | Answer | Difficulty |
|----|--------|------------|
| 1 | B | Easy |
| 2 | C | Easy |
| 3 | A | Easy |
| 4 | B | Easy |
| 5 | A | Easy |
| 6 | B | Medium |
| 7 | C | Medium |
| 8 | C | Medium |
| 9 | A | Medium |
| 10 | D | Medium |
| 11 | B | Hard |
| 12 | C | Hard |
| 13 | A | Hard |
| 14 | A | Hard |
| 15 | D | Hard |

---

## Scoring Guide

| Score | Rating | Recommendation |
|-------|--------|----------------|
| 14-15 | Expert | Model-serving section complete |
| 11-13 | Proficient | Review the KV sizing formula |
| 8-10 | Developing | Re-study batching and quantization |
| 0-7 | Novice | Restart the lecture |

---

**Previous**: [04 - HF Inference SDK](04-hf-inference-sdk-quiz.md)
