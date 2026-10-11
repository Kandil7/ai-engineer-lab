# DevMate Architecture

DevMate is a layered Python service. Each layer has one responsibility and is
tested in isolation.

## Layers

- **ingest**: reads files (`DocumentLoader`) and splits them into chunks. Three
  chunkers are available: `fixed` (fixed-size windows), `recursive` (splits on
  structure), and `ast_aware` (splits on code boundaries).
- **index**: turns text into vectors (`EmbeddingService`) and stores them in a
  vector database behind a `BaseVectorStore` interface. The production adapter is
  Qdrant.
- **retrieve**: hybrid retrieval (dense vectors plus keyword matching) followed by
  an optional reranker, returning the top chunks.
- **llm**: a provider-agnostic client with streaming, retries, structured output,
  and a fallback chain across Anthropic, OpenAI, Groq, and Ollama.
- **obs**: tracing (Langfuse) and a cost ledger.
- **api**: a FastAPI application exposing `/health`, `/ready`, `/ask`, `/ingest`,
  and `/ai/rag/query`.
- **db**: SQLAlchemy models for conversations, messages, eval runs, cost records,
  and documents, with Alembic migrations.

## Data flow

A question flows: embed, retrieve, build a bounded context, generate an answer,
return it with sources and usage. Ingestion flows the other way: load, chunk,
embed, upsert.
