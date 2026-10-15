# Model Serving 05: Inference Optimization — Glossary

## Quick Reference Table

| Term | Definition | Key Point |
|------|-----------|-----------|
| Activation quantization | Quantizing activations as well as weights | Needs calibration; higher risk |
| AWQ | Activation-aware 4-bit weight quantization | Protects salient channels |
| Continuous batching | Re-forming the batch at every decoding step | The throughput win |
| Cost per 1k tokens | Amortized or list price per thousand tokens | Measured, not theoretical |
| Decode phase | Emitting one token per step per sequence | Memory-bound |
| Fallback ladder | local -> cloud -> cached -> degraded terminal | Every hop needs a timeout |
| FP8 | 8-bit floating point storage and math | Needs Ada/Hopper tensor cores |
| GGUF / Q4_K_M | llama.cpp block-wise quant format, Ollama default | ~0.6 bytes/param in practice |
| GPTQ | Calibration-based post-training INT4 quantization | Per-group error compensation |
| Grammar-constrained decoding | Masking tokens to a regex/EBNF language | Same mechanism as JSON schema |
| INT4 / INT8 weight-only | Weights stored narrow, computed wider | Biggest memory lever |
| Iteration-level scheduling | Admit/retire requests after each token | Definition of continuous batching |
| KV cache | Per-layer K and V vectors for every past token | Grows with seq_len x batch |
| KV-cache quantization | Storing the cache in fp8/int8 | Halves cache, keeps weight fidelity |
| max_model_len | Longest sequence the engine will serve | Sizes the KV reservation |
| Model routing | Sending each request to small/mid/strong | Needs router evaluation |
| Ollama | llama.cpp-based local GGUF runner | Development path, not concurrency |
| PagedAttention | KV cache in fixed blocks from a shared pool | vLLM's core idea |
| Perplexity delta | Quantized perplexity minus baseline | Cheap gate, not sufficient alone |
| Prefix caching | Reusing KV for a shared prompt prefix | Saves prefill only |
| Prefill phase | Reading the prompt, building the KV cache | Compute-bound, sets TTFT |
| Quality floor | Minimum golden-set score for a change | Blocks "fast but wrong" |
| RadixAttention | Prefix KV sharing via a radix tree | SGLang's core idea |
| Speculative decoding | Draft k tokens, target verifies in one pass | Output distribution preserved |
| Structured output | Schema/grammar-constrained generation | Format guaranteed, semantics not |
| TGI | Hugging Face Text Generation Inference server | Grammar parameter since 1.4.3 |
| TTFT | Time to first token | Queueing plus prefill |
| vLLM | High-throughput serving engine | PagedAttention plus continuous batching |
| Weight-only quantization | Only the weights are narrowed | Accuracy risk is task-dependent |

---

## Detailed Definitions

### Activation quantization

**Definition:** Quantizing the activations (the intermediate tensors flowing between
layers) in addition to the weights, usually to 8 bits. It enables narrower compute
paths rather than only narrower memory reads, but activation outliers make it more
sensitive than weight-only quantization, so it needs calibration data.

**Example:**
```python
# weight-only: store narrow, compute wide
y = matmul(x_fp16, w_int8_dequantized_to_fp16)

# W8A8: both sides narrow, hardware can run INT8 end to end
y = matmul(x_int8, w_int8)
```

**Related Terms:** Weight-only quantization, INT4 / INT8, FP8

**Key Facts:**
- Weight-only shrinks reads; activation quantization also narrows the math
- On Turing (sm_75) the practical paths are INT8/INT4, not FP8

---

### AWQ

**Definition:** Activation-aware weight quantization. It identifies the salient weight
channels by looking at activation magnitudes on a small calibration set, keeps those
channels at higher precision, and packs the rest at 4 bits. The result is 4-bit
weights with a small accuracy cost and kernels that run well on ordinary GPUs.

**Example:**
```text
model = awq_quantize(model, calibration_batch)   # conceptually
# ship: 7.6B x ~0.5 bytes/param ~= 4 GB of weights
```

**Related Terms:** GPTQ, Weight-only quantization, Perplexity delta

**Key Facts:**
- Post-training: no fine-tuning, minutes to hours on a calibration set
- Verify with perplexity delta and task eval regardless of method

