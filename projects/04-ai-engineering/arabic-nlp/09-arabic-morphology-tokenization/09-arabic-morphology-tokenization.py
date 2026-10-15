"""
Arabic NLP — 09: Arabic Morphology, Tokenization and Surface Variation
=====================================================================
Topics: root-and-pattern morphology, proclitics and enclitics, conservative
clitic segmentation, tokenization as a retrieval decision, diacritics as
signal, dialect-vs-MSA surface variation, and a pipeline audit that emits
MOR001-MOR007 findings for misconfiguration.

Why this matters:
    An Arabic whitespace word is a fusion: proclitics and enclitics attach
    around a patterned root, short vowels are mostly unwritten, and dialects
    spell the same concept differently. Every choice at this level (segment
    or not, which normalizer, which subword vocab, which variety) is a
    retrieval decision: it changes recall, token cost, and whether a quoted
    passage can still be shown verbatim. This exercise ships the four tools
    the lecture measures with: a display-preserving normalizer, a
    conservative clitic segmenter, a tokenizer-comparison harness, and a
    config auditor whose GOOD pack must score ZERO findings while the BAD
    pack surfaces all seven planted pathologies.

Run:      python 09-arabic-morphology-tokenization.py
          python 09-arabic-morphology-tokenization.py corpus.json
"""

from __future__ import annotations

import json
import string
import sys
import unicodedata
from dataclasses import dataclass

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

NORMALIZER_VERSION = "ar-morph-norm-1.0"

# ----------------------------------------------------------------------------
# 1. Data models
# ----------------------------------------------------------------------------


@dataclass(frozen=True)
class TextSample:
    """One observed string. `raw` is the verbatim display form: it is never
    mutated by normalization or segmentation, exactly like Athar's
    Passage.original. `kind` and `variety` record what the string is for
    (lexical, citation, quranic, query) and which variety it belongs to."""

    sample_id: str
    raw: str
    kind: str  # "lexical" | "citation" | "quranic" | "query"
    variety: str  # "msa" | "classical" | "egyptian" | "levantine" | "gulf"
    note: str = ""


@dataclass(frozen=True)
class StoredText:
    """The two-text record: original (display and citation) plus the derived
    working copy, its per-word clitic segments, the normalizer version that
    produced them, and the source variety. Invariants: `original` is
    byte-identical to the observed input; re-normalizing `original` always
    reproduces `normalized`; segments re-join to `normalized`."""

    original: str
    normalized: str
    words: tuple[str, ...]
    segments: tuple[tuple[str, ...], ...]
    normalizer_version: str
    variety: str


@dataclass(frozen=True)
class Finding:
    """One pipeline misconfiguration. severity: "error" (stored data is
    destroyed or double-processed) or "warning" (silent quality loss or a
    governance gap). code: MOR001..MOR007. line: 1-based line in the
    pipeline config listing where the misconfiguration is declared."""

    severity: str
    code: str
    line: int
    message: str


@dataclass(frozen=True)
class PipelineStep:
    """One declared pipeline stage. `input_source` names what the step
    consumes ("text", "normalized text", "segmented text",
    "subword_tokens"), because stage ORDER alone cannot say whether
    segmentation runs on characters or on token ids."""

    line: int
    name: str
    input_source: str = "text"


@dataclass(frozen=True)
class PipelineConfig:
    """A pipeline as configuration, which is what the auditor inspects."""

    name: str
    steps: tuple[PipelineStep, ...]
    keep_original: bool
    tashkeel_target: str  # "working-copy" | "stored"
    stored_content: tuple[str, ...]  # content classes the index stores
    eval_gate: bool  # stemming before embedding gated by evaluation?
    dialect_sources: tuple[str, ...]  # varieties present in the corpus
    variety_decision: str | None  # documented variety policy, or None
    record_normalizer_version: bool
    fold_digits: bool


@dataclass(frozen=True)
class TokenizerSpec:
    """A candidate tokenizer. unit: "word" (whitespace, vocabulary lookup),
    "subword" (greedy longest-match over a fragment vocabulary), or "byte"
    (greedy longest-match; uncovered characters fall back to their UTF-8
    bytes, which is how a model without Arabic coverage behaves)."""

    name: str
    unit: str  # "word" | "subword" | "byte"
    vocab: frozenset[str]
    unk: str = "<unk>"

    def analyze(self, text: str) -> tuple[list[str], int, int]:
        """Return (tokens, unknown_chars, fallback_chars). unknown_chars are
        characters the vocabulary cannot represent; fallback_chars are
        characters paid for as raw UTF-8 bytes instead of vocab units."""
        tokens: list[str] = []
        unknown_chars = 0
        fallback_chars = 0
        if self.unit == "word":
            for word in text.split():
                if word in self.vocab:
                    tokens.append(word)
                else:
                    tokens.append(self.unk)
                    unknown_chars += len(word)
            return tokens, unknown_chars, fallback_chars
        for word in text.split():
            i = 0
            while i < len(word):
                matched = ""
                for j in range(len(word), i, -1):
                    piece = word[i:j]
                    if piece in self.vocab:
                        matched = piece
                        break
                if matched:
                    tokens.append(matched)
                    i += len(matched)
                elif self.unit == "byte":
                    for byte in word[i].encode("utf-8"):
                        tokens.append(f"<0x{byte:02X}>")
                    fallback_chars += 1
                    i += 1
                else:
                    tokens.append(self.unk)
                    unknown_chars += 1
                    i += 1
        return tokens, unknown_chars, fallback_chars


