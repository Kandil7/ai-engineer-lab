# Schema Walkthrough

This guide walks through each property of the `CHAPTER_DATA` schema with examples. Use it to write new chapters that conform to the contract without modifying engine code.

The full schema is defined in `schema/chapter.schema.json`. This document explains what each field means and how to populate it correctly.

---

## Top-Level Structure

```json
{
  "meta": {...},           // Chapter identity and licensing
  "sections": [...],       // Hierarchical content with paragraphs
  "glossary": [...],       // Curated terms for popovers
  "conceptMap": {...},     // Concept relationships
  "labs": [...],           // Interactive simulations
  "figures": [...],        // Inline SVG diagrams
  "flashcards": [...],     // Spaced repetition cards
  "quiz": [...],           // Active recall questions
  "collocations": [...],   // Common phrases with Arabic meanings
  "connections": [...]     // Links to related chapters
}
```

**Required fields**: `meta`, `sections`, `glossary`, `conceptMap`, `labs`, `figures`, `flashcards`, `quiz`, `collocations`, `connections`

All arrays must have at least one element. Empty objects are not allowed.

---

## 1. Meta Object

Defines the chapter's identity, source, and language settings.

```json
"meta": {
  "chapterId": "rag-pipeline",              // Stable slug for file naming
  "title": "Retrieval-Augmented Generation", // Display title
  "subtitle": "Building RAG systems",       // Optional subtitle
  "sourceTitle": "My AI Book",              // Source document name
  "sourceType": "original",                 // See enum below
  "sourceLocator": "Chapter 4",             // Chapter number/anchor
  "license": "CC-BY-4.0",                   // See enum below
  "attribution": "Required attribution line.", // For licensed content
  "language": "en-ar",                      // en | ar | en-ar
  "estMinutes": 25,                         // Estimated reading time
  "conceptCount": 5                         // Number of concept-map nodes
}
```

### Meta Properties

| Property | Type | Required | Description |
|----------|------|----------|-------------|
| `chapterId` | string | Yes | Stable slug matching `^[a-z0-9][a-z0-9-]*$` |
| `title` | string | Yes | Display title for the chapter |
| `subtitle` | string | No | Optional subtitle |
| `sourceTitle` | string | Yes | Book/document name shown in credits |
| `sourceType` | enum | Yes | book \| roadmap \| paper \| repo-doc \| original |
| `sourceLocator` | string | Yes | Chapter number, section anchor, or local path |
| `license` | enum | Yes | personal-study \| CC-BY-4.0 \| public-domain \| MIT |
| `attribution` | string | No | Required attribution for licensed content |
| `language` | enum | Yes | en \| ar \| en-ar |
| `estMinutes` | integer | Yes | Reading time estimate (1-600) |
| `conceptCount` | integer | Yes | Number of nodes in conceptMap |

### sourceType Values

- **book**: Copyrighted text that must stay out of the repo (only study layer committed)
- **roadmap**: Learning path documentation
- **paper**: Academic paper excerpts
- **repo-doc**: Documentation from a repository
- **original**: Original content authored for the studio

### license Values

- **personal-study**: Text may not be committed to public repos
- **CC-BY-4.0**: Creative Commons attribution required
- **public-domain**: No restrictions
- **MIT**: Permissive license with minimal requirements

---

## 2. Sections Array

Hierarchical content divided into sections of increasing depth (level 1-3).

```json
"sections": [
  {
    "id": "s1",                               // Section identifier
    "title": "Introduction to RAG",           // Section title
    "order": 1,                               // Display order (1-based)
    "level": 1,                               // Depth level (1 = highest)
    "paragraphs": [
      { "kind": "text", "text": "..."},
      { "kind": "code", "code": "..."},
      { "kind": "formula", "formula": "..." }
    ],
    "keySentences": [                         // Skim-mode highlights
      "RAG combines retrieval with generation."
    ],
    "takeaways": [                            // Key learning points
      "RAG retrieves context before generating answers.",
      "This reduces hallucinations."
    ],
    "studyAid": {                             // AI-badged study aid
      "whyItMatters": "...",
      "badge": "AI"
    },
    "confusion": {                            // Simplified explanation
      "simpleEnglish": "...",
      "simpleArabic": "...",
      "analogy": "..."
    },
    "prediction": {                           // Predictive question
      "question": "...",
      "answer": "..."
    },
    "wordIds": ["w01", "w02"]                 // Glossary terms in this section
  }
]
```