---

### Continuous batching

**Definition:** Serving at iteration granularity: after every generated token the
scheduler decides who joins (a request that just finished prefill) and who leaves (a
request that emitted its end token). Batches are never waited on or run to completion
as fixed units.

**Example:**
```text
step 10: [A B C D]   C finishes -> E joins at step 11
step 11: [A B D E]   A finishes -> F joins at step 12
```

**Related Terms:** Iteration-level scheduling, Static batching, vLLM

**Key Facts:**
- Removes wait-to-fill, head-of-line blocking, and padding waste
- Ollama lacks it at production concurrency (Model Serving 02)

---

### Cost per 1k tokens

**Definition:** The money a thousand output tokens costs on a given path. For a hosted
API it is the list price; for a self-hosted GPU it is amortized hardware plus power
divided by the tokens actually served per hour.

**Example:**
```python
cost_per_1k = (gpu_amortized_per_hour / measured_tokens_per_hour) * 1000
```

**Related Terms:** Quality floor, TTFT, Objective

**Key Facts:**
- Use measured throughput, never the vendor's peak number
- Batching and prefix caching both lower it; quantization lowers it further

---

### Decode phase

**Definition:** The generation loop that emits one token per step per sequence. Each
step must read every weight in the model, so decode is memory-bound and gets faster in
aggregate as sequences are batched into the same weight read.

**Example:**
```text
step: read weights once -> produce next token for sequences A, B, C
```

**Related Terms:** Prefill phase, Continuous batching, TTFT

**Key Facts:**
- Sets tokens per second, the throughput metric
- KV reads grow with context length; weight reads do not

---

### Fallback ladder

**Definition:** The ordered degradation path a request takes when a model fails or
times out: local model, then cloud model, then cached answer, then an honest degraded
terminal state. Every hop carries a timeout, and the paid hop carries a budget cap.

**Example:**
```text
request -> local 7B -timeout-> cloud -timeout-> cached -> degraded response
```

**Related Terms:** Model routing, TTFT, Quality floor

**Key Facts:**
- A hop without a timeout can hang forever and never fall back
- The cloud hop needs a cost cap or an outage becomes an invoice
- The terminal state must be explicit; never fabricate a citation

---

### FP8

**Definition:** An 8-bit floating point format (E4M3 for weights, E5M2 for gradients
and sometimes activations). It halves memory against fp16 and runs at full speed only
on hardware with FP8 tensor cores: Ada and Hopper.

**Example:**
```text
H100 / Ada: FP8 tensor cores -> storage and math win
RTX 5000 (Turing, sm_75):     -> no FP8 tensor cores, conversions only
```

**Related Terms:** INT8, Activation quantization, KV-cache quantization

**Key Facts:**
- It is a hardware feature lever, not a universal free lunch
- On this workstation INT8/INT4/GGUF are the real levers

---

### GGUF / Q4_K_M

**Definition:** The file format (GGUF) and quantization family (k-quants) used by
llama.cpp and therefore by Ollama. Q4_K_M mixes 4-bit blocks with importance-scaled
super-blocks; "M" is the medium quality point in the Q2_K to Q6_K range.

**Example:**
```text
qwen2.5-coder:7b (Ollama default) -> Q4_K_M, ~4.6 GB file for 7.6B params
# that is ~0.6 bytes/param, not 0.5: scales and mixed blocks add overhead
```

**Related Terms:** Ollama, Weight-only quantization, AWQ

**Key Facts:**
- Deployment format for local dev; engines like vLLM prefer AWQ/GPTQ/HQQ
- The ideal 0.5 bytes/param is a floor, not a file size

---

### GPTQ

**Definition:** Post-training quantization that minimizes layer output error using
second-order information from a calibration set, quantizing weights group by group
with per-group scales. The standard 4-bit alternative to AWQ.

**Example:**
```text
gptq = quantize(model, bits=4, group_size=128, calibration=calib_batch)
```

**Related Terms:** AWQ, Weight-only quantization, Perplexity delta

**Key Facts:**
- Error compensation is why it beats naive rounding
- Ship it behind the same eval gate as any other 4-bit choice

---

### Grammar-constrained decoding

