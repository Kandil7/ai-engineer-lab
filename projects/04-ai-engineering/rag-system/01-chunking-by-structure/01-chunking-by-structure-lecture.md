# RAG System 01: Chunking by Source Structure

## 🎯 Topic Overview

Chunking is the highest-leverage retrieval decision: too large and the
signal drowns, too small and meaning fragments. For structured sources —
books with pages, chapters, and sections — the chunker must respect the
source's own structure. This lecture covers structure-aware chunking, the
two-text discipline, and measuring chunking by retrieval quality.

## 📚 Learning Objectives

By the end of this lecture, you will be able to:

1. Chunk by the source's natural boundaries (page, section, paragraph)
2. Apply the two-text discipline inside chunks (original + searchable)
3. Carry provenance (book_id, page, source_version) on every chunk
4. Measure chunking strategies with recall@k on a labeled set
5. Choose chunk size from the source's structure, not a default

---

## 1. Structure Is the Boundary

A book has pages, chapters, sections, paragraphs. Chunking by those
boundaries preserves meaning: a paragraph is a complete thought, a section
is a complete argument. Blind fixed-size chunking cuts mid-thought and
mid-sentence. The rule: prefer the source's own boundaries, and only fall
back to size limits when a unit is too large.

```python
# Structure-aware: one chunk per paragraph, capped by a token limit
def chunk_paragraphs(text, max_tokens=500):
    chunks = []
    for para in text.split("\n\n"):
        if len(para.split()) <= max_tokens:
            chunks.append(para)
        else:
            chunks.extend(split_long_paragraph(para, max_tokens))
    return chunks
```

## 2. The Two-Text Discipline in Chunks

Every chunk carries two texts: `original` (verbatim, for display and
citation) and `searchable` (normalized, for indexing). The index operates on
`searchable`; the answer cites `original`. Normalization never alters what
the user sees quoted. This is the same discipline from the Arabic NLP
section, now applied at the chunk level.

## 3. Provenance on Every Chunk

Each chunk carries book_id, page, source_version, and a chunk index. The
chunk is traceable to its exact source location — the roadmap's exit test.
A chunk without provenance cannot be cited honestly.

```python
{
    "chunk_id": "b1:p7:2",
    "book_id": "b1",
    "page": 7,
    "source_version": "v1",
    "original": "...",
    "searchable": "...",
}
```

## 4. Measuring Chunking

Chunking choices are measured, not assumed. Fix the labeled query set, fix
k, vary only the chunker, read recall@k. A strategy that gains 5pp recall
is worth its complexity; one that gains nothing is not. The measurement is
the same protocol as the retrieval topics — chunking is evaluated by what
retrieval can find.

## 5. Code and Mixed Sources

Code has hard structure (functions, classes) that paragraphs approximate
poorly. AST-aware chunking splits on syntax boundaries with line ranges, so
a retrieved chunk is a complete citable unit. For Athar's books, page and
paragraph boundaries are the natural units; for code corpora, syntax
boundaries win. The chunker follows the source's structure.

## Common Mistakes

- Fixed-size chunking that cuts mid-thought on structured sources.
- Normalizing the display text (breaks the quote).
- Chunks without provenance (uncitable).
- Choosing a chunker without measuring recall.

## Key Takeaways

1. Chunk by the source's natural boundaries.
2. Two texts per chunk: original for citation, searchable for matching.
3. Provenance on every chunk.
4. Measure chunking by retrieval recall.