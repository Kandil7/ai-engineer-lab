# Model Serving 02: Self-Hosted Models — Glossary

## Quick Reference Table

| Term | Definition | Example |
|------|-----------|---------|
| Self-hosting | Running the model on your infrastructure | local GPU |
| Ollama | Simple local serving, OpenAI-compatible | dev/single-user |
| vLLM | High-throughput production serving | paged attention |
| VRAM budget | Weights + KV cache + activations | checked before run |
| OpenAI-compatible | The standard API shape | base URL swap |
| Quantization | Reducing model precision | 4-bit |
| Continuous batching | vLLM's throughput optimization | production |

---

## Alphabetical Glossary

### Continuous batching

**Definition:** vLLM's throughput optimization: requests are batched
dynamically as they arrive. The production advantage over Ollama.

**Example:**
```python
# multiple requests served in one forward pass
```

**Related concepts:** vLLM

---

### Ollama

**Definition:** The simplest self-hosting path: download, run, get an
OpenAI-compatible API. Handles quantization and memory.

**Example:**
```bash
ollama run llama3.1:8b
```

**Related concepts:** vLLM, OpenAI-compatible

---

### OpenAI-compatible

**Definition:** The standard API shape. The application code is identical
whether calling OpenAI or a local model — only the base URL changes.

**Example:**
```python
# base_url="http://localhost:11434/v1"
```

**Related concepts:** Ollama

---

### Quantization

**Definition:** Reducing model precision (e.g., 4-bit) to fit in less
VRAM. Trades a little quality for a lot of memory.

**Example:**
```python
# 7B at 4-bit: ~4 GB vs 16-bit: ~14 GB
```

**Related concepts:** VRAM budget

---

### Self-hosting

**Definition:** Running the model on your own infrastructure. Eliminates
per-token cost but adds infrastructure work.

**Example:**
```python
# local GPU serves the model
```

**Related concepts:** Ollama, vLLM

---

### VRAM budget

**Definition:** Weights + KV cache + activations. Checked before the run
to avoid OOM.

**Example:**
```python
# 7B at 4-bit: ~4 GB weights + KV cache + activations
```

**Related concepts:** Quantization

---

### vLLM

**Definition:** High-throughput production serving with paged attention
and continuous batching. The production path.

**Example:**
```bash
vllm serve meta-llama/Llama-3.1-8B
```

**Related concepts:** Continuous batching, Ollama

---

## Related Concepts

- **Choosing a model**: the cost axis (topic 01)
- **Inference serving**: the serving architecture (topic 03)
- **LoRA/QLoRA**: the memory math (fine-tuning 02)

## Key Takeaways

1. Self-hosting trades cost for infrastructure.
2. Ollama for development; vLLM for production.
3. The VRAM budget decides the model size.
4. The API is OpenAI-compatible.
5. Measure local latency.