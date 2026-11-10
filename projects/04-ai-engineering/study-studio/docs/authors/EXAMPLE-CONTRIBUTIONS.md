# How to Contribute New Chapters

This guide explains how to add new chapters to the Study Studio repository and get them included in the build.

---

## Quick Start for First-Timers

1. **Fork the repository** on GitHub
2. **Create a branch**: `git checkout -b feat/new-chapter-about-transformers`
3. **Write your chapter JSON** in `schema/your-chapter.json`
4. **Validate it** with `python scripts/validate_chapter.py schema/your-chapter.json`
5. **Build it** with `python scripts/build_studio.py --chapter schema/your-chapter.json --out build`
6. **Open the HTML file** offline and verify it works
7. **Create a pull request** describing your chapter

---

## Writing Your Chapter JSON

### Step 1: Create the Schema File

```bash
touch schema/new-chapter-transformers.json
```

Then populate it with content following the schema in `schema/chapter.schema.json`. Use existing chapters as templates.

### Step 2: Populate Meta Information

Start with the chapter identity:

```json
{
  "meta": {
    "chapterId": "transformer-architecture",
    "title": "Transformer Architecture",
    "subtitle": "Encoder-decoder fundamentals",
    "sourceTitle": "My AI Learning Guide",
    "sourceType": "original",
    "sourceLocator": "Chapter 5",
    "license": "CC-BY-4.0",
    "attribution": "Content created for the AI Engineer Lab.",
    "language": "en-ar",
    "estMinutes": 30,
    "conceptCount": 8
  },
```

### Step 3: Write Content Sections

Add sections with paragraphs, study aids, and bilingual explanations. See `SCHEMA-WALKTHROUGH.md` for details on each field.

Example structure:

```json
"sections": [
  {
    "id": "s1",
    "title": "Why Transformers Changed NLP",
    "order": 1,
    "level": 1,
    "paragraphs": [
      {
        "kind": "text",
        "text": "Transformers enabled parallel training...",
        "explainArabic": "أعطاها الانتباه المتوازي..."
      }
    ],
    ...
  }
],
```

### Step 4: Add Glossary Terms

Curated technical vocabulary for rich popovers:

```json
"glossary": [
  {
    "id": "w01",
    "term": "encoder",
    "ipa": "ˈɛŋkərdə",
    "meaningEn": "Processes input tokens into representations.",
    "meaningAr": "يعالج رموز الإدخال إلى تمثيلات.",
    "wordType": "noun",
    "technical": true,
    "conceptId": "c01"
  },
```

### Step 5: Build the Concept Map

Define relationships between concepts:

```json
"conceptMap": {
  "nodes": [
    {
      "id": "c01",
      "label": "Encoder",
      "kind": "core",
      "definition": "Processes inputs through self-attention.",
      "sectionId": "s1",
      "wordIds": ["w01"]
    }
  ],
  "edges": [
    { "from": "c01", "to": "c02", "relation": "feeds into" }
  ]
},
```

### Step 6: Create a Lab or Two

Add interactive simulations. Even one lab demonstrates the kind field:

```json
"labs": [
  {
    "id": "l01",
    "title": "Self-attention visualization",
    "goal": "See attention heads focusing on different relations.",
    "kind": "attention",
    "controls": [...],
    "tasks": [...],
    "takeawayEn": "Self-attention learns positional and semantic relations.",
    "takeawayAr": "الانتباه الذاتي يتعلم العلاقات الموضعية والدلالية.",
    "simulationNote": "Illustrative simulation, not real model output."
  }
],
```

### Step 7: Add Figures, Flashcards, Quiz Items

Complete the remaining arrays with content matching their schemas. See each catalog guide for examples.

### Step 8: Validate Before Building

```bash
python scripts/validate_chapter.py schema/new-chapter-transformers.json
```

Fix any errors shown in output before proceeding.

---

## Building Your Chapter

### Single Chapter Build

```bash
python scripts/build_studio.py --chapter schema/new-chapter-transformers.json --out build
```

