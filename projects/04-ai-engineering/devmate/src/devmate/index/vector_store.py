"""
Vector store abstraction with Qdrant implementation.
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any

from qdrant_client import QdrantClient, models

from devmate.config import settings
from devmate.ingest.chunker import Document
from devmate.obs.tracing import tracer


@dataclass
class SearchResult:
    """Result from vector search."""

    id: str
    score: float
    content: str
    metadata: dict[str, Any]
    vector: list[float] | None = None


@dataclass
class VectorStoreConfig:
    """Configuration for vector store."""

    collection_name: str
    vector_size: int
    distance: str = "cosine"
    on_disk: bool = True
    hnsw_m: int = 16
    hnsw_ef_construct: int = 100


class BaseVectorStore(ABC):
    """Abstract base class for vector stores."""

    @abstractmethod
    async def initialize(self):
        """Initialize the vector store."""
        pass

    @abstractmethod
    async def upsert(self, documents: list[Document]) -> int:
        """Insert or update documents."""
        pass

    @abstractmethod
    async def search(
        self,
        query_vector: list[float],
        limit: int = 10,
        filter: dict[str, Any] | None = None,
    ) -> list[SearchResult]:
        """Search for similar vectors."""
        pass

    @abstractmethod
    async def delete(self, ids: list[str]) -> bool:
        """Delete documents by IDs."""
        pass

    @abstractmethod
    async def get(self, id: str) -> Document | None:
        """Get a document by ID."""
        pass

    @abstractmethod
    async def count(self) -> int:
        """Get total document count."""
        pass

    @abstractmethod
    async def close(self):
        """Close connections."""
        pass


class QdrantVectorStore(BaseVectorStore):
    """Qdrant vector store implementation."""

    def __init__(self, config: VectorStoreConfig = None) -> None:
        self.config = config or VectorStoreConfig(
            collection_name=settings.qdrant_collection,
            vector_size=settings.qdrant_vector_size,
            distance=settings.qdrant_distance,
        )
        self.client: QdrantClient | None = None
        self._initialized = False

    async def initialize(self) -> None:
        """Initialize Qdrant client and collection."""
        if self._initialized:
            return

        async with tracer.trace("vectorstore.initialize", collection=self.config.collection_name):
            self.client = QdrantClient(
                host=settings.qdrant_host,
                port=settings.qdrant_port,
                api_key=settings.qdrant_api_key,
                https=settings.qdrant_https,
            )

            # Check if collection exists
            collections = self.client.get_collections().collections
            collection_names = [c.name for c in collections]

            if self.config.collection_name not in collection_names:
                await self._create_collection()

            self._initialized = True

    async def _create_collection(self) -> None:
        """Create the collection with optimized settings."""
        distance_map = {
            "cosine": models.Distance.COSINE,
            "dot": models.Distance.DOT,
            "euclidean": models.Distance.EUCLID,
        }

        self.client.create_collection(
            collection_name=self.config.collection_name,
            vectors_config=models.VectorParams(
                size=self.config.vector_size,
                distance=distance_map.get(self.config.distance, models.Distance.COSINE),
                on_disk=self.config.on_disk,
            ),
            optimizers_config=models.OptimizersConfigDiff(
                indexing_threshold=20000,
            ),
            hnsw_config=models.HnswConfigDiff(
                m=self.config.hnsw_m,
                ef_construct=self.config.hnsw_ef_construct,
                full_scan_threshold=10000,
            ),
        )

        # Create payload indexes for common filter fields
        index_fields = [
            ("language", "keyword"),
            ("source_type", "keyword"),
            ("filename", "keyword"),
            ("chunk_type", "keyword"),
            ("repo_name", "keyword"),
        ]

        for field_name, field_schema in index_fields:
            try:
                self.client.create_payload_index(
                    collection_name=self.config.collection_name,
                    field_name=field_name,
                    field_schema=field_schema,
                )
            except Exception:
                # Index might already exist
                pass

    async def upsert(self, documents: list[Document]) -> int:
        """Upsert documents with embeddings."""
        if not self._initialized:
            await self.initialize()

        if not documents:
            return 0

        async with tracer.trace("vectorstore.upsert", count=len(documents)):
            points = []

            for doc in documents:
                if doc.embedding is None:
                    raise ValueError(f"Document {doc.id} has no embedding")

                point = models.PointStruct(
                    id=doc.id,
                    vector=doc.embedding,
                    payload={
                        "content": doc.content,
                        **doc.metadata,
                    },
                )
                points.append(point)

            # Batch upsert
            batch_size = 100
            upserted = 0

            for i in range(0, len(points), batch_size):
                batch = points[i : i + batch_size]
                self.client.upsert(
                    collection_name=self.config.collection_name,
                    points=batch,
                )
                upserted += len(batch)

            return upserted

    async def search(
        self,
        query_vector: list[float],
        limit: int = 10,
        filter: dict[str, Any] | None = None,
    ) -> list[SearchResult]:
        """Search for similar vectors with optional filtering."""
        if not self._initialized:
            await self.initialize()

        async with tracer.trace("vectorstore.search", limit=limit):
            # Build filter
            query_filter = None
            if filter:
                conditions = []
                for key, value in filter.items():
                    if isinstance(value, list):
                        conditions.append(
                            models.FieldCondition(
                                key=key,
                                match=models.MatchAny(any=value),
                            )
                        )
                    else:
                        conditions.append(
                            models.FieldCondition(
                                key=key,
                                match=models.MatchValue(value=value),
                            )
                        )

                if conditions:
                    query_filter = models.Filter(must=conditions)

            results = self.client.search(
                collection_name=self.config.collection_name,
                query_vector=query_vector,
                limit=limit,
                query_filter=query_filter,
                with_payload=True,
                with_vectors=False,
            )

            search_results = []
            for hit in results:
                payload = hit.payload or {}
                content = payload.pop("content", "")

                search_results.append(
                    SearchResult(
                        id=str(hit.id),
                        score=hit.score,
                        content=content,
                        metadata=payload,
                    )
                )

            return search_results

    async def hybrid_search(
        self,
        query_vector: list[float],
        query_text: str,
        limit: int = 10,
        filter: dict[str, Any] | None = None,
        semantic_weight: float = 0.7,
        keyword_weight: float = 0.3,
    ) -> list[SearchResult]:
        """Hybrid search combining semantic and keyword (BM25) search."""
        if not self._initialized:
            await self.initialize()

        async with tracer.trace("vectorstore.hybrid_search", limit=limit):
            # Semantic search
            semantic_results = await self.search(query_vector, limit * 2, filter)

            # Keyword search using Qdrant's text search (requires payload index)
            # For now, we'll use a simple payload filter approach
            # In production, use Qdrant's sparse vectors or external BM25

            keyword_results = []
            if query_text.strip():
                # Use scroll with text filter as approximation
                try:
                    # This is a simplified version - real BM25 would use sparse vectors
                    scroll_results = self.client.scroll(
                        collection_name=self.config.collection_name,
                        scroll_filter=models.Filter(
                            must=[
                                models.FieldCondition(
                                    key="content",
                                    match=models.MatchText(text=query_text),
                                )
                            ]
                            + (
                                [
                                    models.FieldCondition(key=k, match=models.MatchValue(value=v))
                                    for k, v in filter.items()
                                ]
                                if filter
                                else []
                            )
                        )
                        if filter
                        else models.Filter(
                            must=[
                                models.FieldCondition(
                                    key="content", match=models.MatchText(text=query_text)
                                )
                            ]
                        ),
                        limit=limit * 2,
                        with_payload=True,
                        with_vectors=False,
                    )

                    for hit in scroll_results[0]:
                        payload = hit.payload or {}
                        content = payload.pop("content", "")
                        keyword_results.append(
                            SearchResult(
                                id=str(hit.id),
                                score=1.0,  # Placeholder score
                                content=content,
                                metadata=payload,
                            )
                        )
                except Exception:
                    pass

            # Reciprocal Rank Fusion
            return self._rrf_fusion(semantic_results, keyword_results, limit)

    def _rrf_fusion(
        self,
        semantic_results: list[SearchResult],
        keyword_results: list[SearchResult],
        limit: int,
        k: int = 60,
    ) -> list[SearchResult]:
        """Reciprocal Rank Fusion for combining search results."""
        scores = {}
        result_map = {}

        for rank, result in enumerate(semantic_results):
            scores[result.id] = scores.get(result.id, 0) + 1 / (k + rank + 1)
            result_map[result.id] = result

        for rank, result in enumerate(keyword_results):
            scores[result.id] = scores.get(result.id, 0) + 1 / (k + rank + 1)
            if result.id not in result_map:
                result_map[result.id] = result

        # Sort by combined score
        sorted_ids = sorted(scores.keys(), key=lambda x: scores[x], reverse=True)

        fused_results = []
        for result_id in sorted_ids[:limit]:
            result = result_map[result_id]
            # Create new result with fused score
            fused_results.append(
                SearchResult(
                    id=result.id,
                    score=scores[result_id],
                    content=result.content,
                    metadata=result.metadata,
                )
            )

        return fused_results

    async def delete(self, ids: list[str]) -> bool:
        """Delete documents by IDs."""
        if not self._initialized:
            await self.initialize()

        self.client.delete(
            collection_name=self.config.collection_name,
            points_selector=models.PointIdsList(points=ids),
        )
        return True

    async def get(self, id: str) -> Document | None:
        """Get a document by ID."""
        if not self._initialized:
            await self.initialize()

        results = self.client.retrieve(
            collection_name=self.config.collection_name,
            ids=[id],
            with_payload=True,
            with_vectors=True,
        )

        if not results:
            return None

        hit = results[0]
        payload = hit.payload or {}
        content = payload.pop("content", "")

        return Document(
            id=str(hit.id),
            content=content,
            metadata=payload,
            embedding=hit.vector,
        )

    async def count(self) -> int:
        """Get total document count."""
        if not self._initialized:
            await self.initialize()

        info = self.client.get_collection(self.config.collection_name)
        return info.points_count

    async def close(self) -> None:
        """Close the client."""
        if self.client:
            self.client.close()
            self.client = None
            self._initialized = False


# Factory function
_vector_store_instance: BaseVectorStore | None = None


async def get_vector_store() -> BaseVectorStore:
    """Get or create the global vector store instance."""
    global _vector_store_instance

    if _vector_store_instance is None:
        _vector_store_instance = QdrantVectorStore()
        await _vector_store_instance.initialize()

    return _vector_store_instance


async def close_vector_store() -> None:
    """Close the global vector store."""
    global _vector_store_instance

    if _vector_store_instance:
        await _vector_store_instance.close()
        _vector_store_instance = None