### Section Properties

| Property | Type | Required | Description |
|----------|------|----------|-------------|
| `id` | string | Yes | Pattern: `^s[0-9]+$` (e.g., "s1") |
| `title` | string | Yes | Section title |
| `order` | integer | Yes | Display order (minimum 1) |
| `level` | integer | Yes | Depth level (1-3, where 1 = highest) |
| `paragraphs` | array | Yes | List of paragraph objects |
| `keySentences` | array | No | Substrings for skim mode |
| `takeaways` | array | No | Key learning points |
| `studyAid` | object | No | AI-badged study aid |
| `confusion` | object | No | Simplified explanation |
| `prediction` | object | No | Predictive question |
| `wordIds` | array | No | Glossary IDs appearing in section |

### Paragraph Kinds

- **text**: Regular prose paragraph
- **code**: Code block with language specification
- **list**: Bulleted list with items
- **quote**: Block quote
- **formula**: Mathematical formula with symbol definitions

### studyAid Object

Provides an AI-generated study aid badge next to the text.

```json
"studyAid": {
  "whyItMatters": "RAG retrieval quality is about selecting relevant context.",
  "badge": "AI"
}
```

### confusion Object

Simplifies complex concepts for learners who struggle.

```json
"confusion": {
  "simpleEnglish": "The model picks relevant documents instead of guessing.",
  "simpleArabic": "النموذج يختار المستندات ذات الصلة بدلاً من التخمين.",
  "analogy": "Like a librarian who finds the right books for your question."
}
```

### prediction Object

Prepares learners by asking them to predict before revealing answers.

```json
"prediction": {
  "question": "If we retrieve more documents, will accuracy improve?",
  "answer": "Not necessarily; too much context can confuse the model."
}
```

---

## 3. Glossary Array

Curated technical and academic vocabulary for rich popovers.

```json
"glossary": [
  {
    "id": "w01",                    // Unique term ID
    "term": "attention",            // Term to display
    "ipa": "əˈtɛnʃən",              // Optional pronunciation
    "meaningEn": "...",             // English definition
    "meaningAr": "...",             // Arabic definition
    "wordType": "noun",             // noun | verb | adjective | adverb | phrase
    "example": "...",               // Example sentence
    "technical": true,              // Whether this is a technical term
    "conceptId": "c01",             // Link to concept map node
    "labId": "l01"                  // Link to lab simulation
  }
]
```

### Glossary Properties

| Property | Type | Required | Description |
|----------|------|----------|-------------|
| `id` | string | Yes | Pattern: `^w[0-9]+$` (e.g., "w01") |
| `term` | string | Yes | Term to display in text |
| `ipa` | string | No | Phonetic pronunciation (IPA) |
| `meaningEn` | string | Yes | English definition |
| `meaningAr` | string | Yes | Arabic definition |
| `wordType` | enum | Yes | Part of speech |
| `example` | string | No | Example sentence |
| `technical` | boolean | No | Whether term is technical vocabulary |
| `conceptId` | string | No | Link to concept map node |
| `labId` | string | No | Link to lab simulation |

### wordType Values

- **noun**: Person, place, thing, or idea
- **verb**: Action or state
- **adjective**: Describing word
- **adverb**: Modifying word (usually ends in -ly)
- **phrase**: Multi-word expression

---

## 4. ConceptMap Object

Visual concept map showing relationships between key ideas.