@dataclass(frozen=True)
class TokenizerReport:
    """One tokenizer's cost and coverage over a corpus."""

    name: str
    tokens: int
    words: int
    tokens_per_word: float
    unk_rate: float  # share of characters the vocabulary could not cover
    fallback_rate: float  # share of characters paid as UTF-8 byte tokens


# ----------------------------------------------------------------------------
# 2. Display-preserving normalization (working copy only)
# ----------------------------------------------------------------------------

_ALEF_MAP = {"أ": "ا", "إ": "ا", "آ": "ا", "ٱ": "ا"}
_ARABIC_INDIC_DIGITS = {chr(0x0660 + i): str(i) for i in range(10)}
_EXTENDED_INDIC_DIGITS = {chr(0x06F0 + i): str(i) for i in range(10)}
_DIGIT_MAP = {**_ARABIC_INDIC_DIGITS, **_EXTENDED_INDIC_DIGITS}


def strip_tashkeel(text: str) -> str:
    """Strip combining marks (fatha, damma, kasra, sukun, shadda, tanween,
    superscript alef). Only ever applied to a working copy: the display copy
    keeps tashkeel because stripping a stored Quranic or citation string is
    unrecoverable."""
    return "".join(ch for ch in text if unicodedata.category(ch) != "Mn")


def normalize_working_copy(text: str, *, fold_digits: bool = True) -> str:
    """Working-copy normalization for matching and embedding (versioned).

    The original string is never mutated: this function derives a second
    column. Rules, in order:
    - NFC first, so precomposed and decomposed inputs agree.
    - Tashkeel stripped (display copy keeps it).
    - Tatweel removed (U+0640 is decorative and often a PDF artifact).
    - Alef variants أ إ آ ٱ folded to ا.
    - Alef maqsura ى folded to ي (keys only; display keeps ى).
    - Arabic-Indic and Extended Arabic-Indic digits folded to ASCII.
    - Whitespace collapsed.
    Ta marbuta ة -> ه is deliberately NOT applied here: it is a fuzzy-only
    relaxation (see normalize_fuzzy_key), because folding it in the index
    copy merges genuinely distinct words."""
    text = unicodedata.normalize("NFC", text)
    text = strip_tashkeel(text)
    text = text.replace("ـ", "")
    for src, dst in _ALEF_MAP.items():
        text = text.replace(src, dst)
    text = text.replace("ى", "ي")
    if fold_digits:
        text = "".join(_DIGIT_MAP.get(ch, ch) for ch in text)
    return " ".join(text.split()).strip()


def normalize_fuzzy_key(text: str) -> str:
    """Relaxed candidate-generation key: the index key plus ة -> ه folding.
    Used only to GENERATE candidates (blocking, recall probes); never as the
    equality key that scores or merges them."""
    return normalize_working_copy(text).replace("ة", "ه")


# ----------------------------------------------------------------------------
# 3. Conservative clitic segmentation
# ----------------------------------------------------------------------------

CONJUNCTION = "و"
ARTICLE = "ال"
# Fused preposition + article forms: ب/ك/ف keep the article's alef; ل elides it.
_FUSED_PREPOSITIONS = ("ب", "ك", "ف")
_ELVOWEL_LAM = "لل"
_BARE_PREPOSITIONS = ("ب", "ل")  # composition rule only, never bare stripping
_MULTI_SUFFIXES = ("ها", "هم", "هن", "هما", "كم", "كن", "نا", "كما")
_SINGLE_SUFFIXES = ("ه", "ي", "ك")
_MIN_PREFIX_REST = 3  # after any prefix strip, at least 3 characters remain
_MIN_MULTI_BASE = 2  # base before a multi-char suffix must be >= 2
_MIN_SINGLE_BASE = 4  # base before a single-char suffix must be >= 4
# Lexically fused words that mimic the preposition + suffix pattern but are
# NOT split: لكن is the single word "but"; كنا ("we were") is protected by
# the single-char base rule and the bare-preposition ban alike.
_COMPOSITION_GUARD = frozenset({"لكن"})
KNOWN_CLITICS = frozenset(
    {CONJUNCTION, ARTICLE, "ب", "ك", "ل", "ف"}
    | set(_MULTI_SUFFIXES)
    | set(_SINGLE_SUFFIXES)
)


