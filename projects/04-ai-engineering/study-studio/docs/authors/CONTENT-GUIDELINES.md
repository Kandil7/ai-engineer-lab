# Content Guidelines for Study Studio Chapters

This guide explains how to write content that preserves the integrity of your source material while adding study aids. Follow these rules to keep your chapters accurate, compliant, and engaging.

---

## 1. Text Integrity Rules

### Rule 1: Never Reword Source Text

**Why:** A chapter is a textbook. Rewording changes the author's voice, loses nuance, and risks introducing errors. Study aids sit beside the text, not inside it.

**Do this:**
```json
"paragraphs": [
  {
    "kind": "text",
    "text": "The exact text from your source document.", // Verbatim
    "explainArabic": "نفس النص بالضبط مع الشرح العربي." // Added study aid
  }
]
```

**Don't do this:**
```json
"paragraphs": [
  {
    "kind": "text",
    "text": "The model reads tokens and weights attention. // Reworded! ❌",
    ...
  }
]
```

### Rule 2: Keep Paragraph Boundaries

Preserve paragraph breaks from the source. Each `<section>.paragraphs[]` element corresponds to one visual paragraph.

**Example:**
```json
"sections": [
  {
    "id": "s1",
    "title": "Introduction",
    "paragraphs": [
      { "kind": "text", "text": "First paragraph text." },
      { "kind": "text", "text": "Second paragraph text." } // Not merged into one long string
    ]
  }
]
```

### Rule 3: Preserve Code Blocks Exactly

Code blocks must match your source exactly. Add language hints (`code`, `language`), but never modify the code itself.

```json
{
  "kind": "code",
  "language": "python",
  "text": "def attention(n):\n    return n * n" // Exact copy from source
}
```

### Rule 4: Keep Formula Text Separate

Mathematical formulas use the `formula` kind with optional symbol definitions.

```json
{
  "kind": "formula",
  "text": "pairs(n) = n(n-1)/2",
  "symbols": [
    { "symbol": "n", "meaning": "number of tokens" },
    { "symbol": "pairs(n)", "meaning": "comparison count" }
  ]
}
```

---

## 2. Study Aid Badging

### Rule: All Derived Content Is AI-Badged

**Why:** Learners must distinguish between your source text and generated explanations. Badging builds trust.

**Where to badge:**
- Arabic explanations: `explainArabic` field (automatically badged)
- Glossary meanings: In popover, not in main text
- Quiz items: Generated questions are marked with AI badge in UI
- Lab instructions: Simulation tasks are study aids
- Figure captions: Narration is derived content

**Not badged:**
- Source paragraph text
- Original code blocks
- Your own writing (original chapter content)

```json
"studyAid": {
  "whyItMatters": "This explains why attention matters for RAG.",
  "badge": "AI" // Automatically rendered as badge in UI
}
```

---

## 3. Language Mode Rules

### Rule: Arabic Is Meaning, Not Translation

**Why:** Literal translations of technical prose sound unnatural. Arabic explanations should convey the same idea, not word-for-word translate sentences.

**Do this:**
```json
{
  "text": "The attention mechanism weights earlier tokens for context.",
  "explainArabic": "الانتباه يعطي رموز سابقة أوزانًا للسياق." // Same idea, natural Arabic
}
```

**Don't do this:**
```json
"explainArabic": "آلية الانتباه تزن الرموز السابقة لـ... context = سياق" // Literal ❌
```

### Rule: Keep English and Code LTR

English text uses `dir="ltr"`. Arabic explanations use `dir="rtl"` with `lang="ar"`. Mixed lines wrap Arabic fragments in `<bdi>` to prevent reordering.

**Example of mixed content:**
```json
{
  "text": "See the <mark data-id=\"w01\">attention</mark> mechanism.",
  "explainArabic": "انظر للآلية" // Wraps naturally in BIDI container
}
```

---

## 4. Lab Writing Rules

### Rule: Labs Are Simulations, Not Measurements

**Why:** Every lab is a teaching tool, not a production system. Be clear about this.

**Required field:**
```json
"simulationNote": "Illustrative simulation, not real model output." // Exact string
```

This exact note appears in the lab UI to prevent learners from mistaking simulated results for measured data.

### Rule: Use Exact Disclaimer String

Never modify `simulationNote`. The validator rejects any chapter with a different string.

**Invalid examples:**
- `"This is just a simulation."` → Rejected
- `"Illustrative simulation, not real model output!"` → Rejected (extra punctuation)
- `"Illustrative simulation, not real model output"` → Missing period ❌

---

## 5. Quiz Writing Rules

### Rule: Provide Both Language Explanations

Every quiz item must have `explanationEn` and `explanationAr`. These are derived content and are AI-badged in the UI.

```json
{
  "type": "mcq",
  "prompt": "What is attention?",
  "options": ["It weighs tokens", "It predicts next token", "It compresses text"],
  "answer": ["It weighs tokens"],
  "explanationEn": "Attention computes scores between tokens.",
  "explanationAr": "الانتباه يحسب درجات بين الرموز."
}
```

### Rule: Answer Format Varies by Type