```json
"conceptMap": {
  "nodes": [
    {
      "id": "c01",                  // Node identifier
      "label": "Attention",         // Display label
      "kind": "core",               // core | supporting | advanced
      "definition": "...",          // Concept definition
      "sectionId": "s1",            // Section where concept is introduced
      "labId": "l01",               // Related lab (optional)
      "wordIds": ["w01"]            // Glossary terms defining this concept
    }
  ],
  "edges": [
    { "from": "c01", "to": "c02", "relation": "operates over" },
    { "from": "c03", "to": "c04", "relation": "enables" }
  ],
  "learningPath": ["c01", "c02", "c03"] // Suggested study order
}
```

### ConceptMap Properties

| Property | Type | Required | Description |
|----------|------|----------|-------------|
| `nodes` | array | Yes | List of concept nodes |
| `edges` | array | Yes | List of relationship edges |
| `learningPath` | array | No | Suggested study order |

### Concept Node Properties

| Property | Type | Required | Description |
|----------|------|----------|-------------|
| `id` | string | Yes | Pattern: `^c[0-9]+$` (e.g., "c01") |
| `label` | string | Yes | Display label for the concept |
| `kind` | enum | Yes | core \| supporting \| advanced |
| `definition` | string | No | Concept definition |
| `sectionId` | string | No | Section where concept is introduced |
| `labId` | string | No | Related lab (optional) |
| `wordIds` | array | No | Glossary terms defining this concept |

### edge relation Examples

- "operates over": Concept applies to another concept's domain
- "enables": One concept enables another
- "contrasts with": Two opposing concepts
- "extends": Builds upon another concept
- "requires": Prerequisite relationship

---

## 5. Labs Array

Interactive simulations for hands-on learning.

```json
"labs": [
  {
    "id": "l01",                    // Lab identifier
    "title": "Attention heatmap",   // Lab title
    "goal": "See which tokens attend to each other.", // Learning goal
    "kind": "attention",            // See valid kinds below
    "controls": [
      {
        "id": "sentence",          // Control identifier
        "label": "Sentence",       // Display label
        "kind": "text",            // slider | toggle | select | text
        "default": "the bank approved the river loan"
      },
      {
        "id": "sharpness",
        "label": "Sharpness",
        "kind": "slider",
        "min": 0.5,
        "max": 4,
        "step": 0.1,
        "default": 1.5,
        "unit": "x"
      }
    ],
    "tasks": [
      {
        "prompt": "Hover the query token 'bank' and read the weight on 'river'.",
        "check": "The river weight is high because bank and river belong to the same phrase."
      },
      {
        "prompt": "Switch the query to 'approved'.",
        "check": "The river weight drops."
      }
    ],
    "takeawayEn": "...",            // One-line takeaway in English
    "takeawayAr": "...",            // One-line takeaway in Arabic
    "simulationNote": "Illustrative simulation, not real model output." // Required exact string
  }
]
```

### Lab Properties

| Property | Type | Required | Description |
|----------|------|----------|-------------|
| `id` | string | Yes | Pattern: `^l[0-9]+$` (e.g., "l01") |
| `title` | string | Yes | Lab title |
| `goal` | string | Yes | Learning goal |
| `kind` | enum | Yes | See valid kinds below |
| `controls` | array | Yes | Input controls for the simulation |
| `tasks` | array | Yes | Exactly 3 guided tasks with prompts and checks |
| `takeawayEn` | string | Yes | One-line takeaway in English |
| `takeawayAr` | string | Yes | One-line takeaway in Arabic |
| `simulationNote` | constant | Yes | Exact required string |

### Valid Lab Kinds

- **tokenizer**: Tokenize text and show token IDs
- **embedding**: Vector space visualization
- **attention**: Attention weight distribution
- **sampling**: Temperature/k-top sampling demonstration
- **rag-pipeline**: Multi-step RAG simulation
- **training**: SGD/Adam optimizer visualization
- **quantization**: Weight precision impact
- **metrics**: Evaluation metric calculation
- **cost-latency**: Cost and latency estimation
- **generic**: Custom lab runner template

