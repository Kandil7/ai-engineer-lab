"""
Embedding service for generating vector representations.
"""

import asyncio
import hashlib
from abc import ABC, abstractmethod
from dataclasses import dataclass

import httpx
import tiktoken

from devmate.config import settings
from devmate.obs.cost import TokenUsage, cost_tracker
from devmate.obs.tracing import tracer


@dataclass
class EmbeddingResult:
    """Result of embedding generation."""

    embeddings: list[list[float]]
    usage: TokenUsage
    model: str
    latency_ms: float


class BaseEmbeddingProvider(ABC):
    """Abstract base class for embedding providers."""

    @property
    @abstractmethod
    def model_name(self) -> str:
        pass

    @property
    @abstractmethod
    def dimensions(self) -> int:
        pass

    @abstractmethod
    async def embed(self, texts: list[str]) -> EmbeddingResult:
        pass

    @abstractmethod
    def count_tokens(self, text: str) -> int:
        pass


class OpenAIEmbeddingProvider(BaseEmbeddingProvider):
    """OpenAI-compatible embeddings provider.

    The base URL and key are overridable (EMBEDDING_BASE_URL / EMBEDDING_API_KEY)
    so any OpenAI-compatible embeddings endpoint works — Jina, Google, Together,
    Voyage — without an OpenAI key. Defaults to OpenAI when unset.
    """

    def __init__(self, model: str = None, api_key: str = None, base_url: str = None) -> None:
        self._model = model or settings.embedding_model
        self._api_key = api_key or settings.embedding_api_key or settings.openai_api_key

        if not self._api_key:
            raise ValueError(
                "No embeddings key configured (set EMBEDDING_API_KEY or OPENAI_API_KEY)"
            )

        self.client = httpx.AsyncClient(
            base_url=base_url or settings.embedding_base_url or "https://api.openai.com/v1",
            headers={
                "Authorization": f"Bearer {self._api_key}",
                "Content-Type": "application/json",
            },
            timeout=httpx.Timeout(60.0, connect=10.0),
        )

        # Token encoding
        try:
            self.encoding = tiktoken.encoding_for_model(self._model)
        except KeyError:
            self.encoding = tiktoken.get_encoding("cl100k_base")

    @property
    def model_name(self) -> str:
        return self._model

    @property
    def dimensions(self) -> int:
        dim_map = {
            "text-embedding-3-small": 1536,
            "text-embedding-3-large": 3072,
            "text-embedding-ada-002": 1536,
        }
        # Unknown (non-OpenAI) models take the configured dimension.
        return dim_map.get(self._model, settings.embedding_dimensions)

    def count_tokens(self, text: str) -> int:
        return len(self.encoding.encode(text))

    async def embed(self, texts: list[str]) -> EmbeddingResult:
        """Generate embeddings for a batch of texts."""
        if not texts:
            return EmbeddingResult(
                embeddings=[],
                usage=TokenUsage(0, 0, 0),
                model=self._model,
                latency_ms=0,
            )

        import time

        start_time = time.perf_counter()

        async with tracer.trace("embedding.generate", model=self._model, count=len(texts)):
            # Batch texts to avoid token limits
            batch_size = settings.embedding_batch_size
            all_embeddings = []
            total_prompt_tokens = 0

            for i in range(0, len(texts), batch_size):
                batch = texts[i : i + batch_size]

                payload = {
                    "model": self._model,
                    "input": batch,
                    "encoding_format": "float",
                }

                # Add dimensions for newer models
                if self._model in ("text-embedding-3-small", "text-embedding-3-large"):
                    payload["dimensions"] = self.dimensions

                response = await self.client.post("/embeddings", json=payload)
                response.raise_for_status()
                data = response.json()

                batch_embeddings = [item["embedding"] for item in data["data"]]
                all_embeddings.extend(batch_embeddings)

                usage = data.get("usage", {})
                total_prompt_tokens += usage.get("prompt_tokens", 0)

            latency_ms = (time.perf_counter() - start_time) * 1000

            usage = TokenUsage(
                prompt_tokens=total_prompt_tokens,
                completion_tokens=0,
                total_tokens=total_prompt_tokens,
            )

            cost_tracker.record_usage("openai", self._model, usage, latency_ms)

            return EmbeddingResult(
                embeddings=all_embeddings,
                usage=usage,
                model=self._model,
                latency_ms=latency_ms,
            )


