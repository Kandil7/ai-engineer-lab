# Model Serving 04: HF Inference SDK — Glossary

## Quick Reference Table

| Term | Definition | Example |
|------|-----------|---------|
| HF Inference SDK | The Python wrapper for the Inference API | InferenceClient |
| Hub model | A model hosted on the Hugging Face Hub | mistralai/Mistral-7B |
| Inference Endpoints | Dedicated, autoscaled deployment | production |
| Free tier | Rate-limited shared API | development |
| Feature extraction | The embedding task | text -> vector |
| Rate limit | The free-tier request bound | 429 |
| Hub selection | Choosing a model by task/language/size | golden set |

---

## Alphabetical Glossary

### Feature extraction

**Definition:** The embedding task: text to vector. One of the Hub's task
types.

**Example:**
```python
client.feature_extraction("text")
```

**Related concepts:** Hub model

---

### Free tier

**Definition:** The rate-limited shared Inference API. For development
and testing; not production.

**Example:**
```python
# shared capacity; 429 on rate limit
```

**Related concepts:** Rate limit

---

### HF Inference SDK

**Definition:** The Python wrapper for the Hugging Face Inference API.
The client is created with a Hub model ID.

**Example:**
```python
from huggingface_hub import InferenceClient

client = InferenceClient(model="mistralai/Mistral-7B")
```

**Related concepts:** Hub model

---

### Hub model

**Definition:** A model hosted on the Hugging Face Hub, identified by
`org/name`. Selected by task, language, and size.

**Example:**
```python
# mistralai/Mistral-7B-Instruct-v0.2
```

**Related concepts:** Hub selection

---

### Hub selection

**Definition:** Choosing a model from the Hub by task, language, and size.
Evaluated on the golden set.

**Example:**
```python
# shortlist by task; evaluate on the golden set
```

**Related concepts:** Hub model

---

### Inference Endpoints

**Definition:** Dedicated, autoscaled deployments. Consistent latency, no
rate limits. The production path.

**Example:**
```python
client = InferenceClient(model="https://my-endpoint.endpoints.huggingface.cloud")
```

**Related concepts:** Free tier

---

### Rate limit

**Definition:** The free tier's request bound. Exceeding it returns a 429.

**Example:**
```python
# HTTP 429 on the free tier
```

**Related concepts:** Free tier

---

## Related Concepts

- **Choosing a model**: the model selection (topic 01)
- **Self-hosted models**: the alternative (topic 02)
- **Embeddings**: the feature-extraction task (embeddings 01)

## Key Takeaways

1. The SDK wraps the Inference API.
2. Models are selected from the Hub.
3. Inference Endpoints are the production path.
4. Free-tier limits are for development.
5. HF vs self-hosting is a volume/privacy/latency decision.