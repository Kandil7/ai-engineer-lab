# Quiz Catalog

This catalog documents all supported quiz types in the Study Studio. Each type specifies the data shape, scoring logic, and examples for creating your own questions.

---

## Quiz Structure Overview

Every quiz item shares this structure:

```json
{
  "id": "q01",                           // Unique question identifier
  "type": "<quiz-type>",                 // See valid types below
  "prompt": "Question text",             // Displayed to the learner
  "options": [...],                      // Answer options (type-dependent)
  "answer": [...],                       // Correct answer(s)
  "answerText": "...",                   // Human-readable answer (for fill-code)
  "explanationEn": "English explanation.",
  "explanationAr": "Arabic explanation."
}
```

### Type-Dependent Fields

| Quiz Type | Has options? | Answer Format | needs explanation arrays? |
|-----------|-------------|---------------|--------------------------|
| **mcq** | Yes (4 recommended) | Array of correct option texts | Yes |
| **true-false** | Yes (2) | `["True"]` or `["False"]` | Yes |
| **order** | No (array of options to reorder) | Ordered array of all options | Yes |
| **match** | Yes (pairs of "left\|right") | Array of correct pair strings | Yes |
| **fill-code** | No (single answer text) | String or array with code line | Optional `answerText` |
| **spot-mistake** | Yes (options explaining the error) | Text explaining what's wrong | Yes |
| **explain** | No (free response) | Array of key phrases to include | Yes |

---

## 1. mcq (Multiple Choice Question)

Standard multiple choice with 4 options recommended.

### Data Shape

```json
{
  "id": "q01",
  "type": "mcq",
  "prompt": "What does attention do?",
  "options": [
    "It scores every earlier token against the current one.",
    "It predicts the next token directly.",
    "It compresses the input into a single number.",
    "It removes irrelevant context."
  ],
  "answer": ["It scores every earlier token against the current one."],
  "explanationEn": "Attention computes scores, normalizes them to weights, and mixes tokens.",
  "explanationAr": "الانتباه يحسب الدرجات، يعيد تكييفها إلى أوزان، ويمزج الرموز."
}
```

### Scoring Logic

- Single choice: Only the exact answer text matches as correct
- Multiple choices allowed: Array with all correct answers
- All options must be strings with non-empty content
- Best practice: Include one clearly correct and 3 plausible distractors

### Example Variations

#### Single Correct Answer
```json
{
  "type": "mcq",
  "prompt": "Which word is a noun?",
  "options": ["run", "quickly", "apple", "beautiful"],
  "answer": ["apple"],
  "explanationEn": "'Apple' names a thing, making it a noun.",
  "explanationAr": "'Apple' اسم لشيء، لذا هو مفرد."
}
```

#### Multiple Correct Answers (Less Common)
```json
{
  "type": "mcq",
  "prompt": "Select all sentences that end with a period.",
  "options": [
    "The sky is blue.",
    "What do you want?",
    "Run fast!",
    "I love learning."
  ],
  "answer": ["The sky is blue.", "I love learning."],
  "explanationEn": "Declarative sentences end with periods.",
  "explanationAr": "الجملة الخبرية تنتهي بنقطة."
}
```

---

## 2. true-false

Two-option question for concept verification.

### Data Shape

```json
{
  "id": "q02",
  "type": "true-false",
  "prompt": "Attention work grows quadratically with context length.",
  "options": ["True", "False"],
  "answer": ["True"],
  "explanationEn": "Doubling the input roughly quadruples attention comparisons.",
  "explanationAr": "تضاعف الإدخال يربّع عدد المقارنات تقريبًا."
}
```

### Scoring Logic

- Either `["True"]` or `["False"]` can be the correct answer
- Both options are typically required for clarity
- Consider using exact capitalization: "True" not "true"

### Example Variations

#### Scientific Fact
```json
{
  "type": "true-false",
  "prompt": "The softmax function outputs values that sum to one.",
  "options": ["True", "False"],
  "answer": ["True"],
  "explanationEn": "Softmax normalizes scores into a probability distribution.",
  "explanationAr": "الsoftmax يعيد تكييف الدرجات لتوزع احتمالي مجموعها واحد."
}
```

#### Conceptual Misconception
```json
{
  "type": "true-false",
  "prompt": "All words in a paragraph are equally important.",
  "options": ["True", "False"],
  "answer": ["False"],
  "explanationEn": "Attention lets the model focus on relevant words.",
  "explanationAr": "الانتباه يركز على الكلمات ذات الصلة فقط."
}
```