def segment_word(word: str) -> tuple[str, ...]:
    """Conservative clitic segmentation of ONE normalized (undiacritized)
    whitespace word. Rules, in order:

      R1  conjunction و  when >= 3 characters would remain
      R2  fused preposition + definite article (بال كال فال) and the elided
          lam form لل -> (ل, ال, rest), each requiring >= 3 to remain
      R3  plain definite article ال when >= 3 would remain
      R4  bare preposition ب/ل composed with a multi-char pronoun suffix
          (بها -> ب, ها), minus the fused-word guard list
      R5  one pronoun suffix: multi-char (base >= 2) before single-char
          (base >= 4), so الله, وجه, علي, موسى stay whole

    What it must NOT do: strip pattern or root material. كتب stays كتب and
    كتاب is never ك + تاب — a root is not a segment. Aggressive stemming is
    a different, evaluation-gated stage (see MOR003).

    Precision over recall by design: bare prepositions without an article
    are never stripped (كتاب must never become ك + تاب), and short-base
    suffix splits are refused (عليه and كتبه stay whole). The lecture's
    trade-off section measures what that costs."""
    rest = word
    parts: list[str] = []
    # R1: conjunction proclitic
    if rest.startswith(CONJUNCTION) and len(rest) - 1 >= _MIN_PREFIX_REST:
        parts.append(CONJUNCTION)
        rest = rest[1:]
    # R2: fused preposition + article (alef survives: بال كال فال)
    for preposition in _FUSED_PREPOSITIONS:
        if rest.startswith(preposition + ARTICLE):
            remainder = rest[len(preposition) + len(ARTICLE) :]
            if len(remainder) >= _MIN_PREFIX_REST:
                parts.extend((preposition, ARTICLE))
                rest = remainder
                break
    # R2b: elided lam article: ل + ال is written لل (alef dropped after ل)
    if rest.startswith(_ELVOWEL_LAM):
        remainder = rest[len(_ELVOWEL_LAM) :]
        if len(remainder) >= _MIN_PREFIX_REST:
            parts.extend(("ل", ARTICLE))
            rest = remainder
    # R3: plain determination article
    if rest.startswith(ARTICLE) and len(rest) - len(ARTICLE) >= _MIN_PREFIX_REST:
        parts.append(ARTICLE)
        rest = rest[len(ARTICLE) :]
    # R4: bare preposition composed with a multi-char pronoun suffix
    composed = False
    if rest in _COMPOSITION_GUARD:
        composed = False
    else:
        for preposition in _BARE_PREPOSITIONS:
            if rest.startswith(preposition) and rest[1:] in _MULTI_SUFFIXES:
                parts.extend((preposition, rest[1:]))
                rest = ""
                composed = True
                break
    # R5: one pronoun suffix, multi-char before single-char
    if not composed and rest:
        multi = next((s for s in _MULTI_SUFFIXES if rest.endswith(s)), None)
        if multi is not None and len(rest) - len(multi) >= _MIN_MULTI_BASE:
            parts.append(rest[: len(rest) - len(multi)])
            parts.append(multi)
            rest = ""
        else:
            single = next((s for s in _SINGLE_SUFFIXES if rest.endswith(s)), None)
            if single is not None and len(rest) - 1 >= _MIN_SINGLE_BASE:
                parts.append(rest[:-1])
                parts.append(single)
                rest = ""
    if rest:
        parts.append(rest)
    # Invariant: in a split, only known clitics may be short; extracted
    # stems keep >= 3 characters. An unsplit short word (مش, في, من) is a
    # complete lexical item, not an extracted stem, and passes untouched.
    if len(parts) > 1:
        for part in parts:
            if part not in KNOWN_CLITICS:
                assert len(part) >= _MIN_PREFIX_REST, (
                    f"segment {part!r} of {word!r} is neither a known clitic "
                    f"nor a >= {_MIN_PREFIX_REST}-character stem"
                )
    return tuple(parts)


def segment_text(normalized: str) -> tuple[tuple[str, ...], ...]:
    """Segment every whitespace word of a normalized working copy."""
    return tuple(segment_word(word) for word in normalized.split())


def reconstruct(segments: tuple[tuple[str, ...], ...]) -> str:
    """Re-join segmented words back into the normalized string. Exactly one
    orthographic rule is needed: the lam article elides its alef after the
    preposition ل (ل + ال -> لل). Every other clitic concatenates directly,
    so display fidelity round-trips from what was stored."""
    words: list[str] = []
    for parts in segments:
        buffer = ""
        for part in parts:
            if buffer.endswith("ل") and part == ARTICLE:
                buffer += "ل"
            else:
                buffer += part
        words.append(buffer)
    return " ".join(words)


def store_text(sample: TextSample) -> StoredText:
    """The pipeline for one sample: keep the original, derive the working
    copy, segment the working copy. The original is copied first and never
    touched again — the MOR001 property holds by construction."""
    original = sample.raw
    normalized = normalize_working_copy(original)
    segments = segment_text(normalized)
    return StoredText(
        original=original,
        normalized=normalized,
        words=tuple(normalized.split()),
        segments=segments,
        normalizer_version=NORMALIZER_VERSION,
        variety=sample.variety,
    )


# ----------------------------------------------------------------------------
# 4. Tokenizer comparison harness
# ----------------------------------------------------------------------------

