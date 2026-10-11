"""Ingest a small baked-in sample corpus on startup.

A production image has no repository on disk, so a fresh deploy has an empty
vector store and cannot answer anything. This loads ``sample_corpus/`` (shipped
in the image) and ingests it once, when the collection is empty.

Failure is never fatal: if there is no corpus, the store already has data, or
the embedding provider is unavailable, it logs and returns 0 so the API still
starts (and ``/ready`` reports the true state).
"""

from __future__ import annotations

import logging
from pathlib import Path

from devmate.config import settings
from devmate.ingest.chunker import DocumentLoader, get_chunker

logger = logging.getLogger(__name__)


async def ensure_sample_corpus(path: str | Path | None = None) -> int:
    """Ingest the sample corpus if the vector store is empty.

    Returns the number of chunks added (0 when skipped or on failure).
    """
    from devmate.index.vector_store import get_vector_store
    from devmate.retrieve.rag import get_rag_pipeline

    corpus = Path(path if path is not None else settings.sample_corpus_path)
    if not corpus.exists():
        logger.info("sample corpus not found at %s; skipping", corpus)
        return 0

    try:
        store = await get_vector_store()
        if await store.count() > 0:
            logger.info("vector store already populated; skipping sample ingest")
            return 0

        loader = DocumentLoader(chunker=get_chunker("recursive"))
        documents = list(loader.load_repository(corpus))
        if not documents:
            logger.info("sample corpus at %s produced no documents", corpus)
            return 0

        pipeline = await get_rag_pipeline()
        chunks = await pipeline.ingest_documents(documents)
        logger.info("ingested %d sample chunks from %s", chunks, corpus)
        return chunks
    except Exception as exc:
        logger.warning("sample corpus ingest skipped: %s", exc)
        return 0
