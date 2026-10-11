# DevMate Overview

DevMate is an AI assistant for code repositories. You point it at a repository or a
documentation folder, it ingests and indexes the content, and then answers questions
about it with grounded, cited responses.

The system is built as a single continuously-growing service rather than a set of
demos. It combines retrieval-augmented generation (RAG), agents, the Model Context
Protocol (MCP), and observability in one codebase.

## What it can do

- **Ingest** a repository: walk the files, split them into chunks, embed the chunks,
  and store the vectors in Qdrant.
- **Answer questions**: embed the question, retrieve the most relevant chunks, and
  ask a language model to answer using only that context, citing sources.
- **Track cost**: every model call records tokens and an estimated dollar cost.
- **Trace**: every call produces a span for observability.

## Where it runs

DevMate runs offline by default using Ollama for the language model and embeddings.
It can also run against cloud providers. The public demo uses Groq for generation and
OpenAI for embeddings, backed by managed Postgres, Redis, and a Qdrant cluster.
