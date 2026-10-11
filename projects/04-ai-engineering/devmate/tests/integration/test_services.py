"""Integration tests for DevMate against live Qdrant and Redis.

These exercise the real adapters, not raw clients:

- ``QdrantVectorStore``: create a collection, upsert documents with embeddings,
  search by vector, filter by payload metadata, and read a document back.
- ``SemanticCache``: store and retrieve a response through Redis.

They need live infrastructure:

    docker compose -f infra/docker/docker-compose.yml up -d qdrant redis

Every test is marked ``integration``; the default unit run excludes it (see the
``addopts`` in pyproject.toml), and CI runs it in the integration job with
Qdrant and Redis service containers. No paid API is called here.
"""

from __future__ import annotations

import uuid

import pytest

from devmate.cache.semantic_cache import SemanticCache
from devmate.index.vector_store import QdrantVectorStore, VectorStoreConfig
from devmate.ingest.chunker import Document

pytestmark = pytest.mark.integration


def _collection_name() -> str:
    return f"devmate_it_{uuid.uuid4().hex[:8]}"


@pytest.mark.asyncio
async def test_qdrant_vector_store_roundtrip() -> None:
    name = _collection_name()
    store = QdrantVectorStore(VectorStoreConfig(collection_name=name, vector_size=4))
    await store.initialize()
    try:
        docs = [
            Document(
                id=str(uuid.uuid4()),
                content="alpha",
                metadata={"filename": "a.py"},
                embedding=[1.0, 0.0, 0.0, 0.0],
            ),
            Document(
                id=str(uuid.uuid4()),
                content="beta",
                metadata={"filename": "b.py"},
                embedding=[0.0, 1.0, 0.0, 0.0],
            ),
        ]
        assert await store.upsert(docs) == 2
        assert await store.count() == 2

        hits = await store.search([1.0, 0.0, 0.0, 0.0], limit=1)
        assert hits and hits[0].content == "alpha"

        got = await store.get(docs[0].id)
        assert got is not None
        assert got.content == "alpha"
    finally:
        try:
            if store.client is not None:
                store.client.delete_collection(name)
        except Exception:
            pass
        await store.close()


@pytest.mark.asyncio
async def test_qdrant_metadata_filter() -> None:
    name = _collection_name()
    store = QdrantVectorStore(VectorStoreConfig(collection_name=name, vector_size=4))
    await store.initialize()
    try:
        await store.upsert(
            [
                Document(
                    id=str(uuid.uuid4()),
                    content="a",
                    metadata={"filename": "a.py"},
                    embedding=[1.0, 0.0, 0.0, 0.0],
                ),
                Document(
                    id=str(uuid.uuid4()),
                    content="b",
                    metadata={"filename": "b.py"},
                    embedding=[1.0, 0.0, 0.0, 0.0],
                ),
            ]
        )
        hits = await store.search([1.0, 0.0, 0.0, 0.0], limit=5, filter={"filename": "b.py"})
        assert len(hits) == 1
        assert hits[0].content == "b"
    finally:
        try:
            if store.client is not None:
                store.client.delete_collection(name)
        except Exception:
            pass
        await store.close()


@pytest.mark.asyncio
async def test_semantic_cache_redis_roundtrip() -> None:
    cache = SemanticCache()
    await cache.initialize()
    assert cache.redis_client is not None, "Redis must be reachable for integration tests"
    try:
        query = f"integration query {uuid.uuid4().hex}"
        embedding = [0.1, 0.2, 0.3]
        await cache.set(query, embedding, "answer-42", {"tokens": 3}, "test-model")

        hit = await cache.get(query, embedding, "test-model")
        assert hit is not None
        assert hit.response == "answer-42"
    finally:
        await cache.clear()
        await cache.close()