**Definition:** Restricting generation to a formal language given as a regular
expression or EBNF grammar. The engine compiles the grammar to an automaton and masks
the logits at each step so only tokens inside the language remain selectable.

**Example:**
```python
# TGI grammar parameter (since 1.4.3), compiled via outlines then cached
client.generate(prompt, grammar={"type": "regex", "value": r"\d{3}-\d{4}"})
```

**Related Terms:** Structured output, JSON schema, TGI

**Key Facts:**
- Same masking mechanism as JSON-schema constraints, more expressive input
- When grammar and model intent disagree, output can be valid yet degenerate

---

### INT4 / INT8 weight-only quantization

**Definition:** Storing weights at 4 or 8 bits while computing in a wider type after
dequantization, or in narrow integer paths where hardware allows. It attacks the
dominant decode cost, reading weights, without touching activations.

**Example:**
```python
weights_gb = params_b * bytes_per_param  # 7.6 B x 2 = 15.2 GB at 16-bit
assert params_b * 0.5 < weights_gb  # 4-bit is ~3.8 GB ideal
```

**Related Terms:** AWQ, GPTQ, Activation quantization

**Key Facts:**
- INT8 is the low-risk first step; INT4 is the big lever with real risk
- The accuracy cost is task-dependent; measure it, never assume it

---

### Iteration-level scheduling

**Definition:** The scheduling granularity behind continuous batching: the admit/retire
decision is taken after every decoding iteration rather than once per batch. It is the
mechanism, continuous batching the policy.

**Example:**
```text
for each token step:
    admit(prefill_done_requests) ; retire(finished_requests) ; run_batch()
```

**Related Terms:** Continuous batching, Orca-style serving, vLLM

**Key Facts:**
- Lets a request join mid-stream instead of waiting for the next batch
- Combined with chunked prefill, it keeps p95 flat under long prompts

---

### KV cache

**Definition:** The per-layer key and value vectors of every token processed so far,
kept so attention for the next token does not recompute the entire prefix. Its size is
`layers x 2 x kv_heads x head_dim x dtype_bytes x seq_len x batch`.

**Example:**
```python
kv_bytes = 28 * 2 * 8 * 128 * 2 * 8192 * 4  # 7B-class GQA, fp16, 4 seqs
# 3,758,096,384 bytes ~= 3.76 GB for the cache alone
```

**Related Terms:** max_model_len, KV-cache quantization, Prefix caching

**Key Facts:**
- Fixed by weights, unbounded by context: the long-context cost center
- Engines size their reservation from max_model_len x concurrent sequences

---

### KV-cache quantization

**Definition:** Storing cached keys and values at 8 or fewer bits instead of 16. It
shrinks the cache, not the model, so weight fidelity is untouched and capacity
(context length times batch) roughly doubles.

**Example:**
```text
fp16 KV at 8k, batch 4: 3.76 GB   ->   fp8 KV: 1.88 GB
```

**Related Terms:** KV cache, FP8, max_model_len

**Key Facts:**
- A separate dial from weight quantization; combine either way
- On Turing, fp8 storage saves memory and costs a conversion per read

---

### max_model_len

**Definition:** The longest sequence (prompt plus generation) the engine will accept,
and the number engines multiply by the concurrency limit to size the KV cache. Zero or
unbounded means the reservation cannot be reasoned about.

**Example:**
```python
max_model_len = 8192  # DevMate: ollama_num_ctx aligned to its budget
kv_reserve = kv_bytes_per_token * max_model_len * max_concurrent
```

**Related Terms:** KV cache, Prefix caching, TTFT

**Key Facts:**
- Raising 4k -> 32k reserves 8x KV even for short prompts
- Pair it with prefix caching only when it is an explicit bound (finding INF003)

---

### Model routing

**Definition:** Directing each request to a small, mid, or strong model according to
its task or difficulty, using heuristic rules or a fast classifier, so easy traffic
pays small-model prices.

**Example:**
```text
classify-question  -> small model
grounded answer    -> strong model + RAG + citations
summarization      -> mid model + prefix cache
```

**Related Terms:** Fallback ladder, Quality floor, Cost per 1k tokens

**Key Facts:**
- Pays only when traffic is mixed and dominated by simple requests
- Its failure mode is silent: a misroute answers wrongly, not with an error
- Evaluate route accuracy and quality per route, not just total cost

