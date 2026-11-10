# Chapter Numbering and Naming Conventions

This guide explains how to name new chapters, their IDs, and the related identifiers (glossary terms, concepts, labs, figures, flashcards, quiz items). Follow these conventions to keep your chapters consistent and machine-readable.

---

## 1. Chapter Identity

### `chapterId`

Used for:
- File naming: `build/<chapterId>.html`
- localStorage progress keys: `study-studio.progress.<chapterId>`
- Lab and figure cross-references

**Rules:**
- Must match regex: `^[a-z0-9][a-z0-9-]*$`
- Lowercase letters, digits, hyphens only
- No spaces or special characters
- Start with a letter

**Examples:**
```json
"chapterId": "rag-pipeline"
"chapterId": "transformer-architecture"
"chapterId": "llm-evaluation-guide"
```

**Invalid examples:**
- `"rag pipeline"` (contains space)
- `"RAG-Pipeline"` (uppercase letters)
- `"_rag"` (starts with underscore)

---

## 2. Glossary Term IDs

Each glossary entry needs a unique `id` that links to technical concepts in the text.

### Naming pattern: `wNNN`

Where NNN is a zero-padded number starting from 01 within the chapter.

**Examples:**
```json
{ "id": "w01", "term": "attention" }
{ "id": "w02", "term": "token" }
{ "id": "w03", "term": "embedding" }
```

### Usage in text

Reference glossary terms in paragraph prose using `<mark data-id="w01">attention</mark>`:

```json
"text": "The <mark data-id=\"w01\">attention</mark> mechanism weighs earlier tokens."
```

---

## 3. Concept IDs

Used for the concept map and organizing quiz items.

### Naming pattern: `cNNN`

Where NNN is a zero-padded number starting from 01.

**Examples:**
```json
{ "id": "c01", "label": "Attention" }
{ "id": "c02", "label": "Token" }
{ "id": "c03", "label": "Embedding" }
```

### Linking to glossary terms

Concepts can reference the glossary term that defines it:

```json
{
  "id": "c01",
  "label": "Attention",
  "wordIds": ["w01"]
}
```

---

## 4. Lab IDs

Each lab simulation gets a unique identifier for cross-referencing.

### Naming pattern: `lNNN`

Where NNN is a zero-padded number starting from 01.

**Examples:**
```json
{ "id": "l01", "title": "Attention heatmap" }
{ "id": "l02", "title": "RAG pipeline simulator" }
{ "id": "l03", "title": "Training dynamics" }
```

### Linking concepts to labs

```json
{
  "id": "c01",
  "label": "Attention",
  "labId": "l01"
}
```

---

## 5. Figure IDs

Inline SVG figures with hotspot annotations.

### Naming pattern: `fNNN`

Where NNN is a zero-padded number starting from 01.

**Examples:**
```json
{ "id": "f01", "title": "Score-weight-mix cycle" }
{ "id": "f02", "title": "Transformer architecture" }
```

---

## 6. Flashcard IDs

For Leitner-box spaced repetition cards.

### Naming pattern: `kNNN`

Where NNN is a zero-padded number starting from 01.

**Examples:**
```json
{ "id": "k01", "front": "What does attention do?" }
{ "id": "k02", "front": "token" }
```

---

## 7. Quiz Item IDs

For active recall questions.

### Naming pattern: `qNNN`

Where NNN is a zero-padded number starting from 01.

**Examples:**
```json
{ "id": "q01", "type": "mcq", "prompt": "What does attention do?" }
{ "id": "q02", "type": "true-false", "prompt": "Attention is quadratic." }
```

---

## 8. ID Assignment Workflow

When creating a new chapter:

1. **Start numbering at 01** for each category (w, c, l, f, k, q)
2. **Increment sequentially** as you add items
3. **Skip reserved IDs** — don't reuse IDs from other chapters
4. **Link concept to glossary/lab** using the ID fields

### Example: Assigning IDs for a new chapter

```json
{
  "meta": {
    "chapterId": "my-new-chapter"
  },
  "glossary": [
    { "id": "w01", "term": "embedding", ... },
    { "id": "w02", "term": "vector", ... }
  ],
  "conceptMap": {
    "nodes": [
      { "id": "c01", "label": "Embedding space", "wordIds": ["w01"], "labId": "l01" },
      { "id": "c02", "label": "Vector similarity", "wordIds": ["w02"] }
    ]
  },
  "labs": [
    { "id": "l01", "title": "Embedding visualization", ... }
  ],
  "flashcards": [
    { "id": "k01", "front": "What is an embedding?", ... }
  ],
  "quiz": [
    { "id": "q01", "type": "mcq", ... }
  ]
}
```

---

## 9. Best Practices

- **Keep IDs simple**: Only use letters, digits, and hyphens in `chapterId`
- **Document the mapping**: If you create external references to your chapter, include a mapping table
- **Review before building**: Verify all IDs are unique across categories (no w01 = c01 confusion)
- **Use consistent spacing**: Don't leave gaps in numbering; use l01, l02, not l01, l03

---

## 10. Reserved ID Ranges

The study-studio schema doesn't reserve ranges, but these conventions help avoid conflicts when:

- Sharing chapters across projects
- Exporting/importing content between tools
- Linking to external documentation

**Suggested ranges:**
- Glossary terms: `w001` - `w999`
- Concepts: `c001` - `c999`
- Labs: `l001` - `l999`
- Figures: `f001` - `f999`
- Flashcards: `k001` - `k999`
- Quiz items: `q001` - `q999`

These ranges are not enforced by the schema, but using them makes it easier to identify and fix duplicate IDs during review.