class LocalEmbeddingProvider(BaseEmbeddingProvider):
    """Local embeddings using sentence-transformers."""

    def __init__(self, model_name: str = "BAAI/bge-base-en-v1.5") -> None:
        self._model_name = model_name
        self._model = None
        self._dimensions = 768  # bge-base

    @property
    def model_name(self) -> str:
        return self._model_name

    @property
    def dimensions(self) -> int:
        return self._dimensions

    def _load_model(self) -> None:
        """Lazy load the model."""
        if self._model is None:
            from sentence_transformers import SentenceTransformer

            self._model = SentenceTransformer(self._model_name)
            self._dimensions = self._model.get_sentence_embedding_dimension()

    def count_tokens(self, text: str) -> int:
        # Rough approximation
        return len(text) // 4

    async def embed(self, texts: list[str]) -> EmbeddingResult:
        """Generate embeddings locally."""
        if not texts:
            return EmbeddingResult(
                embeddings=[],
                usage=TokenUsage(0, 0, 0),
                model=self._model_name,
                latency_ms=0,
            )

        import time

        start_time = time.perf_counter()

        self._load_model()

        async with tracer.trace("embedding.generate", model=self._model_name, count=len(texts)):
            # Run in thread pool to avoid blocking
            loop = asyncio.get_event_loop()
            embeddings = await loop.run_in_executor(
                None, lambda: self._model.encode(texts, normalize_embeddings=True).tolist()
            )

            latency_ms = (time.perf_counter() - start_time) * 1000

            # Estimate tokens
            total_tokens = sum(self.count_tokens(t) for t in texts)
            usage = TokenUsage(
                prompt_tokens=total_tokens,
                completion_tokens=0,
                total_tokens=total_tokens,
            )

            # Local embeddings are free
            cost_tracker.record_usage("local", self._model_name, usage, latency_ms)

            return EmbeddingResult(
                embeddings=embeddings,
                usage=usage,
                model=self._model_name,
                latency_ms=latency_ms,
            )


class OllamaEmbeddingProvider(BaseEmbeddingProvider):
    """Local embeddings via Ollama — runs fully offline, no API key required."""

    _DIMENSIONS = {
        "nomic-embed-text": 768,
        "mxbai-embed-large": 1024,
        "all-minilm": 384,
    }

    def __init__(self, model: str | None = None, base_url: str | None = None) -> None:
        self._model = model or settings.ollama_embedding_model
        self._dimensions = self._DIMENSIONS.get(self._model, settings.embedding_dimensions)
        self.client = httpx.AsyncClient(
            base_url=(base_url or settings.ollama_base_url).rstrip("/"),
            timeout=httpx.Timeout(60.0, connect=5.0),
        )

    @property
    def model_name(self) -> str:
        return self._model

    @property
    def dimensions(self) -> int:
        return self._dimensions

    def count_tokens(self, text: str) -> int:
        # Ollama exposes no tokenizer over HTTP; rough approximation.
        return len(text) // 4

    async def embed(self, texts: list[str]) -> EmbeddingResult:
        """Generate embeddings for a batch of texts via /api/embed."""
        if not texts:
            return EmbeddingResult(
                embeddings=[],
                usage=TokenUsage(0, 0, 0),
                model=self._model,
                latency_ms=0,
            )

        import time

        start_time = time.perf_counter()

        async with tracer.trace("embedding.generate", model=self._model, count=len(texts)):
            batch_size = settings.embedding_batch_size
            all_embeddings: list[list[float]] = []
            total_prompt_tokens = 0

            for i in range(0, len(texts), batch_size):
                batch = texts[i : i + batch_size]
                response = await self.client.post(
                    "/api/embed",
                    json={"model": self._model, "input": batch},
                )
                response.raise_for_status()
                data = response.json()
                all_embeddings.extend(data.get("embeddings", []))
                total_prompt_tokens += data.get("prompt_eval_count", 0)

            latency_ms = (time.perf_counter() - start_time) * 1000

            usage = TokenUsage(
                prompt_tokens=total_prompt_tokens,
                completion_tokens=0,
                total_tokens=total_prompt_tokens,
            )

            # Local inference has no per-token cost
            cost_tracker.record_usage("ollama", self._model, usage, latency_ms)

            return EmbeddingResult(
                embeddings=all_embeddings,
                usage=usage,
                model=self._model,
                latency_ms=latency_ms,
            )