_SUBWORD_UNITS = frozenset(
    {
        # clitics an Arabic-aware subword vocab keeps whole
        "و",
        "ال",
        "ب",
        "ل",
        "ف",
        "ك",
        "ها",
        "نا",
        "هم",
        "كم",
        # stems and words from the sample corpus
        "كتاب",
        "مسافر",
        "الله",
        "بسم",
        "الرحمن",
        "الرحيم",
        "الحديث",
        "حديث",
        "ايمان",
        "موسي",
        "مدرسة",
        "طبعة",
        "دار",
        "1445",
        "7",
        "مش",
        "فاضي",
        "اروح",
        "دلوقتي",
        "بعرف",
        "وين",
        "رح",
        "ما",
        "هالكتاب",
        "وايد",
        "حلو",
    }
)

# A multilingual tokenizer with no Arabic coverage: Latin units only.
_LATIN_VOCAB = frozenset(
    set(string.ascii_letters)
    | set(string.digits)
    | {"-", "'", "al", "fat", "bari", "ar", "el", "bin"}
)


def build_word_vocab(texts: list[str]) -> frozenset[str]:
    """Whitespace word types of the corpus. Built from the corpus itself so
    the baseline reports zero out-of-vocabulary; production builds the vocab
    from a training split and measures the rate on held-out text."""
    vocab: set[str] = set()
    for text in texts:
        vocab.update(text.split())
    return frozenset(vocab)


def compare_tokenizers(
    texts: list[str], specs: tuple[TokenizerSpec, ...]
) -> tuple[TokenizerReport, ...]:
    """Tokenize the same corpus under every candidate tokenizer and report
    tokens-per-word, unknown-character rate, and byte-fallback rate. This is
    the measurable check the lecture demands before choosing a tokenizer."""
    words = sum(len(text.split()) for text in texts)
    total_chars = sum(len(text) for text in texts) or 1
    reports: list[TokenizerReport] = []
    for spec in specs:
        tokens: list[str] = []
        unk_chars = 0
        fallback_chars = 0
        for text in texts:
            text_tokens, text_unk, text_fallback = spec.analyze(text)
            tokens.extend(text_tokens)
            unk_chars += text_unk
            fallback_chars += text_fallback
        reports.append(
            TokenizerReport(
                name=spec.name,
                tokens=len(tokens),
                words=words,
                tokens_per_word=round(len(tokens) / words, 2) if words else 0.0,
                unk_rate=round(unk_chars / total_chars, 3),
                fallback_rate=round(fallback_chars / total_chars, 3),
            )
        )
    return tuple(reports)


# ----------------------------------------------------------------------------
# 5. Display-fidelity check
# ----------------------------------------------------------------------------


def check_display_fidelity(samples: tuple[TextSample, ...]) -> int:
    """Prove the stored original round-trips: byte-identical to the observed
    input (tashkeel, tatweel, Arabic-Indic digits and all), re-normalizable
    to the stored working copy, and re-joinable from the stored segments.
    Returns the number of samples that round-trip; any failure raises."""
    passed = 0
    for sample in samples:
        stored = store_text(sample)
        assert stored.original == sample.raw, (
            f"{sample.sample_id}: original must round-trip byte-for-byte, "
            f"got {stored.original!r} vs {sample.raw!r}"
        )
        assert normalize_working_copy(stored.original) == stored.normalized, (
            f"{sample.sample_id}: re-normalizing the stored original must "
            f"reproduce the stored working copy"
        )
        joined = reconstruct(stored.segments)
        assert joined == stored.normalized, (
            f"{sample.sample_id}: segments must re-join to the working copy, "
            f"got {joined!r} vs {stored.normalized!r}"
        )
        assert stored.normalizer_version == NORMALIZER_VERSION
        passed += 1
    # The two properties that are unrecoverable if violated:
    quranic = next(s for s in samples if s.kind == "quranic")
    stored = store_text(quranic)
    assert any(unicodedata.category(ch) == "Mn" for ch in stored.original), (
        "stored Quranic original must keep tashkeel"
    )
    assert not any(unicodedata.category(ch) == "Mn" for ch in stored.normalized), (
        "working copy must be undiacritized"
    )
    digits = next(s for s in samples if s.sample_id == "digits-arabic-indic")
    stored = store_text(digits)
    assert "١٤٤٥" in stored.original, "stored original keeps Arabic-Indic digits"
    assert "1445" in stored.normalized, "working copy folds them to ASCII"
    return passed


# ----------------------------------------------------------------------------
# 6. Pipeline configuration and audit (MOR001-MOR007)
# ----------------------------------------------------------------------------

RULE_CATALOG: tuple[tuple[str, str, str], ...] = (
    ("MOR001", "error", "normalizer destroys the display form (original not retained)"),
    (
        "MOR002",
        "error",
        "tashkeel stripped from a stored Quranic/citation string rather than a working copy",
    ),
    (
        "MOR003",
        "warning",
        "aggressive stemming applied before embedding with no evaluation gate",
    ),
    (
        "MOR004",
        "warning",
        "mixed dialect sources indexed without an explicit variety decision",
    ),
    ("MOR005", "warning", "normalizer version not recorded with the index"),
    (
        "MOR006",
        "error",
        "segmentation applied to text already subword-tokenized (double segmentation)",
    ),
    ("MOR007", "warning", "digits not folded so ١٤٤٥ and 1445 never match"),
)