---

### Ollama

**Definition:** A local model runner built on llama.cpp that downloads GGUF quants,
manages memory, and exposes an OpenAI-compatible API. It is the development path in
this track, and the server behind DevMate's local `qwen2.5-coder:7b`.

**Example:**
```text
ollama pull qwen2.5-coder:7b     # Q4_K_M default
POST http://localhost:11434/v1   # OpenAI-compatible surface
```

**Related Terms:** GGUF, vLLM, Continuous batching

**Key Facts:**
- Minutes to a running model; ideal for development and single users
- Exposes `num_ctx`, which is DevMate's `ollama_num_ctx = 8192` fix

---

### PagedAttention

**Definition:** vLLM's core memory idea: the KV cache is allocated in fixed-size blocks
drawn from a shared pool, with a per-sequence block table, exactly as an operating
system pages virtual memory instead of reserving contiguous runs.

**Example:**
```text
sequence KV:  [ 16 tok ][ 16 tok ][ 16 tok ]  -> block table [B7, B2, B9]
pool:         [ B0 ][ B1 ][ B2 ] ... [ free ]   fragments reused instantly
```

**Related Terms:** KV cache, Prefix caching, vLLM

**Key Facts:**
- Near-eliminates KV fragmentation and over-reservation
- Blocks can be shared: two requests with one prefix point at the same blocks

---

### Perplexity delta

**Definition:** The perplexity of a quantized (or otherwise modified) model minus the
perplexity of its baseline on the same corpus. A cheap, sensitive early-warning number
for quality drift, declared with an acceptable bound before the run.

**Example:**
```python
delta = quant_ppl - base_ppl  # e.g. 6.42 -> 6.51
assert delta <= max_ppl_delta  # gate 1 of 2
```

**Related Terms:** Quality floor, AWQ, GPTQ

**Key Facts:**
- Cheap to compute and sensitive, but blind to task behavior
- Always pair it with a task metric on the golden set

---

### Prefix caching

**Definition:** Reusing cached KV for the leading tokens of a prompt so a request with
an identical prefix skips that part of prefill. Matching is normally exact, by token
hash at block granularity; fuzzy matching recovers hits when prefixes share content
but not token boundaries.

**Example:**
```text
[system][document][history][question]   <- cache the stable left side
change one byte early -> every token after it changes -> cache miss there
```

**Related Terms:** PagedAttention, RadixAttention, KV cache

**Key Facts:**
- Saves prefill (TTFT), never decode
- One byte at the front invalidates everything downstream of it

---

### Prefill phase

**Definition:** The first pass over the prompt, which processes all prompt tokens in
parallel and builds the KV cache. Compute-bound, prompt-length-bound, and the
component of TTFT you can shorten with prefix caching.

**Example:**
```text
TTFT = queueing + prefill(prompt)      # long prompt -> long TTFT
```

**Related Terms:** Decode phase, TTFT, Prefix caching

**Key Facts:**
- Parallel over prompt tokens, so batching helps it less than decode
- It is what a shared prompt prefix lets you skip entirely

---

### Quality floor

**Definition:** The minimum score on the golden set that a configuration must hold for
a change to ship, independent of how much faster or cheaper it is. It is one of the
three objective numbers, alongside the p95 SLO and the cost ceiling.

**Example:**
```python
if after.quality_score < obj.quality_floor:
    reject("faster is not better if the answers got worse")
```

**Related Terms:** Perplexity delta, Model routing, Objective

**Key Facts:**
- Catches routing downgrades and quantization drift in one gate
- Below the floor, latency and cost numbers are irrelevant

---

### RadixAttention

**Definition:** SGLang's core idea: keep cached KV in a radix tree keyed by token
sequences so requests with common prefixes share cache nodes at token granularity,
with eviction managed over the tree.

**Example:**
```text
              root
           /   |   \
      [system prompt] [other]
          /    \
    [doc A]  [doc A + question 1]
```

**Related Terms:** PagedAttention, Prefix caching, SGLang

**Key Facts:**
- The same goal as vLLM's block sharing, different data structure
- Still bound by the same KV capacity physics on 16 GB

---

### Speculative decoding

**Definition:** A cheap drafter proposes k tokens and the target model verifies all of
them in one forward pass, accepting a prefix via rejection sampling that provably
preserves the target model's output distribution.

