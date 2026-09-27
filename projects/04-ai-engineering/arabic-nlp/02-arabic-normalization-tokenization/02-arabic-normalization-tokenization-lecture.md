# Arabic NLP 02: Normalization and Tokenization

## 🎯 Topic Overview

Normalization decides what "the same" means in Arabic, and tokenization
decides what the index can match. Get normalization wrong and the index
splits one word into many variants; get tokenization wrong and morphology
fragments recall. This lecture covers the normalization pipeline (diacritics,
hamza, tatweel, punctuation), the tokenization options from whitespace to
morphological analyzers, and how to measure the choice instead of guessing.

## 📚 Learning Objectives

By the end of this lecture, you will be able to:

1. Build a normalization pipeline: strip diacritics, unify hamza forms, remove tatweel
2. Explain why hamza normalization matters and which forms to unify
3. Choose a tokenization strategy from whitespace to morphological analysis
4. Measure tokenization quality with recall on a small labeled set
5. Keep the original text intact while normalizing only the search side

---

## 1. The Normalization Pipeline

```python
import unicodedata


def normalize_arabic(text: str) -> str:
    text = unicodedata.normalize("NFD", text)
    text = "".join(c for c in text if unicodedata.category(c) != "Mn")  # diacritics
    text = unicodedata.normalize("NFC", text)
    text = text.replace("\u0640", "")  # tatweel (ـ)
    text = text.replace("أ", "ا").replace("إ", "ا").replace("آ", "ا")  # hamza on alif
    text = text.replace("ؤ", "و").replace("ئ", "ي")  # hamza on waw/ya
    return text
```

The pipeline is order-sensitive: decompose first, strip combining marks,
recompose, then unify hamza forms and remove tatweel. Each step is a
deliberate choice with a recall consequence — document why each is present.

## 2. Hamza Normalization

Hamza (ء) sits on carriers: أ إ آ ؤ ئ. A query with "أ" must match text with
"ا" or "إ". Unifying all hamza-on-alif forms to bare alif is the standard
trade: it gains recall and loses the ability to distinguish أ vs ا — a loss
that matters only in specific domains (proper names, Quranic text). Decide
per corpus and record the decision.

## 3. Tokenization Options

| Strategy | What it does | Recall | Cost |
|---|---|---|---|
| Whitespace split | Splits on spaces | Low (morphology fragments) | Free |
| Prefix/suffix stripping | Removes common affixes (ال، و، ب) | Medium | Cheap |
| Light stemming | Reduces words to roots | High | Medium |
| Morphological analyzer | Full root+pattern analysis | Highest | Expensive, language-specific |

Whitespace is the default that fails Arabic. Light stemming (strip the
definite article ال and common prefixes) is the pragmatic middle ground for
most corpora. Full morphological analysis is powerful but needs a mature
tool and careful error handling.

## 4. Measuring the Choice

Never pick a tokenizer by taste. Build a small labeled set of query-to-passage
pairs, run each strategy, and compare recall@k. The exercise does exactly
this on a tiny corpus so the protocol is muscle memory. A tokenizer that
gains 5pp recall on your corpus is worth its complexity; one that gains
nothing is not.

## 5. The Two-Text Discipline Applied

Normalization and tokenization operate only on the `searchable` text. The
`original` text stays verbatim for display and citation. This is the same
discipline from topic 01, now with the full pipeline attached to the search
side.

## Common Mistakes

- Normalizing the display text (breaks quotes).
- Applying hamza normalization to a corpus where it loses meaning (Quranic text).
- Choosing a tokenizer without measuring recall.
- Forgetting the pipeline order (strip before recompose).

## Key Takeaways

1. Normalization is an ordered, documented pipeline.
2. Hamza unification is a recall-vs-precision trade, decided per corpus.
3. Tokenization choices are measured, not assumed.
4. Normalize the search text; never the quote.