### Control Types

- **slider**: Range input with min, max, step
- **toggle**: Boolean on/off switch
- **select**: Dropdown or radio buttons
- **text**: Text input (limited to short values)

---

## 6. Figures Array

Inline SVG diagrams with hotspot annotations and step-by-step narration.

```json
"figures": [
  {
    "id": "f01",                      // Figure identifier
    "title": "Score-weight-mix cycle", // Figure title
    "svg": "<svg ...>",               // Inline SVG markup
    "captionEn": "...",               // Caption in English
    "captionAr": "...",               // Caption in Arabic
    "steps": [                        // Step-by-step narration
      {
        "narrativeEn": "Score: compare tokens.",
        "narrativeAr": "الدرجة: قارن الرموز.",
        "highlight": ["f01-box"]      // Element IDs to highlight
      }
    ],
    "hotspots": [                     // Interactive annotations
      {
        "target": "f01-s",            // SVG element ID
        "what": "Compares query against keys.",
        "inputs": "Current token, earlier tokens.",
        "outputs": "Raw scores.",
        "mistakes": "Treating score as probability."
      }
    ],
    "buildOrder": ["f01-s", "f01-w"] // Correct assembly order (optional)
  }
]
```

### Figure Properties

| Property | Type | Required | Description |
|----------|------|----------|-------------|
| `id` | string | Yes | Pattern: `^f[0-9]+$` (e.g., "f01") |
| `title` | string | Yes | Figure title |
| `svg` | string | Yes | Inline SVG markup |
| `captionEn` | string | Yes | English caption |
| `captionAr` | string | Yes | Arabic caption |
| `steps` | array | No | Step-by-step narration |
| `hotspots` | array | No | Interactive annotations |
| `buildOrder` | array | No | Correct assembly order |

### SVG Rules

- No external image references (no `url()` with http/https)
- No script elements
- All shapes must be closed (SVG validates)
- Use semantic elements (`<rect>`, `<circle>`, `<path>`) for hotspots
- Assign IDs to elements you want to highlight or annotate

### hotspot Object

Describes what each interactive element represents.

| Property | Type | Required | Description |
|----------|------|----------|-------------|
| `target` | string | Yes | SVG element ID to target |
| `what` | string | Yes | What this part does |
| `inputs` | string | Yes | Input data description |
| `outputs` | string | Yes | Output description |
| `mistakes` | string | Yes | Common mistakes with this component |

---

## 7. Flashcards Array

Spaced repetition cards for vocabulary retention.

```json
"flashcards": [
  {
    "id": "k01",                      // Card identifier
    "front": "What does attention do?", // Front side
    "back": "It scores earlier tokens...", // Back side
    "backAr": "تحسب درجة كل رمز سابق...", // Arabic back (optional)
    "kind": "term",                   // term | en-ar | code
    "conceptId": "c01",               // Related concept
    "code": "def attention(...):"     // Code snippets (optional)
  }
]
```

### Flashcard Properties

| Property | Type | Required | Description |
|----------|------|----------|-------------|
| `id` | string | Yes | Pattern: `^k[0-9]+$` (e.g., "k01") |
| `front` | string | Yes | Front side text |
| `back` | string | Yes | Back side in English |
| `backAr` | string | No | Arabic translation (optional) |
| `kind` | enum | Yes | term | en-ar | code |
| `conceptId` | string | No | Related concept from conceptMap |
| `code` | string | No | Code snippet for kind=code |

### Flashcard kinds

- **term**: Standard term definition card
- **en-ar**: English-to-Arabic translation card
- **code**: Programming concept or API reference

---

## 8. Quiz Array

Active recall questions with multiple question types.

```json
"quiz": [
  {
    "id": "q01",                      // Question identifier
    "type": "mcq",                    // See valid types below
    "prompt": "What does attention do?",
    "options": [
      "It scores every earlier token...",
      "It predicts the next token directly",
      "It compresses the input"
    ],
    "answer": ["It scores every earlier token..."], // Correct answer(s)
    "explanationEn": "...",           // English explanation
    "explanationAr": "...",           // Arabic explanation
    "conceptId": "c01",               // Related concept
    "needsConfidence": true           // Show confidence rating (optional)
  }
]
```

