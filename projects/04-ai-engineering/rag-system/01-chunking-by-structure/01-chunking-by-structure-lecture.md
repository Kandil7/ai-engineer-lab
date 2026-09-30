# RAG System 01: Chunking by Source Structure

## Topic Overview

Chunking is the bridge between raw source text and retrievable passages. The boundary decision — where one passage ends and the next begins — determines retrieval quality more than the embedding model or the reranker. A chunk that splits a paragraph in half will never be retrieved as a coherent unit; a chunk that merges two unrelated topics will retrieve noise for both. For Arabic Islamic texts, this decision is harder than for English prose because the source structure is hierarchical (verse, hadith, legal ruling) and the text conventions (diacritics, citations) carry meaning.

The core insight: **the boundary should follow the source's own structure, not a character count.** A verse boundary is always a valid passage boundary. A paragraph boundary is usually valid. A character count is a last resort.

## Learning Objectives

By the end of this lecture, you will be able to:

1. Explain why character-count chunking fails for structured text
2. Identify the natural boundary types in Arabic Islamic sources
3. Design a structure-aware chunker that respects hierarchy
4. Carry provenance (book, page, version) on every chunk
5. Implement the two-text discipline (original + searchable form)
6. Test chunking quality with a golden set
7. Connect chunking decisions to downstream retrieval metrics

## Prerequisites

- Arabic text fundamentals (arabic-nlp 01)
- Basic understanding of RAG pipelines

---

## 1. The Chunking Problem

### What chunking does

A source document is a continuous stream of text. Retrieval needs
discrete passages — units small enough to embed meaningfully and large
enough to be self-contained. Chunking performs this split.

```
Source:    [continuous text stream]
              ↓ chunking
Passages:  [chunk 1] [chunk 2] [chunk 3] ...
              ↓ embedding
Vectors:   [vec 1]   [vec 2]   [vec 3]   ...
```

### Why boundaries matter

Consider a Quranic verse that spans three lines. If a character-count
chunker cuts at the midpoint of line two, the resulting passage contains
a fragment of the verse and a fragment of the next verse. When the user
asks about the verse, the retriever will find the fragment — but the
fragment is incomplete, and the answer built from it will be wrong.

```
Bad boundary (character count at 200):
  "...ذلك الكتاب لا ريب فيه هدى للمتقين الذين يؤمنون بالغيب ويقيمون"
  (cuts mid-verse, includes start of next verse)

Good boundary (verse structure):
  "ذلك الكتاب لا ريب فيه هدى للمتقين" (verse 2, complete)
  "الذين يؤمنون بالغيب ويقيمون الصلاة" (verse 3, complete)
```

### The three approaches

| Approach | Boundary source | Quality | Cost |
|----------|----------------|---------|------|
| Character count | Fixed length | Poor for structured text | Cheap |
| Sliding window | Overlapping windows | Better recall, poor precision | Medium |
| **Structure-aware** | **Source hierarchy** | **Best** | **Needs parsing** |

---

## 2. Structure-Aware Chunking

### The principle

**The source's own structure defines the passages.** Every author
provides structure markers: chapter headings, section titles, verse
numbers, hadith boundaries, paragraph breaks. These are the natural
passage boundaries.

### Boundary types in Arabic Islamic sources

| Source | Boundary | Example marker |
|--------|----------|----------------|
| Quran | Verse (آية) | Verse number, "﴿﴾" markers |
| Hadith | Narration (حديث) | "عن ..." / "قال ..." / isnad chains |
| Fiqh | Ruling (مسألة) | "مسألة:" / "الحكم:" / numbered sections |
| Tafsir | Commentary unit | Verse reference + commentary |
| General prose | Paragraph / section | "##" headings, blank lines |

### The hierarchy

Arabic Islamic texts have a natural hierarchy. A chunker that respects
this hierarchy produces passages at the right granularity:

```
Book
  └─ Chapter (باب)
       └─ Section (فصل)
            └─ Ruling/Narration (مسألة/حديث)
                 └─ Verse (آية)  ← often the best passage unit
```

**The passage should be the smallest self-contained unit.** For Quranic
tafsir, that is often one verse plus its commentary. For hadith
collections, that is one narration. For fiqh manuals, that is one ruling.

### Implementation sketch

```python
def chunk_by_structure(document: str) -> list[dict]:
    """Split a document at its natural structural boundaries."""
    chunks = []
    current = []
    current_meta = {"verse": None, "hadith": None}

    for segment in parse_segments(document):
        if is_boundary(segment):
            # Flush the current chunk
            if current:
                chunks.append(make_chunk(current, current_meta))
            current = [segment.text]
            current_meta = extract_metadata(segment)
        else:
            current.append(segment.text)

    if current:
        chunks.append(make_chunk(current, current_meta))
    return chunks
```

The key functions: `is_boundary(segment)` detects structural breaks;
`extract_metadata(segment)` captures the provenance.

---

## 3. The Two-Text Discipline

### What it means

Every passage exists in two forms:

1. **Original text** — the verbatim source, used for display and citation
2. **Searchable text** — a normalized form, used for embedding and retrieval

The two forms are stored together. The original is what the user sees;
the searchable form is what the embedding model processes.

```python
class Passage:
    original: str  # "قالَ اللهُ تَعالى: ﴿إِنَّ اللهَ مَعَ الصَّابِرِينَ﴾"
    searchable: str  # "قال الله تعالى ان الله مع الصابرين"
    source: SourceLocation
```

### Why both

- **Original:** The user needs the exact wording. Arabic diacritics,
  punctuation, and citation markers carry meaning. Displaying normalized
  text is unacceptable for scholarly content.