**Example:**
```text
draft:   [t1 t2 t3 t4]        cheap, one pass
target:  verify all four in a single forward pass
result:  accepted run, then resample from the first mismatch
```

**Related Terms:** Decode phase, KV cache, Weight-only quantization

**Key Facts:**
- Speed only: output distribution is unchanged, unlike quantization
- Helps at batch 1-4 with predictable tokens; hurts under large batch or load
- A draft model costs VRAM; n-gram drafting costs none

---

### Structured output

**Definition:** Producing output that conforms to a machine-readable contract, via
JSON-schema constrained decoding, grammar constraints, or retry-and-repair. Constraints
guarantee shape; only semantic validation guarantees meaning.

**Example:**
```python
response_format = {
    "type": "json_schema",
    "json_schema": {"name": "Answer", "schema": schema, "strict": True},
}
```

**Related Terms:** Grammar-constrained decoding, TGI, Quality floor

**Key Facts:**
- Engine constraints cost masking per token; retries cost extra generations
- Truncation under max_tokens can leave an incomplete object

---

### TGI

**Definition:** Hugging Face's Text Generation Inference: a production server with
streaming, request queues, continuous batching, quantized weight loading, and, since
v1.4.3, a `grammar` parameter for JSON/regex/Pydantic constraints compiled through
outlines.

**Example:**
```python
client.generate(prompt, grammar={"type": "json", "value": json_schema})
# first request compiles the grammar; later requests reuse the cache
```

**Related Terms:** vLLM, Grammar-constrained decoding, Structured output

**Key Facts:**
- Fits teams already standardized on the HF ecosystem
- Grammar compile latency is a first-request cost worth caching

---

### TTFT

**Definition:** Time to first token: queueing plus prefill, the number users feel
while waiting for an answer to start. Rising p95 TTFT is the earliest overload signal
a serving system has.

**Example:**
```text
p95 TTFT 800 ms at concurrency 8  ->  queue is forming, check the batch policy
```

**Related Terms:** Prefill phase, Prefix caching, Continuous batching

**Key Facts:**
- A long prompt raises TTFT without lowering decode rate
- Report p50 and p95; the average hides the queue

---

### vLLM

**Definition:** A high-throughput serving engine built on PagedAttention and
iteration-level scheduling, with an OpenAI-compatible API, prefix caching, guided
decoding, speculative decoding, and support for AWQ, GPTQ, and FP8 weights.

**Example:**
```text
vllm serve model/AWQ-4bit --max-model-len 8192 --gpu-memory-utilization 0.90
```

**Related Terms:** PagedAttention, Continuous batching, Ollama

**Key Facts:**
- The production counterpart to Ollama's development path (Model Serving 02)
- max_model_len and the concurrency limit together size its KV reservation

---

### Weight-only quantization

**Definition:** Narrowing only the weights while activations stay in a wider type,
trading a little accuracy for far smaller weight reads, which is where decode spends
its time. AWQ, GPTQ, and GGUF quants are all weight-only methods.

**Example:**
```text
7.6B params:  fp16 15.2 GB | INT8 7.6 GB | INT4 ~3.8 GB (ideal)
```

**Related Terms:** Activation quantization, AWQ, KV-cache quantization

**Key Facts:**
- The first lever to reach for on a 16 GB card
- Independent of KV precision; combine the two as the budget requires

---

## Related Concepts

- **Choosing a model** (Model Serving 01): the four axes this lecture operationalizes
- **Self-hosted models** (Model Serving 02): the 16 GB budget and the engine choice
- **Inference serving** (Model Serving 03): the API contract, percentiles, fallbacks
- **DevMate failure modes**: `projects/04-ai-engineering/devmate/docs/failure-modes.md`

## Key Takeaways

1. The objective is p95 SLO plus cost ceiling plus quality floor, measured together.
2. The engine sets the ceiling: PagedAttention and iteration-level scheduling are why.
3. KV cache, not weights, dominates long context; the sizing formula decides feasibility.
4. Quantization ships behind a perplexity delta and a task eval, never a vibe check.
5. Prefix caching, KV quantization, and speculative decoding are independent dials,
   each with a regime where it pays and one where it does not.