---

## 3. order (Reorder Items)

Learners arrange items into the correct sequence.

### Data Shape

```json
{
  "id": "q03",
  "type": "order",
  "prompt": "Put the attention steps in the order they run.",
  "options": ["Score: compare tokens.", "Weight: normalize scores.", "Mix: blend tokens."],
  "answer": ["Score: compare tokens.", "Weight: normalize scores.", "Mix: blend tokens."],
  "explanationEn": "Score produces raw comparisons, weight normalizes them to probabilities, mix combines weighted tokens.",
  "explanationAr": "الدرجة ثم الوزن ثم الخلط."
}
```

### Scoring Logic

- All options must be in the exact order specified in `answer`
- No partial credit; all items must be correctly ordered
- Best for procedural knowledge with a fixed sequence

### Example Variations

#### Chronological Order
```json
{
  "type": "order",
  "prompt": "Arrange these events in chronological order.",
  "options": [
    "Tokenization splits text into IDs.",
    "Model reads tokens sequentially.",
    "Attention weights select relevant context."
  ],
  "answer": [
    "Tokenization splits text into IDs.",
    "Model reads tokens sequentially.",
    "Attention weights select relevant context."
  ],
  "explanationEn": "Text must be tokenized before the model can process it, then attention runs after reading.",
  "explanationAr": "يجب توكن النص قبل المعالجة، ثم الانتباه بعد القراءة."
}
```

#### Process Flow
```json
{
  "type": "order",
  "prompt": "Order the RAG pipeline stages.",
  "options": [
    "User submits a question.",
    "Retrieval finds relevant chunks.",
    "Reranking selects the best chunks.",
    "Generation answers the question."
  ],
  "answer": [
    "User submits a question.",
    "Retrieval finds relevant chunks.",
    "Reranking selects the best chunks.",
    "Generation answers the question."
  ],
  "explanationEn": "The RAG pipeline flows from user input through retrieval to generation.",
  "explanationAr": "خطوة المستخدم، ثم الاسترجاع، ثم الترتيب، ثم الإجابة."
}
```

---

## 4. match (Matching Pairs)

Learners match items from two columns into correct pairs.

### Data Shape

```json
{
  "id": "q04",
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
  ],
  "explanationEn": "Attention is the mechanism, token is the unit, benchmark is the measurement.",
  "explanationAr": "attention آلية، token وحدة، benchmark قياس."
}
```

### Scoring Logic

- `options`: Left column items as "left\|right" pairs (any order)
- `answer`: Correct pairings with left item first
- Each option string contains both parts separated by `|`
- Learners drag left items to correct right items

### Example Variations

#### Technical Terms Matching
```json
{
  "type": "match",
  "prompt": "Match each concept to its definition.",
  "options": [
    "embedding | vector representation of text",
    "context window | tokens the model can see",
    "hallucination | made-up information"
  ],
  "answer": [
    "embedding | vector representation of text",
    "context window | tokens the model can see",
    "hallucination | made-up information"
  ],
  "explanationEn": "Embeddings encode meaning in vectors, context limits what's visible, hallucinations are fabrications.",
  "explanationAr": "المضمّنات ترمز المعنى، السياق يحدّ النطاق، الهلوسة إخبار كاذب."
}
```

#### Phrase Matching
```json
{
  "type": "match",
  "prompt": "Match each phrase with its antonym.",
  "options": [
    "fast | slow",
    "hot | cold",
    "gain | loss"
  ],
  "answer": [
    "fast | slow",
    "hot | cold",
    "gain | loss"
  ],
  "explanationEn": "These are opposite pairs of concepts.",
  "explanationAr": "هذه أزواج متضادة."
}
```

---

## 5. fill-code (Code Completion)

Learners complete a code snippet with the correct implementation.

### Data Shape

```json
{
  "id": "q05",
  "type": "fill-code",
  "prompt": "Complete the function to compute attention pairs.",
  "options": ["return n * (n - 1) // 2"],
  "answerText": "n * (n - 1) / 2",
  "explanationEn": "Each token compares with every earlier token, giving n*(n-1)/2 comparisons total.",
  "explanationAr": "كل رمز يقارن بكل رمز سابق، فالإجمالي n(n-1)/2."
}
```

### Scoring Logic

