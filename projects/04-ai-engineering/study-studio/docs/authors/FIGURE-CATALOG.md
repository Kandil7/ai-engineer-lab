# Figure Catalog: Inline SVG Guidelines

This guide explains how to create inline SVG figures for the Study Studio. Inline SVG keeps your chapter as a single file without external image dependencies.

---

## Overview

Figures in Study Studio are:
- **Inline SVG**: Written directly in JSON as a string
- **No external references**: No `url()` with http/https, no `<img src>`
- **Semantic elements**: Use `<rect>`, `<circle>`, `<path>` for hotspots
- **Step-based narration**: Play through animations with English/Arabic commentary

### SVG Rules Checklist

Before adding a figure to your chapter:

- [ ] SVG markup is contained in a single string (no newlines that break JSON)
- No `url("...")` referencing external images or fonts
- No `<script>` elements inside the SVG
- All shapes are closed (`<path>` with complete d attribute, not open paths)
- Element IDs assigned to components you want to highlight
- Hotspot targets match element IDs in the SVG

---

## Figure Structure

```json
{
  "id": "f01",                                   // Unique figure identifier
  "title": "Figure title for display",           // Shown above the figure
  "svg": "<svg ...>",                            // Inline SVG markup
  "captionEn": "English caption below figure",   // Caption in English
  "captionAr": "Arabic caption below figure",    // Caption in Arabic
  "steps": [                                     // Step-by-step narration
    {
      "narrativeEn": "Step one explanation.",
      "narrativeAr": "شرح الخطوة الأولى.",
      "highlight": ["f01-element-id"]            // IDs to highlight
    }
  ],
  "hotspots": [                                  // Interactive annotations
    {
      "target": "f01-element-id",                // SVG element ID
      "what": "What this component does.",
      "inputs": "Input data or signals.",
      "outputs": "Output results.",
      "mistakes": "Common mistakes with this component."
    }
  ],
  "buildOrder": ["f01-step1", "f01-step2"]      // Correct assembly order (optional)
}
```

---

## SVG Best Practices

### Element ID Naming

Assign IDs to elements you want to highlight or annotate:

- Use the figure ID as prefix: `"f01-query-box"`, `"f01-key-distribution"`
- Keep IDs short but descriptive
- Avoid special characters except hyphens and underscores
- Don't reuse IDs within the same SVG

### Element Types

| Element | Use Case | Example |
|---------|----------|---------|
| `<rect>` | Boxes, containers | `"x=\"10\" y=\"10\" width=\"100\" height=\"50\" id=\"f01-box\""` |
| `<circle>` | Circular nodes, dots | `r=\"10\" id=\"f01-node\"` |
| `<path>` | Freeform shapes, curved lines | `d=\"M10 10 L100 100 Z\" id=\"f01-triangle\"` |
| `<text>` | Labels inside shapes | Use for annotations (not hotspots) |
| `<line>` | Connections, arrows | `x1=\"10\" y1=\"10\" x2=\"100\" y2=\"100\" id=\"f01-arrow\"` |

### Closing Shapes

All paths and polygons must be closed:

**Correct (closed path):**
```xml
<path d="M10 10 L100 10 L100 100 L10 100 Z" id="f01-box"/>
// Z closes the path back to the starting point
```

**Incorrect (open path):**
```xml
<path d="M10 10 L100 10 L100 100"> <!-- Missing closing segment -->
```

Open paths won't validate in strict SVG parsers.

---

## Example Figures

### 1. Score-Weight-Mix Cycle

Simple three-box flow diagram:

```json
{
  "id": "f01",
  "title": "The attention step cycle",
  "svg": "<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 640 200' role='img' aria-label='Score weight mix cycle'><rect width='640' height='200' fill='#f7f7f4'/><g font-family='Segoe UI, Helvetica, Arial, sans-serif' fill='#1c1f26'><rect id='f01-s' x='30' y='60' width='160' height='70' rx='10' fill='#2a78d6'/><text x='110' y='102' font-size='20' fill='#ffffff' text-anchor='middle'>Score</text><rect id='f01-w' x='240' y='60' width='160' height='70' rx='10' fill='#7b5ea7'/><text x='320' y='102' font-size='20' fill='#ffffff' text-anchor='middle'>Weight</text><rect id='f01-m' x='450' y='60' width='160' height='70' rx='10' fill='#1f9d76'/><text x='530' y='102' font-size='20' fill='#ffffff' text-anchor='middle'>Mix</text><path id='f01-e1' d='M190 95 L238 95' stroke='#9196a0' stroke-width='3' marker-end='url(#f01-arrow)'/><path id='f01-e2' d='M400 95 L448 95' stroke='#9196a0' stroke-width='3' marker-end='url(#f01-arrow)'/><text x='320' y='168' font-size='14' fill='#555a66' text-anchor='middle'>one attention step</text><defs><marker id='f01-arrow' markerWidth='8' markerHeight='8' refX='6' refY='4' orient='auto'><path d='M0 0 L8 4 L0 8 z' fill='#9196a0'/></marker></defs></g></svg>",
  "captionEn": "One attention step runs score, weight, and mix in sequence.",
  "captionAr": "خطوة الانتباه تمر بالدرجة، الوزن، والخلط بالتتابع.",
  "steps": [
    {
      "narrativeEn": "Score: compare the current token against every earlier token.",
      "narrativeAr": "الدرجة: قارن الرمز الحالي بكل رمز سابق.",
      "highlight": ["f01-s"]
    },
    {
      "narrativeEn": "Weight: normalize the scores so they sum to one.",
      "narrativeAr": "الوزن: وحّد الدرجات بحيث يكون مجموعها واحدًا.",
      "highlight": ["f01-w"]
    },
    {
      "narrativeEn": "Mix: blend earlier tokens into the current representation.",
      "narrativeAr": "الخلط: امزج الرموز السابقة داخل تمثيل الرمز الحالي.",
      "highlight": ["f01-m"]
    }
  ],
  "hotspots": [
    {
      "target": "f01-s",
      "what": "Compares the current token's query vector against every earlier key vector.",
      "inputs": "Current token, all earlier tokens.",
      "outputs": "One raw score per earlier token.",
      "mistakes": "Treating a high score as a high probability of appearing in the answer."
    },
    {
      "target": "f01-w",
      "what": "Turns raw scores into weights that sum to one across earlier tokens.",
      "inputs": "Raw scores.",
      "outputs": "A weight per earlier token.",
      "mistakes": "Reading a weight as a share of the final answer."
    },
    {
      "target": "f01-m",
      "what": "Combines earlier token values into the current token's representation.",
      "inputs": "Weights and earlier token values.",
      "outputs": "The enriched current representation.",
      "mistakes": "Forgetting that the same weights are reused by later layers."
    }
  ],
  "buildOrder": ["f01-s", "f01-w", "f01-m"]
}
```

### 2. Transformer Architecture

Encoder-decoder architecture with attention flows:

```json
{
  "id": "f02",
  "title": "Transformer encoder-decoder",
  "svg": "<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 800 400'><rect width='800' height='400' fill='#fafafa'/><g font-family='system-ui, sans-serif' fill='#333'><text x='20' y='30' font-size='18'>Input tokens</text><rect id='f02-inputs' x='30' y='50' width='140' height='300' rx='5' stroke='#666' stroke-width='2'/><g id='f02-encoders'><line x1='70' y1='100' x2='680' y2='100' stroke='#ccc' stroke-dasharray='4'/><line x1='70' y1='150' x2='680' y2='150' stroke='#ccc' stroke-dasharray='4'/><line x1='70' y1='200' x2='680' y2='200' stroke='#ccc' stroke-dasharray='4'/></g><rect id='f02-encoder' x='320' y='50' width='160' height='300' rx='10' fill='#dfe6e9'/><text x='400' y='205' font-size='20' text-anchor='middle'>Encoder</text><rect id='f02-decoder' x='510' y='50' width='160' height='300' rx='10' fill='#74b9ff'/><text x='590' y='205' font-size='20' text-anchor='middle'>Decoder</text><path id='f02-ea' d='M530 130 L460 130' stroke='#e17055' stroke-width='2'/><path id='f02-da' d='M530 180 L460 180' stroke='#e17055' stroke-width='2'/><path id='f02-ae' d='M420 130 L490 130' stroke='#e17055' stroke-width='2'/><path id='f02-de' d='M420 180 L490 180' stroke='#e17055' stroke-width='2'/><path id='f02-aa' d='M460 130 L490 130' stroke='#e17055' stroke-width='2'/><path id='f02-dd' d='M460 180 L490 180' stroke='#e17055' stroke-width='2'/></g><text x='400' y='380' font-size='14' text-anchor='middle'>Self-attention flows and cross-attention between encoder-decoder</text></svg>",
  "captionEn": "Encoder processes inputs, decoder attends to encoded representations.",
  "captionAr": "المشفر يعالج المدخلات، المشفر يتبع التمثيلات المشفرة.",
  "steps": [
    {
      "narrativeEn": "Input tokens pass through the encoder stack.",
      "narrativeAr": "رموز الإدخال تمر عبر تكدس المشفر.",
      "highlight": ["f02-inputs", "f02-encoders"]
    },
    {
      "narrativeEn": "Encoder self-attention attends over input positions.",
      "narrativeAr": "انتباه المشفر للانتباه على مواقع الإدخال.",
      "highlight": ["f02-encoder"]
    },
    {
      "narrativeEn": "Decoder attends to encoder outputs via cross-attention.",
      "narrativeAr": "المشفر يتبع مخرجات المشفر عبر الانتباه المشترك.",
      "highlight": ["f02-decoder", "f02-ea", "f02-da", "f02-ae", "f02-de"]
    }
  ],
  "hotspots": [
    {
      "target": "f02-inputs",
      "what": "Input token embeddings before encoding.",
      "inputs": "Raw text tokenized and embedded.",
      "outputs": "Encoded representations for attention.",
      "mistakes": "Treating embeddings as the final representation."
    },
    {
      "target": "f02-encoder",
      "what": "Encoder stack with self-attention layers.",
      "inputs": "Input token positions.",
      "outputs": "Encoded position representations.",
      "mistakes": "Confusing encoder attention with cross-attention."
    },
    {
      "target": "f02-decoder",
      "what": "Decoder stack generating output tokens.",
      "inputs": "Encoder outputs via cross-attention, causal mask for autoregression.",
      "outputs": "Generated token sequence.",
      "mistakes": "Ignoring the causal mask that prevents looking ahead."
    }
  ],
  "buildOrder": []
}
```