### Quiz Item Types

| Type | Description | Answer Format |
|------|-------------|---------------|
| **mcq** | Multiple choice (4 options recommended) | Array of correct option texts |
| **true-false** | True or false statement | `["True"]` or `["False"]` |
| **order** | Reorder items into correct sequence | Ordered array of option texts |
| **match** | Match pairs from two columns | Array of "left \| right" pairs |
| **fill-code** | Fill in code snippet | Correct code line(s) |
| **spot-mistake** | Identify error in statement/code | Explanation text |
| **explain** | Explain concept in own words | Key phrases to include |

### Quiz Item Properties

| Property | Type | Required | Description |
|----------|------|----------|-------------|
| `id` | string | Yes | Pattern: `^q[0-9]+$` (e.g., "q01") |
| `type` | enum | Yes | See valid types above |
| `prompt` | string | Yes | Question prompt |
| `options` | array | No | Answer options (for mcq, true-false, order) |
| `answer` | array | Yes | Correct answer(s) or ordered list |
| `answerText` | string | No | Human-readable answer for fill-code |
| `explanationEn` | string | Yes | English explanation |
| `explanationAr` | string | Yes | Arabic explanation |
| `conceptId` | string | No | Related concept |
| `needsConfidence` | boolean | No | Show confidence rating |

### match type example

```json
{
  "id": "q02",
  "type": "match",
  "prompt": "Match each word to its meaning.",
  "options": [
    "attention | a unit of text the model reads",
    "token | the mechanism that weighs earlier tokens",
    "benchmark | a measurement on real hardware"
  ],
  "answer": [
    "attention | the mechanism that weighs earlier tokens",
    "token | a unit of text the model reads",
    "benchmark | a measurement on real hardware"
  ]
}
```

---

## 9. Collocations Array

Common phrases with Arabic translations.

```json
"collocations": [
  {
    "phrase": "attention head",
    "meaningAr": "رأس الانتباه، وحدة فرعية.",
    "example": "Each attention head learns a different relation."
  }
]
```

### Collocation Properties

| Property | Type | Required | Description |
|----------|------|----------|-------------|
| `phrase` | string | Yes | English phrase |
| `meaningAr` | string | Yes | Arabic meaning |
| `example` | string | No | Example sentence |

---

## 10. Connections Array

Links to related chapters for curriculum continuity.

```json
"connections": [
  {
    "chapterId": "example-chunking",   // Target chapter ID
    "title": "Chunking by structure",   // Connection title
    "conceptIds": ["c4", "c5"],         // Shared concepts
    "note": "Next chapter covers chunking strategies."
  }
]
```

### Connection Properties

| Property | Type | Required | Description |
|----------|------|----------|-------------|
| `chapterId` | string | Yes | ID of the related chapter |
| `title` | string | Yes | Connection title (for curriculum navigation) |
| `conceptIds` | array | Yes | Shared concept IDs |
| `note` | string | No | Additional context for the connection |

---

## Validation Checklist

Before building your chapter JSON:

- [ ] `chapterId` matches `^[a-z0-9][a-z0-9-]*$`
- [ ] All 9 top-level fields present and non-empty
- [ ] At least one section, glossary term, concept, lab, figure, flashcard, and quiz item
- [ ] All IDs unique within their category (w*, c*, l*, f*, k*, q*)
- [ ] Each lab has exactly 3 tasks with prompts and checks
- [ ] `simulationNote` equals exact required string for every lab
- [ ] No external references in SVG or text nodes
- [ ] All glossary entries have both English and Arabic meanings
- [ ] Concept map nodes reference existing glossary terms via `wordIds`

Run `python scripts/validate_chapter.py your-chapter.json` to validate before building.