- **Searchable:** Embedding models need consistent input. Normalized
  text (without diacritics, with unified alef forms) produces more
  stable embeddings. A query "الله" should match "الله" and "اللَّهَ".

### The rule

**Never lose the original.** Normalization is for retrieval, not for
display. The two-text discipline is enforced in the data model — a
passage without both forms is invalid.

---

## 4. Provenance on Every Chunk

### What to carry

Every chunk must answer: where did this text come from?

```python
class SourceLocation:
    book_id: str  # "b3" (book 3)
    page: int  # 12 (page 12)
    source_version: str  # "v2" (the corpus version)
    chunk_index: int  # 0 (position in the document)
```

### Why provenance matters

1. **Citation:** The answer cites evidence ids. The id encodes the source.
2. **Staleness detection:** If the corpus version changes, cached chunks
   from the old version are stale.
3. **Debugging:** When retrieval returns the wrong chunk, provenance
   identifies the source location for diagnosis.

### The citation path

```
User query → retrieval → context (with evidence ids)
    → answer (with citations: b3:p12:0)
    → user clicks citation → sees original text + source location
```

The evidence id `b3:p12:0` = book b3, page 12, chunk 0. The id is
deterministic — the same source always produces the same id.

---

## 5. Edge Cases and Failure Modes

### Edge case: a verse that spans two pages

The chunker should keep the verse together even if it crosses a page
boundary. The provenance records both pages. The rule: structural
integrity beats page alignment.

### Edge case: a hadith with a long isnad chain

The chain (isnad) is part of the hadith but may be hundreds of words.
Options: (a) keep the full hadith including isnad, (b) separate the
isnad from the matn (text), (c) include a truncated isnad. The right
choice depends on the retrieval goal — if the question is about the
ruling, the matn matters more.

### Edge case: repeated text

Basmala ("بسم الله الرحمن الرحيم") appears thousands of times. A naive
chunker creates thousands of identical chunks. The fix: either merge
them (keeping the first occurrence) or add a location marker so each is
distinct.

### Failure mode: chunks too small

A chunk of 5 words is not self-contained. The retriever finds it but the
answer has no context. The minimum chunk size should be one complete
structural unit — at minimum, one sentence.

### Failure mode: chunks too large

A chunk of 2000 words covers multiple topics. The retriever finds it for
any of the topics, diluting the signal. The maximum should be one
structural unit plus minimal surrounding context.

---

## 6. Testing Chunking Quality

### What to test

| Test | What it checks | Pass condition |
|------|---------------|----------------|
| Boundary alignment | Chunks end at structural boundaries | No mid-verse cuts |
| Self-contained | Each chunk makes sense alone | Human reads it, understands |
| Coverage | All source text appears in some chunk | No text lost |
| Uniqueness | No duplicated chunks | Deduplication works |
| Provenance | Every chunk has complete source info | book_id, page, version present |

### The golden set for chunking

Create 20-30 known passages from the corpus. Check that the chunker
produces them as single units. If a known verse appears split across two
chunks, the chunker has a bug.

---

## 7. Connection to the Roadmap

The roadmap's exit test: "chunks respect source structure (verse, hadith,
passage boundaries)." This is not a preference — it is the difference
between a RAG system that answers correctly and one that retrieves noise.

The chunking decision cascades:
- Bad chunks → bad embeddings → bad retrieval → bad context → bad answers
- Good chunks → clean embeddings → precise retrieval → clear context → grounded answers

Chunking is the foundation. Everything downstream depends on it.

---

## Real-World Application

In a production Islamic-text RAG system:

1. The ingestion pipeline parses each source document by structure.
2. Each structural unit becomes one chunk with full provenance.
3. The original text and searchable text are stored together.
4. The chunk id is deterministic (book:page:chunk).
5. The golden set tests boundary alignment on known passages.
6. Retrieval metrics (recall@5, MRR) are measured against the golden set.

The chunking quality directly determines whether a user asking "ما حكم
الصلاة في السفر؟" gets the complete, correct ruling or a fragment.

---

## Common Mistakes

1. **Character-count chunking on structured text** — cuts mid-verse,
   mid-hadith, mid-ruling. Use the source structure.

2. **Losing the original text** — normalizing for retrieval but storing
   only the normalized form. Keep both.

3. **No provenance** — chunks without source location. Cannot cite,
   cannot detect staleness, cannot debug.

4. **Chunks too small** — single words or fragments. Not self-contained.

5. **Chunks too large** — whole pages or sections. Multiple topics
   dilute retrieval.

6. **Ignoring Arabic text conventions** — not handling diacritics,
   basmala repetition, or citation markers in the chunker.

7. **No boundary testing** — never checking that known passages appear
   as single units in the golden set.

---

## Key Takeaways

1. Boundaries follow the source's structure, not a character count.
2. The smallest self-contained unit is the right passage size.
3. Every chunk carries original text AND searchable text.
4. Provenance (book, page, version) is mandatory.
5. Bad chunking cascades into bad answers — get this right first.

---

## Self-Check Questions

1. Why does character-count chunking fail for Quranic text?
2. What are the natural boundary types in hadith collections?
3. What is the "two-text discipline" and why does it matter?
4. What provenance fields does every chunk need?
5. How would you test that your chunker respects verse boundaries?

---

## Further Reading / Connections

- **arabic-nlp 02** — normalization for the searchable text form
- **rag-system 02** — hard filters on chunk metadata (provenance)
- **rag-system 04** — how chunks become the context
- **ai-evaluation 01** — golden sets for testing chunking quality
- **data-engineering 02** — schemas and contracts for chunk metadata