def _step_line(config: PipelineConfig, name: str) -> int:
    lines = [s.line for s in config.steps if s.name == name]
    return min(lines) if lines else 0


def _first_step(config: PipelineConfig, name: str) -> PipelineStep | None:
    matching = [s for s in config.steps if s.name == name]
    return min(matching, key=lambda s: s.line) if matching else None


def audit(config: PipelineConfig) -> list[Finding]:
    """Inspect a pipeline configuration and emit one Finding per violated
    rule. Severity policy: "error" means stored data was destroyed or a
    stage double-processed it (unrecoverable without re-ingestion);
    "warning" means silent quality loss or a governance gap (recoverable,
    but it must be visible)."""
    findings: list[Finding] = []

    # MOR001: the display form must survive normalization.
    if not config.keep_original:
        findings.append(
            Finding(
                "error",
                "MOR001",
                _step_line(config, "normalize"),
                "normalizer overwrites the stored original; the display form "
                "is destroyed and no downstream stage can show the source verbatim",
            )
        )

    # MOR002: tashkeel may be stripped only for a working copy, never from a
    # stored Quranic or citation string (stripping a stored ayah is unrecoverable).
    if config.tashkeel_target == "stored" and set(config.stored_content) & {
        "quranic",
        "citation",
    }:
        offending = sorted(set(config.stored_content) & {"quranic", "citation"})
        findings.append(
            Finding(
                "error",
                "MOR002",
                _step_line(config, "normalize"),
                f"tashkeel stripped from stored {', '.join(offending)} content "
                f"(sample: {QURANIC_SAMPLE_ID}); the original reading cannot be "
                f"reconstructed from the index",
            )
        )

    # MOR003: stemming before embedding is allowed only behind an evaluation gate.
    stem_step = _first_step(config, "stem")
    embed_line = _step_line(config, "embed")
    if (
        stem_step is not None
        and embed_line
        and stem_step.line < embed_line
        and not config.eval_gate
    ):
        findings.append(
            Finding(
                "warning",
                "MOR003",
                stem_step.line,
                f"aggressive stem feeds embedding (stem line {stem_step.line} < "
                f"embed line {embed_line}) with no evaluation gate; meaning the "
                f"model needs may be destroyed (كتب/كُتُب/كِتَاب collapse)",
            )
        )

    # MOR004: one variety decision must exist whenever the corpus mixes varieties.
    if len(set(config.dialect_sources)) > 1 and not config.variety_decision:
        sources = ", ".join(sorted(set(config.dialect_sources)))
        findings.append(
            Finding(
                "warning",
                "MOR004",
                _step_line(config, "index"),
                f"corpus mixes varieties ({sources}) but no variety decision is "
                f"recorded; MSA-heavy and dialect queries cannot both be tuned",
            )
        )

    # MOR005: normalized keys are meaningless without the rules that made them.
    if not config.record_normalizer_version:
        findings.append(
            Finding(
                "warning",
                "MOR005",
                _step_line(config, "index"),
                f"index stores keys without normalizer version {NORMALIZER_VERSION}; "
                f"a rule change would silently mix incomparable key generations",
            )
        )

    # MOR006: clitic segmentation consumes text, not WordPiece/BPE ids.
    segment_step = _first_step(config, "segment")
    if segment_step is not None and segment_step.input_source == "subword_tokens":
        findings.append(
            Finding(
                "error",
                "MOR006",
                segment_step.line,
                "clitic segmenter consumes subword tokens from an earlier stage; "
                "segmenting token ids is double segmentation and splits the "
                "model's own vocabulary units",
            )
        )

    # MOR007: fold digits so Arabic-Indic and ASCII numerals compare equal.
    if not config.fold_digits:
        unfolded = normalize_working_copy("١٤٤٥", fold_digits=False)
        folded = normalize_working_copy("١٤٤٥")
        findings.append(
            Finding(
                "warning",
                "MOR007",
                _step_line(config, "normalize"),
                f"digits not folded: {unfolded!r} never equals {folded!r}, so "
                f"edition, page, and year fields silently never match",
            )
        )
    return findings


# ----------------------------------------------------------------------------
# 7. Sample corpus (exercises every normalizer and segmenter rule)
# ----------------------------------------------------------------------------

QURANIC_SAMPLE_ID = "quranic"

