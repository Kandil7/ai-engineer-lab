"""Unit tests for the RAG context budget (devmate.retrieve.rag._build_context).

Regression guard for the logged mistake: 20 retrieved chunks stuffed into
the system prompt overflowed qwen2.5-coder:7b's Ollama context (HTTP 500).
The budget must bound the context regardless of how many chunks retrieval
returns. No Qdrant, no LLM, no network.
"""

from devmate.config import settings
from devmate.retrieve.rag import RAGPipeline
from devmate.retrieve.retriever import RerankResult


def _chunk(i: int, size: int) -> RerankResult:
    return RerankResult(
        content="x" * size,
        score=1.0 / (i + 1),
        metadata={"filename": f"file_{i}.py", "chunk_type": "function", "name": f"fn_{i}"},
    )


def test_context_respects_char_budget() -> None:
    """20 x 1000-char chunks must not produce a context over the budget."""
    pipeline = RAGPipeline()
    results = [_chunk(i, 1000) for i in range(20)]
    context = pipeline._build_context(results)

    budget = settings.rag_context_char_budget
    # The last appended chunk may overshoot; the *count* of chunks is what the
    # budget bounds — assert total stays under budget + one chunk.
    assert len(context) <= budget + 1100, f"context too large: {len(context)} chars"
    assert context.count("[Source") < 20, "all 20 chunks were stuffed in despite the budget"


def test_context_always_includes_first_chunk() -> None:
    """A single oversized chunk must still be included (never an empty context)."""
    pipeline = RAGPipeline()
    context = pipeline._build_context([_chunk(0, settings.rag_context_char_budget * 3)])
    assert context.startswith("[Source 1:")
    assert "x" * 100 in context


def test_context_empty_results() -> None:
    pipeline = RAGPipeline()
    assert pipeline._build_context([]) == ""


def test_context_preserves_order_and_headers() -> None:
    pipeline = RAGPipeline()
    results = [_chunk(i, 50) for i in range(3)]
    context = pipeline._build_context(results)
    assert "[Source 1: file_0" in context
    assert "[Source 3: file_2" in context
    assert context.index("[Source 1") < context.index("[Source 3")