---

## Animation Considerations

Study Studio figures support step-by-step narration. When creating animations:

### Highlight Elements

Use the `highlight` array in each step to specify which elements light up:

```json
"steps": [
  {
    "narrativeEn": "Step one.",
    "narrativeAr": "الخطوة الأولى.",
    "highlight": ["f01-element-a", "f01-element-b"] // Multiple highlights allowed
  }
]
```

### Animated Packets (Optional)

For more advanced figures, animate "packets" flowing along edges using `offset-path`:

```xml
<circle r="3" fill="#0984e3">
  <animateMotion dur="2s" repeatCount="indefinite" path="M10 10 L100 100"/>
</circle>
```

**Note**: Animated elements must not trigger layout shifts. Use `transform` animations only.

---

## Hotspot Writing Guide

Each hotspot should describe a component in detail:

### what

What the component does in one sentence:

```json
"what": "Compares queries to keys to compute attention scores."
```

### inputs

What data or signals enter this component:

```json
"inputs": "Query vectors from current token and key vectors from all earlier tokens."
```

### outputs

What the component produces:

```json
"outputs": "A vector of raw attention scores, one per earlier token."
```

### mistakes

Common misconceptions or errors learners make:

```json
"mistakes": "Treating a high score as probability without softmax normalization."
```

---

## Build Order (Optional)

Use `buildOrder` for interactive assembly exercises:

```json
"buildOrder": ["f01-s", "f01-w", "f01-m"]
```

This enables the learner to drag components into the correct sequence. Leave empty if not used.

---

## Accessibility Considerations

- Include `role="img"` and `aria-label` on the SVG root
- Use semantic elements (`<rect>`, `<circle>`) rather than decorative shapes alone
- Add `title` attributes to text elements for screen readers
- Ensure captions are meaningful in both languages

---

## Summary Checklist for Figure Authors

Before adding a figure:

- [ ] SVG is valid (no unclosed paths, proper syntax)
- No external URLs referenced (`url(http://...)`, `@import`)
- Element IDs unique within the SVG and match hotspot targets
- Each step has both English and Arabic narration
- Hotspot descriptions complete (what, inputs, outputs, mistakes)
- Build order specified if enabling interactive assembly

Example minimal figure (validate first with an external SVG checker):

```json
{
  "id": "f03",
  "title": "Simple two-box diagram",
  "svg": "<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 400 150'><rect width='400' height='150' fill='#fff'/><rect id='f03-a' x='50' y='50' width='100' height='50' rx='5' fill='#a2d9ff'/><text x='100' y='80' text-anchor='middle'>Input</text><rect id='f03-b' x='250' y='50' width='100' height='50' rx='5' fill='#74b9ff'/><text x='300' y='80' text-anchor='middle'>Output</text></svg>",
  "captionEn": "Input flows to output through the model.",
  "captionAr": "الإدخال يمر عبر النموذج إلى المخرج.",
  "steps": [
    {
      "narrativeEn": "Input enters the model.",
      "narrativeAr": "الإدخال يدخل النموذج.",
      "highlight": ["f03-a"]
    },
    {
      "narrativeEn": "Output emerges from the model.",
      "narrativeAr": "المخرج ينتهي من النموذج.",
      "highlight": ["f03-b"]
    }
  ],
  "hotspots": [
    {
      "target": "f03-a",
      "what": "Input data for the model.",
      "inputs": "Tokenized text or vectors.",
      "outputs": "Model representation.",
      "mistakes": "Assuming input is already encoded."
    },
    {
      "target": "f03-b",
      "what": "Output from the model.",
      "inputs": "Model's internal state.",
      "outputs": "Token prediction or probability distribution.",
      "mistakes": "Treating output as deterministic rather than probabilistic."
    }
  ],
  "buildOrder": []
}
```