SAMPLES: tuple[TextSample, ...] = (
    TextSample(
        "alef-hamza-1",
        "كتاب الايمان",
        "lexical",
        "msa",
        "bare alef spelling of the title",
    ),
    TextSample(
        "alef-hamza-2",
        "كتاب الإيمان",
        "lexical",
        "msa",
        "hamza-on-ya spelling of the same title",
    ),
    TextSample(
        "alef-madda",
        "آية الكتاب",
        "lexical",
        "msa",
        "madda alef folds to bare alef in the key only",
    ),
    TextSample(
        "maqsura",
        "موسى",
        "lexical",
        "msa",
        "final alef maqsura; key folds ى to ي while display keeps ى",
    ),
    TextSample(
        "teh-marbuta",
        "مدرسة",
        "lexical",
        "msa",
        "ta marbuta; never folded in the index copy",
    ),
    TextSample(
        "teh-marbuta-fuzzy",
        "مدرسه",
        "lexical",
        "msa",
        "ha spelling that stays distinct in the index copy",
    ),
    TextSample(
        "tatweel",
        "كــتاب",
        "lexical",
        "msa",
        "U+0640 tatweel artifact as PDF extraction emits it",
    ),
    TextSample(
        "digits-arabic-indic",
        "طبعة دار الحديث ١٤٤٥",
        "citation",
        "msa",
        "Arabic-Indic digits in an edition line",
    ),
    TextSample(
        "digits-ascii",
        "طبعة دار الحديث 1445",
        "citation",
        "msa",
        "ASCII spelling of the same edition line",
    ),
    TextSample(
        "quranic",
        "بِسْمِ ٱللَّهِ ٱلرَّحْمَٰنِ ٱلرَّحِيمِ",
        "quranic",
        "classical",
        "full tashkeel; stripping a stored copy would be unrecoverable",
    ),
    TextSample(
        "dialect-egyptian",
        "مش فاضي أروح دلوقتي",
        "query",
        "egyptian",
        "negation مش, future أروح, adverb دلوقتي",
    ),
    TextSample(
        "dialect-levantine",
        "ما بعرف وين رح أروح",
        "query",
        "levantine",
        "negation ما, future رح",
    ),
    TextSample(
        "dialect-gulf",
        "هالكتاب وايد حلو",
        "query",
        "gulf",
        "demonstrative+article هال, intensifier وايد",
    ),
    TextSample(
        "arabizi-query",
        "fat7 al-bari",
        "query",
        "msa",
        "Arabizi transliteration: 7 stands for ح (query-time variant)",
    ),
    TextSample(
        "clitic-chain",
        "وكتابها",
        "lexical",
        "msa",
        "conjunction + noun + pronoun suffix",
    ),
    TextSample(
        "clitic-article-chain",
        "والكتابها",
        "lexical",
        "msa",
        "conjunction + determination + noun + pronoun suffix",
    ),
    TextSample(
        "clitic-lam",
        "للمسافر",
        "lexical",
        "msa",
        "preposition ل + definite article with elided alef",
    ),
    TextSample(
        "clitic-bi",
        "بالكتاب",
        "lexical",
        "msa",
        "preposition ب + definite article",
    ),
)


# ----------------------------------------------------------------------------
# 8. BAD and GOOD pipeline configurations
# ----------------------------------------------------------------------------

# BAD pack: every planted pathology, one finding per rule.
# - normalize overwrites the stored original (MOR001)
# - tashkeel stripped from stored quranic/citation content (MOR002)
# - subword_tokenize runs first, then the segmenter eats token ids (MOR006)
# - aggressive stem feeds embedding with no evaluation gate (MOR003)
# - index drops the normalizer version (MOR005)
# - five varieties indexed with no variety decision (MOR004)
# - digits left unfolded (MOR007)
BAD_PIPELINE = PipelineConfig(
    name="BAD",
    steps=(
        PipelineStep(11, "load"),
        PipelineStep(13, "normalize"),
        PipelineStep(15, "subword_tokenize"),
        PipelineStep(17, "segment", "subword_tokens"),
        PipelineStep(19, "stem"),
        PipelineStep(21, "embed"),
        PipelineStep(23, "index"),
    ),
    keep_original=False,
    tashkeel_target="stored",
    stored_content=("quranic", "citation", "lexical"),
    eval_gate=False,
    dialect_sources=("msa", "classical", "egyptian", "levantine", "gulf"),
    variety_decision=None,
    record_normalizer_version=False,
    fold_digits=False,
)

# GOOD pack: the same corpus, governed. Must produce ZERO findings.
# - original kept; tashkeel stripped from the working copy only
# - embed runs on normalized text; no stem upstream of it
# - the model's subword tokenizer runs on normalized text, not on segments
# - clitic segmentation and the gated stem serve the lexical arm only
# - index records the normalizer version and folds digits
# - varieties mixed, but with an explicit documented variety decision
GOOD_PIPELINE = PipelineConfig(
    name="GOOD",
    steps=(
        PipelineStep(11, "load"),
        PipelineStep(13, "normalize"),
        PipelineStep(15, "embed"),
        PipelineStep(17, "subword_tokenize"),
        PipelineStep(19, "segment", "normalized text"),
        PipelineStep(21, "stem", "segmented text"),
        PipelineStep(23, "index"),
    ),
    keep_original=True,
    tashkeel_target="working-copy",
    stored_content=("quranic", "citation", "lexical"),
    eval_gate=True,
    dialect_sources=("msa", "classical", "egyptian", "levantine", "gulf"),
    variety_decision=(
        "ar-morph-variety-1.0: every passage is stamped with its source "
        "variety; queries default to msa+classical, dialect queries route "
        "through the documented expansion map; sources never mix silently"
    ),
    record_normalizer_version=True,
    fold_digits=True,
)


