"""
Semantic caching layer for LLM responses.
"""

import contextlib
import hashlib
import json
import time
from dataclasses import dataclass
from typing import Any

import numpy as np
import redis.asyncio as redis

from devmate.config import settings
from devmate.obs.tracing import tracer


@dataclass
class CacheEntry:
    """A cached response entry."""

    key: str
    query: str
    query_embedding: list[float]
    response: str
    usage: dict[str, Any]
    model: str
    created_at: float
    hits: int = 0


class SemanticCache:
    """Semantic cache using vector similarity for LLM responses."""

    def __init__(self) -> None:
        self.redis_client: redis.Redis | None = None
        self.enabled = True
        self.threshold = settings.semantic_cache_threshold
        self.ttl = settings.cache_ttl_seconds
        self._local_cache: dict[str, CacheEntry] = {}

    async def initialize(self) -> None:
        """Initialize Redis connection."""
        try:
            self.redis_client = redis.from_url(
                settings.redis_connection_url,
                encoding="utf-8",
                decode_responses=True,
            )
            await self.redis_client.ping()
        except Exception:
            self.redis_client = None

    def _cache_key(self, query: str, model: str) -> str:
        """Generate cache key."""
        content = f"{model}:{query}"
        return hashlib.sha256(content.encode()).hexdigest()[:32]

    def _embedding_key(self, query: str) -> str:
        """Key for storing embeddings."""
        return f"emb:{hashlib.sha256(query.encode()).hexdigest()[:16]}"

    def _cosine_similarity(self, a: list[float], b: list[float]) -> float:
        """Compute cosine similarity between two vectors."""
        if not a or not b:
            return 0.0
        a_arr = np.array(a)
        b_arr = np.array(b)
        return float(np.dot(a_arr, b_arr) / (np.linalg.norm(a_arr) * np.linalg.norm(b_arr)))

    async def get(self, query: str, query_embedding: list[float], model: str) -> CacheEntry | None:
        """Get cached response if semantically similar query exists."""
        if not self.enabled:
            return None

        async with tracer.trace("cache.get", model=model):
            # Check exact match first
            exact_key = self._cache_key(query, model)

            # Try Redis
            if self.redis_client:
                try:
                    data = await self.redis_client.get(f"cache:{exact_key}")
                    if data:
                        entry_data = json.loads(data)
                        entry = CacheEntry(**entry_data)
                        entry.hits += 1
                        await self.redis_client.setex(
                            f"cache:{exact_key}",
                            self.ttl,
                            json.dumps(entry.__dict__),
                        )
                        return entry
                except Exception:
                    pass

            # Check local cache for exact match
            if exact_key in self._local_cache:
                entry = self._local_cache[exact_key]
                entry.hits += 1
                return entry

            # Semantic search in local cache
            best_match = None
            best_score = 0.0

            for entry in self._local_cache.values():
                if entry.model != model:
                    continue
                score = self._cosine_similarity(query_embedding, entry.query_embedding)
                if score > best_score and score >= self.threshold:
                    best_score = score
                    best_match = entry

            if best_match:
                best_match.hits += 1
                return best_match

            return None

    async def set(
        self,
        query: str,
        query_embedding: list[float],
        response: str,
        usage: dict[str, Any],
        model: str,
    ) -> None:
        """Cache a response."""
        if not self.enabled:
            return

        entry = CacheEntry(
            key=self._cache_key(query, model),
            query=query,
            query_embedding=query_embedding,
            response=response,
            usage=usage,
            model=model,
            created_at=time.time(),
        )

        # Store in local cache
        self._local_cache[entry.key] = entry

        # Store in Redis
        if self.redis_client:
            with contextlib.suppress(Exception):
                await self.redis_client.setex(
                    f"cache:{entry.key}",
                    self.ttl,
                    json.dumps(entry.__dict__),
                )

        # Limit local cache size
        if len(self._local_cache) > 1000:
            # Remove oldest entries
            sorted_entries = sorted(
                self._local_cache.items(),
                key=lambda x: x[1].created_at,
            )
            for key, _ in sorted_entries[:100]:
                del self._local_cache[key]

    async def get_stats(self) -> dict[str, Any]:
        """Get cache statistics."""
        total_hits = sum(e.hits for e in self._local_cache.values())
        return {
            "enabled": self.enabled,
            "threshold": self.threshold,
            "ttl_seconds": self.ttl,
            "local_entries": len(self._local_cache),
            "total_hits": total_hits,
            "redis_connected": self.redis_client is not None,
        }

    async def clear(self) -> None:
        """Clear all cache entries."""
        self._local_cache.clear()
        if self.redis_client:
            try:
                keys = await self.redis_client.keys("cache:*")
                if keys:
                    await self.redis_client.delete(*keys)
            except Exception:
                pass

    async def close(self) -> None:
        """Close Redis connection."""
        if self.redis_client:
            await self.redis_client.aclose()


# Global cache instance
semantic_cache = SemanticCache()