- `options` can be a single string or array of alternatives
- Exact string match required (whitespace-sensitive)
- `answerText`: Human-readable version for display to the learner
- Useful for testing algorithmic understanding

### Example Variations

#### Multiple Valid Implementations
```json
{
  "type": "fill-code",
  "prompt": "Add parentheses to group the denominator.",
  "options": [
    "return n * (n - 1) / (2)",
    "return n * (n - 1) // 2"
  ],
  "answerText": "n * (n - 1) / 2",
  "explanationEn": "Python accepts both integer division and floating-point.",
  "explanationAr": "بايثون تقبل القسمة الصحيحة والعشرية."
}
```

#### Bug Fixing
```json
{
  "type": "fill-code",
  "prompt": "Fix the off-by-one error in this loop.",
  "options": ["for i in range(n - 1)"],
  "answerText": "range(n - 1)",
  "explanationEn": "The last token has no earlier token to compare against.",
  "explanationAr": "الآخر لا يقارن مع أي سابق."
}
```

---

## 6. spot-mistake (Error Identification)

Learners identify what's wrong in a statement or code.

### Data Shape

```json
{
  "id": "q06",
  "type": "spot-mistake",
  "prompt": "A reviewer says: 'This benchmark shows attention costs 12 million operations.' Find the problem.",
  "options": [
    "Nothing is wrong, benchmarks are always better than arithmetic",
    "The function computes the pair count, so it is arithmetic and not a measured benchmark",
    "The count should be divided by two",
    "The function ignores the model size"
  ],
  "answer": [
    "The function computes the pair count, so it is arithmetic and not a measured benchmark"
  ],
  "explanationEn": "A formula shows the shape of the curve. Only measuring your own stack gives a real number.",
  "explanationAr": "المعادلة تُظهر الشكل فقط، والرقم الحقيقي يأتي من القياس."
}
```

### Scoring Logic

- Options present plausible-sounding but incorrect explanations
- Answer is the statement identifying what's wrong and why
- Tests critical thinking and concept understanding

### Example Variations

#### Misleading Claim
```json
{
  "type": "spot-mistake",
  "prompt": "'Adding more context tokens always improves accuracy.' What's missing?",
  "options": [
    "More context always helps, so this is correct.",
    "Too much context can confuse the model and increase cost.",
    "The claim only applies to smaller models."
  ],
  "answer": [
    "Too much context can confuse the model and increase cost."
  ],
  "explanationEn": "Quadratic growth means very long contexts become unaffordable and may hurt accuracy.",
  "explanationAr": "التربيع يجعل السياقات الطويلة باهظة وقد تضر الدقة."
}
```

#### Code Bug
```json
{
  "type": "spot-mistake",
  "prompt": "'This attention layer computes softmax over all tokens.' What's the issue?",
  "options": [
    "Softmax is applied to every attention head.",
    "The softmax should be over the key dimensions, not value dimensions.",
    "This is correct for a standard self-attention implementation."
  ],
  "answer": [
    "The softmax should be over the key dimensions, not value dimensions."
  ],
  "explanationEn": "Attention scores are computed by comparing queries to keys, then normalized over that axis.",
  "explanationAr": "الsoftmax يوحّد الدرجات على محور المفاتيح."
}
```

---

## 7. explain (Free Response Checklist)

Learners explain a concept; their answer is checked against key phrases.

### Data Shape

```json
{
  "id": "q07",
  "type": "explain",
  "prompt": "In your own words, why does attention cost grow quadratically?",
  "answer": [
    "Every token attends to every earlier token",
    "So the comparison count is n times n minus one over two",
    "That growth means context must be managed, not maximised"
  ],
  "answerText": "Explain in your own words.",
  "explanationEn": "Look for two parts: the n squared count, and the consequence that context must be managed rather than maximized.",
  "explanationAr": "ابحث عن جزأين: عدّ n²، وأن السياق يجب أن يُدار لا أن يُكبَّر."
}
```

### Scoring Logic

- `answer`: Array of key phrases or concepts that should appear
- Learners type their own explanation
- Engine checks if all key phrases are present in the response
- Tests understanding and ability to articulate concepts

### Example Variations

#### Concept Definition
```json
{
  "type": "explain",
  "prompt": "Explain what an embedding is.",
  "answer": [
    "A vector representation",
    "Of a word or token",
    "In a high-dimensional space"
  ],
  "answerText": "Describe embeddings in your own words.",
  "explanationEn": "Embeddings are dense vectors that capture semantic meaning.",
  "explanationAr": "المضمّنات متجهات كثيفة ترمز المعنى الدلالي."
}
```

