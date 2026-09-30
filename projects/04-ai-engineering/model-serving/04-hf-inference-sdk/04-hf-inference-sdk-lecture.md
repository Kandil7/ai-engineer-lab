# Model Serving 04: Hugging Face Inference SDK

## 🎯 Topic Overview

The Hugging Face Inference SDK calls models hosted on the HF Inference
Endpoints or the free inference API. This lecture covers the SDK, the
model selection, and the production endpoint.

## 📚 Learning Objectives

By the end of this lecture, you will be able to:

1. Call the HF Inference API
2. Select a model from the Hub
3. Use Inference Endpoints for production
4. Handle the free-tier limits
5. Compare HF against self-hosting

---

## 1. The SDK

The HF Inference SDK wraps the API. A model is specified by its Hub ID;
the SDK handles the request. The free tier has rate limits; production
uses Inference Endpoints. The roadmap's exit test: "the HF Inference SDK
is used."

```python
from huggingface_hub import InferenceClient

client = InferenceClient(model="mistralai/Mistral-7B-Instruct-v0.2")
```

## 2. Model Selection

The Hub hosts thousands of models. Selection is by task (text-generation,
feature-extraction), language, and size. The golden set evaluates the
shortlist. The roadmap's exit test: "the model is selected from the Hub."

## 3. Inference Endpoints

Inference Endpoints are dedicated, autoscaled deployments. They offer
consistent latency and no rate limits. The deployment is the production
path; the free API is the development path. The roadmap's exit test:
"Inference Endpoints are used for production."

## 4. Free-Tier Limits

The free API has rate limits and shared capacity. It is fine for
development and testing; production needs dedicated capacity. The
roadmap's exit test: "free-tier limits are understood."

## 5. HF vs Self-Hosting

HF Inference is managed — no infrastructure. Self-hosting is unmanaged —
full control, more work. The choice depends on volume, privacy, and
latency requirements. The roadmap's exit test: "the comparison is
documented."

## Common Mistakes

- Using the free tier in production (rate limits).
- No model evaluation on the Hub selection.
- Ignoring the free-tier limits.
- Not comparing against self-hosting.
- Locking the app to the HF SDK.

## Key Takeaways

1. The SDK wraps the Inference API.
2. Models are selected from the Hub.
3. Inference Endpoints are the production path.
4. Free-tier limits are for development.
5. HF vs self-hosting is a volume/privacy/latency decision.