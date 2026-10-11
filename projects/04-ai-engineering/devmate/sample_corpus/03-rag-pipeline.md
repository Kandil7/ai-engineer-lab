# The RAG Pipeline

Retrieval-augmented generation (RAG) grounds a language model in retrieved
documents so it answers from real content instead of guessing.

## Steps

1. **Embed the question** into a vector using the embedding service.
2. **Retrieve** the nearest chunks from the vector store. DevMate supports hybrid
   retrieval, combining dense vector similarity with keyword matching, then an
   optional reranker to reorder the candidates.
3. **Build the context** under a character budget. The retrieval top-k is a
   candidate count, not a prompt guarantee: stuffing every chunk into the prompt
   overflows small models and dilutes what matters. The first chunk is always
   included even if it alone exceeds the budget.
4. **Generate** the answer with the language model, instructed to use only the
   provided context and to cite sources.

## Chunking

Chunking decides the retrieval unit. Fixed-size chunking is simple and predictable.
Recursive chunking respects structure. AST-aware chunking splits on code
boundaries, which helps for source code because a function stays in one chunk.

## Abstention

If the retrieved context does not contain enough information, the pipeline is
instructed to say so rather than invent an answer. This is the difference between a
useful assistant and a confident wrong one.