- **mcq/true-false**: Array with correct option text(s)
- **order**: Ordered array of all options (no partial credit)
- **match**: Array of "left | right" pair strings
- **fill-code**: String or array with correct code line(s)
- **spot-mistake**: Single string explaining the mistake
- **explain**: Array of key phrases to include in answer

---

## 6. Glossary Writing Rules

### Rule: Provide Both Language Meanings

Every glossary entry needs `meaningEn` and `meaningAr`. The Arabic is a definition, not a translation of the example sentence.

```json
{
  "id": "w01",
  "term": "attention",
  "ipa": "əˈtɛnʃən",
  "meaningEn": "The mechanism that weighs earlier tokens.",
  "meaningAr": "آلية الترجيح بين الرموز السابقة.",
  "wordType": "noun"
}
```

### Rule: IPA Is Optional

Not every term needs an IPA pronunciation. Omit the `ipa` field if you don't have a reliable transcription. The schema allows it to be absent.

---

## 7. Figure Writing Rules

### Rule: Inline SVG Only

No external image files. Write SVG markup directly in the JSON. This keeps your chapter as a single file.

**Do this:**
```json
{
  "id": "f01",
  "svg": "<svg xmlns=\"...\" viewBox=\"0 0 400 200\"><rect id=\"s1\" .../></svg>",
  ...
}
```

**Don't do this:**
- Reference `<img src="diagram.png">` → External reference, build fails
- Use `url("https://example.com/icon.svg")` → Loads external resource, build fails

### Rule: Hotspot Descriptions Are Complete

Each hotspot must explain what the component does, its inputs and outputs, and common mistakes.

```json
{
  "hotspots": [
    {
      "target": "f01-query-box",
      "what": "The query vector selects which keys to attend to.",
      "inputs": "Query vector from current token.",
      "outputs": "Raw attention scores before softmax.",
      "mistakes": "Treating a high score as high probability without normalization."
    }
  ]
}
```

---

## 8. Best Practices Summary

### Do's

- ✅ Write natural Arabic explanations, not literal translations
- ✅ Keep source text verbatim with study aids beside it
- ✅ Include `explainArabic` for paragraphs needing clarification
- ✅ Badge all derived content in the UI (automatic via schema)
- ✅ Provide complete hotspot descriptions for figures
- ✅ Use both languages for all definitions and explanations

### Don'ts

- ❌ Reword source paragraphs to simplify or clarify
- ❌ Omit `explainArabic` from paragraphs that need it
- ❌ Modify code blocks from the source
- ❌ Use external image URLs in SVG or text
- ❌ Make quiz explanations language-imbalanced
- ❌ Omit the exact `simulationNote` string in labs

---

## 9. Example: Complete Section with Study Aids

```json
{
  "id": "s1",
  "title": "Why Attention Matters",
  "order": 1,
  "level": 1,
  "paragraphs": [
    {
      "kind": "text",
      "text": "A language model reads one token at a time. When it sees the word bank, it cannot know yet whether the next word will be river or account.",
      "explainArabic": "الموديل يقرأ رمزًا واحدًا في كل مرة. عند رؤية كلمة bank لا يعرف إذا كان التالي river أم account."
    },
    {
      "kind": "text",
      "text": "Every earlier token stays available, but the model must decide which ones matter for the next prediction.",
      "explainArabic": "كل رمز سابق متاح، لكن الموديل يجب أن يختار أيهم يهم للتنبؤ التالي."
    }
  ],
  "keySentences": [
    "The model must decide which tokens matter.",
    "Attention helps with this selection."
  ],
  "takeaways": [
    "Without attention, the model treats all context equally.",
    "Attention lets the model focus on what matters."
  ],
  "studyAid": {
    "whyItMatters": "Retrieval quality in RAG is about the same question: which parts of the input deserve weight?",
    "badge": "AI"
  },
  "confusion": {
    "simpleEnglish": "The model gives bigger votes to words that matter.",
    "simpleArabic": "الموديل يعطي كلمات مهمة صوتًا أكبر.",
    "analogy": "A librarian who highlights the relevant books in a stack."
  },
  "prediction": {
    "question": "If we add more tokens, does attention work harder?",
    "answer": "Yes; quadratic growth means doubling input quadruples the work."
  },
  "wordIds": ["w01", "w02"]
}
```

This section demonstrates:
- Verbatim source text in `paragraphs[].text`
- Arabic explanations added without rewording English
- Study aid badge on why attention matters for retrieval
- Simplified explanation for learners who need it
- Predictive question to prepare for later content
- Glossary term references via `wordIds`

---

## 10. Review Checklist

Before building your chapter, verify:

- [ ] No source text has been rewritten or summarized in place
- [ ] All paragraphs with Arabic explanations have `explainArabic`
- [ ] All glossary entries have both English and Arabic meanings
- [ ] All quiz items have both language explanations
- [ ] All labs have the exact `simulationNote` string
- [ ] No external URLs appear in SVG or text nodes
- [ ] Code blocks match source exactly
- [ ] Formula text is separate from surrounding prose

Run validation before building:

```bash
python scripts/validate_chapter.py schema/your-chapter.json
```

A valid chapter exits with code 0. Errors are printed with their location and message.