# ----------------------------------------------------------------------------
# 9. Self-checks
# ----------------------------------------------------------------------------


def check_normalizer() -> None:
    """The variant pairs the lecture promises this normalizer handles, plus
    the two it refuses (ta marbuta folding, diacritic loss in the original)."""
    # Alef variants unify in the working copy.
    assert normalize_working_copy("كتاب الإيمان") == normalize_working_copy(
        "كتاب الايمان"
    )
    assert normalize_working_copy("آية") == normalize_working_copy("اية")
    assert normalize_working_copy("ٱلله") == normalize_working_copy("الله")
    # Alef maqsura folds to ya in keys; display keeps the observed spelling.
    assert normalize_working_copy("موسى") == normalize_working_copy("موسي")
    # Tatweel (U+0640) is decorative and often a PDF artifact.
    assert normalize_working_copy("كــتاب") == normalize_working_copy("كتاب")
    # Digits fold in both scripts.
    assert normalize_working_copy("١٤٤٥") == normalize_working_copy("1445")
    assert normalize_working_copy("۱۴۴۵") == normalize_working_copy("1445")
    assert normalize_working_copy("١٤٤٥", fold_digits=False) != normalize_working_copy(
        "1445"
    )
    # Tashkeel is stripped from the working copy only.
    assert normalize_working_copy("محمَّد") == normalize_working_copy("محمد")
    # NFC: decomposed and precomposed hamza-alef agree.
    assert normalize_working_copy("ا" + "́") == normalize_working_copy("ا")
    assert normalize_working_copy("ا" + "́") == normalize_working_copy("أ")
    # Ta marbuta: NEVER folded in the index copy, only in fuzzy keys.
    assert normalize_working_copy("مدرسة") != normalize_working_copy("مدرسه")
    assert normalize_fuzzy_key("مدرسة") == normalize_fuzzy_key("مدرسه")
    # The Quranic probe: idempotent, and tashkeel gone from the working copy.
    probe = "بِسْمِ ٱللَّهِ ٱلرَّحْمَٰنِ ٱلرَّحِيمِ"
    assert normalize_working_copy(probe) == "بسم الله الرحمن الرحيم"
    assert normalize_working_copy(
        normalize_working_copy(probe)
    ) == normalize_working_copy(probe)


def check_segmenter() -> None:
    """The clitic chains, the guards, and the promise that a root is never
    split into segments."""
    # Clitic chains split into their morphemes.
    assert segment_word("وكتابها") == ("و", "كتاب", "ها")
    assert segment_word("والكتابها") == ("و", "ال", "كتاب", "ها")
    assert segment_word("وبالكتابها") == ("و", "ب", "ال", "كتاب", "ها")
    assert segment_word("بالكتاب") == ("ب", "ال", "كتاب")
    assert segment_word("فالكتاب") == ("ف", "ال", "كتاب")
    assert segment_word("للمسافر") == ("ل", "ال", "مسافر")
    assert segment_word("الكتاب") == ("ال", "كتاب")
    assert segment_word("كتابها") == ("كتاب", "ها")
    assert segment_word("علمهم") == ("علم", "هم")
    assert segment_word("بها") == ("ب", "ها")
    assert segment_word("ولنا") == ("و", "ل", "نا")
    # Guards: the article must not eat الله, and short bases stay whole.
    assert segment_word("الله") == ("الله",)
    assert segment_word("وجه") == ("وجه",)
    assert segment_word("علي") == ("علي",)
    assert segment_word("موسي") == ("موسي",)  # normalized موسى
    assert segment_word("لكن") == ("لكن",)  # fused-word guard
    # A root is not a segment; bare prepositions never strip (كتاب !~ ك + تاب).
    assert segment_word("كتب") == ("كتب",)
    assert segment_word("كتاب") == ("كتاب",)
    assert segment_word("بكتاب") == ("بكتاب",)
    # Losslessness on every sample word.
    for sample in SAMPLES:
        stored = store_text(sample)
        assert reconstruct(stored.segments) == stored.normalized, sample.sample_id
        for parts in stored.segments:
            # Unsplit short words are whole lexical items; the stem-length
            # rule applies only to parts extracted by a split.
            if len(parts) == 1:
                continue
            for part in parts:
                if part not in KNOWN_CLITICS:
                    assert len(part) >= _MIN_PREFIX_REST, (sample.sample_id, part)


def check_display_fidelity_round() -> None:
    check_display_fidelity(SAMPLES)


# ----------------------------------------------------------------------------
# 10. Demo helpers
# ----------------------------------------------------------------------------


def print_examples() -> None:
    print("=== working copy vs stored original ===")
    for sample_id in ("quranic", "digits-arabic-indic", "tatweel", "alef-hamza-2"):
        sample = next(s for s in SAMPLES if s.sample_id == sample_id)
        stored = store_text(sample)
        print(f"  {sample_id}: {stored.original!r}")
        print(f"    -> working copy: {stored.normalized!r}")
    print("=== conservative segmentation (normalized words) ===")
    for word in ("وكتابها", "والكتابها", "بالكتاب", "للمسافر", "الله", "كتب"):
        parts = " | ".join(segment_word(word))
        print(f"  {word} -> {parts}")
    print("=== sample corpus ===")
    varieties = sorted({s.variety for s in SAMPLES})
    print(f"  {len(SAMPLES)} samples; varieties: {', '.join(varieties)}")
    fidelity = check_display_fidelity(SAMPLES)
    print(f"  display fidelity: {fidelity}/{len(SAMPLES)} samples round-trip")