This:
1. Validates the chapter JSON
2. Checks paragraph hashes (creates sidecar if needed)
3. Inlines CSS and JS from `engine/`
4. Writes `build/new-chapter-transformers.html`

### Batch Build All Chapters

Build all chapters in `schema/`:

```bash
python scripts/build_studio.py --schema-dir schema --out build
```

This iterates through each `.json` file in the specified directory and builds them to `build/`.

---

## Testing Your Chapter Manually

### Offline Test

1. Open `build/new-chapter-transformers.html` by double-clicking (no network)
2. Verify:
   - Content displays correctly
   - Word highlighting works with pointer movement
   - Glossary popovers open
   - Arabic explanations appear in appropriate modes
   - Figures play through steps
   - Labs initialize and respond to controls
   - Quiz items submit and score correctly
   - Flashcards flip on click

### Self-Test Mode (Optional)

If Chrome is available:

```bash
python scripts/build_studio.py --chapter schema/new-chapter-transformers.json --out build --selftest
```

This runs headless browser checks for layout shift, popover functionality, and figure narration.

---

## PR Template for Contributions

When submitting your chapter, use this structure for the PR description:

```markdown
# New Chapter: [Title]

**Summary**: Brief description of what learners will understand by reading this chapter.

**Chapter JSON**: `schema/new-chapter-transformers.json`

**Built HTML**: `build/new-chapter-transformers.html`

## What's Included

- **Concepts covered**: List of key ideas (encoder-decoder, self-attention, cross-attention)
- **Labs**: Any interactive simulations included
- **Quiz items**: Number of questions and types used
- **Estimated time**: As specified in meta.estMinutes

## Testing Checklist

- [ ] Chapter validates with `validate_chapter.py`
- [ ] All 14 verification checks pass (or `--selftest` reports success)
- [ ] Opens offline without errors
- [ ] Word highlighting causes no layout shift
- [ ] Arabic explanations appear correctly
- [ ] All figures play through steps
- [ ] Labs initialize and respond to controls

## Related Issues

References any related issues or discussions.

---

Thank you for contributing! Your chapter helps learners understand AI engineering concepts.
```

---

## Contribution Guidelines

### Content Quality Standards

- **Originality**: Prefer original content (`sourceType: "original"`) over copyrighted material
- **Accuracy**: Verify technical claims before including
- **Bilingual balance**: Ensure Arabic explanations are natural, not literal translations
- **Lab completeness**: All labs must have exactly 3 tasks with realistic checks

### File Organization

When contributing:

1. Add new chapter JSON to `schema/`
2. Build to `build/` directory (engine is shared from `engine/`)
3. Update `README.md` if adding significant new features or tracks

### Code of Conduct

Be respectful in discussions. If you spot schema errors or edge cases, open an issue rather than editing other contributors' work without permission.

---

## Common Issues and Solutions

### Error: Contract check FAILED

The chapter JSON violates the schema:

```
ERROR   required  meta.chapterId: missing
```

**Fix**: Add `chapterId` to the meta object.

### Error: paragraph X drifted from recorded hash

Your source text changed after validation but before building.

**Fix**: Either update the sidecar file or ensure you're building immediately after editing.

### Error: external reference found in figure SVG

Your SVG contains `url("https://...")` which loads an external resource.

**Fix**: Remove the URL or use an inline data URI (for simple icons only).

---

## Getting Help

If you encounter issues:

1. **Check the schema**: Open `schema/chapter.schema.json` and verify your fields match
2. **Read the catalogs**: Each feature has a catalog guide explaining its use
3. **Run validation**: `validate_chapter.py` shows errors with locations
4. **Inspect the built file**: Open in browser DevTools to see inline JSON

---

## Summary of Steps for Contributors

1. Fork and branch
2. Write chapter JSON following schema
3. Validate with `validate_chapter.py`
4. Build with `build_studio.py`
5. Manually test offline
6. Submit PR with description

Thank you for helping make Study Studio a better learning resource!