#### Process Description
```json
{
  "type": "explain",
  "prompt": "Describe how the RAG pipeline works.",
  "answer": [
    "User asks a question",
    "Retrieval finds relevant documents",
    "Generation uses retrieved context to answer"
  ],
  "answerText": "Explain the RAG process step by step.",
  "explanationEn": "RAG retrieves information before generating an answer, combining retrieval with generation.",
  "explanationAr": "RAG يسترجع معلومات قبل الإجابة، يجمع بين الاسترجاع والإنتاج."
}
```

---

## Best Practices for Quiz Writing

### Question Design

- **Clarity**: State the question in simple, direct language
- **Distractors**: Make wrong answers plausible but clearly incorrect
- **Scope**: Keep each question focused on one concept
- **Difficulty**: Mix easy (true-false) with harder (order, match) questions

### Answer Writing

- **Explanations**: Always provide both English and Arabic explanations
- **Accuracy**: Ensure explanations are technically correct
- **Language balance**: Don't make one language's explanation significantly longer

### Cultural Adaptation

When writing for Arabic-speaking audiences:

- Use familiar terminology or provide glossary cross-references
- Consider examples relevant to learners' contexts
- Test with native speakers when possible

### Answer Length Guidelines

| Type | Option Count | Recommended |
|------|-------------|-------------|
| mcq | 3-5 | 4 options (1 correct, 3 plausible) |
| true-false | 2 | Always include both |
| order | Variable | 2-6 items to reorder |
| match | Pairs | 3-6 pairs (more is harder) |
| fill-code | 1-3 alternatives | Provide 1-2 alternative correct forms if applicable |
| spot-mistake | 3-4 | 1 correct, 2-3 plausible misconceptions |
| explain | Free response | Array of 2-5 key phrases |

---

## Quiz Types Summary

| Type | Learner Action | Tests | Best For |
|------|----------------|-------|----------|
| mcq | Select one option from list | Recognition | Concept verification, vocabulary |
| true-false | Judge statement as T/F | Basic understanding | Quick concept checks |
| order | Reorder items | Procedural knowledge | Steps, sequences, pipelines |
| match | Pair left with right | Association | Definitions, concepts, translations |
| fill-code | Complete code snippet | Implementation | Syntax, algorithms, patterns |
| spot-mistake | Identify error and explain | Critical thinking | Misconceptions, debugging |
| explain | Write explanation and key points | Articulation | Concept mastery, understanding |

---

## Example: Full Quiz Array

A complete quiz section with varied question types:

```json
{
  "quiz": [
    {
      "id": "q01",
      "type": "mcq",
      "prompt": "What does attention do?",
      "options": [
        "It scores every earlier token against the current one.",
        "It predicts the next token directly.",
        "It compresses the input into a single number."
      ],
      "answer": ["It scores every earlier token against the current one."],
      "explanationEn": "Attention computes scores, normalizes to weights, and mixes.",
      "explanationAr": "الانتباه يحسب الدرجات، يعيد تكييفها إلى أوزان، ويمزج الرموز."
    },
    {
      "id": "q02",
      "type": "true-false",
      "prompt": "Doubling input quadruples attention work.",
      "options": ["True", "False"],
      "answer": ["True"],
      "explanationEn": "Attention is quadratic in context length.",
      "explanationAr": "الانتباه تربيعي في طول السياق."
    },
    {
      "id": "q03",
      "type": "order",
      "prompt": "Order the attention steps.",
      "options": ["Score", "Weight", "Mix"],
      "answer": ["Score", "Weight", "Mix"],
      "explanationEn": "Score computes, Weight normalizes, Mix combines.",
      "explanationAr": "الدرجة تحسب، الوزن يعيد تكييف، الخلط يدمج."
    },
    {
      "id": "q04",
      "type": "match",
      "prompt": "Match words to meanings.",
      "options": [
        "attention | a scoring mechanism",
        "token | text unit",
        "weight | scaled contribution"
      ],
      "answer": [
        "attention | a scoring mechanism",
        "token | text unit",
        "weight | scaled contribution"
      ],
      "explanationEn": "Attention scores, tokens are units, weights scale contributions.",
      "explanationAr": "الانتباه يحسب الدرجات، التوكن وحدة النص، الوزن يقيّم المساهمة."
    }
  ]
}
```