def run_pack(config: PipelineConfig) -> list[Finding]:
    findings = audit(config)
    print(f"=== {config.name} pack: pipeline audit ===")
    for finding in findings:
        print(
            f"  [{finding.severity}] {finding.code} line {finding.line}: {finding.message}"
        )
    errors = sum(1 for f in findings if f.severity == "error")
    warnings = len(findings) - errors
    print(f"  findings: {len(findings)} (errors: {errors}, warnings: {warnings})")
    if config.name == "GOOD" and not findings:
        print("GOOD pack clean")
    return findings


def print_tokenizer_report(texts: list[str]) -> None:
    word_vocab = build_word_vocab(texts)
    specs = (
        TokenizerSpec("word-whitespace", "word", word_vocab),
        TokenizerSpec("subword-greedy", "subword", _SUBWORD_UNITS),
        TokenizerSpec("byte-fallback", "byte", _LATIN_VOCAB),
    )
    reports = compare_tokenizers(texts, specs)
    words = sum(len(text.split()) for text in texts)
    print(f"=== tokenizer comparison over {len(texts)} texts ({words} words) ===")
    print(
        f"  {'tokenizer':<18}{'tokens':>8}{'tok/word':>10}"
        f"{'unk chars':>11}{'byte chars':>12}"
    )
    for report in reports:
        print(
            f"  {report.name:<18}{report.tokens:>8}{report.tokens_per_word:>10}"
            f"{report.unk_rate:>11.1%}{report.fallback_rate:>12.1%}"
        )
    print("  unk chars: characters the vocabulary cannot cover;")
    print("  byte chars: characters paid as raw UTF-8 bytes (2 per Arabic letter)")


# ----------------------------------------------------------------------------
# 11. External corpus loader (Windows-BOM tolerant)
# ----------------------------------------------------------------------------


def load_texts(path: str) -> list[str]:
    """Load texts from a JSON array, a {"texts": [...]} object, or JSONL.
    utf-8-sig so files saved by Windows tools with a BOM still parse."""
    with open(path, encoding="utf-8-sig") as handle:
        raw = handle.read().strip()
    if not raw:
        raise ValueError(f"empty corpus file: {path}")
    try:
        data = json.loads(raw)
    except json.JSONDecodeError:
        data = [json.loads(line) for line in raw.splitlines() if line.strip()]
    if isinstance(data, dict):
        data = data.get("texts", [])
    texts: list[str] = []
    for entry in data:
        if isinstance(entry, str):
            texts.append(entry)
        elif isinstance(entry, dict):
            value = entry.get("text") or entry.get("original")
            if not isinstance(value, str):
                raise ValueError(f"corpus entry has no text/original field: {entry!r}")
            texts.append(value)
        else:
            raise ValueError(f"unsupported corpus entry: {entry!r}")
    if not texts:
        raise ValueError(f"no texts in corpus file: {path}")
    return texts


def run_corpus_file(path: str) -> int:
    texts = load_texts(path)
    print(f"=== corpus file: {path} ({len(texts)} texts, BOM-tolerant load) ===")
    passed = 0
    for i, text in enumerate(texts):
        normalized = normalize_working_copy(text)
        segments = segment_text(normalized)
        if (
            reconstruct(segments) == normalized
            and normalize_working_copy(text) == normalized
        ):
            passed += 1
        else:
            print(f"  [error] text {i}: display-fidelity round-trip failed")
    print(f"  display fidelity: {passed}/{len(texts)} texts round-trip")
    print_tokenizer_report([normalize_working_copy(t) for t in texts])
    return 0 if passed == len(texts) else 1


# ----------------------------------------------------------------------------
# 12. Demo and self-checks
# ----------------------------------------------------------------------------


def main(argv: list[str]) -> int:
    if len(argv) > 1:
        return run_corpus_file(argv[1])
    check_normalizer()
    check_segmenter()
    check_display_fidelity_round()
    print_examples()
    print()
    bad_findings = run_pack(BAD_PIPELINE)
    print()
    good_findings = run_pack(GOOD_PIPELINE)
    assert sorted(f.code for f in bad_findings) == sorted(
        code for code, _, _ in RULE_CATALOG
    ), (
        f"BAD pack must surface all seven rules, got {sorted(f.code for f in bad_findings)}"
    )
    assert len(bad_findings) == len(RULE_CATALOG), (
        f"BAD pack must emit exactly one finding per rule, got {len(bad_findings)}"
    )
    assert good_findings == [], (
        f"GOOD pack must produce zero findings, got {good_findings}"
    )
    print()
    print_tokenizer_report([store_text(s).normalized for s in SAMPLES])
    print()
    print("all self-checks passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