def get_embedding_provider() -> BaseEmbeddingProvider:
    """Resolve the embedding provider from settings.

    Offline-first: defaults to Ollama. If EMBEDDING_PROVIDER=openai but no
    key is configured, falls back to Ollama instead of raising at import
    time (which previously crashed every key-less environment).
    """
    import logging

    name = settings.embedding_provider.lower()

    if name == "openai" and not (settings.embedding_api_key or settings.openai_api_key):
        logging.getLogger(__name__).warning(
            "EMBEDDING_PROVIDER=openai but no embeddings key is set "
            "(EMBEDDING_API_KEY / OPENAI_API_KEY); using Ollama instead"
        )
        name = "ollama"

    if name == "ollama":
        return OllamaEmbeddingProvider()
    if name == "openai":
        return OpenAIEmbeddingProvider()
    if name == "local":
        return LocalEmbeddingProvider()
    raise ValueError(f"Unknown embedding provider: {name!r}. Use 'ollama', 'openai', or 'local'.")


class EmbeddingService:
    """Unified embedding service with caching and batching."""

    def __init__(self, provider: BaseEmbeddingProvider = None) -> None:
        self.provider = provider or get_embedding_provider()
        self._cache: dict = {}
        self._cache_enabled = True

    def _cache_key(self, text: str) -> str:
        """Generate cache key for text."""
        return hashlib.sha256(text.encode()).hexdigest()[:32]

    async def embed(self, texts: list[str], use_cache: bool = True) -> EmbeddingResult:
        """Generate embeddings with optional caching."""
        if not texts:
            return EmbeddingResult(
                embeddings=[],
                usage=TokenUsage(0, 0, 0),
                model=self.provider.model_name,
                latency_ms=0,
            )

        # Check cache
        if use_cache and self._cache_enabled:
            cached_embeddings = []
            uncached_texts = []
            uncached_indices = []

            for i, text in enumerate(texts):
                key = self._cache_key(text)
                if key in self._cache:
                    cached_embeddings.append((i, self._cache[key]))
                else:
                    uncached_texts.append(text)
                    uncached_indices.append(i)

            if not uncached_texts:
                # All cached
                embeddings = [None] * len(texts)
                for i, emb in cached_embeddings:
                    embeddings[i] = emb
                return EmbeddingResult(
                    embeddings=embeddings,
                    usage=TokenUsage(0, 0, 0),
                    model=self.provider.model_name,
                    latency_ms=0,
                )

            # Generate for uncached
            result = await self.provider.embed(uncached_texts)

            # Update cache
            for idx, embedding in zip(uncached_indices, result.embeddings):
                key = self._cache_key(texts[idx])
                self._cache[key] = embedding

            # Merge cached and new
            final_embeddings = [None] * len(texts)
            for i, emb in cached_embeddings:
                final_embeddings[i] = emb
            for idx, emb in zip(uncached_indices, result.embeddings):
                final_embeddings[idx] = emb

            return EmbeddingResult(
                embeddings=final_embeddings,
                usage=result.usage,
                model=result.model,
                latency_ms=result.latency_ms,
            )

        return await self.provider.embed(texts)

    async def embed_single(self, text: str) -> list[float]:
        """Embed a single text."""
        result = await self.embed([text])
        return result.embeddings[0] if result.embeddings else []

    def count_tokens(self, text: str) -> int:
        return self.provider.count_tokens(text)

    def clear_cache(self) -> None:
        """Clear embedding cache."""
        self._cache.clear()

    @property
    def dimensions(self) -> int:
        return self.provider.dimensions

    @property
    def model_name(self) -> str:
        return self.provider.model_name


# Global embedding service
embedding_service = EmbeddingService()
